# -*- coding: utf-8 -*-
import datetime
import json
import random
import re
import time

import pymysql
import requests
from scrapy import Selector
import ssl
import tool
from save_database import save_db
from proxiesssss import proxise
pro = proxise()

ssl._create_default_https_context = ssl._create_unverified_context
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
}

def get_zhaobiao_info(title,zhao_time,info_url):
    print(info_url)
    time.sleep(2)
    resp = requests.get(info_url, headers=headers,proxies=pro,timeout=20)
    resp.encoding = "utf8"
    sel = Selector(resp)
    item = {}
    item['zhao_time'] = zhao_time
    item['title'] = title
    item['info_url'] = info_url
    try:
        item['body'] = sel.xpath('//div[@class="ninfo-con"]').extract_first()
        item['detail'] = item['body'].replace('\n', '').replace("\t", '').replace("\r", '').replace('\xa0', '').replace('\xc2', '').replace(' ', '')
    except:
        item['body'] = sel.xpath('//div[@class="main-text"]').extract_first()
        item['detail'] = item['body'].replace('\n', '').replace("\t", '').replace("\r", '').replace('\xa0', '').replace(
            '\xc2', '').replace(' ', '')
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
    item['nativeplace'] = tool.get_title_city(item['title'])
    if item['nativeplace'] == 0:
        item['nativeplace'] = tool.more(item['title']+item['detail'])
    item['infotype'] = tool.get_infotype(item['title'])
    item['shi'] = int(str(item['nativeplace']).split('.')[0])
    item['sheng'] = tool.get_sheng(item['title'])
    if len(str(item['shi'])) == 4:
        item['sheng'] = str(item['shi'])[:2] + '00'
    elif len(str(item['shi'])) == 5:
        item['sheng'] = str(item['shi'])[:3] + '00'
    item['email'] = ''
    item['tel'] = tool.get_tel(item['detail'])
    item['address'] = tool.get_address(item['detail'])
    item['linkman'] = tool.get_linkman(item['detail'])
    item['function'] = tool.get_function(item['detail'])  # detail["projectBudget"]
    item['click'] = random.randint(500, 1000)
    item['resource'] = "中煤招标与采购网"
    save_db(item)

def get_project(url):
    resp = requests.get(url,headers=headers,proxies=pro,timeout=20)
    resp.encoding = 'utf8'
    sel = Selector(resp)
    titles = sel.xpath('//*[@id="list1"]/li')
    now_time = tool.date
    # now_time = '2021-07-28'
    for ti in titles:
        title = ti.xpath('./a/@title').extract_first()
        zhao_time = ti.xpath('./a/em/text()').extract_first().strip()
        info_url = 'http://www.zmzb.com' + ti.xpath('./a/@href').extract_first()
        if '测试' in title:
            continue
        if tool.Transformation(now_time) <= tool.Transformation(zhao_time):
            get_zhaobiao_info(title,zhao_time,info_url)
        else:
            print('日期不符', zhao_time)

if __name__ == '__main__':
    import traceback, os
    try:
        requests.adapters.DEFAULT_RETRIES = 5  # 增加重连次数
        s = requests.session()
        s.keep_alive = False  # 关闭多余连接
        requests.packages.urllib3.disable_warnings()
        # http://www.zmzb.com/cms/channel/ywgg1gc/index.htm?pageNo=2
        urls = ['http://www.zmzb.com/cms/channel/ywgg1gc/index.htm?pageNo={}', 'http://www.zmzb.com/cms/channel/ywgg1hw/index.htm?pageNo={}',
                'http://www.zmzb.com/cms/channel/ywgg1fw/index.htm?pageNo={}']
        for i in range(1, 3):
            for url in urls:
                get_project(url.format(str(i)))
    except Exception as e:
        traceback.print_exc()
        tool.send_error('报错文件：'+str(os.path.basename(__file__))+'报错信息：'+str(e))
