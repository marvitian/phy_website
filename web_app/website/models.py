from . import db 

from flask_login import UserMixin
from sqlalchemy.sql import func # gives date and time

class User(db.Model, UserMixin):
    # TODO: Change to just DATE NOT DATETIME
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150))
    password = db.Column(db.String(150))
    phy_cfgs = db.Column(db.JSON)
    # data_rates = db.Column(db.JSON())
    release_date = db.Column(db.DateTime(timezone=True))
    output_path = db.Column(db.String(150))
    requests = db.relationship('Request')
    
    
class Request(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.JSON)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    status = db.Column(db.String(150))
    output_rate = db.Column(db.SmallInteger)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    



