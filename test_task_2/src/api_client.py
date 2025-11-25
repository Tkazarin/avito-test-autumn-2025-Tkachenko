import requests
import re
from typing import Dict, Any


class ApiClient:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.session.headers.update(
            {"Content-Type": "application/json", "Accept": "application/json"}
        )

    def create_item(self, payload: dict) -> Dict[str, Any]:
        """
        Создает объявление и возвращает распарсенные данные с ID
        """
        url = f"{self.base_url}/api/1/item"
        response = self.session.post(url, json=payload)

        data = {}
        if response.status_code == 200:
            data = response.json()
            if "status" in data and "Сохранили объявление - " in data["status"]:
                match = re.search(
                    r"Сохранили объявление - ([a-f0-9-]+)", data["status"]
                )
                if match:
                    data["id"] = match.group(1)

        result = {
            "data": data,
            "status_code": response.status_code,
            "response": response,
        }
        return result

    def get_item(self, item_id: str):
        """
        Получает данные объявления по ID
        """
        url = f"{self.base_url}/api/1/item/{item_id}"
        return self.session.get(url)

    def get_items_by_seller(self, seller_id: int):
        """
        Возвращает список объявлений продавца
        """
        url = f"{self.base_url}/api/1/{seller_id}/item"
        return self.session.get(url)

    def get_stats(self, item_id: str):
        """
        Получает статистику по объявлению
        """
        url = f"{self.base_url}/api/1/statistic/{item_id}"
        return self.session.get(url)

    def delete_item(self, item_id: str):
        """
        Удаляет объявление по ID
        """
        url = f"{self.base_url}/api/2/item/{item_id}"
        return self.session.delete(url)
