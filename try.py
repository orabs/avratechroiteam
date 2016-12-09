import sqlite3
import json
str1 = str()
data = sqlite3.connect('finalproject')

for row in (data.execute('SELECT * FROM worshipers')):
    str1 = json.dumps(row)

print((str1))

def go_to():
    pass