# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 金昌市公共资源交易平台
class baoshan_ggzy:
    def __init__(self):
        self.url_list = [  # App_Web_aagzcwt4 会定时更改
            'http://ggzy.jcs.gov.cn/pro-api-construction/construction/bidder/bidSection/list?pageNum={}&pageSize=10&releaseTime=&search=&informationType=ANNOUNCEMENT&departmentId=&projectType=SZFJ',
                         ]
        self.url = self.url_list.pop(0)
        self.headers = {
            'Accept': '*/*',
            'Cookie': 'Hm_lvt_1b8209d1dfbb21e021496ae1e24fe5c6=1628212962; userName=; number=2524672; SERVERID=4d62721a8af0a177f0525005d7426499|1628213246|1628212961; Hm_lpvt_1b8209d1dfbb21e021496ae1e24fe5c6=1628213246',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        }
        # u = 'http://ggzy.jcs.gov.cn/InfoPage/TradeInfomation.aspx?state=1,2,3'
        # t = tool.requests_get(u, self.headers)
        # code = HTML(t).xpath('//*[@id="form1"]/script[2]/@src')[0]
        # self.code = code.split(',')[1].replace('.ashx', '')


    def parse(self):
        date = tool.date
        # date = '2021-08-04'
        page = 0
        while True:
            time.sleep(1)
            page += 1
            # data = 'infoType=0\ncurr='+str(page)+'\nkeywords=\nqueryStr=and\ta.PrjPropertyNew\tin\t(1,2,3,21,22,23,24,5,6,12,14,15,16,17,18,19,20,4,7,8,9,11,41,31,13,44,43,551,552,553,0,441,442,443,0,331,332,333,0,2000)\tand\ta.Field1\tin(2952,2953,2954)'
            # text = tool.requests_post(self.url.format(self.code), data, self.headers)
            text = tool.requests_get(self.url.format(page), self.headers)
            if text is False or '未将对象引用设置到对象的实例' in text:
                print('未将对象引用设置到对象的实例')
                time.sleep(5)
                page -= 1
                continue
            print('*' * 20, page, '*' * 20)
            detail = json.loads(text)['rows']
            for li in detail:
                title = li['content']
                url = 'http://ggzy.jcs.gov.cn/pro-api/web/tradingInfo/getConstructionProjectInfo/' + str(li['projectId'])
                date_Today = li['releaseTime'][:10]
                if '测试' in title:
                    continue
                # print(title, url, date_Today)
                # time.sleep(666)
                if tool.Transformation(date_Today) >= tool.Transformation(date):
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
        # code = url.split('?')[1].replace('TenderProject=', '')
        # data = 'tenderId=' + code
        # url_to = 'http://ggzy.jcs.gov.cn/ajax/eclec_Monitor_demand,{}.ashx?_method=getTenderProjetId&_session=no'
        # t = tool.session_post(url_to.format(self.code), data)
        # data = 'tenderId=' + t.replace("'", '')
        # url_to = 'http://ggzy.jcs.gov.cn/ajax/eclec_Monitor_demand,{}.ashx?_method=getTenderDetailinfo&_session=no'
        # detail_html = tool.session_post(url_to.format(self.code), data)
        # detail_text = ''.join(re.findall('>(.*?)<', detail_html, re.S)).replace('\xa0', '').replace('\n',
        #                                                                                             ''). \
        #     replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
        print(url)
        t = tool.requests_get(url, self.headers).replace('\xa9', '').replace('<br>&nbsp;&nbsp;', '')
        # print(t)
        # time.sleep(2222)
        url_html = etree.HTML(t)
        detail = url_html.xpath('//*[@id="TDContent"]')[0]
        detail_html = etree.tostring(detail, method='HTML')
        detail_html = html.unescape(detail_html.decode()).replace("display: none", '').replace("\u2022", '').replace(
            '\xa0', '')
        detail_text = url_html.xpath('string(//*[@id="TDContent"])').replace('\xa0', '').replace('\n',
                                                                                                 ''). \
            replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
        if len(detail_html) < 200:
            int('a')


        if '没有相关公告' in detail_text:
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
        item['resource'] = '金昌市公共资源交易平台'
        item['shi'] = 14503
        item['sheng'] = 14500
        item['removal']= title
        process_item(item)

    def get_nativeplace(self, addr):
        city = ''
        city_list = [['14503.001', '金川区'], ['14503.002', '永昌县']]

        for i in city_list:
            if i[1] in addr:
                city = float(i[0])
                break
        if city == '':
            city = 14503
        return city

if __name__ == '__main__':
    import traceback, os
    try:
        jl = baoshan_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
        tool.send_error('报错文件：'+str(os.path.basename(__file__))+'报错信息：'+str(e))


