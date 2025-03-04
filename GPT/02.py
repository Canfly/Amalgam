from datetime import datetime
from typing import List, Dict

class Person:
    def __init__(self, name: str):
        self.name = name
        self.groups = []

    def join_group(self, group: 'Group'):
        self.groups.append(group)
        group.add_member(self)
        record_transaction(f"{self.name} joined {group.name}")


class Group:
    def __init__(self, name: str, members: List[Person] = None):
        self.name = name
        self.members = members if members else []
        self.brands = []

    def add_member(self, person: Person):
        self.members.append(person)
        record_transaction(f"{person.name} added to group {self.name}")

    def create_brand(self, brand_name: str):
        new_brand = Brand(brand_name, self)
        self.brands.append(new_brand)
        record_transaction(f"Brand {brand_name} created by group {self.name}")
        return new_brand


class Brand:
    def __init__(self, name: str, group: Group):
        self.name = name
        self.group = group
        self.products = []

    def create_product(self, product_name: str):
        new_product = Product(product_name, self)
        self.products.append(new_product)
        record_transaction(f"Product {product_name} created under brand {self.name}")
        return new_product


class Product:
    def __init__(self, name: str, brand: Brand):
        self.name = name
        self.brand = brand


# Simple ledger for transactions (could be replaced by blockchain logic)
ledger: List[Dict[str, str]] = []

def record_transaction(details: str):
    transaction = {
        "details": details,
        "timestamp": datetime.now().isoformat()
    }
    ledger.append(transaction)

def display_ledger():
    for transaction in ledger:
        print(f"{transaction['timestamp']}: {transaction['details']}")

# Example usage
if __name__ == "__main__":
    # Creating people
    p1 = Person("Alice")
    p2 = Person("Bob")
    p3 = Person("Charlie")

    # Forming a group
    group1 = Group("Development Team")
    p1.join_group(group1)
    p2.join_group(group1)
    p3.join_group(group1)

    # Group creates a brand
    brand1 = group1.create_brand("TechBrand")

    # Brand creates a product
    product1 = brand1.create_product("Smartphone")

    # Displaying transaction ledger
    display_ledger()

