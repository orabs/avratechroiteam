from flask import Flask
from flask_sqlalchemy import SQLAlchemy

import datetime
from datetime import date


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/User/PycharmProjects/FinalProject/gabay'
db = SQLAlchemy(app)


class Worshipers(db.Model):
    __tablename__ = 'worshipers'
    id = db.Column('id', db.Integer, primary_key=True)
    firstname = db.Column('firstname', db.String)
    lastname = db.Column('lastname', db.String)
    phone = db.Column('phone', db.String)
    city = db.Column('city', db.String)
    addres = db.Column('addres', db.String)
    mail = db.Column('mail', db.String)
    clan = db.Column('clan', db.String)
    father_name = db.Column('father_name', db.String)
    LastAliya = db.Column('LastAliya', db.Date)

    def __init__(self, id, firstname=None, lastname=None, phone=None, city=None, addres=None, mail=None, clan=None, father_name=None, lastaliya=None):

        self.id2 = id
        self.firstname = firstname
        self.lastname = lastname
        self.phone = phone
        self.city = city
        self.addres = addres
        self.mail = mail
        self.clan = clan
        self.father_name = father_name
        self.lastaliya = lastaliya