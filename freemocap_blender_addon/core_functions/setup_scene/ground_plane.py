"""Ground presentation shared by the run-all controller and Parquet scenes."""
import bpy
import numpy as np

from ..materials.create_checkerboard_material import create_checkerboard_material


def create_ground_plane(trajectory=None, parent=None):
    points = np.asarray(trajectory, dtype=float).reshape(-1, 3) if trajectory is not None else np.empty((0, 3))
    points = points[np.isfinite(points).all(axis=1)]
    size = max(float(np.ptp(points[:, :2], axis=0).max()) * 2, 10.) if len(points) else 10.
    bpy.ops.mesh.primitive_plane_add(size=size, location=(0, 0, 0))
    ground = bpy.context.object
    ground.name = 'ground_plane'
    ground.parent = parent
    ground.data.materials.append(create_checkerboard_material(
        name='ground_checkerboard', color1=(.02, .02, .15, 1), color2=(.01, .01, .08, 1),
        square_scale=size / .5, roughness=1., metallic=1.))
    return ground
