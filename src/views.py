import datetime
import json
import requests
import pandas as pd
from dotenv import load_dotenv
import os


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
greeting = greeting(today) # для п.1 задания


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
    """Функция принимает словарь и дополняет его информацией по кэшбэку"""
    sum_operation = sum_operation_dict_func
    for key, value in sum_operation.items():
        if key == 'cards':
            for i in value:
                cashback_operation = i.get('total_spent')/100
                i["cashback"] = cashback_operation

    return sum_operation

cashback = cashback(sum_operation_dict) # для п.2 задания (приветствие + операции по кратам с кэшбэком)
# print(cashback(sum_operation_dict(date_period_operations(path, input_date), card_operation_dict(date_period_operations(path, input_date), greeting(today)))))


def top_five(date_period_operations_func, cashback_func):
    """Функция принимает словарь и дополняет его ключом и значениями по топ 5 операциям по сумме платежа"""
    start_dict = date_period_operations_func
    start_dict_sorted = sorted(start_dict, key=lambda x: x['Сумма операции с округлением'], reverse=True)
    start_dict_top_five = []
    final_dict = {"top_transactions": []}
    for i in range(5):
        start_dict_top_five.append(start_dict_sorted[i])
    for operation in start_dict_top_five:
        a = {}
        a["date"] = operation['Дата платежа']
        a["amount"] = operation['Сумма операции с округлением']
        a["category"] = operation['Категория']
        a["description"] = operation['Описание']
        final_dict["top_transactions"].append(a)
    cashback = cashback_func
    cashback.update(final_dict)

    return cashback

top_five = top_five(date_period_operations, cashback)
# print(top_five)


def currency_rates(url_path, top_five_func):
    """Функция принимет URL сайта с курсом валют и выводит актуальную цену на USD и EUR и добавляет в словарь отчета"""
    response = requests.get(url_path)
    result = response.json()
    usd = result['Valute']['USD']['Value']
    eur = result['Valute']['EUR']['Value']

    work_piece_dict = [{"currency": "USD", "rate": usd}, {"currency": "EUR", "rate": eur}]
    final_dict = {"currency_rates": work_piece_dict}
    top_five_func.update(final_dict)


    return top_five_func


url = "https://www.cbr-xml-daily.ru/daily_json.js"
currency_rates = currency_rates(url, top_five)

# print(currency_rates)


def stock_prices():
    url = "https://financialmodelingprep.com/stable/price-target-latest-news?page=0&limit=10"

    load_dotenv()
    api_key = os.getenv("API_KEY")

    headers = {"apikey": api_key}

    response = requests.get(url, headers=headers)

    # status_code = response.status_code
    result = response.json()

    return result

stock_prices = stock_prices()

print(stock_prices)



def json_convert(final_dict:dict):
    """Функция принимает словарь и выдает объект JSON"""
    final_dict_info = final_dict
    json_convert_info = json.dumps(final_dict_info, ensure_ascii=False)
    return json_convert_info

json_convert = json_convert(cashback)

# print(json_convert)


