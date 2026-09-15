from src.step1_tabulation import generate_and_save_nodes
from src.step2_system_builder import build_tridiagonal_system
from src.step3_thomas_algorithm import solve_thomas
from src.step4_5_spline_coefficients import compute_all_coefficients
from src.step6_7_tabulation_and_plots import run_fine_tabulation, plot_results

def main():
    x0 = 0.0
    xn = 10.0
    n = 20  # Кількість інтервалів (n = 20..30 за умовою)

    # Пункт 1: Табуляція вузлів
    x_nodes, y_nodes = generate_and_save_nodes(x0, xn, n)

    # Пункт 2: Побудова матриці СЛАР
    alpha, beta, gamma, delta, h = build_tridiagonal_system(x_nodes, y_nodes, n)

    # Пункти 3-4: Метод прогонки та отримання c_i
    c = solve_thomas(alpha, beta, gamma, delta, n)
    print("Знайдені коефіцієнти c:", [round(val, 4) for val in c[1:]])  # <-- Додайте цей рядок

    # Пункт 5: Обчислення a_i, b_i, d_i
    a, b, c, d = compute_all_coefficients(x_nodes, y_nodes, h, c, n)

    # Пункт 6: Детальна табуляція
    x_fine, y_exact, y_spline, errors = run_fine_tabulation(x_nodes, a, b, c, d, n)

    # Пункт 7: Побудова та експорт графіків
    plot_results(x_nodes, y_nodes, x_fine, y_exact, y_spline, errors)

    print(f"Розрахунок завершено. Максимальна похибка: {max(errors):.6e}")

if __name__ == "__main__":
    main()