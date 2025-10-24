from factorial import fact_recursive, fact_recursive_lru, fact_iterative, fact_iterative_lru
from utils import generate_random_numbers, draw_plot
from benchmark import benchmark


def main():
    """
    Проведение бенчмарков со сравнениями разных версий факториала:
    1) Сравнение lru_cache РекФакт и НРекФакт
    2) Сравнение n/a optimization РекФакт и НРекФакт
    3) Сравнение РекФакт (lru_cache) и РекФакт n/a optimization
    4) Сравнение НРекФакт (lru_cache) и НРекФакт n/a optimization

    :return: None
    """
    test_numbers = generate_random_numbers(size=10)
    print('Числа:', *test_numbers)

    print('\nИспытание 1 (рекурсия с мемоизацией / итеративный алгоритм с мемоизацией')
    rec_lru_results, iter_lru_results = benchmark(test_numbers, fact_recursive_lru, fact_iterative_lru)
    for n, r1, r2 in zip(test_numbers, rec_lru_results, iter_lru_results):
        print(f'n={n}; рекурсия с мемоизацией {r1:.10f} с, итерация с мемоизацией {r2:.10f} с')
    draw_plot(test_numbers, rec_lru_results, iter_lru_results,
              label1='Рекурсия с мемоизацией', label2='Итерация с мемоизацией',
              title='Сравнение lru_cache РекФакт и НРекФакт')

    print('\nИспытание 2 (рекурсия без мемоизации / итеративный алгоритм без мемоизации')
    rec_results, iter_results = benchmark(test_numbers, fact_recursive, fact_iterative)
    for n, r1, r2 in zip(test_numbers, rec_results, iter_results):
        print(f'n={n}; рекурсия без мемоизации {r1:.10f} с, итерация без мемоизации {r2:.10f} с')
    draw_plot(test_numbers, rec_results, iter_results,
              label1='Рекурсия без мемоизации', label2='Итерация без мемоизации',
              title='Сравнение n/a optimization РекФакт и НРекФакт')

    print('\nИспытание 3 (рекурсия с мемоизацией / рекурсия без мемоизации')
    rec_lru_results, rec_results = benchmark(test_numbers, fact_recursive_lru, fact_recursive)
    for n, r1, r2 in zip(test_numbers, rec_lru_results, rec_results):
        print(f'n={n}; рекурсия с мемоизацией {r1:.10f} с, рекурсия без мемоизации {r2:.10f} с')
    draw_plot(test_numbers, rec_lru_results, rec_results,
              label1='Рекурсия с мемоизацией', label2='Рекурсия без мемоизации',
              title='Сравнение РекФакт (lru_cache) и РекФакт n/a optimization')

    print('\nИспытание 4 (итеративный алгоритм с мемоизацией / итеративный алгоритм без мемоизации')
    iter_lru_results, iter_results = benchmark(test_numbers, fact_iterative_lru, fact_iterative)
    for n, r1, r2 in zip(test_numbers, iter_lru_results, iter_results):
        print(f'n={n}; итерация с мемоизацией {r1:.10f} с, итерация без мемоизации {r2:.10f} с')
    draw_plot(test_numbers, iter_lru_results, iter_results,
              label1='Итерация с мемоизацией', label2='Итерация без мемоизации',
              title='Сравнение НРекФакт (lru_cache) и НРекФакт n/a optimization')

    print('\nПовтор испытания 1 (рекурсия с мемоизацией / итеративный алгоритм с мемоизацией')
    rec_lru_results, iter_lru_results = benchmark(test_numbers, fact_recursive_lru, fact_iterative_lru)
    for n, r1, r2 in zip(test_numbers, rec_lru_results, iter_lru_results):
        print(f'n={n}; рекурсия с мемоизацией {r1:.10f} с, итерация с мемоизацией {r2:.10f} с')
    draw_plot(test_numbers, rec_lru_results, iter_lru_results,
              label1='Рекурсия с мемоизацией', label2='Итерация с мемоизацией',
              title='(повтор) Сравнение lru_cache РекФакт и НРекФакт')

if __name__ == '__main__':
    main()
