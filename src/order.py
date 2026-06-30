from src.base_store_item import BaseStoreItem
from src.product import Product


class Order(BaseStoreItem):
    """
    Класс для представления заказа.
    Содержит ссылку на товар, количество и итоговую стоимость.
    В заказе может быть указан только один товар.
    """

    product: Product
    quantity: int
    name: str
    description: str

    def __init__(self, product: Product, quantity: int) -> None:
        """
        Инициализация заказа.

        :param product: Товар, который был куплен.
        :param quantity: Количество купленного товара.
        :raises ValueError: Если количество меньше или равно нулю.
        """
        if quantity <= 0:
            raise ValueError("Количество товара в заказе должно быть положительным")

        self.product = product
        self.quantity = quantity
        self.name = f"Заказ {product.name}"
        self.description = f"Заказ товара {product.name}"

    @property
    def total_cost(self) -> float:
        """
        Итоговая стоимость заказа.
        Рассчитывается как произведение цены товара на количество.
        """
        return self.product.price * self.quantity

    def __str__(self) -> str:
        """
        Строковое представление заказа.
        """
        return f"{self.name}: {self.quantity} шт. x {self.product.price} руб. " f"= {self.total_cost} руб."
