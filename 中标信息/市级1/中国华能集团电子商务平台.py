# -*- coding: utf-8 -*-
import datetime
import random
import re
import time
import json
import pymysql
import requests
from scrapy import Selector
import json
import ssl
import tool

from save_database import save_db, process_item


ssl._create_default_https_context = ssl._create_unverified_context
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
}

def get_zhaobiao_info(title,zhao_time,info_url):
    time.sleep(2)
    resp = tool.requests_(info_url, headers)
    resp.encoding = "utf8"
    sel = Selector(resp)
    item = {}
    item['title'] = title
    item['url'] = info_url
    item['date'] = zhao_time
    item['body'] = sel.xpath('//div[@class="detail_box qst_box"]').extract_first()
    print(item)
    item['detail'] = item['body'].replace('\n', '').replace("\t", '').replace("\r", '').replace('\xa0', '').replace('\xc2', '').replace(' ', '')
    item['senddate'] = int(time.time())
    item['mid'] = 1403
    item['typeid'] = tool.get_typeid(item['title'])
    item['endtime'] = tool.get_endtime(item['detail'])
    if item['endtime'] == '':
        item['endtime'] = int(time.mktime(time.strptime(zhao_time, "%Y-%m-%d")))
    else:
        try:
            item['endtime'] = int(time.mktime(time.strptime(item['endtime'], "%Y-%m-%d")))
        except:
            item['endtime'] = int(time.mktime(time.strptime(zhao_time, "%Y-%m-%d")))
    item['nativeplace'] = tool.get_title_city(item['title'])
    if item['nativeplace'] == 0:
        item['nativeplace'] = tool.more(item['title']+ item['detail'])
    item['infotype'] = tool.get_infotype(item['title'])
    item['email'] = ''
    item['tel'] = tool.get_tel(item['detail'])
    item['winner'] = tool.get_winner(item['detail'])
    item['address'] = tool.get_address(item['detail'])
    item['linkman'] = tool.get_linkman(item['detail'])
    item['function'] = tool.get_function(item['detail'])  # detail["projectBudget"]
    item['click'] = random.randint(500, 1000)
    item['resource'] = "中国华能集团电子商务平台"
    item['shi'] = int(str(item['nativeplace']).split('.')[0])
    item['sheng'] = tool.get_sheng(item['title'])
    if len(str(item['shi'])) == 4:
        item['sheng'] = str(item['shi'])[:2] + '00'
    elif len(str(item['shi'])) == 5:
        item['sheng'] = str(item['shi'])[:3] + '00'
    print(item)
    # save_db(item)
    process_item(item)

def get_project(url):
    types = ['103','105','ZBHXRGG','104','108','107','131','133','132']
    # for i in range(1,6):
    # for type in types:
    page=0
    date = tool.date
    while True:
        page+=1
        print('*' * 20, page, '*' * 20)
        data = {
            'type': '104',
            'searchWay': 'onTitle',
            'search':'',
            'ifend': 'in',
            'start': (page-1)*10,
            'limit': '10'
        }
        resp = tool.requests_post_(url, data, headers)
        resp.encoding='utf8'
        sel = Selector(resp)
        titles = sel.xpath('//*[@id="pageForm"]/ul/li')
        for ti in titles:
            try:
                title = ti.xpath('./a/@title').extract_first()
                info_url = "http://ec.chng.com.cn/ecmall/announcement/announcementDetail.do?announcementId=" + ti.xpath('./a/@href').extract_first().split("'")[1]
                zhao_time = ti.xpath('./p/text()').extract_first()
                print(title,zhao_time,info_url)
                if tool.Transformation(date) <= tool.Transformation(zhao_time):
                    time.sleep(1 + random.random() * 10)
                    get_zhaobiao_info(title,zhao_time,info_url)
                else:
                    print('日期不符, 正在切换类型...', zhao_time, info_url)
                    return
            except Exception:
                traceback.print_exc()

if __name__ == '__main__':
    import traceback, os
    try:
        requests.adapters.DEFAULT_RETRIES = 5  # 增加重连次数
        s = requests.session()
        s.keep_alive = False  # 关闭多余连接
        requests.packages.urllib3.disable_warnings()
        url = 'http://ec.chng.com.cn/ecmall/more.do'
        get_project(url)
    except Exception as e:
        traceback.print_exc()
