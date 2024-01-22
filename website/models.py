from . import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    email = db.Column(db.Text)
    username = db.Column(db.Text)
    password = db.Column(db.Text)

class Classes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    centername = db.Column(db.Text)
    coachname = db.Column(db.Text)
    phone = db.Column(db.Text)
    location = db.Column(db.Text)
    price = db.Column(db.Integer) 
    aboutcoach = db.Column(db.Text) 
    admin = db.Column(db.Text)     
    
class carts(db.Model):
    no = db.Column(db.Integer,primary_key=True)
    id = db.Column(db.Integer)
    centername = db.Column(db.Text)
    coachname = db.Column(db.Text)
    phone = db.Column(db.Text)
    location = db.Column(db.Text)
    price = db.Column(db.Integer) 
    admin = db.Column(db.Text) 
    owner = db.Column(db.Text)

class complate(db.Model):
    no = db.Column(db.Integer,primary_key=True)
    id = db.Column(db.Integer)
    centername = db.Column(db.Text)
    coachname = db.Column(db.Text)
    phone = db.Column(db.Text)
    location = db.Column(db.Text)
    price = db.Column(db.Integer) 
    admin = db.Column(db.Text) 
    owner = db.Column(db.Text)
    time = db.Column(db.DateTime, default=lambda: datetime.utcnow().replace(microsecond=0)) 

class Callback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text,nullable=False)
    phone = db.Column(db.Text,nullable=False)
    email = db.Column(db.Text,nullable=False)
    message = db.Column(db.Text,nullable=False)