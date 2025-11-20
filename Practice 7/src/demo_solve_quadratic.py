import logging
from .logger_dec import logger
from .solve_quadratic import solve_quadratic

file_logger = logging.getLogger('solutions_file')
file_logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler('../logs/solutions.log', mode='w', encoding='utf-8')
file_formatter = logging.Formatter('%(levelname)s: %(message)s')
file_handler.setFormatter(file_formatter)
file_logger.addHandler(file_handler)


@logger(handle=file_logger)
def solve_quadratic_file(a, b, c):
    return solve_quadratic(a, b, c)


if __name__ == '__main__':
    demo = [
        (1, -3, 2),
        (1, 1, 1),
        ('abc', 2, 1),
        (0, 0, 5),
    ]

    for case in demo:
        try:
            solve_quadratic_file(*case)
        except Exception:
            pass
