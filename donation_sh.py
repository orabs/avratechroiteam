import sqlite3
from datetime import datetime


def add_donation(worshiper,donationdate,donation):
    donationdate = datetime.date(donationdate)
    examination = sqlite3.connect('gabay')
    l = []
    for i in examination.execute('SELECT id FROM worshipers'):
        l.append(i[0])
    if worshiper in l:
        examination.execute('INSERT INTO donations (worshiper,donationdate, donation) VALUES (\"{}\",\"{}\",\"{}\")'.format(worshiper, donationdate, donation))
        examination.commit()
    else:
        raise ValueError("Id not exist in the database")

print(add_donation(worshiper=226, donationdate=datetime(day=5,month=6,year=1987), donation='100'))

def delete_donation(worshiper):
    examination = sqlite3.connect('gabay')
    l = []
    for i in examination.execute('SELECT worshiper FROM donations'):
        l.append(i[0])
    if str(worshiper) in l:
        examination.execute("DELETE FROM donations WHERE worshiper=\"{}\"".format(worshiper))
        examination.cursor()
        examination.commit()



# delete_donation(225)