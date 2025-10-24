"""
Вариант 10
"""

from utils import plot_results
from benchmark import benchmark


def main():
    heights = range(2, 19)
    recursive_results, iterative_results = benchmark(heights)

    print("Результаты (сек.):")
    for h, t_rec, t_iter in zip(heights, recursive_results, iterative_results):
        print(f"Высота {h}; рекурсивный алгоритм {t_rec:.6f}, нерекурсивный алгоритм {t_iter:.6f}")

    plot_results(heights, recursive_results, iterative_results)


if __name__ == "__main__":
    main()
