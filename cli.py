import requests

BASE_URL = "http://127.0.0.1:5000"

def view_inventory():
    print(requests.get(f"{BASE_URL}/inventory").json())

def add_product(name, brand, stock, price):
    data = {"product_name": name, "brand": brand, "stock": stock, "price": price}
    requests.post(f"{BASE_URL}/inventory", json=data)
