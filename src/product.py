from typing import Any, Dict, List, Optional


class Product:
    """Класс для представления продукта."""

    name: str
    description: str
    __price: float  # приватный атрибут
    quantity: int

    def __init__(self, name: str, description: str, price: float, quantity: int) -> None:
        self.name = name
        self.description = description
        self.__price = price  # используем приватный атрибут
        self.quantity = quantity

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

        # Дополнительное задание: подтверждение при понижении цены
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
        # Дополнительное задание: проверка на дубликаты
        if products_list is not None:
            for product in products_list:
                if product.name == product_dict["name"]:
                    # Товар уже существует - складываем количество
                    product.quantity += product_dict["quantity"]
                    # При конфликте цен выбираем более высокую
                    if product_dict["price"] > product.price:
                        product.price = product_dict["price"]
                    return product

        # Создаем новый продукт
        return cls(
            name=product_dict["name"],
            description=product_dict["description"],
            price=product_dict["price"],
            quantity=product_dict["quantity"],
        )
