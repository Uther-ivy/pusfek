# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 锡林郭勒盟公共资源
class xilinguolemeng_ggzy:
    def __init__(self):
        self.url_list = [f'http://116.115.114.182:9091/document/jsgc/noticeInfo/findInfoByPage?pageNo=1&pageSize=10&noticeType=zbgg&regionCode=152500&_={int(time.time()*1000)}'
        ]
        self.url = self.url_list.pop(0)
        self.headers = {
            'Cookie': 'ASP.NET_SessionId=r40kdcifshq4a2barfgrsm55; ASP.NET_SessionId_NS_Sig=oenCV6md2zog4FC_; _gscu_1550197462=78882362a0uf3f11; _gscbrs_1550197462=1; _gscs_1550197462=78882362xnah8011|pv:29',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
        }

    def parse(self):
        date = tool.date
        # date = '2021-07-22'
        page = 0
        while True:
            page += 1
            text = tool.requests_get(self.url, self.headers)
            print('*' * 20, page, '*' * 20)
            detail = json.loads(text)['data']['items']
            for i in detail:
                title = i['name']
                id=i["id"]
                url2 =f'http://116.115.114.182:9091/document/jsgc/noticeInfo/details?id={id}&_={int(time.time()*1000)}'
                date_Today = i['releaseTime']
                # print(title, url, date_Today)
                # time.sleep(666)
                if tool.Transformation(date) <= tool.Transformation(date_Today):
                    if tool.removal(title, date):
                        self.parse_detile(title, url2, date)
                    else:
                        print('【existence】', url2)
                        continue
                else:
                    print('日期不符, 正在切换类型...', date_Today)
                    self.url = self.url_list.pop(0)
                    page = 0
                    break
            if page == 20:
                self.url = self.url_list.pop(0)
                break
    def parse_detile(self, title, url2, date):
        print(url2)
        url_html = tool.requests_get(url2, self.headers)
        print(url_html)
        detail=json.loads(url_html)
        detail_html=detail["data"]["content"]
        item = {}
        item['title'] = title.replace('\u2022', '')
        item['url'] = url2
        item['date'] = date
        item['typeid'] = tool.get_typeid(item['title'])
        item['senddate'] = int(time.time())
        item['mid'] = 867
        item['nativeplace'] = self.get_nativeplace(item['title'])
        item['infotype'] = tool.get_infotype(item['title'])
        item['body'] = tool.qudiao_width(detail_html)
        item['endtime'] = tool.get_endtime(detail_html)
        if item['endtime'] == '':
            item['endtime'] = int(time.mktime(time.strptime(date, "%Y-%m-%d")))
        else:
            try:
                item['endtime'] = int(time.mktime(time.strptime(item['endtime'], "%Y-%m-%d")))
            except:
                item['endtime'] = int(time.mktime(time.strptime(date, "%Y-%m-%d")))
        item['tel'] = tool.get_tel(detail_html)
        item['email'] = ''
        item['address'] = tool.get_address(detail_html)
        item['linkman'] = tool.get_linkman(detail_html)
        item['function'] = tool.get_function(detail_html)
        item['resource'] = '锡林郭勒盟公共资源'
        item['shi'] = 3011
        item['sheng'] = 3000
        item['removal']= title
        # print(item["body"])
        process_item(item)

    def get_nativeplace(self, addr):
        city = ''
        city_list = [['3011.001', '二连浩特市'], ['3011.01', '正镶白旗'], ['3011.011', '正蓝旗'], ['3011.012', '多伦县'], ['3011.002', '锡林浩特市'], ['3011.003', '阿巴嘎旗'], ['3011.004', '苏尼特左旗'], ['3011.005', '苏尼特右旗'], ['3011.006', '东乌珠穆沁旗'], ['3011.007', '西乌珠穆沁旗'], ['3011.008', '太仆寺旗'], ['3011.009', '镶黄旗']]
        for i in city_list:
            if i[1] in addr:
                city = float(i[0])
                break
        if city == '':
            city = 3011
        return city

if __name__ == '__main__':
    import traceback, os
    try:
        jl = xilinguolemeng_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
        tool.send_error('报错文件：'+str(os.path.basename(__file__))+'报错信息：'+str(e))


