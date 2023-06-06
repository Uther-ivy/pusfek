# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 国际机电设备招标采购平台
class wenshan_ggzy:
    def __init__(self):
        self.url_list = [
            'https://www.chinamae.com/purchases/category/2', #招标公告
                    ]
        self.url = self.url_list.pop(0)
        self.headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
    'Cookie': '__bid_n=187694aa79249578884207; __51cke__=; FPTOKEN=b6CfE4GIKCkc6SUtvqUfeNXv8lRL6dH8bxDZsltY4AkLlTRgQeRNAgE8q/9jqNN6ZJDwv9D5L7O3yZiPLt6qcWTLYJiqXOm1ZO5Hze3DB5o5YIm/einQDQ3qmZFFZ2FXmWn6WkbAMtaMloPHNlwmv8p+nNvf2YWyzZ82RBJtVmqMRUjY83tebJwiVrcpG1WpQdo8eaiKj15dPO3PfngufyqRF8JQ8435ySznrFygbIeVtXFbVeEBvLCLJ9IuLSWVKXQSJg4xOSq0aGrxYLWD5qbfZuLPX1vYYmUQnmVErueRnPNGCsn8fNsIny0vFNbbHNYT9zi++hfaZCybO+3t5Hk4XlUra80glVWm7e5X0CvcSrjkwIZSs3MQXjh2VIEEfMiDWyMF8O8HSa1r+cirGw==|g4Ia+vSzNNu3/L2lXw3FPDpZiZg51UqD/C67B+Ym+EM=|10|9ab23c78b09b61f08b8d66496f6621de; __tins__20730959=%7B%22sid%22%3A%201681266215863%2C%20%22vd%22%3A%203%2C%20%22expires%22%3A%201681268114881%7D; __51laig__=3; XSRF-TOKEN=eyJpdiI6IlpjUHhrMWdHOUxuMUJZMGRKelpFa0E9PSIsInZhbHVlIjoibnhiaDhKNHJFS25JQWYyVWVXTGRCTHhcL1puZkxMVVZJdHZFYUoxY3NcL3d2cUhxRUJra3NrXC9xVWh1TFhYcis1TkFtUzdia1o5XC90M2IyTCtDSjc1TjZBPT0iLCJtYWMiOiI2ZTY0Zjg2YmY0ZGQ4NDlhODQ3ZjQxNWI3Y2QxZjA2YWQwYTg0MThjODEwMzIwZGUxYzcxNTI2MjA4NTQ5MjgwIn0%3D; laravel_session=eyJpdiI6IjVqVVU5QXQ4T3kxYnVvaW5VV3hrcEE9PSIsInZhbHVlIjoieGh6WkhNbGtaY1dmdzJZMDY1RjNKWlVoeEZXdm1QaEpOSGVEOUh2cDBFWWk3TXRkVnc5bFo3cU1Vb3ZcL2FGMXdTOHFldHRFMHJxMnpMdE9KTTJlMXhnPT0iLCJtYWMiOiIxNGJkZWJhNTU0YzkyZjg4YTNhZTU3MDk3M2M4YjFkMzc3NjIzZGU0YWEyODU3MTk4YTZkOTlmMzFlYWRjZWUwIn0%3D'
}
    def parse(self):
        date = tool.date
        # date = '2020-09-21'
        page = 2
        while True:
            page += 1
            data = {
                "_token": "bgDreTCRpkhZYlrBH40kWATnsGtSGYOOvBHo9U4i",
                "province": "0",
                "city": "0",
                "county": "0",
                "period": "0",
                "scout": "",
                "page": page,
                "totalPages": "481813"
            }
            text = tool.requests_post(url=self.url, headers=self.headers,data=data)
            print('*' * 20, page, '*' * 20)
            html = HTML(text)
            # print(11, text)
            # time.sleep(6666)

            detail = html.xpath('//div[@class="list"]/ul/li')
            for li in detail:
                title = li.xpath('./a/@title')[0]
                href = li.xpath('./a/@href')[0]
                date_Today=time.strftime('%Y-%m-%d')
                url = 'https://www.chinamae.com' + href
                # print(title, url, date_Today)
                # time.sleep(666)
                # self.parse_detile(title, url, date_Today)
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
                print('日期不符, 正在切换类型')
                self.url = self.url_list.pop(0)
                break

    def parse_detile(self, title, url, date):
        print(url)
        t = tool.requests_get(url, self.headers)
        # print(t)
        # time.sleep(2222)
        url_html = etree.HTML(t)
        detail = url_html.xpath('//div[@class="content"]')[0]
        detail_html = etree.tostring(detail, method='HTML')
        detail_html = html.unescape(detail_html.decode()).replace("display: none", '')
        detail_text = url_html.xpath('string(//div[@class="content"])').replace('\xa0', '').replace('\n', ''). \
            replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
        if len(t) < 200:
            int('a')
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
        item['resource'] = '国际机电设备招标采购平台'
        item['shi'] = 6507
        item['sheng'] = 6500
        item['removal'] = title
        # print(item)
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



