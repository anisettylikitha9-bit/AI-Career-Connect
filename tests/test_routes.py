"""
Test: Feature routes authorization and rendering.
"""

import pytest
from app import create_app, db
from app.models import User


@pytest.fixture
def app():
    app = create_app('testing')
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


def test_protected_routes_redirect_unauthenticated(client):
    """Unauthenticated users should be redirected to login page."""
    routes = ['/', '/dashboard/', '/chat/', '/resume/', '/interview/', '/roadmap/']
    for route in routes:
        response = client.get(route, follow_redirects=True)
        assert response.status_code == 200
        assert b'Login' in response.data


def test_authenticated_dashboard_access(client, app):
    """Authenticated user should be able to access the dashboard."""
    with app.app_context():
        user = User(username='dashuser', email='dash@example.com')
        user.set_password('pass123')
        db.session.add(user)
        db.session.commit()

    client.post('/auth/login', data={'email': 'dash@example.com', 'password': 'pass123'})
    response = client.get('/dashboard/')
    assert response.status_code == 200
    assert b'Dashboard' in response.data
