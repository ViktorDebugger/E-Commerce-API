from unittest.mock import patch, MagicMock

def test_checkout_empty_cart_fails(client, auth_headers):
    response = client.post('/checkout', headers=auth_headers)
    assert response.status_code == 400

@patch('stripe.PaymentIntent.create')
def test_checkout_creates_order_and_clears_cart(mock_create, client, auth_headers, admin_auth_headers):
    mock_create.return_value = MagicMock(id='pi_fake123', client_secret='pi_fake123_secret_abc')

    product_response = client.post(
        '/products', json={'name': 'Mouse', 'price': '24.99', 'stock': 10}, headers=admin_auth_headers
    )
    product_id = product_response.json()['id']
    client.post('/cart/items', json={'product_id': product_id, 'quantity': 2}, headers=auth_headers)

    response = client.post('/checkout', headers=auth_headers)
    assert response.status_code == 201
    body = response.json()
    assert body['order']['total'] == '49.98'
    assert body['order']['status'] == 'pending'
    assert body['client_secret'] == 'pi_fake123_secret_abc'

    cart_response = client.get('/cart', headers=auth_headers)
    assert cart_response.json()['items'] == []