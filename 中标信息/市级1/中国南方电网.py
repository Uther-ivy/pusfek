# -*- coding: utf-8 -*-
import datetime
import json
import random
import re
import time
import traceback

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

def get_zhaobiao_info(zhao_time,info_url,title):
    resp = tool.requests_(info_url, headers)
    resp.encoding = "utf8"
    sel = Selector(resp)
    item = {}

    item['title'] = title
    item['url'] = info_url
    item['date'] = zhao_time
    item['body'] = sel.xpath('//div[@class="Content"]').extract_first()
    detail = sel.xpath('string(//div[@class="Content"])').extract_first()
    item['detail'] = detail.replace('\n', '').replace("\t", '').replace("\r", '').replace('\xa0', '').replace('\xc2', '').replace(' ', '')
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
        item['nativeplace'] = tool.more(item['title']+item['detail'])
    item['infotype'] = tool.get_infotype(item['title'])
    item['shi'] = int(str(item['nativeplace']).split('.')[0])  # 4502
    item['sheng'] = tool.get_sheng(item['title'])
    item['email'] = ''
    item['tel'] = tool.get_tel(item['detail'])
    item['winner'] = tool.get_winner(item['detail'])
    item['address'] = tool.get_address(item['detail'])
    item['linkman'] = tool.get_linkman(item['detail'])
    item['function'] = tool.get_function(item['detail'])  # detail["projectBudget"]
    item['click'] = random.randint(500, 1000)
    item['resource'] = "中国南方电网"
    process_item(item)

def get_project():
    page=0
    date=tool.date
    while True:
        page += 1
        print('*' * 20, page, '*' * 20)
        url=f'http://www.bidding.csg.cn/dbsearch.jspx?pageNo={page}&channelId=52&types=&org=&q=%E4%B8%AD%E6%A0%87'

        resp = tool.requests_(url, headers)
        resp.encoding='uft8'
        sel = Selector(resp)
        titles = sel.xpath('//div[@class="List2"]/ul/li')
        for ti in titles:
            try:
                title = ti.xpath('./a[2]/text()').extract_first()
                print(title)
                info_url = "http://www.bidding.csg.cn" + ti.xpath('./a/@href').extract_first()
                zhao_time = ti.xpath('./span/span/text()').extract_first().strip()
                # print(title,info_url,zhao_time)
                if tool.Transformation(date) <= tool.Transformation(zhao_time):
                    # print(title,info_url,zhao_time)
                    time.sleep(3+random.random()*10)
                    get_zhaobiao_info(zhao_time,info_url,title)
                else:
                    print('日期不符, 正在切换类型...', zhao_time, info_url)
                    return
            except Exception:
                traceback.print_exc()

if __name__ == '__main__':
    requests.adapters.DEFAULT_RETRIES = 5  # 增加重连次数
    s = requests.session()
    s.keep_alive = False  # 关闭多余连接
    requests.packages.urllib3.disable_warnings()
    url_list = [
        # "http://www.bidding.csg.cn/zbgg/index_1.jhtml",
        # "http://www.bidding.csg.cn/zbgg/index_2.jhtml",
        # "http://www.bidding.csg.cn/zbgg/index_3.jhtml",
        # "http://www.bidding.csg.cn/fzbgg/index_1.jhtml",
        # "http://www.bidding.csg.cn/fzbgg/index_2.jhtml",
        # "http://www.bidding.csg.cn/fzbgg/index_3.jhtml",
        # "http://www.bidding.csg.cn/zbhxrgs/index_1.jhtml",
        # "http://www.bidding.csg.cn/zbhxrgs/index_2.jhtml",
        # "http://www.bidding.csg.cn/zbhxrgs/index_3.jhtml",
        # "http://www.bidding.csg.cn/fbgg/index_1.jhtml",
        # "http://www.bidding.csg.cn/fbgg/index_2.jhtml",
        # "http://www.bidding.csg.cn/fbgg/index_3.jhtml",
    ]

    # for url in url_list:
    get_project()