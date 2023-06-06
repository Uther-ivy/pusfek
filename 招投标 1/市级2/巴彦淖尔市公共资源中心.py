# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 巴彦淖尔市公共资源中心
class wenshan_ggzy:
    def __init__(self):
        self.url_list = ['http://ggzyjy.bynr.gov.cn/EpointWebBuilder/tradeInfoSearchAction.action?cmd=getList'
                         '&categorynums=018001&xiaqucode=&sdt=&edt=&jylx=&siteguid=7eb5f7f1-9041-43ad-8e13-8fcb82ea831a'
                         '&pageSize=15&pageIndex={}',
                         'http://ggzyjy.bynr.gov.cn/EpointWebBuilder/tradeInfoSearchAction.action?cmd=getList'
                         '&categorynums=018002&xiaqucode=&sdt=&edt=&jylx=&siteguid=7eb5f7f1-9041-43ad-8e13-8fcb82ea831a'
                         '&pageSize=15&pageIndex={}'
                         ]
        self.url = self.url_list.pop(0)
        self.headers = {
            'Cookie': 'homeid=1a444a31-e460-47ff-9931-1c075c0f3cd8',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        }

    def parse(self):
        date = tool.date
        # date = '2020-04-02'
        page = 0
        while True:
            page += 1
            text = tool.requests_get(self.url.format(page), self.headers)
            print('*' * 20, page, '*' * 20)
            # print(11, text)
            # time.sleep(6666)
            detail = json.loads(json.loads(text)['custom'])['Table']
            for li in detail:
                title = li['titles']
                url = 'http://ggzyjy.bynr.gov.cn' + li['href']
                date_Today = li['infodate']
                # print(title, url, date_Today)
                # time.sleep(666)
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
                self.url = self.url_list.pop(0)
                break
    def parse_detile(self, title, url, date):
        print(url)
        url_html = etree.HTML(tool.requests_get(url, self.headers))
        code = url_html.xpath('//*[@id="relationguid"]/@value')[0]
        url_to = 'http://ggzyjy.bynr.gov.cn/detailjson/' + code + '/' + url.split('/')[-1].replace('html', 'json')
        json_ = json.loads(tool.requests_get(url_to, self.headers))
        detail_html = json_['infocontent']
        detail_text = json_['infocontent2'].replace('\xa0', '').replace('\n', '').\
            replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
        if len(detail_html) < 200:
            int('a')
        # print(detail_html)
        # print(detail_text.replace('\xa0','').replace('\xa5',''))
        # time.sleep(6666)
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
        item['resource'] = '巴彦淖尔市公共资源中心'
        item['shi'] = 3008
        item['sheng'] = 3000
        item['removal']= title
        process_item(item)
    def get_nativeplace(self, addr):
        city = ''
        city_list = [['3008.001', '临河区'], ['3008.002', '五原县'], ['3008.003', '磴口县'], ['3008.004', '乌拉特前旗'], ['3008.005', '乌拉特中旗'], ['3008.006', '乌拉特后旗'], ['3008.007', '杭锦后旗']]

        for i in city_list:
            if i[1] in addr:
                city = float(i[0])
                break
        if city == '':
            city = 3008
        return city

if __name__ == '__main__':
    import traceback,os
    try:
        jl = wenshan_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
        tool.send_error('报错文件：'+str(os.path.basename(__file__))+'报错信息：'+str(e))



