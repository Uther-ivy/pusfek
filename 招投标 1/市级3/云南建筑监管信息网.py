# -*- coding: utf-8 -*-
import json
import re
import time, html

import execjs
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 必联网
class baoshan_ggzy:
    def __init__(self):
        self.url_list = [
          'https://www.ynjzjgcx.com/web/pro/getTenderingNoticeList'
        ]
        self.url = self.url_list.pop(0)
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        }


    def parse(self):
        date = tool.date
        # date = '2020-12-17'
        page = 0
        while True:
            page += 1
            data=f"pageNo={page}&pageSize=20&key=&t="
            text = tool.requests_post(self.url, headers=self.headers,data=data)
            print('*' * 20, page, '*' * 20)
            print(text)
            html = HTML(text)
            # print(11, text)
            # time.sleep(6666)
            detail = json.loads(text)['list']
            for li in detail:
                title = li['name']
                url = li['tenderingNoticeId']

                date_Today = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(li['fileOfferingStartDate']/1000))).split(' ')[0]
                if '测试' in title:
                    continue
                # print(title, url, date_Today)
                # time.sleep(666)
                if tool.Transformation(date) <= tool.Transformation(date_Today):
                    if tool.removal(title, date):
                        self.parse_detile(title, url, date_Today)
                    else:
                        print('【existence】', url)
                        continue
                else:
                    print('日期不符, 正在切换类型', date_Today, self.url)
                    self.url = self.url_list.pop(0)
                    page = 0
                    break
            if page == 20:
                self.url = self.url_list.pop(0)
                page = 0

    def parse_detile(self, title, url, date):
        print(url)
        url1='https://www.ynjzjgcx.com/web/pro/getTenderingNoticeById'
        data=f'tenderingNoticeId={url}&t='
        t = tool.requests_post1(url1,data=data,headers=self.headers)
        print(t)
        text=json.loads(t)['object']

        item = {}
        item['title'] = title
        item['url'] = 'https://www.ynjzjgcx.com/webHtml/pub/pro/biddingAnnouncement/view.html?n=pub&id='+url
        item['date'] = date
        item['typeid'] = tool.get_typeid(item['title'])
        item['senddate'] = int(time.time())
        item['mid'] = 867
        item['nativeplace'] = tool.get_city(item['title'])
        item['infotype'] = tool.get_infotype(item['title'])
        item['body'] = t
        item['endtime'] =   time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(text['fileOfferingEndDate'] / 1000))).split(' ')[0]

        if item['endtime'] == '':
            item['endtime'] = int(time.mktime(time.strptime(date, "%Y-%m-%d")))
        else:
            try:
                item['endtime'] = int(time.mktime(time.strptime(item['endtime'], "%Y-%m-%d")))
            except:
                item['endtime'] = int(time.mktime(time.strptime(date, "%Y-%m-%d")))
        item['tel'] = text['agentContactNamePhone']
        item['email'] = ''
        item['address'] = ''
        item['linkman'] = text['tradingPlatform']
        item['function'] = text['tenderingSections'][0]['tenderBail']
        item['resource'] = '云南建筑监管信息网'
        item['shi'] = tool.get_city(item['title'])
        item['sheng'] = tool.get_sheng(item['title'])
        item['removal']= item['title']
        process_item(item)

    def get_nativeplace(self, addr):
        city = ''
        city_list = [['7004.001','梅列区'],['7004.01','泰宁县'],['7004.011','建宁县'],['7004.012','永安市'],['7004.002','三元区'],
    ['7004.003','明溪县'],['7004.004','清流县'],['7004.005','宁化县'],['7004.006','大田县'],['7004.007','尤溪县'],
    ['7004.008','沙　县'],['7004.009','将乐县']]
        for i in city_list:
            if i[1] in addr:
                city = float(i[0])
                break
        if city == '':
            city = 7004
        return city

if __name__ == '__main__':
    import traceback,os
    try:
        jl = baoshan_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
        tool.send_error('报错文件：'+str(os.path.basename(__file__))+'报错信息：'+str(e))



