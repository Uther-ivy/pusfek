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

def get_zhaobiao_info(zhao_time,info_url,title):
    resp = requests.get(info_url, headers=headers ,proxies=pro,timeout=20)
    resp.encoding = "utf8"
    sel = Selector(resp)
    if resp.status_code == 200:
        item = {}
        item['zhao_time'] = zhao_time
        item['title'] = title
        item['info_url'] = info_url
        item['body'] = sel.xpath('//div[@class="con"]').extract_first()
        detail = sel.xpath('string(//div[@class="con"])').extract_first()
        item['detail'] = detail.replace('\n', '').replace("\t", '').replace("\r", '').replace('\xa0', '').replace('\xc2', '').replace(' ', '')
        item['senddate'] = int(time.time())
        item['mid'] = 1403
        item['typeid'] = tool.get_typeid(title)
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
            item['nativeplace'] = tool.more(item['title']+detail)
        item['infotype'] = tool.get_infotype(title)
        item['shi'] = int(str(item['nativeplace']).split('.')[0])  # 4502
        item['sheng'] = tool.get_sheng(title)
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
        item['resource'] = "国家能源招标网"
        save_db(item)

def get_project(url):
    resp = requests.get(url,headers=headers,proxies=pro,timeout=20)
    resp.encoding='uft8'
    sel = Selector(resp)
    titles = sel.xpath('//div[@class="right-bd"]/ul[1]/li')
    now_time = tool.date
    for ti in titles:
        title = ti.xpath('./div/a[2]/text()').extract_first().strip()
        info_url = "http://www.shenhuabidding.com.cn" + ti.xpath('./div/a[1]/@href').extract_first()
        zhao_time = ti.xpath('./span/text()').extract_first().strip()
        # print(title,info_url,zhao_time)
        if tool.Transformation(now_time) <= tool.Transformation(zhao_time):
            # print(title,info_url,zhao_time)
            get_zhaobiao_info(zhao_time,info_url,title)
        else:
            print(zhao_time)

if __name__ == '__main__':
    requests.adapters.DEFAULT_RETRIES = 5  # 增加重连次数
    s = requests.session()
    s.keep_alive = False  # 关闭多余连接
    requests.packages.urllib3.disable_warnings()
    url_list = [
        "http://www.shenhuabidding.com.cn/bidweb/001/001002/1.html",
        "http://www.shenhuabidding.com.cn/bidweb/001/001001/1.html",
        "http://www.shenhuabidding.com.cn/bidweb/001/001003/1.html",
        "http://www.shenhuabidding.com.cn/bidweb/001/001004/1.html",
        "http://www.shenhuabidding.com.cn/bidweb/001/001005/1.html",
        "http://www.shenhuabidding.com.cn/bidweb/001/001006/1.html",
        "http://www.shenhuabidding.com.cn/bidweb/001/001007/1.html",
        "http://www.shenhuabidding.com.cn/bidweb/001/001008/1.html",
        "http://www.shenhuabidding.com.cn/bidweb/001/001002/2.html",
        "http://www.shenhuabidding.com.cn/bidweb/001/001001/2.html",
        "http://www.shenhuabidding.com.cn/bidweb/001/001003/2.html",
        "http://www.shenhuabidding.com.cn/bidweb/001/001004/2.html",
        "http://www.shenhuabidding.com.cn/bidweb/001/001005/2.html",
        "http://www.shenhuabidding.com.cn/bidweb/001/001006/2.html",
        "http://www.shenhuabidding.com.cn/bidweb/001/001007/2.html",
        "http://www.shenhuabidding.com.cn/bidweb/001/001008/2.html",
        "http://www.shenhuabidding.com.cn/bidweb/001/001002/3.html",
        "http://www.shenhuabidding.com.cn/bidweb/001/001001/3.html",
        "http://www.shenhuabidding.com.cn/bidweb/001/001003/3.html",
        "http://www.shenhuabidding.com.cn/bidweb/001/001004/3.html",
        "http://www.shenhuabidding.com.cn/bidweb/001/001005/3.html",
        "http://www.shenhuabidding.com.cn/bidweb/001/001006/3.html",
        "http://www.shenhuabidding.com.cn/bidweb/001/001007/3.html",
        "http://www.shenhuabidding.com.cn/bidweb/001/001008/3.html",
    ]
    for url in url_list:
        get_project(url)