from typing import Iterator, List

import pytest

from src.category import Category
from src.product import Product


@pytest.fixture(autouse=True)
def reset_category_counters() -> Iterator[None]:
    """
    Фикстура для сброса атрибутов класса.
    Возвращает Iterator[None], так как использует yield и не передает значение в тест.
    """
    # Сброс перед тестом
    Category.category_count = 0
    Category.product_count = 0

    yield

    # Сброс после теста
    Category.category_count = 0
    Category.product_count = 0


@pytest.fixture
def sample_product() -> Product:
    """Возвращает один стандартный объект Product."""
    return Product("Test Phone", "Great phone", 50000.0, 10)


@pytest.fixture
def sample_products_list() -> List[Product]:
    """Возвращает список из нескольких объектов Product."""
    return [
        Product("Phone 1", "Description 1", 10000.0, 5),
        Product("Phone 2", "Description 2", 20000.0, 8),
        Product("Phone 3", "Description 3", 30000.0, 12),
    ]


@pytest.fixture
def sample_category(sample_products_list: List[Product]) -> Category:
    """
    Возвращает стандартный объект Category,
    зависящий от фикстуры sample_products_list.
    """
    return Category("Smartphones", "Mobile devices for everyday life", sample_products_list)
