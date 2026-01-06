import json

from src.utils import get_cards, get_currency_rates, get_greeting, get_stock_prices, get_top_transactions


def main_page(date_time: str):
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

    return json_answer
