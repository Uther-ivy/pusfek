import json
import logging
import math
import random
import re
import time
import traceback
from binascii import a2b_hex

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
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'
        }

    def replace_ip(self):
        print("ip获取中")
        proxy = ip_proxys.replace_ip()

        self.proxys = {
            'http': proxy,
            'https': proxy
        }


    def jiemi_(self, cipher_text):
        true = ""
        null = ""
        false=""
        key = 'jo8j9wGw%6HbxfFn'.encode('utf-8')
        iv = "0123456789ABCDEF".encode('utf-8')
        mode = AES.MODE_CBC
        cryptos = AES.new(key, mode, iv)
        plain_text_ = cryptos.decrypt(a2b_hex(cipher_text))
        print(plain_text_)
        Plain_text = bytes.decode(plain_text_)
        Plain_text = re.findall(r'(.*})', Plain_text)[0]
        return eval(Plain_text)



    def req_(self, url):
        prox = self.proxys
        # self.headers['token'] = token
        res = self._session.get(url=url, headers=self.headers,proxies=prox,  verify=False, timeout=60)
        if res.status_code == requests.codes.ok:
            res_data = res.content.decode()
            return res_data


    def request_(self, url):
        try:
            time.sleep(random.random() * 10)
            res = self.req_(url)
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
    def channel_info(self,value):
        try:
            for page in range(100):
                channel_url = f"https://jzsc.mohurd.gov.cn/api/webApi/dataservice/query/comp/list?" \
                              f"qy_region=130000&" \
                              f"apt_code={value}&" \
                              f"qy_type=QY_ZZ_ZZZD_001&" \
                              f"pg={page}&" \
                              f"pgsz=15&" \
                              f"total="
                url='https://sky.mohurd.gov.cn/skyapi/api/statis/getResult?_t=0.4809449572782587&keys=corp%2Fdata_search%2Fpage&qyTypeCode=&aptCode=&regionNum=130000&pageNumber=1&pageSize=15&keyWord='
                print(channel_url)
                resdata = self.jiemi_(self.request_(url))
                print(resdata)
                if resdata:
                    data=resdata['data']
                    # range(math.ceil(data / 15))
                    if data['list']:
                        for res in data['list']:
                            # print(res)
                            company=res.get('QY_NAME')
                            yield company
                    else:
                        print('没数据了')
                        break
                else:
                    print('没数据了')
                    break

        except Exception as e:
            logging.error(f"获取失败{e}\n{traceback.format_exc()}")


if __name__ == '__main__':
         spider = get_company()
         spider.replace_ip()
         certification={

# '建筑工程施工总承包特级':'D101T',
# '建筑工程施工总承包一级.txt':'D101A',
# '建筑工程施工总承包二级.txt':'D101B',
# '电力工程施工总承包特级':'D106T',
# '电力工程施工总承包一级':'D106A',
# '电力工程施工总承包二级':'D106B',
# '市政公用工程施工总承包特级':'D110T',
# '市政公用工程施工总承包一级':'D110A',
# '市政公用工程施工总承包二级':'D110B',
# '公路工程施工总承包特级':'D102T',
# '公路工程施工总承包一级':'D102A',
# '公路工程施工总承包二级':'D102B',
# '水利水电工程施工总承包特级':'D105T',
# '水利水电工程施工总承包一级':'D105A',
# '水利水电工程施工总承包二级':'D105B',
# '机电工程施工总承包特级':'D112T',
# '机电工程施工总承包一级':'D112A',
# '机电工程施工总承包二级':'D112B',
}
         for certifica,value in certification.items():
            file=f'./companyname/{certifica}.txt'
            # print(file ,value)
            for comname  in spider.channel_info(value):
                print(comname)
                spider.write_data(file, comname)