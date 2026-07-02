from typing import Any


class BasePrintMixin:
    """
    Миксин для вывода информации о создании объекта в консоль.
    При создании объекта печатает имя класса и переданные аргументы.
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        args_repr = ", ".join(repr(arg) for arg in args)
        if kwargs:
            kwargs_repr = ", ".join(f"{k}={repr(v)}" for k, v in kwargs.items())
            if args_repr:
                args_repr += ", "
            args_repr += kwargs_repr

        print(f"{self.__class__.__name__}({args_repr})")
        super().__init__()
