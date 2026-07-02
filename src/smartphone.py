from src.product import Product


class Smartphone(Product):
    """Класс для представления смартфона (наследник Product)."""

    name: str
    description: str
    quantity: int
    efficiency: float
    model: str
    memory: int
    color: str

    def __init__(
        self,
        name: str,
        description: str,
        price: float,
        quantity: int,
        efficiency: float,
        model: str,
        memory: int,
        color: str,
    ) -> None:
        """
        Инициализация смартфона.

        :param name: Название товара.
        :param description: Описание товара.
        :param price: Цена товара.
        :param quantity: Количество на складе.
        :param efficiency: Производительность.
        :param model: Модель.
        :param memory: Объем встроенной памяти (ГБ).
        :param color: Цвет.
        """
        super().__init__(name, description, price, quantity)
        self.efficiency = efficiency
        self.model = model
        self.memory = memory
        self.color = color
