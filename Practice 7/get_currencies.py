import sys

import requests
from logger_dec import logger
from typing import List, Dict, Union


@logger(handle=sys.stdout)
def get_currencies(currency_codes: List[str],
                   url: str = 'https://www.cbr-xml-daily.ru/daily_json.js',
                   timeout: float = 10) -> Dict[str, Union[float, str]]:
    """
    Получить курсы валют по списку кодов

    :param currency_codes: список кодов валют
    :param url: url api, по умолчанию Центробанк
    :param timeout: таймаут запроса в секундах
    :returns: словарь вида {"код валюты": курс} или сообщение о том что код не найден
    :raises ConnectionError: если API недоступен
    :raises ValueError: если тело ответа не является корректным json
    """

    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise ConnectionError(f'API недоступен: {e}')

    try:
        data = response.json()
    except ValueError as e:
        raise ValueError(f'Некорректный JSON: {e}')

    valute = data.get("Valute")
    if not isinstance(valute, dict):
        return {
            code: 'Структура JSON не содержит ключа "Valute"'
            for code in currency_codes
        }

    result = {}

    for code in currency_codes:
        if code not in valute:
            result[code] = f'Код валюты "{code}" не найден'
            continue

        entry = valute[code]
        value = entry.get('Value')

        if not isinstance(value, (int, float)):
            result[code] = f'Некорректный тип курса у "{code}": {type(value).__name__}'
            continue

        result[code] = value

    return result
