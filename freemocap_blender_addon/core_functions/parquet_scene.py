"""Scene presentation shared by the saved-pose and constraint import routes.

Presentation never reconstructs or edits the native segment poses. The existing
Skelly asset has legacy vertex-group names; that asset vocabulary is translated
at this boundary, independently of tracker keypoints and model landmark names.
"""
import json
import math
from pathlib import Path

import bpy
import numpy as np
from mathutils import Matrix, Quaternion, Vector


def asset_segments():
    mapping = dict(face='skull', pelvis='pelvis', spine='sacrolumbar',
                   **{'spine.001': 'thoracic', 'neck': 'cervical_spine'})
    for side, suffix in [('left', 'L'), ('right', 'R')]:
        for old, new in [('upper_arm', 'upper_arm'), ('forearm', 'lower_arm'),
                         ('thigh', 'upper_leg'), ('shin', 'lower_leg'),
                         ('foot', 'foot'), ('heel.02', 'toes')]:
            mapping[old + '.' + suffix] = side + '_' + new
        for i, digit in enumerate(('index', 'middle', 'ring', 'pinky'), 1):
            mapping['palm.{:02d}.{}'.format(i, suffix)] = side + '_' + digit + '_metacarpal'
            for j, part in enumerate(('proximal', 'middle', 'distal'), 1):
                mapping['f_{}.{:02d}.{}'.format(digit, j, suffix)] = side + '_' + digit + '_' + part + '_phalanx'
        for i, part in enumerate(('metacarpal', 'proximal_phalanx', 'distal_phalanx'), 1):
            mapping['thumb.{:02d}.{}'.format(i, suffix)] = side + '_thumb_' + part
    return mapping


def bind(mesh, rig, groups):
    mesh.parent = rig
    for name, indices in groups.items():
        mesh.vertex_groups.new(name=name).add(indices, 1., 'REPLACE')
    modifier = mesh.modifiers.new('Blender skeleton deformation', 'ARMATURE')
    modifier.object = rig


def rigid_meshes(result, parent):
    """One visible rigid shape for every Blender bone, driven by that bone."""
    from .meshes.rigid_body_meshes.helpers.make_bone_mesh import make_bone_mesh
    from .meshes.rigid_body_meshes.helpers.put_meshes_on_empties import get_bone_mesh_color_and_squish
    rig = result['rig']
    objects = []
    for bone in rig.data.bones:
        canonical = asset_segments().get(bone.name, bone.name)
        style = canonical
        if canonical.endswith(('.L', '.R')):
            style = ('left_' if canonical.endswith('.L') else 'right_') + canonical[:-2]
        if any(digit in canonical for digit in ('thumb', 'index', 'middle', 'ring', 'pinky')):
            style = ('left' if canonical.startswith('left_') else 'right') + '_hand'
        color, squish = get_bone_mesh_color_and_squish(style)
        obj = make_bone_mesh(name='rigid_body_' + bone.name, length=bone.length,
                             squish_scale=squish, joint_color=color, cone_color=color,
                             axis_visible=False)
        orientation = (bone.tail_local - bone.head_local).to_track_quat('Z', 'Y')
        for vertex in obj.data.vertices:
            vertex.co = bone.head_local + orientation @ vertex.co
        bind(obj, rig, {bone.name: list(range(len(obj.data.vertices)))})
        obj.parent = parent
        obj['segment_name'] = bone.name
        objects.append(obj)
    return objects



def native_skelly(result):
    """Fit each rigid asset part in its owning segment's local coordinates.

    Native armature deformation is T(origin) Q(world): its rest drawing basis
    cancels out. Thus vertices belong in segment-local coordinates, not in the
    connected T-pose expected by the legacy mesh attachment helper.
    """
    from .meshes.skelly_mesh.portable_asset import load_skelly_mesh
    from .meshes.skelly_mesh.helpers.skelly_vertex_groups import _SKELLY_VERTEX_GROUPS
    data = result['data']
    segments = {s['name']: s for s in data['model']['skeleton']['segments']}
    mapping = asset_segments()
    if not set(mapping.values()).issubset(segments):
        return None  # Non-human contract fixtures still get their segment meshes.
    landmarks = {p['name']: p for p in data['model']['skeleton']['landmarks']}
    rest = data['model']['rest_pose']
    world_rest = {}

    def rest_rotation(name):
        if name not in world_rest:
            q = rest['orientations'][name]
            local = Quaternion(tuple(q[k] for k in 'wxyz'))
            parent = rest['parents'][name]
            world_rest[name] = rest_rotation(parent) @ local if parent else local
        return world_rest[name]

    from .meshes.skelly_mesh.attachment_frame import attachment_rotation
    obj = load_skelly_mesh(canonical=True)
    attachment_frames = json.loads(obj['attachment_frames'])
    obj.modifiers.clear()
    original = [v.co.copy() for v in obj.data.vertices]
    memberships = {g.name: [] for g in obj.vertex_groups}
    for v in obj.data.vertices:
        for g in v.groups:
            if g.weight > 0:
                memberships[obj.vertex_groups[g.group].name].append(v.index)
    weights = {}
    assigned = set()
    for old in _SKELLY_VERTEX_GROUPS:
        name = mapping[old]
        indices = memberships[old]
        source_head = original[memberships[old + '_origin'][0]]
        source_tail = (original[memberships['pelvis_left'][0]] if old == 'pelvis'
                       else original[memberships[old + '_end'][0]])
        source_vector = source_tail - source_head
        segment = segments[name]
        endpoint = landmarks[segment['frame']['primary_point']]
        if endpoint['segment'] != name:
            raise ValueError('Asset endpoint is not local to segment ' + name)
        local_tail = Vector(endpoint['position']) * (data['scales'][name] / 1000.)
        if local_tail.length < 1e-8 or source_vector.length < 1e-8:
            raise ValueError('Cannot fit zero-length Skelly part ' + old)
        rest_q = rest_rotation(name)
        frame = attachment_frames[old]
        secondary_name = frame.get('model_secondary_landmark')
        local_secondary = None
        if secondary_name is not None:
            secondary = landmarks[secondary_name]
            if (secondary['segment'] != name or
                    segment['frame'].get('secondary_point') != secondary_name):
                raise ValueError('Asset secondary landmark disagrees with model frame: ' + name)
            local_secondary = Vector(secondary['position'])
        rotation = attachment_rotation(source_vector, local_tail, rest_q,
                                       frame['roll_reference'], local_secondary)
        scale = local_tail.length / source_vector.length
        if old == 'pelvis':
            source_width = (original[memberships['pelvis_left'][0]] -
                            original[memberships['pelvis_right'][0]]).length
            target_width = (Vector(landmarks['left_hip_socket']['position']) -
                            Vector(landmarks['right_hip_socket']['position'])).length
            scale = target_width * data['scales'][name] / 1000. / source_width
        for index in indices:
            if index in assigned:
                raise ValueError('Overlapping rigid asset groups at vertex ' + str(index))
            obj.data.vertices[index].co = rotation @ ((original[index] - source_head) * scale)
            assigned.add(index)
        weights[name] = indices
    # Helper origin/end vertices have no faces; remove their weights. Every
    # rendered vertex must belong to an explicitly mapped rigid part.
    surface = {i for poly in obj.data.polygons for i in poly.vertices}
    if not surface.issubset(assigned):
        raise ValueError('Unmapped surface vertices in Skelly mesh')
    obj.vertex_groups.clear()
    bind(obj, result['rig'], weights)
    obj['binding'] = 'Skelly asset parts mapped to canonical segment-local coordinates'
    return obj


def videos(result, parent):
    """Direct mesh/material construction works without optional Blender add-ons."""
    root = Path(result['data']['path']).parent
    folder = next((root / n for n in ('annotated_videos', 'synchronized_videos')
                   if (root / n).is_dir() and any(p.suffix.lower() == '.mp4' for p in (root / n).iterdir())), None)
    objects = []
    if folder is None:
        return objects
    paths = sorted(p for p in folder.iterdir() if p.suffix.lower() == '.mp4')
    for index, path in enumerate(paths):
        image = bpy.data.images.load(str(path), check_existing=True)
        if not image.size[0] or not image.size[1]:
            raise ValueError('Cannot decode video: ' + str(path))
        height, width = 2., 2. * image.size[0] / image.size[1]
        mesh = bpy.data.meshes.new('video_plane')
        mesh.from_pydata([(-width/2, 0, 0), (width/2, 0, 0),
                          (width/2, 0, height), (-width/2, 0, height)], [], [(0, 1, 2, 3)])
        uv = mesh.uv_layers.new()
        for loop, coords in zip(uv.data, [(0, 0), (1, 0), (1, 1), (0, 1)]):
            loop.uv = coords
        obj = bpy.data.objects.new('video_' + path.stem, mesh)
        bpy.context.collection.objects.link(obj)
        obj.parent = parent
        obj.location = ((index - (len(paths)-1)/2) * (width + .2), 2.5, .1)
        obj['video_path'] = str(path)
        material = bpy.data.materials.new('video_' + path.stem)
        material.use_nodes = True
        nodes = material.node_tree.nodes
        nodes.clear()
        texture = nodes.new('ShaderNodeTexImage')
        texture.image = image
        texture.image_user.use_auto_refresh = True
        texture.image_user.frame_duration = image.frame_duration
        # Source frame zero is movie frame one. Starting at zero preserves that
        # relation even when the loaded recording starts at a later source frame.
        texture.image_user.frame_start = 0
        emission = nodes.new('ShaderNodeEmission')
        output = nodes.new('ShaderNodeOutputMaterial')
        material.node_tree.links.new(texture.outputs['Color'], emission.inputs['Color'])
        material.node_tree.links.new(emission.outputs[0], output.inputs['Surface'])
        mesh.materials.append(material)
        objects.append(obj)
    return objects


def cameras(result, parent):
    objects = []
    folder = Path(result['data']['path']).parent / 'synchronized_videos'
    for camera in result['data']['camera_geometry']:
        datablock = bpy.data.cameras.new('Capture_' + camera['id'])
        obj = bpy.data.objects.new(datablock.name, datablock)
        bpy.context.collection.objects.link(obj)
        obj.parent = parent
        obj.location = np.asarray(camera['world_position']) / 1000.
        obj.rotation_mode = 'QUATERNION'
        obj.rotation_quaternion = Matrix(camera['world_orientation']).to_quaternion() @ Quaternion((1, 0, 0), math.pi)
        width, height = camera['image_size']
        intrinsics = camera['intrinsics']
        datablock.sensor_fit = 'HORIZONTAL'
        datablock.sensor_width = 36
        datablock.lens = intrinsics['fx'] * 36 / width
        datablock.shift_x = ((width - 1) / 2 - intrinsics['cx']) / width
        datablock.shift_y = (intrinsics['cy'] - (height - 1) / 2) / width * intrinsics['fx'] / intrinsics['fy']
        datablock.display_size = .15
        obj['camera_id'] = camera['id']
        obj['calibration'] = json.dumps(camera)
        path = folder / Path(camera['id']).name
        if path.is_file():
            background = datablock.background_images.new()
            background.source = 'MOVIE_CLIP'
            background.clip = bpy.data.movieclips.load(str(path), check_existing=True)
            background.clip.frame_start = 0
            datablock.show_background_images = True
        objects.append(obj)
    return objects


def build_scene(result):
    from .parquet_import import empty, trajectory, animate, curves
    root, rig, data = result['root'], result['rig'], result['data']
    rig.name = root.name + '_Blender_skeleton_rig'
    groups = {name: empty(name, root) for name in
              ('rigid_body_meshes_parent', 'videos_parent', 'capture_cameras_parent')}
    rigid = rigid_meshes(result, groups['rigid_body_meshes_parent'])
    if result['segments']:
        skelly = native_skelly(result)
    else:
        from .meshes.skelly_mesh.attach_skelly_mesh import attach_skelly_mesh_to_rig
        before = set(bpy.data.objects)
        attach_skelly_mesh_to_rig(rig, {})
        skelly = next(o for o in set(bpy.data.objects) - before if o.type == 'MESH')
    com = None
    if 'center_of_mass' in data['channels'].get('DERIVED_POINTS', {}):
        values = data['channels']['DERIVED_POINTS']['center_of_mass']
        target = trajectory('center_of_mass', values, data['frames'], root)
        from .meshes.center_of_mass.center_of_mass_mesh import create_center_of_mass_mesh
        com = create_center_of_mass_mesh(parent_object=root, center_of_mass_empty=target)
        target.hide_set(True)  # Hide the helper, not the COM sphere (run-all behavior).
        fc = curves(com)
        for visibility in ('hide_viewport', 'hide_render'):
            animate(fc, visibility, data['frames'], (~np.isfinite(values).all(axis=1)).astype(float))
    video_objects = videos(result, groups['videos_parent'])
    # The canonical model faces +Y. Put the presentation wall behind it,
    # rotating the planes together so their textures remain front-facing.
    # Capture calibration and recorded motion remain in their original frame.
    groups['videos_parent'].rotation_euler.z = math.pi
    camera_objects = cameras(result, groups['capture_cameras_parent'])
    if camera_objects:
        first_camera = data['camera_geometry'][0]
        render = bpy.context.scene.render
        render.resolution_x, render.resolution_y = first_camera['image_size']
        render.resolution_percentage = 100
        render.pixel_aspect_x = 1.
        render.pixel_aspect_y = first_camera['intrinsics']['fx'] / first_camera['intrinsics']['fy']
    from .setup_scene.ground_plane import create_ground_plane
    ground = create_ground_plane(data['channels'].get('DERIVED_POINTS', {}).get('center_of_mass'), root)
    overview = bpy.data.objects.new('FreeMoCap_overview', bpy.data.cameras.new('FreeMoCap_overview'))
    bpy.context.collection.objects.link(overview)
    overview.parent = root
    overview.location = (-3.5, 7, 2.8)
    view_target = Vector((0, -.5, 1))
    overview.rotation_euler = (view_target - overview.location).to_track_quat('-Z', 'Y').to_euler()
    overview.data.lens = 40
    overview.data.sensor_fit = 'HORIZONTAL'
    bpy.context.scene.camera = overview
    light = bpy.data.objects.new('FreeMoCap_light', bpy.data.lights.new('FreeMoCap_light', 'AREA'))
    bpy.context.collection.objects.link(light)
    light.parent = root
    light.location = (-1, 3, 5)
    light.rotation_euler = (Vector((0, 0, 1)) - light.location).to_track_quat('-Z', 'Y').to_euler()
    light.data.energy = 1000
    light.data.shape = 'DISK'
    light.data.size = 5
    # The run-all controller hides organizational empties, not their mesh children.
    groups['rigid_body_meshes_parent'].hide_set(True)
    for obj in list(result['landmarks'].values()) + list(result['segments'].values()) + list(result['targets'].values()):
        obj.hide_set(True)
    scene = bpy.context.scene
    scene.unit_settings.system = 'METRIC'
    scene.unit_settings.scale_length = 1.
    props = getattr(scene, 'freemocap_properties', None)
    if props is not None:
        props.data_parent_collection.add().name = root.name
        props.scope_data_parent = root.name
    from .setup_scene.set_viewport_shading import set_viewport_to_material_preview
    set_viewport_to_material_preview()
    # Store an orbitable front overview in every saved workspace, including
    # background exports where there is no active window/VIEW_3D context.
    for screen in bpy.data.screens:
        for area in screen.areas:
            if area.type != 'VIEW_3D':
                continue
            space = area.spaces.active
            space.lens = overview.data.lens
            region = space.region_3d
            region.view_rotation = overview.rotation_euler.to_quaternion()
            region.view_location = view_target
            region.view_distance = (overview.location - view_target).length
            region.view_perspective = 'PERSP'
    # The factory cube otherwise obscures a meter-scale subject. Keep it
    # recoverable rather than deleting an existing scene object.
    cube = bpy.data.objects.get(bpy.app.translations.pgettext_data('Cube'))
    if (cube is not None and cube.type == 'MESH' and cube.parent is None
            and len(cube.data.vertices) == 8 and len(cube.data.polygons) == 6
            and all(all(abs(abs(c) - 1.) < 1e-6 for c in v.co) for v in cube.data.vertices)):
        cube.hide_set(True)
        cube.hide_render = True
    report = dict(rigid_bodies=len(rigid), skelly_mesh=skelly.name if skelly else None,
                  videos=len(video_objects), capture_cameras=len(camera_objects),
                  center_of_mass=com is not None)
    root['scene_build_report'] = json.dumps(report)
    result.update(scene_report=report, rigid_bodies=rigid, skelly_mesh=skelly,
                  videos=video_objects, cameras=camera_objects, ground=ground, center_of_mass=com,
                  overview=overview)
