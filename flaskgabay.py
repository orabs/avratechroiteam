import sqlite3
from flask import Flask, redirect, url_for, request,render_template
app = Flask(__name__)



@app.route('/<table>')
def hello(table):
   database = sqlite3.connect('gabay')
   data=database.execute("select * from {}".format(table))
   qu1=data.fetchall()

   return render_template("home.html",qu1=qu1,table=table)

if __name__ == '__main__':
   app.run(debug=True)


