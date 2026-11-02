"""Build/export Skelly in factory-startup background Blender with an explicit exporter.

No package installation or saved preferences. Uses the official versioned VRM
exporter and humanoid APIs [@vrmAddon4103].
"""
from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path
import sys
import tempfile

import bpy
import numpy as np
from mathutils import Matrix, Quaternion, Vector


def load_exporter(path: Path):
    spec = importlib.util.spec_from_file_location('io_scene_vrm', path / '__init__.py',
                                                 submodule_search_locations=[str(path)])
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    if tuple(module.bl_info['version']) != (4, 10, 3):
        raise ValueError('This export tool is validated against VRM Add-on 4.10.3')
    module.register()
    # The factory-startup process needs an in-memory preference instance. It is
    # never saved, and this script never installs files in a Blender user folder.
    bpy.context.preferences.use_preferences_save = False
    bpy.context.preferences.addons.new().module = spec.name
    return module


def build_avatar(payload: dict):
    for obj in list(bpy.data.objects):
        bpy.data.objects.remove(obj, do_unlink=True)
    rest = {bone['name']: bone for bone in payload['bones']}
    points, faces, material_ids, groups = [], [], [], {}
    for part in payload['artwork']['parts']:
        name = part['name']
        triangles = np.asarray(part['indices']).reshape(-1, 3)
        used, remapped = np.unique(triangles, return_inverse=True)
        local = np.asarray(part['positions']).reshape(-1, 3)[used]
        rotation = np.asarray(Quaternion(rest[name]['orientation']).to_matrix())
        world = local @ rotation.T * rest[name]['artworkScaleMeters'] + rest[name]['fittedOriginMeters']
        base = len(points)
        groups[name] = list(range(base, base + len(world)))
        points.extend(world.tolist())
        faces.extend((remapped.reshape(-1, 3) + base).tolist())
        material_ids.extend(part['faceMaterials'])
    points = np.asarray(points)
    # Presentation placement: put the artwork's soles at the ground plane.
    # This common translation changes neither anatomy nor any relative pose.
    floor_offset = -float(points[:, 2].min())
    points[:, 2] += floor_offset
    origin_shift = Vector((0, 0, floor_offset))
    armature = bpy.data.objects.new('Skelly', bpy.data.armatures.new('Skelly'))
    bpy.context.collection.objects.link(armature)
    bpy.context.view_layer.objects.active = armature
    armature.select_set(True)
    bpy.ops.object.mode_set(mode='EDIT')
    # Blender bone +Y displays the Forge segment +Z axis; retain full roll.
    bone_axis = Matrix(((1, 0, 0), (0, 0, -1), (0, 1, 0))).to_4x4()
    for item in payload['bones']:
        bone = armature.data.edit_bones.new(item['name'])
        position = Vector(item['fittedOriginMeters']) + origin_shift
        orientation = Quaternion(item['orientation']).to_matrix()
        if payload.get('vrmVersion') == '1.0':
            # VRM0 freezes rest rotations itself. For VRM1, normalize only the
            # presentation rig: cancel the assembly orientation and glTF's bone
            # basis change [@blenderGltfJointExport]. World surfaces/heads stay
            # unchanged; source rest orientations remain in the input manifest.
            orientation = Matrix(payload['coordinateBindings']['exporterInputFromSource']).transposed()
        bone.matrix = Matrix.Translation(position) @ orientation.to_4x4() @ bone_axis
        bone.length = max(item['fittedLengthMeters'], .001)
    for item in payload['bones']:
        parent = payload['avatarParents'][item['name']]
        if parent:
            armature.data.edit_bones[item['name']].parent = armature.data.edit_bones[parent]
    bpy.ops.object.mode_set(mode='OBJECT')
    mesh = bpy.data.meshes.new('Skelly artwork')
    mesh.from_pydata(points.tolist(), [], faces)
    mesh.update()
    body = bpy.data.objects.new('Skelly artwork', mesh)
    bpy.context.collection.objects.link(body)
    body.parent = armature
    for definition in payload['artwork']['materials']:
        material = bpy.data.materials.new(definition['name'])
        material.use_nodes = True
        principled = material.node_tree.nodes.get('Principled BSDF')
        for name, value in definition['inputs'].items():
            if name in principled.inputs:
                principled.inputs[name].default_value = value
        material.diffuse_color = definition['inputs']['Base Color']
        mesh.materials.append(material)
    for polygon, material_id in zip(mesh.polygons, material_ids, strict=True):
        polygon.material_index = material_id
    for name, vertices in groups.items():
        body.vertex_groups.new(name=name).add(vertices, 1, 'REPLACE')
    modifier = body.modifiers.new('Forge rigid segment binding', 'ARMATURE')
    modifier.object = armature
    body.select_set(True)
    # Rotate the complete presentation assembly into the official exporter's
    # VRM0 authoring-facing convention. Source geometry/rest data stay canonical.
    armature.matrix_world = Matrix(payload['coordinateBindings']['exporterInputFromSource']).to_4x4()
    bpy.context.view_layer.update()
    return armature, body, groups, floor_offset


def verify_articulation(armature, body, groups, humanoid):
    """Exercise every mapped body/finger joint against exact skin transforms."""
    indices = [vertices[len(vertices) // 2] for vertices in groups.values()]
    names = list(groups)
    max_error = 0.
    moved = []
    for source in humanoid.values():
        pose = armature.pose.bones[source]
        pose.rotation_mode = 'QUATERNION'
        pose.rotation_quaternion = Quaternion(Vector((1, .3, .2)).normalized(), .23)
        bpy.context.view_layer.update()
        evaluated = body.evaluated_get(bpy.context.evaluated_depsgraph_get())
        expected_movement = 0.
        for name, index in zip(names, indices, strict=True):
            base = body.data.vertices[index].co
            transform = armature.pose.bones[name].matrix @ armature.data.bones[name].matrix_local.inverted()
            expected = transform @ base
            actual = evaluated.data.vertices[index].co
            max_error = max(max_error, (actual - expected).length)
            expected_movement = max(expected_movement, (expected - base).length)
        if expected_movement <= 1e-6:
            raise ValueError(f'Humanoid bone does not drive artwork: {source}')
        moved.append(source)
        pose.rotation_quaternion = Quaternion()
        bpy.context.view_layer.update()
    if max_error > 2e-6:
        raise ValueError(f'Rigid skin transform mismatch: {max_error} m')
    return dict(testedBones=moved, maximumSkinErrorMeters=max_error)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=Path, required=True)
    parser.add_argument('--exporter', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args(sys.argv[sys.argv.index('--') + 1:])
    scratch = args.output.resolve().parent / 'tmp'
    scratch.mkdir(parents=True, exist_ok=True)
    tempfile.tempdir = str(scratch)
    payload = json.loads(args.input.read_text(encoding='utf-8'))
    asset_policy = json.loads((Path(__file__).resolve().parents[1] /
        'freemocap_blender_addon/assets/skelly_asset.json').read_text(encoding='utf-8'))
    exporter = load_exporter(args.exporter.resolve())
    bpy.context.preferences.filepaths.file_preview_type = 'NONE'
    bpy.context.preferences.filepaths.save_version = 0
    armature, body, groups, offset = build_avatar(payload)
    articulation = verify_articulation(armature, body, groups, payload['humanoid'])
    extension = armature.data.vrm_addon_extension
    vrm_version = payload.get('vrmVersion', '0.0')
    extension.spec_version = vrm_version
    humanoid = extension.vrm0.humanoid if vrm_version == '0.0' else extension.vrm1.humanoid
    humanoid.pose = humanoid.POSE_REST_POSITION_POSE.identifier
    if vrm_version == '0.0':
        type(humanoid).fixup_human_bones(armature)
        for mapping in humanoid.human_bones:
            if mapping.bone in payload['humanoid']:
                mapping.node.bone_name = payload['humanoid'][mapping.bone]
        type(humanoid).update_all_bone_name_candidates(bpy.context, armature.data.name, force=True)
        meta = extension.vrm0.meta
        meta.title = asset_policy['name']
        meta.version = ''
        meta.author = 'FreeMoCap Project'
        meta.reference = asset_policy['notice']
        meta.license_name = 'CC0'
        meta.other_license_url = asset_policy['licenseUrl']
        meta.allowed_user_name = 'Everyone'
        meta.violent_ussage_name = 'Allow'
        meta.sexual_ussage_name = 'Allow'
        meta.commercial_ussage_name = 'Allow'
        extension.vrm0.first_person.first_person_bone.bone_name = payload['humanoid']['head']
    else:
        for name, mapping in humanoid.human_bones.human_bone_name_to_human_bone().items():
            if name.value in payload['humanoid']:
                mapping.node.bone_name = payload['humanoid'][name.value]
        type(humanoid.human_bones).update_all_bone_name_candidates(bpy.context, armature.data.name, force=True)
        meta = extension.vrm1.meta
        meta.vrm_name = asset_policy['name']
        meta.version = ''
        meta.authors.add().value = 'FreeMoCap Project'
        meta.copyright_information = asset_policy['notice']
        meta.references.add().value = asset_policy['licenseUrl']
        meta.other_license_url = asset_policy['licenseUrl']
        meta.avatar_permission = 'everyone'
        meta.allow_excessively_violent_usage = True
        meta.allow_excessively_sexual_usage = True
        meta.allow_political_or_religious_usage = True
        meta.allow_antisocial_or_hate_usage = True
        meta.commercial_usage = 'corporation'
        meta.credit_notation = 'unnecessary'
        meta.allow_redistribution = True
        meta.modification = 'allowModificationRedistribution'
    validation = sys.modules['io_scene_vrm.editor.validation']
    preferences = sys.modules['io_scene_vrm.common.preferences'].get_preferences(bpy.context)
    preferences.export_only_selections = True
    bpy.types.Scene.skelly_vrm_validation = bpy.props.CollectionProperty(type=validation.VrmValidationError)
    errors = bpy.context.scene.skelly_vrm_validation
    validation.WM_OT_vrm_validator.detect_errors(bpy.context, errors, armature.name)
    diagnostics = [dict(severity=item.severity, message=item.message) for item in errors]
    if any(item['severity'] == 0 for item in diagnostics):
        raise ValueError(f'Official VRM validation failed: {diagnostics}')
    args.output.parent.mkdir(parents=True, exist_ok=True)
    blend_path = args.output.with_suffix('.blend')
    bpy.ops.wm.save_as_mainfile(filepath=str(blend_path))
    result = bpy.ops.export_scene.vrm(filepath=str(args.output.resolve()),
        armature_object_name=armature.name, export_only_selections=True,
        use_addon_preferences=False, ignore_warning=True)
    if result != {'FINISHED'} or not args.output.is_file():
        raise RuntimeError(f'VRM export failed: {result}')
    args.output.with_suffix('.LICENSE.txt').write_text(
        asset_policy['notice'] + '\n\n' + asset_policy['licenseUrl'] + '\n\n' +
        asset_policy['scope'] + '\n' + asset_policy['softwareLicense'] + '\n' +
        (asset_policy['vrm1LicenseNote'] + '\n' if vrm_version == '1.0' else ''), encoding='utf-8')
    if vrm_version == '1.0':
        # The exporter substitutes "undefined" for an empty author revision.
        # This field is optional, unlike specVersion [@vrm1MetadataSchema].
        glb = sys.modules['io_scene_vrm.common.gltf']
        document, binary = glb.parse_glb(args.output.read_bytes())
        document['extensions']['VRMC_vrm']['meta'].pop('version', None)
        args.output.write_bytes(glb.pack_glb(document, binary))
    report = dict(vrmVersion=vrm_version, exporterVersion=list(exporter.bl_info['version']),
                  boneCount=len(armature.data.bones), humanoidCount=len(payload['humanoid']),
                  triangles=len(body.data.polygons), vertexCount=len(body.data.vertices),
                  artworkSha256=payload['artworkSha256'], bodyHeightMeters=payload['bodyHeightMeters'], fitMode=payload['fitMode'],
                  coordinateBindings=payload['coordinateBindings'],
                  floorOffsetMeters=offset, articulation=articulation,
                  exporterDiagnostics=diagnostics,
                  avatarParentProjection=[dict(bone=item['name'], sourceParent=item['parent'],
                      avatarParent=payload['avatarParents'][item['name']]) for item in payload['bones']
                      if item['parent'] != payload['avatarParents'][item['name']]],
                  userReceiverAcceptance=False,
                  limitations=['Live receiver acceptance pending', 'No face expressions or eye tracking'])
    # Round-trip our just-created local asset; no external file or license grant
    # is involved. The direct API avoids a GUI license dialog in background mode.
    for obj in list(bpy.data.objects):
        bpy.data.objects.remove(obj, do_unlink=True)
    importer = sys.modules['io_scene_vrm.importer.import_scene']
    preferences.extract_textures_into_folder = False
    preferences.enable_mtoon_outline_preview = False
    imported = importer.import_vrm(args.output.resolve(), preferences, bpy.context, license_validation=False)
    imported_rigs = [obj for obj in bpy.data.objects if obj.type == 'ARMATURE']
    if imported != {'FINISHED'} or len(imported_rigs) != 1:
        raise ValueError('Official importer did not reconstruct one avatar')
    rig = imported_rigs[0]
    if vrm_version == '0.0':
        imported_mapping = {item.bone: item.node.bone_name for item in rig.data.vrm_addon_extension.vrm0.humanoid.human_bones
                            if item.node.bone_name}
    else:
        imported_mapping = {name.value: item.node.bone_name for name, item in
                            rig.data.vrm_addon_extension.vrm1.humanoid.human_bones.human_bone_name_to_human_bone().items()
                            if item.node.bone_name}
    if imported_mapping != payload['humanoid']:
        raise ValueError(f'Roundtrip humanoid mappings changed: {imported_mapping}')
    expected_parents = payload['avatarParents']
    actual_parents = {name: rig.data.bones[name].parent.name if rig.data.bones[name].parent else None
                      for name in expected_parents}
    if expected_parents != actual_parents:
        raise ValueError('Roundtrip avatar hierarchy changed')
    report['roundtrip'] = dict(officialImporter=True, humanoidMappings=len(imported_mapping),
                               avatarHierarchyPreserved=True,
                               meshObjects=sum(obj.type == 'MESH' for obj in bpy.data.objects))
    args.output.with_suffix('.build-report.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    print(json.dumps(report))


if __name__ == '__main__':
    main()
