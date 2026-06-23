from typing import List

from src.category import Category
from src.product import Product


class CategoryIterator:
    """
    Вспомогательный класс для итерации по товарам одной категории.
    Позволяет перебирать товары в цикле for.
    """

    def __init__(self, category: Category) -> None:
        # Обращаемся к приватному списку через name mangling
        self._products: List[Product] = category._Category__products  # type: ignore[attr-defined]
        self._index: int = 0

    def __iter__(self) -> "CategoryIterator":
        """Возвращает сам объект как итератор."""
        return self

    def __next__(self) -> Product:
        """Возвращает очередной товар категории или поднимает StopIteration."""
        if self._index >= len(self._products):
            raise StopIteration
        product = self._products[self._index]
        self._index += 1
        return product
