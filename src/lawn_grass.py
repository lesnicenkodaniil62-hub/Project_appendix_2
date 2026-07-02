from src.product import Product


class LawnGrass(Product):
    """Класс для представления газонной травы (наследник Product)."""

    name: str
    description: str
    quantity: int
    country: str
    germination_period: str
    color: str

    def __init__(
        self,
        name: str,
        description: str,
        price: float,
        quantity: int,
        country: str,
        germination_period: str,
        color: str,
    ) -> None:
        """
        Инициализация газонной травы.

        :param name: Название товара.
        :param description: Описание товара.
        :param price: Цена товара.
        :param quantity: Количество на складе.
        :param country: Страна-производитель.
        :param germination_period: Срок прорастания.
        :param color: Цвет.
        """
        super().__init__(name, description, price, quantity)
        self.country = country
        self.germination_period = germination_period
        self.color = color
