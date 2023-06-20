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
def update_data(id,url):
    sql = f"update dede_arctiny set url='{url}' where id='{id}';"
    data = excute_mysql(sql, commit=True)
    print(data)
    return data


def search_data():
    sql = "select  id,url from dede_arctiny where url like'https://cg.95306.cn/proxy/portal/elasticSearch/indexView?noticeId=%';"
    data= excute_mysql(sql)
    print(data)
    return data
def del_():
    sql = f" delete from dede_addoninfos7 where url='http://cr16g.crcc.cn%';"
    data = excute_mysql(sql,commit=True)
    print(data)
    return data

# del_()
for data in search_data():
    id=data[0]
    url=data[1].replace('https://cg.95306.cn/proxy/portal/elasticSearch/indexView?noticeId=','https://cg.95306.cn/baseinfor/notice/informationShow?id=')
    update_data(id, url)
    print(id, url)