# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool,random
from save_database import process_item
from save_database import save_db
# 首创股份电子商务平台
class baoshan_ggzy:
    def __init__(self):
        self.url_list = [
            'https://ecp.capitalwater.cn/sccms/category/list.html?searchDate=1996-10-19&dates=300&word=&categoryIds=2,3,4,5,10&categoryId=&tabName=%E6%8B%9B%E6%A0%87%E5%85%AC%E5%91%8A&projectIndustryName=&tenderType=&page={}',
            'https://ecp.capitalwater.cn/sccms/category/list.html?searchDate=1996-10-19&dates=300&word=&categoryIds=12,13,14,2678&categoryId=&tabName=%E9%9D%9E%E6%8B%9B%E6%A0%87%E5%85%AC%E5%91%8A&projectIndustryName=&tenderType=&page={}'
        ]
        self.url = self.url_list.pop(0)
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Cookie': 'JSESSIONID=937554EB19F04ECD37F4E224B658C062',
            'Host': 'ecp.capitalwater.cn',
            # 'Referer': 'http://ecp.capitalwater.cn/sccms/category/list.html?searchDate=1996-06-23&dates=300&word=&categoryIds=2,3,4,5,10&categoryId=&tabName=%E6%8B%9B%E6%A0%87%E5%85%AC%E5%91%8A&projectIndustryName=&tenderType=&page=1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        }

    def parse(self):
        page = 0
        while True:
            page += 1
            date = tool.date
            print('-'*50, page)
            text = tool.requests_get(self.url.format(page),self.headers)
            if '没有检索到数据！' in text:
                print('没有检索到数据！')
                return
            html = HTML(text)
            detail = html.xpath('//*[@class="newslist"]/li')
            for li in detail:
                url= li.xpath('./a/@href')[0]
                title = li.xpath('./a/@title')[0]
                date_Today = li.xpath('./a/div/text()')[0].replace('\r', '').replace('\n', '').replace('\t', '').replace(' ', '')
                if '发布' in date_Today:
                    continue
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
                    print('日期不符, 正在切换类型', date_Today, self.url)
                    return


    def parse_detile(self, title, url, date):
        print(url)
        t = tool.requests_get(url, self.headers)
        url_html = etree.HTML(t)
        pdfpath = url_html.xpath('//iframe[@id="pdfContainer"]//@src')[0]
        item = {}
        item['zhao_time'] = date
        item['title'] = title
        item['info_url'] = url
        item['body'] = f'<embed width="100%" height="100%"  src="{pdfpath}"></embed>'
        item['detail'] = item['body'].replace('\n', '').replace("\t", '').replace("\r", '').replace('\xa0', '').replace(
            '\xc2', '').replace(' ', '')
        item['senddate'] = int(time.time())
        item['mid'] = 1403
        item['resource'] = '首创股份电子商务平台'
        item['typeid'] = tool.get_typeid(title)
        item['endtime'] = tool.get_endtime(item['detail'])
        if item['endtime'] == '':
            item['endtime'] = int(time.mktime(time.strptime(date, "%Y-%m-%d")))
        else:
            try:
                item['endtime'] = int(time.mktime(time.strptime(item['endtime'], "%Y-%m-%d")))
            except:
                item['endtime'] = int(time.mktime(time.strptime(date, "%Y-%m-%d")))
        item['nativeplace'] =tool.more(title + item['detail'])
        item['infotype'] = tool.get_infotype(title)
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
        item['email'] = ''
        item['tel'] = tool.get_tel(item['detail'])
        item['address'] = tool.get_address(item['detail'])
        item['linkman'] = tool.get_linkman(item['detail'])
        item['function'] = tool.get_function(item['detail'])  # detail["projectBudget"]
        item['click'] = random.randint(500, 1000)
        save_db(item)


if __name__ == '__main__':

    import traceback, os
    try:
        jl = baoshan_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
        # tool.send_error('报错文件：'+str(os.path.basename(__file__))+'报错信息：'+str(e))


