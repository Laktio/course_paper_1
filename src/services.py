import json

import pandas as pd


def year_month_filter(path: str, year: str, month: str):
    """Функция принимает путь к файлу с транзакциями, год для анализа,
    месяц для анализа и выводит список словарей с операциями по таблице операций"""
    year_month = month + "." + year
    with open(path, encoding="utf-8"):
        reader = pd.read_excel(path, index_col=0)
        operation_list = reader.to_dict(orient="records")
        filter_operation_list = list(
            filter(lambda x: year_month in str(x["Дата платежа"]), operation_list)
        )

        return filter_operation_list


input_year = "2021"
input_moth = "06"
path = "C:\\Users\\ber_l\\OneDrive\\Рабочий стол\\Python\\Projects\\PythonProject\\data\\operations.xlsx"
year_month_filter_variable = year_month_filter(path, input_year, input_moth)

# print (year_month_filter_variable)


def caregory_filter(year_month_filter_func):
    """Функция список словарей всех операций за указанный месяц и год и выводит словарь с указанием в качестве
    ключей категории, а в качестве значений сумму кэшбэка (1руб на каждые 100руб) в этих категориях
    """
    category_list = []
    for operation in year_month_filter_func:
        category_operation = {}
        category_operation[operation["Категория"]] = operation[
            "Сумма операции с округлением"
        ]
        category_list.append(category_operation)
    category_dict = {}
    for i in category_list:
        for key in i:
            try:
                category_dict[key] += round(i[key] / 100)
            except:
                category_dict[key] = round(i[key] / 100)

    return category_dict


caregory_filter_variable = caregory_filter(year_month_filter_variable)

# print (caregory_filter_variable)


def json_convert_services(caregory_filter_func: dict):
    """Функция принимает словарь и выдает объект JSON"""
    category_dict = caregory_filter_func
    json_category_dict = json.dumps(category_dict, ensure_ascii=False)
    return json_category_dict


json_convert_variable = json_convert_services(caregory_filter_variable)

print(json_convert_variable)
