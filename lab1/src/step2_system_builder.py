def build_tridiagonal_system(x_nodes, y_nodes, n):
    """
    Формує коефіцієнти альфа, бета, гамма, дельта системи рівнянь для c_i.
    Використовує 1-індексацію (розмірність n + 1).
    """
    # Кроки між вузлами: h[k] = x_{k+1} - x_k для k = 0..n-1
    h = [x_nodes[i] - x_nodes[i - 1] for i in range(1, n + 1)]

    alpha = [0.0] * (n + 1)
    beta = [0.0] * (n + 1)
    gamma = [0.0] * (n + 1)
    delta = [0.0] * (n + 1)

    # 1. Крайова умова зліва: вільний сплайн S1''(x0) = 0 => c1 = 0
    alpha[1] = 0.0
    beta[1] = 1.0
    gamma[1] = 0.0
    delta[1] = 0.0

    # 2. Рівняння неперервності перших похідних для внутрішніх вузлів (i = 2..n-1)
    for i in range(2, n):
        h_prev = h[i - 2]  # h_{i-1}
        h_curr = h[i - 1]  # h_i

        alpha[i] = h_prev
        beta[i] = 2.0 * (h_prev + h_curr)
        gamma[i] = h_curr
        delta[i] = 3.0 * (
            (y_nodes[i] - y_nodes[i - 1]) / h_curr -
            (y_nodes[i - 1] - y_nodes[i - 2]) / h_prev
        )

    # 3. Крайова умова справа: Sn''(xn) = 0 => 2*cn + 6*dn*hn = 0
    h_n_prev = h[n - 2]
    h_n_curr = h[n - 1]

    alpha[n] = h_n_prev
    beta[n] = 2.0 * (h_n_prev + h_n_curr)
    gamma[n] = 0.0
    delta[n] = 3.0 * (
        (y_nodes[n] - y_nodes[n - 1]) / h_n_curr -
        (y_nodes[n - 1] - y_nodes[n - 2]) / h_n_prev
    )

    return alpha, beta, gamma, delta, h