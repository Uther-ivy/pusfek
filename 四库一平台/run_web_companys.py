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
from spider.sql import insert_skid


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
    def channel_info(self,region,cret):
        try:
            total=0
            for page in range(100):
                print('*'*30,page,'*'*20)
                channel_url = f"https://jzsc.mohurd.gov.cn/APi/webApi/dataservice/query/comp/list?" \
                              f"qy_region={region}&" \
                              f"apt_code={cret}&" \
                              f"pg={page}&" \
                              f"pgsz=15&" \
                              f"total={total}"


                # url='https://sky.mohurd.gov.cn/skyapi/api/statis/getResult?_t=0.4809449572782587&keys=corp%2Fdata_search%2Fpage&qyTypeCode=&aptCode=&regionNum=130000&pageNumber=1&pageSize=15&keyWord='
                print(channel_url)
                resdata = self.jiemi_(self.request_(channel_url))
                print(resdata)
                if resdata:
                    data=resdata['data']
                    total=data['total']
                    # range(math.ceil(data / 15))
                    if data['list']:
                        for res in data['list']:
                            # print(res)
                            cname=res.get('QY_NAME')
                            cid =res.get('QY_ID')
                            insert_skid(cname,cid)
                            yield str([cname,cid])
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
         region_code = [#'110000', '120000', '130000', '140000', '150000', '210000', '220000','230000','310000','320000','330000','340000',

                        '350000','360000',
                        '370000','410000','420000','430000','440000','450000','460000','500000',
                        '510000','520000','530000','540000','610000','620000','630000','640000',
                        '650000','660000'
                        ]
         certs=[
      {
        'APT_ORDER': 0,
        'APT_CASENAME': '建筑工程施工总承包特级',
        'APT_ISEND': '1',
        'APT_CODE': 'D101T',
        'APT_TYPE': 'QY_ZZ_ZZZD_001',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 0,
        'APT_CASENAME': '公路工程施工总承包特级',
        'APT_ISEND': '1',
        'APT_CODE': 'D102T',
        'APT_TYPE': 'QY_ZZ_ZZZD_001',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 0,
        'APT_CASENAME': '铁路工程施工总承包特级',
        'APT_ISEND': '1',
        'APT_CODE': 'D103T',
        'APT_TYPE': 'QY_ZZ_ZZZD_001',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 0,
        'APT_CASENAME': '港口与航道工程施工总承包特级',
        'APT_ISEND': '1',
        'APT_CODE': 'D104T',
        'APT_TYPE': 'QY_ZZ_ZZZD_001',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 0,
        'APT_CASENAME': '水利水电工程施工总承包特级',
        'APT_ISEND': '1',
        'APT_CODE': 'D105T',
        'APT_TYPE': 'QY_ZZ_ZZZD_001',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 0,
        'APT_CASENAME': '电力工程施工总承包特级',
        'APT_ISEND': '1',
        'APT_CODE': 'D106T',
        'APT_TYPE': 'QY_ZZ_ZZZD_001',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 0,
        'APT_CASENAME': '矿山工程施工总承包特级',
        'APT_ISEND': '1',
        'APT_CODE': 'D107T',
        'APT_TYPE': 'QY_ZZ_ZZZD_001',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 0,
        'APT_CASENAME': '冶金工程施工总承包特级',
        'APT_ISEND': '1',
        'APT_CODE': 'D108T',
        'APT_TYPE': 'QY_ZZ_ZZZD_001',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 0,
        'APT_CASENAME': '石油化工工程施工总承包特级',
        'APT_ISEND': '1',
        'APT_CODE': 'D109T',
        'APT_TYPE': 'QY_ZZ_ZZZD_001',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 0,
        'APT_CASENAME': '市政公用工程施工总承包特级',
        'APT_ISEND': '1',
        'APT_CODE': 'D110T',
        'APT_TYPE': 'QY_ZZ_ZZZD_001',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计综合资质甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A1A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计煤炭行业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A201A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计化工石化医药行业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A202A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计石油天然气（海洋石油）行业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A203A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计电力行业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A204A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计冶金行业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A205A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计军工行业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A206A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计机械行业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A207A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计商物粮行业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A208A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计核工业行业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A209A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计电子通信广电行业（电子工程）甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A21001A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计电子通信广电行业（通信工程）甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A21002A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计电子通信广电行业（广电工程）甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A21003A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计轻纺行业（轻工工程）甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A21101A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计轻纺行业（纺织工程）甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A21102A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计建材行业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A212A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计铁道行业甲（Ⅰ）级',
        'APT_ISEND': '1',
        'APT_CODE': 'A213A1',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计铁道行业甲（Ⅱ）级',
        'APT_ISEND': '1',
        'APT_CODE': 'A213A2',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计公路行业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A214A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计水运行业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A215A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计民航行业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A216A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计市政行业（燃气工程、轨道交通工程除外）甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A21701A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计市政行业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A217A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计农林行业（农业工程）甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A21801A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计农林行业（林业工程）甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A21802A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计水利行业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A219A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计海洋行业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A220A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计建筑行业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A221A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计煤炭行业矿井专业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A30101A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计煤炭行业露天矿专业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A30102A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计煤炭行业选煤厂专业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A30103A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计化工石化医药行业炼油工程专业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A30201A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计化工石化医药行业化工工程专业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A30202A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计化工石化医药行业石油及化工产品储运专业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A30203A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计化工石化医药行业化工矿山专业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A30204A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计化工石化医药行业生化、生物药专业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A30205A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计化工石化医药行业中成药专业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A30206A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计化工石化医药行业化学原料药专业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A30207A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计化工石化医药行业药物制剂专业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A30208A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计化工石化医药行业医疗器械（含药品内包装）专业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A30209A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计石油天然气（海洋石油）行业油田地面专业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A30301A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计石油天然气（海洋石油）行业气田地面专业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A30302A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计石油天然气（海洋石油）行业管道输送专业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A30303A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计石油天然气（海洋石油）行业海洋石油专业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A30304A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计石油天然气（海洋石油）行业油气库专业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A30305A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计石油天然气（海洋石油）行业油气加工专业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A30306A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计石油天然气（海洋石油）行业石油机械制造与修理专业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A30307A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计电力行业火力发电（含核电站常规岛设计）专业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A30401A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计电力行业水力发电（含抽水蓄能、潮汐）专业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A30402A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计电力行业风力发电专业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A30403A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计电力行业送电工程专业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A30405A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计电力行业变电工程专业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A30406A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计冶金行业金属冶炼工程专业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A30501A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计冶金行业金属材料工程专业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A30502A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计冶金行业焦化和耐火材料工程专业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A30503A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计冶金行业冶金矿山工程专业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A30504A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计军工行业导弹及火箭弹工程专业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A30601A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计军工行业弹、火工品及固体发动机工程专业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A30602A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计军工行业燃机、动力装置及航天发动机工程专业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A30603A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计军工行业控制系统、光学、光电、电子、仪表工程专业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A30604A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计军工行业科研、靶场、试验、教育培训工程专业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A30605A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计军工行业地面设备工程专业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A30606A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计军工行业航天空间飞行器工程专业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A30607A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计军工行业运载火箭制造工程专业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A30608A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计军工行业地面制导站工程专业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A30609A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计军工行业航空飞行器工程专业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A30610A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计军工行业机场工程专业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A30611A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计军工行业船舶制造工程专业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A30612A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计军工行业船舶机械工程专业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A30613A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计军工行业船舶水工工程专业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A30614A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计军工行业坦克、装甲车辆工程专业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A30615A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计军工行业枪、炮工程专业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A30616A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计军工行业火、炸药工程专业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A30617A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计军工行业防化、民爆器材工程专业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A30618A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计机械行业通用设备制造业工程专业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A30701A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计机械行业专用设备制造业工程专业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A30702A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计机械行业交通运输设备制造业工程专业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A30703A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计机械行业电气机械设备制造业工程专业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A30704A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计机械行业金属制品业工程专业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A30705A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计机械行业仪器仪表及文化办公机械制造业工程专业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A30706A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计机械行业机械加工专业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A30707A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计机械行业热加工专业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A30708A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计机械行业表面处理专业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A30709A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计机械行业检测专业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A30710A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计机械行业物料搬运及仓储专业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A30711A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计商物粮行业冷冻冷藏工程专业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A30801A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计商物粮行业肉食品加工工程专业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A30802A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计商物粮行业批发配送与物流仓储工程专业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A30803A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计商物粮行业成品油储运工程专业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A30804A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计商物粮行业粮食工程专业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A30805A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计商物粮行业油脂工程专业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A30806A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计核工业行业反应堆工程设计（含核电站反应堆工程）专业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A30901A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计核工业行业核燃料加工制造及处理工程专业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A30902A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计核工业行业铀矿山及选冶工程专业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A30903A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计核工业行业核设施退役及放射性三废处理处置工程专业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A30904A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计核工业行业核技术及同位素应用工程专业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A30905A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计电子通信广电行业电子整机产品项目工程专业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A31001A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计电子通信广电行业电子基础产品项目工程专业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A31002A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计电子通信广电行业显示器件项目工程专业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A31003A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计电子通信广电行业微电子产品项目工程专业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A31004A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计电子通信广电行业电子特种环境工程专业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A31005A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计电子通信广电行业电子系统工程专业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A31006A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计电子通信广电行业有线通信专业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A31007A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计电子通信广电行业无线通信专业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A31008A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计电子通信广电行业邮政工程专业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A31009A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计电子通信广电行业通信铁塔专业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A31010A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计电子通信广电行业广播电视中心专业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A31011A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计电子通信广电行业广播电视发射专业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A31012A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计电子通信广电行业广播电视传输专业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A31013A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计电子通信广电行业电影工程专业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A31014A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计轻纺行业制浆造纸工程专业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A31101A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计轻纺行业食品发酵烟草工程专业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A31102A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计轻纺行业制糖工程专业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A31103A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计轻纺行业日化及塑料工程专业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A31104A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计轻纺行业日用硅酸盐工程专业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A31105A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计轻纺行业制盐及盐化工程专业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A31106A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计轻纺行业皮革毛皮及制品专业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A31107A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计轻纺行业家电电子及日用机械专业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A31108A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计轻纺行业纺织工程专业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A31109A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计轻纺行业印染工程专业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A31110A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计轻纺行业服装工程专业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A31111A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计轻纺行业化纤原料工程专业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A31112A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计轻纺行业化纤工程专业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A31113A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计建材行业水泥工程专业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A31201A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计建材行业玻璃、陶瓷、耐火材料工程专业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A31202A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计建材行业新型建筑材料工程专业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A31203A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计建材行业非金属矿及原料制备工程专业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A31204A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计建材行业无机非金属材料及制品工程专业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A31205A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计铁道行业桥梁专业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A31301A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计铁道行业轨道专业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A31302A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计铁道行业隧道专业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A31303A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计铁道行业电气化专业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A31304A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计铁道行业通信信号专业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A31305A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计公路行业公路专业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A31401A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计公路行业特大桥梁专业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A31402A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计公路行业特长隧道专业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A31403A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计公路行业交通工程专业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A31404A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计水运行业港口工程专业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A31501A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计水运行业航道工程专业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A31502A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计水运行业通航建筑工程专业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A31503A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计水运行业修造船厂水工工程专业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A31504A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计水运行业港口装卸工艺专业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A31505A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计水运行业水上交通管制工程专业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A31506A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计民航行业机场总体规划工程专业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A31601A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计民航行业场道、目视助航工程专业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A31602A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计民航行业通信、导航、航管及航站楼弱电工程专业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A31603A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计民航行业供油工程专业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A31604A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计市政行业给水工程专业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A31701A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计市政行业排水工程专业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A31702A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计市政行业城镇燃气工程专业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A31703A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计市政行业热力工程专业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A31704A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计市政行业道路工程专业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A31705A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计市政行业桥梁工程专业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A31706A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计市政行业城市隧道工程专业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A31707A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计市政行业公共交通工程专业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A31708A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计市政行业载人索道专业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A31709A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计市政行业轨道交通工程专业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A31710A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计市政行业环境卫生工程专业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A31711A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计农林行业农业综合开发生态工程专业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A31801A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计农林行业种植业工程专业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A31802A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计农林行业兽医/畜牧工程专业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A31803A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计农林行业渔港/渔业工程专业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A31804A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计农林行业设施农业工程专业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A31805A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计农林行业林产工业工程专业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A31806A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计农林行业林产化学工程专业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A31807A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计农林行业营造林工程专业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A31808A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计农林行业森林资源环境工程专业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A31809A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计农林行业森林工业工程专业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A31810A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计水利行业水库枢纽专业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A31901A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计水利行业引调水专业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A31902A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计水利行业灌溉排涝专业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A31903A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计水利行业河道整治专业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A31904A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计水利行业城市防洪专业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A31905A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计水利行业围垦专业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A31906A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计水利行业水土保持专业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A31907A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计水利行业水文设施专业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A31908A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计海洋行业沿岸工程专业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A32001A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计海洋行业离岸工程专业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A32002A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计海洋行业海水利用专业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A32003A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计建筑行业（建筑工程）甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A32101A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计建筑行业（人防工程）甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A32102A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计建筑设计事务所甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A401A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计结构设计事务所甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A402A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计机电设计事务所甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A403A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计建筑装饰工程专项甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A501A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计建筑智能化系统专项甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A502A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计建筑幕墙工程专项甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A503A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计轻型钢结构工程专项甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A504A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计风景园林工程专项甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A505A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计消防设施工程专项甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A506A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计环境工程专项（水污染防治工程）甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A50701A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计环境工程专项（大气污染防治工程）甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A50702A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计环境工程专项（固体废物处理处置工程）甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A50703A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计环境工程专项（物理污染防治工程）甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A50704A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计环境工程专项（污染修复工程）甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A50705A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程设计照明工程专项甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'A508A',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程勘察综合资质甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'B1A',
        'APT_TYPE': 'QY_ZZ_ZZZD_003',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '建筑智能化工程设计与施工一级',
        'APT_ISEND': '1',
        'APT_CODE': 'C1A',
        'APT_TYPE': 'QY_ZZ_ZZZD_005',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '消防设施工程设计与施工一级',
        'APT_ISEND': '1',
        'APT_CODE': 'C2A',
        'APT_TYPE': 'QY_ZZ_ZZZD_005',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '建筑装饰装修工程设计与施工一级',
        'APT_ISEND': '1',
        'APT_CODE': 'C3A',
        'APT_TYPE': 'QY_ZZ_ZZZD_005',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '建筑幕墙工程设计与施工一级',
        'APT_ISEND': '1',
        'APT_CODE': 'C4A',
        'APT_TYPE': 'QY_ZZ_ZZZD_005',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '建筑工程施工总承包一级',
        'APT_ISEND': '1',
        'APT_CODE': 'D101A',
        'APT_TYPE': 'QY_ZZ_ZZZD_001',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '公路工程施工总承包一级',
        'APT_ISEND': '1',
        'APT_CODE': 'D102A',
        'APT_TYPE': 'QY_ZZ_ZZZD_001',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '铁路工程施工总承包一级',
        'APT_ISEND': '1',
        'APT_CODE': 'D103A',
        'APT_TYPE': 'QY_ZZ_ZZZD_001',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '港口与航道工程施工总承包一级',
        'APT_ISEND': '1',
        'APT_CODE': 'D104A',
        'APT_TYPE': 'QY_ZZ_ZZZD_001',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '水利水电工程施工总承包一级',
        'APT_ISEND': '1',
        'APT_CODE': 'D105A',
        'APT_TYPE': 'QY_ZZ_ZZZD_001',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '电力工程施工总承包一级',
        'APT_ISEND': '1',
        'APT_CODE': 'D106A',
        'APT_TYPE': 'QY_ZZ_ZZZD_001',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '矿山工程施工总承包一级',
        'APT_ISEND': '1',
        'APT_CODE': 'D107A',
        'APT_TYPE': 'QY_ZZ_ZZZD_001',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '冶金工程施工总承包一级',
        'APT_ISEND': '1',
        'APT_CODE': 'D108A',
        'APT_TYPE': 'QY_ZZ_ZZZD_001',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '石油化工工程施工总承包一级',
        'APT_ISEND': '1',
        'APT_CODE': 'D109A',
        'APT_TYPE': 'QY_ZZ_ZZZD_001',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '市政公用工程施工总承包一级',
        'APT_ISEND': '1',
        'APT_CODE': 'D110A',
        'APT_TYPE': 'QY_ZZ_ZZZD_001',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '通信工程施工总承包一级',
        'APT_ISEND': '1',
        'APT_CODE': 'D111A',
        'APT_TYPE': 'QY_ZZ_ZZZD_001',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '机电工程施工总承包一级',
        'APT_ISEND': '1',
        'APT_CODE': 'D112A',
        'APT_TYPE': 'QY_ZZ_ZZZD_001',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '地基基础工程专业承包一级',
        'APT_ISEND': '1',
        'APT_CODE': 'D201A',
        'APT_TYPE': 'QY_ZZ_ZZZD_001',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '起重设备安装工程专业承包一级',
        'APT_ISEND': '1',
        'APT_CODE': 'D202A',
        'APT_TYPE': 'QY_ZZ_ZZZD_001',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '电子与智能化工程专业承包一级',
        'APT_ISEND': '1',
        'APT_CODE': 'D204A',
        'APT_TYPE': 'QY_ZZ_ZZZD_001',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '消防设施工程专业承包一级',
        'APT_ISEND': '1',
        'APT_CODE': 'D205A',
        'APT_TYPE': 'QY_ZZ_ZZZD_001',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '防水防腐保温工程专业承包一级',
        'APT_ISEND': '1',
        'APT_CODE': 'D206A',
        'APT_TYPE': 'QY_ZZ_ZZZD_001',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '桥梁工程专业承包一级',
        'APT_ISEND': '1',
        'APT_CODE': 'D207A',
        'APT_TYPE': 'QY_ZZ_ZZZD_001',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '隧道工程专业承包一级',
        'APT_ISEND': '1',
        'APT_CODE': 'D208A',
        'APT_TYPE': 'QY_ZZ_ZZZD_001',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '钢结构工程专业承包一级',
        'APT_ISEND': '1',
        'APT_CODE': 'D209A',
        'APT_TYPE': 'QY_ZZ_ZZZD_001',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '建筑装修装饰工程专业承包一级',
        'APT_ISEND': '1',
        'APT_CODE': 'D211A',
        'APT_TYPE': 'QY_ZZ_ZZZD_001',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '建筑机电安装工程专业承包一级',
        'APT_ISEND': '1',
        'APT_CODE': 'D212A',
        'APT_TYPE': 'QY_ZZ_ZZZD_001',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '建筑幕墙工程专业承包一级',
        'APT_ISEND': '1',
        'APT_CODE': 'D213A',
        'APT_TYPE': 'QY_ZZ_ZZZD_001',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '古建筑工程专业承包一级',
        'APT_ISEND': '1',
        'APT_CODE': 'D214A',
        'APT_TYPE': 'QY_ZZ_ZZZD_001',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '城市及道路照明工程专业承包一级',
        'APT_ISEND': '1',
        'APT_CODE': 'D215A',
        'APT_TYPE': 'QY_ZZ_ZZZD_001',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '公路路面工程专业承包一级',
        'APT_ISEND': '1',
        'APT_CODE': 'D216A',
        'APT_TYPE': 'QY_ZZ_ZZZD_001',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '公路路基工程专业承包一级',
        'APT_ISEND': '1',
        'APT_CODE': 'D217A',
        'APT_TYPE': 'QY_ZZ_ZZZD_001',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '公路交通工程（公路安全设施）专业承包一级',
        'APT_ISEND': '1',
        'APT_CODE': 'D21801A',
        'APT_TYPE': 'QY_ZZ_ZZZD_001',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '公路交通工程（公路机电工程）专业承包一级',
        'APT_ISEND': '1',
        'APT_CODE': 'D21802A',
        'APT_TYPE': 'QY_ZZ_ZZZD_001',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '公路交通工程专业承包一级',
        'APT_ISEND': '1',
        'APT_CODE': 'D218A',
        'APT_TYPE': 'QY_ZZ_ZZZD_001',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '铁路电务工程专业承包一级',
        'APT_ISEND': '1',
        'APT_CODE': 'D219A',
        'APT_TYPE': 'QY_ZZ_ZZZD_001',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '铁路铺轨架梁工程专业承包一级',
        'APT_ISEND': '1',
        'APT_CODE': 'D220A',
        'APT_TYPE': 'QY_ZZ_ZZZD_001',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '铁路电气化工程专业承包一级',
        'APT_ISEND': '1',
        'APT_CODE': 'D221A',
        'APT_TYPE': 'QY_ZZ_ZZZD_001',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '机场场道工程专业承包一级',
        'APT_ISEND': '1',
        'APT_CODE': 'D222A',
        'APT_TYPE': 'QY_ZZ_ZZZD_001',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '民航空管工程及机场弱电系统工程专业承包一级',
        'APT_ISEND': '1',
        'APT_CODE': 'D223A',
        'APT_TYPE': 'QY_ZZ_ZZZD_001',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '机场目视助航工程专业承包一级',
        'APT_ISEND': '1',
        'APT_CODE': 'D224A',
        'APT_TYPE': 'QY_ZZ_ZZZD_001',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '港口与海岸工程专业承包一级',
        'APT_ISEND': '1',
        'APT_CODE': 'D225A',
        'APT_TYPE': 'QY_ZZ_ZZZD_001',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '航道工程专业承包一级',
        'APT_ISEND': '1',
        'APT_CODE': 'D226A',
        'APT_TYPE': 'QY_ZZ_ZZZD_001',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '通航建筑物工程专业承包一级',
        'APT_ISEND': '1',
        'APT_CODE': 'D227A',
        'APT_TYPE': 'QY_ZZ_ZZZD_001',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '港航设备安装及水上交管工程专业承包一级',
        'APT_ISEND': '1',
        'APT_CODE': 'D228A',
        'APT_TYPE': 'QY_ZZ_ZZZD_001',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '水工金属结构制作与安装工程专业承包一级',
        'APT_ISEND': '1',
        'APT_CODE': 'D229A',
        'APT_TYPE': 'QY_ZZ_ZZZD_001',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '水利水电机电安装工程专业承包一级',
        'APT_ISEND': '1',
        'APT_CODE': 'D230A',
        'APT_TYPE': 'QY_ZZ_ZZZD_001',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '河湖整治工程专业承包一级',
        'APT_ISEND': '1',
        'APT_CODE': 'D231A',
        'APT_TYPE': 'QY_ZZ_ZZZD_001',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '输变电工程专业承包一级',
        'APT_ISEND': '1',
        'APT_CODE': 'D232A',
        'APT_TYPE': 'QY_ZZ_ZZZD_001',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '核工程专业承包一级',
        'APT_ISEND': '1',
        'APT_CODE': 'D233A',
        'APT_TYPE': 'QY_ZZ_ZZZD_001',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '海洋石油工程专业承包一级',
        'APT_ISEND': '1',
        'APT_CODE': 'D234A',
        'APT_TYPE': 'QY_ZZ_ZZZD_001',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '环保工程专业承包一级',
        'APT_ISEND': '1',
        'APT_CODE': 'D235A',
        'APT_TYPE': 'QY_ZZ_ZZZD_001',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程监理综合资质',
        'APT_ISEND': '1',
        'APT_CODE': 'E1X',
        'APT_TYPE': 'QY_ZZ_ZZZD_002',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程监理房屋建筑工程专业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'E201A',
        'APT_TYPE': 'QY_ZZ_ZZZD_002',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程监理冶炼工程专业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'E202A',
        'APT_TYPE': 'QY_ZZ_ZZZD_002',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程监理矿山工程专业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'E203A',
        'APT_TYPE': 'QY_ZZ_ZZZD_002',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程监理化工石油工程专业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'E204A',
        'APT_TYPE': 'QY_ZZ_ZZZD_002',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程监理水利水电工程专业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'E205A',
        'APT_TYPE': 'QY_ZZ_ZZZD_002',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程监理电力工程专业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'E206A',
        'APT_TYPE': 'QY_ZZ_ZZZD_002',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程监理农林工程专业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'E207A',
        'APT_TYPE': 'QY_ZZ_ZZZD_002',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程监理铁路工程专业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'E208A',
        'APT_TYPE': 'QY_ZZ_ZZZD_002',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程监理公路工程专业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'E209A',
        'APT_TYPE': 'QY_ZZ_ZZZD_002',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程监理港口与航道工程专业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'E210A',
        'APT_TYPE': 'QY_ZZ_ZZZD_002',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程监理航天航空工程专业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'E211A',
        'APT_TYPE': 'QY_ZZ_ZZZD_002',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程监理通信工程专业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'E212A',
        'APT_TYPE': 'QY_ZZ_ZZZD_002',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程监理市政公用工程专业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'E213A',
        'APT_TYPE': 'QY_ZZ_ZZZD_002',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程监理机电安装工程专业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'E214A',
        'APT_TYPE': 'QY_ZZ_ZZZD_002',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程招标代理甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'FA',
        'APT_TYPE': 'QY_ZZ_ZZZD_006',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 1,
        'APT_CASENAME': '工程造价咨询甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'IA',
        'APT_TYPE': 'QY_ZZ_ZZZD_007',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程设计煤炭行业乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A201B',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程设计化工石化医药行业乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A202B',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程设计石油天然气（海洋石油）行业乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A203B',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程设计电力行业乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A204B',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程设计冶金行业乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A205B',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程设计军工行业乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A206B',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程设计机械行业乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A207B',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程设计商物粮行业乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A208B',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程设计电子通信广电行业（电子工程）乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A21001B',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程设计电子通信广电行业（通信工程）乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A21002B',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程设计电子通信广电行业（广电工程）乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A21003B',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程设计轻纺行业（轻工工程）乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A21101B',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程设计轻纺行业（纺织工程）乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A21102B',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程设计建材行业乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A212B',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程设计铁道行业乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A213B',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程设计水运行业乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A215B',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程设计民航行业乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A216B',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程设计市政行业（燃气工程、轨道交通工程除外）乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A21701B',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程设计市政行业乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A217B',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程设计农林行业（农业工程）乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A21801B',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程设计农林行业（林业工程）乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A21802B',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程设计水利行业乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A219B',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程设计海洋行业乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A220B',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程设计建筑行业乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A221B',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程设计煤炭行业矿井专业乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A30101B',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程设计煤炭行业露天矿专业乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A30102B',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程设计煤炭行业选煤厂专业乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A30103B',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程设计化工石化医药行业炼油工程专业乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A30201B',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程设计化工石化医药行业化工工程专业乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A30202B',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程设计化工石化医药行业石油及化工产品储运专业乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A30203B',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程设计化工石化医药行业化工矿山专业乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A30204B',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程设计化工石化医药行业生化、生物药专业乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A30205B',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程设计化工石化医药行业中成药专业乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A30206B',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程设计化工石化医药行业化学原料药专业乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A30207B',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程设计化工石化医药行业药物制剂专业乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A30208B',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程设计化工石化医药行业医疗器械（含药品内包装）专业乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A30209B',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程设计石油天然气（海洋石油）行业油田地面专业乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A30301B',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程设计石油天然气（海洋石油）行业气田地面专业乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A30302B',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程设计石油天然气（海洋石油）行业管道输送专业乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A30303B',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程设计石油天然气（海洋石油）行业海洋石油专业乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A30304B',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程设计石油天然气（海洋石油）行业油气库专业乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A30305B',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程设计石油天然气（海洋石油）行业油气加工专业乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A30306B',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程设计石油天然气（海洋石油）行业石油机械制造与修理专业乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A30307B',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程设计电力行业火力发电（含核电站常规岛设计）专业乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A30401B',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程设计电力行业水力发电（含抽水蓄能、潮汐）专业乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A30402B',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程设计电力行业风力发电专业乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A30403B',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程设计电力行业新能源发电专业乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A30404B',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程设计电力行业送电工程专业乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A30405B',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程设计电力行业变电工程专业乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A30406B',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程设计冶金行业金属冶炼工程专业乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A30501B',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程设计冶金行业金属材料工程专业乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A30502B',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程设计冶金行业焦化和耐火材料工程专业乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A30503B',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程设计冶金行业冶金矿山工程专业乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A30504B',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程设计军工行业导弹及火箭弹工程专业乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A30601B',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程设计军工行业弹、火工品及固体发动机工程专业乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A30602B',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程设计军工行业燃机、动力装置及航天发动机工程专业乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A30603B',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程设计军工行业控制系统、光学、光电、电子、仪表工程专业乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A30604B',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程设计军工行业科研、靶场、试验、教育培训工程专业乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A30605B',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程设计军工行业地面设备工程专业乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A30606B',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程设计军工行业航天空间飞行器工程专业乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A30607B',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程设计军工行业运载火箭制造工程专业乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A30608B',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程设计军工行业地面制导站工程专业乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A30609B',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程设计军工行业航空飞行器工程专业乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A30610B',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程设计军工行业机场工程专业乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A30611B',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程设计军工行业船舶制造工程专业乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A30612B',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程设计军工行业船舶机械工程专业乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A30613B',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程设计军工行业船舶水工工程专业乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A30614B',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程设计军工行业坦克、装甲车辆工程专业乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A30615B',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程设计军工行业枪、炮工程专业乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A30616B',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程设计军工行业火、炸药工程专业乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A30617B',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程设计军工行业防化、民爆器材工程专业乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A30618B',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程设计机械行业通用设备制造业工程专业乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A30701B',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程设计机械行业专用设备制造业工程专业乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A30702B',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程设计机械行业交通运输设备制造业工程专业乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A30703B',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程设计机械行业电气机械设备制造业工程专业乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A30704B',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程设计机械行业金属制品业工程专业乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A30705B',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程设计机械行业仪器仪表及文化办公机械制造业工程专业乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A30706B',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程设计机械行业机械加工专业乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A30707B',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程设计机械行业热加工专业乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A30708B',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程设计机械行业表面处理专业乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A30709B',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程设计机械行业检测专业乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A30710B',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程设计机械行业物料搬运及仓储专业乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A30711B',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程设计商物粮行业冷冻冷藏工程专业乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A30801B',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程设计商物粮行业肉食品加工工程专业乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A30802B',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程设计商物粮行业批发配送与物流仓储工程专业乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A30803B',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程设计商物粮行业成品油储运工程专业乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A30804B',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程设计商物粮行业粮食工程专业乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A30805B',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程设计商物粮行业油脂工程专业乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A30806B',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程设计核工业行业核燃料加工制造及处理工程专业乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A30902B',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程设计核工业行业铀矿山及选冶工程专业乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A30903B',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程设计核工业行业核设施退役及放射性三废处理处置工程专业乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A30904B',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程设计核工业行业核技术及同位素应用工程专业乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A30905B',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程设计电子通信广电行业电子整机产品项目工程专业乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A31001B',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程设计电子通信广电行业电子基础产品项目工程专业乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A31002B',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程设计电子通信广电行业显示器件项目工程专业乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A31003B',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程设计电子通信广电行业微电子产品项目工程专业乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A31004B',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程设计电子通信广电行业电子特种环境工程专业乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A31005B',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程设计电子通信广电行业电子系统工程专业乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A31006B',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程设计电子通信广电行业有线通信专业乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A31007B',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程设计电子通信广电行业无线通信专业乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A31008B',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程设计电子通信广电行业邮政工程专业乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A31009B',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程设计电子通信广电行业通信铁塔专业乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A31010B',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程设计电子通信广电行业广播电视中心专业乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A31011B',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程设计电子通信广电行业广播电视发射专业乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A31012B',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程设计电子通信广电行业广播电视传输专业乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A31013B',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程设计电子通信广电行业电影工程专业乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A31014B',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程设计轻纺行业制浆造纸工程专业乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A31101B',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程设计轻纺行业食品发酵烟草工程专业乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A31102B',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程设计轻纺行业制糖工程专业乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A31103B',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程设计轻纺行业日化及塑料工程专业乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A31104B',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程设计轻纺行业日用硅酸盐工程专业乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A31105B',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程设计轻纺行业制盐及盐化工程专业乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A31106B',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程设计轻纺行业皮革毛皮及制品专业乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A31107B',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程设计轻纺行业家电电子及日用机械专业乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A31108B',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程设计轻纺行业纺织工程专业乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A31109B',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程设计轻纺行业印染工程专业乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A31110B',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程设计轻纺行业服装工程专业乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A31111B',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程设计轻纺行业化纤原料工程专业乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A31112B',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程设计轻纺行业化纤工程专业乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A31113B',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程设计建材行业水泥工程专业乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A31201B',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程设计建材行业玻璃、陶瓷、耐火材料工程专业乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A31202B',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程设计建材行业新型建筑材料工程专业乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A31203B',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程设计建材行业非金属矿及原料制备工程专业乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A31204B',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程设计建材行业无机非金属材料及制品工程专业乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A31205B',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程设计公路行业公路专业乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A31401B',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程设计公路行业交通工程专业乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A31404B',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程设计水运行业港口工程专业乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A31501B',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程设计水运行业航道工程专业乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A31502B',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程设计水运行业通航建筑工程专业乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A31503B',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程设计水运行业修造船厂水工工程专业乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A31504B',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程设计水运行业港口装卸工艺专业乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A31505B',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程设计水运行业水上交通管制工程专业乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A31506B',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程设计市政行业给水工程专业乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A31701B',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程设计市政行业排水工程专业乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A31702B',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程设计市政行业城镇燃气工程专业乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A31703B',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程设计市政行业热力工程专业乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A31704B',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程设计市政行业道路工程专业乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A31705B',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程设计市政行业桥梁工程专业乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A31706B',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程设计市政行业公共交通工程专业乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A31708B',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程设计市政行业环境卫生工程专业乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A31711B',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程设计农林行业农业综合开发生态工程专业乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A31801B',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程设计农林行业种植业工程专业乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A31802B',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程设计农林行业兽医/畜牧工程专业乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A31803B',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程设计农林行业渔港/渔业工程专业乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A31804B',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程设计农林行业设施农业工程专业乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A31805B',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程设计农林行业林产工业工程专业乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A31806B',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程设计农林行业林产化学工程专业乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A31807B',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程设计农林行业营造林工程专业乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A31808B',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程设计农林行业营造林工程专业丙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A31808C',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程设计农林行业森林资源环境工程专业乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A31809B',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程设计农林行业森林工业工程专业乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A31810B',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程设计水利行业水库枢纽专业乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A31901B',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程设计水利行业引调水专业乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A31902B',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程设计水利行业灌溉排涝专业乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A31903B',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程设计水利行业河道整治专业乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A31904B',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程设计水利行业城市防洪专业乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A31905B',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程设计水利行业围垦专业乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A31906B',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程设计水利行业水土保持专业乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A31907B',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程设计水利行业水文设施专业乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A31908B',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程设计海洋行业沿岸工程专业乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A32001B',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程设计海洋行业离岸工程专业乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A32002B',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程设计海洋行业海水利用专业乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A32003B',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程设计海洋行业海洋能利用专业乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A32004B',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程设计建筑行业（建筑工程）乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A32101B',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程设计建筑行业（人防工程）乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A32102B',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程设计建筑装饰工程专项乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A501B',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程设计建筑智能化系统专项乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A502B',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程设计建筑幕墙工程专项乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A503B',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程设计轻型钢结构工程专项乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A504B',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程设计风景园林工程专项乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A505B',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程设计消防设施工程专项乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A506B',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程设计环境工程专项（水污染防治工程）乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A50701B',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程设计环境工程专项（大气污染防治工程）乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A50702B',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程设计环境工程专项（固体废物处理处置工程）乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A50703B',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程设计环境工程专项（物理污染防治工程）乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A50704B',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程设计环境工程专项（污染修复工程）乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A50705B',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程设计照明工程专项乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A508B',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程勘察岩土工程专业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'B203A',
        'APT_TYPE': 'QY_ZZ_ZZZD_003',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程勘察岩土工程专业乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'B203B',
        'APT_TYPE': 'QY_ZZ_ZZZD_003',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '建筑智能化工程设计与施工二级',
        'APT_ISEND': '1',
        'APT_CODE': 'C1B',
        'APT_TYPE': 'QY_ZZ_ZZZD_005',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '消防设施工程设计与施工二级',
        'APT_ISEND': '1',
        'APT_CODE': 'C2B',
        'APT_TYPE': 'QY_ZZ_ZZZD_005',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '建筑装饰装修工程设计与施工二级',
        'APT_ISEND': '1',
        'APT_CODE': 'C3B',
        'APT_TYPE': 'QY_ZZ_ZZZD_005',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '建筑幕墙工程设计与施工二级',
        'APT_ISEND': '1',
        'APT_CODE': 'C4B',
        'APT_TYPE': 'QY_ZZ_ZZZD_005',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '建筑工程施工总承包二级',
        'APT_ISEND': '1',
        'APT_CODE': 'D101B',
        'APT_TYPE': 'QY_ZZ_ZZZD_001',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '公路工程施工总承包二级',
        'APT_ISEND': '1',
        'APT_CODE': 'D102B',
        'APT_TYPE': 'QY_ZZ_ZZZD_001',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '铁路工程施工总承包二级',
        'APT_ISEND': '1',
        'APT_CODE': 'D103B',
        'APT_TYPE': 'QY_ZZ_ZZZD_001',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '港口与航道工程施工总承包二级',
        'APT_ISEND': '1',
        'APT_CODE': 'D104B',
        'APT_TYPE': 'QY_ZZ_ZZZD_001',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '水利水电工程施工总承包二级',
        'APT_ISEND': '1',
        'APT_CODE': 'D105B',
        'APT_TYPE': 'QY_ZZ_ZZZD_001',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '电力工程施工总承包二级',
        'APT_ISEND': '1',
        'APT_CODE': 'D106B',
        'APT_TYPE': 'QY_ZZ_ZZZD_001',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '矿山工程施工总承包二级',
        'APT_ISEND': '1',
        'APT_CODE': 'D107B',
        'APT_TYPE': 'QY_ZZ_ZZZD_001',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '冶金工程施工总承包二级',
        'APT_ISEND': '1',
        'APT_CODE': 'D108B',
        'APT_TYPE': 'QY_ZZ_ZZZD_001',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '石油化工工程施工总承包二级',
        'APT_ISEND': '1',
        'APT_CODE': 'D109B',
        'APT_TYPE': 'QY_ZZ_ZZZD_001',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '市政公用工程施工总承包二级',
        'APT_ISEND': '1',
        'APT_CODE': 'D110B',
        'APT_TYPE': 'QY_ZZ_ZZZD_001',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '通信工程施工总承包二级',
        'APT_ISEND': '1',
        'APT_CODE': 'D111B',
        'APT_TYPE': 'QY_ZZ_ZZZD_001',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '机电工程施工总承包二级',
        'APT_ISEND': '1',
        'APT_CODE': 'D112B',
        'APT_TYPE': 'QY_ZZ_ZZZD_001',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '地基基础工程专业承包二级',
        'APT_ISEND': '1',
        'APT_CODE': 'D201B',
        'APT_TYPE': 'QY_ZZ_ZZZD_001',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '起重设备安装工程专业承包二级',
        'APT_ISEND': '1',
        'APT_CODE': 'D202B',
        'APT_TYPE': 'QY_ZZ_ZZZD_001',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '电子与智能化工程专业承包二级',
        'APT_ISEND': '1',
        'APT_CODE': 'D204B',
        'APT_TYPE': 'QY_ZZ_ZZZD_001',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '消防设施工程专业承包二级',
        'APT_ISEND': '1',
        'APT_CODE': 'D205B',
        'APT_TYPE': 'QY_ZZ_ZZZD_001',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '防水防腐保温工程专业承包二级',
        'APT_ISEND': '1',
        'APT_CODE': 'D206B',
        'APT_TYPE': 'QY_ZZ_ZZZD_001',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '桥梁工程专业承包二级',
        'APT_ISEND': '1',
        'APT_CODE': 'D207B',
        'APT_TYPE': 'QY_ZZ_ZZZD_001',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '隧道工程专业承包二级',
        'APT_ISEND': '1',
        'APT_CODE': 'D208B',
        'APT_TYPE': 'QY_ZZ_ZZZD_001',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '钢结构工程专业承包二级',
        'APT_ISEND': '1',
        'APT_CODE': 'D209B',
        'APT_TYPE': 'QY_ZZ_ZZZD_001',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '建筑装修装饰工程专业承包二级',
        'APT_ISEND': '1',
        'APT_CODE': 'D211B',
        'APT_TYPE': 'QY_ZZ_ZZZD_001',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '建筑机电安装工程专业承包二级',
        'APT_ISEND': '1',
        'APT_CODE': 'D212B',
        'APT_TYPE': 'QY_ZZ_ZZZD_001',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '建筑幕墙工程专业承包二级',
        'APT_ISEND': '1',
        'APT_CODE': 'D213B',
        'APT_TYPE': 'QY_ZZ_ZZZD_001',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '古建筑工程专业承包二级',
        'APT_ISEND': '1',
        'APT_CODE': 'D214B',
        'APT_TYPE': 'QY_ZZ_ZZZD_001',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '城市及道路照明工程专业承包二级',
        'APT_ISEND': '1',
        'APT_CODE': 'D215B',
        'APT_TYPE': 'QY_ZZ_ZZZD_001',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '公路路面工程专业承包三级',
        'APT_ISEND': '1',
        'APT_CODE': 'D216C',
        'APT_TYPE': 'QY_ZZ_ZZZD_001',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '公路路基工程专业承包二级',
        'APT_ISEND': '1',
        'APT_CODE': 'D217B',
        'APT_TYPE': 'QY_ZZ_ZZZD_001',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '公路交通工程（公路安全设施）专业承包二级',
        'APT_ISEND': '1',
        'APT_CODE': 'D21801B',
        'APT_TYPE': 'QY_ZZ_ZZZD_001',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '公路交通工程（公路机电工程）专业承包二级',
        'APT_ISEND': '1',
        'APT_CODE': 'D21802B',
        'APT_TYPE': 'QY_ZZ_ZZZD_001',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '公路交通工程专业承包二级',
        'APT_ISEND': '1',
        'APT_CODE': 'D218B',
        'APT_TYPE': 'QY_ZZ_ZZZD_001',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '铁路电务工程专业承包二级',
        'APT_ISEND': '1',
        'APT_CODE': 'D219B',
        'APT_TYPE': 'QY_ZZ_ZZZD_001',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '铁路铺轨架梁工程专业承包二级',
        'APT_ISEND': '1',
        'APT_CODE': 'D220B',
        'APT_TYPE': 'QY_ZZ_ZZZD_001',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '铁路电气化工程专业承包二级',
        'APT_ISEND': '1',
        'APT_CODE': 'D221B',
        'APT_TYPE': 'QY_ZZ_ZZZD_001',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '机场场道工程专业承包二级',
        'APT_ISEND': '1',
        'APT_CODE': 'D222B',
        'APT_TYPE': 'QY_ZZ_ZZZD_001',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '民航空管工程及机场弱电系统工程专业承包二级',
        'APT_ISEND': '1',
        'APT_CODE': 'D223B',
        'APT_TYPE': 'QY_ZZ_ZZZD_001',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '机场目视助航工程专业承包二级',
        'APT_ISEND': '1',
        'APT_CODE': 'D224B',
        'APT_TYPE': 'QY_ZZ_ZZZD_001',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '港口与海岸工程专业承包二级',
        'APT_ISEND': '1',
        'APT_CODE': 'D225B',
        'APT_TYPE': 'QY_ZZ_ZZZD_001',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '航道工程专业承包二级',
        'APT_ISEND': '1',
        'APT_CODE': 'D226B',
        'APT_TYPE': 'QY_ZZ_ZZZD_001',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '通航建筑物工程专业承包二级',
        'APT_ISEND': '1',
        'APT_CODE': 'D227B',
        'APT_TYPE': 'QY_ZZ_ZZZD_001',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '港航设备安装及水上交管工程专业承包二级',
        'APT_ISEND': '1',
        'APT_CODE': 'D228B',
        'APT_TYPE': 'QY_ZZ_ZZZD_001',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '水工金属结构制作与安装工程专业承包二级',
        'APT_ISEND': '1',
        'APT_CODE': 'D229B',
        'APT_TYPE': 'QY_ZZ_ZZZD_001',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '水利水电机电安装工程专业承包二级',
        'APT_ISEND': '1',
        'APT_CODE': 'D230B',
        'APT_TYPE': 'QY_ZZ_ZZZD_001',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '河湖整治工程专业承包二级',
        'APT_ISEND': '1',
        'APT_CODE': 'D231B',
        'APT_TYPE': 'QY_ZZ_ZZZD_001',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '输变电工程专业承包二级',
        'APT_ISEND': '1',
        'APT_CODE': 'D232B',
        'APT_TYPE': 'QY_ZZ_ZZZD_001',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '核工程专业承包二级',
        'APT_ISEND': '1',
        'APT_CODE': 'D233B',
        'APT_TYPE': 'QY_ZZ_ZZZD_001',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '海洋石油工程专业承包二级',
        'APT_ISEND': '1',
        'APT_CODE': 'D234B',
        'APT_TYPE': 'QY_ZZ_ZZZD_001',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '环保工程专业承包二级',
        'APT_ISEND': '1',
        'APT_CODE': 'D235B',
        'APT_TYPE': 'QY_ZZ_ZZZD_001',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程监理房屋建筑工程专业乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'E201B',
        'APT_TYPE': 'QY_ZZ_ZZZD_002',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程监理冶炼工程专业乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'E202B',
        'APT_TYPE': 'QY_ZZ_ZZZD_002',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程监理矿山工程专业乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'E203B',
        'APT_TYPE': 'QY_ZZ_ZZZD_002',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程监理化工石油工程专业乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'E204B',
        'APT_TYPE': 'QY_ZZ_ZZZD_002',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程监理水利水电工程专业乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'E205B',
        'APT_TYPE': 'QY_ZZ_ZZZD_002',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程监理电力工程专业乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'E206B',
        'APT_TYPE': 'QY_ZZ_ZZZD_002',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程监理农林工程专业乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'E207B',
        'APT_TYPE': 'QY_ZZ_ZZZD_002',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程监理铁路工程专业乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'E208B',
        'APT_TYPE': 'QY_ZZ_ZZZD_002',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程监理公路工程专业乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'E209B',
        'APT_TYPE': 'QY_ZZ_ZZZD_002',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程监理港口与航道工程专业乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'E210B',
        'APT_TYPE': 'QY_ZZ_ZZZD_002',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程监理航天航空工程专业乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'E211B',
        'APT_TYPE': 'QY_ZZ_ZZZD_002',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程监理通信工程专业乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'E212B',
        'APT_TYPE': 'QY_ZZ_ZZZD_002',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程监理市政公用工程专业乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'E213B',
        'APT_TYPE': 'QY_ZZ_ZZZD_002',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程监理机电安装工程专业乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'E214B',
        'APT_TYPE': 'QY_ZZ_ZZZD_002',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程招标代理乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'FB',
        'APT_TYPE': 'QY_ZZ_ZZZD_006',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 2,
        'APT_CASENAME': '工程造价咨询乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'IB',
        'APT_TYPE': 'QY_ZZ_ZZZD_007',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 3,
        'APT_CASENAME': '工程设计水利行业丙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A219C',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 3,
        'APT_CASENAME': '工程设计电力行业送电工程专业丙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A30405C',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 3,
        'APT_CASENAME': '工程设计电力行业变电工程专业丙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A30406C',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 3,
        'APT_CASENAME': '工程设计公路行业公路专业丙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A31401C',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 3,
        'APT_CASENAME': '工程设计市政行业给水工程专业丙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A31701C',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 3,
        'APT_CASENAME': '工程设计市政行业排水工程专业丙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A31702C',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 3,
        'APT_CASENAME': '工程设计市政行业城镇燃气工程专业丙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A31703C',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 3,
        'APT_CASENAME': '工程设计市政行业热力工程专业丙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A31704C',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 3,
        'APT_CASENAME': '工程设计市政行业道路工程专业丙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A31705C',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 3,
        'APT_CASENAME': '工程设计市政行业环境卫生工程专业丙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A31711C',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 3,
        'APT_CASENAME': '工程设计水利行业水库枢纽专业丙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A31901C',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 3,
        'APT_CASENAME': '工程设计水利行业引调水专业丙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A31902C',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 3,
        'APT_CASENAME': '工程设计水利行业灌溉排涝专业丙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A31903C',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 3,
        'APT_CASENAME': '工程设计水利行业河道整治专业丙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A31904C',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 3,
        'APT_CASENAME': '工程设计水利行业城市防洪专业丙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A31905C',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 3,
        'APT_CASENAME': '工程设计水利行业围垦专业丙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A31906C',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 3,
        'APT_CASENAME': '工程设计水利行业水土保持专业丙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A31907C',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 3,
        'APT_CASENAME': '工程设计建筑行业（建筑工程）丙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A32101C',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 3,
        'APT_CASENAME': '工程设计建筑装饰工程专项丙级',
        'APT_ISEND': '1',
        'APT_CODE': 'A501C',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 3,
        'APT_CASENAME': '工程勘察岩土工程专业（岩土工程勘察）甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'B20301A',
        'APT_TYPE': 'QY_ZZ_ZZZD_003',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 3,
        'APT_CASENAME': '工程勘察岩土工程专业（岩土工程勘察）乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'B20301B',
        'APT_TYPE': 'QY_ZZ_ZZZD_003',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 3,
        'APT_CASENAME': '工程勘察岩土工程专业（岩土工程勘察）丙级',
        'APT_ISEND': '1',
        'APT_CODE': 'B20301C',
        'APT_TYPE': 'QY_ZZ_ZZZD_003',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 3,
        'APT_CASENAME': '工程勘察岩土工程专业（岩土工程设计）甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'B20302A',
        'APT_TYPE': 'QY_ZZ_ZZZD_003',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 3,
        'APT_CASENAME': '工程勘察岩土工程专业（岩土工程设计）乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'B20302B',
        'APT_TYPE': 'QY_ZZ_ZZZD_003',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 3,
        'APT_CASENAME': '工程勘察岩土工程专业（岩土工程物探测试检测监测）甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'B20303A',
        'APT_TYPE': 'QY_ZZ_ZZZD_003',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 3,
        'APT_CASENAME': '工程勘察岩土工程专业（岩土工程物探测试检测监测）乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'B20303B',
        'APT_TYPE': 'QY_ZZ_ZZZD_003',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 3,
        'APT_CASENAME': '建筑装饰装修工程设计与施工三级',
        'APT_ISEND': '1',
        'APT_CODE': 'C3C',
        'APT_TYPE': 'QY_ZZ_ZZZD_005',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 3,
        'APT_CASENAME': '建筑工程施工总承包三级',
        'APT_ISEND': '1',
        'APT_CODE': 'D101C',
        'APT_TYPE': 'QY_ZZ_ZZZD_001',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 3,
        'APT_CASENAME': '公路工程施工总承包三级',
        'APT_ISEND': '1',
        'APT_CODE': 'D102C',
        'APT_TYPE': 'QY_ZZ_ZZZD_001',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 3,
        'APT_CASENAME': '铁路工程施工总承包三级',
        'APT_ISEND': '1',
        'APT_CODE': 'D103C',
        'APT_TYPE': 'QY_ZZ_ZZZD_001',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 3,
        'APT_CASENAME': '港口与航道工程施工总承包三级',
        'APT_ISEND': '1',
        'APT_CODE': 'D104C',
        'APT_TYPE': 'QY_ZZ_ZZZD_001',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 3,
        'APT_CASENAME': '水利水电工程施工总承包三级',
        'APT_ISEND': '1',
        'APT_CODE': 'D105C',
        'APT_TYPE': 'QY_ZZ_ZZZD_001',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 3,
        'APT_CASENAME': '电力工程施工总承包三级',
        'APT_ISEND': '1',
        'APT_CODE': 'D106C',
        'APT_TYPE': 'QY_ZZ_ZZZD_001',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 3,
        'APT_CASENAME': '矿山工程施工总承包三级',
        'APT_ISEND': '1',
        'APT_CODE': 'D107C',
        'APT_TYPE': 'QY_ZZ_ZZZD_001',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 3,
        'APT_CASENAME': '冶金工程施工总承包三级',
        'APT_ISEND': '1',
        'APT_CODE': 'D108C',
        'APT_TYPE': 'QY_ZZ_ZZZD_001',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 3,
        'APT_CASENAME': '石油化工工程施工总承包三级',
        'APT_ISEND': '1',
        'APT_CODE': 'D109C',
        'APT_TYPE': 'QY_ZZ_ZZZD_001',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 3,
        'APT_CASENAME': '市政公用工程施工总承包三级',
        'APT_ISEND': '1',
        'APT_CODE': 'D110C',
        'APT_TYPE': 'QY_ZZ_ZZZD_001',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 3,
        'APT_CASENAME': '通信工程施工总承包三级',
        'APT_ISEND': '1',
        'APT_CODE': 'D111C',
        'APT_TYPE': 'QY_ZZ_ZZZD_001',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 3,
        'APT_CASENAME': '机电工程施工总承包三级',
        'APT_ISEND': '1',
        'APT_CODE': 'D112C',
        'APT_TYPE': 'QY_ZZ_ZZZD_001',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 3,
        'APT_CASENAME': '地基基础工程专业承包三级',
        'APT_ISEND': '1',
        'APT_CODE': 'D201C',
        'APT_TYPE': 'QY_ZZ_ZZZD_001',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 3,
        'APT_CASENAME': '起重设备安装工程专业承包三级',
        'APT_ISEND': '1',
        'APT_CODE': 'D202C',
        'APT_TYPE': 'QY_ZZ_ZZZD_001',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 3,
        'APT_CASENAME': '桥梁工程专业承包三级',
        'APT_ISEND': '1',
        'APT_CODE': 'D207C',
        'APT_TYPE': 'QY_ZZ_ZZZD_001',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 3,
        'APT_CASENAME': '隧道工程专业承包三级',
        'APT_ISEND': '1',
        'APT_CODE': 'D208C',
        'APT_TYPE': 'QY_ZZ_ZZZD_001',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 3,
        'APT_CASENAME': '钢结构工程专业承包三级',
        'APT_ISEND': '1',
        'APT_CODE': 'D209C',
        'APT_TYPE': 'QY_ZZ_ZZZD_001',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 3,
        'APT_CASENAME': '建筑机电安装工程专业承包三级',
        'APT_ISEND': '1',
        'APT_CODE': 'D212C',
        'APT_TYPE': 'QY_ZZ_ZZZD_001',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 3,
        'APT_CASENAME': '古建筑工程专业承包三级',
        'APT_ISEND': '1',
        'APT_CODE': 'D214C',
        'APT_TYPE': 'QY_ZZ_ZZZD_001',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 3,
        'APT_CASENAME': '城市及道路照明工程专业承包三级',
        'APT_ISEND': '1',
        'APT_CODE': 'D215C',
        'APT_TYPE': 'QY_ZZ_ZZZD_001',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 3,
        'APT_CASENAME': '公路路面工程专业承包二级',
        'APT_ISEND': '1',
        'APT_CODE': 'D216B',
        'APT_TYPE': 'QY_ZZ_ZZZD_001',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 3,
        'APT_CASENAME': '公路路基工程专业承包三级',
        'APT_ISEND': '1',
        'APT_CODE': 'D217C',
        'APT_TYPE': 'QY_ZZ_ZZZD_001',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 3,
        'APT_CASENAME': '铁路电务工程专业承包三级',
        'APT_ISEND': '1',
        'APT_CODE': 'D219C',
        'APT_TYPE': 'QY_ZZ_ZZZD_001',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 3,
        'APT_CASENAME': '铁路电气化工程专业承包三级',
        'APT_ISEND': '1',
        'APT_CODE': 'D221C',
        'APT_TYPE': 'QY_ZZ_ZZZD_001',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 3,
        'APT_CASENAME': '港口与海岸工程专业承包三级',
        'APT_ISEND': '1',
        'APT_CODE': 'D225C',
        'APT_TYPE': 'QY_ZZ_ZZZD_001',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 3,
        'APT_CASENAME': '航道工程专业承包三级',
        'APT_ISEND': '1',
        'APT_CODE': 'D226C',
        'APT_TYPE': 'QY_ZZ_ZZZD_001',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 3,
        'APT_CASENAME': '通航建筑物工程专业承包三级',
        'APT_ISEND': '1',
        'APT_CODE': 'D227C',
        'APT_TYPE': 'QY_ZZ_ZZZD_001',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 3,
        'APT_CASENAME': '水工金属结构制作与安装工程专业承包三级',
        'APT_ISEND': '1',
        'APT_CODE': 'D229C',
        'APT_TYPE': 'QY_ZZ_ZZZD_001',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 3,
        'APT_CASENAME': '水利水电机电安装工程专业承包三级',
        'APT_ISEND': '1',
        'APT_CODE': 'D230C',
        'APT_TYPE': 'QY_ZZ_ZZZD_001',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 3,
        'APT_CASENAME': '河湖整治工程专业承包三级',
        'APT_ISEND': '1',
        'APT_CODE': 'D231C',
        'APT_TYPE': 'QY_ZZ_ZZZD_001',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 3,
        'APT_CASENAME': '输变电工程专业承包三级',
        'APT_ISEND': '1',
        'APT_CODE': 'D232C',
        'APT_TYPE': 'QY_ZZ_ZZZD_001',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 3,
        'APT_CASENAME': '环保工程专业承包三级',
        'APT_ISEND': '1',
        'APT_CODE': 'D235C',
        'APT_TYPE': 'QY_ZZ_ZZZD_001',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 3,
        'APT_CASENAME': '工程监理房屋建筑工程专业丙级',
        'APT_ISEND': '1',
        'APT_CODE': 'E201C',
        'APT_TYPE': 'QY_ZZ_ZZZD_002',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 3,
        'APT_CASENAME': '工程监理水利水电工程专业丙级',
        'APT_ISEND': '1',
        'APT_CODE': 'E205C',
        'APT_TYPE': 'QY_ZZ_ZZZD_002',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 3,
        'APT_CASENAME': '工程监理公路工程专业丙级',
        'APT_ISEND': '1',
        'APT_CODE': 'E209C',
        'APT_TYPE': 'QY_ZZ_ZZZD_002',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 3,
        'APT_CASENAME': '工程监理市政公用工程专业丙级',
        'APT_ISEND': '1',
        'APT_CODE': 'E213C',
        'APT_TYPE': 'QY_ZZ_ZZZD_002',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 3,
        'APT_CASENAME': '工程招标代理暂定级',
        'APT_ISEND': '1',
        'APT_CODE': 'FZ',
        'APT_TYPE': 'QY_ZZ_ZZZD_006',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 4,
        'APT_CASENAME': '工程设计建筑行业（建筑工程）丁级',
        'APT_ISEND': '1',
        'APT_CODE': 'A32101D',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 4,
        'APT_CASENAME': '工程勘察水文地质勘察专业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'B201A',
        'APT_TYPE': 'QY_ZZ_ZZZD_003',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 4,
        'APT_CASENAME': '工程勘察水文地质勘察专业乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'B201B',
        'APT_TYPE': 'QY_ZZ_ZZZD_003',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 4,
        'APT_CASENAME': '工程勘察水文地质勘察专业丙级',
        'APT_ISEND': '1',
        'APT_CODE': 'B201C',
        'APT_TYPE': 'QY_ZZ_ZZZD_003',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 5,
        'APT_CASENAME': '工程勘察工程测量专业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'B202A',
        'APT_TYPE': 'QY_ZZ_ZZZD_003',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 5,
        'APT_CASENAME': '工程勘察工程测量专业乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'B202B',
        'APT_TYPE': 'QY_ZZ_ZZZD_003',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 5,
        'APT_CASENAME': '工程勘察工程测量专业丙级',
        'APT_ISEND': '1',
        'APT_CODE': 'B202C',
        'APT_TYPE': 'QY_ZZ_ZZZD_003',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 6,
        'APT_CASENAME': '工程勘察海洋工程勘察专业（海洋工程测量）甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'B20401A',
        'APT_TYPE': 'QY_ZZ_ZZZD_003',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 6,
        'APT_CASENAME': '工程勘察海洋工程勘察专业（海洋工程测量）乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'B20401B',
        'APT_TYPE': 'QY_ZZ_ZZZD_003',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 6,
        'APT_CASENAME': '工程勘察海洋工程勘察专业（海洋岩土工程勘察）甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'B20402A',
        'APT_TYPE': 'QY_ZZ_ZZZD_003',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 6,
        'APT_CASENAME': '工程勘察海洋工程勘察专业（海洋岩土工程勘察）乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'B20402B',
        'APT_TYPE': 'QY_ZZ_ZZZD_003',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 6,
        'APT_CASENAME': '工程勘察海洋工程勘察专业（海洋工程环境调查）甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'B20403A',
        'APT_TYPE': 'QY_ZZ_ZZZD_003',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 6,
        'APT_CASENAME': '工程勘察海洋工程勘察专业（海洋工程环境调查）乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'B20403B',
        'APT_TYPE': 'QY_ZZ_ZZZD_003',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 6,
        'APT_CASENAME': '工程勘察海洋工程勘察专业甲级',
        'APT_ISEND': '1',
        'APT_CODE': 'B204A',
        'APT_TYPE': 'QY_ZZ_ZZZD_003',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 6,
        'APT_CASENAME': '工程勘察海洋工程勘察专业乙级',
        'APT_ISEND': '1',
        'APT_CODE': 'B204B',
        'APT_TYPE': 'QY_ZZ_ZZZD_003',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 7,
        'APT_CASENAME': '工程勘察工程钻探劳务',
        'APT_ISEND': '1',
        'APT_CODE': 'B301X',
        'APT_TYPE': 'QY_ZZ_ZZZD_003',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 7,
        'APT_CASENAME': '工程勘察凿井劳务',
        'APT_ISEND': '1',
        'APT_CODE': 'B302X',
        'APT_TYPE': 'QY_ZZ_ZZZD_003',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 8,
        'APT_CASENAME': '工程设计电子通信广电行业无线通信专业',
        'APT_ISEND': '1',
        'APT_CODE': 'A31008',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': 9,
        'APT_CASENAME': '工程设计电子通信广电行业邮政工程专业',
        'APT_ISEND': '1',
        'APT_CODE': 'A31009',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': '',
        'APT_CASENAME': '工程设计军工行业防化、民爆器材工程专业',
        'APT_ISEND': '1',
        'APT_CODE': 'A30618\t',
        'APT_TYPE': 'QY_ZZ_ZZZD_004',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': '',
        'APT_CASENAME': '预拌混凝土专业承包不分等级',
        'APT_ISEND': '1',
        'APT_CODE': 'D203X',
        'APT_TYPE': 'QY_ZZ_ZZZD_001',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': '',
        'APT_CASENAME': '模板脚手架专业承包不分等级',
        'APT_ISEND': '1',
        'APT_CODE': 'D210X',
        'APT_TYPE': 'QY_ZZ_ZZZD_001',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': '',
        'APT_CASENAME': '特种工程(结构补强)专业承包不分等级',
        'APT_ISEND': '1',
        'APT_CODE': 'D23601X',
        'APT_TYPE': 'QY_ZZ_ZZZD_001',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': '',
        'APT_CASENAME': '特种工程(建筑物纠偏和平移)专业承包不分等级',
        'APT_ISEND': '1',
        'APT_CODE': 'D23602X',
        'APT_TYPE': 'QY_ZZ_ZZZD_001',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': '',
        'APT_CASENAME': '特种工程(特殊设备起重吊装)专业承包不分等级',
        'APT_ISEND': '1',
        'APT_CODE': 'D23603X',
        'APT_TYPE': 'QY_ZZ_ZZZD_001',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': '',
        'APT_CASENAME': '特种工程（特种防雷）专业承包不分等级',
        'APT_ISEND': '1',
        'APT_CODE': 'D23604X',
        'APT_TYPE': 'QY_ZZ_ZZZD_001',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': '',
        'APT_CASENAME': '特种工程专业承包不分等级',
        'APT_ISEND': '1',
        'APT_CODE': 'D236X',
        'APT_TYPE': 'QY_ZZ_ZZZD_001',
        'VALID_FLAG': '1'
      },
      {
        'APT_ORDER': '',
        'APT_CASENAME': '工程监理事务所',
        'APT_ISEND': '1',
        'APT_CODE': 'E3X',
        'APT_TYPE': 'QY_ZZ_ZZZD_002',
        'VALID_FLAG': '1'
      }
    ]
         for region in region_code:
            # print(file ,value)
            for apt in certs:
                cert= apt.get('APT_CODE')
                print(apt)
                for comname  in spider.channel_info(region,cert):
                    print(region)
                    print(comname)
                    spider.write_data('namessss.txt', comname)
