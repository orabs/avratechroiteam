import sqlite3
from flask import Flask, redirect, url_for, request, render_template, make_response
from flask_sqlalchemy import SQLAlchemy
import sql_alchemy_gabay as al
import main_def
import jewish
from datetime import datetime

def eng_date_to_heb(date):
    holydaydict = {jewish.JewishDate(1, 1, 1): "ראש השנה יום ראשון", jewish.JewishDate(1, 1, 2): "ראש השנה יום שני",
                   jewish.JewishDate(1, 1, 15): "חג סוכות", jewish.JewishDate(1, 1, 16): "חול המועד סוכות",
                   jewish.JewishDate(1, 1, 17): "חול המועד סוכות", jewish.JewishDate(1, 1, 18): "ראש השנה"}

    month_con = {1: "תשרי", 2: "חשון", 3: "כסלו", 4: "טבת", 5: "שבת", 6: "אדר א'", 7: "אדר ב'", 8: "ניסן",
                 9: "אייר", 10: "סיוון", 11: "תמוז", 12: "אב", 13: "אלול"}
    day_con = {1: "א'", 2: "ב'", 3: "ג'", 4: "ד'", 5: "ה'", 6: "ו'", 7: "ז'", 8: "ח'",
               9: "ט'", 10: "י'", 11: "יא'", 12: "יב'", 13: "יג'", 14: "יד'", 15: "טו'", 16: "טז'", 17: "יז'",
               18: "יח'", 19: "יט'", 20: "כ'", 21: "כא'", 22: "כב'", 23: "כג'", 24: "כד'", 25: "כה'", 26: "כו'",
               27: "כז'", 28: "כח'", 29: "כט'", 30: "ל'"}
    month_con = {1: "תשרי", 2: "חשון", 3: "כסלו", 4: "טבת", 5: "שבת", 6: "אדר א'", 7: "אדר ב'", 8: "ניסן",
                 9: "אייר", 10: "סיוון", 11: "תמוז", 12: "אב", 13: "אלול"}
    year_con = {5771: "התשעא'", 5772: "התשעב'", 5773: "התשעג'", 5774: "התשעד'",5776: "התשעו'", 5775:  "התשעה'" ,5777: "התשעז'", 5778: "התשעח'", 5779: "התשעט'", 5780: "התשפ'", 5781: "התשפא'", 5782: "התשפב'",
                7: "התשפג'", 5783: "התשפד'"}
    return "{} , {} ,  {}".format(day_con[date.day], month_con[date.month], year_con[date.year])

app = Flask(__name__)
app.config['SECRET_KEY'] = 'DontTellAnyone'


@app.route('/', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        result = request.form
        resdict = dict(result)
        database = sqlite3.connect('gabay')
        data = (database.execute("select * from users")).fetchall()
        # print(data)
        # print(resdict["username"][0])
        # print(resdict["password"][0])
        for item in data:
            tempuser = item[1]
            temppass = item[2]
            # print(tempuser,temppass)
            if str(resdict["username"][0]) == str(tempuser) and str(resdict["password"][0]) == str(temppass):
                login = str(item[1])
                print(login + "this")
                level = (al.Users.query.filter_by(username=str(login)).first()).lvl
                print(level[0])
                level = level[0]
                logincookie = make_response(render_template("indexafterlogin.html", user=str(resdict["username"][0])))
                logincookie.set_cookie('level', str(resdict["username"][0]))
                return logincookie
            if str(resdict["username"][0]) == str(tempuser) and not str(resdict["password"][0]) == str(temppass):
                return "Wrong Password"
        return "No Such Username"
    elif request.method == "GET":

        username = request.cookies.get('level')
        print(username)
        login = al.Users.query.filter_by(username=username).first()

        # print(data[0][0])
        if request.cookies.get('level'):
            return render_template("indexafterlogin.html", user=login.username)
        else:
            return render_template("index.html")


@app.route('/table/<table>')
def view_tables(table):
    username = request.cookies.get('level')
    data = sqlite3.connect('gabay')
    login = data.execute("select lvl from users where username='{}'".format(username)).fetchone()
    print(login)
    if login:
        if login[0] == 'admin':
            database = sqlite3.connect('gabay')
            data = database.execute("select * from {}".format(table))
            cursor = database.execute('select * from {}'.format(table))
            cols = list(map(lambda x: x[0], cursor.description))
            qu1 = data.fetchall()
            cols = tuple(cols)
            cols = [x for x in cols]
            print(cols)
            return render_template("tables.html", qu1=qu1, table=table, cols=cols)
        if login[0] == 'mod':
            return "You not alowed to get this information"
    else:
        return "You not Login"


@app.route('/add_worshiper', methods=['POST', 'GET'])
def add_worshiper():
    if request.method == 'POST':
        result = request.form
        resdict = dict(result)
        print(resdict)
        print(type(resdict["firstname"]))
        strdate = resdict["LastAliya"][0]
        print(strdate)
        print(type(strdate))
        datedate = datetime.date(datetime.strptime(strdate, "%Y-%m-%d"))
        print(datedate)
        print(type(datedate))
        worshiper = al.Worshipers(firstname=str(resdict["firstname"][0]), lastname=str(resdict["lastname"][0]),
                                  phone=str(resdict["phone"][0]), city=str(resdict["city"][0]),
                                  addres=str(resdict["addres"][0]), mail=str(resdict["mail"][0]),
                                  clan=str(resdict["clan"][0]), father_name=str(resdict["father_name"][0]),
                                  lastaliya=datedate)
        print(resdict["LastAliya"][0])
        print(type(resdict["LastAliya"][0]))
        al.db.session.add(worshiper)
        al.db.session.commit()

        return " המתפלל הוסף בהצלחה למערכת!! "

    elif request.method == "GET":

        return render_template("worshipers.html")


@app.route('/add_aliya', methods=['POST', 'GET'])
def add_aliya():
    if request.method == 'POST':
        result = request.form
        resdict = dict(result)
        worshiper=resdict["worshiper"][0].split(",")
        worshiper=worshiper[0]
        comment=((resdict["comment"][0]))
        print(type(comment))
        print(comment)
        date = datetime.date(datetime.strptime((resdict["date"][0]), "%Y-%m-%d"))
        aliya = al.Aliyot(comment=comment,reason=str(resdict["reason"][0]), day=(resdict["day"][0]),
                                  date=date, parasha=str(resdict["parasha"][0]),
                                  worshiper=worshiper,aliya=str(resdict["aliya"][0]))

        al.db.session.add(aliya)
        al.db.session.commit()

        return " העלייה הוספה בהצלחה למערכת!! "

    elif request.method == "GET":
        lstparasha=[]
        lstday=[]
        lstreason=[]
        lstworshiper=[]
        lstaliya=[]
        for parasha in al.db.session.query(al.Parasha.name).all():
            lstparasha.append(parasha[0])
        for day in al.db.session.query(al.Days.name).all():
            lstday.append(day[0])
        for reason in al.db.session.query(al.Reasons.name).all():
            lstreason.append(reason[0])
        for worshiper in al.db.session.query(al.Worshipers.id,al.Worshipers.firstname,al.Worshipers.lastname).all():
            lstworshiper.append("{},{},{}".format(worshiper[0],worshiper[1],worshiper[2]))
        for aliya in al.db.session.query(al.KindOfAliya.name).all():
            lstaliya.append(aliya[0])
        print(lstworshiper)
        login = request.cookies.get('level')
        user = al.Users.query.filter_by(username=login).first().username
        return render_template("add_aliya.html",user=user,lstparasha=lstparasha,lstaliya=lstaliya,lstday=lstday,lstreason=lstreason,lstworshiper=lstworshiper)


@app.route('/add_event', methods=['POST', 'GET'])
def add_event():

    if request.method == 'POST':
        result = request.form
        resdict = dict(result)
        worshiper = resdict["worshiper"][0].split(",")
        worshiper = worshiper[0]
        comment = ((resdict["comment"][0]))
        print(type(comment))
        print(comment)
        date = datetime.date(datetime.strptime((resdict["date"][0]), "%Y-%m-%d"))
        event = al.Events(comment=comment, eventname=str(resdict["eventname"][0]), day=(resdict["day"][0]),
                          date=date, moed=str(resdict["moed"][0]),
                          worshiper=worshiper)

        al.db.session.add(event)
        al.db.session.commit()

        return "  אירוע הוסף בהצלחה למערכת!! "

    elif request.method == "GET":
        lsteventname = []
        lstday = []
        lstmoed = []
        lstworshiper = []

        for event in al.db.session.query(al.KindOfEvent.name).all():
            lsteventname.append(event[0])
        for day in al.db.session.query(al.Days.name).all():
            lstday.append(day[0])
        for moed in al.db.session.query(al.Moed.name).all():
            lstmoed.append(moed[0])
        for worshiper in al.db.session.query(al.Worshipers.id, al.Worshipers.firstname, al.Worshipers.lastname).all():
            lstworshiper.append("{},{},{}".format(worshiper[0], worshiper[1], worshiper[2]))

        print(lstworshiper)
        login = request.cookies.get('level')
        user = al.Users.query.filter_by(username=login).first().username
        return render_template("add_event.html", user=user, lstevent=lsteventname, lstmoed=lstmoed, lstday=lstday, lstworshiper=lstworshiper)


@app.route('/add_donation', methods=['POST', 'GET'])
def add_donation():
    if request.method == 'POST':
        result = request.form
        resdict = dict(result)
        print(resdict)
        print(type(resdict["firstname"]))
        strdate = resdict["LastAliya"][0]
        print(strdate)
        print(type(strdate))
        datedate = datetime.date(datetime.strptime(strdate, "%Y-%m-%d"))
        print(datedate)
        print(type(datedate))
        worshiper = al.Worshipers(firstname=str(resdict["firstname"][0]), lastname=str(resdict["lastname"][0]),
                                  phone=str(resdict["phone"][0]), city=str(resdict["city"][0]),
                                  addres=str(resdict["addres"][0]), mail=str(resdict["mail"][0]),
                                  clan=str(resdict["clan"][0]), father_name=str(resdict["father_name"][0]),
                                  lastaliya=datedate)
        print(resdict["LastAliya"][0])
        print(type(resdict["LastAliya"][0]))
        al.db.session.add(worshiper)
        al.db.session.commit()

        return " המתפלל הוסף בהצלחה למערכת!! "

    elif request.method == "GET":
        return render_template("add_donation.html")


@app.route('/add_yorzait', methods=['POST', 'GET'])
def add_yorzait():
    if request.method == 'POST':
        result = request.form
        resdict = dict(result)
        print(resdict)
        print(type(resdict["firstname"]))
        strdate = resdict["LastAliya"][0]
        print(strdate)
        print(type(strdate))
        datedate = datetime.date(datetime.strptime(strdate, "%Y-%m-%d"))
        print(datedate)
        print(type(datedate))
        worshiper = al.Worshipers(firstname=str(resdict["firstname"][0]), lastname=str(resdict["lastname"][0]),
                                  phone=str(resdict["phone"][0]), city=str(resdict["city"][0]),
                                  addres=str(resdict["addres"][0]), mail=str(resdict["mail"][0]),
                                  clan=str(resdict["clan"][0]), father_name=str(resdict["father_name"][0]),
                                  lastaliya=datedate)
        print(resdict["LastAliya"][0])
        print(type(resdict["LastAliya"][0]))
        al.db.session.add(worshiper)
        al.db.session.commit()

        return " המתפלל הוסף בהצלחה למערכת!! "

    elif request.method == "GET":
        return render_template("add_yorzait.html")


@app.route('/add_niftar', methods=['POST', 'GET'])
def add_niftar():
    if request.method == 'POST':
        result = request.form
        resdict = dict(result)
        print(resdict)
        print(type(resdict["firstname"]))
        strdate = resdict["LastAliya"][0]
        print(strdate)
        print(type(strdate))
        datedate = datetime.date(datetime.strptime(strdate, "%Y-%m-%d"))
        print(datedate)
        print(type(datedate))
        worshiper = al.Worshipers(firstname=str(resdict["firstname"][0]), lastname=str(resdict["lastname"][0]),
                                  phone=str(resdict["phone"][0]), city=str(resdict["city"][0]),
                                  addres=str(resdict["addres"][0]), mail=str(resdict["mail"][0]),
                                  clan=str(resdict["clan"][0]), father_name=str(resdict["father_name"][0]),
                                  lastaliya=datedate)
        print(resdict["LastAliya"][0])
        print(type(resdict["LastAliya"][0]))
        al.db.session.add(worshiper)
        al.db.session.commit()

        return " המתפלל הוסף בהצלחה למערכת!! "

    elif request.method == "GET":
        return render_template("worshipers.html")


@app.route('/update_worshiper', methods=['POST', 'GET'])
def update_worshiper():
    if request.method == 'POST':

        if request.form['submit'] == 'Update':
            # # result = request.form
            # id=request.form["id"]
            # print(request.form["id"])
            firstname = request.form["firstname2"]
            lastname = request.form["lastname2"]
            phone = request.form["phone2"]
            city = request.form["city2"]
            addres = request.form["addres2"]
            mail = request.form["mail2"]
            clan = request.form["clan2"]
            father_name = request.form["father_name2"]
            lastaliya = request.form["lastaliya2"]
            lastaliya = datetime.date(datetime.strptime(lastaliya, "%Y-%m-%d"))
            print(firstname, lastaliya)
            al.db.session.query(al.Worshipers).filter(al.Worshipers.id == 227). \
                update({al.Worshipers.firstname: firstname, al.Worshipers.lastname: al.Worshipers.lastname,
                        al.Worshipers.phone: phone, al.Worshipers.city: city, al.Worshipers.addres: addres,
                        al.Worshipers.mail: mail, al.Worshipers.clan: clan, al.Worshipers.father_name: father_name,
                        al.Worshipers.lastaliya: lastaliya})
            al.db.session.commit()
            # print(type(lastaliya))
            # # worshiper = al.Worshipers(firstname=str(resdict["firstname"][0]), lastname=str(resdict["lastname"][0]),
            # #                           phone=str(resdict["phone"][0]), city=str(resdict["city"][0]),
            # #                           addres=str(resdict["addres"][0]), mail=str(resdict["mail"][0]),
            # #                           clan=str(resdict["clan"][0]), father_name=str(resdict["father_name"][0]),
            # #                           lastaliya=datedate)
            # # print(resdict["LastAliya"][0])
            # # print(type(resdict["LastAliya"][0]))
            # # al.db.session.add(worshiper)
            # # al.db.session.commit()
            return " המתפלל  עודכן בהצלחה למערכת!! "


        elif request.form['submit'] == 'View':
            # database = sqlite3.connect('gabay')
            id = request.form["id"]
            worshiper1 = al.Worshipers.query.filter_by(id=int(id)).first()
            firstname = worshiper1.firstname
            lastname = worshiper1.lastname
            phone = worshiper1.phone
            city = worshiper1.city
            addres = worshiper1.addres
            mail = worshiper1.mail
            clan = worshiper1.clan
            father_name = worshiper1.father_name
            lastaliya = worshiper1.lastaliya

            print(lastname, firstname)
            print(id)
            print(type(id))
            return render_template("update_worshiper.html", firstname=firstname, lastname=lastname, phone=phone,
                                   city=city, addres=addres, mail=mail, clan=clan, lastaliya=lastaliya,
                                   father_name=father_name, lstid=[id])



    elif request.method == "GET":

        lstfirst = []
        lstlast = []
        lstid = []
        database = sqlite3.connect('gabay')
        for id in al.db.session.query(al.Worshipers.id).all():
            lstid.append(id[0])
        for first in al.db.session.query(al.Worshipers.id).all():
            lstfirst.append(first[0])
        for last in al.db.session.query(al.Worshipers.id).all():
            lstlast.append(last[0])
        login = request.cookies.get('level')
        print(login)
        user = al.Users.query.filter_by(username=login).first()
        if user:
            print(user)
            return render_template("update_worshiper.html", lstid=lstid, user=user.username)
        else:
            return "You are not login"


@app.route('/delete_worshiper', methods=['POST', 'GET'])
def delete_worshiper():
    if request.method == 'POST':
        if request.form['submit'] == 'View':
            id = request.form["id"]
            firstname = (al.Worshipers.query.filter_by(id=id).first()).firstname
            lastname = (al.Worshipers.query.filter_by(id=id).first()).lastname
            print(lastname, firstname)
            print(id)
            print(type(id))

            return render_template("delete_worshiper.html", firstname=firstname, lastname=lastname, lstid=[id])
        if request.form['submit'] == 'Delete':
            id = request.form["id"]
            id2 = int(id)
            worshiper = al.Worshipers.query.filter_by(id=id2).first()
            print(worshiper.id)
            al.db.session.delete(worshiper)
            al.db.session.commit()
            # main_def.Worshiper.delete_worshiper_by_id(id)
            return "המתפלל נמחק בהצלחה!!!!!"


    elif request.method == "GET":

        lstid = []
        for id in al.db.session.query(al.Worshipers.id).all():
            lstid.append(id[0])
        login = request.cookies.get('level')
        print(login)
        user = al.Users.query.filter_by(username=login).first()
        print(user)
        return render_template("delete_worshiper.html", lstid=lstid, user=user.username)


@app.route('/delete_aliya', methods=['POST', 'GET'])
def delete_aliya():

    if request.method == 'POST':

        if request.form['submit'] == 'View':
            id = request.form["id"]
            date = (al.Aliyot.query.filter_by(id=int(id)).first()).date
            hebdate=jewish.JewishDate.from_date(date)
            hebdate=eng_date_to_heb(hebdate)
            print(date,hebdate)

            date="{}    , {}".format(date,hebdate)

            worshiperid = (al.Aliyot.query.filter_by(id=int(id)).first()).worshiper
            print(worshiperid)
            worshiper="{} {} ".format((al.Worshipers.query.filter_by(id=int(worshiperid)).first()).lastname,(al.Worshipers.query.filter_by(id=int(worshiperid)).first()).firstname)
            print(id)
            print(type(id))
            return render_template("delete_aliya.html", firstname=date, lastname=worshiper, lstid=[id])

        if request.form['submit'] == 'Delete':
            aliya = request.form["aliya"]
            aliya = (aliya.split(","))[0]
            print(aliya)
            print(type(aliya))
            aliya = al.Aliyot.query.filter_by(id=int(aliya)).first()

            print(type(aliya))
            al.db.session.delete(aliya)
            al.db.session.commit()
            #     # main_def.Worshiper.delete_worshiper_by_id(id)
            return "העליה נמחקה בהצלחה!!!"

    elif request.method == "GET":
        lstaliya=[]
        lstaliya2=al.db.session.query(al.Aliyot)
        for aliya in lstaliya2:
            hebdate2=aliya.date
            print(type(hebdate2))
            hebdate2=jewish.JewishDate.from_date(hebdate2)
            hebdate=eng_date_to_heb(hebdate2)
            print(hebdate)
            lstaliya.append(("{} , {} ,{} ,{} ,{} ,{}".format(aliya.id,aliya.parasha,aliya.worshiper,aliya.day,hebdate,aliya.reason)))
        print(lstaliya)
        login = request.cookies.get('level')
        print(login)
        user = al.Users.query.filter_by(username=login).first()
        print(user)
        return render_template("delete_aliya.html", lstaliya=lstaliya, user=user.username)

@app.route('/delete_event', methods=['POST', 'GET'])
def delete_event():
    if request.method == 'POST':
        event= request.form["event"]
        event=(event.split(","))[0]
        print(event)
        print(type(event))
        event = al.Events.query.filter_by(id=int(event)).first()

        print(type(event))
        al.db.session.delete(event)
        al.db.session.commit()
    #     # main_def.Worshiper.delete_worshiper_by_id(id)
        return "האירוע נמחק בהצלחה!!!"
    elif request.method == "GET":

        lstevent=[]
        lstevent2=al.db.session.query(al.Events)
        for event in lstevent2:
            hebdate2=event.date
            print(type(hebdate2))
            hebdate2=jewish.JewishDate.from_date(hebdate2)
            hebdate=eng_date_to_heb(hebdate2)
            print(hebdate)
            lstevent.append(("{} , {} ,{} ,{} ,{} ,{}".format(event.id,event.eventname,event.worshiper,event.day,hebdate,event.moed)))



        print(lstevent)
        login = request.cookies.get('level')
        print(login)
        user = al.Users.query.filter_by(username=login).first()
        print(user)
        return render_template("delete_event.html", lstevent=lstevent, user=user.username)


@app.route('/delete_donation', methods=['POST', 'GET'])
def delete_donation():
    if request.method == 'POST':
        id = request.form["id"]
        firstname = (al.Worshipers.query.filter_by(id=id).first()).firstname
        lastname = (al.Worshipers.query.filter_by(id=id).first()).lastname
        print(lastname, firstname)
        print(id)
        print(type(id))

        return render_template("delete_worshiper.html", firstname=firstname, lastname=lastname, lstid=[id])
    if request.form['submit'] == 'Delete':
        id = request.form["id"]
        id2 = int(id)
        worshiper = al.Worshipers.query.filter_by(id=id2).first()
        print(worshiper.id)
        al.db.session.delete(worshiper)
        al.db.session.commit()
        # main_def.Worshiper.delete_worshiper_by_id(id)
        return "התרומה הוסרה בהצלחה"

    elif request.method == "GET":
        lstfirst = []
        lstlast = []
        lstid = []
        database = sqlite3.connect('gabay')
        for id in al.db.session.query(al.Worshipers.id).all():
            lstid.append(id[0])
        for first in al.db.session.query(al.Worshipers.id).all():
            lstfirst.append(first[0])
        for last in al.db.session.query(al.Worshipers.id).all():
            lstlast.append(last[0])
        login = request.cookies.get('level')
        print(login)
        user = al.Users.query.filter_by(username=login).first()
        print(user)
        return render_template("delete_donation.html", lstid=lstid, user=user.username)


@app.route('/delete_yorzait', methods=['POST', 'GET'])
def delete_yorzait():
    if request.method == 'POST':
        id = request.form["id"]
        firstname = (al.Worshipers.query.filter_by(id=id).first()).firstname
        lastname = (al.Worshipers.query.filter_by(id=id).first()).lastname
        print(lastname, firstname)
        print(id)
        print(type(id))

        return render_template("delete_worshiper.html", firstname=firstname, lastname=lastname, lstid=[id])
    if request.form['submit'] == 'Delete':
        id = request.form["id"]
        id2 = int(id)
        worshiper = al.Worshipers.query.filter_by(id=id2).first()
        print(worshiper.id)
        al.db.session.delete(worshiper)
        al.db.session.commit()
        # main_def.Worshiper.delete_worshiper_by_id(id)
        return "היורצאייט הוסר בהצלחה"


    elif request.method == "GET":
        lstfirst = []
        lstlast = []
        lstid = []
        database = sqlite3.connect('gabay')
        for id in al.db.session.query(al.Worshipers.id).all():
            lstid.append(id[0])
        for first in al.db.session.query(al.Worshipers.id).all():
            lstfirst.append(first[0])
        for last in al.db.session.query(al.Worshipers.id).all():
            lstlast.append(last[0])
        login = request.cookies.get('level')
        print(login)
        user = al.Users.query.filter_by(username=login).first()
        print(user)
        return render_template("delete_yorzait.html", lstid=lstid, user=user.username)


@app.route('/delete_niftar', methods=['POST', 'GET'])
def delete_niftar():
    if request.method == 'POST':
        id = request.form["id"]
        firstname = (al.Worshipers.query.filter_by(id=id).first()).firstname
        lastname = (al.Worshipers.query.filter_by(id=id).first()).lastname
        print(lastname, firstname)
        print(id)
        print(type(id))

        return render_template("delete_worshiper.html", firstname=firstname, lastname=lastname, lstid=[id])
    if request.form['submit'] == 'Delete':
        id = request.form["id"]
        id2 = int(id)
        worshiper = al.Worshipers.query.filter_by(id=id2).first()
        print(worshiper.id)
        al.db.session.delete(worshiper)
        al.db.session.commit()
        # main_def.Worshiper.delete_worshiper_by_id(id)
        return "נפטר נחמק מהמערכת"



    elif request.method == "GET":
        lstfirst = []
        lstlast = []
        lstid = []
        database = sqlite3.connect('gabay')
        for id in al.db.session.query(al.Worshipers.id).all():
            lstid.append(id[0])
        for first in al.db.session.query(al.Worshipers.id).all():
            lstfirst.append(first[0])
        for last in al.db.session.query(al.Worshipers.id).all():
            lstlast.append(last[0])
        login = request.cookies.get('level')
        print(login)
        user = al.Users.query.filter_by(username=login).first()
        print(user)
        return render_template("delete_nifar.html", lstid=lstid, user=user.username)


@app.route('/next_aliyot_form', methods=['POST', 'GET'])
def next_aliyot_form():
    if request.method == 'POST':
        if request.form['submit'] == "View":
            print(request.form['submit'])
            date = request.form["date"]
            print(date)
            datedate = datetime.strptime(date, "%Y-%m-%d")
            jew = jewish.JewishDate.from_date(datedate)
            jew =eng_date_to_heb(jew)
            print(jew)
            # dic = {jewish.JewishDate(1, 1, 1): "ראש השנה יום ראשון", jewish.JewishDate(1, 1, 2): "ראש השנה יום שני",jewish.JewishDate(1, 1, 15): "חג סוכות", jewish.JewishDate(1, 1, 16): "חול המועד סוכות",jewish.JewishDate(1, 1, 17): "חול המועד סוכות", jewish.JewishDate(1, 1, 18): "ראש השנה"}
            # holyday = dic[jew]
            # id = request.form["id"]

            holyday = "af"
            return render_template("next_aliyot_form.html", jew=jew, holyday=holyday)
        elif request.form['submit'] =="Calc":
            return render_template("next_aliyot_view.html")
    if request.method == "GET":
        return render_template("next_aliyot_form.html")


@app.route("/set")
def setcookie():
    resp = make_response('Setting Level!')
    resp.set_cookie('try', 'added')
    return resp


@app.route("/get")
def getcookie():
    framework = request.cookies.get('try')
    return 'The Frame Work is ' + framework


@app.route('/logout', methods=['POST', 'GET'])
def logout():
    if request.method == 'POST':
        logincookie = make_response(render_template("index.html"))
        logincookie.set_cookie('level', '')
        return logincookie


if __name__ == '__main__':
    app.run(debug=True)
