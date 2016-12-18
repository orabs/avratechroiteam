import sqlite3
from flask import Flask, redirect, url_for, request,render_template,make_response
app = Flask(__name__)
import main_def


@app.route('/',methods = ['POST', 'GET'])
def login():

   if request.method == 'POST':
      result = request.form
      resdict=dict(result)
      database = sqlite3.connect('gabay')
      data = (database.execute("select * from users")).fetchall()
      print(data)
      print(resdict["username"][0])
      print(resdict["password"][0])
      for item in data:
         tempuser=item[1]
         temppass=item[2]
         print(tempuser,temppass)
         if str(resdict["username"][0])==str(tempuser) and str(resdict["password"][0])==str(temppass):
            level=item[3]
            if level == 1:
               logincookie = make_response('You are logged in!')
               logincookie.set_cookie('level', '1')
            if level == 2:
               logincookie = make_response('You are logged in!')
               logincookie.set_cookie('level', '2')
            return  logincookie
         if str(resdict["username"][0])==str(tempuser) and  not str(resdict["password"][0])==str(temppass):
            return "Wrong Password"
      return "No Such Username"
   elif request.method=="GET":
      return render_template("index.html")

@app.route('/<table>')
def hello(table):

   if request.cookies.get('level') == '1':
      database = sqlite3.connect('gabay')
      data=database.execute("select * from {}".format(table))
      cursor = database.execute('select * from {}'.format(table))
      cols = list(map(lambda x: x[0], cursor.description))
      qu1=data.fetchall()
      cols=tuple(cols)
      qu1.insert(0,cols)
      return render_template("home.html",qu1=qu1,table=table,cols=cols)
   if request.cookies.get('level')=='2':
      return "You not alowed to get this information"
   if not request.cookies.get('level'):
      return "You not Login"





@app.route('/add_worshiper',methods = ['POST', 'GET'])
def add_worshiper():
   if request.method == 'POST':
      result = request.form
      resdict=dict(result)
      lst2=[]
      lst=[resdict["firstname"],resdict["lastname"],resdict["phone"],resdict["city"],resdict["addres"],resdict["mail"],resdict["clan"],resdict["father_name"],resdict["LastAliya"]]
      for i in lst:
         for j in i:
            lst2.append(j)

      lst2=[""]+lst2
      print(lst2)
      main_def.Worshiper.add_worshiper_lst(lst2)

      return " המתפלל הוסף בהצלחה למערכת!! "

   elif request.method=="GET":
      return render_template("worshipers.html")

@app.route("/set")
def setcookie():
   resp=make_response('Setting Level!')
   resp.set_cookie('try','added')
   return resp

@app.route("/get")
def getcookie():
   framework=request.cookies.get('try')
   return 'The Frame Work is ' +framework

@app.route('/logout',methods = ['POST', 'GET'])
def logout():
   if request.method == 'POST':
      logincookie = make_response('You Logged out succesfully')
      logincookie.set_cookie('level', '')
      return logincookie



if __name__ == '__main__':

   app.run(debug = True)



