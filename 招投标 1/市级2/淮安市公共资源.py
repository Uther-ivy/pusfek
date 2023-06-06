# -*- coding: utf-8 -*-
import datetime
import json
import random
import re
import time

import pymysql
import requests
from scrapy import Selector
import json
import ssl
import tool
from save_database import save_db
from proxies import proxise
pro = proxise()


ssl._create_default_https_context = ssl._create_unverified_context

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
}

# city_list
def get_nativeplace(text):
    if '淮安市' in text:
        nativeplace = 5508
    elif '清河区' in text:
        nativeplace = 5508.001
    elif '楚州区' in text:
        nativeplace = 5508.002
    elif '涟水县' in text:
        nativeplace = 5508.003
    elif '淮阴区' in text:
        nativeplace = 5508.004
    elif '清浦区' in text:
        nativeplace = 5508.005
    elif '洪泽县' in text:
        nativeplace = 5508.006
    elif '盱眙县' in text:
        nativeplace = 5508.007
    elif '金湖县' in text:
        nativeplace = 5508.008
    else:
        nativeplace = 5508
    return nativeplace

def get_zhaobiao_info(zhao_time,info_url,title):
    resp = requests.get(info_url, headers=headers ,proxies=pro,timeout=20,verify=False)
    resp.encoding = "utf8"
    sel = Selector(resp)
    if resp.status_code == 200:
        item = {}
        item['zhao_time'] = zhao_time
        item['title'] = title
        item['info_url'] = info_url
        item['body'] = sel.xpath('//*[@id="mainContent"]').extract_first()
        detail = sel.xpath('string(//*[@id="mainContent"])').extract_first()
        item['detail'] = detail.replace('\n', '').replace("\t", '').replace("\r", '').replace('\xa0', '').replace('\xc2', '').replace(' ', '')
        item['senddate'] = int(time.time())
        item['mid'] = 1403
        item['typeid'] = tool.get_typeid(item['title'])
        item['endtime'] = tool.get_endtime(item['detail'])
        if item['endtime'] == '':
            item['endtime'] = int(time.mktime(time.strptime(item['zhao_time'], "%Y-%m-%d")))
        else:
            try:
                item['endtime'] = int(time.mktime(time.strptime(item['endtime'], "%Y-%m-%d")))
            except:
                item['endtime'] = int(time.mktime(time.strptime(item['zhao_time'], "%Y-%m-%d")))
        item['nativeplace'] = get_nativeplace(title)
        item['infotype'] = tool.get_infotype(title)
        item['shi'] = int(item['nativeplace'])  # 4502
        item['sheng'] = 5500
        item['email'] = ''
        item['tel'] = tool.get_tel(item['detail'])
        item['address'] = tool.get_address(item['detail'])
        item['linkman'] = tool.get_linkman(item['detail'])
        item['function'] = tool.get_function(item['detail'])  # detail["projectBudget"]
        item['click'] = random.randint(500, 1000)
        item['resource'] = "淮安市公共资源"
        save_db(item)


def get_project(url,now_time):
    resp = requests.get(url,headers=headers,proxies=pro,timeout=20,verify=False)
    resp.encoding='utf8'
    sel = Selector(resp)
    titles = sel.xpath('//*[@id="infolist"]/tr')
    for ti in titles:
        title = ti.xpath('./td[2]/a/@title').extract_first().strip()
        info_url = "http://ggzy.huaian.gov.cn" + ti.xpath('./td[2]/a/@href').extract_first()
        zhao_time = ti.xpath('./td[last()]/text()').extract_first()
        # print(title,info_url,zhao_time)
        if tool.Transformation(now_time) <= tool.Transformation(zhao_time):
            # print(title,info_url,zhao_time)
            get_zhaobiao_info(zhao_time,info_url,title)
        else:
            print('日期不符', zhao_time)

if __name__ == '__main__':
    import traceback, os
    try:
        requests.adapters.DEFAULT_RETRIES = 5  # 增加重连次数
        s = requests.session()
        s.keep_alive = False  # 关闭多余连接
        requests.packages.urllib3.disable_warnings()
        now_time = tool.date
        for i in range(1, 4):
            get_project(
                "http://ggzy.huaian.gov.cn/EpointWeb/ShowInfo/JyxxSearchInfoList.aspx?timebegin=1990-01-01&timeend={}&jyly=&ywlx=&xxlx=&Eptrcontent=&Paging={}".format(
                    now_time, str(i)), now_time)
    except Exception as e:
        traceback.print_exc()
        tool.send_error('报错文件：'+str(os.path.basename(__file__))+'报错信息：'+str(e))
