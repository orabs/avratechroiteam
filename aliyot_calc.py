import datetime
import jewish
import sqlite3
from datetime import timedelta
import random
from xml.etree import ElementTree

class Worshiper():
    def __init__(self, id, firstname, lastname, phone, city, addres, mail, clan, father_name,
                 lastaliya):
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

    # @staticmethod
    # def select_next_readers(
    #         days=30):  # get days and give list of tuple of worshipers ('defult =30 days)
    #     database = sqlite3.connect('gabay')
    #     data = database.execute("Select * from worshipers")
    #     reslst = []
    #     datalst = data.fetchall()
    #     todaydate = datetime.today()
    #     for worshiper in datalst:
    #         lastaliya = worshiper[-1]
    #
    #         lastaliya = datetime.strptime(str(lastaliya), "%d/%m/%Y")
    #         passedtime = ((todaydate - lastaliya))
    #         if int(passedtime.days) > days and worshiper:
    #             reslst.append(worshiper)
    #
    #     return reslst

    @staticmethod
    def add_worshiper_lst(lst):
        database = sqlite3.connect('gabay')

        for worshiper in lst:
            firstname = worshiper[1]
            lastname = worshiper[2]
            phone = worshiper[3]
            city = worshiper[4]
            addres = worshiper[5]
            mail = worshiper[6]
            clan = worshiper[7]
            father_name = worshiper[8]
            lastaliya = worshiper[9]

            database.execute("INSERT INTO worshipers (firstname,lastname,phone,city,addres,mail,clan,father_name,LastAliya)\
             VALUES (\"{}\",\"{}\",\"{}\",\"{}\",\"{}\",\"{}\",\"{}\",\"{}\",\"{}\");".format(
                firstname, lastname, phone, city, addres, mail, clan, father_name, lastaliya))

            database.cursor()
            database.commit()

    @staticmethod
    def delete_worshiper_by_id(id):
        database = sqlite3.connect('gabay')
        database.execute("DELETE FROM worshipers WHERE id=\"{}\"".format(id))
        database.cursor()
        database.commit()

    @staticmethod
    def update_worshiper(old_id=None, new_id=None, id=None, firstname=None, lastname=None,
                         phone=None, city=None, addres=None, mail=None, clan=None,
                         father_name=None, lastaliya=None):
        database = sqlite3.connect('gabay')
        if old_id:
            new_id_exist = database.execute("select id from worshipers where id={}".format(new_id))
            new_id_exist = new_id_exist.fetchone()
            if not new_id_exist:
                old_id_exist = database.execute("select id from worshipers where id={}".format(id))
                old_id_exist = old_id_exist.fetchone()
                if old_id_exist:
                    database.execute(
                        "UPDATE worshipers SET id = {} WHERE id ={};".format(new_id, id))
                else:
                    raise ValueError("Id not exist in the database")

            else:
                raise ValueError("Id allreadey exist in the database")
        if firstname:
            database.execute(
                "UPDATE worshipers SET firstname = \"{firstname}\"  Where id={id};".format(
                    firstname=firstname, id=id))
        if lastname:
            database.execute(
                "UPDATE worshipers SET lastname = {} WHERE  id={};".format(lastname, id))
        if phone:
            database.execute("UPDATE worshipers SET phone = {} WHERE id={};".format(phone, id))
        if city:
            database.execute("UPDATE worshipers SET city = {} WHERE  id={};".format(city, id))
        if addres:
            database.execute("UPDATE worshipers SET addres= {} WHERE  id={};".format(addres, id))
        if mail:
            database.execute(
                "UPDATE worshipers SET mail = \"{mail}\" WHERE  id={id};".format(mail=mail, id=id))
        if clan:
            database.execute("UPDATE worshipers SET clan = {} WHERE  id={};".format(clan, id))
        if father_name:
            database.execute(
                "UPDATE worshipers SET father_name = {} WHERE  id={};".format(father_name, id))
        if lastaliya:
            database.execute(
                "UPDATE worshipers SET LastAliya= {} WHERE  id ={};".format(lastaliya, id))
        database.cursor()
        database.commit()

    @staticmethod
    def add_worshiper(new_firstname=None, new_lastname=None, new_phone=None, new_city=None,
                      new_addres=None, new_mail=None, new_clan=None, new_father_name=None,
                      new_lastaliya=None):
        database = sqlite3.connect('gabay')
        database.execute("INSERT INTO worshipers (firstname,lastname,phone,city,addres,mail,clan,father_name,LastAliya)\
                VALUES (\"{}\",\"{}\",\"{}\",\"{}\",\"{}\",\"{}\",\"{}\",\"{}\",\"{}\");".format(
            new_firstname, \
            new_lastname, new_phone, new_city, new_addres, new_mail, new_clan, new_father_name,
            new_lastaliya))
        database.cursor()
        database.commit()

    # @staticmethod
    # def yortzit():
    #     database = sqlite3.connect('gabay')
    #     data = database.execute('select date,id_mtpalel FROM yort ')
    #     return data

    @staticmethod
    def how_clan(id):
        database = sqlite3.connect('gabay')
        clan = database.execute('select clan FROM worshipers WHERE  id={}'.format(id)).fetchall()
        a = clan[0][0] if clan else None
        return a

    @staticmethod
    def select_next_readers_clan(count,
                                 shevet,
                                 id):  # get days and give list of tuple of worshipers ('defult =30 days)
        id = tuple(id)
        database = sqlite3.connect('gabay')
        data = database.execute(
            "select LastAliya,id from worshipers where clan = \"{}\" and id not in {} ".format(
                shevet, id))
        reslst = []
        id_reslst = []
        for worshiper in data:
            reslst.append([int(worshiper[0].split('-')[0]), int(worshiper[0].split('-')[1]),
                           int(worshiper[0].split('-')[2]), worshiper[1]])
        reslst.sort()
        for i in reslst:
            if count != 0:
                id_reslst.append(i[3])
                count -= 1
        return id_reslst if id_reslst else None

    @staticmethod
    def select_id_LastAliya(LastAliya):
        lst = []
        databace = sqlite3.connect('gabay')
        data = databace.execute(
            "select id from worshipers where LastAliya = '{}'".format(LastAliya))
        for i in data:
            lst.append(i[0])
        return lst

@app.route('/aliyoot_clac', methods=['POST', 'GET'])
def alioot(y, m, d):
    date = datetime.date(y, m, d)
    q = {1: 'Cohen', 2: 'levi', 3: 'shlishi', 4: 'rviai', 5: 'chamishi', 6: 'shishi', 7: 'shviai',
         8: 'maftir'}
    clan = {1: 'Cohen', 2: 'Levi', 3: 'Israel', 4: 'Israel', 5: 'Israel', 6: 'Israel', 7: 'Israel',
            8: ['Cohen', 'Levi', 'Israel']}
    numb_of_aliot = moadim_date(date)
    list_olim = []
    id_olim = ['0', '0']
    if numb_of_aliot:
        for i in range(int(numb_of_aliot.split(':')[1][1])):
            list_olim.append(i + 1)
        list_random = list_olim[:]
    else:
        return 'ther is no olim'
    if len(list_random) > 4:
        clan[len(list_random)] = clan[8]
        q[len(list_random)] = q[8]
    # eroua = input(numb_of_aliot + ', you wont choos alia?')
    # while eroua != 'no':
    #     type_aliah = input('איזה עליה אתה רוצה להעלות')
    #     if type_aliah.isalpha() or int(type_aliah) not in list_olim:
    #         eroua = input('אין עליה כזו, אתה עדיין רוצה לבחור עליה?')
    #         continue
    #
    #
    #     name = input('enter id_mtpallel')
    #     clan_string = clan.pop(int(type_aliah))
    #     clan[int(type_aliah)] = clan_string
    #     if Worshiper.how_clan(int(name)) is None or Worshiper.how_clan(
    #             int(name)) not in clan_string:
    #         eroua = input('השם הנבחר או העליה אינם נכונים. רוצה בחירה אחרת?')
    #         continue
    #     list_olim.insert(int(type_aliah) - 1, (int(name), q[int(type_aliah)]))
    #     list_olim.remove(int(type_aliah))
    #     list_random.remove(int(type_aliah))
    #     id_olim.append(int(name))
    #     eroua = input('you have another event?')
    # if len(list_random) == 0:
    #     return list_olim, date
    if 1 in list_olim:
        id = Worshiper.select_next_readers_clan(1, 'Cohen', id_olim)
        if id:
            list_olim.insert(0, (id[0], 'Cohen'))  # aliat cohanim
            id_olim.append(id[0])
        else:
            list_olim.insert(0, ('ther no Cohen',))
        list_olim.remove(1)
        list_random.remove(1)
    if 2 in list_olim:
        id = Worshiper.select_next_readers_clan(1, 'Levi', id_olim)
        if id:
            list_olim.insert(1, (id[0], 'levi'))  # aliat lavi
            id_olim.append(id[0])
        else:
            list_olim.insert(1, ('ther no Levi',))
        list_olim.remove(2)
        list_random.remove(2)
    if len(list_random) == 0:
        return list_olim, date
    shvooa = 8 if (int(numb_of_aliot.split(':')[1][1])) == 8 else 1
    for i in range(shvooa):  # yortzit function
        a = yortzayd(date + timedelta(days=i), id_olim)
        if a:
            if len(list_olim) in list_olim:
                b = len(list_olim)
                list_olim.insert(b - 1, (int(a[0]), q[8]))
                list_olim.remove(b)
                list_random.remove(b)
            else:
                if Worshiper.how_clan(a[0]) == 'Israel':
                    b = random.choice(list_random)
                    list_olim.insert(b - 1, (int(a[0]), q[b]))
                    list_olim.remove(b)
                    list_random.remove(b)
                list_olim.append('למתפלל {} יש יארצייט'.format(int(a[0])))
    if len(list_random) == 0:
        return list_olim, date
    israelim = Worshiper.select_next_readers_clan(len(list_random), 'Israel',
                                                  id_olim)  # aliot israelim
    for i in israelim:
        b = random.choice(list_random)
        list_olim.remove(b)
        list_random.remove(b)
        list_olim.insert(b - 1, (i, q[b]))
    return list_olim, date


def yortzayd(date, id1):
    id1 = tuple(id1)
    list_id = []
    nm = sqlite3.connect('gabay')
    niftar = nm.execute(
        'SELECT  worshiper,date FROM yorzait where worshiper not in {}'.format(id1))

    for i in niftar:
        id = i[0]
        a = i[1].split('/')
        b = int(a[0]), int(a[1]), int(a[2])
        j = jewish.JewishDate.from_date(datetime.date(b[0], b[1], b[2]))
        yortzayd_date = j.day, j.month
        f = jewish.JewishDate.from_date(date)
        gabay_date = f.day, f.month
        if gabay_date == yortzayd_date:
            list_id.append(id)
    return list_id if list_id else None


def moadim_date(date):
    chagim = jewish.JewishDate.from_date(date)
    weekday = date
    fine_shabat = weekday.isoweekday()
    day = str(chagim)
    yom = ''

    if fine_shabat == 6:
        yom += "SHBAT: 8 olim latora"

    if day[0] is "1" and day[1] == ' ' and '1 Tishrei' not in day:
        yom += "rosh chodesh: 4 olim latora"
    else:
        if '1 Tishrei' in day and day[1] == ' ':
            yom += "rosh hashana: 6 olim latora"
            return yom
        if '2 Tishrei' in day and day[1] == ' ':
            yom += "rosh hashana: 6 olim latora"
            return yom
        if '10 Tishrei' in day:
            yom += 'yom kipur: 7 olim latora'
            return yom
        if '15 Tishrei' in day:
            yom += 'sucot: 6 olim latora'
            return yom
        if '22 Tishrei' in day:
            yom += 'simchat tora: kulam olim latora'
            return yom
        if '15 Nisan' in day:
            yom += 'pesach: 6 olim latora'
            return yom
        if '14 Adar' in day:
            yom += 'purim: 3 olim latora'
            return yom
        if '22 Nisan' in day:
            yom += 'shviy shel pesach: 6 olim latora'
            return yom
        if '6 Sivan' in day:
            yom += 'shavuot: 6 olim latora'
            return yom
        else:
            if fine_shabat == 1:
                yom += 'yom sheni: 3 olim latora'
                return yom
            if fine_shabat == 4:
                yom += 'yom chamishi: 3 olim latora'
                return yom
        return yom


print(alioot(2017,2,4))