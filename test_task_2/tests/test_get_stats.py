import pytest
from src.utils.data_provider import load_test_data

test_data = load_test_data("get_stats_data.json")


@pytest.mark.parametrize("test_case", test_data)
def test_get_stats(api_client, created_items, unique_seller_id, test_case):
    """Тестирование получения статистики по объявлению"""

    item_id = test_case.get("item_id")
    create_payloads = []

    if test_case.get("setup_required"):
        create_payload = {
            "sellerID": unique_seller_id,
            "name": "Тестовый товар для статистики",
            "price": 75000,
            "statistics": {"likes": 15, "viewCount": 150, "contacts": 8},
        }

        create_result = api_client.create_item(create_payload)

        assert create_result["status_code"] == 200, (
            f"Тест: {test_case['name']}\n"
            f"Ожидался статус: 200\n"
            f"Получен статус: {create_result['status_code']}\n"
            f"Ответ: {create_result['data']}"
        )

        assert "id" in create_result["data"], (
            f"Тест: {test_case['name']}\n"
            f"Ответ должен содержать поле id\n"
            f"Ответ: {create_result['data']}"
        )

        item_id = create_result["data"]["id"]
        created_items.append(item_id)
        create_payloads.append(create_payload)

    response = api_client.get_stats(item_id)

    assert response.status_code == test_case["expected_status"], (
        f"Тест: {test_case['name']}\n"
        f"Ожидался статус: {test_case['expected_status']}\n"
        f"Получен статус: {response.status_code}\n"
        f"Ответ: {response.text}"
    )

    if response.status_code == 200:
        data = response.json()
        assert isinstance(data, list), (
            f"Тест: {test_case['name']}\n"
            f"Ответ должен быть списком\n"
            f"Ответ: {data}"
        )

        if len(data) > 0:
            stats = data[0]
            assert "likes" in stats, (
                f"Тест: {test_case['name']}\n" f"Нет поля likes\n" f"Ответ: {stats}"
            )
            assert "viewCount" in stats, (
                f"Тест: {test_case['name']}\n" f"Нет поля viewCount\n" f"Ответ: {stats}"
            )
            assert "contacts" in stats, (
                f"Тест: {test_case['name']}\n" f"Нет поля contacts\n" f"Ответ: {stats}"
            )

        if test_case.get("expected_empty"):
            assert len(data) == 0, (
                f"Тест: {test_case['name']}\n"
                f"Ожидался пустой массив статистики\n"
                f"Ответ: {data}"
            )
