import logging
from functions.get_currencies import get_currencies
from logger_dec import logger

file_logger = logging.getLogger('currency_file')
file_logger.setLevel(logging.INFO)
file_handler = logging.FileHandler('logs/currencies.log', mode='w', encoding='utf-8')
file_formatter = logging.Formatter('%(levelname)s: %(message)s')
file_handler.setFormatter(file_formatter)
file_logger.addHandler(file_handler)


@logger(handle=file_logger)
def get_currencies_file(*args, **kwargs):
    return get_currencies(*args, **kwargs)


if __name__ == '__main__':
    try:
        print(get_currencies_file(['USD', 'EUR', 'XYZ']))
    except Exception:
        pass
