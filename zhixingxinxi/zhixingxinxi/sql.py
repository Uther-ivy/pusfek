# -*- coding: utf-8 -*-
import re
import time
import traceback

import pymysql
from unicodedata import decimal


class serversql(object):
    def __init__(self):
        self.db = pymysql.connect(
                        host='47.92.73.25',
                        port=3306,
                        user='python',
                        password='Kp123...',
                        database='yqc',
                        charset='utf8'
                )

    def insertinto(self,aid, name, province, cardID, casenum, court, disrupt, duty, sexy, performance, time):
        sql='insert into ' \
            'yunqi_zx(aid, name ,province, cardID, casenum, court , disrupt, duty , sexy, performance, time)' \
            'values ' \
            '(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);'
        cur=self.db.cursor()
        cur.execute(sql,(aid,name ,province, cardID, casenum, court , disrupt, duty , sexy, performance, time))
        self.db.commit()

    def companyaid(self,name):
        cur = self.db.cursor()
        sql = "SELECT aid FROM yunqi_addon17 WHERE qymc LIKE %s"
        cur.execute(sql, name)
        companyid = cur.fetchone()
        # print(type(nativeplace), nativeplace[0])
        return companyid

    def selectcase(self,casenum):
        cur = self.db.cursor()
        sql = "SELECT casenum,name FROM yunqi_zx WHERE casenum = %s"
        cur.execute(sql, casenum)
        body = cur.fetchall()
        # print(type(nativeplace), nativeplace[0])
        return body

def rundb(serverdb, datas):
    print('进入mysql')
    print(type(datas),datas)
    # data = eval(data)
    for data in datas:
        name = data.get('name')
        print(name)
        if name:
            aid = serverdb.companyaid(name)
            print(aid)
            casenum = data.get('casenum')
            if casenum :
                isexist = serverdb.selectcase(casenum)
                if not isexist:
                    cardID   = data.get('cardID')
                    province = data.get('province')
                    court = data.get('court')
                    disrupt = data.get('disrupt')
                    duty = data.get('duty')
                    sexy = data.get('sexy')
                    performance = data.get('performance')
                    time = data.get('time')
                    serverdb.insertinto(aid,name, province, cardID, casenum, court, disrupt, duty, sexy, performance, time)
                    print('数据保存成功')

                else:
                    print('已存在')


    # except Exception as e:
    #     print(f"{e}\n{traceback.format_exc()}")

if __name__ == '__main__':

    serverdb = serversql()
    for text in ['zhixing37.txt',
                 'zhixing38.txt',
                 'zhixing39.txt',
                 'zhixing40.txt',
                 'zhixing41.txt',
                 'zhixing42.txt',
                 'zhixing43.txt',
                 'zhixing44.txt',
                 'zhixing45.txt',
                 'zhixing46.txt',
                 'zhixing47.txt',
                 'zhixing48.txt',
                 'zhixing49.txt',
                 'zhixing50.txt',
                 'zhixing51.txt',
                 'zhixing52.txt',
                 'zhixing53.txt','zhixing54.txt','zhixing55.txt','zhixing56.txt','zhixing57.txt','zhixing58.txt','zhixing59.txt','zhixing60.txt']:
        print(text)
        with open(text, 'r', encoding='utf-8') as f:

            all_db = f.readlines()
        for data in all_db:
            data = eval(data)
            # print(type(data),data)
            rundb(serverdb, data)

    """
    id         
    aid        
    name        name
    province   province
    cardID      cardID,
    casenum     casenum,
    court       court,
    disrupt     disrupt
    duty        duty
    sexy        sexy,
    performance performance
    time        time
    """




