import pymysql

conn = pymysql.connect(
    host='47.92.73.25',
    user='duxie',
    password='jtkpwangluo.com',
    db='yqc')
cur=conn.cursor()
sql='select '