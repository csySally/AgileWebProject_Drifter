from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, HiddenField
from wtforms.validators import DataRequired
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User, Send, Reply

class LoginForm(FlaskForm):
  username = StringField('username', validators=[DataRequired()])
  password = PasswordField('password', validators=[DataRequired()])
  submit = SubmitField('login')
  
class RegistrationForm(FlaskForm):
  username = StringField('Username', validators=[DataRequired()])
  password = PasswordField('Password', validators=[DataRequired()])
  password2 = PasswordField(
  'Repeat Password', validators=[DataRequired(), EqualTo('password')])
  submit = SubmitField('Register')
  def validate_username(self, username):
    user = User.query.filter_by(username=username.data).first()
    if user is not None:
      raise ValidationError('Please use a different username.')


class SendForm(FlaskForm):
    send = TextAreaField('Send', validators=[DataRequired()])
    label = StringField('Label')  
    anonymous = BooleanField('Anonymous')
    submit = SubmitField('Send')

class ReplyForm(FlaskForm):
    reply = TextAreaField('Reply', validators=[DataRequired()])
    send_id = TextAreaField('Send ID')
    anonymous = BooleanField('Anonymous')
    submit = SubmitField('Reply')
