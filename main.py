from src.category import Category
from src.category_iterator import CategoryIterator
from src.lawn_grass import LawnGrass
from src.product import Product
from src.smartphone import Smartphone
from src.utils import load_data_from_json

if __name__ == "__main__":
    # ==========================================
    # === ДАННЫЕ (feature 1) ===
    # ==========================================
    print("\n" + "=" * 60)
    print("FEATURE 1: базовая функциональность")
    print("=" * 60)

    product_f1_1 = Product("Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5)
    product_f1_2 = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)
    product_f1_3 = Product("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14)

    print(product_f1_1.name)
    print(product_f1_1.description)
    print(product_f1_1.price)
    print(product_f1_1.quantity)

    print(product_f1_2.name)
    print(product_f1_2.description)
    print(product_f1_2.price)
    print(product_f1_2.quantity)

    print(product_f1_3.name)
    print(product_f1_3.description)
    print(product_f1_3.price)
    print(product_f1_3.quantity)

    category_f1_1 = Category(
        "Смартфоны",
        "Смартфоны, как средство не только коммуникации, но и получения дополнительных функций для удобства жизни",
        [product_f1_1, product_f1_2, product_f1_3],
    )

    print(category_f1_1.name == "Смартфоны")
    print(category_f1_1.description)
    print(len(category_f1_1.products))
    print(category_f1_1.category_count)
    print(category_f1_1.product_count)

    product_f1_4 = Product('55" QLED 4K', "Фоновая подсветка", 123000.0, 7)
    category_f1_2 = Category(
        "Телевизоры",
        "Современный телевизор, который позволяет наслаждаться просмотром, станет вашим другом и помощником",
        [product_f1_4],
    )

    print(category_f1_2.name)
    print(category_f1_2.description)
    print(len(category_f1_2.products))
    print(category_f1_2.products)

    print(Category.category_count)
    print(Category.product_count)

    # ==========================================
    # === ДАННЫЕ (feature 2) ===
    # ==========================================
    print("\n" + "=" * 60)
    print("FEATURE 2: add_product и new_product")
    print("=" * 60)

    print(category_f1_1.products)
    product_f2_5 = Product('55" QLED 4K', "Фоновая подсветка", 123000.0, 7)
    category_f1_1.add_product(product_f2_5)
    print(category_f1_1.products)
    print(category_f1_1.product_count)

    new_product = Product.new_product(
        {
            "name": "Samsung Galaxy S23 Ultra",
            "description": "256GB, Серый цвет, 200MP камера",
            "price": 180000.0,
            "quantity": 5,
        }
    )
    print(new_product.name)
    print(new_product.description)
    print(new_product.price)
    print(new_product.quantity)

    new_product.price = 800
    print(new_product.price)

    new_product.price = -100
    print(new_product.price)
    new_product.price = 0
    print(new_product.price)

    # ==========================================
    # === НОВЫЕ ДАННЫЕ (feature 3: __str__ и __add__) ===
    # ==========================================
    print("=" * 60)
    print("FEATURE 3: __str__ и __add__")
    print("=" * 60)

    product1 = Product("Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5)
    product2 = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)
    product3 = Product("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14)

    print("\n--- Строковое представление продуктов ---")
    print(str(product1))
    print(str(product2))
    print(str(product3))

    category1 = Category(
        "Смартфоны",
        "Смартфоны, как средство не только коммуникации, но и получения дополнительных функций для удобства жизни",
        [product1, product2, product3],
    )

    print("\n--- Строковое представление категории ---")
    print(str(category1))

    print("\n--- Список товаров категории (через геттер products) ---")
    print(category1.products)

    print("--- Сложение продуктов ---")
    print(f"product1 + product2 = {product1 + product2}")
    print(f"product1 + product3 = {product1 + product3}")
    print(f"product2 + product3 = {product2 + product3}")

    print("\n--- Демонстрация CategoryIterator ---")
    iterator = CategoryIterator(category1)
    for i, product in enumerate(iterator, start=1):
        print(f"  {i}. {product}")

    # ==========================================
    # === НОВЫЕ ДАННЫЕ (feature 4: наследники Product) ===
    # ==========================================
    print("\n" + "=" * 60)
    print("FEATURE 4: классы-наследники Smartphone и LawnGrass")
    print("=" * 60)

    # Сбросим счётчики для наглядности
    Category.category_count = 0
    Category.product_count = 0

    smartphone1 = Smartphone(
        "Samsung Galaxy S23 Ultra",
        "256GB, Серый цвет, 200MP камера",
        180000.0,
        5,
        95.5,
        "S23 Ultra",
        256,
        "Серый",
    )
    smartphone2 = Smartphone(
        "Iphone 15",
        "512GB, Gray space",
        210000.0,
        8,
        98.2,
        "15",
        512,
        "Gray space",
    )
    smartphone3 = Smartphone(
        "Xiaomi Redmi Note 11",
        "1024GB, Синий",
        31000.0,
        14,
        90.3,
        "Note 11",
        1024,
        "Синий",
    )

    print("\n--- Смартфон 1 ---")
    print(smartphone1.name)
    print(smartphone1.description)
    print(smartphone1.price)
    print(smartphone1.quantity)
    print(smartphone1.efficiency)
    print(smartphone1.model)
    print(smartphone1.memory)
    print(smartphone1.color)

    print("\n--- Смартфон 2 ---")
    print(smartphone2.name)
    print(smartphone2.description)
    print(smartphone2.price)
    print(smartphone2.quantity)
    print(smartphone2.efficiency)
    print(smartphone2.model)
    print(smartphone2.memory)
    print(smartphone2.color)

    print("\n--- Смартфон 3 ---")
    print(smartphone3.name)
    print(smartphone3.description)
    print(smartphone3.price)
    print(smartphone3.quantity)
    print(smartphone3.efficiency)
    print(smartphone3.model)
    print(smartphone3.memory)
    print(smartphone3.color)

    grass1 = LawnGrass("Газонная трава", "Элитная трава для газона", 500.0, 20, "Россия", "7 дней", "Зеленый")
    grass2 = LawnGrass("Газонная трава 2", "Выносливая трава", 450.0, 15, "США", "5 дней", "Темно-зеленый")

    print("\n--- Трава 1 ---")
    print(grass1.name)
    print(grass1.description)
    print(grass1.price)
    print(grass1.quantity)
    print(grass1.country)
    print(grass1.germination_period)
    print(grass1.color)

    print("\n--- Трава 2 ---")
    print(grass2.name)
    print(grass2.description)
    print(grass2.price)
    print(grass2.quantity)
    print(grass2.country)
    print(grass2.germination_period)
    print(grass2.color)

    print("\n--- Сложение смартфонов ---")
    smartphone_sum = smartphone1 + smartphone2
    print(f"smartphone1 + smartphone2 = {smartphone_sum}")

    print("\n--- Сложение газонной травы ---")
    grass_sum = grass1 + grass2
    print(f"grass1 + grass2 = {grass_sum}")

    print("\n--- Попытка сложить смартфон и траву ---")
    try:
        invalid_sum = smartphone1 + grass1  # type: ignore[operator]
        print(f"Не возникла ошибка TypeError при попытке сложения: {invalid_sum}")
    except TypeError as e:
        print(f"Возникла ошибка TypeError при попытке сложения: {e}")

    print("\n--- Создание категорий для смартфонов и травы ---")
    category_smartphones = Category("Смартфоны", "Высокотехнологичные смартфоны", [smartphone1, smartphone2])
    category_grass = Category("Газонная трава", "Различные виды газонной травы", [grass1, grass2])

    category_smartphones.add_product(smartphone3)

    print("\n--- Список смартфонов в категории ---")
    print(category_smartphones.products)

    print(f"Общее количество товаров: {Category.product_count}")

    print("\n--- Попытка добавить не-продукт в категорию ---")
    try:
        category_smartphones.add_product("Not a product")  # type: ignore[arg-type]
        print("Не возникла ошибка TypeError при добавлении не продукта")
    except TypeError as e:
        print(f"Возникла ошибка TypeError при добавлении не продукта: {e}")

    # ==========================================
    # === ЗАГРУЗКИ ИЗ JSON ===
    # ==========================================
    print("\n" + "=" * 60)
    print("ПРОВЕРКА ЗАГРУЗКИ ИЗ JSON")
    print("=" * 60)

    Category.category_count = 0
    Category.product_count = 0

    json_categories = load_data_from_json("products.json")

    for cat in json_categories:
        print("Загружена категория:", cat.name, "товаров:", len(cat._Category__products))  # type: ignore[attr-defined]

    print("Итого категорий из JSON:", Category.category_count)
    print("Итого товаров из JSON:", Category.product_count)
