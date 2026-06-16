import pytest
from typing import List

from src.utils import load_data_from_json
from src.category import Category
from src.product import Product


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
    assert isinstance(first_category.products, list)

    if len(first_category.products) > 0:
        first_product = first_category.products[0]
        assert isinstance(first_product, Product)
        assert isinstance(first_product.name, str)
        assert isinstance(first_product.price, float)
        assert isinstance(first_product.quantity, int)

    # Тест 3: Проверяем, что атрибуты класса обновились корректно
    # Количество категорий должно совпадать с длиной загруженного списка
    assert Category.category_count == len(categories)

    # Количество товаров должно быть больше 0 (так как в реальном файле они есть)
    assert Category.product_count > 0


def test_load_data_from_json_file_not_found() -> None:
    """
    Проверка корректной обработки отсутствия файла.
    Функция должна выбросить FileNotFoundError с понятным сообщением.
    """
    # Act & Assert
    with pytest.raises(FileNotFoundError) as exc_info:
        load_data_from_json("non_existent_file_12345.json")

    # Проверяем, что сообщение об ошибке содержит ожидаемый текст
    assert "Файл не найден!" in str(exc_info.value)
    assert "non_existent_file_12345.json" in str(exc_info.value)