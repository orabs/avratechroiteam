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

        self.id = id
        self.firstname = firstname
        self.lastname = lastname
        self.phone = phone
        self.city = city
        self.addres = addres
        self.mail = mail
        self.clan = clan
        self.father_name = father_name
        self.lastaliya = lastaliya

#
# class Aliyot(db.Model):
#     __tablename__ = 'Aliyot'
#     id = db.Column('id', db.Integer, primary_key=True)
#     parasha = db.Column('parasha', db.Text)
#     date = db.Column('date', db.Date)
#     comment = db.Column('comment', db.String)
#     aliya = db.Column('aliya', db.String)
#     worshiper = db.Column('worshiper', db.String)
#     day = db.Column('day', db.String)
#     reason = db.Column('reason', db.String)
#
#     def __init__(self, id, parasha=None, date=None, comment=None, aliya=None, worshiper=None, day=None, reason=None):
#
#         self.id = id
#         self.parasha = parasha
#         self.date = date
#         self.comment = comment
#         self.aliya = aliya
#         self.worshiper = worshiper
#         self.day = day
#
#
# class Events(db.Model):
#     __tablename__ = 'events'
#     id = db.Column('id', db.Integer, primary_key=True)
#     eventname = db.Column('eventname', db.String)
#     worshiper = db.Column('worshiper', db.String)
#     comment = db.Column('comment', db.String)
#     day = db.Column('day', db.String)
#     date = db.Column('date', db.Date)
#     moed = db.Column('Moed', db.String)
#
#     def __init__(self, id, eventname=None, worshiper=None, comment=None, day=None, date=None, moed=None):
#
#         self.id = id
#         self.eventname = eventname
#         self.worshiper = worshiper
#         self.comment = comment
#         self.day = day
#         self.date = date
#         self.moed = moed
#
#
# class Donations(db.Model):
#     __tablename__ = 'donations'
#     id = db.Column('id', db.Integer, primary_key=True)
#     worshiper = db.Column('donationdate', db.String)
#     donationdate = db.Column('lastname', db.String)
#     payed = db.Column('payed', db.String)
#
#     def __init__(self, id, worshiper=None, donationdate=None, payed=None):
#         self.id = id
#         self.worshiper = worshiper
#         self.donationdate = donationdate
#         self.payed = payed
#
#
# class Yorziet(db.Model):
#     __tablename__ = 'yorziet'
#     id = db.Column('id', db.Integer, primary_key=True)
#     worshiper = db.Column('worshiper', db.String)
#     niftar = db.Column('niftar', db.String)
#     date = db.Column('date', db.Date)
#     kinship = db.Column('kinship', db.String)
#
#     def __init__(self, id, worshiper=None, niftar=None, date=None, kinship=None):
#         self.id = id
#         self.worshiper = worshiper
#         self.niftar = niftar
#         self.date = date
#         self.kinship = kinship


new1 = Worshipers(608020)
new1.firstname = 'ori'
new1.lastname="moshe"

dates=datetime.date(day=5,month=10,year=1988)

new1.lastaliya=dates
print(new1.lastaliya)

db.session.add(new1)
db.session.commit()
