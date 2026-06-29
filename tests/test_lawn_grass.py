import pytest

from src.category import Category
from src.lawn_grass import LawnGrass
from src.product import Product
from src.smartphone import Smartphone

# ==========================================
# ТЕСТЫ ИНИЦИАЛИЗАЦИИ LAWN GRASS
# ==========================================


def test_lawn_grass_initialization() -> None:
    """Проверка корректности инициализации LawnGrass."""
    grass = LawnGrass(
        name="Газонная трава",
        description="Элитная трава для газона",
        price=500.0,
        quantity=20,
        country="Россия",
        germination_period="7 дней",
        color="Зеленый",
    )

    assert grass.name == "Газонная трава"
    assert grass.description == "Элитная трава для газона"
    assert grass.price == 500.0
    assert grass.quantity == 20
    assert grass.country == "Россия"
    assert grass.germination_period == "7 дней"
    assert grass.color == "Зеленый"


def test_lawn_grass_is_instance_of_product() -> None:
    """LawnGrass должен быть наследником Product."""
    grass = LawnGrass("G", "D", 100.0, 1, "RU", "7", "Green")
    assert isinstance(grass, LawnGrass)
    assert isinstance(grass, Product)


# ==========================================
# ТЕСТЫ СЛОЖЕНИЯ LAWN GRASS
# ==========================================


def test_lawn_grass_add_same_class() -> None:
    """Сложение двух газонных трав должно работать."""
    g1 = LawnGrass("G1", "D", 500.0, 20, "Россия", "7 дней", "Зеленый")
    g2 = LawnGrass("G2", "D", 450.0, 15, "США", "5 дней", "Темно-зеленый")
    # 500*20 + 450*15 = 10000 + 6750 = 16750
    assert g1 + g2 == 16750.0


def test_lawn_grass_add_with_smartphone_raises_type_error() -> None:
    """Сложение травы и смартфона должно выбрасывать TypeError."""
    grass = LawnGrass("G1", "D", 500.0, 20, "Россия", "7 дней", "Зеленый")
    smartphone = Smartphone("S1", "D", 100.0, 5, 90.0, "M1", 128, "Black")

    with pytest.raises(TypeError):
        _ = grass + smartphone  # type: ignore[operator]


def test_lawn_grass_add_with_base_product_raises() -> None:
    """Сложение травы и базового Product должно выбрасывать TypeError."""
    grass = LawnGrass("G1", "D", 500.0, 20, "Россия", "7 дней", "Зеленый")
    base_product = Product("P1", "D", 50.0, 10)

    with pytest.raises(TypeError):
        _ = grass + base_product  # type: ignore[operator]


# ==========================================
# ТЕСТЫ __str__ И ДОБАВЛЕНИЯ В КАТЕГОРИЮ
# ==========================================


def test_lawn_grass_str() -> None:
    """Проверка строкового представления травы."""
    grass = LawnGrass("Grass", "Desc", 500.0, 20, "Россия", "7 дней", "Зеленый")
    assert str(grass) == "Grass, 500.0 руб. Остаток: 20 шт."


def test_lawn_grass_can_be_added_to_category() -> None:
    """Газонная трава должна успешно добавляться в категорию."""
    category = Category("Grass", "Desc", [])
    grass = LawnGrass("G1", "D", 500.0, 20, "Россия", "7 дней", "Зеленый")

    category.add_product(grass)

    assert grass in category._Category__products  # type: ignore[attr-defined]
    assert Category.product_count == 1


def test_lawn_grass_price_setter() -> None:
    """Сеттер цены должен работать для травы."""
    grass = LawnGrass("G1", "D", 500.0, 20, "Россия", "7 дней", "Зеленый")
    grass.price = 600.0
    assert grass.price == 600.0
