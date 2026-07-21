import math

def gradient_descent(error_func, initial_z, args, learning_rate=0.01, tolerance=1e-5, max_iterations=1000):
    z_val = initial_z
    for _ in range(max_iterations):
        gradient = (error_func(z_val + tolerance, *args) - error_func(z_val, *args)) / tolerance
        next_z = z_val - learning_rate * gradient

        # If the change is smaller than the tolerance, optimization is complete
        if abs(next_z - z_val) < tolerance:
            break

        z_val = next_z

    return z_val

def gradient_descent_central(error_func, initial_z, args, learning_rate=0.01, tolerance=1e-7, max_iterations=3000):
    z_val = initial_z
    for _ in range(max_iterations):
        gradient = (error_func(z_val + tolerance, *args) - error_func(z_val - tolerance, *args)) / (2 * tolerance)
        next_z = z_val - learning_rate * gradient

        # If the change is smaller than the tolerance, optimization is complete
        if abs(next_z - z_val) < tolerance:
            break

        z_val = next_z

    return z_val


def minimize_custom(func, x0, args=(), tol=1e-6, max_iter=100):
    """
    Custom 1D minimizer using Brent-Dekker method.
    Returns the optimal z_C value that minimizes the error function.
    """
    # Define the function to minimize (with fixed args)
    f = lambda z: func(z, *args)
    
    # Initial bracketing of the minimum (find a, b such that f(a) > f(c) < f(b))
    a = x0
    c = a
    step = 0.1  # Initial step size (adjust based on expected solution scale)
    fa = fc = f(a)
    
    # Expand search until we find a downward slope
    for _ in range(max_iter):
        b = a + step
        fb = f(b)
        if fb > fc:  # Found upward slope - minimum is bracketed
            break
        a, c, fa, fc = c, b, fc, fb
    else:
        # Fallback if max_iter reached (use last values)
        b = c + step
        fb = f(b)
    
    # Ensure a < b and fa > fc < fb
    if a > b:
        a, b = b, a
        fa, fb = fb, fa
    
    # Brent's method parameters
    gr = (math.sqrt(5) - 1) / 2  # Golden ratio (~0.618)
    d = e = 0.0
    x = w = v = a + gr * (b - a)
    fw = fv = fx = f(x)
    
    # Main optimization loop
    for _ in range(max_iter):
        m = 0.5 * (a + b)
        tol_act = tol * abs(x) + 1e-9
        
        if abs(x - m) <= 2 * tol_act:  # Convergence check
            break
        
        # Try parabolic interpolation
        if abs(e) > tol_act:
            # Fit parabola through x, w, v
            r = (x - w) * (fx - fv)
            q = (x - v) * (fx - fw)
            p = (x - v) * q - (x - w) * r
            q = 2 * (q - r)
            p = -p / q if q > 0 else abs(p) / abs(q) if q != 0 else p
            s = e
            e = d
            
            # Accept parabola if it's "well-behaved"
            if abs(p) < abs(0.5 * q * s) and p > q * (a - x) and p < q * (b - x):
                d = p
            else:
                e = d = gr * (b - x) if x < m else gr * (a - x)
        else:
            e = d = gr * (b - x) if x < m else gr * (a - x)
        
        # Next trial point
        u = x + d if abs(d) > tol_act else x + (tol_act if d >= 0 else -tol_act)
        fu = f(u)
        
        # Update brackets
        if fu <= fx:
            if u >= x:
                a = x
            else:
                b = x
            v, w, x = w, x, u
            fv, fw, fx = fw, fx, fu
        else:
            if u < x:
                a = u
            else:
                b = u
            if fu <= fw or w == x:
                v, w = w, u
                fv, fw = fw, fu
            elif fu <= fv or v == x or v == w:
                v = u
                fv = fu
    
    return x
