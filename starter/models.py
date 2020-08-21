import os
from sqlalchemy import Column, String, Integer, DateTime ,Enum
from flask_sqlalchemy import SQLAlchemy
import json


database_filename = "database.db"
project_dir = os.path.dirname(os.path.abspath(__file__))
database_path = "sqlite:///{}".format(os.path.join(project_dir, database_filename))

db = SQLAlchemy()



def setup_db(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()





class Movie(db.Model):
    id = Column(Integer().with_variant(Integer , 'sqlite'), primary_key=True)
    title = Column(String(80))
    relaseData = Column(String(80))

    def format(self):
        return {
            'id': self.id,
            'title' : self.title,
            'relaseData': self.relaseData
        }


    def insert(self):
        db.session.add(self)
        db.session.commit()


    def delete(self):
        db.session.delete(self)
        db.session.commit()


    def update(self):
        db.session.commit()


class Actor(db.Model):
    id = Column(Integer().with_variant(Integer , 'sqlite'), primary_key=True)
    name  = Column(String(80))
    age = Column(Integer())
    gender = Column(Enum('M', 'F'))
    
    def format(self):
        return {
            'name' : self.name,
            'age' : self.age,
            'gender' : self.gender
        }


    def insert(self):
        db.session.add(self)
        db.session.commit()


    def delete(self):
        db.session.delete(self)
        db.session.commit()


    def update(self):
        db.session.commit()