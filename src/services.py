import pandas as pd
import json
import src.main


def year_month_filter(path:str, year:str, month:str):
    """Функция принимает путь к файлу с транзакциями, год для анализа,
    месяц для анализа и выводит список словарей с операциями по таблице операций"""
    year_month = month + '.' + year
    with open(path, encoding="utf-8"):
        reader = pd.read_excel(path, index_col=0)
        operation_list = reader.to_dict(orient="records")
        filter_operation_list = list(filter(lambda x: year_month in str(x['Дата платежа']), operation_list))
        return filter_operation_list

input_year = "2021"
input_moth = "06"
path = "C:\\Users\\ber_l\\OneDrive\\Рабочий стол\\Python\\Projects\\PythonProject\\data\\operations.xlsx"
year_month_filter = year_month_filter(path, input_year, input_moth)



def caregory_filter(year_month_filter_func):
    """Функция список словарей всех операций за указанный месяц и год и выводит словарь с указанием в качестве
    ключей категории, а в качестве значений сумму кэшбэка (1руб на каждые 100руб) в этих категориях"""
    category_list = []
    for operation in year_month_filter_func:
        category_operation = {}
        category_operation[operation['Категория']] = operation['Сумма операции с округлением']
        category_list.append(category_operation)
    category_dict = {}
    for i in category_list:
        for key in i:
            try:
                category_dict[key] += round(i[key]/100)
            except:
                category_dict[key] = round(i[key]/100)

    return category_dict

caregory_filter = caregory_filter(year_month_filter)


def json_convert(caregory_filter_func:dict):
    category_dict = caregory_filter_func
    json_category_dict = json.dumps(category_dict, ensure_ascii=False)
    return json_category_dict

json_convert = json_convert(caregory_filter)

# print(json_convert)
