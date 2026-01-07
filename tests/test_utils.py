import pytest
from unittest.mock import patch, MagicMock
import pandas as pd
import datetime
import json

from src.utils import (
    get_greeting,
    open_xlsx,
    filter_operations,
    get_cards,
    get_top_transactions,
    open_user_settings,
    get_currency_rates,
    get_stock_prices
)

@pytest.mark.parametrize(
    "mock_hour,expected_greeting",
    [
        (6, "Доброе утро"),
        (13, "Добрый день"),
        (19, "Добрый вечер"),
        (2, "Доброй ночи"),
    ]
)
def test_get_greeting_param(mock_hour, expected_greeting):

    mock_now = datetime.datetime(2026, 1, 1, mock_hour, 0, 0)

    with patch("src.utils.datetime.datetime") as mock_datetime:
        mock_datetime.now.return_value = mock_now

        mock_datetime.strptime = datetime.datetime.strptime
        mock_datetime.side_effect = lambda *args, **kwargs: datetime.datetime(*args, **kwargs)

        with patch("src.utils.logger") as mock_logger:
            greeting = get_greeting()
            assert greeting == expected_greeting
            mock_logger.info.assert_called()

def test_open_xlsx():
    mock_data = pd.DataFrame({
        "Дата операции": ["01.01.2026 12:00:00", "02.01.2026 15:30:00"],
        "Сумма операции": [100, -50],
        "Категория": ["Еда", "Транспорт"]
    })

    with patch("src.utils.pd.read_excel", return_value=mock_data):
        with patch("src.utils.logger") as mock_logger:
            df = open_xlsx()
            assert isinstance(df, pd.DataFrame)
            assert pd.api.types.is_datetime64_any_dtype(df["Дата операции"])
            assert mock_logger.info.called

def test_filter_operations():
    mock_df = pd.DataFrame({
        "Дата операции": pd.to_datetime(["2026-01-01", "2026-01-15", "2026-02-01"]),
        "Сумма операции": [-100, 200, -50]
    })

    with patch("src.utils.open_xlsx", return_value=mock_df):
        with patch("src.utils.logger") as mock_logger:
            filtered = filter_operations("2026-01-20 00:00:00")
            assert len(filtered) == 2
            assert mock_logger.info.called

def test_get_cards():
    mock_df = pd.DataFrame({
        "Дата операции": pd.to_datetime(["2026-01-01", "2026-01-15"]),
        "Сумма операции": [-100, -200],
        "Номер карты": ["1111-2222-3333-4444", "5555-6666-7777-8888"]
    })

    with patch("src.utils.filter_operations", return_value=mock_df):
        with patch("src.utils.logger") as mock_logger:
            cards = get_cards("2026-01-20 00:00:00")
            assert len(cards) == 2
            assert all("total_spent" in c and "cashback" in c for c in cards)
            assert mock_logger.info.called

def test_get_top_transactions():
    mock_df = pd.DataFrame({
        "Дата операции": pd.to_datetime(["2026-01-01", "2026-01-15", "2026-01-20"]),
        "Сумма операции": [-100, -300, -50],
        "Категория": ["Еда", "Транспорт", "Развлечения"],
        "Описание": ["A", "B", "C"]
    })

    with patch("src.utils.filter_operations", return_value=mock_df):
        with patch("src.utils.logger") as mock_logger:
            top = get_top_transactions("2026-01-20 00:00:00")
            assert len(top) == 3
            assert top[0]["amount"] == 300
            assert mock_logger.info.called

def test_open_user_settings():
    mock_settings = {"user_currencies": ["USD", "EUR"], "user_stocks": ["AAPL", "TSLA"]}
    with patch("builtins.open", new_callable=MagicMock) as mock_file:
        mock_file.return_value.__enter__.return_value.read.return_value = json.dumps(mock_settings)
        with patch("src.utils.logger") as mock_logger:
            settings = open_user_settings()
            assert settings == mock_settings
            assert mock_logger.info.called

def test_get_currency_rates():
    mock_settings = {"user_currencies": ["USD", "EUR"]}
    with patch("src.utils.open_user_settings", return_value=mock_settings):
        with patch("src.utils.requests.request") as mock_request:
            mock_request.return_value.json.side_effect = [
                {"rates": {"RUB": 80}}, {"rates": {"RUB": 90}}
            ]
            with patch("src.utils.logger") as mock_logger:
                rates = get_currency_rates()
                assert rates == [{"currency": "USD", "rate": 80}, {"currency": "EUR", "rate": 90}]
                assert mock_logger.info.called

def test_get_stock_prices():
    mock_settings = {"user_stocks": ["AAPL", "TSLA"]}
    mock_response_data = {
        "data": [
            {"symbol": "AAPL", "close": 150.5},
            {"symbol": "TSLA", "close": 700.1}
        ]
    }
    with patch("src.utils.open_user_settings", return_value=mock_settings):
        with patch("src.utils.requests.get") as mock_get:
            mock_get.return_value.json.return_value = mock_response_data
            with patch("src.utils.logger") as mock_logger:
                stocks = get_stock_prices()
                assert stocks == [{"stock": "AAPL", "price": 150.5}, {"stock": "TSLA", "price": 700.1}]
                assert mock_logger.info.called