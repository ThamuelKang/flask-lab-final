from flask import Flask, request, jsonify

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


@app.route("/", methods=["GET"])
def index():
    return "Hello World"


@app.route("/inventory", methods=["GET"])
def get_inventory():
    return jsonify(inventory)


@app.route("/inventory/<int:item_id>", methods=["GET"])
def get_item(item_id):
    item = find_item(item_id)
    if item:
        return jsonify(item)
    return jsonify({"error": "Item not found"}), 404


if __name__ == "__main__":
    app.run(host="localhost", port=4000, debug=True)
