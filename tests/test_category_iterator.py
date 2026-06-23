from typing import List

import pytest

from src.category import Category
from src.category_iterator import CategoryIterator
from src.product import Product


def test_category_iterator_basic() -> None:
    """Базовая проверка итератора — преобразование в список."""
    p1 = Product("Phone1", "Desc1", 100.0, 5)
    p2 = Product("Phone2", "Desc2", 200.0, 3)
    category = Category("Smartphones", "Desc", [p1, p2])

    iterator = CategoryIterator(category)
    products = list(iterator)

    assert products == [p1, p2]


def test_category_iterator_empty() -> None:
    """Итератор по пустой категории должен вернуть пустой список."""
    category = Category("Empty", "Desc", [])
    iterator = CategoryIterator(category)
    products = list(iterator)
    assert products == []


def test_category_iterator_for_loop() -> None:
    """Проверка работы итератора в цикле for."""
    p1 = Product("Phone1", "Desc1", 100.0, 5)
    p2 = Product("Phone2", "Desc2", 200.0, 3)
    p3 = Product("Phone3", "Desc3", 300.0, 7)
    category = Category("Smartphones", "Desc", [p1, p2, p3])

    iterator = CategoryIterator(category)
    collected: List[Product] = []
    for product in iterator:
        collected.append(product)

    assert collected == [p1, p2, p3]


def test_category_iterator_next_method() -> None:
    """Прямая проверка работы метода __next__."""
    p1 = Product("Phone1", "Desc1", 100.0, 5)
    p2 = Product("Phone2", "Desc2", 200.0, 3)
    category = Category("Smartphones", "Desc", [p1, p2])

    iterator = CategoryIterator(category)

    assert next(iterator) is p1
    assert next(iterator) is p2

    with pytest.raises(StopIteration):
        next(iterator)


def test_category_iterator_exhausted() -> None:
    """После исчерпания итератор должен поднимать StopIteration."""
    p1 = Product("Phone1", "Desc1", 100.0, 5)
    category = Category("Smartphones", "Desc", [p1])

    iterator = CategoryIterator(category)
    list(iterator)  # исчерпываем

    with pytest.raises(StopIteration):
        next(iterator)


def test_category_iterator_returns_product_instances() -> None:
    """Итератор должен возвращать именно объекты Product."""
    p1 = Product("Phone1", "Desc1", 100.0, 5)
    category = Category("Smartphones", "Desc", [p1])

    iterator = CategoryIterator(category)
    for product in iterator:
        assert isinstance(product, Product)


def test_category_iterator_with_fixture(sample_category: Category, sample_products_list: List[Product]) -> None:
    """Проверка итератора с категорией из фикстуры."""
    iterator = CategoryIterator(sample_category)
    products = list(iterator)
    assert products == sample_products_list
    assert len(products) == 3
