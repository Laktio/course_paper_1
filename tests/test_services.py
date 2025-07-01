

from src.services import caregory_filter, json_convert_services, year_month_filter


def test_year_month_filter():
    path = "C:\\Users\\ber_l\\OneDrive\\Рабочий стол\\Python\\Projects\\PythonProject\\data\\operations.xlsx"
    input_year = "2021"
    input_moth = "06"
    result = year_month_filter(path, input_year, input_moth)
    assert result[0]["Дата платежа"] == "30.06.2021"


def test_caregory_filter():
    year_month_filter_func = []
    result = caregory_filter(year_month_filter_func)
    assert result == {}


def test_json_convert_services():
    result = json_convert_services({})
    assert result == "{}"
