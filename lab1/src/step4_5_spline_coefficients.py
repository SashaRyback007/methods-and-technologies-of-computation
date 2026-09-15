def compute_all_coefficients(x_nodes, y_nodes, h, c, n):
    """
    Обчислює коефіцієнти a_i, b_i, d_i для інтервалів i = 1..n.
    """
    a = [0.0] * (n + 1)
    b = [0.0] * (n + 1)
    d = [0.0] * (n + 1)

    for i in range(1, n + 1):
        a[i] = y_nodes[i - 1]
        hi = h[i - 1]

        if i < n:
            d[i] = (c[i + 1] - c[i]) / (3.0 * hi)
            b[i] = (y_nodes[i] - y_nodes[i - 1]) / hi - (hi / 3.0) * (c[i + 1] + 2.0 * c[i])
        else:
            d[n] = -c[n] / (3.0 * hi)
            b[n] = (y_nodes[n] - y_nodes[n - 1]) / hi - (2.0 / 3.0) * hi * c[n]

    return a, b, c, d

def evaluate_spline_value(x_val, x_nodes, a, b, c, d, n):
    """Обчислює значення сплайна S_i(x) для заданої точки x_val."""
    interval_idx = n
    for j in range(1, n + 1):
        if x_nodes[j - 1] <= x_val <= x_nodes[j]:
            interval_idx = j
            break

    dx = x_val - x_nodes[interval_idx - 1]
    return (
        a[interval_idx]
        + b[interval_idx] * dx
        + c[interval_idx] * (dx ** 2)
        + d[interval_idx] * (dx ** 3)
    )