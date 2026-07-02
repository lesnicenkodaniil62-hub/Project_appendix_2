import pytest
from _pytest.capture import CaptureFixture

from src.category import Category
from src.exceptions import ZeroQuantityError
from src.order import Order
from src.product import Product

# ==========================================
# ТЕСТЫ КЛАССА ZeroQuantityError
# ==========================================


def test_zero_quantity_error_is_exception() -> None:
    """ZeroQuantityError должен быть наследником Exception."""
    assert issubclass(ZeroQuantityError, Exception)


def test_zero_quantity_error_message() -> None:
    """ZeroQuantityError должен принимать и хранить сообщение."""
    error = ZeroQuantityError("Тестовое сообщение")
    assert str(error) == "Тестовое сообщение"


def test_zero_quantity_error_can_be_raised() -> None:
    """ZeroQuantityError должен корректно выбрасываться и перехватываться."""
    with pytest.raises(ZeroQuantityError) as exc_info:
        raise ZeroQuantityError("Проверка")
    assert "Проверка" in str(exc_info.value)


# ==========================================
# ТЕСТЫ Product с нулевым количеством (Задание 1)
# ==========================================


def test_product_init_zero_quantity_raises_value_error() -> None:
    """Product с quantity=0 должен выбрасывать ValueError."""
    with pytest.raises(ValueError) as exc_info:
        Product("Test", "Desc", 100.0, 0)
    assert "Товар с нулевым количеством не может быть добавлен" in str(exc_info.value)


def test_product_init_positive_quantity_works() -> None:
    """Product с quantity>0 должен создаваться успешно."""
    product = Product("Test", "Desc", 100.0, 5)
    assert product.quantity == 5


def test_product_init_negative_quantity_works() -> None:
    """Product с quantity<0 создаётся (проверка только на ноль)."""
    product = Product("Test", "Desc", 100.0, -1)
    assert product.quantity == -1


# ==========================================
# ТЕСТЫ middle_price (Задание 2)
# ==========================================


def test_category_middle_price_basic() -> None:
    """Метод middle_price должен считать средний ценник."""
    p1 = Product("P1", "D1", 100.0, 5)
    p2 = Product("P2", "D2", 200.0, 3)
    p3 = Product("P3", "D3", 300.0, 2)
    category = Category("Test", "Desc", [p1, p2, p3])
    # (100 + 200 + 300) / 3 = 200
    assert category.middle_price() == 200.0


def test_category_middle_price_empty() -> None:
    """Для пустой категории middle_price должен возвращать 0 (обработка деления на ноль)."""
    category = Category("Empty", "Desc", [])
    assert category.middle_price() == 0.0


def test_category_middle_price_single() -> None:
    """Для категории с одним товаром middle_price = цене этого товара."""
    p = Product("P1", "D1", 150.0, 5)
    category = Category("Test", "Desc", [p])
    assert category.middle_price() == 150.0


def test_category_middle_price_float_result() -> None:
    """middle_price должен возвращать float при нецелом результате."""
    p1 = Product("P1", "D1", 100.0, 5)
    p2 = Product("P2", "D2", 201.0, 3)
    category = Category("Test", "Desc", [p1, p2])
    # (100 + 201) / 2 = 150.5
    result = category.middle_price()
    assert isinstance(result, float)
    assert result == 150.5


def test_category_middle_price_uses_only_prices() -> None:
    """middle_price должен учитывать только цены, а не количество."""
    p1 = Product("P1", "D1", 100.0, 1000)
    p2 = Product("P2", "D2", 200.0, 1)
    category = Category("Test", "Desc", [p1, p2])
    # (100 + 200) / 2 = 150, а не взвешенное среднее
    assert category.middle_price() == 150.0


# ==========================================
# ТЕСТЫ add_product с ZeroQuantityError (Доп. задание)
# ==========================================


def test_category_add_product_zero_quantity(capsys: CaptureFixture[str]) -> None:
    """add_product с товаром quantity=0 должен обрабатывать ZeroQuantityError."""
    category = Category("Test", "Desc", [])
    product = Product("TestProduct", "Desc", 100.0, 1)
    product.quantity = 0  # обходим проверку в __init__

    category.add_product(product)

    captured = capsys.readouterr()
    assert "нулевым количеством" in captured.out
    assert "завершена" in captured.out
    # Продукт не должен быть добавлен
    assert product not in category._Category__products  # type: ignore[attr-defined]


def test_category_add_product_success_message(capsys: CaptureFixture[str]) -> None:
    """При успешном добавлении товара должно выводиться сообщение о добавлении."""
    category = Category("Test", "Desc", [])
    product = Product("TestProduct", "Desc", 100.0, 5)

    category.add_product(product)

    captured = capsys.readouterr()
    assert "успешно добавлен" in captured.out
    assert "завершена" in captured.out


def test_category_add_product_finally_always_runs(capsys: CaptureFixture[str]) -> None:
    """Сообщение о завершении обработки должно выводиться в любом случае."""
    category = Category("Test", "Desc", [])

    # Успешное добавление
    product_ok = Product("OK", "Desc", 100.0, 1)
    category.add_product(product_ok)
    captured = capsys.readouterr()
    assert "завершена" in captured.out

    # Добавление с нулевым количеством
    product_zero = Product("Zero", "Desc", 100.0, 1)
    product_zero.quantity = 0
    category.add_product(product_zero)
    captured = capsys.readouterr()
    assert "завершена" in captured.out


# ==========================================
# ТЕСТЫ Order с ZeroQuantityError (Доп. задание)
# ==========================================


def test_order_zero_quantity_raises_zero_quantity_error(capsys: CaptureFixture[str]) -> None:
    """Order с quantity=0 должен выбрасывать ZeroQuantityError."""
    product = Product("Test", "Desc", 100.0, 5)
    with pytest.raises(ZeroQuantityError):
        Order(product, 0)
    captured = capsys.readouterr()
    assert "завершена" in captured.out


def test_order_negative_quantity_raises_value_error(capsys: CaptureFixture[str]) -> None:
    """Order с отрицательным количеством должен выбрасывать ValueError."""
    product = Product("Test", "Desc", 100.0, 5)
    with pytest.raises(ValueError):
        Order(product, -1)
    captured = capsys.readouterr()
    assert "завершена" in captured.out


def test_order_success_message(capsys: CaptureFixture[str]) -> None:
    """При успешном создании заказа должно выводиться сообщение."""
    product = Product("Test", "Desc", 100.0, 5)
    order = Order(product, 3)
    captured = capsys.readouterr()
    assert "успешно создан" in captured.out
    assert "завершена" in captured.out
    assert order.quantity == 3
