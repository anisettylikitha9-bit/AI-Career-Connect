"""
Chat Blueprint — AI chat assistant with conversation history.
"""

import uuid
from flask import Blueprint, render_template, request, jsonify, session
from flask_login import login_required, current_user

from app import db
from app.models import ChatHistory
from app.services.ai_service import chat_with_ai

chat_bp = Blueprint('chat', __name__, url_prefix='/chat')


@chat_bp.route('/')
@login_required
def index():
    """Render the chat interface."""
    # Create a new session ID if one doesn't exist
    if 'chat_session_id' not in session:
        session['chat_session_id'] = str(uuid.uuid4())

    # Load existing chat history for this session
    history = ChatHistory.query.filter_by(
        user_id=current_user.id,
        session_id=session['chat_session_id'],
    ).order_by(ChatHistory.timestamp.asc()).all()

    return render_template('chat/index.html', history=history)


@chat_bp.route('/send', methods=['POST'])
@login_required
def send_message():
    """Process a user message and return the AI response."""
    data = request.get_json()
    user_message = data.get('message', '').strip()

    if not user_message:
        return jsonify({'error': 'Empty message'}), 400

    session_id = session.get('chat_session_id', str(uuid.uuid4()))

    # Save user message
    user_chat = ChatHistory(
        user_id=current_user.id,
        role='user',
        message=user_message,
        session_id=session_id,
    )
    db.session.add(user_chat)

    # Build conversation context from history
    history = ChatHistory.query.filter_by(
        user_id=current_user.id,
        session_id=session_id,
    ).order_by(ChatHistory.timestamp.asc()).all()

    messages = [
        {"role": "system", "content": "You are a helpful AI career advisor. Help users with career guidance, resume tips, interview prep, and professional development."},
    ]
    for chat in history:
        messages.append({"role": chat.role, "content": chat.message})
    messages.append({"role": "user", "content": user_message})

    # Get AI response
    ai_response = chat_with_ai(messages)

    # Save AI response
    ai_chat = ChatHistory(
        user_id=current_user.id,
        role='assistant',
        message=ai_response,
        session_id=session_id,
    )
    db.session.add(ai_chat)
    db.session.commit()

    return jsonify({'response': ai_response})


@chat_bp.route('/new-session')
@login_required
def new_session():
    """Start a fresh chat session."""
    session['chat_session_id'] = str(uuid.uuid4())
    return jsonify({'status': 'ok', 'session_id': session['chat_session_id']})


@chat_bp.route('/history')
@login_required
def history():
    """Return all chat sessions for the current user."""
    sessions = db.session.query(ChatHistory.session_id).filter_by(
        user_id=current_user.id
    ).distinct().all()

    return render_template('chat/history.html', sessions=[s[0] for s in sessions])
