import pytest
import pandas as pd
from unittest.mock import patch
from src.services import prepare_transactions, investment_bank


def test_prepare_transactions():

    data = pd.DataFrame({
        "Дата платежа": ["01.01.2026", "05.01.2026"],
        "Сумма операции": [-100, 200],
        "Категория": ["Еда", "Транспорт"]
    })


    with patch("src.services.open_xlsx", return_value=data) as mock_open:

        with patch("src.services.logger") as mock_logger:
            result = prepare_transactions()

            expected = [
                {"Дата платежа": "01.01.2026", "Сумма операции": -100},
                {"Дата платежа": "05.01.2026", "Сумма операции": 200}
            ]
            assert result == expected

            mock_open.assert_called_once()
            mock_logger.info.assert_called_once_with(
                "Функция (prepare_transactions) открыла файл и оставила нужные колонки"
            )

@pytest.fixture
def sample_transactions():
    return [
        {"Дата платежа": "01.01.2026", "Сумма операции": -105},
        {"Дата платежа": "15.01.2026", "Сумма операции": -45},
        {"Дата платежа": "20.01.2026", "Сумма операции": 200},
        {"Дата платежа": "05.02.2026", "Сумма операции": -50},
        {"Дата платежа": "10.02.2026", "Сумма операции": -75},
    ]

@pytest.mark.parametrize(
    "month,limit,expected_sum",
    [
        ("2026-01", 50, 50),
        ("2026-02", 50, 25),
        ("2026-01", 100, 150),
        ("2026-03", 50, 0),
    ]
)
def test_investment_bank_param(sample_transactions, month, limit, expected_sum):
    with patch("src.services.logger") as mock_logger:
        result = investment_bank(month, sample_transactions, limit)
        assert result == expected_sum
        mock_logger.info.assert_called_once_with(
            "Функция (investment_bank) подсчитала сумму, которую удалось бы отложить в копилку"
        )
