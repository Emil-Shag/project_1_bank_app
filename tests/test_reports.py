import pytest
import pandas as pd
from unittest.mock import patch
from src.reports import spending_by_category

@pytest.fixture
def sample_transactions():
    data = {
        "Дата операции": ["2026-01-01", "2025-12-01", "2025-10-01", "2025-09-01"],
        "Категория": ["Еда", "Еда", "Транспорт", "Еда"],
        "Сумма платежа": [-100, -50, -20, -200]
    }
    return pd.DataFrame(data)

def test_spending_by_category_basic(sample_transactions):
    with patch("src.reports.Path.mkdir") as mock_mkdir, \
         patch("src.reports.pd.DataFrame.to_json") as mock_to_json, \
         patch("src.reports.logger") as mock_logger:
        result = spending_by_category(sample_transactions, "Еда", date="2026-01-02")

        # Исправлено: name должен совпадать
        expected_dates = pd.Series(pd.to_datetime(["2026-01-01", "2025-12-01"]), name="Дата операции")
        pd.testing.assert_series_equal(result["Дата операции"].reset_index(drop=True), expected_dates)

        expected_sums = pd.Series([-100, -50], name="Сумма платежа")
        pd.testing.assert_series_equal(result["Сумма платежа"].reset_index(drop=True), expected_sums)

        mock_mkdir.assert_called_once_with(exist_ok=True)
        mock_to_json.assert_called_once()
        mock_logger.info.assert_called_once_with(
            "Функция (spending_by_category) подсчитала сумму трат по выбранной категории"
        )