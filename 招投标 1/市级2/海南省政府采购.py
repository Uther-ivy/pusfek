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
def get_nativeplace(addr):
    city = ''
    # 某省/自治区所有的地级市县
    city_list = [['11000' ,'海南省'] ,['11001' ,'海口市'] ,['11001.001' ,'秀英区'] ,['11001.002' ,'龙华区'] ,['11001.003' ,'琼山区']
                 ,['11001.004' ,'美兰区'] ,['11002' ,'三亚市'] ,['11003' ,'省直辖县级行政单位'] ,['11003.001' ,'五指山市']
                 ,['11003.01' ,'临高县'] ,['11003.011' ,'白沙黎族自治县'] ,['11003.012' ,'昌江黎族自治县'] ,['11003.013' ,'乐东黎族自治县']
                 ,['11003.014' ,'陵水黎族自治县'] ,['11003.015' ,'保亭黎族苗族自治县'] ,['11003.016' ,'琼中黎族苗族自治县']
                 ,['11003.017' ,'西沙群岛'] ,['11003.018' ,'南沙群岛'] ,['11003.019' ,'中沙群岛的岛礁及其海域'] ,['11003.002' ,'琼海市']
                 ,['11003.003' ,'儋州市'] ,['11003.004' ,'文昌市'] ,['11003.005' ,'万宁市'] ,['11003.006' ,'东方市']
                 ,['11003.007' ,'定安县'] ,['11003.008' ,'屯昌县'] ,['11003.009' ,'澄迈县']]
    for i in city_list:
        if i[1] in addr:
            city = float(i[0])
            break
    if city == '':
        city = 11000
    return city


def get_zhaobiao_info(zhao_time,info_url,title):
    resp = requests.get(info_url, headers=headers ,proxies=pro,verify=False, timeout=20)
    resp.encoding = "utf8"
    sel = Selector(resp)
    if resp.status_code == 200:
        item = {}
        item['zhao_time'] = zhao_time
        item['title'] = title
        item['info_url'] = info_url
        item['body'] = sel.xpath('//div[@class="content01"]').extract_first().replace('<a href="','<a href="https://www.ccgp-hainan.gov.cn')
        detail = sel.xpath('string(//div[@class="content01"])').extract_first()
        item['detail'] = detail.replace('\n', '').replace("\t", '').replace("\r", '').replace('\xa0', '').replace('\xc2', '').replace(' ', '')
        item['senddate'] = int(time.time())
        item['mid'] = 1403
        item['typeid'] = tool.get_typeid(title)
        item['endtime'] = tool.get_endtime(item['detail'])
        if item['endtime'] == '':
            item['endtime'] = int(time.mktime(time.strptime(zhao_time, "%Y-%m-%d")))
        else:
            try:
                item['endtime'] = int(time.mktime(time.strptime(item['endtime'], "%Y-%m-%d")))
            except:
                item['endtime'] = int(time.mktime(time.strptime(zhao_time, "%Y-%m-%d")))
        item['nativeplace'] = get_nativeplace(title + item['detail'])
        item['infotype'] = tool.get_infotype(title)
        item['shi'] = int(item['nativeplace'])  # 4502
        item['sheng'] = 11000
        item['email'] = ''
        item['tel'] = tool.get_tel(item['detail'])
        item['address'] = tool.get_address(item['detail'])
        item['linkman'] = tool.get_linkman(item['detail'])
        item['function'] = tool.get_function(item['detail'])  # detail["projectBudget"]
        item['click'] = random.randint(500, 1000)
        item['resource'] = "海南省政府采购网"
        save_db(item)

def get_project(url):
    resp = requests.get(url,headers=headers,verify=False,proxies=pro,timeout=20)
    resp.encoding='uft8'
    sel = Selector(resp)
    titles = sel.xpath('//div[@class="nei03_04_08"]/ul/li')
    now_time = tool.date
    for ti in titles:
        title = ti.xpath('./em/a/text()').extract_first().strip()
        info_url = "https://www.ccgp-hainan.gov.cn" + ti.xpath('./em/a/@href').extract_first()
        zhao_time = ti.xpath('./i/text()').extract_first().strip()
        if '测试' in title:
            continue
        # print(title,info_url,zhao_time)
        if tool.Transformation(now_time) <= tool.Transformation(zhao_time):
            # print(title,info_url,zhao_time)
            get_zhaobiao_info(zhao_time,info_url,title)
        else:
            print('日期不符', zhao_time)


if __name__ == '__main__':
    requests.adapters.DEFAULT_RETRIES = 5  # 增加重连次数
    s = requests.session()
    s.keep_alive = False  # 关闭多余连接
    requests.packages.urllib3.disable_warnings()
    url_list = [
        "https://www.ccgp-hainan.gov.cn/cgw/cgw_list_cgxx.jsp?currentPage=1",
        "https://www.ccgp-hainan.gov.cn/cgw/cgw_list_cgxx.jsp?currentPage=2",
        "https://www.ccgp-hainan.gov.cn/cgw/cgw_list_cgxx.jsp?currentPage=3",
    ]
    for url in url_list:
        get_project(url)