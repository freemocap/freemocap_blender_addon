"""Assertions on actual evaluated meshes/media, not only armature existence."""
import json
import gzip
from pathlib import Path

import bpy
import numpy as np
from mathutils import Matrix, Quaternion, Vector
from bpy_extras.object_utils import world_to_camera_view


def descendants(obj):
    return [child for direct in obj.children for child in [direct] + descendants(direct)]


def check_camera_extrinsics(result):
    """Check actual world-space landmarks against independently stored R,t.

    Comparing only to world_orientation repeats the importer's assumption and
    cannot catch disagreements between that cached pose and the extrinsics.
    This verifies an ideal pinhole projection, not raw-video lens distortion.
    """
    scene = bpy.context.scene
    render = scene.render
    previous = (render.resolution_x, render.resolution_y,
                render.resolution_percentage, render.pixel_aspect_x, render.pixel_aspect_y)
    frame = scene.frame_current
    data = result['data']
    try:
        bpy.context.view_layer.update()
        for obj, camera in zip(result['cameras'], data['camera_geometry']):
            extrinsics = camera['extrinsics']
            rotation = np.asarray(Quaternion(extrinsics['quaternion_wxyz']).to_matrix())
            translation = np.asarray(extrinsics['translation']) / 1000.
            np.testing.assert_allclose(obj.matrix_world.translation,
                                       -rotation.T @ translation, atol=2e-6)
            np.testing.assert_allclose(np.asarray(obj.matrix_world.to_3x3()),
                                       rotation.T @ np.diag([1., -1., -1.]), atol=2e-6)
            width, height = camera['image_size']
            k = camera['intrinsics']
            render.resolution_x, render.resolution_y = width, height
            render.resolution_percentage = 100
            render.pixel_aspect_x, render.pixel_aspect_y = 1., k['fx'] / k['fy']
            checked = 0
            for i in (len(data['frames']) // 3, 2 * len(data['frames']) // 3):
                scene.frame_set(int(data['frames'][i]))
                for name, landmark in result['landmarks'].items():
                    point = data['channels'][data['trajectory_channel']][name][i]
                    if not np.isfinite(point).all():
                        continue
                    camera_point = rotation @ point + translation
                    if camera_point[2] <= .01:
                        continue
                    ndc = world_to_camera_view(scene, obj, landmark.matrix_world.translation)
                    assert ndc.z > 0
                    expected = camera_point[:2] / camera_point[2] * [k['fx'], k['fy']] + [k['cx'], k['cy']]
                    np.testing.assert_allclose([ndc.x * width - .5, (1 - ndc.y) * height - .5],
                                               expected, atol=.005, rtol=0)
                    checked += 1
            assert checked, 'No finite landmarks in front of the calibrated camera'
    finally:
        (render.resolution_x, render.resolution_y, render.resolution_percentage,
         render.pixel_aspect_x, render.pixel_aspect_y) = previous
        scene.frame_set(frame)


def check_anatomy(result, package_path):
    """Independent anatomical landmarks on the artwork, not bind-matrix echoes."""
    with gzip.open(package_path / 'assets/skelly_mesh.json.gz', 'rt', encoding='utf-8') as stream:
        asset = json.load(stream)
    mesh = result['skelly_mesh']
    surface = {v for face in asset['faces'] for v in face}
    skull = [i for i, weight in asset['groups']['face'] if weight and i in surface]
    top = max(skull, key=lambda i: asset['vertices'][i][2])
    front = max(skull, key=lambda i: asset['vertices'][i][1])
    # The skull frame is explicitly +Y nose, +Z vertex, with origin at its base.
    assert mesh.data.vertices[top].co.z > .02, 'Skull top is inverted'
    assert mesh.data.vertices[front].co.y > .02, 'Skull faces backward'
    pelvis = [i for i, weight in asset['groups']['pelvis'] if weight and i in surface]
    left = min(pelvis, key=lambda i: asset['vertices'][i][0])
    right = max(pelvis, key=lambda i: asset['vertices'][i][0])
    assert mesh.data.vertices[left].co.x < mesh.data.vertices[right].co.x, 'Pelvis left/right reversed'
    for frame in (0, len(result['data']['frames']) // 2):
        data = result['data']
        bpy.context.scene.frame_set(int(data['frames'][frame]))
        evaluated = mesh.evaluated_get(bpy.context.evaluated_depsgraph_get())
        q = data['channels']['ROTATIONS_WORLD']['skull'][frame]
        origin = data['channels']['SEGMENT_ORIGINS']['skull'][frame]
        if np.isfinite(q).all() and np.isfinite(origin).all():
            up = Quaternion(q) @ Vector((0, 0, 1))
            forward = Quaternion(q) @ Vector((0, 1, 0))
            assert (evaluated.data.vertices[top].co - Vector(origin)).dot(up) > .02
            assert (evaluated.data.vertices[front].co - Vector(origin)).dot(forward) > .02


def check(result, reference):
    data, rig, skelly = result['data'], result['rig'], result['skelly_mesh']
    assert skelly is not None and len(skelly.data.polygons) > 1000
    assert any(m.type == 'ARMATURE' and m.object == rig for m in skelly.modifiers)
    assert len(result['rigid_bodies']) == len(rig.data.bones)
    # The two layers must retain DIFFERENT presentation contracts.
    assert all(not o.hide_get() and not o.hide_render for o in result['rigid_bodies'])
    for obj in result['rigid_bodies']:
        assert len(obj.data.vertices) > 40, 'Expected the existing cone + joint sphere builder'
        assert {p.material_index for p in obj.data.polygons} == {0, 1}, 'Cone and joint must both exist'
        canonical = obj['segment_name']
        if canonical in ('left_upper_arm', 'upper_arm.L', 'right_upper_arm', 'upper_arm.R'):
            expected = (0, 0, 1, 1) if canonical in ('left_upper_arm', 'upper_arm.L') else (1, 0, 0, 1)
            for mat in obj.data.materials:
                emission = next(n for n in mat.node_tree.nodes if n.type == 'EMISSION')
                np.testing.assert_allclose(emission.inputs['Color'].default_value, expected)
    assert len(skelly.data.materials) == 3
    expected_colors = [(0.37123689, 0.67244279, 0.6938718, 1), (0, 0, 0, 1),
                       (0.69387192, 0.08228248, 0.09530751, 1)]
    for mat, expected in zip(skelly.data.materials, expected_colors):
        shader = next(n for n in mat.node_tree.nodes if n.type == 'BSDF_PRINCIPLED')
        np.testing.assert_allclose(shader.inputs['Base Color'].default_value, expected, atol=1e-6)
    assert {p.material_index for p in skelly.data.polygons} == {0, 1, 2}
    source_asset = Path(__file__).resolve().parents[1] / 'freemocap_blender_addon/assets/skelly_mesh.json.gz'
    with gzip.open(source_asset, 'rt', encoding='utf-8') as stream:
        appearance = json.load(stream)
    np.testing.assert_array_equal([p.material_index for p in skelly.data.polygons], appearance['face_materials'])
    assert result['center_of_mass'] is not None
    assert not result['center_of_mass'].hide_get(), 'Only the COM empty should be hidden'
    for obj, colors, scale in [(result['center_of_mass'], [(0, .5, 1, 1), (1, 0, 1, 1)], 2),
                               (result['ground'], [(.02, .02, .15, 1), (.01, .01, .08, 1)],
                                result['ground'].dimensions.x / .5)]:
        mat = obj.data.materials[0]
        checker = next(n for n in mat.node_tree.nodes if n.type == 'TEX_CHECKER')
        for socket, color in zip(('Color1', 'Color2'), colors):
            np.testing.assert_allclose(checker.inputs[socket].default_value, color, atol=1e-6)
        np.testing.assert_allclose(checker.inputs['Scale'].default_value, scale)
        shaders = [n for n in mat.node_tree.nodes if n.type == 'BSDF_PRINCIPLED']
        assert len(shaders) == 1, 'Configured checker shader must not be replaced'
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
    check_camera_extrinsics(result)
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
    assert all(o.hide_get() for o in result['rigid_bodies'])
    assert not skelly.hide_get(), 'Stick visibility must not hide the anatomical layer'
    ui.show_rigid_bodies = True
    ui.show_center_of_mass = False
    assert result['center_of_mass'].hide_get()
    ui.show_center_of_mass = True
    assert not result['center_of_mass'].hide_get()
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
