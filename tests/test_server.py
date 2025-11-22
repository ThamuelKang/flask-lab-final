import pytest
from server import app
import json

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


def test_get_inventory(client):
    response = client.get("/inventory")
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) >= 2  # At least initial items


def test_get_item(client):
    response = client.get("/inventory/1")
    assert response.status_code == 200
    data = response.get_json()
    assert data["name"] == "Coca Cola"


def test_get_nonexistent_item(client):
    response = client.get("/inventory/999")
    assert response.status_code == 404
    data = response.get_json()
    assert "error" in data


def test_add_item(client):
    new_item = {
        "name": "Test Drink",
        "barcode": "00000001",
        "price": 2.50,
        "stock": 10
    }
    response = client.post("/inventory", json=new_item)
    assert response.status_code == 201
    data = response.get_json()
    assert data["item"]["name"] == "Test Drink"
    assert data["item"]["barcode"] == "00000001"


def test_update_item(client):
    # First, add an item
    new_item = {
        "name": "Update Test",
        "barcode": "00000002",
        "price": 3.00,
        "stock": 5
    }
    post_response = client.post("/inventory", json=new_item)
    item_id = post_response.get_json()["item"]["id"]

    # Update the item
    update_data = {"price": 3.50, "stock": 8}
    put_response = client.put(f"/inventory/{item_id}", json=update_data)
    assert put_response.status_code == 200
    updated_item = put_response.get_json()["item"]
    assert updated_item["price"] == 3.50
    assert updated_item["stock"] == 8


def test_delete_item(client):
    # First, add an item
    new_item = {
        "name": "Delete Test",
        "barcode": "00000003",
        "price": 1.00,
        "stock": 2
    }
    post_response = client.post("/inventory", json=new_item)
    item_id = post_response.get_json()["item"]["id"]

    # Delete the item
    delete_response = client.delete(f"/inventory/{item_id}")
    assert delete_response.status_code == 200

    # Verify deletion
    get_response = client.get(f"/inventory/{item_id}")
    assert get_response.status_code == 404


def test_fetch_openfoodfacts(client):
    # Example barcode that exists in OpenFoodFacts
    barcode = "04963406"  # Coca-Cola
    response = client.get(f"/product/{barcode}")
    assert response.status_code == 200
    data = response.get_json()
    assert "name" in data
    assert "brand" in data
    assert "category" in data
    assert data["barcode"] == barcode
