from unittest.mock import patch, MagicMock

def test_list_orders_empty(client, auth_headers):
    response = client.get('/orders', headers=auth_headers)
    assert response.status_code == 200
    assert response.json() == []

@patch('stripe.PaymentIntent.create')
def test_order_ownership_check(mock_create, client, auth_headers, admin_auth_headers):
    mock_create.return_value = MagicMock(id='pi_fake', client_secret='pi_fake_secret_x')

    product_response = client.post(
        '/products', json={'name': 'Mouse', 'price': '24.99', 'stock': 10}, headers=admin_auth_headers
    )
    product_id = product_response.json()['id']
    client.post('/cart/items', json={'product_id': product_id, 'quantity': 1}, headers=auth_headers)
    checkout_response = client.post('/checkout', headers=auth_headers)
    order_id = checkout_response.json()['order']['id']

    client.post('/auth/signup', json={'email': 'other@example.com', 'password': 'testpass123'})
    login = client.post('/auth/login', json={'email': 'other@example.com', 'password': 'testpass123'})
    other_headers = {'Authorization': f"Bearer {login.json()['access_token']}"}

    response = client.get(f'/orders/{order_id}', headers=other_headers)
    assert response.status_code == 404

    own_response = client.get(f'/orders/{order_id}', headers=auth_headers)
    assert own_response.status_code == 200