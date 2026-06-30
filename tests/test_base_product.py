import pytest

from src.base_product import BaseProduct
from src.lawn_grass import LawnGrass
from src.product import Product
from src.smartphone import Smartphone


def test_base_product_is_abstract() -> None:
    """BaseProduct должен быть абстрактным классом."""
    with pytest.raises(TypeError):
        BaseProduct()  # type: ignore[abstract]


def test_product_inherits_from_base_product() -> None:
    """Product должен наследоваться от BaseProduct."""
    product = Product("Test", "Desc", 100.0, 5)
    assert isinstance(product, BaseProduct)
    assert issubclass(Product, BaseProduct)


def test_smartphone_inherits_from_base_product() -> None:
    """Smartphone должен наследоваться от BaseProduct (через Product)."""
    smartphone = Smartphone("S", "D", 100.0, 5, 90.0, "M", 128, "Black")
    assert isinstance(smartphone, BaseProduct)
    assert issubclass(Smartphone, BaseProduct)


def test_lawn_grass_inherits_from_base_product() -> None:
    """LawnGrass должен наследоваться от BaseProduct (через Product)."""
    grass = LawnGrass("G", "D", 100.0, 5, "RU", "7", "Green")
    assert isinstance(grass, BaseProduct)
    assert issubclass(LawnGrass, BaseProduct)


def test_product_implements_str() -> None:
    """Product должен реализовывать абстрактный метод __str__."""
    product = Product("Test", "Desc", 100.0, 5)
    assert str(product) == "Test, 100.0 руб. Остаток: 5 шт."


def test_product_implements_add() -> None:
    """Product должен реализовывать абстрактный метод __add__."""
    p1 = Product("P1", "D1", 100.0, 5)
    p2 = Product("P2", "D2", 200.0, 3)
    assert p1 + p2 == 1100.0


def test_smartphone_implements_str() -> None:
    """Smartphone должен реализовывать абстрактный метод __str__."""
    smartphone = Smartphone("S", "D", 100.0, 5, 90.0, "M", 128, "Black")
    assert str(smartphone) == "S, 100.0 руб. Остаток: 5 шт."


def test_lawn_grass_implements_str() -> None:
    """LawnGrass должен реализовывать абстрактный метод __str__."""
    grass = LawnGrass("G", "D", 100.0, 5, "RU", "7", "Green")
    assert str(grass) == "G, 100.0 руб. Остаток: 5 шт."


def test_base_product_str_not_implemented() -> None:
    """Абстрактный метод __str__ в BaseProduct должен выбрасывать NotImplementedError."""

    class TestProduct(Product):
        def __str__(self) -> str:
            return super().__str__()

    product = TestProduct("Test", "Desc", 100.0, 5)
    with pytest.raises(NotImplementedError):
        str(product)


def test_base_product_add_not_implemented() -> None:
    """Абстрактный метод __add__ в BaseProduct должен выбрасывать NotImplementedError."""

    class TestProduct(Product):
        def __add__(self, other: object) -> float:
            return super().__add__(other)

    product = TestProduct("Test", "Desc", 100.0, 5)
    other = Product("Other", "Desc", 50.0, 2)
    with pytest.raises(NotImplementedError):
        product + other
