import requests
from typing import List, Dict, Optional
import cbrapi
from datetime import datetime, timedelta


def get_currency_data(currency_codes: List[str],
                      url: str = 'https://www.cbr-xml-daily.ru/daily_json.js') -> Dict[str, Optional[dict]]:
    """
    Получить данные о валютах с API ЦБ РФ

    :param currency_codes: список символьных кодов
    :param url: API Центробанка
    :raise ConnectionError: при ошибке подключения
    :raise ValueError: при некорректном JSON или структуре данных
    :return: словарь вида: {'код валюты': {'NumCode': 'номерной код', 'CharCode': 'символьный код', 'Nominal': номинал, 'Name': 'название валюты', 'Value': курс}, ... }
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        raise ConnectionError(f'API недоступен: {e}')

    try:
        data = response.json()
    except ValueError as e:
        raise ValueError(f'Некорректный JSON: {e}')

    valutes = data.get('Valute', {})
    result = {}

    for code in currency_codes:
        raw = valutes.get(code)
        if raw is None:
            result[code] = None
            continue

        try:
            result[code] = {
                'NumCode': str(raw['NumCode']),
                'CharCode': str(raw['CharCode']),
                'Nominal': int(raw['Nominal']),
                'Name': str(raw['Name']),
                'Value': float(raw['Value']),
            }
        except (KeyError, ValueError, TypeError) as e:
            raise ValueError(f'Некорректные данные для валюты "{code}": {e}')

    return result


def get_historical_rates(char_code: str, days: int = 90) -> List[List[str | float]]:
    """
    Получает исторические курсы валюты к рублю за последние `days` дней
    с использованием библиотеки cbrapi.

    :param char_code: код валюты
    :param days: количество дней, за которые считаются исторические данные (по умолчанию 90)
    :return: список вида [(дата, курс), ...] в хронологическом порядке
    :raises: ValueError
    """

    end_date = datetime.today()
    start_date = end_date - timedelta(days=days)

    try:
        df = cbrapi.get_time_series(
            symbol=char_code,
            first_date=start_date.strftime('%Y-%m-%d'),
            last_date=end_date.strftime('%Y-%m-%d'),
            period='D'
        )
    except Exception as e:
        raise ValueError(f'Ошибка cbrapi для {char_code}: {e}')

    result = []
    for date, rate in df.items():
        date_str = date.strftime('%d.%m.%Y')
        result.append([date_str, float(rate)])

    return result
