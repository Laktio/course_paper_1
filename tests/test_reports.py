import pytest

from src.reports import df_converter, spending_by_category, df_converter_var

@pytest.fixture()
def file_path():
    path = "C:\\Users\\ber_l\\OneDrive\\Рабочий стол\\Python\\Projects\\PythonProject\\data\\operations.xlsx"
    return path


def test_df_converter(file_path):
    result = df_converter(file_path)
    assert result["Дата операции"][0] == "31.12.2021 16:44:00"


def test_spending_by_category():
    input_category = "Супермаркеты"
    input_date = "12.12.2021"
    result = spending_by_category(df_converter_var, input_category, input_date)
    assert result["Дата операции"][0] == "11.12.2021 19:16:58"

