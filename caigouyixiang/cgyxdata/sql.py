import re
import time
import traceback
import pymysql


class serversql(object):
    def __init__(self):
        self.db = pymysql.connect(
                        host='47.92.73.25',
                        port=3306,
                        user='python',
                        password='Kp123...',
                        database='ytb',
                        charset='utf8'
                )

    def insertinto(self,mid, title, senddate, body, url,addtime, click,nativeplace,price):
        sql='insert into ' \
            'dede_addoninfos12(mid, title, senddate, body, url,addtime, click,nativeplace,price)' \
            'values ' \
            '(%s,%s,%s,%s,%s,%s,%s,%s,%s);'
        cur=self.db.cursor()
        cur.execute(sql,(mid, title, senddate, body, url,addtime, click,nativeplace,price))
        self.db.commit()

    def selectcityid(self,city):
        cur = self.db.cursor()
        sql = "SELECT id FROM dede_city WHERE name LIKE %s"
        cur.execute(sql, city)
        nativeplace = cur.fetchone()
        # print(type(nativeplace), nativeplace[0])
        return nativeplace

    def selectbody(self,title):
        cur = self.db.cursor()
        sql = "SELECT body,price FROM dede_addoninfos12 WHERE title LIKE %s"
        cur.execute(sql, title)
        body = cur.fetchone()
        # print(type(nativeplace), nativeplace[0])
        return body

def rundb(serverdb, data):


    districtName = data.get('districtName')

    if districtName:
        nativeplace = serverdb.selectcityid(districtName)  # 地区id
        print(districtName)

    mid = data.get('articleId')  # 用户mid
    title=data.get('title')
    # mid=int(str(time.time()*1000)[::3])
    senddate = data.get('publishDate')  #
    url = data.get('detailurl')  #
    body=data.get('detail')
    addtime = data.get('futher')
    if not addtime:  #
        addtime = int(time.time())
    click = data.get('')  #
    price = data.get('price')

    try:
        reference= serverdb.selectbody(title)
        if not reference:
            serverdb.insertinto(mid, title, senddate, body, url,addtime, click,nativeplace,price)
            print('数据保存成功')
        else:
            print('已存在')
    except Exception as e:
        print(f"{e}\n{traceback.format_exc()}")





if __name__ == '__main__':
    serverdb = serversql()
    with open('hunancgyxspider.txt','r',encoding='utf-8')as f:
        all_db=f.readlines()
        for data in all_db:
            data = eval(data)
            rundb(serverdb,data)

