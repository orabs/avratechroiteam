from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy
import datetime
from datetime import date


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/User/PycharmProjects/FinalProject/gabay'
db = SQLAlchemy(app)


class Worshipers(db.Model):
    __tablename__ = 'worshipers'
    id = db.Column('id', db.Integer, primary_key=True,autoincrement=True)
    firstname = db.Column('firstname', db.String)
    lastname = db.Column('lastname', db.String)
    phone = db.Column('phone', db.String)
    city = db.Column('city', db.String)
    addres = db.Column('addres', db.String)
    mail = db.Column('mail', db.String)
    clan = db.Column('clan', db.String)
    father_name = db.Column('father_name', db.String)
    lastaliya= db.Column('LastAliya', db.Date)

    def __init__(self,  firstname=None, lastname=None, phone=None, city=None, addres=None, mail=None, clan=None, father_name=None, lastaliya=None):

        self.firstname = firstname
        self.lastname = lastname
        self.phone = phone
        self.city = city
        self.addres = addres
        self.mail = mail
        self.clan = clan
        self.father_name = father_name
        self.lastaliya = lastaliya


class Aliyot(db.Model):
    __tablename__ = 'Aliyot'
    id = db.Column('id', db.Integer, primary_key=True,autoincrement=True)
    parasha = db.Column('parasha', db.Text)
    date = db.Column('date', db.Date)
    comment = db.Column('comment', db.String)
    aliya = db.Column('aliya', db.String)
    worshiper = db.Column('worshiper', db.String)
    day = db.Column('day', db.String)
    reason = db.Column('reason', db.String)

    def __init__(self, parasha=None, date=None, comment=None, aliya=None, worshiper=None, day=None, reason=None):


        self.parasha = parasha
        self.date = date
        self.comment = comment
        self.aliya = aliya
        self.worshiper = worshiper
        self.day = day
        self.reason = reason

class Events(db.Model):
    __tablename__ = 'events'
    id = db.Column('id', db.Integer, primary_key=True,autoincrement=True)
    eventname = db.Column('eventname', db.String)
    worshiper = db.Column('worshiper', db.String)
    comment = db.Column('comment', db.String)
    day = db.Column('day', db.String)
    date = db.Column('date', db.Date)
    moed = db.Column('Moed', db.String)

    def __init__(self,  eventname=None, worshiper=None, comment=None, day=None, date=None, moed=None):

        self.eventname = eventname
        self.worshiper = worshiper
        self.comment = comment
        self.day = day
        self.date = date
        self.moed = moed


class Donations(db.Model):
    __tablename__ = 'donations'
    id = db.Column('id', db.Integer, primary_key=True,autoincrement=True)
    worshiper = db.Column('donationdate', db.String)
    donationdate = db.Column('lastname', db.String)
    payed = db.Column('payed', db.String)

    def __init__(self,  worshiper=None, donationdate=None, payed=None):

        self.worshiper = worshiper
        self.donationdate = donationdate
        self.payed = payed


class Yorzait(db.Model):
    __tablename__ = 'yorzait'
    id = db.Column('id', db.Integer, primary_key=True,autoincrement=True)
    worshiper = db.Column('worshiper', db.String)
    niftar = db.Column('niftar', db.String)
    date = db.Column('date', db.Date)
    kinship = db.Column('kinship', db.String)

    def __init__(self, id=None, worshiper=None, niftar=None, date=None, kinship=None):
        self.id = id
        self.worshiper = worshiper
        self.niftar = niftar
        self.date = date
        self.kinship = kinship

class Users(db.Model):

     __tablename__ = 'users'
     id = db.Column('id', db.Integer, primary_key=True,autoincrement=True)
     username = db.Column('username', db.String)
     password = db.Column('password', db.String)
     lvl = db.Column('lvl', db.String)


     def __init__(self, id=None, username=None, password=None, lvl=None):
        self.id = id
        self.username = username
        self.password = password
        self.lvl = lvl
#group table
class Group(db.Model):
    __tablename__ = 'group'
    id = db.Column('id', db.Integer, primary_key=True,autoincrement=True)
    worshiper = db.Column('worshiper', db.String)
    head = db.Column('head', db.String)
    connection = db.Column('connetion', db.String)

    def __init__(self, id=None, worshiper=None, head=None,connection=None):
        self.id = id
        self.worshiper = worshiper
        self.head = head
        self. connection = connection

class Moed(db.Model):

     __tablename__ = 'moed'
     name = db.Column('name', db.String, primary_key=True)

     def __init__(self, name=None):
         self.name = name


#kindofevents table
class KindOfEvent(db.Model):

    __tablename__ = 'kindofevent'
    name = db.Column('name', db.String, primary_key=True)

    def __init__(self, name=None):
        self.name = name

#days table
class Days(db.Model):
    __tablename__ = 'days'
    name = db.Column('name', db.String, primary_key=True)

    def __init__(self, name=None):
        self.name = name
#aa
class Reasons(db.Model):
     __tablename__ = 'Reasons'
     name = db.Column('name', db.String, primary_key=True)
     rank= db.Column('rank', db.String)

     def __init__(self, name=None,rank=None):
         self.name = name
         self.rank = rank
#.
class Parasha(db.Model):

     __tablename__ = 'Parasha'
     name = db.Column('name', db.String, primary_key=True)

     def __init__(self, name=None):
         self.name = name
#s
class KindOfAliya(db.Model):
     __tablename__ = 'kindofaliya'
     name = db.Column('name', db.String, primary_key=True)

     def __init__(self, name=None):
         self.name = name




# #
# new1=Worshipers()
# new1.firstname = 'ori'
# new1.lastname="moshe"
# db.session.query(Worshipers).filter(Worshipers.id == 227).\
# update({Worshipers.firstname: "Yohssi"})
# db.session.commit()
# dates=datetime.date(day=5,month=10,year=1988)
#
# new1.lastaliya=dates
#
#
# db.session.add(new1)
# db.session.commit()
# for u in db.session.query(Users.id).all():
#     print( u[0])
# for i in temp:
#     print(i)
# data=Users.query.filter_by(id=1).first()
# print(type(data.username))
# for i in temp:
#
#     print(temp)
# l=[x for x in((db.session.query(Worshipers.id)).get())]
# print(l)
# blabla=Worshipers(firstname="izik",lastname="gaga")
# db.session.add(blabla)
# # db.session.commit()
# a=Users.query.filter_by(lvl="admin").first()
# print(a.username)
# data=db.session.query(Events)
#
#
# for i in data:
#     print(i)
