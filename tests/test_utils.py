import json
from pathlib import Path
from typing import List

import pytest

from src.category import Category
from src.product import Product
from src.utils import load_data_from_json

# ==========================================
# ТЕСТЫ ЗАГРУЗКИ ИЗ JSON (СУЩЕСТВУЮЩИЙ ФАЙЛ)
# ==========================================


def test_load_data_from_json_success() -> None:
    """
    Проверка успешной загрузки данных из реального файла products.json.
    Проверяет создание объектов и обновление счетчиков класса.
    """
    # Act: Вызываем функцию загрузки
    categories: List[Category] = load_data_from_json("products.json")

    # Тест 1: Проверяем, что вернулся список
    assert isinstance(categories, list)
    assert len(categories) > 0, "Список категорий не должен быть пустым"

    # Тест 2: Проверяем типы объектов внутри списка
    first_category = categories[0]
    assert isinstance(first_category, Category)
    # products теперь строка (геттер), а не список
    assert isinstance(first_category.products, str)

    # Приватный список товаров должен быть списком объектов Product
    private_products = first_category._Category__products  # type: ignore[attr-defined]
    assert isinstance(private_products, list)

    if len(private_products) > 0:
        first_product = private_products[0]
        assert isinstance(first_product, Product)
        assert isinstance(first_product.name, str)
        assert isinstance(first_product.price, float)
        assert isinstance(first_product.quantity, int)

    # Тест 3: Проверяем, что атрибуты класса обновились корректно
    assert Category.category_count == len(categories)
    assert Category.product_count > 0


def test_load_data_from_json_file_not_found() -> None:
    """
    Проверка корректной обработки отсутствия файла.
    Функция должна выбросить FileNotFoundError с понятным сообщением.
    """
    with pytest.raises(FileNotFoundError) as exc_info:
        load_data_from_json("non_existent_file_12345.json")

    assert "Файл не найден!" in str(exc_info.value)
    assert "non_existent_file_12345.json" in str(exc_info.value)


# ==========================================
# НОВЫЕ ТЕСТЫ ДЛЯ НОВОГО ФУНКЦИОНАЛА
# ==========================================


def test_load_data_from_json_products_string_format() -> None:
    """
    Проверка, что после загрузки из JSON геттер products возвращает строку
    в правильном формате: 'Название, X руб. Остаток: X шт.\n'.
    """
    categories = load_data_from_json("products.json")

    for category in categories:
        products_str = category.products
        assert isinstance(products_str, str)

        # Если в категории есть товары, строка не должна быть пустой
        private_products = category._Category__products  # type: ignore[attr-defined]
        if len(private_products) > 0:
            assert products_str != ""
            # Каждая строка должна заканчиваться \n
            assert products_str.endswith("\n")

            # Проверяем формат каждой строки
            lines = [line for line in products_str.split("\n") if line]
            assert len(lines) == len(private_products)

            for line, product in zip(lines, private_products):
                expected = f"{product.name}, {product.price} руб. Остаток: {product.quantity} шт."
                assert line == expected


def test_load_data_from_json_product_price_is_private() -> None:
    """
    Проверка, что у загруженных из JSON продуктов цена является приватным атрибутом.
    """
    categories = load_data_from_json("products.json")

    for category in categories:
        for product in category._Category__products:  # type: ignore[attr-defined]
            # Приватный атрибут должен существовать с манглингом
            assert hasattr(product, "_Product__price")
            # Геттер должен возвращать то же значение
            assert product.price == product._Product__price  # type: ignore[attr-defined]


def test_load_data_from_json_price_setter_works() -> None:
    """
    Проверка, что после загрузки из JSON сеттер цены работает корректно
    (включая проверку на отрицательные значения).
    """
    categories = load_data_from_json("products.json")
    first_product = categories[0]._Category__products[0]  # type: ignore[attr-defined]
    original_price = first_product.price

    # Попытка установить отрицательную цену
    first_product.price = -100
    assert first_product.price == original_price  # цена не изменилась

    # Попытка установить нулевую цену
    first_product.price = 0
    assert first_product.price == original_price

    # Установка корректной положительной цены
    first_product.price = 999.99
    assert first_product.price == 999.99


def test_load_data_from_json_counters_consistency() -> None:
    """
    Проверка согласованности счётчиков после загрузки из JSON:
    product_count должен равняться сумме длин приватных списков всех категорий.
    """
    categories = load_data_from_json("products.json")

    # Собираем длины приватных списков в отдельный список для подсчёта
    product_lengths: List[int] = []
    for cat in categories:
        product_lengths.append(len(cat._Category__products))  # type: ignore[attr-defined]

    total_products = sum(product_lengths)

    assert Category.category_count == len(categories)
    assert Category.product_count == total_products


def test_load_data_from_json_add_product_to_loaded_category() -> None:
    """
    Проверка, что к загруженной из JSON категории можно добавить товар
    через метод add_product и счётчик обновится корректно.
    """
    categories = load_data_from_json("products.json")
    category = categories[0]

    initial_count = Category.product_count
    initial_products_len = len(category._Category__products)  # type: ignore[attr-defined]

    new_product = Product("Test Product", "Test Desc", 100.0, 5)
    category.add_product(new_product)

    assert len(category._Category__products) == initial_products_len + 1  # type: ignore[attr-defined]
    assert Category.product_count == initial_count + 1
    assert new_product in category._Category__products  # type: ignore[attr-defined]


def test_load_data_from_json_with_mock_file(tmp_path: Path) -> None:
    """
    Тест загрузки с использованием мокированного JSON-файла через tmp_path.
    Позволяет проверить работу функции без зависимости от реального файла.
    """
    # Создаём временную папку data и файл products.json
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    json_file = data_dir / "products.json"

    test_data = [
        {
            "name": "Test Category",
            "description": "Test Description",
            "products": [
                {
                    "name": "Product A",
                    "description": "Desc A",
                    "price": 100.0,
                    "quantity": 5,
                },
                {
                    "name": "Product B",
                    "description": "Desc B",
                    "price": 200.0,
                    "quantity": 10,
                },
            ],
        }
    ]

    json_file.write_text(json.dumps(test_data), encoding="utf-8")

    # Создаём структуру src/utils.py для корректной работы Path(__file__)
    src_dir = tmp_path / "src"
    src_dir.mkdir(exist_ok=True)
    utils_file = src_dir / "utils.py"
    utils_file.touch()

    # Патчим __file__ в модуле utils
    from unittest.mock import patch

    with patch("src.utils.__file__", str(utils_file)):
        categories = load_data_from_json("products.json")

    assert len(categories) == 1
    assert categories[0].name == "Test Category"
    assert categories[0].description == "Test Description"
    assert len(categories[0]._Category__products) == 2  # type: ignore[attr-defined]

    products = categories[0]._Category__products  # type: ignore[attr-defined]
    assert products[0].name == "Product A"
    assert products[0].price == 100.0
    assert products[0].quantity == 5
    assert products[1].name == "Product B"
    assert products[1].price == 200.0
    assert products[1].quantity == 10

    # Проверяем формат строки products
    expected_str = "Product A, 100.0 руб. Остаток: 5 шт.\nProduct B, 200.0 руб. Остаток: 10 шт.\n"
    assert categories[0].products == expected_str
