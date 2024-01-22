from wtforms import Form,StringField,TextAreaField,IntegerField,PasswordField,validators

#Kullanıcı Kayıt Formu
class RegisterForm(Form):
    name = StringField("Name Surname:",validators=[validators.Length(min=4,max=24)])
    username = StringField("Username:",validators=[validators.Length(min=4,max=34)])
    email = StringField("Email Address:",validators=[validators.Email(message="Please enter a correct email address!")])
    password = PasswordField("Password:",validators=[
        validators.DataRequired(message="Please enter a password!"),
        validators.EqualTo(fieldname="confirm",message="Your password does not match!")
        ])
    confirm = PasswordField("Password Verify:")
class LoginForm(Form):
    username = StringField("Username:")
    password = PasswordField("Password:")

class CallbackForm(Form):
    pass

#Class Form
class ClassForm(Form):
    centername = StringField("Boxing Center Name:",validators=[validators.Length(min=3,max=100)])
    coachname = StringField("Coach Name:",validators=[validators.Length(min=3,max=20)])
    phone =  StringField("Phone:",validators=[validators.Length(min=11,max=11)])
    location =  StringField("Location:",validators=[validators.Length(min=3,max=20)])
    price = IntegerField("Price:",validators=[validators.NumberRange(min=1)])
    aboutcoach = TextAreaField("Introduce Coach:",validators=[validators.Length(min=10,max=500)])