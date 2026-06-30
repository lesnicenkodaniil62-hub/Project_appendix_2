import pytest

from src.base_store_item import BaseStoreItem


def test_base_store_item_str_not_implemented() -> None:
    """Абстрактный метод __str__ в BaseStoreItem должен выбрасывать NotImplementedError."""

    class TestStoreItem(BaseStoreItem):
        def __init__(self) -> None:
            self.name = "Test"
            self.description = "Desc"

        def __str__(self) -> str:
            return super().__str__()  # type: ignore[safe-super]

    item = TestStoreItem()
    with pytest.raises(NotImplementedError):
        str(item)
