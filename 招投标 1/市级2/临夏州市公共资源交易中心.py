# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 临夏州公共资源交易中心
class wenshan_ggzy:
    def __init__(self):
        self.domain_name = 'http://ggzyjy.linxia.gov.cn'
        self.url_list = [
            'http://ggzyjy.linxia.gov.cn/f/tenderannquainqueryanns/tenderannquainqueryanns/annquainList?tradeType=1&projectName=&pageNo={}&pageSize=20&isAll=&dataType=0&projectType=2&listType=1&projectname=&prjpropertyid=1,2,3,4,5,6,7,8,10,11,12,13,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,32,31,33&tradeArea=1,18,9,10,11,12,13,14,16&tabType=1',
            'http://ggzyjy.linxia.gov.cn/f/tenderannquainqueryanns/tenderannquainqueryanns/annquainList?tradeType=2&projectName=&pageNo={}&pageSize=20&isAll=&dataType=0&projectType=2&listType=1&projectname=&prjpropertyid=1,2,3,4,5,6,7,8,10,11,12,13,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,32,31,33&tradeArea=1,18,9,10,11,12,13,14,16&tabType=1',
            'http://ggzyjy.linxia.gov.cn/f/tenderannquainqueryanns/tenderannquainqueryanns/annquainList?tradeType=3&projectName=&pageNo={}&pageSize=20&isAll=&dataType=0&projectType=2&listType=1&projectname=&prjpropertyid=1,2,3,4,5,6,7,8,10,11,12,13,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,32,31,33&tradeArea=1,18,9,10,11,12,13,14,16&tabType=1',
            'http://ggzyjy.linxia.gov.cn/f/tenderannquainqueryanns/tenderannquainqueryanns/annquainList?tradeType=4&projectName=&pageNo={}&pageSize=20&isAll=&dataType=0&projectType=2&listType=1&projectname=&prjpropertyid=1,2,3,4,5,6,7,8,10,11,12,13,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,32,31,33&tradeArea=1,18,9,10,11,12,13,14,16&tabType=1'
        ]

        self.url = self.url_list.pop(0)
        self.headers = {
            'Accept': 'text/html, */*; q=0.01',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Cookie': 'jeeplus.session.id=cbd51d0ece8c4086b055f07c40986ef2; _gscu_1793677420=147524091umqke14; _gscbrs_1793677420=1; pageSize=20; _gscs_1793677420=147524097xn5hk14|pv:8; pageNo=0',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',

        }

    def parse(self):
        date = tool.date
        # date = '2020-09-29'
        page = 0
        while True:
            page += 1
            text = tool.requests_get(self.url.format(page), self.headers)
            html = HTML(text)
            print('*' * 20, page, '*' * 20)
            # print(11, text.replace('\ufffd', ' ').replace('\u30fb', ' '))
            # time.sleep(6666)
            detail = html.xpath('//*[@class="wq_lx_ggzypzxxItemList hw_list"]/li')
            for li in detail:
                title = li.xpath('./a/div[1]/p/text()')[0].replace('\xa0', '').replace('\n', ''). \
                    replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '').replace("<fontstyle='color:red'>(网)</font>", '')
                url = li.xpath('./a/@href')[0]
                date_Today = li.xpath('./a/span/text()')[0].replace('\xa0', '').replace('\n', ''). \
                    replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '') \
                    .replace('[', '').replace(']', '').replace('/', '-')
                if 'http' not in url:
                    url = self.domain_name + url
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
                    self.url = self.url_list.pop(0)
                    page = 0
                    break
            if page == 20:
                self.url = self.url_list.pop(0)
                break

    def parse_detile(self, title, url, date):
        print(url)
        t = tool.requests_get(url, self.headers).replace('\xa9', '').replace('<br>&nbsp;&nbsp;', '').replace('\ue603', '')\
            .replace('\ue602', '')
        # print(t)
        # time.sleep(2222)
        url_html = etree.HTML(t)
        detail = url_html.xpath('//*[@class="list_left_content"]')[0]
        detail_html = etree.tostring(detail, method='HTML')
        detail_html = html.unescape(detail_html.decode()).replace("display: none", '').replace("\u2022", '').replace('\xa0', '')
        code = url.replace('http://ggzyjy.linxia.gov.cn/f/newservertrade/tenderprojects/', '').replace('/flowpage', '')
        url_to = 'http://ggzyjy.linxia.gov.cn/f/newservertrade/tenderprojects/flowBidpackage?tenderprojectid={}&projectType=A01'
        t = tool.requests_get(url_to.format(code), self.headers).replace('\xa9', '').replace('<br>&nbsp;&nbsp;', '').replace('\ue603',
                                                                                                             '') \
            .replace('\ue602', '')
        detail_html = detail_html.replace('''				</div>
			</div>''', '') + t + '''				</div>
			</div>'''
        detail_text = url_html.xpath('string(//*[@class="list_left_content"])').replace('\xa0', '').replace('\n',
                                                                                                             ''). \
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
        item['resource'] = '临夏州公共资源交易中心'
        item['shi'] = 14513
        item['sheng'] = 14500
        item['removal']= title
        process_item(item)

    def get_nativeplace(self, addr):
        city = ''
        city_list = [['14513.001', '临夏'], ['14513.002', '临夏县'], ['14513.003', '康乐县'], ['14513.004', '永靖县'], ['14513.005', '广河县'], ['14513.006', '和政县'], ['14513.007', '东乡族自治县'], ['14513.008', '积石山保安族东乡族撒拉族自治县']]

        for i in city_list:
            if i[1] in addr:
                city = float(i[0])
                break
        if city == '':
            city = 14513
        return city

if __name__ == '__main__':
    import traceback, os
    try:
        jl = wenshan_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
        tool.send_error('报错文件：'+str(os.path.basename(__file__))+'报错信息：'+str(e))



