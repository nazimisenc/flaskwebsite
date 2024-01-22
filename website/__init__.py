from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_admin.contrib.sqla import ModelView
from flask_admin import Admin
from flask_babel import Babel

db = SQLAlchemy()
DB_NAME = "oxer.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'oxer'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)
    babel = Babel(app)
    
    admin = Admin(app, name='Oxer Admin Panel', template_mode='bootstrap4')

    from .views import views
    
    app.register_blueprint(views, url_prefix='/')

    from .models import users, Classes, carts, Callback, complate
    
    admin.add_view(ModelView(users, db.session))
    admin.add_view(ModelView(Classes, db.session))
    admin.add_view(ModelView(Callback, db.session))
    admin.add_view(ModelView(carts, db.session))
    admin.add_view(ModelView(complate, db.session))

    create_database(app)

    return app



def create_database(app):
    app.app_context().push()

    if not path.exists('website/' + DB_NAME):
        db.create_all()
        print('Created Database!')