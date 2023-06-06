# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from urllib.parse import quote
from save_database import process_item

# 揭阳市公共资源交易中心
class wenshan_ggzy:
    def __init__(self):
        self.url_list = [
            'http://jysggzy.jieyang.gov.cn/api/ords/epfcms/cmsItem/queryCmsItemByParams/004001?page={}',
        ]
        self.url = self.url_list.pop(0)
        self.headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'}
    def parse(self):
        date = tool.date
        # date = '2020-09-24'
        page = 0
        while True:
            page += 1
            text = tool.requests_get(self.url.format(page), self.headers)
            print('*' * 20, page, '*' * 20)
            html = json.loads(text)
            detail=html["items"]
            for li in detail:
                title = li["name"]
                date_Today = li["info_time"].split('T')[0]
                id = li["id"]
                url='http://jysggzy.jieyang.gov.cn/api/ords/epfcms/cmsItem/queryCmsItemDetails/'+id
                if tool.Transformation(date) <= tool.Transformation(date_Today):
                    if tool.removal(title, date):
                        self.parse_detile(title, url, date_Today,id)
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
                break
    def parse_detile(self, title, url, date,id):
        print(url)
        t = requests.get(url=url, headers=self.headers)
        url_html = t.json()
        text_name = url_html["items"][0]["name"]
        name = quote(text_name)
        text_url=f'http://jysggzy.jieyang.gov.cn/#/noticeDetail?name={name}&id={id}'
        detail=url_html["items"][0]["clob_lob_content"]
        item = {}
        item['title'] = title.replace('\u2022', '')
        item['url'] = text_url
        item['date'] = date
        item['typeid'] = tool.get_typeid(item['title'])
        item['senddate'] = int(time.time())
        item['mid'] = 867
        item['nativeplace'] = self.get_nativeplace(item['title'])
        item['infotype'] = tool.get_infotype(item['title'])
        item['body'] = detail
        # item['body'] = tool.update_img(self.domain_name, item['body'])
        item['endtime'] = tool.get_endtime(detail)
        if item['endtime'] == '':
            item['endtime'] = int(time.mktime(time.strptime(date, "%Y-%m-%d")))
        else:
            try:
                item['endtime'] = int(time.mktime(time.strptime(item['endtime'], "%Y-%m-%d")))
            except:
                item['endtime'] = int(time.mktime(time.strptime(date, "%Y-%m-%d")))
        item['tel'] = tool.get_tel(detail)
        item['email'] = ''
        item['address'] = tool.get_address(detail)
        item['linkman'] = tool.get_linkman(detail)
        item['function'] = tool.get_function(detail)
        item['resource'] = '揭阳市公共资源交易平台'
        item['shi'] = 10003
        item['sheng'] = 10000
        item['removal']= title
        process_item(item)
        # print(item['body'])

    def get_nativeplace(self, addr):
        city = ''
        city_list = [['10003.001', '罗湖区'], ['10003.002', '福田区'], ['10003.003', '南山区'], ['10003.004', '宝安区'], ['10003.005', '龙岗区'], ['10003.006', '盐田区'], ['10003.007', '坪山区']]

        for i in city_list:
            if i[1] in addr:
                city = float(i[0])
                break
        if city == '':
            city = 10003
        return city

if __name__ == '__main__':
    import traceback,os
    try:
        jl = wenshan_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
        tool.send_error('报错文件：'+str(os.path.basename(__file__))+'报错信息：'+str(e))


