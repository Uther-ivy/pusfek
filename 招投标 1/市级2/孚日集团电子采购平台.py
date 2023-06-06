# -*- coding: utf-8 -*-
import json
import re
import time, html
from lxml import etree
import tool
from save_database import process_item

# 孚日集团电子采购平台
class alashan_ggzy:
    def __init__(self):
        self.url_code = [
            'http://tender.sunvim.com:8081/BasicData/Site/NewsList/{}?k=f86Jg1QShHZsPoaJQMWz2iST898ktVceHrA8ZqvwjUfcMeimJYP1dJdNfDJPUKxr',
            'http://tender.sunvim.com:8081/HomeSite/Site/NewsList/{}?k=f86Jg1QShHaeWOfo6kk49SST898ktVceHrA8ZqvwjUfcMeimJYP1dJdNfDJPUKxr',
            'http://tender.sunvim.com:8081/BasicData/Site/NewsList/{}?k=f86Jg1QShHbJCZx1w5cS%2BCST898ktVceHrA8ZqvwjUfcMeimJYP1dJdNfDJPUKxr'
        ]
        self.url = self.url_code.pop(0)
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Cookie': 'ASP.NET_SessionId=n0wcug5mcnxe4hhpguvv4oal; LastCookie=2021/4/14 14:43:06',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
        }

    def parse(self):
        date = tool.date
        # date = '2021-04-12'
        page = 0
        while True:
            page += 1
            print('*' * 20, page, '*' * 20)
            text = tool.requests_get(self.url.format(page), self.headers)
            detail = etree.HTML(text).xpath('//*[@id="form1"]/div[3]/div/div[2]/ul[2]/li')
            if len(detail) == 0:
                self.url = self.url_code.pop(0)
                page = 0
                continue
            for li in detail:
                title = li.xpath('./a/@title')[0]
                url = 'http://tender.sunvim.com:8081' + li.xpath('./a/@href')[0]
                date_Today = li.xpath('./span[1]/text()')[0]
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
                    self.url = self.url_code.pop(0)
                    page = 0
                    break
            if page == 20:
                self.url = self.url_code.pop(0)
                break

    def parse_detile(self, title, url, date):
        print(url)
        url_text = tool.requests_get(url, self.headers)
        url_html = etree.HTML(url_text)
        detail = url_html.xpath('//*[@id="divContent"]')[0]
        detail_html = etree.tostring(detail, method='HTML')
        detail_html = html.unescape(detail_html.decode()).replace('\xa0', '')
        detail_text = url_html.xpath('string(//*[@id="divContent"])').replace('\xa0', '').replace('\n',
                                                                                                           '').replace(
            '\r', '').replace('\t',
                              '').replace(
            ' ', '').replace('\xa5', '')
        item = {}
        item['title'] = title.replace('\u2022', '')
        item['url'] = url
        item['date'] = date
        item['typeid'] = tool.get_typeid(item['title'])
        item['senddate'] = int(time.time())
        item['mid'] = 867
        item['nativeplace'] = float(tool.get_title_city(item['title']))
        if item['nativeplace'] == 0:
            item['nativeplace'] = float(tool.more(item['title']+detail_text))
        item['infotype'] = tool.get_infotype(item['title'])
        item['body'] = tool.qudiao_width(detail_html)
        item['body'] = item['body'].replace('''<a href="javascript:SignUp();" class="btn btn-danger btn-sm">报名参加</a>''', '')
        item['body'] = item['body'].replace('''<a href="javascript:BackOption();" class="btn btn-default btn-sm">返回</a>''', '')
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
        item['resource'] = '孚日集团电子采购平台'
        item["shi"] = int(item["nativeplace"])
        if len(str(item["nativeplace"])) == 4:
            item['sheng'] = int(str(item["nativeplace"])[:2] + '00')
        elif len(str(item["nativeplace"])) == 5:
            item['sheng'] = int(str(item["nativeplace"])[:3] + '00')
        else:
            item['sheng'] = 0
        item['removal']= title
        process_item(item)
        # print(item['nativeplace'], item['title'])

if __name__ == '__main__':
    import traceback, os
    try:
        jl = alashan_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
        if 'pop from empty list'!=str(e):
            print('报错')
            traceback.print_exc()
            with open('../error_name.txt', 'a+', encoding='utf-8')as f:
                f.write(str(os.path.basename(__file__)))
                f.write('\n')
                f.write(str(traceback.format_exc()))
                f.write('\n')
        else:
            with open('../success.txt', 'a+', encoding='utf-8')as f:
                f.write(str(os.path.basename(__file__)))
                f.write('\n')
                f.write(str('无连接抓取'))
                f.write('\n')

