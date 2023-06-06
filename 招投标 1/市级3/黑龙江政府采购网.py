# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 必联网
class baoshan_ggzy:
    def __init__(self):
        self.url_list = [
          'http://hljcg.hlj.gov.cn/freecms/rest/v1/notice/selectInfoMoreChannel.do?&siteId=94c965cc-c55d-4f92-8469-d5875c68bd04&channel=c5bff13f-21ca-4dac-b158-cb40accd3035&currPage={}&pageSize=8&noticeType=00101&regionCode=230001&purchaseManner=&title=&openTenderCode=&purchaser=&agency=&purchaseNature=&operationStartTime=&operationEndTime=&selectTimeName=noticeTime'
        ]
        self.url = self.url_list.pop(0)
        self.headers = {
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
            detail = json.loads(text)['data']
            for li in detail:
                title = li['title']
                url = li['htmlpath']
                url_domain = 'http://hljcg.hlj.gov.cn/freecms'
                if 'http' not in url:
                    if '../../' in url:
                        url = url_domain + url[5:]
                    elif '../' in url:
                        url = url_domain + url[2:]
                    elif './' in url:
                        url = url_domain + url[1:]
                    else:
                        url = url_domain + url
                date_Today = li['addtimeStr'].split(' ')[0]
                if '测试' in title:
                    continue
                # print(title, url, date_Today)
                # time.sleep(666)
                if tool.Transformation(date) <= tool.Transformation(date_Today):
                    if tool.removal(title, date):
                        print(url)
                        detail_text =  li['content']

                        item = {}
                        item['title'] = title.replace('\u2022', '')
                        item['url'] = url
                        item['date'] = date
                        item['typeid'] = tool.get_typeid(item['title'])
                        item['senddate'] = int(time.time())
                        item['mid'] = 867
                        item['nativeplace'] = tool.get_city(li['agency'])
                        item['infotype'] = tool.get_infotype(item['title'])
                        item['body'] = tool.qudiao_width(detail_text)
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
                        item['address'] = tool.get_address(detail_text).replace('<em>', '').replace('</em>',
                                                                                                    '').replace('<p>',
                                                                                                                '').replace(
                            '</p>', '')
                        item['linkman'] = tool.get_linkman(detail_text)
                        item['function'] = tool.get_function(detail_text)
                        item['resource'] = '黑龙江政府采购网'
                        item['shi'] = tool.get_city(item['title'])
                        item['sheng'] = tool.get_sheng(item['title'])
                        item['removal'] = title
                        process_item(item)
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
                page = 0

    def parse_detile(self, title, url, date):
        print(url)
        t = tool.requests_get(url, self.headers)
        url_html = etree.HTML(t)
        detail = url_html.xpath('//div[@class="ebnew-details-content mg-t30"]')[0]
        detail_html = etree.tostring(detail, method='HTML')
        detail_html = html.unescape(detail_html.decode()).replace('浏览次数：', '').replace('原文链接', '')
        detail_text = detail_html.replace('\xa0', '').replace('\n', ''). \
            replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
        if len(detail_text) < 300:
            return
        item = {}
        item['title'] = title.replace('\u2022', '')
        item['url'] = url
        item['date'] = date
        item['typeid'] = tool.get_typeid(item['title'])
        item['senddate'] = int(time.time())
        item['mid'] = 867
        item['nativeplace'] = tool.get_city(detail.xpath('//li[6]/span[2]')[0])
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
        item['address'] = tool.get_address(detail_text).replace('<em>','').replace('</em>','').replace('<p>','').replace('</p>','')
        item['linkman'] = tool.get_linkman(detail_text)
        item['function'] = tool.get_function(detail_text)
        item['resource'] = '必联网'
        item['shi'] = tool.get_city(detail.xpath('//li[6]/span[2]')[0])
        item['sheng'] = tool.get_sheng(detail.xpath('//li[6]/span[2]')[0])
        item['removal']= title
        process_item(item)

    def get_nativeplace(self, addr):
        city = ''
        city_list = [['7004.001','梅列区'],['7004.01','泰宁县'],['7004.011','建宁县'],['7004.012','永安市'],['7004.002','三元区'],
    ['7004.003','明溪县'],['7004.004','清流县'],['7004.005','宁化县'],['7004.006','大田县'],['7004.007','尤溪县'],
    ['7004.008','沙　县'],['7004.009','将乐县']]
        for i in city_list:
            if i[1] in addr:
                city = float(i[0])
                break
        if city == '':
            city = 7004
        return city

if __name__ == '__main__':
    import traceback,os
    try:
        jl = baoshan_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
        tool.send_error('报错文件：'+str(os.path.basename(__file__))+'报错信息：'+str(e))



