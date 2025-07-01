from src.main import main


def test_main():
    json_convert_views_func = "from views.py"
    spending_by_category_func = "from reports.py"
    json_convert_services_func = "from services.py"

    result = main(json_convert_views_func, spending_by_category_func, json_convert_services_func)
    assert result == """Веб-страницы. Главная.\n from views.py \n
    Сервисы. Выгодные категории повышенного кешбэка.\n from reports.py \n
    Отчеты. Траты по категории. \n from services.py"""
