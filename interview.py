"""
Interview Blueprint — generate interview questions for a target role.
"""

from flask import Blueprint, render_template, flash
from flask_login import login_required, current_user

from app import db
from app.models import InterviewQuestion
from app.forms import InterviewForm
from app.services.ai_service import generate_interview_questions

interview_bp = Blueprint('interview', __name__, url_prefix='/interview')


@interview_bp.route('/', methods=['GET', 'POST'])
@login_required
def index():
    """Generate interview questions for a specified job role."""
    form = InterviewForm()

    if form.validate_on_submit():
        job_role = form.job_role.data
        questions = generate_interview_questions(job_role)

        # Save to DB
        record = InterviewQuestion(
            user_id=current_user.id,
            job_role=job_role,
            questions_json=questions,
        )
        db.session.add(record)
        db.session.commit()

        flash('Interview questions generated!', 'success')
        return render_template('interview/result.html', questions=questions, job_role=job_role)

    # Past generations
    past = InterviewQuestion.query.filter_by(user_id=current_user.id).order_by(
        InterviewQuestion.created_at.desc()
    ).all()

    return render_template('interview/index.html', form=form, past_questions=past)
