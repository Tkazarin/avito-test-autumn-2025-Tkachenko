import pytest
from src.utils.data_provider import load_test_data

test_data = load_test_data("get_seller_items_data.json")


@pytest.mark.parametrize("test_case", test_data)
def test_get_items_by_seller(api_client, created_items, unique_seller_id, test_case):
    """Тестирование получения объявлений продавца"""

    seller_id = test_case.get("sellerID", unique_seller_id)
    create_payloads = []

    if test_case.get("setup_required"):
        for i in range(2):
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
                f"Тест: {test_case['name']}\n"
                f"Ответ должен содержать поле id\n"
                f"Ответ: {create_result['data']}"
            )

            item_id = create_result["data"]["id"]
            created_items.append(item_id)
            create_payloads.append(create_payload)

    response = api_client.get_items_by_seller(seller_id)

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
            f"Ответ должен быть массивом\n"
            f"Ответ: {data}"
        )

        for item in data:
            assert item["sellerId"] == seller_id, (
                f"Тест: {test_case['name']}\n"
                f"Айди продавца не совпадает\n"
                f"Ожидалось: {seller_id}, Получено: {item.get('sellerId')}"
            )

        if test_case.get("expected_empty"):
            assert len(data) == 0, (
                f"Тест: {test_case['name']}\n"
                f"Ожидался пустой массив объявлений\n"
                f"Ответ: {data}"
            )

        if create_payloads:
            for created, received in zip(create_payloads, data):
                assert received["name"] == created["name"], (
                    f"Тест: {test_case['name']}\n"
                    f"Имя товара не совпадает\n"
                    f"Ожидалось: {created['name']}, Получено: {received['name']}"
                )
                assert received["price"] == created["price"], (
                    f"Тест: {test_case['name']}\n"
                    f"Цена не совпадает\n"
                    f"Ожидалось: {created['price']}, Получено: {received['price']}"
                )
                if "statistics" in received:
                    assert (
                        received["statistics"]["likes"]
                        == created["statistics"]["likes"]
                    ), (
                        f"Тест: {test_case['name']}\n"
                        f"Лайки не совпадают\n"
                        f"Ожидалось: {created['statistics']['likes']}, Получено: {received['statistics']['likes']}"
                    )
                    assert (
                        received["statistics"]["viewCount"]
                        == created["statistics"]["viewCount"]
                    ), (
                        f"Тест: {test_case['name']}\n"
                        f"Просмотры не совпадают\n"
                        f"Ожидалось: {created['statistics']['viewCount']}, Получено: {received['statistics']['viewCount']}"
                    )
                    assert (
                        received["statistics"]["contacts"]
                        == created["statistics"]["contacts"]
                    ), (
                        f"Тест: {test_case['name']}\n"
                        f"Контакты не совпадают\n"
                        f"Ожидалось: {created['statistics']['contacts']}, Получено: {received['statistics']['contacts']}"
                    )
