import traceback

import pymysql
from lxml import etree

import tool
from 市级.衡水市公共资源交易平台 import alashan_ggzy


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
def update_shi(id,code):
    sql = f"update dede_arctiny set shi='{code}',nativeplace='{code}' where id='{id}';"
    data = excute_mysql(sql, commit=True)
    print(data)
    return data
def update_sheng(id,code):
    sql = f"update dede_arctiny set sheng='{code}' where id='{id}';"
    data = excute_mysql(sql, commit=True)
    print(data)
    return data

def updata_body(id ,code):
    sql = f"update dede_arctiny set body='{code}' where id='{id}';"
    data = excute_mysql(sql, commit=True)
    print(data)
    return data
def search_data():
    sql = "select  id ,url,title,senddate from dede_arctiny where url like'http://hsggzy.hengshui.gov.cn/%';"
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


if __name__ == '__main__':

    jl = alashan_ggzy()
    for data in search_data():
        print(data)
        #
        code= jl.parse_detile(data[2], data[1], data[3])
        print(code)

        #     sheng=7500
        #     update_sheng(id, sheng)
        #     if data[1]!=8002.0:
        # shi=7502
        # update_shi(id, shi)
        # print(data)
        id=data[0]
        # updata_body(id,code)
