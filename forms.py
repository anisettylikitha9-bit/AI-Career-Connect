"""
Flask-WTF forms for AI Career Connect.

Contains form classes for user registration, login,
chat input, resume upload, and interview question generation.
"""

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Length


class RegistrationForm(FlaskForm):
    """User registration form."""
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=80)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    """User login form."""
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class ChatForm(FlaskForm):
    """AI chat input form."""
    message = TextAreaField('Your Message', validators=[DataRequired()])
    submit = SubmitField('Send')


class ResumeUploadForm(FlaskForm):
    """Resume file upload form."""
    resume = FileField('Upload Resume (PDF)', validators=[
        FileAllowed(['pdf'], 'Only PDF files are allowed!')
    ])
    submit = SubmitField('Analyze Resume')


class InterviewForm(FlaskForm):
    """Interview question generator form."""
    job_role = StringField('Job Role', validators=[DataRequired(), Length(max=120)])
    submit = SubmitField('Generate Questions')
