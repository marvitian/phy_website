#

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
# from turbo_flask import Turbo
import logging

# Logging Format
format = "%(asctime)s: %(message)s"
logging.basicConfig(format=format, level=logging.INFO,
                    datefmt="%H:%M:%S")

db = SQLAlchemy()
DB_NAME = "databse.db"
app = Flask(__name__) # name of the file
# turbo = Turbo(app)

# Available phy cfgs


def create_app():
    
    app.config['SECRET_KEY'] = 'thesixsemi' # encrypte of secure our cookie data for our app
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}' # My SQLAlchemy databse is stored or located at 
    db.init_app(app) # initialize our databse
    # we need to define our databse models or tables
    # if we want to store something in our databse, we need to define the schema, what the database will look like
    
   
    
    # We need to register the blueprints that we made
    from .views import views
    from .auth import auth
    
    app.register_blueprint(views, url_prefix='/')   # url_prefix - the prefix for the blueprint
    app.register_blueprint(auth, url_prefix='/')

    # we need to make sure .models runs to define the classes
    from .models import User, Request
    # create_database(app)
    
    with app.app_context():
        db.create_all()
    
    
    login_manager = LoginManager()
    # where should flask redirect us if the user is not logged in and there's a login required?
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    
    # Telling flask how we load a user
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id)) # works like filter_by except by default it filters by id
    
    
    return app

# checks if databse exists, if it doesn't create it
def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')