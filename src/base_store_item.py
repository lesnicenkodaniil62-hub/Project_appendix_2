from abc import ABC, abstractmethod


class BaseStoreItem(ABC):
    """
    Абстрактный базовый класс для элементов магазина.
    Определяет общий интерфейс для категорий и заказов.
    """

    name: str
    description: str

    @abstractmethod
    def __str__(self) -> str:
        """
        Строковое представление элемента магазина.
        Должен быть реализован в подклассах.
        """
        pass
