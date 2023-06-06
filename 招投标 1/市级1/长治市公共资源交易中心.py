# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 长治市公共资源交易中心
class changzhi_ggzy:
    def __init__(self):
        self.url_list = [
            # 工程建设
            'http://ggzy.changzhi.gov.cn/jyxxJsgc/index_{}.htm',
            # 政府采购
            'http://ggzy.changzhi.gov.cn/jyxxZfcg/index_{}.htm',
        ]

        self.url = self.url_list.pop(0)
        self.headers = {
            'Cookie': 'clientlanguage=zh_CN; _gscu_447861846=79416540s5m7l121; _gscbrs_447861846=1; _gscs_447861846=794165404190o821|pv:4',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        }

    def parse(self):
        date = tool.date
        # date = '2021-08-03'
        page = 0
        while True:
            page += 1
            text = tool.requests_get(self.url.format(page), self.headers)
            print('*' * 20, page, '*' * 20)
            html = HTML(text)
            detail = html.xpath('//*[@id="main"]/div/div[4]/ul[2]/li')
            for li in detail:
                title = li.xpath('./a/@title')[0]
                url = 'http://ggzy.changzhi.gov.cn' + li.xpath('./a/@href')[0]
                url = re.findall('http.*?htm', url)[0]
                date_Today = li.xpath('./span/text()')[0]
                # print(title, url, date_Today)
                # time.sleep(666)
                if tool.Transformation(date) <= tool.Transformation(date_Today):
                    if tool.removal(title, date):
                        self.parse_detile(title, url, date_Today)
                    else:
                        print('【existence】', url)
                        continue
                else:
                    print('日期不符, 正在切换类型...', date_Today)

                    return
            if page == 20:
                self.url = self.url_list.pop(0)
                break
    def parse_detile(self, title, url, date):
        print(url)
        url_html = etree.HTML(tool.requests_get(url, self.headers))
        detail = url_html.xpath('//*[@id="main"]/div/div[3]/div[2]')[0]
        detail_html = etree.tostring(detail, method='HTML')
        detail_html = html.unescape(detail_html.decode())
        detail_text = url_html.xpath('string(//*[@id="main"]/div/div[3]/div[2])').replace('\xa0', '').replace('\n', '').\
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
        item['resource'] = '长治市公共资源交易中心'
        item['shi'] = 2504
        item['sheng'] = 2500
        item['removal']= title
        process_item(item)

    def get_nativeplace(self, addr):
        city = ''
        city_list = [['2504.001', '城区'], ['2504.01', '武乡县'], ['2504.011', '沁县'], ['2504.012', '沁源县'], ['2504.013', '潞城市'], ['2504.002', '郊区'], ['2504.003', '长治县'], ['2504.004', '襄垣县'], ['2504.005', '屯留县'], ['2504.006', '平顺县'], ['2504.007', '黎城县'], ['2504.008', '壶关县'], ['2504.009', '长子县']]
        for i in city_list:
            if i[1] in addr:
                city = float(i[0])
                break
        if city == '':
            city = 2504
        return city
if __name__ == '__main__':
    import traceback, os

    try:
        jl = changzhi_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
        tool.send_error('报错文件：'+str(os.path.basename(__file__))+'报错信息：'+str(e))


