import pytest
from src.utils.data_provider import load_test_data

test_data = load_test_data("get_item_data.json")


@pytest.mark.parametrize("test_case", test_data)
def test_get_item(api_client, created_items, unique_seller_id, test_case):
    """Тестирование получения объявления по ID"""

    item_id = test_case["item_id"]
    create_payload = None

    if test_case.get("setup_required"):
        create_payload = {
            "sellerID": unique_seller_id,
            "name": "Тестовый товар для получения",
            "price": 50000,
            "statistics": {"likes": 10, "viewCount": 100, "contacts": 5},
        }

        create_result = api_client.create_item(create_payload)

        assert create_result["status_code"] == 200, (
            f"Тест: {test_case['name']}\n"
            f"Ожидался статус: 200\n"
            f"Получен статус: {create_result['status_code']}\n"
            f"Ответ: {create_result['data']}"
        )

        assert "id" in create_result["data"], (
            f"Тест: {test_case['name']}\nОтвет должен содержать поле id\n"
            f"Ответ: {create_result['data']}"
        )

        item_id = create_result["data"]["id"]
        created_items.append(item_id)

    response = api_client.get_item(item_id)

    assert response.status_code == test_case["expected_status"], (
        f"Тест: {test_case['name']}\n"
        f"Ожидался статус: {test_case['expected_status']}\n"
        f"Получен статус: {response.status_code}\n"
        f"Ответ: {response.text}"
    )

    if response.status_code == 200:
        data = response.json()
        assert isinstance(
            data, list
        ), f"Тест: {test_case['name']}\nОтвет должен быть массивом\nОтвет: {data}"

        if len(data) > 0:
            item_data = data[0]
            assert (
                "id" in item_data
            ), f"Тест: {test_case['name']}\nОтвет должен содержать поле Идентикификатор\nОтвет: {item_data}"
            assert (
                "sellerId" in item_data
            ), f"Тест: {test_case['name']}\nОтвет должен содержать поле Айди продавца\nОтвет: {item_data}"
            assert (
                "name" in item_data
            ), f"Тест: {test_case['name']}\nОтвет должен содержать поле Название\nОтвет: {item_data}"
            assert (
                "price" in item_data
            ), f"Тест: {test_case['name']}\nОтвет должен содержать поле Цена\nОтвет: {item_data}"

            if create_payload:
                assert item_data["sellerId"] == create_payload["sellerID"], (
                    f"Тест: {test_case['name']}\nАйди продавца не совпадает\n"
                    f"Ожидалось: {create_payload['sellerID']}, Получено: {item_data['sellerId']}"
                )
                assert item_data["name"] == create_payload["name"], (
                    f"Тест: {test_case['name']}\nНазвание не совпадает\n"
                    f"Ожидалось: {create_payload['name']}, Получено: {item_data['name']}"
                )
                assert item_data["price"] == create_payload["price"], (
                    f"Тест: {test_case['name']}\nЦена не совпадает\n"
                    f"Ожидалось: {create_payload['price']}, Получено: {item_data['price']}"
                )
                assert (
                    item_data.get("statistics", {}).get("likes")
                    == create_payload["statistics"]["likes"]
                ), (
                    f"Тест: {test_case['name']}\nЛайки не совпадают\n"
                    f"Ожидалось: {create_payload['statistics']['likes']}, Получено: {item_data.get('statistics', {}).get('likes')}"
                )
                assert (
                    item_data.get("statistics", {}).get("viewCount")
                    == create_payload["statistics"]["viewCount"]
                ), (
                    f"Тест: {test_case['name']}\nПросмотры не совпадают\n"
                    f"Ожидалось: {create_payload['statistics']['viewCount']}, Получено: {item_data.get('statistics', {}).get('viewCount')}"
                )
                assert (
                    item_data.get("statistics", {}).get("contacts")
                    == create_payload["statistics"]["contacts"]
                ), (
                    f"Тест: {test_case['name']}\nКонтакты не совпадают\n"
                    f"Ожидалось: {create_payload['statistics']['contacts']}, Получено: {item_data.get('statistics', {}).get('contacts')}"
                )
