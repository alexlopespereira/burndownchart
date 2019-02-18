from flask_wtf import Form
from flask_wtf.file import FileRequired, FileAllowed
from wtforms import PasswordField, StringField, SubmitField, IntegerField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, EqualTo, Length

# Set your classes here.


class InputForm(Form):
    date = DateField('Data da Digitizacao', format='%Y-%m-%d')
    qtd = IntegerField()
    submit = SubmitField("Enviar")


class LoginForm(Form):
    name = StringField('Username', [DataRequired()])
    password = PasswordField('Password', [DataRequired()])


class ForgotForm(Form):
    email = StringField(
        'Email', validators=[DataRequired(), Length(min=6, max=40)]
    )
