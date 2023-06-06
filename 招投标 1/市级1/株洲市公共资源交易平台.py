# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 株洲市公共资源交易平台
class zhuzhou_ggzy:
    def __init__(self):
        self.url_list = [
            # 房屋市政
            'http://www.zzzyjy.cn/016/016001/{}.html',
            # 市政工程
            'http://www.zzzyjy.cn/016/016002/{}.html',
            # 交通
            'http://www.zzzyjy.cn/016/016003/{}.html',
            # 水利水电
            'http://www.zzzyjy.cn/016/016004/{}.html',
            # 其他
            'http://www.zzzyjy.cn/016/016005/{}.html'
        ]
        self.url = self.url_list.pop(0)
        self.headers = {
            # 'Cookie': 'clientlanguage=zh_CN; UM_distinctid=171539a4000b4-010dd0dbd9aa7d-e343166-1fa400-171539a4001385; CNZZDATA1275214221=535071822-1586244446-%7C1586244446; JSESSIONID=2F8F9B658EDEF12C505618EFF2CCB5D2',
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
            detail = html.xpath('//*[@id="main"]/li')
            for li in detail:
                title = li.xpath('./a/@title')[0]
                url = 'http://www.zzzyjy.cn' + li.xpath('./a/@href')[0]
                date_Today = li.xpath('./span/text()')[0]
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
        detail = url_html.xpath('//*[@class="content"]')[0]
        detail_html = etree.tostring(detail, method='HTML')
        detail_html = html.unescape(detail_html.decode())
        detail_text = url_html.xpath('string(//*[@class="content"])').replace('\xa0', '').replace('\n', '').\
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
        item['resource'] = '株洲市公共资源交易平台'
        item['shi'] = 9502
        item['sheng'] = 9500
        item['removal']= title

        process_item(item)

    def get_nativeplace(self, addr):
        city = ''
        city_list = [['9502.001', '荷塘区'], ['9502.002', '芦淞区'], ['9502.003', '石峰区'], ['9502.004', '天元区'], ['9502.005', '株洲县'], ['9502.006', '攸县'], ['9502.007', '茶陵县'], ['9502.008', '炎陵县'], ['9502.009', '醴陵市']]
        for i in city_list:
            if i[1] in addr:
                city = float(i[0])
                break
        if city == '':
            city = 9502
        return city

if __name__ == '__main__':
    jl = zhuzhou_ggzy()
    jl.parse()


