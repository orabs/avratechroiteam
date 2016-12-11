

def select_next_readers_clan(worshiper=5,shevet="Israel"):                 #get days and give list of tuple of worshipers ('defult =30 days)
    database = sqlite3.connect('gabay')
    data = database.execute(
        "select * from worshipers where clan=\"{}\" order by LastAliya DESC limit {}".format(shevet, worshiper))
    reslst=[]

    datalst=data.fetchall()

    for worshiper in datalst:
        reslst.append(worshiper)


    return reslst