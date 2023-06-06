import json
import logging
import math
import os
import random
import re
import time
import traceback
from binascii import a2b_hex

import execjs
import requests
from Crypto.Cipher import AES

import ip_proxys


class get_company(object):

    def __init__(self):
        self._session=requests.session()

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
        print(prox)
        # self.headers['token'] = token
        res = self._session.get(url=url, headers=self.headers,proxies=prox,  verify=False, timeout=60)
        if res.status_code == requests.codes.ok:
            res_data = res.content.decode()
            return res_data


    def request_(self, url):
        try:
            time.sleep(random.random() * 10)
            res = self.req_(url)
            if not res:
                res=self.req_(url)
                print('None, waiting 10 m')
                print(res)
                time.sleep(600)
                self.replace_ip()
        except Exception:
            logging.info("proxy disabled！！！ change proxy")
            time.sleep(random.random() * 10)
            self.replace_ip()
            res = self.req_(url)
        # print(res)

        return res


    def write_data(self,file,data):
        with open(file,'a',encoding='utf-8') as w:
            w.write(data+'\n')
            w.close()

    # 建设工程企业list
    def channel_info(self):

        page = 0
        while True:
            page += 1
            channel_url = f'https://sky.mohurd.gov.cn/skyapi/api/statis/getResult?' \
                          f'_t=0.4809449572782587&' \
                          f'keys=corp%2Fdata_search%2Fpage&qyTypeCode=&aptCode=&regionNum=130000&pageNumber={page}&pageSize=15&keyWord='
            print(channel_url)
            encrypt=self.request_(channel_url)
            if encrypt:
                print(type(encrypt),encrypt)
                resdata = self.jiemi_(json.loads(encrypt)['data'])
                print(type(resdata),resdata)
                companylist=[]
                for res in json.loads(resdata):
                    print(res)
                    for data in res['data']['records']:
                        if data:
                            companydata={}
                            companydata['cname']=data['corpName']
                            companydata['corcode']=data['corpCode']
                            companydata['cid']=data["id"]
                            companylist.append(companydata)
                        # print(companydata)
                # print(companylist)
                if page >15:
                    page = 0
                    self.replace_ip()
                yield companylist,page

            else:
                print('None, jumppage')
                continue

    def get_company_info(self,cid):
        detail_url = f"https://sky.mohurd.gov.cn/skyapi/api/statis/getExtResult?_t=0.9219150372692497&keys=corp%2Fcorp_detail%2Fdetail&corpId={cid}"
        resdata = json.loads(self.jiemi_(self.request_(detail_url)['data']))[0]['data'][0]
        # print(type(resdata), resdata)
        print(resdata)
        return resdata


def run():
    try:
        spider = get_company()
        spider.replace_ip()
        comname=spider.channel_info()
        file = f'./companyname/appcname.txt'
        for data,page in comname:
            print(type(data), data)
            for cdata in data:
                print(cdata)
                spider.write_data(file, str(cdata))#
            print('page,', page, 'successful')
    except Exception as e:
        logging.error(f"获取失败{e}\n{traceback.format_exc()}")


                # break
def read_name():
    files='./companyname'
    lsdir=os.listdir(files)
    for ls in lsdir:
        files=f'./companyname/{ls}'
        print(ls)
        with open(files, 'r', encoding='utf-8') as r:
            re=r.readlines()
            for a in re:
                print(a.replace('\n',''))
        # print(len(re))
        #     print(type(eval(a)),eval(a))

if __name__ == '__main__':
    # run()
    read_name()

    #     查看appcname.txt
    # with open(file,'r',encoding='utf-8')as r:
    #     re=r.readlines()
    #     print(len(re))
    #     for a in re:
    #         print(type(eval(a)),eval(a))