"""
Speech Service — handles Speech-to-Text and Text-to-Speech.

- STT: Uses the SpeechRecognition library (Google Web Speech API).
- TTS: Uses gTTS (Google Text-to-Speech) to generate audio files.
"""

import os
import uuid
import speech_recognition as sr
from gtts import gTTS
from flask import current_app


def speech_to_text(audio_file_path: str) -> str:
    """
    Convert an audio file to text using SpeechRecognition.

    Args:
        audio_file_path: Path to a WAV audio file.

    Returns:
        Transcribed text string.
    """
    recognizer = sr.Recognizer()

    with sr.AudioFile(audio_file_path) as source:
        audio_data = recognizer.record(source)

    try:
        text = recognizer.recognize_google(
            audio_data,
            language=current_app.config.get('SPEECH_LANG', 'en-US'),
        )
        return text
    except sr.UnknownValueError:
        return "Sorry, I could not understand the audio."
    except sr.RequestError as e:
        return f"Speech recognition service error: {e}"


def text_to_speech(text: str) -> str:
    """
    Convert text to an MP3 audio file using gTTS.

    Args:
        text: The text to convert to speech.

    Returns:
        The relative path to the generated MP3 file (inside static/uploads).
    """
    filename = f"tts_{uuid.uuid4().hex[:8]}.mp3"
    upload_dir = current_app.config['UPLOAD_FOLDER']
    os.makedirs(upload_dir, exist_ok=True)
    filepath = os.path.join(upload_dir, filename)

    tts = gTTS(text=text, lang='en')
    tts.save(filepath)

    # Return path relative to static/ for use in templates
    return f"uploads/{filename}"
