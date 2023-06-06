# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 中国邮政
class baoshan_ggzy:
    def __init__(self):
        self.url_list = [
            # 'http://www.chinapost.com.cn/html1/category/181313/7294-1.htm',
            # 'http://www.chinapost.com.cn/html1/category/181313/7290-1.htm',
            # 'http://www.chinapost.com.cn/html1/category/181313/7295-1.htm',
            # 'http://www.chinapost.com.cn/html1/category/181313/7297-1.htm',
            # 'http://www.chinapost.com.cn/html1/category/181313/7300-1.htm',
            'http://www.chinapost.com.cn/html1/category/181313/7302-{}.htm',
            # 'http://www.chinapost.com.cn/html1/category/181313/7304-1.htm',
            # 'http://www.chinapost.com.cn/html1/category/181392/1124-1.htm',

        ]
        self.url = self.url_list.pop(0)
        self.headers = {
            # 'Cookie': 'homeid=1a444a31-e460-47ff-9931-1c075c0f3cd8',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        }

    def parse(self):
        date = tool.date
        page = 0
        while True:
            page+=1
            print('*'*30,page,'*'*30)
            # date = '2021-07-21'
            text = tool.requests_get(url=self.url.format(page), headers=self.headers)
            html = HTML(text)
            detail = html.xpath('//div[@class="new_list"]//li')
            for li in range(len(detail)-1):
                print(li)
                url = html.xpath(f'(//span[@id="ReportIDname"]//a//@href)[{li+1}]')[0]
                title = html.xpath(f'(//span[@id="ReportIDname"]//a//text())[{li+1}]')[0]
                date_Today = html.xpath(f'(//span[@id="ReportIDIssueTime"]//text())[{li+1}]')[0]
                if '测试' in title:
                    continue
                url_domain = 'http://www.chinapost.com.cn'
                if 'http' not in url:
                    if '../../' in url:
                        url = url_domain + url[5:]
                    elif '../' in url:
                        url = url_domain + url[2:]
                    elif './' in url:
                        url = url_domain + url[1:]
                    else:
                        url = url_domain + url
                # print(title, url, date_Today)
                # # time.sleep(666)
                if tool.Transformation(date) <= tool.Transformation(date_Today):
                    # if tool.removal(title, date):
                    self.parse_detile(title, url, date_Today)
                # else:
                #     print('【existence】', url)
                #     continue
                else:
                    print('日期不符, 正在切换类型', date_Today, self.url)
                    return


    def parse_detile(self, title, url, date):
        t = tool.requests_get(url, self.headers)
        url_html = etree.HTML(t)
        detail = url_html.xpath('//span[@id="ReportIDtext"]')[0]
        # print(detail)
        detail_html = etree.tostring(detail, method='HTML')
        detail_html = html.unescape(detail_html.decode())
        detail_text = url_html.xpath('string(//span[@id="ReportIDtext"])').replace('\xa0', '').replace('\n', ''). \
            replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
        # if len(detail_text) < 100:
        #     return
        item = {}
        item['title'] = title.replace('\u2022', '')
        item['url'] = url
        item['date'] = date
        item['typeid'] = tool.get_typeid(item['title'])
        item['senddate'] = int(time.time())
        item['mid'] = 867
        item['infotype'] = tool.get_infotype(item['title'])
        item['body'] = tool.qudiao_width(detail_html)
        item['endtime'] = tool.get_endtime(detail_text)
        item['nativeplace'] = tool.get_title_city(item['title'])
        if item['nativeplace'] == 0:
            item['nativeplace'] = tool.more(item['title']+ detail_text)
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
        item['resource'] = '中国邮政网'
        if '.' in str(item["nativeplace"]):
            item["shi"] = int(float(str(item["nativeplace"]).replace("['","").split('.')[0]))
        else:
            item["shi"] = int(float(item["nativeplace"]))
        if len(str(int(item["shi"]))) == 4:
            item['sheng'] = int(str(item["shi"])[:2] + '00')
        elif len(str(int(item["shi"]))) == 5:
            item['sheng'] = int(str(item["shi"])[:3] + '00')
        else:
            item['sheng'] = 0
        # print(item)
        item['removal']= title
        process_item(item)

    # def get_nativeplace(self, addr):
    #     city = ''
    #     city_list = [['5509.005', '阜宁县']]
    #
    #     for i in city_list:
    #         if i[1] in addr:
    #             city = float(i[0])
    #             break
    #     if city == '':
    #         city = 7008
    #     return city

if __name__ == '__main__':

    import traceback, os
    try:
        jl = baoshan_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
        tool.send_error('报错文件：'+str(os.path.basename(__file__))+'报错信息：'+str(e))


