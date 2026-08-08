"""
Speech Blueprint — handles Speech-to-Text and Text-to-Speech endpoints.
"""

import os
import uuid
from flask import Blueprint, request, jsonify, current_app
from flask_login import login_required

from app.services.speech_service import speech_to_text, text_to_speech

speech_bp = Blueprint('speech', __name__, url_prefix='/speech')


@speech_bp.route('/stt', methods=['POST'])
@login_required
def stt():
    """
    Receive an audio file (WAV) and return transcribed text.
    Used by the frontend microphone recording feature.
    """
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file provided'}), 400

    audio_file = request.files['audio']
    upload_dir = current_app.config['UPLOAD_FOLDER']
    os.makedirs(upload_dir, exist_ok=True)

    filename = f"stt_{uuid.uuid4().hex[:8]}.wav"
    filepath = os.path.join(upload_dir, filename)
    audio_file.save(filepath)

    text = speech_to_text(filepath)

    # Clean up temp file
    os.remove(filepath)

    return jsonify({'text': text})


@speech_bp.route('/tts', methods=['POST'])
@login_required
def tts():
    """
    Receive text and return a path to the generated MP3 audio file.
    Used to read AI responses aloud.
    """
    data = request.get_json()
    text = data.get('text', '').strip()

    if not text:
        return jsonify({'error': 'No text provided'}), 400

    audio_path = text_to_speech(text)
    return jsonify({'audio_url': f'/static/{audio_path}'})
