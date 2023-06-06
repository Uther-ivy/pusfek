# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 中核集团电子采购平台
class baoshan_ggzy:
    def __init__(self):
        # self.url_list = [
            # 'https://www.cnncecp.com/xfzbgg/index.jhtml',
            # 'https://www.cnncecp.com/zhfcghxr/index.jhtml',
            # 'https://www.cnncecp.com/zhfcgjg/index.jhtml',
            # 'https://www.cnncecp.com/zhfzzgg/index.jhtml'

        # ]
        # self.url = self.url_list.pop(0)
        self.headers = {
            # 'Cookie': 'homeid=1a444a31-e460-47ff-9931-1c075c0f3cd8',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        }

    def parse(self):
        date = tool.date
        page=0
        while True:
            page+=1
            print('*' * 20, page, '*' * 20)

            if page==1:
                url='https://www.cnncecp.com/zhzbjggs/index.jhtml'
            else:
                url= f'https://www.cnncecp.com/zhzbjggs/index_{page}.jhtml'
            text = tool.requests_get(url,self.headers)
            # print(text)
            html = HTML(text)
            detail = html.xpath('//div[@class="List1"]//li')

            # print(de)
            for li in range(len(detail)):
                try:
                    # print(html.xpath('(//table[@id="dataTable"]//tr//@id)[1]'))
                    url= html.xpath(f'(//div[@class="List1"]//li//a//@href)[{li+1}]')[0]
                    title = ''.join(html.xpath(f'(//div[@class="List1"]//li//a//text())[{li+1}]')).strip()
                    date_Today = html.xpath(f'(//div[@class="List1"]//li//span[@class="Right Gray"]//text())[{li+1}]')[0].replace('\r','').replace('\n','').strip().split(' ')[0].strip().replace('/','-')
                    if '发布' in date_Today:
                        continue
                    if '测试' in title:
                        continue
                    url='https://www.cnncecp.com'+url
                    # print(title, url, date_Today)
                    # # time.sleep(666)
                    if tool.Transformation(date) <= tool.Transformation(date_Today):
                        # if tool.removal(title, date):
                            self.parse_detile(title, url, date_Today)
                        # else:
                        #     print('【existence】', url)
                        #     continue
                    else:
                        # print(tool.Transformation(date),self.Transformation(date_Today))
                        print('日期不符, 正在切换类型', date_Today, url)
                        return
                except Exception as e:
                    traceback.print_exc()

    def parse_detile(self, title, url, date):
        print(url)
        t = tool.requests_get(url, self.headers)
        url_html = etree.HTML(t)
        try:
            detail = url_html.xpath('//div[@class="WordSection1"]')[0]
        except:
            try:
                detail = url_html.xpath('//div[@class="Contnet"]')[0]
            except:
                return
        # print(detail)
        detail_html = etree.tostring(detail, method='HTML')
        detail_html = html.unescape(detail_html.decode())
        detail_text = url_html.xpath('string(//div[@class="WordSection1"])').replace('\xa0', '').replace('\n', ''). \
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
        item['winner'] = tool.get_winner(detail_text)
        item['address'] = tool.get_address(detail_text)
        item['linkman'] = tool.get_linkman(detail_text)
        item['function'] = tool.get_function(detail_text)
        item['resource'] = '中核集团电子采购平台'
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

if __name__ == '__main__':

    import traceback, os
    try:
        jl = baoshan_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
