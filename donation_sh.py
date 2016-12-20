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


def delete_donation(worshiper):
    examination = sqlite3.connect('gabay')
    l = []
    for i in examination.execute('SELECT worshiper FROM donations'):
        l.append(i[0])
    if str(worshiper) in l:
        examination.execute("DELETE FROM donations WHERE worshiper=\"{}\"".format(worshiper))
        examination.cursor()
        examination.commit()


def update_donation(id, worshiper=None, donationdate=None, donation=None):
    if donationdate:
        donationdate = datetime.date(donationdate)
    examination = sqlite3.connect('gabay')
    l = []
    for i in examination.execute('SELECT id FROM donations'):
        l.append(i[0])
    if id in l:
        if worshiper:
            l = []
            for i in examination.execute('SELECT id FROM worshipers'):
                l.append(i[0])
            if worshiper in l:
                examination.execute("UPDATE donations SET worshiper = '{}' WHERE  id = {};".format(worshiper, id))
            else:
                raise ValueError("Id not exist in the database")
        if donationdate:
            examination.execute("UPDATE donations SET donationdate = '{}' WHERE  id = {};".format(donationdate, id))
        if donation:
            examination.execute("UPDATE donations SET donation = '{}' WHERE  id = {};".format(donation, id))
        examination.cursor()
        examination.commit()
    else:
        raise ValueError("Id not exist in the database")
