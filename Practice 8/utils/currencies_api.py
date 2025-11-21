import requests
from typing import List, Dict, Optional


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
        raise ConnectionError(f"API недоступен: {e}")

    try:
        data = response.json()
    except ValueError as e:
        raise ValueError(f"Некорректный JSON: {e}")

    valutes = data.get("Valute", {})
    result = {}

    for code in currency_codes:
        raw = valutes.get(code)
        if raw is None:
            result[code] = None
            continue

        try:
            result[code] = {
                "NumCode": str(raw["NumCode"]),
                "CharCode": str(raw["CharCode"]),
                "Nominal": int(raw["Nominal"]),
                "Name": str(raw["Name"]),
                "Value": float(raw["Value"]),
            }
        except (KeyError, ValueError, TypeError) as e:
            raise ValueError(f"Некорректные данные для валюты '{code}': {e}")

    return result
