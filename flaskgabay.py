import sqlite3
from flask import Flask, redirect, url_for, request, render_template, make_response
from flask_sqlalchemy import SQLAlchemy
import sql_alchemy_gabay as al
import main_def
import jewish
from datetime import datetime

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
        database = sqlite3.connect('gabay')
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


@app.route('/delete_worshiper', methods=['POST', 'GET'])
def delete_worshiper():
    if request.method == 'POST':
        if request.form['submit'] == 'View':
            database = sqlite3.connect('gabay')
            id = request.form["id"]
            firstname = database.execute("select firstname from worshipers where id={}".format(int(id)))
            lastname = database.execute("select lastname from worshipers where id={}".format(int(id)))
            firstname = firstname.fetchone()
            lastname = lastname.fetchone()
            firstname = firstname[0]
            lastname = lastname[0]
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
            return "deleted"


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
        return render_template("delete_worshiper.html", lstid=lstid, user=user.username)


@app.route('/next_aliyot_form', methods=['POST', 'GET'])
def next_aliyot_form():
    if request.method == 'POST':
        print(request.form['submit'])
        if request.form['submit'] == 'View':
            date = request.form["date"]
            print(type(date))
            jew = jewish.JewishDate.from_date(date)
            dic = {jewish.JewishDate(1, 1, 1): "ראש השנה יום ראשון", jewish.JewishDate(1, 1, 2): "ראש השנה יום שני",
                   jewish.JewishDate(1, 1, 15): "חג סוכות", jewish.JewishDate(1, 1, 16): "חול המועד סוכות",
                   jewish.JewishDate(1, 1, 17): "חול המועד סוכות", jewish.JewishDate(1, 1, 18): "ראש השנה"}
            holyday = dic[jew]
            id = request.form["id"]
            return render_template("next_aliyot_form.html", jew=jew, holyday=holyday, lstid=[id])

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
