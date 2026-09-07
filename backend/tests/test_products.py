def test_list_products_empty(client):
    response = client.get('/products')
    assert response.status_code == 200
    assert response.json() == []

def test_create_product_requires_admin(client, auth_headers):
    response = client.post(
        '/products', json={'name': 'Mouse', 'price': '24.99', 'stock': 10}, headers=auth_headers
    )
    assert response.status_code == 403

def test_create_and_get_product(client, admin_auth_headers):
    create_response = client.post(
        '/products', json={'name': 'Mouse', 'price': '24.99', 'stock': 10}, headers=admin_auth_headers
    )
    assert create_response.status_code == 201
    product_id = create_response.json()['id']

    get_response = client.get(f'/products/{product_id}')
    assert get_response.status_code == 200
    assert get_response.json()['name'] == 'Mouse'

def test_get_nonexistent_product_404(client):
    response = client.get('/products/999')
    assert response.status_code == 404

def test_search_products(client, admin_auth_headers):
    client.post('/products', json={'name': 'Wireless Mouse', 'price': '24.99', 'stock': 10}, headers=admin_auth_headers)
    client.post('/products', json={'name': 'Keyboard', 'price': '49.99', 'stock': 5}, headers=admin_auth_headers)

    response = client.get('/products?search=mouse')
    assert response.status_code == 200
    results = response.json()
    assert len(results) == 1
    assert results[0]['name'] == 'Wireless Mouse'

def test_update_product_requires_admin(client, admin_auth_headers, auth_headers):
    create_response = client.post(
        '/products', json={'name': 'Mouse', 'price': '24.99', 'stock': 10}, headers=admin_auth_headers
    )
    product_id = create_response.json()['id']

    response = client.patch(f'/products/{product_id}', json={'price': '19.99'}, headers=auth_headers)
    assert response.status_code == 403

def test_update_product_as_admin(client, admin_auth_headers):
    create_response = client.post(
        '/products', json={'name': 'Mouse', 'price': '24.99', 'stock': 10}, headers=admin_auth_headers
    )
    product_id = create_response.json()['id']

    response = client.patch(f'/products/{product_id}', json={'price': '19.99'}, headers=admin_auth_headers)
    assert response.status_code == 200
    assert response.json()['price'] == '19.99'

def test_update_nonexistent_product_404(client, admin_auth_headers):
    response = client.patch('/products/999', json={'price': '19.99'}, headers=admin_auth_headers)
    assert response.status_code == 404

def test_delete_nonexistent_product_404(client, admin_auth_headers):
    response = client.delete('/products/999', headers=admin_auth_headers)
    assert response.status_code == 404

def test_delete_product_as_admin(client, admin_auth_headers):
    create_response = client.post(
        '/products', json={'name': 'Mouse', 'price': '24.99', 'stock': 10}, headers=admin_auth_headers
    )
    product_id = create_response.json()['id']

    response = client.delete(f'/products/{product_id}', headers=admin_auth_headers)
    assert response.status_code == 204

    get_response = client.get(f'/products/{product_id}')
    assert get_response.status_code == 404