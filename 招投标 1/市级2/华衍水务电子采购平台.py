# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 华衍水务电子采购平台
class baoshan_ggzy:
    def __init__(self):
        self.url_list = [
            'https://caigou.huayanwater.com/yunbidding/index/platsysinfo!queryNotice.action?siteFlag=false&titleParam=&platInfoPage.pageSize=10&platInfoPage.pageNo={}&type=1%2C5%2C6%2C9&styleType=',
            'https://caigou.huayanwater.com/yunbidding/index/platsysinfo!queryNotice.action?siteFlag=false&titleParam=&platInfoPage.pageSize=10&platInfoPage.pageNo={}&type=3&styleType=',
            'https://caigou.huayanwater.com/yunbidding/index/platsysinfo!queryNotice.action?siteFlag=false&titleParam=&platInfoPage.pageSize=10&platInfoPage.pageNo={}&type=4%2C11%2C7%2C16&styleType='
        ]
        self.url = self.url_list.pop(0)
        self.headers = {
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Cookie': 'SESSION=f0b05999-e533-4ae0-96dc-5fa0ca9e2f40; JSESSIONID=8419CC7C9C27842543849F570722B4F5.32node2',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        }

    def parse(self):
        date = tool.date
        # date = '2021-08-16'
        page = 0
        while True:
            page += 1
            text = tool.requests_get(self.url.format(page), self.headers).replace('\u2022', '')
            print('*' * 20, page, '*' * 20)
            detail = json.loads(text)['param1']['result']
            for li in detail:
                title = li['title'].replace('\n', '').replace('\t', '').replace(' ', '').replace('\r', '')
                url = 'https://caigou.huayanwater.com/yunbidding/index/platsysinfo!noticeDoUrl.action?platInfoId='+li['id']
                date_Today = li['publishTime'][:10]\
                    .replace('\n', '').replace('\t', '').replace(' ', '').replace('\r', '').replace('[', '').replace(']', '')
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
            if page == 5:
                self.url = self.url_list.pop(0)
                break

    def parse_detile(self, title, url, date):
        print(url)
        u = 'https://caigou.huayanwater.com/yunbidding/index/platsysinfo!queryContextById.action?siteFlag=false'
        data = 'platInfoId='+url.replace('https://caigou.huayanwater.com/yunbidding/index/platsysinfo!noticeDoUrl.action?platInfoId=', '')
        t = tool.requests_post(u, data, self.headers)
        detail_html = json.loads(t)['param1']['content']
        detail_text = ''.join(re.findall('>(.*?)<', detail_html, re.S)).replace('\xa0', '').replace('\n', ''). \
            replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
        item = {}
        item['title'] = title.replace('\u2022', '')
        item['url'] = url
        item['date'] = date
        item['typeid'] = tool.get_typeid(item['title'])
        item['senddate'] = int(time.time())
        item['mid'] = 867
        item['infotype'] = tool.get_infotype(item['title'])
        item['body'] = tool.qudiao_width(detail_html)
        item['endtime'] = tool.get_endtime(detail_text)
        if item['endtime'] == '':
            item['endtime'] = int(time.mktime(time.strptime(date, "%Y-%m-%d")))
        else:
            try:
                item['endtime'] = int(time.mktime(time.strptime(item['endtime'], "%Y-%m-%d")))
            except:
                item['endtime'] = int(time.mktime(time.strptime(date, "%Y-%m-%d")))
        item['tel'] = tool.get_tel(detail_text)
        item['email'] = ''
        item['address'] = tool.get_address(detail_text)
        item['linkman'] = tool.get_linkman(detail_text)
        item['function'] = tool.get_function(detail_text)
        item['resource'] = '华衍水务电子采购平台'
        item['sheng'] = 6500
        item['nativeplace'] = self.get_nativeplace(title)
        item['shi'] = 6502
        item['removal']= title
        process_item(item)

    def get_nativeplace(self, addr):
        city = ''
        city_list = [['6502.001', '镜湖区'], ['6502.002', '马塘区'], ['6502.003', '新芜区'], ['6502.004', '鸠江区'], ['6502.005', '芜湖县'], ['6502.006', '繁昌县'], ['6502.007', '南陵县']]

        for i in city_list:
            if i[1] in addr:
                city = float(i[0])
                break
        if city == '':
            city = 6502
        return city

if __name__ == '__main__':
    import traceback,os
    try:
        jl = baoshan_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()



