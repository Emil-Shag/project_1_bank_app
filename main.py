from src.views import main_page
from src.services import prepare_transactions, investment_bank

if __name__ == "__main__":
    result_views = main_page(input("Введите строку с датой и временем в формате YYYY-MM-DD HH:MM:SS"))
    print(result_views)

    a = investment_bank("2021-12", prepare_transactions(), 50)
    print(a)