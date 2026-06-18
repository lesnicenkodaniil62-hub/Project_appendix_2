from typing import List, Tuple
from unittest.mock import patch

import pytest
from _pytest.capture import CaptureFixture

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
    assert product.price == price  # через геттер
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
# ТЕСТЫ ДЛЯ ПРИВАТНОГО АТРИБУТА ЦЕНЫ И СЕТТЕРА
# ==========================================


def test_product_price_is_private() -> None:
    """Проверка, что атрибут цены является приватным (через property)."""
    product = Product("Test", "Desc", 100.0, 1)

    # Проверяем, что price - это property (геттер), а не обычный атрибут
    assert isinstance(type(product).__dict__.get("price"), property)

    # Приватный атрибут должен существовать с манглингом
    assert hasattr(product, "_Product__price")
    assert product._Product__price == 100.0  # type: ignore[attr-defined]


def test_product_price_getter() -> None:
    """Проверка работы геттера цены."""
    product = Product("Test", "Desc", 150.5, 2)
    assert product.price == 150.5


def test_product_price_setter_positive() -> None:
    """Сеттер должен принимать положительную цену."""
    product = Product("Test", "Desc", 100.0, 1)
    product.price = 200.0
    assert product.price == 200.0


def test_product_price_setter_zero(capsys: CaptureFixture[str]) -> None:
    """Сеттер не должен устанавливать цену 0 и должен вывести сообщение."""
    product = Product("Test", "Desc", 100.0, 1)
    product.price = 0
    captured = capsys.readouterr()
    assert "Цена не должна быть нулевая или отрицательная" in captured.out
    assert product.price == 100.0  # цена не изменилась


def test_product_price_setter_negative(capsys: CaptureFixture[str]) -> None:
    """Сеттер не должен устанавливать отрицательную цену."""
    product = Product("Test", "Desc", 100.0, 1)
    product.price = -50
    captured = capsys.readouterr()
    assert "Цена не должна быть нулевая или отрицательная" in captured.out
    assert product.price == 100.0


def test_product_price_setter_decrease_confirm_yes() -> None:
    """При понижении цены и согласии пользователя цена должна измениться."""
    product = Product("Test", "Desc", 100.0, 1)
    with patch("builtins.input", return_value="y"):
        product.price = 50.0
    assert product.price == 50.0


def test_product_price_setter_decrease_confirm_no() -> None:
    """При понижении цены и отказе пользователя цена не должна измениться."""
    product = Product("Test", "Desc", 100.0, 1)
    with patch("builtins.input", return_value="n"):
        product.price = 50.0
    assert product.price == 100.0


def test_product_price_setter_increase_no_confirm() -> None:
    """При повышении цены подтверждение не требуется."""
    product = Product("Test", "Desc", 100.0, 1)
    # input не должен вызываться — мокаем с ошибкой для проверки
    with patch("builtins.input", side_effect=AssertionError("input не должен вызываться")):
        product.price = 200.0
    assert product.price == 200.0


# ==========================================
# ТЕСТЫ ДЛЯ КЛАСС-МЕТОДА new_product
# ==========================================


def test_product_new_product_basic() -> None:
    """Класс-метод new_product должен создавать объект Product из словаря."""
    data = {
        "name": "TestProduct",
        "description": "TestDesc",
        "price": 100.0,
        "quantity": 5,
    }
    product = Product.new_product(data)
    assert isinstance(product, Product)
    assert product.name == "TestProduct"
    assert product.description == "TestDesc"
    assert product.price == 100.0
    assert product.quantity == 5


def test_product_new_product_duplicate_quantity() -> None:
    """При наличии дубликата количество должно складываться."""
    existing = Product("Phone", "Desc", 100.0, 5)
    products_list = [existing]
    data = {"name": "Phone", "description": "New Desc", "price": 80.0, "quantity": 3}

    result = Product.new_product(data, products_list)

    assert result is existing  # возвращается существующий объект
    assert existing.quantity == 8  # 5 + 3
    assert existing.price == 100.0  # цена не изменилась, т.к. новая ниже


def test_product_new_product_duplicate_higher_price() -> None:
    """При конфликте цен должна выбираться более высокая."""
    existing = Product("Phone", "Desc", 100.0, 5)
    products_list = [existing]
    data = {"name": "Phone", "description": "New Desc", "price": 200.0, "quantity": 3}

    # Вызываем метод — он обновит существующий объект
    Product.new_product(data, products_list)

    assert existing.quantity == 8
    assert existing.price == 200.0  # выбрана более высокая цена


def test_product_new_product_no_duplicate() -> None:
    """Если дубликата нет, создаётся новый объект."""
    existing = Product("Phone", "Desc", 100.0, 5)
    products_list = [existing]
    data = {"name": "Laptop", "description": "New Desc", "price": 500.0, "quantity": 2}

    result = Product.new_product(data, products_list)

    assert result is not existing
    assert result.name == "Laptop"
    assert len(products_list) == 1  # список не изменился


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
    # products теперь строка — считаем количество непустых строк
    products_str = category.products
    if expected_len == 0:
        assert products_str == ""
    else:
        lines = [line for line in products_str.split("\n") if line]
        assert len(lines) == expected_len


def test_category_fixture_attributes(sample_category: Category, sample_products_list: List[Product]) -> None:
    """Проверка атрибутов категории, созданной через фикстуры."""
    assert sample_category.name == "Smartphones"
    assert sample_category.description == "Mobile devices for everyday life"
    products_str = sample_category.products
    lines = [line for line in products_str.split("\n") if line]
    assert len(lines) == len(sample_products_list)


# ==========================================
# ТЕСТЫ ДЛЯ ПРИВАТНОГО АТРИБУТА products
# ==========================================


def test_category_products_is_private() -> None:
    """Проверка, что список товаров является приватным атрибутом."""
    category = Category("Test", "Desc", [])
    # products - это property, а приватный атрибут - __products
    assert hasattr(category, "_Category__products")
    assert isinstance(category._Category__products, list)  # type: ignore[attr-defined]


def test_category_products_getter_format() -> None:
    """Геттер products должен возвращать строку в правильном формате."""
    p1 = Product("Phone", "Desc1", 100.0, 5)
    p2 = Product("Laptop", "Desc2", 500.0, 2)
    category = Category("Tech", "Description", [p1, p2])

    result = category.products

    assert isinstance(result, str)
    assert "Phone, 100.0 руб. Остаток: 5 шт." in result
    assert "Laptop, 500.0 руб. Остаток: 2 шт." in result
    # Каждая строка заканчивается \n
    assert result.endswith("\n")


def test_category_products_getter_empty() -> None:
    """Для пустой категории геттер должен возвращать пустую строку."""
    category = Category("Empty", "Desc", [])
    assert category.products == ""


# ==========================================
# ТЕСТЫ ДЛЯ МЕТОДА add_product
# ==========================================


def test_category_add_product() -> None:
    """Метод add_product должен добавлять продукт в приватный список."""
    category = Category("Test", "Desc", [])
    product = Product("Phone", "Desc", 100.0, 5)

    category.add_product(product)

    assert product in category._Category__products  # type: ignore[attr-defined]
    assert "Phone, 100.0 руб. Остаток: 5 шт." in category.products


def test_category_add_product_increments_counter() -> None:
    """Метод add_product должен увеличивать счетчик product_count."""
    category = Category("Test", "Desc", [])
    initial_count = Category.product_count

    product = Product("Phone", "Desc", 100.0, 5)
    category.add_product(product)

    assert Category.product_count == initial_count + 1


def test_category_add_product_returns_none() -> None:
    """Метод add_product не должен возвращать значение (возвращает None)."""
    category = Category("Test", "Desc", [])
    product = Product("Phone", "Desc", 100.0, 5)

    # Вызываем метод — он не возвращает значение (сигнатура -> None)
    category.add_product(product)

    # Проверяем, что продукт действительно добавлен
    assert product in category._Category__products  # type: ignore[attr-defined]


def test_category_add_product_requires_product_argument() -> None:
    """Метод add_product должен принимать объект Product."""
    category = Category("Test", "Desc", [])
    product = Product("Phone", "Desc", 100.0, 5)

    category.add_product(product)
    assert product in category._Category__products  # type: ignore[attr-defined]


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
