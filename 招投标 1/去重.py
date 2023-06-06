# -*- coding: utf-8 -*-
import save_database


conn = save_database.conn
cursor = conn.cursor()

sql = 'select url from reptile'

cursor.execute(sql)
ls = cursor.fetchall()
lss = list(set(ls))


for i in lss:
    num = 0
    for j in ls:
        if i == j:
            num+=1
    if num >1:
        print(i, num)

