# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 长沙市公共资源交易平台
class changsha_ggzy:
    def __init__(self):
        self.url_list = [
            # 房屋市政
            'http://fwpt.csggzy.cn/jyxxfjsz/index_{}.jhtml',
            # 交通工程
            'http://fwpt.csggzy.cn/jyxxjtgc/index_{}.jhtml',
            # 水利工程
            'http://fwpt.csggzy.cn/jyxxslgc/index_{}.jhtml',
            # 政府采购
            'http://fwpt.csggzy.cn/jyxxzfcg/index_{}.jhtml',
            # 医药采购
            'http://fwpt.csggzy.cn/jyxxyycg/index_{}.jhtml'
        ]
        self.url = self.url_list.pop(0)
        self.headers = {
            'Cookie': 'clientlanguage=zh_CN; UM_distinctid=171539a4000b4-010dd0dbd9aa7d-e343166-1fa400-171539a4001385; CNZZDATA1275214221=535071822-1586244446-%7C1586244446; JSESSIONID=2F8F9B658EDEF12C505618EFF2CCB5D2',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        }

    def parse(self):
        date = tool.date
        # date = '2020-04-02'
        page = 0
        while True:
            page += 1
            text = tool.requests_get(self.url.format(page), self.headers)
            print('*' * 20, page, '*' * 20)
            html = HTML(text)
            # print(11, res)
            # time.sleep(6666)
            detail = html.xpath('/html/body/div[4]/div[4]/div/div[3]/div[2]/ul/li')
            for li in detail:
                title = li.xpath('./p[1]/a/@title')[0]
                url = 'http://fwpt.csggzy.cn' + li.xpath('./p[1]/a/@href')[0]
                date_Today = li.xpath('./p[2]/text()')[0]
                # print(title, url, date_Today)
                # time.sleep(666)
                if '测试' in title:
                    continue
                if tool.Transformation(date) <= tool.Transformation(date_Today):
                    if tool.removal(title, date):
                        self.parse_detile(title, url, date_Today)
                    else:
                        print('【existence】', url)
                        continue
                else:
                    print('日期不符, 正在切换类型', date_Today)
                    self.url = self.url_list.pop(0)
                    page = 0
                    break
            if page == 20:
                self.url = self.url_list.pop(0)
                break

    def parse_detile(self, title, url, date):
        print(url)
        url_html = etree.HTML(tool.requests_get(url, self.headers))
        detail = url_html.xpath('//*[@id="printArea"]')[0]
        detail_html = etree.tostring(detail, method='HTML')
        detail_html = html.unescape(detail_html.decode())
        detail_text = url_html.xpath('string(//*[@id="printArea"])').replace('\xa0', '').replace('\n', '').\
            replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
        # print(detail_text.replace('\xa0','').replace('\xa5',''))
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
        item['body'] = detail_html
        width_list = re.findall('width="(.*?)"', item["body"])
        for i in width_list:
            item["body"] = item["body"].replace('width="{}"'.format(i), '')
        width_list = re.findall('WIDTH: (.*?)pt;', item["body"])
        for i in width_list:
            item["body"] = item["body"].replace('WIDTH: {}pt;'.format(i), '')
        width_list = re.findall('width: (.*?)px;', item["body"])
        for i in width_list:
            item["body"] = item["body"].replace('width: {}px;'.format(i), '')
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
        item['winner'] = tool.get_winner(detail_text)
        item['address'] = tool.get_address(detail_text)
        item['linkman'] = tool.get_linkman(detail_text)
        item['function'] = tool.get_function(detail_text)
        item['resource'] = '长沙市公共资源交易平台'
        item['shi'] = 9501
        item['sheng'] = 9500
        item['removal']= title
        process_item(item)

    def get_nativeplace(self, addr):
        city = ''
        city_list = [['9501.001', '芙蓉区'], ['9501.002', '天心区'], ['9501.003', '岳麓区'], ['9501.004', '开福区'], ['9501.005', '雨花区'], ['9501.006', '长沙县'], ['9501.007', '望城县'], ['9501.008', '宁乡县'], ['9501.009', '浏阳市']]
        for i in city_list:
            if i[1] in addr:
                city = float(i[0])
                break
        if city == '':
            city = 9501
        return city

if __name__ == '__main__':

    import traceback,os
    try:
        jl = changsha_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
        tool.send_error('报错文件：'+str(os.path.basename(__file__))+'报错信息：'+str(e))


