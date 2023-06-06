# -*- coding: utf-8 -*-
import json
import re
import time, html
from lxml import etree
import tool
from save_database import process_item

# 射阳县人民政府
class alashan_ggzy:
    def __init__(self):
        self.url_code = [
            'http://sheyang.yancheng.gov.cn/module/web/jpage/dataproxy.jsp?startrecord={}&endrecord={}&perpage=15&col=1&appid=1&webid=55&path=%2F&columnid=30516&sourceContentType=1&unitid=32978&webname=%E5%B0%84%E9%98%B3%E5%8E%BF%E4%BA%BA%E6%B0%91%E6%94%BF%E5%BA%9C&permissiontype=0',
            'http://sheyang.yancheng.gov.cn/module/web/jpage/dataproxy.jsp?startrecord={}&endrecord={}&perpage=15&col=1&appid=1&webid=55&path=%2F&columnid=30517&sourceContentType=1&unitid=32978&webname=%E5%B0%84%E9%98%B3%E5%8E%BF%E4%BA%BA%E6%B0%91%E6%94%BF%E5%BA%9C&permissiontype=0',
            'http://sheyang.yancheng.gov.cn/module/web/jpage/dataproxy.jsp?startrecord={}&endrecord={}&perpage=14&col=1&appid=1&webid=55&path=%2F&columnid=16537&sourceContentType=1&unitid=32978&webname=%E5%B0%84%E9%98%B3%E5%8E%BF%E4%BA%BA%E6%B0%91%E6%94%BF%E5%BA%9C&permissiontype=0',
            'http://sheyang.yancheng.gov.cn/module/web/jpage/dataproxy.jsp?startrecord={}&endrecord={}&perpage=14&col=1&appid=1&webid=55&path=%2F&columnid=16541&sourceContentType=1&unitid=32978&webname=%E5%B0%84%E9%98%B3%E5%8E%BF%E4%BA%BA%E6%B0%91%E6%94%BF%E5%BA%9C&permissiontype=0',
            'http://sheyang.yancheng.gov.cn/module/web/jpage/dataproxy.jsp?startrecord={}&endrecord={}&perpage=14&col=1&appid=1&webid=55&path=%2F&columnid=16539&sourceContentType=1&unitid=32978&webname=%E5%B0%84%E9%98%B3%E5%8E%BF%E4%BA%BA%E6%B0%91%E6%94%BF%E5%BA%9C&permissiontype=0',
            'http://sheyang.yancheng.gov.cn/module/web/jpage/dataproxy.jsp?startrecord={}&endrecord={}&perpage=14&col=1&appid=1&webid=55&path=%2F&columnid=16540&sourceContentType=1&unitid=32978&webname=%E5%B0%84%E9%98%B3%E5%8E%BF%E4%BA%BA%E6%B0%91%E6%94%BF%E5%BA%9C&permissiontype=0',
        ]
        self.url = self.url_code.pop(0)
        self.headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Cookie': 'isInitAreaCode=null; _gscu_653689772=78282348u2bs1g18; _gscbrs_653689772=1; UM_distinctid=16f78f570621fa-0e76a94f9f3d2d-e343166-1fa400-16f78f570631fc; _gscs_653689772=t782895054fvlkv12|pv:14; CNZZDATA1260595804=985342442-1578282342-%7C1578291895',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
        }

    def parse(self):
        date = tool.date
        # date = '2021-04-02'
        page = 0
        while True:
            page += 1
            print('*' * 20, page, '*' * 20)
            # print(self.url.format(1+42*(page-1), 42*page))
            text = tool.requests_get(self.url.format(1+42*(page-1), 42*page), self.headers)
            detail = re.findall('<li><a href="(.*?)" target="_blank".*? title="(.*?)">.*?</a>(.*?)</li>', text, re.S)
            # print(111, detail_ls)
            # time.sleep(666)
            for url,title, date_Today in detail:
                url = 'http://sheyang.yancheng.gov.cn' + url
                date_Today = date_Today.replace('[', '').replace(']', '').replace(' ', '')
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
                    print(self.url)
                    page = 0

                    break
                    # break


    def parse_detile(self, title, url, date):
        print(url)
        url_text = tool.requests_get(url, self.headers)
        url_html = etree.HTML(url_text)
        detail = url_html.xpath('//*[@id="zoom"]')[0]
        detail_html = etree.tostring(detail, method='HTML')
        detail_html = html.unescape(detail_html.decode())
        detail_text = url_html.xpath('string(//*[@id="zoom"])').replace('\xa0', '').replace('\n', '').replace('\r', '').replace('\t',
                                                                                                                  '').replace(
            ' ', '').replace('\xa5', '')
        item = {}
        item['title'] = title.replace('\u2022', '')
        item['url'] = url
        item['date'] = date
        item['typeid'] = tool.get_typeid(item['title'])
        item['senddate'] = int(time.time())
        item['mid'] = 867
        item['nativeplace'] = 5509.006
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
        item['resource'] = '射阳县人民政府'
        item['shi'] = 5509
        item['sheng'] = 5500
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
