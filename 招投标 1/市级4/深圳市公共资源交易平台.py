# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 深圳市公共资源交易中心
class wenshan_ggzy:
    def __init__(self):
        self.domain_name = 'https://www.szggzy.com'
        self.url_list = [
            'https://www.szggzy.com/cms/api/v1/trade/content/page',
        ]
        self.url = self.url_list.pop(0)
        self.headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            # 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Host': 'www.szggzy.com',
            'Cookie': f'Hm_lvt_42d6d6c9d2c97bcda19906bdfe55f5c0=1678853044; G3_SESSION_V=NjFkNmYwOTEtMWUyNS00Yzg0LWE2MWQtNTk1ODNlZWI4ZmM4; Hm_lpvt_42d6d6c9d2c97bcda19906bdfe55f5c0={int(time.time())}',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',

        }
    def parse(self):
        date = tool.date
        # date = '2020-09-24'
        page = 0
        while True:
            data = {"modelId": 1378, "channelId": 2851,
                    "fields": [{"fieldName": "jygg_gglxmc_rank1", "fieldValue": "招标公告"},
                               {"fieldName": "jygg_gglxmc", "fieldValue": "招标公告"}], "title": None,
                    "releaseTimeBegin": None, "releaseTimeEnd": None, "page": page, "size": 10}
            page += 1
            text = tool.requests_post_to(self.url.format(page),data, self.headers)
            print('*' * 20, page, '*' * 20)
            html = json.loads(text)
            detail = html["data"]["content"]
            for li in detail:
                title = li["noticeTitle"]
                date_Today = li["updateTime"].split(' ')[0]
                contentId = li["contentId"]
                url=f'https://www.szggzy.com/cms/api/v1/trade/content/detail?contentId={contentId}'
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
        t = requests.get(url=url, headers=self.headers)
        url_html = t.json()
        detail=url_html['data']['txt']
        # print(detail)

        # try:
        # detail = url_html.xpath('//*[@class="div-content"]')[0]

        # detail_html = etree.tostring(detail, method='HTML')
        # detail_html = html.unescape(detail_html.decode()).replace("display: none", '')
        # detail_text = url_html.xpath('string(//*[@class="div-content"])').replace('\xa0', '').replace('\n',
        #                                                                                                         ''). \
        #     replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
        # except:
        #     detail = url_html.xpath('//*[@class="conTxt"]')[0]
        #     detail_html = etree.tostring(detail, method='HTML')
        #     detail_html = html.unescape(detail_html.decode()).replace("display: none", '')
        #     detail_text = url_html.xpath('string(//*[@class="conTxt"])').replace('\xa0', '').replace('\n',
        #                                                                                                        ''). \
        #         replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
        item = {}
        item['title'] = title.replace('\u2022', '')
        item['url'] = url
        item['date'] = date
        item['typeid'] = tool.get_typeid(item['title'])
        item['senddate'] = int(time.time())
        item['mid'] = 867
        item['nativeplace'] = self.get_nativeplace(item['title'])
        item['infotype'] = tool.get_infotype(item['title'])
        item['body'] = detail
        # item['body'] = tool.update_img(self.domain_name, item['body'])
        item['endtime'] = tool.get_endtime(detail)
        if item['endtime'] == '':
            item['endtime'] = int(time.mktime(time.strptime(date, "%Y-%m-%d")))
        else:
            try:
                item['endtime'] = int(time.mktime(time.strptime(item['endtime'], "%Y-%m-%d")))
            except:
                item['endtime'] = int(time.mktime(time.strptime(date, "%Y-%m-%d")))
        item['tel'] = tool.get_tel(detail)
        item['email'] = ''
        item['address'] = tool.get_address(detail)
        item['linkman'] = tool.get_linkman(detail)
        item['function'] = tool.get_function(detail)
        item['resource'] = '深圳市公共资源交易平台'
        item['shi'] = 10003
        item['sheng'] = 10000
        item['removal']= title
        process_item(item)
        # print(item['body'])

    def get_nativeplace(self, addr):
        city = ''
        city_list = [['10003.001', '罗湖区'], ['10003.002', '福田区'], ['10003.003', '南山区'], ['10003.004', '宝安区'], ['10003.005', '龙岗区'], ['10003.006', '盐田区'], ['10003.007', '坪山区']]

        for i in city_list:
            if i[1] in addr:
                city = float(i[0])
                break
        if city == '':
            city = 10003
        return city

if __name__ == '__main__':
    import traceback,os
    try:
        jl = wenshan_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
        tool.send_error('报错文件：'+str(os.path.basename(__file__))+'报错信息：'+str(e))


