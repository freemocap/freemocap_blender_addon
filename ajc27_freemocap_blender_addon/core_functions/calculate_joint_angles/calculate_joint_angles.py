import numpy as np
import math as m
from mathutils import Vector
from typing import Dict, List, Tuple, Optional

from ajc27_freemocap_blender_addon.core_functions.calculate_joint_angles.joint_angle_definitions import (
    JointAngleDefinition,
    RotationVectorDefinition,
    ProjectedVectorDefinition,
)

# Define type aliases for better readability
MarkerPositions = np.ndarray
FrameIndex = int
AngleValue = float


class JointAngleCalculator:
    def __init__(self, marker_names: List[str], marker_frame_xyz: MarkerPositions):
        self.marker_names = marker_names
        self.marker_frame_xyz = marker_frame_xyz
        self.marker_name_to_index = {name: idx for idx, name in enumerate(marker_names)}
        
    def get_marker_position(self, frame: FrameIndex, marker_name: str) -> np.ndarray:
        """Get the position of a marker in a specific frame."""
        return self.marker_frame_xyz[frame, self.marker_name_to_index[marker_name]]
    
    def create_vector(self, origin_pos: np.ndarray, end_pos: np.ndarray) -> Vector:
        """Create a Vector from two positions."""
        return Vector(end_pos) - Vector(origin_pos)
    
    def calculate_reference_vector(self, frame: FrameIndex, definition: Dict) -> Vector:
        """Calculate the reference vector based on its definition."""
        vec_type = definition['type']
        
        if vec_type == 'vector':
            origin_pos = self.get_marker_position(frame, definition['reference_vector_origin'])
            end_pos = self.get_marker_position(frame, definition['reference_vector_end'])
            return self.create_vector(origin_pos, end_pos)
            
        elif vec_type == 'crossproduct':
            vec1 = self.create_vector(
                self.get_marker_position(frame, definition['reference_cross_1_origin']),
                self.get_marker_position(frame, definition['reference_cross_1_end'])
            )
            vec2 = self.create_vector(
                self.get_marker_position(frame, definition['reference_cross_2_origin']),
                self.get_marker_position(frame, definition['reference_cross_2_end'])
            )
            return vec1.cross(vec2)
            
        elif vec_type == 'doublecrossproduct':
            vec1 = self.create_vector(
                self.get_marker_position(frame, definition['reference_cross_1_origin']),
                self.get_marker_position(frame, definition['reference_cross_1_end'])
            )
            vec2 = self.create_vector(
                self.get_marker_position(frame, definition['reference_cross_2_origin']),
                self.get_marker_position(frame, definition['reference_cross_2_end'])
            )
            vec3 = self.create_vector(
                self.get_marker_position(frame, definition['reference_cross_3_origin']),
                self.get_marker_position(frame, definition['reference_cross_3_end'])
            )
            return vec1.cross(vec2).cross(vec3)
            
        elif vec_type == 'average':
            vec1 = self.create_vector(
                self.get_marker_position(frame, definition['reference_average_1_origin']),
                self.get_marker_position(frame, definition['reference_average_1_end'])
            )
            vec2 = self.create_vector(
                self.get_marker_position(frame, definition['reference_average_2_origin']),
                self.get_marker_position(frame, definition['reference_average_2_end'])
            )
            return (vec1 + vec2) / 2
            
        else:
            raise ValueError(f"Invalid reference vector type: {vec_type}")
    
    def calculate_plane_axis(self, frame: FrameIndex, axis_def: Dict) -> Vector:
        """Calculate a plane axis based on its definition."""
        axis_type = axis_def['type']

        if axis_type == 'vector':
            origin_pos = self.get_marker_position(frame, axis_def['plane_axis_origin'])
            end_pos = self.get_marker_position(frame, axis_def['plane_axis_end'])
            return self.create_vector(origin_pos, end_pos).normalized()
            
        elif axis_type == 'crossproduct':
            vec1 = self.create_vector(
                self.get_marker_position(frame, axis_def['plane_axis_cross_1_origin']),
                self.get_marker_position(frame, axis_def['plane_axis_cross_1_end'])
            ).normalized()
            vec2 = self.create_vector(
                self.get_marker_position(frame, axis_def['plane_axis_cross_2_origin']),
                self.get_marker_position(frame, axis_def['plane_axis_cross_2_end'])
            ).normalized()
            return vec1.cross(vec2).normalized()
            
        elif axis_type == 'doublecrossproduct':
            vec1 = self.create_vector(
                self.get_marker_position(frame, axis_def['plane_axis_cross_1_origin']),
                self.get_marker_position(frame, axis_def['plane_axis_cross_1_end'])
            ).normalized()
            vec2 = self.create_vector(
                self.get_marker_position(frame, axis_def['plane_axis_cross_2_origin']),
                self.get_marker_position(frame, axis_def['plane_axis_cross_2_end'])
            ).normalized()
            vec3 = self.create_vector(
                self.get_marker_position(frame, axis_def['plane_axis_cross_3_origin']),
                self.get_marker_position(frame, axis_def['plane_axis_cross_3_end'])
            ).normalized()
            return vec1.cross(vec2).cross(vec3).normalized()
            
        elif axis_type == 'average':
            vec1 = self.create_vector(
                self.get_marker_position(frame, axis_def['plane_axis_average_1_origin']),
                self.get_marker_position(frame, axis_def['plane_axis_average_1_end'])
            ).normalized()
            vec2 = self.create_vector(
                self.get_marker_position(frame, axis_def['plane_axis_average_2_origin']),
                self.get_marker_position(frame, axis_def['plane_axis_average_2_end'])
            ).normalized()
            return ((vec1 + vec2) / 2).normalized()
            
        elif axis_type == 'average_crossproduct':
            vec1 = self.create_vector(
                self.get_marker_position(frame, axis_def['plane_axis_average_1_origin']),
                self.get_marker_position(frame, axis_def['plane_axis_average_1_end'])
            ).normalized()
            vec2 = self.create_vector(
                self.get_marker_position(frame, axis_def['plane_axis_average_2_origin']),
                self.get_marker_position(frame, axis_def['plane_axis_average_2_end'])
            ).normalized()
            avg = ((vec1 + vec2) / 2).normalized()
            
            vec3 = self.create_vector(
                self.get_marker_position(frame, axis_def['plane_axis_cross_1_origin']),
                self.get_marker_position(frame, axis_def['plane_axis_cross_1_end'])
            ).normalized()
            return avg.cross(vec3).normalized()
            
        else:
            raise ValueError(f"Unsupported axis type: {axis_type}")
    
    def calculate_projected_vector(
        self, 
        frame: FrameIndex, 
        projection_def: ProjectedVectorDefinition
    ) -> Tuple[np.ndarray, Vector]:
        """Calculate a projected vector and its plane normal."""
        # Get the vector to project
        proj_vec_origin = self.get_marker_position(frame, projection_def.origin)
        proj_vec_end = self.get_marker_position(frame, projection_def.end)
        vec_to_project = proj_vec_end - proj_vec_origin
        
        # Calculate plane axes
        axis1 = self.calculate_plane_axis(frame, projection_def.projection_plane.axis1)
        axis2 = self.calculate_plane_axis(frame, projection_def.projection_plane.axis2)
        
        # Define plane and project vector
        plane_normal = axis1.cross(axis2).normalized()
        vec_proj = vec_to_project - plane_normal * vec_to_project.dot(plane_normal)
        
        # Return projected position and plane normal
        return (proj_vec_origin + vec_proj, plane_normal)
    
    def calculate_rotation_vector(
        self, 
        frame: FrameIndex, 
        rotation_def: RotationVectorDefinition
    ) -> Tuple[Vector, Optional[Vector]]:
        """Calculate the rotation vector and optionally its plane normal."""
        origin_pos = self.get_marker_position(frame, rotation_def.origin)
        
        if isinstance(rotation_def.end, str):
            # Simple vector case
            end_pos = self.get_marker_position(frame, rotation_def.end)
            return (self.create_vector(origin_pos, end_pos), None)
        else:
            # Projected vector case
            end_pos, plane_normal = self.calculate_projected_vector(frame, rotation_def.end)
            return (self.create_vector(origin_pos, end_pos), plane_normal)
    
    def calculate_joint_angle(
        self, 
        frame: FrameIndex, 
        angle_def: JointAngleDefinition
    ) -> AngleValue:
        """Calculate a single joint angle for a specific frame."""
        # Calculate reference vector
        reference_vector = self.calculate_reference_vector(frame, angle_def.reference_vector)
        
        # Calculate rotation vector and get plane normal if available
        rotation_vector, rotation_plane_normal = self.calculate_rotation_vector(
            frame, angle_def.rotation_vector
        )
        
        # Calculate angle between vectors
        angle = m.degrees(rotation_vector.angle(reference_vector))
        
        # Determine angle sign using cross product and plane normal
        cross_product = reference_vector.cross(rotation_vector)
        if rotation_plane_normal is None:
            rotation_plane_normal = cross_product
        
        if cross_product.dot(rotation_plane_normal) < 0:
            angle = -angle

        # Add the zero offset angle
        angle += angle_def.zero_offset
            
        return angle

def calculate_joint_angles(
    output_path: str,
    marker_names: List[str],
    marker_frame_xyz: MarkerPositions,
    joint_angles_definitions: Dict[str, JointAngleDefinition]
) -> None:
    """Main function to calculate all joint angles for all frames."""
    print("Calculating joint angles...")
    
    # Initialize calculator and result array
    calculator = JointAngleCalculator(marker_names, marker_frame_xyz)
    angle_list = list(joint_angles_definitions.keys())
    angle_values = np.full((marker_frame_xyz.shape[0], len(angle_list)), np.nan)
    
    # Calculate angles for each frame and joint
    for frame in range(marker_frame_xyz.shape[0]):
        for joint_angle_name, angle_def in joint_angles_definitions.items():
            try:
                angle = calculator.calculate_joint_angle(frame, angle_def)
                angle_values[frame, angle_list.index(joint_angle_name)] = angle
            except Exception as e:
                print(f"Error calculating {joint_angle_name} for frame {frame}: {str(e)}")
                continue
    
    # Save results to CSV
    np.savetxt(
        output_path,
        angle_values,
        delimiter=",",
        header=",".join(angle_list),
        comments='',
        fmt='%.8f',
    )

    # Save results to a numpy file
    np.save(output_path.replace('.csv', '.npy'), angle_values) 
