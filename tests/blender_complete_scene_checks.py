"""Assertions on actual evaluated meshes/media, not only armature existence."""
import json
from pathlib import Path

import bpy
import numpy as np
from mathutils import Matrix, Quaternion, Vector
from bpy_extras.object_utils import world_to_camera_view


def descendants(obj):
    return [child for direct in obj.children for child in [direct] + descendants(direct)]


def check(result, reference):
    data, rig, skelly = result['data'], result['rig'], result['skelly_mesh']
    assert skelly is not None and len(skelly.data.polygons) > 1000
    assert any(m.type == 'ARMATURE' and m.object == rig for m in skelly.modifiers)
    assert len(result['rigid_bodies']) == len(rig.data.bones)
    assert result['center_of_mass'] is not None
    center_values = data['channels']['DERIVED_POINTS']['center_of_mass']
    center_frames = {0, len(center_values) // 2, len(center_values) - 1}
    missing = np.flatnonzero(~np.isfinite(center_values).all(axis=1))
    if len(missing):
        center_frames.add(int(missing[0]))
    for i in sorted(center_frames):
        bpy.context.scene.frame_set(int(data['frames'][i]))
        valid = bool(np.isfinite(center_values[i]).all())
        com = result['center_of_mass']
        assert com.hide_viewport != valid and com.hide_render != valid
        if valid:
            np.testing.assert_allclose(com.matrix_world.translation, center_values[i], atol=2e-6)
    assert result['ground'].parent == result['root']
    assert result['cameras'], 'Reference recording must exercise capture cameras'
    assert len(result['cameras']) == len(data['camera_geometry'])
    assert len(result['videos']) == len([m for m in reference['media'] if 'annotated_videos' in Path(m['path']).parts])
    assert result['videos'], 'Reference recording must exercise video loading'
    for plane in result['videos']:
        texture = next(n for n in plane.data.materials[0].node_tree.nodes if n.type == 'TEX_IMAGE')
        assert texture.image.source == 'MOVIE'
        assert texture.image_user.use_auto_refresh
        assert texture.image_user.frame_start == 0
        assert texture.image_user.frame_duration >= len(data['frames'])
        assert Path(texture.image.filepath).is_file()
        assert len(plane.data.uv_layers) == 1
    for obj, calibration in zip(result['cameras'], data['camera_geometry']):
        np.testing.assert_allclose(obj.location, np.asarray(calibration['world_position']) / 1000., atol=1e-6)
        # OpenCV +Z forward/+Y down -> Blender -Z forward/+Y up.
        expected = np.asarray(calibration['world_orientation']) @ np.diag([1., -1., -1.])
        np.testing.assert_allclose(np.asarray(obj.rotation_quaternion.to_matrix()), expected, atol=1e-6)
        assert obj.data.background_images[0].clip is not None
        width, height = calibration['image_size']
        point_cv = Vector((.1, .2, 2.))
        point_world = Vector(obj.location) + Matrix(calibration['world_orientation']) @ point_cv
        ndc = world_to_camera_view(bpy.context.scene, obj, point_world)
        pixels = [ndc.x * width - .5, (1 - ndc.y) * height - .5]
        intrinsics = calibration['intrinsics']
        np.testing.assert_allclose(pixels, [intrinsics['fx'] * .05 + intrinsics['cx'],
                                           intrinsics['fy'] * .1 + intrinsics['cy']], atol=1e-3)
    before = None
    for i in [len(data['frames']) // 3, 2 * len(data['frames']) // 3]:
        bpy.context.scene.frame_set(int(data['frames'][i]))
        dg = bpy.context.evaluated_depsgraph_get()
        evaluated = skelly.evaluated_get(dg)
        actual = np.array([v.co[:] for v in evaluated.data.vertices])
        assert np.isfinite(actual).all()
        if before is not None:
            assert np.max(np.linalg.norm(actual - before, axis=1)) > .01, 'Mesh does not animate'
        before = actual
        # Check one surface vertex per bone against the actual deformation,
        # catching wrong rest-space binding, detached parts, and lost weights.
        surface = {v for p in skelly.data.polygons for v in p.vertices}
        for group in skelly.vertex_groups:
            if group.name not in rig.pose.bones:
                continue
            vertex = next((v for v in skelly.data.vertices if v.index in surface and
                           any(g.group == group.index and g.weight == 1 for g in v.groups)), None)
            if vertex is None:
                continue
            if result['segments']:
                q = data['channels']['ROTATIONS_WORLD'][group.name][i]
                origin = data['channels']['SEGMENT_ORIGINS'][group.name][i]
                if not (np.isfinite(q).all() and np.isfinite(origin).all()):
                    continue
                expected = np.array(Quaternion(q) @ vertex.co) + origin
            else:
                bone = rig.evaluated_get(dg).pose.bones[group.name]
                expected = np.array(bone.matrix @ bone.bone.matrix_local.inverted() @ vertex.co)
            np.testing.assert_allclose(actual[vertex.index], expected, atol=2e-5, rtol=0)
        for obj in result['rigid_bodies']:
            bone = rig.evaluated_get(dg).pose.bones[obj['segment_name']]
            point = bone.matrix @ bone.bone.matrix_local.inverted() @ obj.data.vertices[0].co
            np.testing.assert_allclose(obj.evaluated_get(dg).data.vertices[0].co, point, atol=2e-5)
    props = bpy.context.scene.freemocap_properties
    assert props.scope_data_parent == result['root'].name
    ui = bpy.context.scene.freemocap_ui_properties
    ui.show_skelly_mesh = False
    assert skelly.hide_get()
    ui.show_skelly_mesh = True
    assert not skelly.hide_get()
    ui.show_rigid_bodies = True
    assert all(not o.hide_get() for o in result['rigid_bodies'])
    ui.show_rigid_bodies = False
    ui.show_videos = False
    assert all(o.hide_get() for o in result['videos'])
    ui.show_videos = True
    assert all(not o.hide_get() for o in result['videos'])
    return dict(mesh_vertices=len(skelly.data.vertices), mesh_deformation=True,
                videos=len(result['videos']), cameras=len(result['cameras']), scope_controls=True,
                skelly_name=skelly.name, root_name=result['root'].name)


def check_reopened(report):
    root = bpy.data.objects[report['root_name']]
    state = json.loads(root['scene_build_report'])
    assert state['videos'] == report['videos']
    mesh = bpy.data.objects[report['skelly_name']]
    assert mesh.modifiers[0].object is not None
    assert len([o for o in descendants(root) if o.get('video_path')]) == report['videos']
    assert len([o for o in descendants(root) if o.get('camera_id')]) == report['cameras']


def render_preview(result, path):
    scene = bpy.context.scene
    previous = {o: o.hide_render for o in scene.objects}
    engine, camera, filepath = scene.render.engine, scene.camera, scene.render.filepath
    resolution = (scene.render.resolution_x, scene.render.resolution_y, scene.render.resolution_percentage)
    owned = set(descendants(result['root']))
    try:
        for obj in scene.objects:
            if obj not in owned:
                obj.hide_render = True
        scene.camera = result['overview']
        scene.render.engine = 'CYCLES'
        scene.cycles.device = 'CPU'
        scene.cycles.samples = 8
        scene.render.resolution_x, scene.render.resolution_y = 960, 720
        scene.render.resolution_percentage = 100
        scene.render.filepath = str(path)
        scene.frame_set(int(result['data']['frames'][len(result['data']['frames']) // 2]))
        bpy.ops.render.render(write_still=True)
    finally:
        for obj, hidden in previous.items():
            obj.hide_render = hidden
        scene.render.engine, scene.camera, scene.render.filepath = engine, camera, filepath
        scene.render.resolution_x, scene.render.resolution_y, scene.render.resolution_percentage = resolution
