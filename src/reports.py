import datetime

from typing import Optional

import pandas as pd


def df_converter(path):
    """Функция принимает путь к файлу Excel и выводит DF с содержимым"""
    with open(path, encoding="utf-8"):
        reader = pd.read_excel(path)

    return reader


path = "C:\\Users\\ber_l\\OneDrive\\Рабочий стол\\Python\\Projects\\PythonProject\\data\\operations.xlsx"
df_converter_var = df_converter(path)

# print(df_converter_var)


def spending_by_category(
    transactions: pd.DataFrame, category: str, date: Optional[str] = None
) -> pd.DataFrame:
    """Функция принимает на вход:
    датафрейм с транзакциями,
    название категории,
    опциональную дату.
    Если дата не передана, то берется текущая дата.
    Функция возвращает траты по заданной категории за последние три месяца (от переданной даты).
    """
    if date is None:
        date_obj = datetime.date.today()
    else:
        date_obj = datetime.datetime.strptime(date, "%d.%m.%Y")

    three_months_delta = datetime.timedelta(days=90)
    three_months_ago = date_obj - three_months_delta
    date_list = []
    date_list_str = []
    while three_months_ago < date_obj:
        date_list.append(three_months_ago)
        three_months_ago += datetime.timedelta(days=1)

    for date in date_list:
        date_str = date.strftime("%d.%m.%Y")
        date_list_str.append(date_str)

    operation_list = transactions.to_dict(orient="records")
    filter_by_date = list(
        filter(lambda x: str(x["Дата платежа"]) in date_list_str, operation_list)
    )

    filter_by_category = list(
        filter(lambda x: x["Категория"] == category, filter_by_date)
    )

    filter_df = pd.DataFrame.from_dict(filter_by_category)

    return filter_df


input_category = "Супермаркеты"
input_date = "12.12.2021"
spending_by_category_var = spending_by_category(
    df_converter_var, input_category, input_date
)

# print(spending_by_category_var)
