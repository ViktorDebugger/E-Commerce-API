def test_get_cart_creates_empty_cart(client, auth_headers):
    response = client.get('/cart', headers=auth_headers)
    assert response.status_code == 200
    assert response.json()['items'] == []

def test_add_item_to_cart(client, auth_headers, admin_auth_headers):
    product_response = client.post(
        '/products', json={'name': 'Mouse', 'price': '24.99', 'stock': 10}, headers=admin_auth_headers
    )
    product_id = product_response.json()['id']

    response = client.post('/cart/items', json={'product_id': product_id, 'quantity': 2}, headers=auth_headers)
    assert response.status_code == 201
    body = response.json()
    assert len(body['items']) == 1
    assert body['total'] == '49.98'

def test_add_same_product_increases_quantity(client, auth_headers, admin_auth_headers):
    product_response = client.post(
        '/products', json={'name': 'Mouse', 'price': '24.99', 'stock': 10}, headers=admin_auth_headers
    )
    product_id = product_response.json()['id']

    client.post('/cart/items', json={'product_id': product_id, 'quantity': 2}, headers=auth_headers)
    response = client.post('/cart/items', json={'product_id': product_id, 'quantity': 3}, headers=auth_headers)

    assert len(response.json()['items']) == 1
    assert response.json()['items'][0]['quantity'] == 5

def test_add_nonexistent_product_404(client, auth_headers):
    response = client.post('/cart/items', json={'product_id': 999, 'quantity': 1}, headers=auth_headers)
    assert response.status_code == 404

def test_update_cart_item_quantity(client, auth_headers, admin_auth_headers):
    product_response = client.post(
        '/products', json={'name': 'Mouse', 'price': '24.99', 'stock': 10}, headers=admin_auth_headers
    )
    product_id = product_response.json()['id']
    add_response = client.post('/cart/items', json={'product_id': product_id, 'quantity': 2}, headers=auth_headers)
    item_id = add_response.json()['items'][0]['id']

    response = client.patch(f'/cart/items/{item_id}', json={'quantity': 5}, headers=auth_headers)
    assert response.status_code == 200
    assert response.json()['items'][0]['quantity'] == 5

def test_update_nonexistent_cart_item_404(client, auth_headers):
    response = client.patch('/cart/items/999', json={'quantity': 5}, headers=auth_headers)
    assert response.status_code == 404

def test_remove_cart_item(client, auth_headers, admin_auth_headers):
    product_response = client.post(
        '/products', json={'name': 'Mouse', 'price': '24.99', 'stock': 10}, headers=admin_auth_headers
    )
    product_id = product_response.json()['id']
    add_response = client.post('/cart/items', json={'product_id': product_id, 'quantity': 2}, headers=auth_headers)
    item_id = add_response.json()['items'][0]['id']

    response = client.delete(f'/cart/items/{item_id}', headers=auth_headers)
    assert response.status_code == 200
    assert response.json()['items'] == []

def test_cannot_modify_another_users_cart_item(client, admin_auth_headers):
    client.post('/auth/signup', json={'email': 'usera@example.com', 'password': 'testpass123'})
    login_a = client.post('/auth/login', json={'email': 'usera@example.com', 'password': 'testpass123'})
    headers_a = {'Authorization': f"Bearer {login_a.json()['access_token']}"}

    product_response = client.post(
        '/products', json={'name': 'Mouse', 'price': '24.99', 'stock': 10}, headers=admin_auth_headers
    )
    product_id = product_response.json()['id']
    add_response = client.post('/cart/items', json={'product_id': product_id, 'quantity': 1}, headers=headers_a)
    item_id = add_response.json()['items'][0]['id']

    client.post('/auth/signup', json={'email': 'userb@example.com', 'password': 'testpass123'})
    login_b = client.post('/auth/login', json={'email': 'userb@example.com', 'password': 'testpass123'})
    headers_b = {'Authorization': f"Bearer {login_b.json()['access_token']}"}

    response = client.delete(f'/cart/items/{item_id}', headers=headers_b)
    assert response.status_code == 404