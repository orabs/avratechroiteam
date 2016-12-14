import sqlite3
from datetime import datetime

def add_donation(worshiper,donation):
    examination = sqlite3.connect('gabay')
    re = examination.execute('SELECT id  FROM worshipers')
    for i in re:
        if worshiper  == i[0]: #or donationdate is not datetime:
            examination.execute('INSERT INTO donations (worshiper, donation) VALUES (\"{}\",\"{}\")'.format(worshiper,donation))
            # examination.cursor()
            examination.commit()
    raise ValueError("Id not exist in the database")

# # a = datetime(1988,12,12)
# # add_donation(224,'50')
#
# examination = sqlite3.connect('gabay')
# re = examination.execute('INSERT INTO donations (worshiper, donation) VALUES (\"{}\",\"{}\")'.format(224,100))
# re=re.fetchall()

print(add_donation(224,'50'))
gaga