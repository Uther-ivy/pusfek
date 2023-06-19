import traceback

import pymysql




def pooldb_conn():
    try:
        pooldb  = pymysql.connect(
    host='47.92.73.25',
    port=3306,
    user='duxie',
    password='jtkpwangluo.com',
    database='ytb',
    charset='utf8'
)
        return pooldb
    except Exception as e:
        traceback.format_exc()
        pooldb_conn()

def close_mysql(cur,pooldb):
    cur.close()
    pooldb.close()

def excute_mysql(sql, params=None, commit=False):

        pooldb = pooldb_conn()
        cur = pooldb.cursor()
        try:
            cur.execute(sql,params)
            if commit:
                pooldb.commit()
            data = cur.fetchall()
            return data
        except Exception as e:
            print(f"Error: {e}\n {sql}")
            print(traceback.format_exc())
        finally:
            close_mysql(cur,pooldb)

def search_url():

    # sql = f"select * from dede_addoninfos7 where title  like 'http://cr16g.crcc.cn%';"
    sql = "select * from dede_arctiny where title ='沈阳和平区';"
    data= excute_mysql(sql)
    print(data)
    return data
def del_():
    sql = f" delete from dede_addoninfos7 where url='http://cr16g.crcc.cn%';"
    data = excute_mysql(sql,commit=True)
    print(data)
    return data

# del_()
search_url()