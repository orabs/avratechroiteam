
import datetime
import jewish
import sqlite3
from flask import Flask, redirect, url_for, request
import json
today = datetime.date.today()
jewish_today = jewish.JewishDate.from_date(today)
rosh_hashannah = jewish.JewishDate(jewish_today.year + 1, 1, 1)
days_to_rh = rosh_hashannah.to_sdn() - jewish_today.to_sdn()
print(dir(jewish_today))

print(today)
print(jewish_today)
monthinhebrew={1:"תשרי",2:"חשון",3:"כסלו",4:"טבת",5:"שבט",6:"אדר א'",7:"אדר ב'",8:"ניסן",9:"אייר",10:"סיוון",11:"תמוז'",12:"אב",13:"אלול"}



print(monthinhebrew[(jewish_today.month)])

print(jewish_today)
print(jewish_today.isLeapYear)

print(jewish_today)




# app = Flask(__name__)
#
# @app.route('/worshipers')
# def worshipers():
#     str1 = str()
#     data = sqlite3.connect('finalproject')
#
#
#     for row in (data.execute('SELECT * FROM worshipers')):
#         str1 +="\n"+(json.dumps(row))
#
#
#     return "<table>{}</table>".format(str1)
#
#
# if __name__ == '__main__':
#    app.run(debug = True)