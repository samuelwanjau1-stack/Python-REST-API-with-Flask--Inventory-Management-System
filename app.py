from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

# Mock Database: Initialized with an item containing an ID
inventory = [
    {
        "id": 1, 
        "product_name": "Organic Almond Milk", 
        "brands": "Silk", 
        "ingredients_text": "Filtered water, almonds, cane sugar", 
        "price": 5.99, 
        "stock": 10
    }
]

# --- CRUD Routes ---

@app.route('/inventory', methods=['GET'])
def get_all():
    return jsonify(inventory), 200

@app.route('/inventory/<int:id>', methods=['GET'])
def get_item(id):
    item = next((i for i in inventory if i['id'] == id), None)
    return jsonify(item) if item else (jsonify({"error": "Item not found"}), 404)

@app.route('/inventory', methods=['POST'])
def add_item():
    new_data = request.json
    new_item = {
        "id": len(inventory) + 1,
        "product_name": new_data.get('product_name'),
        "brands": new_data.get('brands'),
        "ingredients_text": new_data.get('ingredients_text', ''),
        "price": new_data.get('price', 0.0),
        "stock": new_data.get('stock', 0)
    }
    inventory.append(new_item)
    return jsonify(new_item), 201

@app.route('/inventory/<int:id>', methods=['PATCH'])
def update_item(id):
    item = next((i for i in inventory if i['id'] == id), None)
    if not item:
        return jsonify({"error": "Item not found"}), 404
    
    data = request.json
    item.update(data)
    return jsonify(item), 200

@app.route('/inventory/<int:id>', methods=['DELETE'])
def delete_item(id):
    global inventory
    inventory = [i for i in inventory if i['id'] != id]
    return '', 204

# --- External API Integration ---

@app.route('/fetch-api/<barcode>', methods=['GET'])
def fetch_external(barcode):
    """
    Queries OpenFoodFacts API and returns the product details.
    """
    url = f"https://world.openfoodfacts.org/api/v0/product/{barcode}.json"
    response = requests.get(url)
    
    if response.status_code == 200:
        return jsonify(response.json()), 200
    return jsonify({"error": "Failed to fetch from external API"}), 502

if __name__ == '__main__':
    # Debug mode is helpful for development
    app.run(debug=True)