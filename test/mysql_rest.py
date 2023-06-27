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
def update_data(id,sheng):
    sql = f"update dede_arctiny set sheng='{sheng}' where id='{id}';"
    data = excute_mysql(sql, commit=True)
    print(data)
    return data


def search_data():
    sql = "select  id,sheng from dede_arctiny where url like'http://ggzyjy.liaocheng.gov.cn/%';"
    data= excute_mysql(sql)
    print(data)
    return data
# def del_():
#     sql = f"--  delete from dede_addoninfos7 where url='http://cr16g.crcc.cn%';"
#     data = excute_mysql(sql,commit=True)
#     print(data)
#     return data

# del_()

# search_data()

for data in search_data():
    id=data[0]
    sheng=8000
    update_data(id, sheng)
    # print(data)

