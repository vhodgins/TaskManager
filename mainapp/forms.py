from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, BooleanField, ValidationError, DateTimeField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from mainapp.models import User
from flask_login import current_user

class Check(FlaskForm):

    submit = SubmitField()


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])

    password = PasswordField('Password', validators=[DataRequired()])

    remember = BooleanField('Remember Me')

    submit = SubmitField('Login')


class CreateTask(FlaskForm):
    title = TextAreaField('Title', validators=[DataRequired(), Length(max=100)])

    content = StringField('Content', validators=[])

    #deadline = DateTimeField('Deadline', validators=[DataRequired()])
    days = IntegerField('Days', validators=[])
    weeks = IntegerField('Weels', validators=[])

    submit = SubmitField('Create Task')



class CommentForm(FlaskForm):

    content = StringField('Content', validators=[])

    #deadline = DateTimeField('Deadline', validators=[DataRequired()])

    submit = SubmitField('Post Comment')



class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=1, max=15)])

    email = StringField('Email', validators=[DataRequired(), Email()])

    password = PasswordField('Password', validators=[DataRequired()])

    passwordConf = PasswordField('Password Confirmation', validators=[EqualTo('password')])

    remember = BooleanField('Remember Me')

    submit = SubmitField('Login')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('This Username is Taken')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('This Email is Taken')

class UpdateForm(FlaskForm):
    username = StringField('username', validators=[DataRequired(), Length(min=2, max=20)])

    email = StringField('email', validators=[DataRequired(), Email()])

    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])

    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('This Username is Taken')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('This Email is Taken')
