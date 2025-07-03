
from unittest.mock import patch

import pytest


from src.views import (
    card_operation_dict,
    cashback,
    currency_rates,
    date_period_operations,
    greeting,
    json_convert_views,
    stock_prices,
    sum_operation_dict,
    top_five
)


def test_greeting():
    result = greeting("10:20:21")
    assert result == "Доброе утро"


def test_date_period_operations():
    input_date = "2020-10-12 10:20:21"
    path = "C:\\Users\\ber_l\\OneDrive\\Рабочий стол\\Python\\Projects\\PythonProject\\data\\operations.xlsx"
    result = date_period_operations(path, input_date)

    assert result[0]["Дата платежа"] == "12.10.2020"


def test_card_operation_dict():
    date_period_operations_func = []
    greeting_func = "Доброе утро"
    result = card_operation_dict(date_period_operations_func, greeting_func)
    assert result["cards"] == []


def test_sum_operation_dict():
    date_period_operations_func = []
    card_operation_dict_func = {}
    result = sum_operation_dict(date_period_operations_func, card_operation_dict_func)
    assert result == {}


def test_cashback():
    sum_operation_dict_func = {}
    result = cashback(sum_operation_dict_func)
    assert result == {}


@pytest.fixture
def test_list_of_dict() -> list:
    return [
        {
            "Дата платежа": "12.10.2020",
            "Номер карты": "*7197",
            "Статус": "OK",
            "Сумма операции": -92.0,
            "Валюта операции": "RUB",
            "Сумма платежа": -92.0,
            "Валюта платежа": "RUB",
            "Кэшбэк": "nan",
            "Категория": "Фастфуд",
            "MCC": 5814.0,
            "Описание": "Rumyanyj Khleb",
            "Бонусы (включая кэшбэк)": 1,
            "Округление на инвесткопилку": 0,
            "Сумма операции с округлением": 92.0,
        },
        {
            "Дата платежа": "12.10.2020",
            "Номер карты": "*7197",
            "Статус": "OK",
            "Сумма операции": -120.0,
            "Валюта операции": "RUB",
            "Сумма платежа": -120.0,
            "Валюта платежа": "RUB",
            "Кэшбэк": "nan",
            "Категория": "Фастфуд",
            "MCC": 5814.0,
            "Описание": "Kofe s sobojj",
            "Бонусы (включая кэшбэк)": 2,
            "Округление на инвесткопилку": 0,
            "Сумма операции с округлением": 120.0,
        },
        {
            "Дата платежа": "12.10.2020",
            "Номер карты": "*7197",
            "Статус": "OK",
            "Сумма операции": -163.98,
            "Валюта операции": "RUB",
            "Сумма платежа": -163.98,
            "Валюта платежа": "RUB",
            "Кэшбэк": "nan",
            "Категория": "Супермаркеты",
            "MCC": 5411.0,
            "Описание": "Магнит",
            "Бонусы (включая кэшбэк)": 3,
            "Округление на инвесткопилку": 0,
            "Сумма операции с округлением": 163.98,
        },
        {
            "Дата платежа": "11.10.2020",
            "Номер карты": "*7197",
            "Статус": "OK",
            "Сумма операции": -100.0,
            "Валюта операции": "RUB",
            "Сумма платежа": -100.0,
            "Валюта платежа": "RUB",
            "Кэшбэк": "nan",
            "Категория": "Фастфуд",
            "MCC": 5814.0,
            "Описание": "Kofe s sobojj",
            "Бонусы (включая кэшбэк)": 2,
            "Округление на инвесткопилку": 0,
            "Сумма операции с округлением": 100.0,
        },
        {
            "Дата платежа": "11.10.2020",
            "Номер карты": "*7197",
            "Статус": "OK",
            "Сумма операции": -117.98,
            "Валюта операции": "RUB",
            "Сумма платежа": -117.98,
            "Валюта платежа": "RUB",
            "Кэшбэк": "nan",
            "Категория": "Супермаркеты",
            "MCC": 5411.0,
            "Описание": "Магнит",
            "Бонусы (включая кэшбэк)": 2,
            "Округление на инвесткопилку": 0,
            "Сумма операции с округлением": 117.98,
        },
    ]


def test_top_five(test_list_of_dict):

    result = top_five(test_list_of_dict, {})
    assert result == {
        "top_transactions": [
            {
                "amount": 163.98,
                "category": "Супермаркеты",
                "date": "12.10.2020",
                "description": "Магнит",
            },
            {
                "amount": 120.0,
                "category": "Фастфуд",
                "date": "12.10.2020",
                "description": "Kofe s sobojj",
            },
            {
                "amount": 117.98,
                "category": "Супермаркеты",
                "date": "11.10.2020",
                "description": "Магнит",
            },
            {
                "amount": 100.0,
                "category": "Фастфуд",
                "date": "11.10.2020",
                "description": "Kofe s sobojj",
            },
            {
                "amount": 92.0,
                "category": "Фастфуд",
                "date": "12.10.2020",
                "description": "Rumyanyj Khleb",
            },
        ]
    }


@patch("requests.get")
def test_currency_rates(mock_get):
    mock_get.return_value.json.return_value = {
        "Valute": {"USD": {"Value": ""}, "EUR": {"Value": ""}}
    }
    result = currency_rates("", {})
    assert result == {
        "currency_rates": [
            {"currency": "USD", "rate": ""},
            {"currency": "EUR", "rate": ""},
        ]
    }


@patch("requests.get")
def test_stock_prices(mock_get):
    mock_get.return_value.json.return_value = []
    result = stock_prices({})
    assert result == {"stock_prices": []}


def test_json_convert_views():
    result = json_convert_views({})
    assert result == "{}"
