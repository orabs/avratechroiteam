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

# add_donation(worshiper=230, donationdate=datetime(day=5,month=6,year=1987), donation='100')

def delete_donation(worshiper):
    examination = sqlite3.connect('gabay')
    l = []
    for i in examination.execute('SELECT worshiper FROM donations'):
        l.append(i[0])
    if str(worshiper) in l:
        examination.execute("DELETE FROM donations WHERE worshiper=\"{}\"".format(worshiper))
        examination.cursor()
        examination.commit()

def update_donation(worshiper, donationdate=None, donation=None):
    # donationdate = datetime.date(donationdate)
    examination = sqlite3.connect('gabay')
    l = []
    for i in examination.execute('SELECT worshiper FROM donations'):
        l.append(i[0])
    if str(worshiper) in l:
        if donationdate:
            examination.execute("UPDATE donations SET donationdate = '{}' WHERE  worshipers.id = {};".format(donationdate, worshiper))
        if donation:
            examination.execute("UPDATE donations SET donation = '{}' WHERE  worshipers.id = {};".format(donation, worshiper))
        examination.cursor()
        examination.commit()
    else:
        raise ValueError("Id not exist in the database")

def update_donation1(id, worshiper=None, donationdate=None, donation=None):
    # donationdate = datetime.date(donationdate)
    examination = sqlite3.connect('gabay')
    l = []
    for i in examination.execute('SELECT id FROM donations'):
        l.append(i[0])
    if id in l:
        if donationdate:
            examination.execute("UPDATE donations SET donationdate = '{}' WHERE  id = {};".format(donationdate, id))
        if donation:
            examination.execute("UPDATE donations SET donation = '{}' WHERE  id = {};".format(donation, id))
        examination.cursor()
        examination.commit()
    else:
        raise ValueError("Id not exist in the database")
# delete_donation(230)
update_donation(worshiper=229, donation='200')