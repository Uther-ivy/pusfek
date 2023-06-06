# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item


# 国投集团电子采购平台
class baoshan_ggzy:
    def __init__(self):
        self.url_list = [
            'https://www.sdicc.com.cn/cgxx/ggList?caiGouType=1',

        ]
        self.url = self.url_list.pop(0)
        self.headers = {
            # 'Cookie': 'homeid=1a444a31-e460-47ff-9931-1c075c0f3cd8',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        }

    def Transformation(self, date):
        """日期转时间戳"""
        timeArray = time.strptime(date, "%d-%Y-%m")
        timeStamp = int(time.mktime(timeArray))
        return timeStamp

    def parse(self):
        while True:
            date = tool.date
            # date='2021-04-20'
            text = tool.requests_get(self.url, self.headers)
            # print(text)
            html = HTML(text)
            detail = html.xpath('//div[@class="tbody"]//tr')

            # print(de)
            for li in range(len(detail)):
                # print(html.xpath('(//table[@id="dataTable"]//tr//@id)[1]'))
                # url= 'http://www.jyggjy.cn/'+html.xpath(f'(//div[@class="tbody"]//tr//@onclick)[{li+1}]')[0].split(',')[0].replace('(','').replace("'",'')
                ggGuid = html.xpath(f'(//div[@class="tbody"]//tr//@onclick)[{li + 1}]')[0].split(',')[0].replace('(',
                                                                                                                 '').replace(
                    "'", '').replace('urlChange', '')
                gcGuid = html.xpath(f'(//div[@class="tbody"]//tr//@onclick)[{li + 1}]')[0].split(',')[1].replace(')',
                                                                                                                 '').replace(
                    "'", '')
                url = f'https://www.sdicc.com.cn/cgxx/ggDetail?gcGuid={gcGuid}&ggGuid={ggGuid}'
                # urls_=re.findall("view\('(.*?)','(.*?)'\);",urls)
                # print(urls_)
                title = ''.join(html.xpath(f'((//div[@class="tbody"]//tr)[{li + 1}]//span)[1]//text()')).strip()
                #
                date_Today = html.xpath(f'((//div[@class="tbody"]//tr)[{li + 1}]//span)[3]//text()')[0].replace('[',
                                                                                                                '').replace(
                    ']', '').strip()
                # print(li+1,url,title,date_Today)
                if '发布' in date_Today:
                    continue
                # month=re.findall('(\d*)-\d*-\d*',date_Today)
                # day=re.findall('\d*-(\d*)-\d*',date_Today)
                # print(month,day)
                if '测试' in title:
                    continue
                # urls=re.findall("(.*?)\(\'(.*?)\'\)",url)[0]
                # url='http://ggzy.qqhr.gov.cn'+url
                print(title, url, date_Today)
                #
                # # time.sleep(666)
                if tool.Transformation(date) <= tool.Transformation(date_Today):
                    if tool.removal(title, date):
                        self.parse_detile(title, url, date_Today)
                    else:
                        print('【existence】', url)
                        continue
                else:
                    # print(tool.Transformation(date),self.Transformation(date_Today))
                    print('日期不符, 正在切换类型', date_Today, self.url)
                    self.url = self.url_list.pop(0)
                    page = 0
                    continue
            self.url = self.url_list.pop(0)

    def parse_detile(self, title, url, date):
        t = tool.requests_get(url, self.headers)
        url_html = etree.HTML(t)
        detail = url_html.xpath('//div[@class="dg-flex-item"]')[0]
        # print(detail)
        detail_html = etree.tostring(detail, method='HTML')
        detail_html = html.unescape(detail_html.decode())
        detail_text = url_html.xpath('string(//div[@class="dg-flex-item"])').replace('\xa0', '').replace('\n', ''). \
            replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
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
            item['nativeplace'] = tool.more(item['title']+detail_text)
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
        item['resource'] = '国投集团电子采购平台'
        if '.' in str(item["nativeplace"]):
            item["shi"] = int(float(str(item["nativeplace"]).replace("['", "").split('.')[0]))
        else:
            item["shi"] = int(float(item["nativeplace"]))
        if len(str(int(item["shi"]))) == 4:
            item['sheng'] = int(str(item["shi"])[:2] + '00')
        elif len(str(int(item["shi"]))) == 5:
            item['sheng'] = int(str(item["shi"])[:3] + '00')
        else:
            item['sheng'] = 0
        # print(item)
        item['removal'] = title
        process_item(item)


if __name__ == '__main__':

    import traceback, os

    try:
        jl = baoshan_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
