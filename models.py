from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import UserMixin , current_user
import datetime
import time
from datetime import datetime as dt
from flask_admin.contrib.sqla import ModelView
from flask_admin import AdminIndexView

db = SQLAlchemy()
class Userr(UserMixin,db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    FirstName = db.Column(db.String(255), nullable=False)
    LastName = db.Column(db.String(255), nullable=False)
    Password = db.Column(db.String(255), nullable=False)
    Mail = db.Column(db.String(255), unique=True, nullable=True)
    Phone = db.Column(db.String(255), unique=True,nullable=False)
    Photo = db.Column(db.Text, nullable=True)
    Role = db.Column(db.String(255), default='Admin')
    
class Car(db.Model):
    __tablename__= 'cars'
    id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(300))
    Marque = db.Column(db.String(300))
    Modele = db.Column(db.String(300))
    Version = db.Column(db.String(300))
    Kilo= db.Column(db.String(300))
    Energie = db.Column(db.String(300))
    Boite = db.Column(db.String(300))
    Description  = db.Column(db.Text)
    Photos = db.Column(db.Text)


class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated

class MyModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated