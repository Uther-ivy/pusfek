# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 漳州市公共资源交易网
class baoshan_ggzy:
    def __init__(self):
        self.url_list = [
            'http://www.zzgcjyzx.com/Front/gcxx/002001/002001001/?Paging={}',
            'http://www.zzgcjyzx.com/Front/gcxx/002001/002001002/?pageing={}',
            'http://www.zzgcjyzx.com/Front/gcxx/002001/002001003/?pageing={}',
            'http://www.zzgcjyzx.com/Front/gcxx/002001/002001005/?pageing={}',
            'http://www.zzgcjyzx.com/Front/gcxx/002002/002002001/?pageing={}',
            'http://www.zzgcjyzx.com/Front/gcxx/002002/002002006/?pageing={}',
            'http://www.zzgcjyzx.com/Front/gcxx/002002/002002002/?pageing={}'
        ]
        self.url = self.url_list.pop(0)
        self.headers = {
            'Cookie': 'homeid=1a444a31-e460-47ff-9931-1c075c0f3cd8',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        }

    def parse(self):
        date = tool.date
        # date = '2020-12-17'
        page = 0
        while True:
            page += 1
            text = tool.requests_get(self.url.format(page), self.headers)
            print('*' * 20, page, '*' * 20)
            html = HTML(text)
            # print(11, text)
            # time.sleep(6666)
            detail = html.xpath('/html/body/table/tr/td[2]/table/tr/td[4]/table/tr[2]/td/table/tr')
            for li in detail:
                title = li.xpath('./td[2]/a/@title')[0].replace('\n', '').replace('\t', '').replace(' ', '').replace(
                    '\r', '')
                url = li.xpath('./td[2]/a/@href')[0]
                url_domain = 'http://www.zzgcjyzx.com'
                if 'http' not in url:
                    if '../../' in url:
                        url = url_domain + url[5:]
                    elif '../' in url:
                        url = url_domain + url[2:]
                    elif './' in url:
                        url = url_domain + url[1:]
                    else:
                        url = url_domain + url
                date_Today = li.xpath('./td[3]/text()')[0].replace('\n', '').replace('\t', '').replace(' ', '').replace(
                    '\r', '')
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
                    return


    def parse_detile(self, title, url, date):
        print(url)
        t = tool.requests_get(url, self.headers)
        url_html = etree.HTML(t)
        detail = url_html.xpath('//*[@id="tblInfo"]')[0]
        detail_html = etree.tostring(detail, method='HTML')
        detail_html = html.unescape(detail_html.decode()).split('<!--正文结束-->')[0] + '</div>'
        detail_text = url_html.xpath('string(//*[@id="tblInfo"])').replace('\xa0', '').replace('\n', ''). \
            replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
        if len(detail_text) < 100:
            return
        item = {}
        item['title'] = title.replace('\u2022', '')
        item['url'] = url
        item['date'] = date
        item['typeid'] = tool.get_typeid(item['title'])
        item['senddate'] = int(time.time())
        item['mid'] = 867
        item['nativeplace'] = self.get_nativeplace(item['title'])
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
        item['resource'] = '漳州市公共资源交易网'
        item['shi'] = 7006
        item['sheng'] = 7000
        item['removal']= title
        process_item(item)

    def get_nativeplace(self, addr):
        city = ''
        city_list = [['7006.001', '芗城区'], ['7006.01', '华安县'], ['7006.011', '龙海市'], ['7006.002', '龙文区'],
                     ['7006.003', '云霄县'], ['7006.004', '漳浦县'], ['7006.005', '诏安县'], ['7006.006', '长泰县'],
                     ['7006.007', '东山县'], ['7006.008', '南靖县'], ['7006.009', '平和县']]
        for i in city_list:
            if i[1] in addr:
                city = float(i[0])
                break
        if city == '':
            city = 7006
        return city

if __name__ == '__main__':
    import traceback, os
    try:
        jl = baoshan_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
        tool.send_error('报错文件：'+str(os.path.basename(__file__))+'报错信息：'+str(e))


