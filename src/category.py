from typing import List

from src.product import Product


class Category:
    """Класс для представления категории товаров."""

    name: str
    description: str
    products: List[Product]

    # Атрибуты класса (общие для всех экземпляров)
    category_count: int = 0
    product_count: int = 0

    def __init__(self, name: str, description: str, products: List[Product]):
        self.name = name
        self.description = description
        self.products = products

        Category.category_count += 1
        Category.product_count += len(self.products)
