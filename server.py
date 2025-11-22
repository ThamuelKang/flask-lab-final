from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

inventory = [
    {
        "id": 1,
        "name": "Coca Cola",
        "barcode": "04963406",
        "price": 1.99,
        "stock": 24,
        "brand": "Coca-Cola",
        "category": "Beverage",
    },
    {
        "id": 2,
        "name": "Pepsi",
        "barcode": "01234567",
        "price": 1.79,
        "stock": 18,
        "brand": "PepsiCo",
        "category": "Beverage",
    },
]


def find_item(item_id):
    return next((item for item in inventory if item["id"] == item_id), None)


# Home
@app.route("/", methods=["GET"])
def index():
    return "Hello World"


# Inventory GET
@app.route("/inventory", methods=["GET"])
def get_inventory():
    return jsonify(inventory)


# Inventory POST
@app.route("/inventory", methods=["POST"])
def add_item():
    data = request.get_json()

    # Check for required fields
    required_fields = ["name", "barcode", "price", "stock"]
    missing_field = False

    for field in required_fields:
        if field not in data:
            missing_field = True
            break

    if missing_field:
        return jsonify({"error": "Missing required fields"}), 400

    # New ID
    new_id = max([item["id"] for item in inventory], default=0) + 1

    new_item = {
        "id": new_id,
        "name": data["name"],
        "barcode": data["barcode"],
        "price": data["price"],
        "stock": data["stock"],
        "brand": data.get("brand", ""),
        "category": data.get("category", ""),
    }

    inventory.append(new_item)
    return jsonify({"message": "Item added", "item": new_item}), 201


# Inventory GET by ID
@app.route("/inventory/<int:item_id>", methods=["GET"])
def get_item(item_id):
    item = find_item(item_id)
    if item:
        return jsonify(item)
    return jsonify({"error": "Item not found"}), 404


# Get product from OpenFoodFacts
@app.route("/product/<barcode>", methods=["GET"])
def fetch_product(barcode):
    url = f"https://world.openfoodfacts.org/api/v0/product/{barcode}.json"
    response = requests.get(url)

    if response.status_code != 200:
        return jsonify({"error": "Failed to fetch product"}), 500

    data = response.json()
    if data.get("status") != 1:
        return jsonify({"error": "Product not found"}), 404

    product = data["product"]
    product_info = {
        "name": product.get("product_name"),
        "brand": product.get("brands"),
        "category": product.get("categories"),
        "barcode": product.get("code"),
    }
    return jsonify(product_info)


if __name__ == "__main__":
    app.run(host="localhost", port=5555, debug=True)
