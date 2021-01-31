from flask_wtf import Form
from wtforms import StringField, BooleanField , PasswordField,validators,IntegerField

class LoginForm(Form):
    email = StringField('email',validators=[validators.required()])
    password = PasswordField('password',validators=[validators.required()])



class RegisterForm(Form):
    name = StringField('name',validators=[validators.required()])
    rollno = IntegerField('rollno',validators=[validators.required()])
    email = StringField('email',validators=[validators.required()])
    password = PasswordField('password',validators=[validators.required()])
    standard = StringField('standard',validators=[validators.required()])
    marks = StringField('marks')
