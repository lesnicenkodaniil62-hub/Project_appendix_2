from typing import List, Tuple

import pytest

from src.category import Category
from src.product import Product

# ==========================================
# ТЕСТЫ ДЛЯ КЛАССА Product
# ==========================================


@pytest.mark.parametrize(
    "name, description, price, quantity",
    [
        ("Samsung Galaxy S23", "256GB, Gray", 180000.0, 5),
        ("Iphone 15", "512GB, Space Gray", 210000.0, 8),
        ("Xiaomi Redmi", "1024GB, Blue", 31000.0, 14),
        ("Тестовый товар", "Описание", 0.0, 0),
    ],
)
def test_product_initialization_parametrized(name: str, description: str, price: float, quantity: int) -> None:
    """Проверка корректности инициализации Product через параметризацию данных."""
    product = Product(name, description, price, quantity)

    assert product.name == name
    assert product.description == description
    assert product.price == price
    assert product.quantity == quantity
    assert isinstance(product.price, float)
    assert isinstance(product.quantity, int)


def test_product_fixture_attributes(sample_product: Product) -> None:
    """Проверка атрибутов продукта, созданного через фикстуру."""
    assert sample_product.name == "Test Phone"
    assert sample_product.description == "Great phone"
    assert sample_product.price == 50000.0
    assert sample_product.quantity == 10


# ==========================================
# ТЕСТЫ ДЛЯ КЛАССА Category
# ==========================================


@pytest.mark.parametrize(
    "cat_name, cat_desc, products_list, expected_len",
    [
        ("Смартфоны", "Мобильные устройства", [Product("P1", "D1", 100.0, 1)], 1),
        ("Телевизоры", "Для просмотра", [Product("P1", "D1", 100.0, 1), Product("P2", "D2", 200.0, 2)], 2),
        ("Пустая категория", "Без товаров", [], 0),
    ],
)
def test_category_initialization_parametrized(
    cat_name: str, cat_desc: str, products_list: List[Product], expected_len: int
) -> None:
    """Проверка корректности инициализации Category через параметризацию данных."""
    category = Category(cat_name, cat_desc, products_list)

    assert category.name == cat_name
    assert category.description == cat_desc
    assert len(category.products) == expected_len
    assert isinstance(category.products, list)

    for item in category.products:
        assert isinstance(item, Product)


def test_category_fixture_attributes(sample_category: Category, sample_products_list: List[Product]) -> None:
    """Проверка атрибутов категории, созданной через фикстуры."""
    assert sample_category.name == "Smartphones"
    assert sample_category.description == "Mobile devices for everyday life"
    assert len(sample_category.products) == len(sample_products_list)


# ==========================================
# ТЕСТЫ ДЛЯ АТРИБУТОВ КЛАССА (СЧЕТЧИКИ)
# ==========================================


@pytest.mark.parametrize(
    "categories_data, expected_cat_count, expected_prod_count",
    [
        (
            [
                ("Cat1", "Desc1", [Product("P1", "D1", 10.0, 1), Product("P2", "D2", 20.0, 2)]),
                ("Cat2", "Desc2", [Product("P3", "D3", 30.0, 3)]),
            ],
            2,
            3,
        ),
        ([("Cat1", "Desc1", []), ("Cat2", "Desc2", []), ("Cat3", "Desc3", [])], 3, 0),
        ([("Cat1", "Desc1", [Product(f"P{i}", "D", 10.0, 1) for i in range(5)])], 1, 5),
    ],
)
def test_class_counters_parametrized(
    categories_data: List[Tuple[str, str, List[Product]]], expected_cat_count: int, expected_prod_count: int
) -> None:
    """Проверка автоматического подсчета категорий и товаров через параметризацию."""
    for cat_name, cat_desc, products in categories_data:
        Category(cat_name, cat_desc, products)

    assert Category.category_count == expected_cat_count
    assert Category.product_count == expected_prod_count


def test_class_counters_with_fixtures(sample_category: Category, sample_products_list: List[Product]) -> None:
    """Проверка счетчиков с использованием фикстур."""
    assert Category.category_count == 1
    assert Category.product_count == len(sample_products_list)
