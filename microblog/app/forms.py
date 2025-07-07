from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo,Length
import sqlalchemy as sa
from app import db
from app.models import User
from wtforms import TextAreaField
from flask_babel import _, lazy_gettext as _l


class LoginForm(FlaskForm):
    username = StringField(_l("Username"), validators=[DataRequired()])
    password = PasswordField(_l("Password"), validators=[DataRequired()])
    remember_me = BooleanField(_l("Remember Me"))
    submit = SubmitField(_l("Sign in"))

class RegistrationForm(FlaskForm):
    username = StringField(_l('Username'), validators=[DataRequired()])
    password = PasswordField(_l("Password"), validators=[DataRequired()])
    email = StringField(_l("Email"), validators=[DataRequired(), Email()])
    password2 = PasswordField(_l("Repeat password"), validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField(_l("Register"))

    def validate_username(self,username):
        user = db.session.scalar(sa.select(User).where(User.username == username.data))
        if user is not None:
            raise ValidationError(_l("Please use a different name."))
        
    def validate_email(self, email):
        user = db.session.scalar(sa.select(User).where(User.email==email.data))
        if user is not None:
            raise ValidationError(_l("Please use a different email address."))
        
class EditProfileForm(FlaskForm):
    username = StringField(_l("Username"), validators=[DataRequired()])
    about_me = StringField(_l("About me"), validators=[Length(min=0, max=140)])
    submit= SubmitField(_l("Submit"))


    def __init__(self, original_username, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data!=self.original_username:
            user = db.session.scalar(sa.select(User).where(User.username==username.data))
            if user is not None:
                raise ValidationError(_l("Please use different username"))
            
class EmptyForm(FlaskForm):
    submit= SubmitField("Submit")
    

class PostForm(FlaskForm):
    post = TextAreaField(_l("Say something"), validators=[DataRequired(),Length(min=1,max=14)])
    submit = SubmitField(_l("Submit"))

class ResetPasswordRequestForm(FlaskForm):
    email = StringField(_l("Email"), validators=[DataRequired(), Email()])
    submit=SubmitField(_l("Reset password"))


class ResetPasswordForm(FlaskForm):
    password = PasswordField(_l("Password"), validators=[DataRequired()])
    password2 = PasswordField(_l("Repeat password"), validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField(_l("Request password reset"))