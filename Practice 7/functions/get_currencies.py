import requests
from typing import List, Dict


def get_currencies(currency_codes: List[str],
                   url: str = 'https://www.cbr-xml-daily.ru/daily_json.js') -> Dict[str, float]:
    """
    Получить курсы валют с API Центробанка России

    :param currency_codes: список кодов валют
    :param url: URL для запроса

    :raise ConnectionError: API недоступен
    :raise ValueError: JSON некорректный
    :raise TypeError: курс валюты имеет неверный тип

    :returns: словарь вида {'код валюты': курс или сообщение об ошибке}
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise ConnectionError(f'API недоступен: {e}')

    try:
        data = response.json()
    except ValueError as e:
        raise ValueError(f'Некорректный JSON: {e}')

    valutes = data.get('Valute', {})

    result = {}
    for code in currency_codes:
        if code in valutes:
            value = valutes[code].get('Value')
            if not isinstance(value, (int, float)):
                raise TypeError(f'Курс валюты {code} имеет неверный тип')
            result[code] = value
        else:
            result[code] = f"Код валюты '{code}' не найден"

    return result
