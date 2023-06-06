# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 铜陵市公共资源交易中心
class wenshan_ggzy:
    def __init__(self):
        self.url_list = [
            # 'https://bulletin.cebpubservice.com/xxfbcmses/search/bulletin.html?searchDate=1998-03-20&dates=300&word=&categoryId=88&industryName=&area=&status=&publishMedia=&sourceInfo=&showStatus=1&page={}', #招标公告
            'https://bulletin.cebpubservice.com/xxfbcmses/search/result.html?searchDate=1998-04-12&dates=300&word=&categoryId=90&industryName=&area=&status=&publishMedia=&sourceInfo=&showStatus=&page={}'
                    ]
        self.url = self.url_list.pop(0)
        self.headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
         }
    def parse(self):
        date = tool.date
        # date = '2020-09-21'
        page = 0
        while True:
            page += 1
            text = tool.requests_get(url=self.url.format(page), headers=self.headers)
            print('*' * 20, page, '*' * 20)
            html = HTML(text)
            # print(11, text)
            # time.sleep(6666)
            detail = html.xpath('//table[@class="table_text"]//tr')
            for li in detail[1:]:
               try:
                    title = "".join(li.xpath('./td[1]//text()')).strip(' ').replace('\t', '').replace('\r', '').replace(' ',
                                                                                                                        '').replace(
                        '\n', '')
                    date_Today = "".join(li.xpath('./td[5]/text()')).replace('\t', '').replace('\r', '').replace('\n', '')
                    url="".join(li.xpath('./td[1]/a/@href')).split('\'')[1]
                    # print(title, url, date_Today)
                    # time.sleep(666)
                    # self.parse_detile(title, url, date_Today)
                    if tool.Transformation(date) <= tool.Transformation(date_Today):
                        # if tool.removal(title, date):
                            self.parse_detile(title, url, date_Today)
                        # else:
                        #     print('【existence】', url)
                        #     continue
                    else:
                        print('日期不符, 正在切换类型', date_Today)
                        return
               except Exception:
                    traceback.print_exc()

    def parse_detile(self, title, url, date):
        print(url)
        t = tool.requests_get(url, self.headers)
        # print(t)
        # time.sleep(2222)
        url_html = etree.HTML(t)
        index=url_html.xpath('//div[@class="mian_list_03"]/@index')[0]
        pdf='https://bulletin.cebpubservice.com/resource/ceb/js/pdfjs-dist/web/viewer.html?file='+f'https://details.cebpubservice.com:7443/bulletin/getBulletin/2dc9da1d112b4d9f8443e31e59a362a5/{index}'
        item = {}
        item['title'] = title.replace('\u2022', '')
        item['url'] = url
        item['date'] = date
        item['typeid'] = tool.get_typeid(item['title'])
        item['senddate'] = int(time.time())
        item['mid'] = 867
        item['nativeplace'] = self.get_nativeplace(item['title'])
        item['infotype'] = tool.get_infotype(item['title'])
        item['body'] = pdf
        item['body'] = item['body'].replace('''<a href="http://www.hfztb.cn" target="_blank"><img src="../Template/Default/images/wybm.png"></a>''', '')
        # print(item['body'].replace('\xa0', '').replace('\xa5', '').replace('\xb3', ''))
        # time.sleep(6666)
        item['endtime'] = 0
        if item['endtime'] == '':
            item['endtime'] = int(time.mktime(time.strptime(date, "%Y-%m-%d")))
        else:
            try:
                item['endtime'] = int(time.mktime(time.strptime(item['endtime'], "%Y-%m-%d")))
            except:
                item['endtime'] = int(time.mktime(time.strptime(date, "%Y-%m-%d")))
        item['tel'] = 0
        item['email'] = ''
        item['winner'] = ''
        item['address'] = 0
        item['linkman'] = 0
        item['function'] = 0
        item['resource'] = '中国招标投标公共服务平台'
        item['shi'] = 6507
        item['sheng'] = 6500
        item['removal']= title
        # print(item["body"])
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



