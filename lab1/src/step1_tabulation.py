import math
import os


def f(x):
  """Досліджувана трансцендентна функція."""
  return math.sin(x) * math.exp(-0.2 * x)


def generate_and_save_nodes(x0, xn, n, output_path="data/nodes.txt"):
  os.makedirs(os.path.dirname(output_path), exist_ok=True)
  h = (xn - x0) / n

  x_nodes = [x0 + i * h for i in range(n + 1)]
  y_nodes = [f(x) for x in x_nodes]

  with open(output_path, "w", encoding="utf-8") as file:
    file.write("i\tx_i\t\ty_i\n")
    for i in range(n + 1):
      file.write(f"{i}\t{x_nodes[i]:.6f}\t{y_nodes[i]:.6f}\n")

  return x_nodes, y_nodes