from datetime import datetime
from functools import wraps
from pathlib import Path
from typing import Any, Optional

import pandas as pd


def record_result(func: Any) -> Any:
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        df = func(*args, **kwargs)

        reports_dir = Path("reports")
        reports_dir.mkdir(exist_ok=True)
        filename = "reports_result.json"
        file_path = reports_dir / filename
        df.to_json(file_path, orient="records", force_ascii=False, date_format="iso", indent=4)
        return df

    return wrapper


@record_result
def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> pd.DataFrame:
    """Функция, возвращающая траты по заданной категории за последние три месяца"""
    if date is None:
        finish_date = datetime.now()
    else:
        finish_date = pd.to_datetime(date)

    start_date = finish_date - pd.DateOffset(months=3)

    df = transactions.copy()
    df["Дата операции"] = pd.to_datetime(df["Дата операции"])

    filtered_operations = df[
        (df["Категория"] == category) & (df["Дата операции"] >= start_date) & (df["Дата операции"] <= finish_date)
    ]

    filtered_operations = filtered_operations[filtered_operations["Сумма платежа"] < 0]

    return filtered_operations
