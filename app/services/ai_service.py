"""
Mistral AI Service — wraps the Mistral API client.

Provides helper functions for:
- General chat completions
- Resume analysis prompts
- Interview question generation prompts
- Career roadmap generation prompts
"""

try:
    from mistralai import Mistral
except ImportError:
    from mistralai.client import Mistral
from flask import current_app


def _get_client():
    """Create and return a Mistral client using the configured API key."""
    api_key = current_app.config['MISTRAL_API_KEY']
    return Mistral(api_key=api_key)


def chat_with_ai(messages: list[dict]) -> str:
    """
    Send a list of messages to Mistral and return the assistant's reply.

    Args:
        messages: List of dicts with 'role' and 'content' keys.

    Returns:
        The assistant's response text.
    """
    client = _get_client()
    model = current_app.config['MISTRAL_MODEL']

    response = client.chat.complete(
        model=model,
        messages=messages,
    )
    return response.choices[0].message.content


def analyze_resume(resume_text: str) -> str:
    """Send resume text to Mistral for career-focused analysis."""
    messages = [
        {
            "role": "system",
            "content": (
                "You are a senior career coach and resume analyst. "
                "Analyze the following resume and provide: "
                "1) A score out of 100, "
                "2) Strengths, "
                "3) Weaknesses, "
                "4) Actionable improvement suggestions, "
                "5) Recommended job roles."
            ),
        },
        {"role": "user", "content": resume_text},
    ]
    return chat_with_ai(messages)


def generate_interview_questions(job_role: str) -> str:
    """Generate interview questions for a specific job role."""
    messages = [
        {
            "role": "system",
            "content": (
                "You are an expert technical interviewer. "
                "Generate 10 interview questions (mix of technical and behavioral) "
                "for the given job role. For each question, provide a brief ideal answer hint."
            ),
        },
        {"role": "user", "content": f"Job role: {job_role}"},
    ]
    return chat_with_ai(messages)


def generate_career_roadmap(career_goal: str) -> str:
    """Generate a career roadmap for a given goal."""
    messages = [
        {
            "role": "system",
            "content": (
                "You are a career planning expert. "
                "Create a detailed 6-month career roadmap including: "
                "1) Skills to learn (with resources), "
                "2) Projects to build, "
                "3) Certifications to pursue, "
                "4) Networking strategies, "
                "5) Monthly milestones."
            ),
        },
        {"role": "user", "content": f"Career goal: {career_goal}"},
    ]
    return chat_with_ai(messages)
