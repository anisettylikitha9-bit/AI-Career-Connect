"""
Database models for AI Career Connect.

Defines all SQLAlchemy ORM models:
- User          : registered users (login / registration)
- ChatHistory   : stores every AI conversation message
- ResumeAnalysis: stores resume analysis results
- InterviewQuestion: stores generated interview questions
"""

from datetime import datetime, timezone
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login_manager


# Flask-Login user loader callback
@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


class User(UserMixin, db.Model):
    """Registered user account."""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    chats = db.relationship('ChatHistory', backref='user', lazy='dynamic')
    resumes = db.relationship('ResumeAnalysis', backref='user', lazy='dynamic')
    interviews = db.relationship('InterviewQuestion', backref='user', lazy='dynamic')

    def __init__(self, username=None, email=None, **kwargs):
        if username is not None:
            kwargs['username'] = username
        if email is not None:
            kwargs['email'] = email
        super().__init__(**kwargs)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'


class ChatHistory(db.Model):
    """Stores each message in a user ↔ AI conversation."""
    __tablename__ = 'chat_history'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    role = db.Column(db.String(20), nullable=False)          # 'user' or 'assistant'
    message = db.Column(db.Text, nullable=False)
    session_id = db.Column(db.String(36), nullable=False)     # groups messages in one chat session
    timestamp = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def __init__(self, user_id=None, role=None, message=None, session_id=None, **kwargs):
        if user_id is not None:
            kwargs['user_id'] = user_id
        if role is not None:
            kwargs['role'] = role
        if message is not None:
            kwargs['message'] = message
        if session_id is not None:
            kwargs['session_id'] = session_id
        super().__init__(**kwargs)

    def __repr__(self):
        return f'<Chat {self.role}: {self.message[:30]}>'


class ResumeAnalysis(db.Model):
    """Stores the result of an AI resume analysis."""
    __tablename__ = 'resume_analyses'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    analysis_text = db.Column(db.Text, nullable=False)
    score = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def __init__(self, user_id=None, filename=None, analysis_text=None, score=None, **kwargs):
        if user_id is not None:
            kwargs['user_id'] = user_id
        if filename is not None:
            kwargs['filename'] = filename
        if analysis_text is not None:
            kwargs['analysis_text'] = analysis_text
        if score is not None:
            kwargs['score'] = score
        super().__init__(**kwargs)

    def __repr__(self):
        return f'<Resume {self.filename}>'


class InterviewQuestion(db.Model):
    """Stores generated interview questions per role / topic."""
    __tablename__ = 'interview_questions'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    job_role = db.Column(db.String(120), nullable=False)
    questions_json = db.Column(db.Text, nullable=False)       # JSON array of Q&A pairs
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def __init__(self, user_id=None, job_role=None, questions_json=None, **kwargs):
        if user_id is not None:
            kwargs['user_id'] = user_id
        if job_role is not None:
            kwargs['job_role'] = job_role
        if questions_json is not None:
            kwargs['questions_json'] = questions_json
        super().__init__(**kwargs)

    def __repr__(self):
        return f'<Interview {self.job_role}>'
