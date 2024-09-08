from datetime import datetime
from typing import List, Dict
from colorama import Fore, Style, init

# Инициализация colorama для раскрашивания текста
init(autoreset=True)

class Person:
    def __init__(self, name: str):
        self.name = name
        self.groups = []

    def join_group(self, group: 'Group'):
        self.groups.append(group)
        group.add_member(self)
        record_transaction(f"{Fore.YELLOW}{self.name}{Style.RESET_ALL} присоединился к группе {Fore.GREEN}{group.name}{Style.RESET_ALL}")


class Group:
    def __init__(self, name: str, members: List[Person] = None):
        self.name = name
        self.members = members if members else []
        self.brands = []

    def add_member(self, person: Person):
        self.members.append(person)
        record_transaction(f"{Fore.YELLOW}{person.name}{Style.RESET_ALL} добавлен в группу {Fore.GREEN}{self.name}{Style.RESET_ALL}")

    def create_brand(self, brand_name: str):
        new_brand = Brand(brand_name, self)
        self.brands.append(new_brand)
        record_transaction(f"Бренд {Fore.CYAN}{brand_name}{Style.RESET_ALL} создан группой {Fore.GREEN}{self.name}{Style.RESET_ALL}")
        return new_brand


class Brand:
    def __init__(self, name: str, group: Group):
        self.name = name
        self.group = group
        self.products = []

    def create_product(self, product_name: str):
        new_product = Product(product_name, self)
        self.products.append(new_product)
        record_transaction(f"Продукт {Fore.MAGENTA}{product_name}{Style.RESET_ALL} создан брендом {Fore.CYAN}{self.name}{Style.RESET_ALL}")
        return new_product


class Product:
    def __init__(self, name: str, brand: Brand):
        self.name = name
        self.brand = brand


# Простая система для записи транзакций (может быть заменена на логику блокчейна)
ledger: List[Dict[str, str]] = []

def record_transaction(details: str):
    transaction = {
        "details": details,
        "timestamp": datetime.now().isoformat()
    }
    ledger.append(transaction)

def display_ledger():
    print("\nЖурнал транзакций:")
    for transaction in ledger:
        print(f"{transaction['timestamp']}: {transaction['details']}")


# Примеры использования
if __name__ == "__main__":
    # Пример 1: Создание группы и бренда
    print("Пример 1: Создание группы и бренда")
    p1 = Person("Алиса")
    p2 = Person("Боб")
    
    # Создаем группу и присоединяем людей
    group1 = Group("Техническая команда")
    p1.join_group(group1)
    p2.join_group(group1)

    # Группа создает бренд
    brand1 = group1.create_brand("TechBrand")

    # Бренд создает продукт
    product1 = brand1.create_product("Смартфон")

    # Пример 2: Добавление нового пользователя и продукта
    print("\nПример 2: Добавление нового пользователя и создание нового продукта")
    p3 = Person("Чарли")
    p3.join_group(group1)

    # Новый бренд и продукт
    brand2 = group1.create_brand("GadgetBrand")
    product2 = brand2.create_product("Ноутбук")

    # Вывод журнала транзакций
    display_ledger()
