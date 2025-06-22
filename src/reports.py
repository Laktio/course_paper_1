import datetime
import json
from typing import Optional
import pandas as pd


def df_converter(path):
    with open(path, encoding="utf-8"):
        reader = pd.read_excel(path)

    return reader

path = "C:\\Users\\ber_l\\OneDrive\\Рабочий стол\\Python\\Projects\\PythonProject\\data\\operations.xlsx"
df_converter = df_converter(path)

# print(df_converter)


def spending_by_category(transactions: pd.DataFrame,
                         category: str,
                         date: Optional[str] = None) -> pd.DataFrame:
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
    filter_by_date = list(filter(lambda x: str(x['Дата платежа']) in date_list_str, operation_list))

    filter_by_date_df = pd.DataFrame.from_dict(filter_by_date)

    return filter_by_date_df

input_category = "Супермаркеты"
input_date = "12.12.2021"
spending_by_category = spending_by_category(df_converter, input_category, input_date)

print(spending_by_category)