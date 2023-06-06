# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 长兴县公共资源交易中心
class wenshan_ggzy:
    def __init__(self):
        self.url_list = [
            'https://ggzy.zjcx.gov.cn/cxweb/showinfo/zbgg.aspx', #招标公告
                    ]
        self.url = self.url_list.pop(0)
        self.headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'}
    def parse(self):
        date = tool.date
        # date = '2020-09-21'
        page = 0
        while True:
            page += 1
            data={'__VIEWSTATE': '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',
'__VIEWSTATEGENERATOR': '87C4C5EF',
'__EVENTTARGET': 'Pager',
'__EVENTARGUMENT': page,
'__VIEWSTATEENCRYPTED': ""
}
            text = tool.requests_post(url=self.url,data=data,headers=self.headers)
            # print(text)
            print('*' * 20, page, '*' * 20)
            html = HTML(text)
            # print(11, text)
            # time.sleep(6666)
            detail = html.xpath('//table[@id="DataGrid1"]//tr')
            for li in detail:
                title = li.xpath('./td[2]/a/text()')[0]
                href = li.xpath('./td[2]/a/@href')[0]
                date_Today = "".join(li.xpath('./td[3]/text()')).replace('\n', '').replace('\r', '').replace('\t', '')
                url='https://ggzy.zjcx.gov.cn'+href
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
        detail = url_html.xpath('//table[@id="tblInfo"]')[0]
        detail_html = etree.tostring(detail, method='HTML')
        detail_html = html.unescape(detail_html.decode()).replace("display: none", '')
        detail_text = url_html.xpath('string(//table[@id="tblInfo"])').replace('\xa0', '').replace('\n', '').\
            replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
        if len(detail_html) < 200:
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
        item['body'] = item['body'].replace('''<a href="http://www.hfztb.cn" target="_blank"><img src="../Template/Default/images/wybm.png"></a>''', '')
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
        item['resource'] = '长兴县公共资源交易中心'
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



