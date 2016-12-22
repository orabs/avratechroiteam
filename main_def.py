import datetime
import sqlite3
from datetime import datetime


class Worshiper():
    def __init__(self, id, firstname, lastname, phone, city, addres, mail, clan, father_name, lastaliya):
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

    @staticmethod
    def select_next_readers(days=30):  # get days and give list of tuple of worshipers ('defult =30 days)
        database = sqlite3.connect('gabay')
        data = database.execute("Select * from worshipers")
        reslst = []
        datalst = data.fetchall()
        todaydate = datetime.today()
        for worshiper in datalst:
            lastaliya = worshiper[-1]

            lastaliya = datetime.strptime(str(lastaliya), "%d/%m/%Y")
            passedtime = ((todaydate - lastaliya))
            if int(passedtime.days) > days and worshiper:
                reslst.append(worshiper)

        return reslst

    @staticmethod
    def select_next_readers_clan(worshiper=5,shevet="Israel"):  # get days and give list of tuple of worshipers ('defult =30 days)
        database = sqlite3.connect('gabay')
        data = database.execute("select * from worshipers where clan=\"{}\" order by LastAliya DESC limit {}".format(shevet, worshiper))
        datalst = data.fetchall()

        return datalst

    @staticmethod
    def add_worshiper_lst(lst):
        database = sqlite3.connect('gabay')

        firstname = lst[1]
        lastname = lst[2]
        phone = lst[3]
        city = lst[4]
        addres = lst[5]
        mail = lst[6]
        clan = lst[7]
        father_name = lst[8]
        lastaliya = lst[9]

        database.execute("INSERT INTO worshipers (firstname,lastname,phone,city,addres,mail,clan,father_name,LastAliya)\
             VALUES (\"{}\",\"{}\",\"{}\",\"{}\",\"{}\",\"{}\",\"{}\",\"{}\",\"{}\");".format(firstname, lastname,
                                                                                              phone, city, addres, mail,
                                                                                              clan, father_name,
                                                                                              lastaliya))

        database.cursor()
        database.commit()

    @staticmethod
    def delete_worshiper_by_id(id):
        database = sqlite3.connect('gabay')
        database.execute("DELETE FROM worshipers WHERE id=\"{}\"".format(id))
        database.cursor()
        database.commit()

    @staticmethod
    def update_worshiper(old_id=None, new_id=None, id=None, firstname=None, lastname=None, phone=None, city=None,
                         addres=None, mail=None, clan=None, father_name=None, lastaliya=None):
        database = sqlite3.connect('gabay')
        if old_id:
            new_id_exist = database.execute("select id from worshipers where id={}".format(new_id))
            new_id_exist = new_id_exist.fetchone()
            if not new_id_exist:
                old_id_exist = database.execute("select id from worshipers where id={}".format(id))
                old_id_exist = old_id_exist.fetchone()
                if old_id_exist:
                    database.execute("UPDATE worshipers SET id = {} WHERE id ={};".format(new_id, id))
                else:
                    raise ValueError("Id not exist in the database")

            else:
                raise ValueError("Id allreadey exist in the database")
        id_exist = database.execute("select id from worshipers where id={}".format(id))
        id_exist = id_exist.fetchone()


        if id_exist[0]:

            if firstname:
                database.execute(
                    "UPDATE worshipers SET firstname = \"{firstname}\"  Where id={id};".format(firstname=firstname,
                                                                                               id=id))
            if lastname:
                database.execute("UPDATE worshipers SET lastname = '{lastname}' WHERE  id=id{};".format(lastname=lastname,id= id))
            if phone:
                database.execute("UPDATE worshipers SET phone = '{phone}' WHERE id={id};".format(phone=phone, id=id))
            if city:
                database.execute("UPDATE worshipers SET city = '{city}' WHERE  id={id};".format(city=city, id=id))
            if addres:
                database.execute("UPDATE worshipers SET addres= '{addres}' WHERE  id={id};".format(addres=addres,id= id))
            if mail:
                database.execute("UPDATE worshipers SET mail = '{mail}' WHERE  id={id};".format(mail=mail, id=id))
            if clan:
                database.execute("UPDATE worshipers SET clan = '{clan}' WHERE  id={id};".format(clan=clan,id= id))
            if father_name:
                database.execute("UPDATE worshipers SET father_name = '{father_name}' WHERE  id={id};".format(father_name=father_name,id= id))
            if lastaliya:
                database.execute("UPDATE worshipers SET LastAliya= '{lastaliya}' WHERE  id ={id};".format(lastaliya=lastaliya,id=id))
        else:
            raise ValueError("Id not exist in the database")

        database.cursor()
        database.commit()
# lets see if it works
    @staticmethod
    def add_worshiper(new_firstname=None, new_lastname=None, new_phone=None, new_city=None, new_addres=None,
                      new_mail=None, new_clan=None, new_father_name=None, new_lastaliya=None):
        database = sqlite3.connect('gabay')
        database.execute("INSERT INTO worshipers (firstname,lastname,phone,city,addres,mail,clan,father_name,LastAliya)\
                VALUES ('{}','{}','{}','{}','{}','{}','{}','{}','{}');".format(new_firstname, \
                                                                                                 new_lastname,
                                                                                                 new_phone, new_city,
                                                                                                 new_addres, new_mail,
                                                                                                 new_clan,
                                                                                                 new_father_name,
                                                                                                 new_lastaliya))
        database.cursor()
        database.commit()


# hello world
# update_worshiper(old_id=1000,new_id=999)
# Worshiper.add_worshiper(new_addres="blabla")
#
# Worshiper.add_worshiper(new_firstname="orly",new_lastname="arbes",new_city="jeruslam")
# database = sqlite3.connect('gabay')
# data=database.execute("SELECT name FROM sqlite_master WHERE type='table';")
# qu1=data.fetchall()
# qu1.pop(0)
# print(qu1[0][0])
#aineoanhetaet

#
# cursor = database.execute('select * from worshipers')
# data=cursor.fetchall()
#
# tup=tuple()
# cols = list(map(lambda x: x[0], cursor.description))
# tup=tuple(cols)
# print(tup)
#
# data.insert(0,tup)
# print(data)
#
#

# Worshiper.update_worshiper(id=608044,lastaliya="17/10/2016")
