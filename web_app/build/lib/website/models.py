from . import db # from this package __init__.py import db

# Module helps us log users in
from flask_login import UserMixin
from sqlalchemy.sql import func # gives date and time

# A databse model is a layout or blueprint for an object that will be stored in your database 
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
class User(db.Model, UserMixin):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150))    # either company name or person's name
    password = db.Column(db.String(150))
    phy_cfg = db.Column(db.JSON)
    # data_rates = db.Column(db.JSON())
    release_date = db.Column(db.DateTime(timezone=True))
    perm_lvl = db.Column(db.SmallInteger)
    requests = db.relationship('Request')
    
    
class Request(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.JSON) # TODO: db.JSON? I have to decide how it will be recieved first
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    status = db.Column(db.String(150))
    output_rate = db.Column(db.SmallInteger)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    



