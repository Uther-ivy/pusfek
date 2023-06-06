import json
import logging
import random
import re
import threading
import time
import traceback
from urllib.parse import quote

import execjs
import pymysql
import requests
from dbutils.pooled_db import PooledDB

from spider import ip_proxys


class get_company(object):

    def __init__(self):
        self._session=requests.session()
        self.companyset=set()
        self.citycode=[]
        self.proxys = {
            'http': '',
            'https': ''
        }

        self.headers= {
        'token':'t_6b47c131f6f148a89bfd528b01145219',
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'
        }

    def replace_ip(self):
        proxy = ip_proxys.replace_ip()

        self.proxys = {
                'http': proxy,
                'https': proxy
            }



    def jiemi_(self, data):
        js_infos = '''function deCrypt(t) {
            Object.defineProperty(exports, "__esModule", {
            value: !0
        }), exports.deCrypt = exports.enCrypt = void 0;
            var e = require("./js/38B128C16AECE6CF5ED740C61D4FAC62.js"), r = e.enc.Hex.parse("cd3b2e6d63473cadda38a9106b6b4e07");
            console.log(r)
            var p = e.AES.decrypt(t, r, {
                mode: e.mode.ECB,
                padding: e.pad.Pkcs7,
            });
            utf8String = e.enc.Utf8.stringify(p);
            return utf8String;
        }

        module.exports.init = function (arg1) {
            //调用函数，并返回
            console.log(deCrypt(arg1));
        };'''

        dedata = execjs.compile(js_infos).call('deCrypt', data)
        # 读取结果
        print('解密完成')
        return dedata

    def req_(self, url):
        prox = self.proxys
        res = self._session.get(url=url, headers=self.headers,proxies=prox,  verify=False, timeout=60)
        if res.status_code == requests.codes.ok:
            res_data = json.loads(res.content.decode())
            return res_data


    def request_(self, url):
        try:
            res = self.req_(url)
            if not res:
                self.replace_ip()
                res=self.req_(url)
                print(res)
        except Exception:
            logging.info("proxy disabled！！！ change proxy")
            time.sleep(random.random() * 10)
            self.replace_ip()
            res = self.req_(url)

        return res



    def get_company_id(self,companyname):
        name=companyname.replace('\n','')
        url = f"https://sky.mohurd.gov.cn/skyapi/api/statis/getResult?_t=0.41493411788348533&keys=corp%2Fdata_search" \
              f"%2Fpage&qyTypeCode=&aptCode=&regionNum=&pageNumber=1&pageSize=15&keyWord={quote(name)}"
        resdata = json.loads(self.jiemi_(self.request_(url)['data']))[0]['data']['records']
        print(resdata)
        if len(resdata) > 0:
            for data in resdata:
                companydata = {}
                companydata['cname'] = data['corpName']
                companydata['cid'] = data["id"]
                # print(companydata)
                self.companyset.add(str(companydata))
                # time.sleep(5+random.random()*5)
            # return self.companyset
        else:
            print(companyname, '没搜到')
            # times = time.time()
            # insert_yunqi_cai(name, times)

    def get_company_info(self,cid,name):
        detail_url = f"https://sky.mohurd.gov.cn/skyapi/api/statis/getExtResult?_t=0.9219150372692497&keys=corp%2Fcorp_detail%2Fdetail&corpId={cid}"
        try:
            resdata = json.loads(self.jiemi_(self.request_(detail_url)['data']))[0]['data'][0]
            # print(type(resdata), resdata)
            print(resdata)
            cityid = resdata.get('regionFullname').replace('-省直辖县级行政区划', '')
            print(cityid)
            if "-" in cityid:
                cityid = re.findall(r'\w+\-(\w+)', cityid)[0]
                print(cityid)
            else:
                cityid = re.findall(r'\w+', cityid)[0]
                print(cityid)
            nativeplace = findcityid(cityid)
            print(name,nativeplace)
            updata_sql(name, nativeplace)
        except Exception:
            print('出错，已经存入nativeerror')
            write_name('nativeerror.txt', name)
        # time.sleep(22222)
        # return resdata


db=PooledDB(
    creator=pymysql,
    blocking=True,
    maxconnections=1000,
    maxshared=1000,
    host='47.92.73.25',
    user='python',
    passwd='Kp123...',
    db='yqc',
    port=3306,
    charset="utf8"
)
def findcityid(name):
    with open('yunqi_city.json', 'r', encoding='utf8') as r:
        lines = eval(r.read())
        # print(lines)
    for lis in lines.get('RECORDS'):
        # print(lis['typename'],type(lis['typename']))
        if name in lis['name']:
            print(lis['name'], lis['id'])
            return lis['id']

def get_sql_company(data):
    pooldb = db.connection()
    cur = pooldb.cursor()
    sql = "select qymc from yunqi_addon17 where (nativeplace='{}')".format(data)
    cur.execute(sql)
    data = cur.fetchall()

    cur.close()
    pooldb.close()

    return data

def updata_sql(qymc,native):
    pooldb = db.connection()
    cur = pooldb.cursor()
    sql = f"update yunqi_addon17 set nativeplace = '{native}' where qymc='{qymc}';"
    cur.execute(sql)
    pooldb.commit()
    cur.close()
    pooldb.close()
#


def write_name(files,ls):
        with open(f'companyname/{files}', 'a', encoding='utf-8')as w:
            w.write(ls+'\n')
        # print(spider.companyset)
def get_name():
    companyall = get_sql_company('0')
    for ls in companyall:
        write_name('errorname.txt', ls[0])

def updata_sql_company_nativeplce():
    try:

        fil = '0'
        spider = get_company()
        with open('companyname/errorname2.txt', 'r', encoding='utf-8') as r:
            companylist = r.readlines()
            print(companylist)
        # companylist=['陕西合勉温建设工程有限公司','陕西时温建设工程有限公司']
        while True:
            threads = []
            if len(companylist) > 10:
                rangenum = 10
            elif len(companylist) < 10 and len(companylist) > 0:
                rangenum = len(companylist)
            else:
                break
            for n in range(rangenum):
                companyname = companylist.pop().replace('\n', '')
                print(companyname)
                threadid = threading.Thread(target=spider.get_company_id, args=(companyname,))
                threadid.start()
                threadid.join()
            # print(spider.companyset)
            for company in spider.companyset:
                # time.sleep(5 + random.random() * 5)
                companybase = eval(company)
                print(companybase)
                cid = companybase.get('cid')
                cname = companybase.get('cname')
                scthread = threading.Thread(target=spider.get_company_info, args=(cid, cname))
                print('*' * 20, scthread.getName(), '*' * 20)
                scthread.start()
                threads.append(scthread)
            for thread in threads:
                thread.join()
            spider.companyset.clear()
    except Exception:
        traceback.print_exc()

if __name__ == '__main__':
    # get_name()
    updata_sql_company_nativeplce()
    # get_company_info(cid)
    # nativeplace = findcityid('山东省')
    # print(nativeplace)
    # datalist = updata_sql_company_nativeplce(name,nativeplace)
    # print(data)
