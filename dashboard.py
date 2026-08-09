"""
Dashboard Blueprint — dynamic dashboard with user stats and activity.
"""

from flask import Blueprint, render_template
from flask_login import login_required, current_user

from app.models import ChatHistory, ResumeAnalysis, InterviewQuestion

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')


@dashboard_bp.route('/')
@login_required
def index():
    """Render the main dashboard with aggregated user statistics."""
    stats = {
        'total_chats': ChatHistory.query.filter_by(user_id=current_user.id, role='user').count(),
        'total_resumes': ResumeAnalysis.query.filter_by(user_id=current_user.id).count(),
        'total_interviews': InterviewQuestion.query.filter_by(user_id=current_user.id).count(),
        'recent_chats': ChatHistory.query.filter_by(
            user_id=current_user.id
        ).order_by(ChatHistory.timestamp.desc()).limit(5).all(),
        'recent_resumes': ResumeAnalysis.query.filter_by(
            user_id=current_user.id
        ).order_by(ResumeAnalysis.created_at.desc()).limit(3).all(),
    }
    return render_template('dashboard/index.html', stats=stats)
