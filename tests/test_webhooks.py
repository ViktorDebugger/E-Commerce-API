from unittest.mock import patch, MagicMock

import stripe

@patch('stripe.Webhook.construct_event')
@patch('stripe.PaymentIntent.create')
def test_webhook_marks_order_paid(mock_payment_intent_create, mock_construct_event, client, auth_headers, admin_auth_headers):
    mock_payment_intent_create.return_value = MagicMock(id='pi_test123', client_secret='pi_test123_secret_x')

    product_response = client.post(
        '/products', json={'name': 'Mouse', 'price': '24.99', 'stock': 10}, headers=admin_auth_headers
    )
    product_id = product_response.json()['id']
    client.post('/cart/items', json={'product_id': product_id, 'quantity': 1}, headers=auth_headers)
    checkout_response = client.post('/checkout', headers=auth_headers)
    order_id = checkout_response.json()['order']['id']

    mock_construct_event.return_value = {
        'type': 'payment_intent.succeeded',
        'data': {'object': {'id': 'pi_test123'}},
    }

    response = client.post(
        '/webhooks/stripe',
        content=b'{}',
        headers={'stripe-signature': 'fake-signature'},
    )
    assert response.status_code == 200

    order_response = client.get(f'/orders/{order_id}', headers=auth_headers)
    assert order_response.json()['status'] == 'paid'

@patch('stripe.Webhook.construct_event')
def test_webhook_rejects_invalid_signature(mock_construct_event, client):
    mock_construct_event.side_effect = stripe.error.SignatureVerificationError('bad sig', 'sig_header')

    response = client.post(
        '/webhooks/stripe',
        content=b'{}',
        headers={'stripe-signature': 'bad-signature'},
    )
    assert response.status_code == 400

@patch('stripe.Webhook.construct_event')
def test_webhook_ignores_unhandled_event_types(mock_construct_event, client):
    mock_construct_event.return_value = {
        'type': 'customer.created',
        'data': {'object': {'id': 'cus_fake'}},
    }

    response = client.post(
        '/webhooks/stripe',
        content=b'{}',
        headers={'stripe-signature': 'fake-signature'},
    )
    assert response.status_code == 200