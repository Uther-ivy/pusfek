import json
import logging
import random
import re
import time
import traceback
import urllib.parse

import requests as requests

class bdzxspider(object):
    def __init__(self):
        self._session=requests.session()
        self.proxys = {
            'http': '',
            'https': ''
        }
        self.headers= {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'
    }
    def replace_ip(self):
        print("ip获取中")
        headers2 = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'
        }
        url = 'http://api2.xkdaili.com/tools/XApi.ashx?apikey=XK856A0B599311BA6A85&qty=1&format=json&split=0&sign=5ef92dedf192e4c668afc6fd3e3c428b'
        try:
            text_ = requests.get(url, headers=headers2, timeout=60).text
            response = json.loads(text_)
            print(response)
            # res=response['RESULT']
            res = response['data'][0]
            ip1 = 'http://{}:{}'.format(res['ip'], res['port'])
            ip2 = 'http://{}:{}'.format(res['ip'], res['port'])
            # redisconn.set(f'ip_{ip_num}', json.dumps(ip))
            self.proxys['http']=ip1
            self.proxys['https']=ip2
            # time.sleep(400)# break
            print(self.proxys)
        except Exception as e:
            logging.error(f"获取失败{e}\n{traceback.format_exc()}")
            time.sleep(20)
            # continue

    # def get_proxys():
    #     proxys = {
    #         'http': ip1,
    #         'https': ip2
    #     }
    #     print(proxys)
    #     return json.dumps(proxys)

    def req_(self, url):
        prox=self.proxys
        res = self._session.get(url=url, headers=self.headers, proxies=prox, verify=False, timeout=60)
        if res.status_code == requests.codes.ok:
            # print(res.content.decode())
            res_data = res.content.decode()
            return res_data

    def request_(self, url):
        try:
            # time.sleep(random.random() * 10)
            res = self.req_(url)
        except Exception:
            logging.info("proxy disabled！！！ change proxy")
            time.sleep(random.random() * 10)
            self.replace_ip()
            res = self.req_(url)
        return res


    def bdzhixin(self,name):
        zx_lists = []
        url = 'https://sp1.baidu.com/8aQDcjqpAAV3otqbppnN2DJv/api.php?' \
              'resource_id=6899&' \
              'query=%E5%A4%B1%E4%BF%A1%E8%A2%AB%E6%89%A7%E8%A1%8C%E4%BA%BA%E5%90%8D%E5%8D%95&' \
              f'cardNum=&' \
              f'iname={urllib.parse.quote(name)}&' \
              'areaName=&' \
              'from_mid=1&ie=utf-8&oe=utf-8&format=json&t=1667204886210&cb=jQuery110203509269674718134_1667204816211&_=1667204816212'
        try:
            res= self.request_(url)
            if res:
                # print(type(res), res)
                data = re.findall('jQuery\d+\_\d+\((.*)\)', res)
                list_zx = eval(data[0])['data'][0]['disp_data']
                # print(list_zx)
                if list_zx:
                    for zxpr in list_zx:
                        print(zxpr)
                        zx_dict = {}
                        zx_dict['id'] = zxpr['SiteId']
                        zx_dict['province'] = zxpr['areaNameNew']
                        zx_dict['cardID'] = zxpr['cardNum']
                        zx_dict['casenum'] = zxpr['caseCode']
                        zx_dict['court'] = zxpr['gistUnit']
                        zx_dict['disrupt'] = zxpr['disruptTypeName']
                        zx_dict['duty']= zxpr['duty']
                        zx_dict['name'] = zxpr['iname']
                        zx_dict['sexy'] = zxpr['sexy']
                        zx_dict['performance'] = zxpr['performance']
                        zx_dict['time'] = int(time.mktime(time.strptime(zxpr['publishDate'], "%Y年%m月%d日")))

                        zx_lists.append(zx_dict)
                    print(zx_lists)
                    return zx_lists
                else:
                    print("没有被执行案件")
                    return ''
        except Exception as e:
            logging.error(f"获取失败{e}\n{traceback.format_exc()}")

if __name__ == '__main__':

    # name = '北京百度建筑装饰工程有限公司'  # 公司名或人名
    # card = ''  # 身份证或组织机构代码9113010057****7053
    line = ''
    try:
        fil = '52'
        flies = f'企业名称/{fil}.txt'
        spider = bdzxspider()
        with open(file=flies, mode="r", encoding="utf-8") as r:
            data = r.readlines()
            # print(data)
        # data=['北京百度建筑装饰工程有限公司']
        spider.replace_ip()
        try:
            for line in data:
                print(type(line), line)
                zhixingdb = spider.bdzhixin(line.strip())
                print(zhixingdb)
                if zhixingdb:
                    with open(file=f"zhixingxinxi/zhixing{fil}.txt", mode="a", encoding="utf-8") as w:
                        data = w.write(str(zhixingdb) + '\n')
                    print('完成')

                else:
                    with open(file=f"zhixingxinxi/meizhixing{fil}.txt", mode="a", encoding="utf-8") as w:
                        data = w.write(str(line))
                        print(line, '没搜到')
            w.close()
        except Exception as e:
            print(e)
        r.close()
    except Exception as e:
        logging.error(f"{line}获取失败{e}\n{traceback.format_exc()}")
