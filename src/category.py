from typing import List

from src.base_store_item import BaseStoreItem
from src.product import Product


class Category(BaseStoreItem):
    """Класс для представления категории товаров."""

    name: str
    description: str
    __products: List[Product]  # приватный атрибут

    category_count: int = 0
    product_count: int = 0

    def __init__(self, name: str, description: str, products: List[Product]):
        self.name = name
        self.description = description
        self.__products = products

        Category.category_count += 1
        Category.product_count += len(self.__products)

    def __str__(self) -> str:
        """Строковое представление категории."""
        total_quantity = sum(product.quantity for product in self.__products)
        return f"{self.name}, количество продуктов: {total_quantity} шт."

    def add_product(self, product: object) -> None:
        """Добавляет продукт в категорию и увеличивает счетчик товаров."""
        if not isinstance(product, Product):
            raise TypeError(
                f"Можно добавлять только объекты класса Product или его наследников, "
                f"получен объект типа {type(product).__name__}"
            )
        self.__products.append(product)
        Category.product_count += 1

    @property
    def products(self) -> str:
        """Геттер, возвращающий строку со списком товаров."""
        result = ""
        for product in self.__products:
            result += f"{product}\n"
        return result
