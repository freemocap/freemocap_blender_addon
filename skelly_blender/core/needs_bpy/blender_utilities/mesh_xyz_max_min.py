from dataclasses import dataclass

import bpy
import numpy as np


@dataclass
class MaxMin:
    min: float
    max: float


@dataclass
class XYZMaxMin:
    x: MaxMin
    y: MaxMin
    z: MaxMin


def find_mesh_xyz_maxmin(mesh: bpy.types.Object) -> XYZMaxMin:
    if mesh and mesh.type == 'MESH':
        vertices = np.array([v.co.to_tuple() for v in mesh.data.vertices])
        min_x, max_x = vertices[:, 0].min(), vertices[:, 0].max()
        min_y, max_y = vertices[:, 1].min(), vertices[:, 1].max()
        min_z, max_z = vertices[:, 2].min(), vertices[:, 2].max()

        return XYZMaxMin(
            x=MaxMin(min=min_x, max=max_x),
            y=MaxMin(min=min_y, max=max_y),
            z=MaxMin(min=min_z, max=max_z)
        )
    else:
        raise ValueError(f"Object {mesh} is not a mesh object!")
