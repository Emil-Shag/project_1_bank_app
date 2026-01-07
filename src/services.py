import math
from typing import Any, Dict, List

import pandas as pd

from src.utils import open_xlsx


def prepare_transactions() -> List[Dict]:
    """Функция, приводящая xlsx файл к необходимому виду"""
    data = open_xlsx()
    columns = ["Дата платежа", "Сумма операции"]
    data_filtered = data[columns]
    result = data_filtered.to_dict(orient="records")
    return result


def investment_bank(month: str, transactions: List[Dict[str, Any]], limit: int) -> float:
    """Функция, подсчитывающая сумму, которую удалось бы отложить в «Инвесткопилку»"""
    invest_sum = 0
    required_year, required_month = map(int, month.split("-"))
    for transaction in transactions:
        date_from_list = transaction["Дата платежа"]
        date = pd.to_datetime(date_from_list, format="%d.%m.%Y")
        if date.year == required_year and date.month == required_month and transaction["Сумма операции"] < 0:
            invest_num = math.ceil(abs(transaction["Сумма операции"]) / limit) * limit - abs(
                transaction["Сумма операции"]
            )
            invest_sum += invest_num
    return round(invest_sum, 2)
