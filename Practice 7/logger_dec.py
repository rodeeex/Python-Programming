import sys
import logging
import functools
from typing import Callable, Any
from custom_exceptions import *


def logger(func: Callable = None, *, handle=sys.stdout) -> Callable:
    """
    Параметризуемый декоратор логирования.

    :param func: функция для декорирования
    :param handle: куда логировать
    :returns: декорированная функция
    """
    if func is None:
        return lambda real_func: logger(real_func, handle=handle)

    is_logging_module = isinstance(handle, logging.Logger)

    def write_log(level: str, message: str):
        if is_logging_module:
            if level == 'INFO':
                handle.info(message)
            elif level == 'WARNING':
                handle.warning(message)
            elif level == 'ERROR':
                handle.error(message)
            elif level == 'CRITICAL':
                handle.critical(message)
            else:
                handle.info(message)
        else:
            prefix = '' if level == 'INFO' else f'{level}: '
            handle.write(prefix + message + '\n')

    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        func_name = func.__name__
        write_log('INFO', f'Начало вызова функции {func_name} с аргументами: args={args}, kwargs={kwargs}')
        try:
            result = func(*args, **kwargs)
            write_log('INFO', f'Функция {func_name} завершилась успешно. Результат: {result}')
            return result
        except CriticalError as e:
            write_log('CRITICAL', f'В функции {func_name} возникло критическое исключение: {e} ({type(e).__name__})')
            raise
        except WarningMessage as e:
            write_log('WARNING', f'В функции {func_name} возникло предупреждение: {e} ({type(e).__name__})')
            raise
        except Exception as e:
            write_log('ERROR', f'В функции {func_name} возникло исключение: {e} ({type(e).__name__})')
            raise

    return wrapper
