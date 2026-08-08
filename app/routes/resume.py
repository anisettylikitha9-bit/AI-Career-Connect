"""
Resume Blueprint — upload and AI-analyze resumes.
"""

import os
from flask import Blueprint, render_template, flash, redirect, url_for, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename

from app import db
from app.models import ResumeAnalysis
from app.forms import ResumeUploadForm
from app.services.ai_service import analyze_resume

resume_bp = Blueprint('resume', __name__, url_prefix='/resume')


def _extract_text_from_pdf(filepath: str) -> str:
    """Extract raw text from a PDF file using pdfminer."""
    from pdfminer.high_level import extract_text
    return extract_text(filepath)


@resume_bp.route('/', methods=['GET', 'POST'])
@login_required
def index():
    """Upload a resume PDF and receive AI analysis."""
    form = ResumeUploadForm()

    if form.validate_on_submit():
        file = form.resume.data
        filename = secure_filename(file.filename)
        upload_dir = current_app.config['UPLOAD_FOLDER']
        os.makedirs(upload_dir, exist_ok=True)
        filepath = os.path.join(upload_dir, filename)
        file.save(filepath)

        # Extract text and analyze
        resume_text = _extract_text_from_pdf(filepath)
        analysis = analyze_resume(resume_text)

        # Save to DB
        record = ResumeAnalysis(
            user_id=current_user.id,
            filename=filename,
            analysis_text=analysis,
            score=0,  # Could be parsed from AI response
        )
        db.session.add(record)
        db.session.commit()

        flash('Resume analyzed successfully!', 'success')
        return render_template('resume/result.html', analysis=analysis, filename=filename)

    # Show past analyses
    past = ResumeAnalysis.query.filter_by(user_id=current_user.id).order_by(
        ResumeAnalysis.created_at.desc()
    ).all()

    return render_template('resume/index.html', form=form, past_analyses=past)
