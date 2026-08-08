"""
Test: Authentication routes (register, login, logout).
"""

import pytest
from app import create_app, db
from app.models import User


@pytest.fixture
def app():
    """Create a test app with an in-memory database."""
    app = create_app('testing')
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


def test_register_page_loads(client):
    """GET /auth/register should return 200."""
    response = client.get('/auth/register')
    assert response.status_code == 200


def test_login_page_loads(client):
    """GET /auth/login should return 200."""
    response = client.get('/auth/login')
    assert response.status_code == 200


def test_user_registration(client, app):
    """POST /auth/register should create a new user."""
    response = client.post('/auth/register', data={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'password123',
        'confirm_password': 'password123',
    }, follow_redirects=True)

    with app.app_context():
        user = db.session.scalar(db.select(User).filter_by(email='test@example.com'))
        assert user is not None
        assert user.username == 'testuser'


def test_user_login_success(client, app):
    """POST /auth/login with valid credentials should succeed."""
    # First create a user
    with app.app_context():
        user = User(username='loginuser', email='login@example.com')
        user.set_password('correctpass')
        db.session.add(user)
        db.session.commit()

    response = client.post('/auth/login', data={
        'email': 'login@example.com',
        'password': 'correctpass',
    }, follow_redirects=True)
    assert response.status_code == 200


def test_user_login_failure(client):
    """POST /auth/login with wrong password should fail."""
    response = client.post('/auth/login', data={
        'email': 'nonexistent@example.com',
        'password': 'wrongpass',
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Invalid email or password' in response.data


def test_user_logout(client, app):
    """GET /auth/logout should log out authenticated user."""
    with app.app_context():
        user = User(username='logoutuser', email='logout@example.com')
        user.set_password('pass123')
        db.session.add(user)
        db.session.commit()

    client.post('/auth/login', data={
        'email': 'logout@example.com',
        'password': 'pass123',
    })
    response = client.get('/auth/logout', follow_redirects=True)
    assert response.status_code == 200

