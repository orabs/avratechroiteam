
monthinhebrew={1:"תשרי",2:"חשון",3:"כסלו",4:"טבת",5:"שבט",6:"אדר א'",7:"אדר ב'",8:"ניסן",9:"אייר",10:"סיוון",11:"תמוז'",12:"אב",13:"אלול"}

from flask import *
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


import sqlite3
database = sqlite3.connect('gabay')
data = database.execute("select * from users").fetchall()
for item in data:
     tempuser = item[1]
     temppass = item[2]
     print(tempuser, temppass)

database.cursor()
database.commit()


