# -*- coding: utf-8 -*-
import json
import re
import time, html
from lxml import etree
import tool
from save_database import process_item

# 仙桃市公共资源交易中心
class alashan_ggzy:
    def __init__(self):
        self.url_code = [
            # '311',
            # '313',
            '314'
        ]
        self.url = self.url_code.pop(0)
        self.headers = {
            'Accept': '*/*',
            'Cookie': 'ASP.NET_SessionId=tgsujrbrp14ppzbj0uuihufp',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
        }

    def parse(self):
        cookie=tool.get_cookie('http://www.xtggzy.com')['ASP.NET_SessionId']
        self.headers['Cookie']='ASP.NET_SessionId='+cookie
        date = tool.date
        # date = '2021-04-14'
        page = 27
        url_to = 'http://www.xtggzy.com/ProjectBuild/List'
        while True:
            page += 1
            print('*' * 20, page, '*' * 20)
            data = {
                'mountType': 314,
                'name': '',
                'page': page,
                'rows': '10'
            }
            # print(data)
            text = tool.requests_post_to(url_to, data, self.headers)
            # print(111, text)
            # time.sleep(666)
            detail = json.loads(text)['rows']
            for li in detail:
                try:
                    title = li['Title']
                    url = 'http://www.xtggzy.com/ProjectBuild/ArticleDetailed?articleId=' + str(li['RId'])
                    date_Today = li['DateTime'].replace('\r', '').replace('\t', '').replace(' ', '')
                    # print(title, url, date_Today)
                    # time.sleep(666)
                    if tool.Transformation(date) <= tool.Transformation(date_Today):
                        # if tool.removal(title, date):
                            self.parse_detile(title, url, date_Today)
                        # else:
                        #     print('【existence】', url)
                        #     continue
                    else:
                        print('日期不符, 正在切换类型...', date_Today)
                        return
                except Exception as e:
                    traceback.print_exc()


    def parse_detile(self, title, url, date):
        print(url)
        url_text = tool.requests_get(url, self.headers)
        url_html = etree.HTML(url_text)
        detail = url_html.xpath('/html/body/div[3]/div/div[2]/div/div[2]')[0]
        detail_html = etree.tostring(detail, method='HTML')
        detail_html = html.unescape(detail_html.decode())
        detail_text = url_html.xpath('string(/html/body/div[3]/div/div[2]/div/div[2])').replace('\xa0', '').replace('\n',
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
        item['nativeplace'] = 9014.001
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
        item['winner'] = tool.get_winner(detail_text)
        item['address'] = tool.get_address(detail_text)
        item['linkman'] = tool.get_linkman(detail_text)
        item['function'] = tool.get_function(detail_text)
        item['resource'] = '仙桃市公共资源交易中心'
        item['shi'] = 9014
        item['sheng'] = 9000
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
