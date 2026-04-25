import pytest
import requests
from unittest.mock import patch
from app import app, inventory

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_get_inventory(client):
    """Test reading all items"""
    rv = client.get('/inventory')
    assert rv.status_code == 200
    assert isinstance(rv.json, list)

def test_add_item(client):
    """Test creating a new item"""
    new_item = {"product_name": "Test Milk", "brand": "Test Brand", "stock": 5, "price": 2.99}
    rv = client.post('/inventory', json=new_item)
    assert rv.status_code == 201
    assert rv.json['product_name'] == "Test Milk"

def test_update_item(client):
    """Test patching/updating an existing item"""
    update_data = {"stock": 20}
    rv = client.patch('/inventory/1', json=update_data)
    assert rv.status_code == 200
    assert rv.json['stock'] == 20

def test_delete_item(client):
    """Test deleting an item"""
    rv = client.delete('/inventory/1')
    assert rv.status_code == 204

def test_external_api_fetch(client):
    """Test external API integration using a mock to simulate OpenFoodFacts"""
    with patch('requests.get') as mocked_get:
        # We simulate the API response structure
        mock_response = {"status": 1, "product": {"product_name": "Organic Almond Milk"}}
        mocked_get.return_value.json.return_value = mock_response
        
        rv = client.get('/fetch-api/12345')
        
        assert rv.status_code == 200
        assert rv.json['product']['product_name'] == "Organic Almond Milk"
        mocked_get.assert_called_once()