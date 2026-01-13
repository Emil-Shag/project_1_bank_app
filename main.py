from src.reports import spending_by_category
from src.services import investment_bank, prepare_transactions
from src.utils import open_xlsx
from src.views import main_page

if __name__ == "__main__":
    result_views = main_page(input("Введите строку с датой и временем в формате YYYY-MM-DD HH:MM:SS"))
    print(result_views)

    result_services = investment_bank("2021-12", prepare_transactions(), 50)
    print(result_services)

    result_reports = spending_by_category(open_xlsx(), "Супермаркеты", "2021-12-31 21:15:58")
    print(result_reports)
