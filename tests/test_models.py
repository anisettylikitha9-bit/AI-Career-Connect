"""
Test: Database models creation and relationships.
"""

import pytest
from app import create_app, db
from app.models import User, ChatHistory, ResumeAnalysis


@pytest.fixture
def app():
    app = create_app('testing')
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


def test_user_password_hashing(app):
    """User password should be hashed and verifiable."""
    with app.app_context():
        user = User(username='test', email='test@test.com')
        user.set_password('secret')
        assert user.check_password('secret') is True
        assert user.check_password('wrong') is False


def test_chat_history_relationship(app):
    """ChatHistory should link back to User."""
    with app.app_context():
        user = User(username='test', email='test@test.com')
        user.set_password('secret')
        db.session.add(user)
        db.session.commit()

        chat = ChatHistory(
            user_id=user.id,
            role='user',
            message='Hello',
            session_id='abc123',
        )
        db.session.add(chat)
        db.session.commit()

        assert user.chats.count() == 1
