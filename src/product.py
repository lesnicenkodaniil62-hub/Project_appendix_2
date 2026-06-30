from typing import Any, Dict, List, Optional

from src.base_product import BaseProduct
from src.mixin import BasePrintMixin


class Product(BasePrintMixin, BaseProduct):
    """Класс для представления продукта."""

    name: str
    description: str
    __price: float  # приватный атрибут
    quantity: int

    def __init__(self, name: str, description: str, price: float, quantity: int) -> None:
        super().__init__(name, description, price, quantity)
        self.name = name
        self.description = description
        self.__price = price
        self.quantity = quantity

    def __str__(self) -> str:
        """Строковое представление продукта."""
        return f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт."

    def __add__(self, other: object) -> float:
        """
        Сложение двух продуктов.
        Возвращает сумму произведений цены на количество у двух объектов.
        Разрешено складывать только объекты одного и того же класса.
        """
        if type(self) is not type(other):
            raise TypeError(
                f"Нельзя складывать товары разных классов: " f"{type(self).__name__} и {type(other).__name__}"
            )
        if not isinstance(other, Product):
            raise TypeError("Можно складывать только объекты класса Product или его наследников")
        return self.price * self.quantity + other.price * other.quantity

    @property
    def price(self) -> float:
        """Геттер для приватного атрибута цены."""
        return self.__price

    @price.setter
    def price(self, new_price: float) -> None:
        """Сеттер для цены с проверкой на положительность и подтверждением при понижении."""
        if new_price <= 0:
            print("Цена не должна быть нулевая или отрицательная")
            return

        if new_price < self.__price:
            answer = input(f"Цена понижается с {self.__price} до {new_price}. Подтвердить? (y/n): ")
            if answer.lower() != "y":
                return

        self.__price = new_price

    @classmethod
    def new_product(cls, product_dict: Dict[str, Any], products_list: Optional[List["Product"]] = None) -> "Product":
        """
        Класс-метод для создания продукта из словаря.
        Дополнительно проверяет наличие дубликатов по имени в products_list.
        """
        if products_list is not None:
            for product in products_list:
                if product.name == product_dict["name"]:
                    product.quantity += product_dict["quantity"]
                    if product_dict["price"] > product.price:
                        product.price = product_dict["price"]
                    return product

        return cls(
            name=product_dict["name"],
            description=product_dict["description"],
            price=product_dict["price"],
            quantity=product_dict["quantity"],
        )
