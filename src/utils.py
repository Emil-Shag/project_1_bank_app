import datetime
import json
import os
from typing import Any, Dict, List

import pandas as pd
import requests
from dotenv import load_dotenv

load_dotenv()


def get_greeting() -> str:
    """Функция, выводящая приветствие в зависимости от текущего времени"""
    current_date_time = datetime.datetime.now()
    if 5 <= current_date_time.hour < 12:
        return "Доброе утро"
    if 12 <= current_date_time.hour < 18:
        return "Добрый день"
    if 18 <= current_date_time.hour < 23:
        return "Добрый вечер"
    else:
        return "Доброй ночи"


def open_xlsx() -> pd.DataFrame:
    """Функция, считывающая данные с xlsx файла"""
    excel_data = pd.read_excel("data/operations.xlsx")
    excel_data["Дата операции"] = pd.to_datetime(excel_data["Дата операции"], format="%d.%m.%Y %H:%M:%S")
    return excel_data


def filter_operations(date_time: str) -> pd.DataFrame:
    """Функция, фильтрующая операции по дате"""
    finish_date = datetime.datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S")
    start_date = finish_date.replace(day=1)
    excel_data = open_xlsx()
    filtered_operations = excel_data[
        (excel_data["Дата операции"] >= start_date) & (excel_data["Дата операции"] <= finish_date)
    ]
    return filtered_operations


def get_cards(date_time: str) -> list:
    """Функция, формирующая список карт с общей суммой расходов и кешбэком"""
    filtered_operations = filter_operations(date_time)
    cards_grouped = filtered_operations.groupby("Номер карты")
    sum_operations = cards_grouped["Сумма операции"].sum()
    cards_list = []
    for card_number, total_spent in sum_operations.items():
        cards_list.append(
            {
                "last_digits": card_number[-4:],
                "total_spent": round(abs(total_spent), 2),
                "cashback": round(abs(total_spent) * 0.01, 2),
            }
        )
    return cards_list


def get_top_transactions(date_time: str) -> List[Dict]:
    """Функция, которая выводит топ-5 транзакций по сумме платежа"""
    filtered_operations = filter_operations(date_time)
    filtered_operations["Сумма операции"] = filtered_operations["Сумма операции"].abs()
    filter_by_amount = filtered_operations.sort_values("Сумма операции", ascending=False).head(5)
    top_transactions_list = []
    for _, row in filter_by_amount.iterrows():
        top_transactions_list.append(
            {
                "date": row["Дата операции"].strftime("%d.%m.%Y"),
                "amount": row["Сумма операции"],
                "category": row["Категория"],
                "description": row["Описание"],
            }
        )
    return top_transactions_list


def open_user_settings() -> Any:
    """Функция, открывающая файл с пользовательскими настройками"""
    with open("data/user_settings.json", "r", encoding="utf-8") as f:
        settings = json.load(f)
    return settings


def get_currency_rates() -> List[Dict]:
    """Функция, запрашивающая курс валют"""
    settings = open_user_settings()
    currencies = settings["user_currencies"]
    currency_rates_list = []
    for currency in currencies:
        url = f"https://api.apilayer.com/exchangerates_data/latest?symbols=RUB&base={currency}"
        payload = {}
        headers = {"apikey": os.getenv("API_KEY_1")}
        response = requests.request("GET", url, headers=headers, data=payload)
        rate = response.json()["rates"]["RUB"]
        currency_rates_list.append({"currency": currency, "rate": round(rate, 2)})
    return currency_rates_list


def get_stock_prices() -> List[Dict]:
    """Функция, запрашивающая стоимость акций"""
    settings = open_user_settings()
    stocks = settings["user_stocks"]
    symbols_str = ",".join(stocks)
    api_key = os.getenv("API_KEY_2")
    url = f"https://api.marketstack.com/v1/eod?access_key={api_key}&symbols={symbols_str}&limit=1"
    response = requests.get(url)
    data = response.json().get("data", [])
    stock_prices_list = []
    for i in data:
        stock_prices_list.append({"stock": i["symbol"], "price": float(i["close"])})

    return stock_prices_list
