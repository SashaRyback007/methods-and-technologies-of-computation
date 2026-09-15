def solve_thomas(alpha, beta, gamma, delta, n):
    """
    Розв'язок тридіагональної СЛАР методом прогонки.
    Повертає знайдений вектор c розмірністю n + 1 (індекси 1..n).
    """
    A = [0.0] * (n + 1)
    B = [0.0] * (n + 1)
    c = [0.0] * (n + 1)

    # Пряма прогонка (знаходження коефіцієнтів A_i, B_i)
    A[1] = -gamma[1] / beta[1]
    B[1] = delta[1] / beta[1]

    for i in range(2, n):
        denom = alpha[i] * A[i - 1] + beta[i]
        A[i] = -gamma[i] / denom
        B[i] = (delta[i] - alpha[i] * B[i - 1]) / denom

    # Зворотна прогонка (обчислення c_n, c_{n-1}, ..., c_1)
    denom_n = alpha[n] * A[n - 1] + beta[n]
    c[n] = (delta[n] - alpha[n] * B[n - 1]) / denom_n

    for i in range(n - 1, 0, -1):
        c[i] = A[i] * c[i + 1] + B[i]

    return c