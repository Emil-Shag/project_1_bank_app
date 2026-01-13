import logging
import math
from typing import Any, Dict, List

import pandas as pd

from src.utils import open_xlsx

logger = logging.getLogger("services.log")
file_handler = logging.FileHandler("services.log", "w")
file_formatter = logging.Formatter("%(asctime)s %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)


def prepare_transactions() -> List[Dict]:
    """Функция, приводящая xlsx файл к необходимому виду"""
    data = open_xlsx()
    columns = ["Дата платежа", "Сумма операции"]
    data_filtered = data[columns]
    result = data_filtered.to_dict(orient="records")
    logger.info("Функция (prepare_transactions) открыла файл и оставила нужные колонки")
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
    logger.info("Функция (investment_bank) подсчитала сумму, которую удалось бы отложить в копилку")
    return round(invest_sum, 2)
