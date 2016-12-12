
import datetime
import jewish
import sqlite3
from datetime import datetime


class Worshiper():
    # def __init__(self,id,firstname,lastname,phone,city,addres,mail,clan,father_name,lastaliya):
    #     self.id=id
    #     self.firstname=firstname
    #     self.lastname=lastname
    #     self.phone=phone
    #     self.city=city
    #     self.addres=addres
    #     self.mail=mail
    #     self.clan=clan
    #     self.father_name=father_name
    #     self.lastaliya=lastaliya





    @staticmethod
    def select_next_readers(days=30):                 #get days and give list of tuple of worshipers ('defult =30 days)
        database = sqlite3.connect('gabay')
        data = database.execute("Select * from worshipers")
        reslst=[]
        datalst=data.fetchall()
        todaydate=datetime.today()
        for worshiper in datalst:
             lastaliya=worshiper[-1]

             lastaliya=datetime.strptime(str(lastaliya),"%d/%m/%Y")
             passedtime=((todaydate-lastaliya))
             if int(passedtime.days)>days and worshiper:
                 reslst.append(worshiper)

        return reslst

    @staticmethod
    def select_next_readers_clan(worshiper=5,shevet="Israel"):                 #get days and give list of tuple of worshipers ('defult =30 days)
        database = sqlite3.connect('gabay')
        data = database.execute(
            "select * from worshipers where clan=\"{}\" order by LastAliya DESC limit {}".format(shevet, worshiper))
        reslst=[]

        datalst=data.fetchall()

        for worshiper in datalst:
            reslst.append(worshiper)


        return reslst

    @staticmethod
    def add_worshiper_lst(lst):
        database = sqlite3.connect('gabay')

        for worshiper in lst:

            firstname =worshiper[1]
            lastname = worshiper[2]
            phone = worshiper[3]
            city = worshiper[4]
            addres = worshiper[5]
            mail = worshiper[6]
            clan = worshiper[7]
            father_name = worshiper[8]
            lastaliya = worshiper[9]

            database.execute("INSERT INTO worshipers (firstname,lastname,phone,city,addres,mail,clan,father_name,LastAliya)\
             VALUES (\"{}\",\"{}\",\"{}\",\"{}\",\"{}\",\"{}\",\"{}\",\"{}\",\"{}\");".format(firstname,lastname,phone,city,addres,mail,clan,father_name,lastaliya))

            database.cursor()
            database.commit()

    @staticmethod
    def delete_worshiper_by_id(id):
        database = sqlite3.connect('gabay')
        database.execute("DELETE FROM worshipers WHERE id=\"{}\"".format(id))
        database.cursor()
        database.commit()

    @staticmethod
    def update_worshiper(new_id=None,old_id=None,old_firstname=None,new_firstname=None,old_lastname=None,new_lastname=None,new_phone=None,old_phone=None,new_city=None,old_city=None,new_addres=None,old_addres=None,new_mail=None,old_mail=None,new_clan=None,old_clan=None,new_father_name=None,old_father_name=None,new_lastaliya=None,old_lastliya=None):
        database = sqlite3.connect('gabay')
        if old_id:
            new_id_exist=database.execute("select id from worshipers where id={}".format(new_id))
            new_id_exist=new_id_exist.fetchone()
            if not new_id_exist:
                old_id_exist = database.execute("select id from worshipers where id={}".format(old_id))
                old_id_exist = old_id_exist.fetchone()
                if old_id_exist:
                    database.execute("UPDATE worshipers SET id = {} WHERE id ={};".format(new_id,old_id))
                else:
                    raise ValueError("Id not exist in the database")

            else:
                raise ValueError("Id allreadey exist in the database")
        if old_firstname:
            database.execute("UPDATE worshipers SET firstname = {} WHERE firstname ={};".format(new_firstname,old_firstname))
        if old_lastname:
            database.execute("UPDATE worshipers SET id = {} WHERE id ={};".format(new_lastname,old_lastname))
        if old_phone:
            database.execute("UPDATE worshipers SET id = {} WHERE id ={};".format(new_phone,old_phone))
        if old_city:
            database.execute("UPDATE worshipers SET id = {} WHERE id ={};".format(new_city,old_city))
        if old_addres:
            database.execute("UPDATE worshipers SET id = {} WHERE id ={};".format(new_addres,old_addres))
        if old_mail:
            database.execute("UPDATE worshipers SET id = {} WHERE id ={};".format(new_mail,old_mail))
        if old_clan:
            database.execute("UPDATE worshipers SET id = {} WHERE id ={};".format(new_clan,old_clan))
        if old_father_name:
            database.execute("UPDATE worshipers SET id = {} WHERE id ={};".format(new_father_name,old_father_name))
        if old_lastliya:
            database.execute("UPDATE worshipers SET id = {} WHERE id ={};".format(new_lastaliya,old_lastliya))

    @staticmethod
    def add_worshiper(new_firstname=None,new_lastname=None,new_phone=None,new_city=None,new_addres=None,new_mail=None,new_clan=None,new_father_name=None,new_lastaliya=None):
        database = sqlite3.connect('gabay')
        database.execute("INSERT INTO worshipers (firstname,lastname,phone,city,addres,mail,clan,father_name,LastAliya)\
                VALUES (\"{}\",\"{}\",\"{}\",\"{}\",\"{}\",\"{}\",\"{}\",\"{}\",\"{}\");".format(new_firstname,\
                            new_lastname,new_phone,new_city, new_addres, new_mail, new_clan,new_father_name, new_lastaliya))
        database.cursor()
        database.commit()
#hello world
# update_worshiper(old_id=1000,new_id=999)
# Worshiper.add_worshiper(new_addres="blabla")
#
# Worshiper.add_worshiper(new_firstname="orly",new_lastname="arbes",new_city="jeruslam")

Worshiper.delete_worshiper_by_id(1002)