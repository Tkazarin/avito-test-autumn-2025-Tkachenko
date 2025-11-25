import pytest
import random
from src.utils.data_provider import load_test_data

test_data = load_test_data("create_item_data.json")


@pytest.mark.parametrize("test_case", test_data)
def test_create_item(api_client, created_items, test_case):
    """Тестирование создания объявления"""

    payload = test_case["payload"].copy()

    result = api_client.create_item(payload)

    assert result["status_code"] == test_case["expected_status"], (
        f"Тест: {test_case['name']}\n"
        f"Ожидался статус: {test_case['expected_status']}\n"
        f"Получен статус: {result['status_code']}\n"
        f"Ответ: {result['data']}"
    )

    if result["status_code"] == 200:
        data = result["data"]
        assert "id" in data, "Ответ должен содержать поле id"
        created_items.append(data["id"])


def test_create_duplicate_advertisements_different_ids(api_client, created_items):
    """TC-033 Проверка что одинаковые объявления получают разные ID"""

    payload = {
        "sellerID": 332025,
        "name": "Одинаковый товар",
        "price": 500,
        "statistics": {"likes": 5, "viewCount": 50, "contacts": 2},
    }

    result1 = api_client.create_item(payload)
    assert (
        result1["status_code"] == 200
    ), f"Ожидался статус 200, получен {result1['status_code']}, ответ: {result1['data']}"
    data1 = result1["data"]
    assert "id" in data1, "Ответ должен содержать поле id"
    item_id1 = data1["id"]
    created_items.append(item_id1)

    result2 = api_client.create_item(payload)
    assert (
        result2["status_code"] == 200
    ), f"Ожидался статус 200, получен {result2['status_code']}, ответ: {result2['data']}"
    data2 = result2["data"]
    assert "id" in data2, "Ответ должен содержать поле id"
    item_id2 = data2["id"]
    created_items.append(item_id2)

    assert (
        item_id1 != item_id2
    ), f"ID одинаковых объявлений должны отличаться, но получены одинаковые: {item_id1}"
