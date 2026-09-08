def test_signup_and_login(client):
    signup_response = client.post(
        '/auth/signup', json={'email': 'a@b.com', 'password': 'testpass123'}
    )
    assert signup_response.status_code == 201
    body = signup_response.json()
    assert body['email'] == 'a@b.com'
    assert 'hashed_password' not in body

    login_response = client.post(
        '/auth/login', json={'email': 'a@b.com', 'password': 'testpass123'}
    )

    assert login_response.status_code == 200
    assert 'access_token' in login_response.json()

def test_login_wrong_password_fails(client):
    client.post(
        '/auth/signup', json={'email': 'a@b.com', 'password': 'testpass123'}
    )
    response = client.post(
        '/auth/login', json={'email': 'a@b.com', 'password': 'wrongpassword'}
    )

    assert response.status_code == 401

def test_signup_duplicate_email_fails(client):
    client.post('/auth/signup', json={'email': 'a@b.com', 'password': 'testpass123'})
    response = client.post(
        '/auth/signup', json={'email': 'a@b.com', 'password': 'testpass123'}
    )
    assert response.status_code == 400

def test_read_me_requires_auth(client):
    response = client.get('/auth/me')
    assert response.status_code == 401

def test_read_me_rejects_token_for_deleted_user(client):
    from core.security import create_access_token

    token = create_access_token(subject='99999')
    response = client.get(
        '/auth/me', headers={'Authorization': f'Bearer {token}'}
    )
    assert response.status_code == 401

def test_read_me_rejects_invalid_token(client):
    response = client.get(
        '/auth/me', headers={'Authorization': 'Bearer garbage-token'}
    )
    assert response.status_code == 401

def test_login_read_me(client):
    client.post(
        '/auth/signup', json={'email': 'a@b.com', 'password': 'testpass123'}
    )
    login_response = client.post(
        '/auth/login', json={'email': 'a@b.com', 'password': 'testpass123'}
    )
    token = login_response.json()['access_token']

    response = client.get(
        '/auth/me', headers={'Authorization': f'Bearer {token}'}
    )
    assert response.status_code == 200
    body = response.json()
    assert body['email'] == 'a@b.com'
    assert 'hashed_password' not in body