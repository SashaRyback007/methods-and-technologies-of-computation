import math
import os
from src.step1_tabulation import f
from src.step4_5_spline_coefficients import evaluate_spline_value


def run_fine_tabulation(
    x_nodes, a, b, c, d, n, n_factor=20, output_path="data/tabulation_results.txt"
):
  os.makedirs(os.path.dirname(output_path), exist_ok=True)
  n_eval = n_factor * n
  x0, xn = x_nodes[0], x_nodes[n]
  h_fine = (xn - x0) / n_eval

  x_fine, y_exact, y_spline, errors = [], [], [], []

  for k in range(n_eval + 1):
    xv = x0 + k * h_fine
    ye = f(xv)
    ys = evaluate_spline_value(xv, x_nodes, a, b, c, d, n)
    err = abs(ye - ys)

    x_fine.append(xv)
    y_exact.append(ye)
    y_spline.append(ys)
    errors.append(err)

  with open(output_path, "w", encoding="utf-8") as file:
    file.write("x\tf(x)\tS(x)\tError\n")
    for k in range(n_eval + 1):
      file.write(
          f"{x_fine[k]:.4f}\t{y_exact[k]:.6f}\t{y_spline[k]:.6f}\t{errors[k]:.6e}\n"
      )

  return x_fine, y_exact, y_spline, errors


def save_svg_plot(
    x_data, y1_data, y2_data, title, filename, label1="f(x)", label2="S(x)"
):
  width, height = 800, 450
  pad = 60
  min_x, max_x = min(x_data), max(x_data)

  all_y = y1_data + (y2_data if y2_data else [])
  min_y, max_y = min(all_y), max(all_y)
  if min_y == max_y:
    max_y += 1.0

  def to_svg_x(x):
    return pad + (x - min_x) / (max_x - min_x) * (width - 2 * pad)

  def to_svg_y(y):
    return height - pad - (y - min_y) / (max_y - min_y) * (height - 2 * pad)

  pts1 = " ".join(
      [f"{to_svg_x(x):.1f},{to_svg_y(y):.1f}" for x, y in zip(x_data, y1_data)]
  )
  pts2 = (
      " ".join([
          f"{to_svg_x(x):.1f},{to_svg_y(y):.1f}"
          for x, y in zip(x_data, y2_data)
      ])
      if y2_data
      else ""
  )

  svg = [
      f'<svg width="{width}" height="{height}"'
      ' xmlns="http://www.w3.org/2000/svg">',
      '<rect width="100%" height="100%" fill="white"/>',
      f'<text x="{width/2}" y="30" font-family="Arial" font-size="18"'
      f' text-anchor="middle" font-weight="bold">{title}</text>',
      f'<line x1="{pad}" y1="{height-pad}" x2="{width-pad}" y2="{height-pad}"'
      ' stroke="black" stroke-width="2"/>',
      (
          f'<line x1="{pad}" y1="{pad}" x2="{pad}" y2="{height-pad}"'
          ' stroke="black" stroke-width="2"/>'
      ),
      (
          '<polyline fill="none" stroke="blue" stroke-width="2"'
          f' points="{pts1}"/>'
      ),
  ]

  if pts2:
    svg.append(
        '<polyline fill="none" stroke="red" stroke-dasharray="5,5"'
        f' stroke-width="2" points="{pts2}"/>'
    )

  svg.append("</svg>")

  with open(filename, "w", encoding="utf-8") as f_out:
    f_out.write("\n".join(svg))


def plot_results(
    x_nodes, y_nodes, x_fine, y_exact, y_spline, errors, output_dir="plots"
):
  os.makedirs(output_dir, exist_ok=True)
  save_svg_plot(
      x_fine,
      y_exact,
      y_spline,
      "Кубічний сплайн S(x) (червоний) та точна f(x) (синій)",
      os.path.join(output_dir, "spline_plot.svg"),
  )
  save_svg_plot(
      x_fine,
      errors,
      [],
      "Абсолютна похибка інтерполяції",
      os.path.join(output_dir, "error_plot.svg"),
  )