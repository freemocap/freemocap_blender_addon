import numpy as np

# Function to translate a marker's fcurve frame position by a delta
def translate_marker(
    hierarchy,
    markers,
    marker_name,
    z_delta,
    frame,
):
    markers[marker_name]['fcurves'][:, frame] += z_delta

    if marker_name in hierarchy and hierarchy[marker_name]['children']:
        for child in hierarchy[marker_name]['children']:
            translate_marker(
                hierarchy,
                markers,
                child,
                z_delta,
                frame,
            )

    return

#  Function to define a quadratic function for marker position attenuation
def quadratic_function(x1, x2, x3, y1, y2, y3):
    A = np.array([
        [x1**2, x1, 1],
        [x2**2, x2, 1],
        [x3**2, x3, 1]
    ])
    b = np.array([y1, y2, y3])
    
    # Solve for the coefficients
    a, b, c = np.linalg.solve(A, b)
    
    # Define the quadratic function
    def quadratic_function(t):
        return a*t**2 + b*t + c
    
    return quadratic_function

# The function that is going to be optimized
def error_function(z_C, x_C, y_C, x_A, y_A, z_A, x_B, y_B, z_B, length_A_to_C, length_B_to_C):
    error1 = (x_A - x_C)**2 + (y_A - y_C)**2 + (z_A - z_C)**2 - length_A_to_C**2
    error2 = (x_B - x_C)**2 + (y_B - y_C)**2 + (z_B - z_C)**2 - length_B_to_C**2
    return error1**2 + error2**2

def error_function_3d(pos_C, p_A, p_B, length_A_to_C, length_B_to_C):
    """
    pos_C: (x, y, z) of the point we are solving for
    p_A: (x, y, z) of the first base point
    p_B: (x, y, z) of the second base point
    length_A_to_C: geometric required distance from A to C
    length_B_to_C: geometric required distance from B to C
    """
    x_C, y_C, z_C = pos_C
    x_A, y_A, z_A = p_A
    x_B, y_B, z_B = p_B
    
    error1 = (x_A - x_C)**2 + (y_A - y_C)**2 + (z_A - z_C)**2 - length_A_to_C**2
    error2 = (x_B - x_C)**2 + (y_B - y_C)**2 + (z_B - z_C)**2 - length_B_to_C**2
    
    return error1**2 + error2**2

# Function to translate a marker's fcurve frame position by a 3D delta
def translate_marker_3d(
    hierarchy,
    markers,
    marker_name,
    delta_3d,
    frame,
):
    markers[marker_name]['fcurves'][:, frame] += delta_3d

    if marker_name in hierarchy and hierarchy[marker_name]['children']:
        for child in hierarchy[marker_name]['children']:
            translate_marker_3d(
                hierarchy,
                markers,
                child,
                delta_3d,
                frame,
            )

    return
