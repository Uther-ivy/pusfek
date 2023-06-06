# -*- coding: utf-8 -*-
import datetime
import json
import random
import re
import time
import json
import pymysql
import requests
from scrapy import Selector
import ssl
import tool
from save_database import save_db, process_item

ssl._create_default_https_context = ssl._create_unverified_context
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
}

def get_zhaobiao_info(title,zhao_time,info_url,url):
    time.sleep(2)
    resp = tool.requests_get(info_url, headers=headers)
    item = {}
    item['title'] = title
    item['url'] = url
    item['date'] = zhao_time
    item['typeid'] = tool.get_typeid(item['title'])
    item['senddate'] = int(time.time())
    item['mid'] = 1403
    txt = resp.replace("jQuery17204731200554495951_1594091905537(", "").replace("})", "}")
    data = json.loads(txt)
    item['body'] = data['data'][0]['content']
    item['detail'] = item['body'].replace('\n', '').replace("\t", '').replace("\r", '').replace('\xa0', '').replace('\xc2', '').replace(' ', '')
    item['nativeplace'] = tool.get_title_city(item['title'])
    if item['nativeplace'] == 0:
        item['nativeplace'] = tool.more(item['title'] + item['detail'])
    item['infotype'] = tool.get_infotype(item['title'])
    item['endtime'] = tool.get_endtime(item['detail'])
    if item['endtime'] == '':
        item['endtime'] = int(time.mktime(time.strptime(item['date'], "%Y-%m-%d")))
    else:
        try:
            item['endtime'] = int(time.mktime(time.strptime(item['endtime'], "%Y-%m-%d")))
        except:
            item['endtime'] = int(time.mktime(time.strptime(item['zhao_time'], "%Y-%m-%d")))
    item['tel'] = tool.get_tel(item['detail'])
    item['email'] = ''
    item['resource'] = "中国联合钢铁网电子商务平台"
    item['winner'] = tool.get_winner(item['detail'])
    item['address'] = tool.get_address(item['detail'])
    item['linkman'] = tool.get_linkman(item['detail'])
    item['function'] = tool.get_function(item['detail'])  # detail["projectBudget"]
    item['click'] = random.randint(500, 1000)
    item['shi'] = int(item['nativeplace'])
    item['sheng'] = tool.get_sheng(item['title'])
    if len(str(item['shi'])) == 4:
        item['sheng'] = str(item['shi'])[:2] + '00'
    elif len(str(item['shi'])) == 5:
        item['sheng'] = str(item['shi'])[:3] + '00'
    process_item(item)

def get_project():
    page=1
    while True:
        page+=1
        print('*'*20,page,'*'*20)
        url = 'http://ec.custeel.com/cgnews.mv?method=getCgnewAlls&callback=jQuery17204731200554495951_1594091905537&categoryID=1002002&title=&cname=&putdate=&pageNum='+str(page)+'&pageSize=200&_={}'
        after_time = time.time()
        af_time = int(str(after_time).split(".")[0]+"000") - 600000
        # print(url)
        # print(url.format(str(af_time)))
        resp = tool.requests_get(url.format(str(af_time)),headers=headers)
        resp_text = "{" + resp.split("({")[1].replace("})","}")
        date = json.loads(resp_text)
        date = date['data']['list']
        now_time = tool.date
        # now_time = '2021-07-23'
        for da in date:
            try:
                title = da['title']
                zhao_time = da['putdate'].split(" ")[0]
                url=f"http://ec.custeel.com/home/announcementDetail.html?number={da['number']}"
                info_url = "http://ec.custeel.com/cgnews.mv?method=getNewsDetail&number=" + da['number'] + "&callback=jQuery17204731200554495951_1594091905537&_=1600151795720"
                print(info_url)
                if tool.Transformation(now_time) <= tool.Transformation(zhao_time):
                    print(title, zhao_time, url)
                    get_zhaobiao_info(title, zhao_time, info_url,url)
                else:
                    print('时间不符',zhao_time,now_time)
                    return
            except Exception as e:
                traceback.print_exc()
                # print("=="*50)

if __name__ == '__main__':
    import traceback, os
    try:
        requests.adapters.DEFAULT_RETRIES = 5  # 增加重连次数
        s = requests.session()
        s.keep_alive = False  # 关闭多余连接
        requests.packages.urllib3.disable_warnings()
        # zhaobiao_url(1) , zhongbiao_url(2)

        get_project()
    except Exception as e:
        traceback.print_exc()
        print(e)
        tool.send_error('报错文件：'+str(os.path.basename(__file__))+'报错信息：'+str(e))
