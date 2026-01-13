import json
from unittest.mock import patch

import pytest

from src.views import main_page


@pytest.fixture
def sample_date_time():
    return "2026-01-20 00:00:00"


def test_main_page_basic(sample_date_time):

    mock_greeting = "Добрый день"
    mock_cards = [{"last_digits": "4444", "total_spent": 300, "cashback": 3}]
    mock_top_transactions = [{"date": "20.01.2026", "amount": 200, "category": "Еда", "description": "A"}]
    mock_currency_rates = [{"currency": "USD", "rate": 80}]
    mock_stock_prices = [{"stock": "AAPL", "price": 150.5}]

    with (
        patch("src.views.get_greeting", return_value=mock_greeting) as mock_greet,
        patch("src.views.get_cards", return_value=mock_cards) as mock_cards_func,
        patch("src.views.get_top_transactions", return_value=mock_top_transactions) as mock_top,
        patch("src.views.get_currency_rates", return_value=mock_currency_rates) as mock_rates,
        patch("src.views.get_stock_prices", return_value=mock_stock_prices) as mock_stocks,
        patch("src.views.logger") as mock_logger,
    ):

        result_json = main_page(sample_date_time)
        result = json.loads(result_json)

        assert result["greeting"] == mock_greeting
        assert result["cards"] == mock_cards
        assert result["top_transactions"] == mock_top_transactions
        assert result["currency_rates"] == mock_currency_rates
        assert result["stock_prices"] == mock_stock_prices

        mock_greet.assert_called_once()
        mock_cards_func.assert_called_once_with(sample_date_time)
        mock_top.assert_called_once_with(sample_date_time)
        mock_rates.assert_called_once()
        mock_stocks.assert_called_once()

        mock_logger.info.assert_called_once_with("Функция (main_page) выполнена")
