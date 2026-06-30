import pytest

from src.base_store_item import BaseStoreItem
from src.category import Category
from src.order import Order
from src.product import Product


def test_order_initialization() -> None:
    """Проверка инициализации Order."""
    product = Product("Test", "Desc", 100.0, 5)
    order = Order(product, 3)
    assert order.product == product
    assert order.quantity == 3
    assert order.name == "Заказ Test"
    assert order.description == "Заказ товара Test"


def test_order_total_cost() -> None:
    """Проверка расчета итоговой стоимости."""
    product = Product("Test", "Desc", 100.0, 5)
    order = Order(product, 3)
    assert order.total_cost == 300.0


def test_order_zero_quantity_raises() -> None:
    """Заказ с нулевым количеством должен выбрасывать ValueError."""
    product = Product("Test", "Desc", 100.0, 5)
    with pytest.raises(ValueError):
        Order(product, 0)


def test_order_negative_quantity_raises() -> None:
    """Заказ с отрицательным количеством должен выбрасывать ValueError."""
    product = Product("Test", "Desc", 100.0, 5)
    with pytest.raises(ValueError):
        Order(product, -1)


def test_order_inherits_from_base_store_item() -> None:
    """Order должен наследоваться от BaseStoreItem."""
    product = Product("Test", "Desc", 100.0, 5)
    order = Order(product, 3)
    assert isinstance(order, BaseStoreItem)
    assert issubclass(Order, BaseStoreItem)


def test_category_inherits_from_base_store_item() -> None:
    """Category должен наследоваться от BaseStoreItem."""
    category = Category("Test", "Desc", [])
    assert isinstance(category, BaseStoreItem)
    assert issubclass(Category, BaseStoreItem)


def test_order_str() -> None:
    """Проверка __str__ для Order."""
    product = Product("Test", "Desc", 100.0, 5)
    order = Order(product, 3)
    result = str(order)
    assert "Заказ Test" in result
    assert "3 шт." in result
    assert "100.0 руб." in result
    assert "300.0 руб." in result


def test_order_with_expensive_product() -> None:
    """Проверка заказа с дорогим товаром."""
    product = Product("iPhone", "Latest model", 150000.0, 10)
    order = Order(product, 2)
    assert order.total_cost == 300000.0
    assert "300000.0 руб." in str(order)


def test_base_store_item_is_abstract() -> None:
    """BaseStoreItem должен быть абстрактным классом."""
    with pytest.raises(TypeError):
        BaseStoreItem()  # type: ignore[abstract]
