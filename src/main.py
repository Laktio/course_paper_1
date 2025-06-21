import datetime
import json

import pandas as pd


def greeting(date:str) -> str:
    """Функция принимает строку с датой в формате YYYY-MM-DD HH:MM:SS и выводит приветствие в зависимости
    от времени суток"""
    date_obj_morning = datetime.datetime.strptime("05:00:00", "%H:%M:%S")
    date_obj_day = datetime.datetime.strptime("11:00:00", "%H:%M:%S")
    date_obj_evening = datetime.datetime.strptime("16:00:00", "%H:%M:%S")
    date_obj_night = datetime.datetime.strptime("21:00:00", "%H:%M:%S")
    date_time = date[-8:]
    date_obj_time = datetime.datetime.strptime(date_time, "%H:%M:%S")

    if date_obj_morning <= date_obj_time <= date_obj_day:
        return "Доброе утро"
    elif date_obj_day <= date_obj_time <= date_obj_evening:
        return "Добрый день"
    elif date_obj_evening <= date_obj_time <= date_obj_night:
        return "Добрый вечер"
    elif date_obj_night <= date_obj_time <= date_obj_time:
        return "Доброй ночи"
    return None


today = str(datetime.datetime.now())[:-7]
greeting = greeting(today)


def date_period_operations(file_path:str, date:str) -> list[dict]:
    """Функция принимает строку с датой в формате YYYY-MM-DD HH:MM:SS и выводит список словарей
    операций с первого числа до указанной даты текущего месяца"""
    date_year = date[:4]
    date_month = date[5:7]
    date_day = date[8:10]
    date_day_list = []
    for date in range(1, int(date_day)+1):
        full_date = str(date).zfill(2) + "." + date_month + "." + date_year
        date_day_list.append(full_date)

    with open(file_path, encoding="utf-8"):
        reader = pd.read_excel(file_path, index_col=0)
        operation_list = reader.to_dict(orient="records")
        filter_operation_list = list(filter(lambda x: str(x['Дата платежа']) in date_day_list, operation_list))

    return filter_operation_list

input_date = "2020-10-12 10:20:21"
path = "C:\\Users\\ber_l\\OneDrive\\Рабочий стол\\Python\\Projects\\PythonProject\\data\\operations.xlsx"
date_period_operations = date_period_operations(path, input_date)
# print(date_period_operations("C:\\Users\\ber_l\\OneDrive\\Рабочий стол\\Python\\Projects\\PythonProject\\data\\operations.xlsx", "2020-10-12 12:20:21"))


def card_operation_dict(date_period_operations_func:list[dict], greeting_func:str) -> dict\
        :
    """Функция принимает список словарей отфильтрованных по дате (функция date_period_operations)
    и выводит словарь с ключом 'cards' и списком словарей в значении с ключами 'last_digits'
    и четырьмя цифрами в значениях"""
    card_operation = {"greeting": greeting_func, "cards": []}
    for operation in date_period_operations_func:
        card_operation["cards"].append({"last_digits":operation['Номер карты']})

    return card_operation

card_operation_dict = card_operation_dict(date_period_operations, greeting)
# card_operation_dict(date_period_operations(path, input_date), greeting(today))


def sum_operation_dict(date_period_operations_func:list[dict], card_operation_dict_func:dict) -> dict:
    """Функция принимает словарь с приветсвием и информацией по номерам карт (функция card_operation_dict)
    и дополняет его информацией по сумме операций под ключом 'total_spent' """
    card_operation = card_operation_dict_func
    for operation in date_period_operations_func:
        sum = operation['Сумма операции с округлением']

        for key, value in card_operation.items():
            if key == 'cards':
                for i in value:
                    i["total_spent"] = sum

    return card_operation

sum_operation_dict = sum_operation_dict(date_period_operations, card_operation_dict)
# print(sum_operation_dict(date_period_operations(path, input_date), card_operation_dict(date_period_operations(path, input_date), greeting(today))))


def cashback(sum_operation_dict_func:dict):
    sum_operation = sum_operation_dict_func
    for key, value in sum_operation.items():
        if key == 'cards':
            for i in value:
                cashback_operation = i.get('total_spent')/100
                i["cashback"] = cashback_operation

    return sum_operation

cashback = cashback(sum_operation_dict)
# print(cashback(sum_operation_dict(date_period_operations(path, input_date), card_operation_dict(date_period_operations(path, input_date), greeting(today)))))


def json_convert(cashback:dict):
    cashback_info = cashback
    json_convert_info = json.dumps(cashback_info)
    return json_convert_info

json_convert = json_convert(cashback)
print(json_convert)


