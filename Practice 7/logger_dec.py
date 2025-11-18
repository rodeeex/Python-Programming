import sys
import logging
import functools


def logger(func=None, *, handle=sys.stdout):
    """Параметризуемый декоратор логирования

    :param func: функция для декорирования
    :param handle: куда логировать
    :returns: декорированная функция
    """

    if func is None:
        return lambda real_func: logger(real_func, handle=handle)

    is_logging_module = isinstance(handle, logging.Logger)

    def write_log_info(message: str):
        if is_logging_module:
            handle.info(message)
        else:
            handle.write(message + '\n')

    def write_log_error(message: str):
        if is_logging_module:
            handle.error(message)
        else:
            handle.write('ERROR: ' + message + '\n')

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        func_name = func.__name__

        write_log_info(f'Начало вызова функции {func_name} с аргументами: args={args}, kwargs={kwargs}')

        try:
            result = func(*args, **kwargs)
            write_log_info(f'Функция {func_name} завершилась успешно. Результат: {result}')
            return result

        except Exception as e:
            write_log_error(f'В функции {func_name} возникло исключение: {e} ({type(e).__name__})')
            raise

    return wrapper
