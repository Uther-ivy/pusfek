# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
import datetime
from save_database import process_item

# 粤采易阳光采购平台
class wenshan_ggzy:
    def __init__(self):
        self.url_list = [
            'https://www.gdycy.com/ycg-gateway/door/home/zhaobiao/notice/list?t={}&zhaoBiaoType=&type=1&mode=&page={}&limit=10&bulletinName=&isYifa=&cityNo=&timeType=&endTime=', #工程招标
           ]
        self.url = self.url_list.pop(0)
        self.headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'}
    def parse(self):
        date = tool.date
        # date = '2020-09-21'
        page = 0
        while True:
            page += 1
            timep = int(time.time() * 1000)
            text = tool.requests_get(url=self.url.format(timep,page),headers=self.headers)
            url_html=json.loads(text)
            print('*' * 20, page, '*' * 20)
            # print(11, text)
            # time.sleep(6666)
            detail = url_html["data"]["list"]
            for li in detail:
                title = li["bulletinName"]
                date_Today = li["bulletinStartTime"]
                id = li["id"]
                noticeId = li["noticeId"]
                url = f'https://www.gdycy.com/ycg-gateway/door/home/zbItem/{id}?noticeId={noticeId}'
                # print(title, url, date_Today)
                # time.sleep(666)
                # self.parse_detile(title, url, date_Today,id,noticeId)
                if tool.Transformation(date) <= tool.Transformation(date_Today):
                    if tool.removal(title, date):
                        self.parse_detile(title, url, date_Today,id,noticeId)
                    else:
                        print('【existence】', url)
                        continue
                else:
                    print('日期不符, 正在切换类型', date_Today)
                    self.url = self.url_list.pop(0)
                    page = 0
                    break
            if page == 20:
                print('日期不符, 正在切换类型')
                self.url = self.url_list.pop(0)
                break

    def parse_detile(self, title, url, date,id,noticeId):
        print(url)
        t = tool.requests_get(url=url,headers=self.headers)
        # print(t)
        # time.sleep(2222)
        url_html = json.loads(t)
        detail_text = url_html["data"]["biddNotice"]["bulletinInfo"]
        index_url=f'https://www.gdycy.com/#/purchasedetauls/?id={id}&type=1&noticeId={noticeId}'
        if detail_text==None or len(detail_text) < 300:
            return
        item = {}
        item['title'] = title.replace('\u2022', '')
        item['url'] = index_url
        item['date'] = date
        item['typeid'] = tool.get_typeid(item['title'])
        item['senddate'] = int(time.time())
        item['mid'] = 867
        item['nativeplace'] = self.get_nativeplace(item['title'])
        item['infotype'] = tool.get_infotype(item['title'])
        item['body'] = tool.qudiao_width(detail_text)
        item['body'] = item['body']
        # print(item['body'].replace('\xa0', '').replace('\xa5', '').replace('\xb3', ''))
        # time.sleep(6666)
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
        item['resource'] = '粤采易阳光采购平台'
        item['shi'] = 6507
        item['sheng'] = 6500
        item['removal']= title
        # print(item["body"])
        process_item(item)
    def get_nativeplace(self, addr):
        city = ''
        city_list = [['6507.001', '铜官山区'], ['6507.002', '狮子山区'], ['6507.003', '郊区'], ['6507.004', '铜陵县']]

        for i in city_list:
            if i[1] in addr:
                city = float(i[0])
                break
        if city == '':
            city = 6507
        return city

if __name__ == '__main__':
    import os,traceback
    try:
        jl = wenshan_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
        tool.send_error('报错文件：'+str(os.path.basename(__file__))+'报错信息：'+str(e))



