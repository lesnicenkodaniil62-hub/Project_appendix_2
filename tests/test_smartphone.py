import pytest

from src.category import Category
from src.lawn_grass import LawnGrass
from src.product import Product
from src.smartphone import Smartphone

# ==========================================
# ТЕСТЫ ИНИЦИАЛИЗАЦИИ SMARTPHONE
# ==========================================


def test_smartphone_initialization() -> None:
    """Проверка корректности инициализации Smartphone."""
    smartphone = Smartphone(
        name="Samsung Galaxy S23 Ultra",
        description="256GB, Серый цвет, 200MP камера",
        price=180000.0,
        quantity=5,
        efficiency=95.5,
        model="S23 Ultra",
        memory=256,
        color="Серый",
    )

    assert smartphone.name == "Samsung Galaxy S23 Ultra"
    assert smartphone.description == "256GB, Серый цвет, 200MP камера"
    assert smartphone.price == 180000.0
    assert smartphone.quantity == 5
    assert smartphone.efficiency == 95.5
    assert smartphone.model == "S23 Ultra"
    assert smartphone.memory == 256
    assert smartphone.color == "Серый"


def test_smartphone_is_instance_of_product() -> None:
    """Smartphone должен быть наследником Product."""
    smartphone = Smartphone("S", "D", 100.0, 1, 90.0, "M", 128, "Black")
    assert isinstance(smartphone, Smartphone)
    assert isinstance(smartphone, Product)


# ==========================================
# ТЕСТЫ СЛОЖЕНИЯ SMARTPHONE
# ==========================================


def test_smartphone_add_same_class() -> None:
    """Сложение двух смартфонов должно работать."""
    s1 = Smartphone("S1", "D", 100.0, 5, 90.0, "M1", 128, "Black")
    s2 = Smartphone("S2", "D", 200.0, 3, 95.0, "M2", 256, "White")
    # 100*5 + 200*3 = 500 + 600 = 1100
    assert s1 + s2 == 1100.0


def test_smartphone_add_with_grass_raises_type_error() -> None:
    """Сложение смартфона и газонной травы должно выбрасывать TypeError."""
    smartphone = Smartphone("S1", "D", 100.0, 5, 90.0, "M1", 128, "Black")
    grass = LawnGrass("G1", "D", 50.0, 10, "Россия", "7 дней", "Зеленый")

    with pytest.raises(TypeError):
        _ = smartphone + grass  # type: ignore[operator]

    with pytest.raises(TypeError):
        _ = grass + smartphone  # type: ignore[operator]


def test_smartphone_add_with_base_product_raises() -> None:
    """Сложение смартфона и базового Product должно выбрасывать TypeError."""
    smartphone = Smartphone("S1", "D", 100.0, 5, 90.0, "M1", 128, "Black")
    base_product = Product("P1", "D", 50.0, 10)

    with pytest.raises(TypeError):
        _ = smartphone + base_product  # type: ignore[operator]


def test_smartphone_add_with_int_raises() -> None:
    """Сложение смартфона с числом должно выбрасывать TypeError."""
    smartphone = Smartphone("S1", "D", 100.0, 5, 90.0, "M1", 128, "Black")
    with pytest.raises(TypeError):
        _ = smartphone + 100  # type: ignore[operator]


# ==========================================
# ТЕСТЫ __str__ И ДОБАВЛЕНИЯ В КАТЕГОРИЮ
# ==========================================


def test_smartphone_str() -> None:
    """Проверка строкового представления смартфона."""
    smartphone = Smartphone("S1", "D", 100.0, 5, 90.0, "M1", 128, "Black")
    assert str(smartphone) == "S1, 100.0 руб. Остаток: 5 шт."


def test_smartphone_can_be_added_to_category() -> None:
    """Смартфон должен успешно добавляться в категорию."""
    category = Category("Smartphones", "Desc", [])
    smartphone = Smartphone("S1", "D", 100.0, 5, 90.0, "M1", 128, "Black")

    category.add_product(smartphone)

    assert smartphone in category._Category__products  # type: ignore[attr-defined]
    assert Category.product_count == 1


def test_smartphone_price_setter() -> None:
    """Сеттер цены должен работать для смартфона."""
    smartphone = Smartphone("S1", "D", 100.0, 5, 90.0, "M1", 128, "Black")
    smartphone.price = 200.0
    assert smartphone.price == 200.0
