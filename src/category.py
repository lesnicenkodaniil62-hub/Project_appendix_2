from typing import List

from src.product import Product


class Category:
    """Класс для представления категории товаров."""

    name: str
    description: str
    __products: List[Product]  # приватный атрибут

    # Атрибуты класса (общие для всех экземпляров)
    category_count: int = 0
    product_count: int = 0

    def __init__(self, name: str, description: str, products: List[Product]):
        self.name = name
        self.description = description
        self.__products = products  # приватный список

        Category.category_count += 1
        Category.product_count += len(self.__products)

    def add_product(self, product: Product) -> None:
        """Добавляет продукт в категорию и увеличивает счетчик товаров."""
        self.__products.append(product)
        Category.product_count += 1

    @property
    def products(self) -> str:
        """Геттер, возвращающий строку со списком товаров в заданном формате."""
        result = ""
        for product in self.__products:
            result += f"{product.name}, {product.price} руб. Остаток: {product.quantity} шт.\n"
        return result
