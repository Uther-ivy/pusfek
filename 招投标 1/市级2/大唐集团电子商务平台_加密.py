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
from proxies import proxise
pro = proxise()

ssl._create_default_https_context = ssl._create_unverified_context
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Host': 'www.cdt-ec.com',
    'Referer': 'http://www.cdt-ec.com/potal-web/pendingGxnotice/where?message_type=0&pageno=1&pagesize=5',
    'Cookie': 'acw_tc=ac11000116474093823233657e00cbc6ea9b763f10efd1cca07c9e20af0fe6; acw_sc__v2=623178e62f43d7abc6a27c23776341bef43b4568',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
}

def get_zhaobiao_info(zhao_time,info_url):
    resp = requests.get(info_url, headers=headers,proxies=pro,timeout=20)
    resp.encoding = "utf8"
    date = json.loads(resp.text)
    item = {}
    item['zhao_time'] = zhao_time
    item['info_url'] = info_url
    item['title'] = date['message_title']
    pro_bidding_mothod = date['pro_bidding_mothod']
    pro_quali_examin = date['pro_quali_examin']
    pro_area = date['pro_area']
    pro_overvier = date['pro_overvier']
    message_url = date['message_url']
    item['body'] = "<h1>" + item['title'] + "</h1><h3>项目概况</h3><table border='0' cellspacing='0' cellpadding='0' class='blockContent'><tbody><tr><th>招标方式</th><td width='400px;'><span class='spangs' >" + pro_bidding_mothod + "</span></td><th>资格审查</th><td><span>" + pro_quali_examin + "</span></td></tr><tr><th>项目区域</th><td colspan='1'><span class='spangs' >" + pro_area + "</span></td></tr><tr><th>概况</th><td colspan='4' id='hhhhhhh'><span>" + pro_overvier + "</span></td></tr></tbody></table></div><div class='block'><a href=" + message_url + "id='oDownLoad'  onclick='pdf()'><span class='pdfflash'>PDF下载</span></a></div></ul>"
    item['detail'] = item['body'].replace('\n', '').replace("\t", '').replace("\r", '').replace('\xa0', '').replace('\xc2', '').replace(' ', '')
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
    item['nativeplace'] = tool.more(item['title'])
    if item['nativeplace'] == 0:
        item['nativeplace'] = tool.more(item['title'])
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
    item['resource'] = "大唐集团电子商务平台"
    save_db(item)

def get_project(url):
    js_ = '''function setCookie(name,value){
                var expiredate=new Date();
                expiredate.setTime(expiredate.getTime()+(3600*1000));
                document.cookie=name+"="+value+";
                expires="+expiredate.toGMTString()+";
                max-age=3600;path=/";
                }
            '''
    resp = requests.get(url,headers=headers,proxies=pro,timeout=20)
    resp.encoding='utf8'
    print(resp.text)
    time.sleep(2222)
    date = json.loads(resp.text)
    now_time = tool.date
    # now_time = '2021-07-27'
    for da in date:
        zhao_time = da['publish_time']/1000
        info_url = "http://www.cdt-ec.com/potal-web/pendingGxnotice/selectbyid?id=" + str(da['id'])
        timeArray = time.localtime(zhao_time)
        otherStyleTime = time.strftime("%Y-%m-%d", timeArray)
        if otherStyleTime == now_time:
            get_zhaobiao_info(otherStyleTime,info_url)
        else:
            print(otherStyleTime)

if __name__ == '__main__':
    requests.adapters.DEFAULT_RETRIES = 5  # 增加重连次数
    s = requests.session()
    s.keep_alive = False  # 关闭多余连接
    requests.packages.urllib3.disable_warnings()
    url = 'http://www.cdt-ec.com/potal-web/pendingGxnotice/where?message_type=0&pageno=1&pagesize=5'
    get_project(url)