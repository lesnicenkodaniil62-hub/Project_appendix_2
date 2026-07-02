from abc import ABC, abstractmethod


class BaseProduct(ABC):
    """
    Абстрактный базовый класс для всех продуктов.
    Определяет общий интерфейс для всех продуктов.
    """

    name: str
    description: str
    quantity: int

    @abstractmethod
    def __str__(self) -> str:
        """
        Строковое представление продукта.
        Должен быть реализован в подклассах.
        """
        pass

    @abstractmethod
    def __add__(self, other: object) -> float:
        """
        Сложение двух продуктов.
        Должен быть реализован в подклассах.
        """
        pass
