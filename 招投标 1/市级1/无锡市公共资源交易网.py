# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 无锡市公共资源交易网
class baoshan_ggzy:
    def __init__(self):
        self.url_list = [
            'http://xzfw.wuxi.gov.cn/intertidwebapp/xzsp/XzspZyjyzx?chanId=53047&jyly=&pageIndex={}&pageSize=20',
            'http://xzfw.wuxi.gov.cn/intertidwebapp/xzsp/XzspZyjyzx?chanId=53051&jyly=&pageIndex={}&pageSize=20',
            'http://xzfw.wuxi.gov.cn/intertidwebapp/xzsp/XzspZyjyzx?chanId=53054&jyly=&pageIndex={}&pageSize=20',
            'http://xzfw.wuxi.gov.cn/intertidwebapp/xzsp/XzspZyjyzx?chanId=53056&jyly=&pageIndex={}&pageSize=20',
            'http://xzfw.wuxi.gov.cn/intertidwebapp/xzsp/XzspZyjyzx?chanId=53061%2C36908%2C36910%2C36911%2C36912%2C36913%2C36914%2C36918&cgpm=A&jyly=&pageIndex={}&pageSize=20',
            'http://xzfw.wuxi.gov.cn/intertidwebapp/xzsp/XzspZyjyzx?chanId=53062%2C36917%2C36919&cgpm=A&jyly=&pageIndex={}&pageSize=20',
            'http://xzfw.wuxi.gov.cn/intertidwebapp/xzsp/XzspZyjyzx?chanId=53063%2C36915%2C36916&cgpm=A&jyly=&pageIndex={}&pageSize=20',
                         ]
        self.url = self.url_list.pop(0)
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36',
        }

    def parse(self):
        date = tool.date
        # date = '2020-11-03'
        page = 0
        data = {}
        while True:
            page += 1
            text = tool.requests_post(self.url.format(page), data, self.headers)
            print('*' * 20, page, '*' * 20)
            # html = HTML(text)
            # print(11, text)
            # time.sleep(6666)
            detail = json.loads(text)['list']
            for li in detail:
                title = li['title'].replace('\n', '').replace('\r', '')\
                    .replace('\t', '').replace(' ', '').replace('<spanstyle="color:red">', '').replace('</span>', '')
                url = li['url']
                if 'http' not in url:
                    url = 'http://xzfw.wuxi.gov.cn' + url
                date_Today = li['writeTime'].replace('\n', '').replace('\r', '') \
                    .replace('\t', '').replace(' ', '').replace('(', '').replace(')', '')
                content = li['content']
                if '测试' in title:
                    continue
                # print(title, url, date_Today)
                # time.sleep(666)
                if tool.Transformation(date_Today) >= tool.Transformation(date):
                    if tool.removal(title, date):
                        self.parse_detile(title, url, date, content)
                    else:
                        print('【existence】', url)
                        continue
                else:
                    print('日期不符, 正在切换类型', date_Today, self.url)
                    return


    def parse_detile(self, title, url, date, content):
        print(url)
        detail_html = content
        detail_text = ''.join(re.findall('>(.*?)<', content)).replace('\xa0', '').replace('\n',
                                                                                                          ''). \
            replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
        # if len(detail_html) < 300:
        #     return
        # print(111, detail_text.replace('\xa0','').replace('\xa5',''))
        # time.sleep(6666)
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
        item['resource'] = '无锡市公共资源交易网'
        item['shi'] = 5502
        item['sheng'] = 5500
        item['removal']= title
        process_item(item)

    def get_nativeplace(self, addr):
        city = ''
        city_list = [['5502.001', '崇安区'], ['5502.002', '南长区'], ['5502.003', '北塘区'], ['5502.004', '锡山区'], ['5502.005', '惠山区'], ['5502.006', '滨湖区'], ['5502.007', '江阴市'], ['5502.008', '宜兴市']]

        for i in city_list:
            if i[1] in addr:
                city = float(i[0])
                break
        if city == '':
            city = 5502
        return city

if __name__ == '__main__':
    import traceback, os
    try:
        jl = baoshan_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
        tool.send_error('报错文件：'+str(os.path.basename(__file__))+'报错信息：'+str(e))


