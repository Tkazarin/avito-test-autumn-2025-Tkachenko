import pytest
import random
from src.api_client import ApiClient


@pytest.fixture(scope="session")
def api_client():
    base_url = "https://qa-internship.avito.com"
    return ApiClient(base_url)


@pytest.fixture
def unique_seller_id():
    """Генерация уникального sellerID для тестов"""
    return random.randint(111111, 999999)


@pytest.fixture
def created_items():
    """Фикстура для хранения созданных объявлений"""
    return []


import pytest


@pytest.fixture(autouse=True)
def cleanup_after_test(api_client, created_items):
    """Автоматическая очистка созданных объявлений после каждого теста"""
    yield
    if not created_items:
        return

    for item_id in created_items[:]:
        try:
            resp = api_client.delete_item(item_id)
            code = None
            if isinstance(resp, dict):
                code = resp.get("status_code") or getattr(
                    resp.get("response", None), "status_code", None
                )
            else:
                code = getattr(resp, "status_code", None)

            if code == 200:
                print(f"Удалено {item_id}")
            else:
                print(f"Не удалось удалить {item_id}, статус {code}")
        except Exception as e:
            print(f"Ошибка при удалении {item_id}: {e}")

    created_items.clear()
