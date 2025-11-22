import requests
import json

BASE_URL = "http://localhost:5555"


def cli_list_inventory():
    response = requests.get(f"{BASE_URL}/inventory")

    if response.status_code == 200:
        items = response.json()  # renamed from 'inventory' to 'items'
        if not items:
            print("Inventory is empty.")
            return
        print("\nInventory:")
        for item in items:
            print(
                f"ID: {item['id']}, Name: {item['name']}, Price: {item['price']}, Stock: {item['stock']}"
            )
    else:
        print("Failed to fetch inventory.")


def cli_add_item():
    print("\nAdd a new inventory item:")
    name = input("Name: ").strip()
    barcode = input("Barcode: ").strip()
    brand = input("Brand: ").strip()
    category = input("Category: ").strip()

    try:
        price = float(input("Price: "))
        stock = int(input("Stock: "))
    except ValueError:
        print("Price must be a number")
        return

    data = {
        "name": name,
        "barcode": barcode,
        "brand": brand,
        "category": category,
        "price": price,
        "stock": stock,
    }

    response = requests.post(f"{BASE_URL}/inventory", json=data)
    if response.status_code == 201:
        print("Item added")
    else:
        print("Failed to add item.")


def cli_view_item():
    try:
        item_id = int(input("Enter the item ID to view: "))
    except ValueError:
        print("Invalid ID.")
        return

    response = requests.get(f"{BASE_URL}/inventory/{item_id}")
    if response.status_code == 200:
        item = response.json()
        print(json.dumps(item, indent=2))
    else:
        print("Item not found.")


def cli_fetch_product():
    barcode = input("Enter product barcode to fetch from OpenFoodFacts: ").strip()
    response = requests.get(f"{BASE_URL}/product/{barcode}")
    if response.status_code == 200:
        product = response.json()
        print("\nProduct Info from OpenFoodFacts:")
        print(json.dumps(product, indent=2))
    else:
        print("Product not found or API error.")


def cli_update_item():
    item_id = int(input("Enter the ID of the item to update: "))
    print("Leave field blank to skip updating that value.")
    name = input("New Name: ").strip()
    barcode = input("New Barcode: ").strip()
    price_input = input("New Price: ").strip()
    stock_input = input("New Stock: ").strip()

    data = {}
    if name:
        data["name"] = name
    if barcode:
        data["barcode"] = barcode
    if price_input:
        data["price"] = float(price_input)
    if stock_input:
        data["stock"] = int(stock_input)

    response = requests.put(f"{BASE_URL}/inventory/{item_id}", json=data)
    if response.status_code == 200:
        print("Item updated successfully!")
        print(json.dumps(response.json()["item"], indent=2))
    else:
        print("Failed to update item:", response.json())


def cli_delete_item():
    item_id = int(input("Enter the ID of the item to delete: "))
    response = requests.delete(f"{BASE_URL}/inventory/{item_id}")
    if response.status_code == 200:
        print("Item deleted successfully!")
    else:
        print("Failed to delete item:", response.json())


def main():
    while True:
        print("\n--- Inventory CLI ---")
        print("1. List inventory")
        print("2. Add item")
        print("3. View item by ID")
        print("4. Update item")
        print("5. Delete item")
        print("6. Fetch product from OpenFoodFacts")
        print("7. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            cli_list_inventory()
        elif choice == "2":
            cli_add_item()
        elif choice == "3":
            cli_view_item()
        elif choice == "4":
            cli_update_item()
        elif choice == "5":
            cli_delete_item()
        elif choice == "6":
            cli_fetch_product()
        elif choice == "7":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number from 1-7.")



if __name__ == "__main__":
    main()
