import json
import logging

from src.utils import get_cards, get_currency_rates, get_greeting, get_stock_prices, get_top_transactions

logger = logging.getLogger("views.log")
file_handler = logging.FileHandler("views.log", "w")
file_formatter = logging.Formatter("%(asctime)s %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)


def main_page(date_time: str) -> str:
    """Функция, определяющая логику главной страницы"""
    greeting = get_greeting()
    cards = get_cards(date_time)
    top_transactions = get_top_transactions(date_time)
    currency_rates = get_currency_rates()
    stock_prices = get_stock_prices()

    dict_answer = {
        "greeting": greeting,
        "cards": cards,
        "top_transactions": top_transactions,
        "currency_rates": currency_rates,
        "stock_prices": stock_prices,
    }

    json_answer = json.dumps(dict_answer, ensure_ascii=False, indent=4)
    logger.info("Функция (main_page) выполнена")
    return json_answer
