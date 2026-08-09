"""
Roadmap Blueprint — generate a career roadmap using AI.
"""

from flask import Blueprint, render_template, request
from flask_login import login_required

from app.services.ai_service import generate_career_roadmap

roadmap_bp = Blueprint('roadmap', __name__, url_prefix='/roadmap')


@roadmap_bp.route('/', methods=['GET', 'POST'])
@login_required
def index():
    """Generate a career roadmap based on user's goal."""
    roadmap = None

    if request.method == 'POST':
        career_goal = request.form.get('career_goal', '').strip()
        if career_goal:
            roadmap = generate_career_roadmap(career_goal)

    return render_template('roadmap/index.html', roadmap=roadmap)
