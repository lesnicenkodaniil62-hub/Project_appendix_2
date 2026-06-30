import pytest

from src.lawn_grass import LawnGrass
from src.product import Product
from src.smartphone import Smartphone


def test_product_init_prints_info(capsys: pytest.CaptureFixture[str]) -> None:
    """При создании Product должна печататься информация о классе и аргументах."""
    product = Product("Test", "Desc", 100.0, 5)
    captured = capsys.readouterr()
    assert "Product(" in captured.out
    assert "'Test'" in captured.out
    assert "'Desc'" in captured.out
    assert "100.0" in captured.out
    assert "5" in captured.out
    # Используем переменную, чтобы избежать F841
    assert product.name == "Test"


def test_smartphone_init_prints_info(capsys: pytest.CaptureFixture[str]) -> None:
    """При создании Smartphone должна печататься информация."""
    smartphone = Smartphone("S", "D", 100.0, 5, 90.0, "M", 128, "Black")
    captured = capsys.readouterr()
    assert "Smartphone(" in captured.out
    assert "'S'" in captured.out
    assert "90.0" in captured.out
    assert "128" in captured.out
    # Используем переменную, чтобы избежать F841
    assert smartphone.name == "S"


def test_lawn_grass_init_prints_info(capsys: pytest.CaptureFixture[str]) -> None:
    """При создании LawnGrass должна печататься информация."""
    grass = LawnGrass("G", "D", 100.0, 5, "RU", "7", "Green")
    captured = capsys.readouterr()
    assert "LawnGrass(" in captured.out
    assert "'G'" in captured.out
    assert "'RU'" in captured.out
    # Используем переменную, чтобы избежать F841
    assert grass.name == "G"


def test_mixin_prints_class_name(capsys: pytest.CaptureFixture[str]) -> None:
    """Миксин должен печатать имя класса, а не BasePrintMixin."""
    product = Product("Test", "Desc", 100.0, 5)
    captured = capsys.readouterr()
    assert "BasePrintMixin" not in captured.out
    assert "Product(" in captured.out
    # Используем переменную, чтобы избежать F841
    assert isinstance(product, Product)


def test_mixin_format_matches_repr(capsys: pytest.CaptureFixture[str]) -> None:
    """Формат вывода должен соответствовать примеру: ClassName(arg1, arg2, ...)."""
    product = Product("Test", "Desc", 100.0, 5)
    captured = capsys.readouterr()
    assert captured.out.startswith("Product(")
    assert captured.out.strip().endswith(")")
    # Используем переменную, чтобы избежать F841
    assert product.price == 100.0


def test_mixin_with_kwargs(capsys: pytest.CaptureFixture[str]) -> None:
    """Миксин должен корректно обрабатывать именованные аргументы."""
    product = Product.new_product(
        {
            "name": "Test",
            "description": "Desc",
            "price": 100.0,
            "quantity": 5,
        }
    )
    assert product is not None  # Устраняет F841
    captured = capsys.readouterr()
    assert "Product(" in captured.out
    assert "name=" in captured.out or "'Test'" in captured.out


def test_mixin_with_kwargs_direct(capsys: pytest.CaptureFixture[str]) -> None:
    """Миксин должен корректно обрабатывать именованные аргументы."""
    from src.mixin import BasePrintMixin

    class TestMixin(BasePrintMixin):
        def __init__(self, name: str, value: int) -> None:
            super().__init__(name=name, value=value)

    TestMixin("Test", 42)  # Вызов напрямую, без присваивания
    captured = capsys.readouterr()
    assert "TestMixin(" in captured.out
    assert "name='Test'" in captured.out
    assert "value=42" in captured.out


def test_mixin_with_args_and_kwargs(capsys: pytest.CaptureFixture[str]) -> None:
    """Миксин должен корректно обрабатывать одновременную передачу позиционных и именованных аргументов."""
    from src.mixin import BasePrintMixin

    class TestMixin(BasePrintMixin):
        def __init__(self, arg1: str, arg2: int, kwarg1: str, kwarg2: int) -> None:
            super().__init__(arg1, arg2, kwarg1=kwarg1, kwarg2=kwarg2)

    TestMixin("pos1", 100, kwarg1="kw1", kwarg2=200)
    captured = capsys.readouterr()
    assert "TestMixin(" in captured.out
    assert "'pos1'" in captured.out
    assert "100" in captured.out
    assert "kwarg1='kw1'" in captured.out
    assert "kwarg2=200" in captured.out
    # Проверяем, что между позиционными и именованными аргументами есть запятая с пробелом
    assert ", kwarg1=" in captured.out
