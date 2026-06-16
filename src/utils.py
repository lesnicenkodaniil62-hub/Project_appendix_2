import json
from pathlib import Path
from typing import List

from src.category import Category
from src.product import Product


def load_data_from_json(file_name: str = "products.json") -> List[Category]:
    """
    Читает данные из JSON файла (из папки data) и создает объекты классов.
    """
    # 1. Находим абсолютный путь к текущему файлу (utils.py)
    current_file_path = Path(__file__).resolve()

    # 2. Поднимаемся на одну папку вверх (из src/ в корень проекта)
    project_root = current_file_path.parent.parent

    # 3. Формируем путь к файлу внутри папки data
    json_file_path = project_root / "data" / file_name

    # 4. Проверка на существование файла для понятной ошибки, если что-то не так
    if not json_file_path.exists():
        raise FileNotFoundError(f"Файл не найден! Проверьте путь: {json_file_path}")

    # 5. Чтение и парсинг JSON
    with open(json_file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    categories = []

    for category_data in data:
        products_list = []

        for product_data in category_data.get("products", []):
            product = Product(
                name=product_data["name"],
                description=product_data["description"],
                price=float(product_data["price"]),
                quantity=int(product_data["quantity"]),
            )
            products_list.append(product)

        category = Category(
            name=category_data["name"], description=category_data["description"], products=products_list
        )
        categories.append(category)

    return categories
