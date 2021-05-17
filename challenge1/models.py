# All code is compliant with PEP8 style guidelines

'''I will be using a Postgres DB with the SQLAlchemy ORM
for data storage and retrieval'''

import os
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy import create_engine
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

''' I do realize that saving both DB and auth env variables in the same file
and loading it in 2 different places is not a good practice, but I didn't
want to go overboard for a technical challenge'''

load_dotenv()
db = SQLAlchemy()

database_path = "postgresql://{}:{}@{}/{}".format(os.getenv('DB_USER'),
                                                  os.getenv('DB_PASSWORD'),
                                                  os.getenv('DB_CONN'),
                                                  os.getenv('DB_NAME'))


def setup_db(app, database_path=database_path):
    '''Sets up configuration and creates DB tables'''
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


class User(db.Model):
    '''DB model for the User entity'''
    __tablename__ = 'users'
    email = Column(String, primary_key=True)
    pets = db.relationship('Pet', backref='owner')
    bids = db.relationship('Bid', backref='user')


class Pet(db.Model):
    '''DB model for the Pet entity'''
    __tablename__ = 'pets'
    id = Column(Integer, primary_key=True)
    uemail = Column(String, ForeignKey(User.email))
    bids = db.relationship('Bid', backref='pet')


class Bid(db.Model):
    '''DB model for the Bid entity'''
    __tablename__ = 'bids'
    id = Column(Integer, primary_key=True)
    uemail = Column(String, ForeignKey(User.email))
    pid = Column(Integer, ForeignKey(Pet.id))
    amount = Column(Integer, nullable=False)

    def format(self):
        return {
            'id': self.id,
            'user': self.uemail,
            'pet_id': self.pid,
            'amount': self.amount
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()
