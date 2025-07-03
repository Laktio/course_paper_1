from src.views import json_convert_views, stock_prices_variable
from src.reports import spending_by_category, df_converter_var
from src.services import json_convert_services, caregory_filter_variable



def main(json_convert_views_func, spending_by_category_func, json_convert_services_func):

    return f"""Веб-страницы. Главная.\n {json_convert_views_func} \n
    Сервисы. Выгодные категории повышенного кешбэка.\n {spending_by_category_func} \n
    Отчеты. Траты по категории. \n {json_convert_services_func}"""


json_convert_views_func = json_convert_views(stock_prices_variable)

input_category = "Супермаркеты"
input_date = "12.12.2021"
spending_by_category_func = spending_by_category(df_converter_var, input_category, input_date)

json_convert_services_func = json_convert_services(caregory_filter_variable)

main_variable = main(json_convert_views_func, spending_by_category_func, json_convert_services_func)

# print(main_variable)
