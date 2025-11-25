import json
import os
import sys

MAX_INT = sys.maxsize


def replace_boundaries(value):
    """Рекурсивно заменяет специальные числовые значения на граничные"""
    if isinstance(value, dict):
        return {k: replace_boundaries(v) for k, v in value.items()}
    elif isinstance(value, list):
        return [replace_boundaries(i) for i in value]
    elif isinstance(value, int):
        if value == 777:
            return MAX_INT
        elif value == 776:
            return MAX_INT + 1
    return value


def load_test_data(file_name: str):
    """Загружает тестовые данные из JSON-файла и применяет замену граничных значений"""
    base_path = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(base_path, "../../tests/data", file_name)
    with open(data_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return replace_boundaries(data)
