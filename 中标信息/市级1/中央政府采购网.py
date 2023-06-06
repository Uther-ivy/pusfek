# -*- coding: utf-8 -*-
import json
import re
import time, html
from lxml import etree
import tool
from save_database import process_item

# 中央政府采购网
class alashan_ggzy:
    def __init__(self):
        self.url_code = [
            # 'https://www.zycg.gov.cn/freecms/rest/v1/notice/selectInfoMore.do?&siteId=6f5243ee-d4d9-4b69-abbd-1e40576ccd7d&channel=d0e7c5f4-b93e-4478-b7fe-61110bb47fd5&currPage={}&pageSize=12&noticeType=57,1,2,3,61&implementWay=1&operationStartTime=&title=&operationEndTime=',
            # 'https://www.zycg.gov.cn/freecms/rest/v1/notice/selectInfoMore.do?&siteId=6f5243ee-d4d9-4b69-abbd-1e40576ccd7d&channel=d0e7c5f4-b93e-4478-b7fe-61110bb47fd5&currPage={}&pageSize=12&noticeType=59,2,61,3,31,32&implementWay=9&operationStartTime=&title=&operationEndTime=',
            # 'https://www.zycg.gov.cn/freecms/rest/v1/notice/selectInfoMore.do?&siteId=6f5243ee-d4d9-4b69-abbd-1e40576ccd7d&channel=d0e7c5f4-b93e-4478-b7fe-61110bb47fd5&currPage={}&pageSize=12&noticeType=59,2,61,31,32,3&implementWay=21&operationStartTime=&title=&operationEndTime=',
            'https://www.zycg.gov.cn/freecms/rest/v1/notice/selectInfoMore.do?&siteId=6f5243ee-d4d9-4b69-abbd-1e40576ccd7d&channel=d0e7c5f4-b93e-4478-b7fe-61110bb47fd5&currPage={}&pageSize=12&noticeType=2&implementWay=1&operationStartTime=&title=&operationEndTime='
        ]
        self.url = self.url_code.pop(0)
        self.headers = {
            'Accept': '*/*',
            'Content-Type': 'application/json;charset=utf-8',
            # 'Host': 'www.zycg.gov.cn',
            'Cookie': 'JSESSIONID=2A7C0E35D52D1E8690A36AD6441433E5; jfe_pin=baac5876; jfe_ts=1639641956.298; jfe_sn=WUK+wMjHYPDk8/Plq+xy1nJWxb4=; VFSESS=cap109181771+salYB7Z8=',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
        }

    def parse(self):
        date = tool.date
        # date = '2021-04-12'
        page = 317
        while True:
            page += 1
            print('*' * 20, page, '*' * 20)
            text = tool.requests_get(self.url.format(page), self.headers)
            detail = json.loads(text)['data']
            for li in detail:
                title = li['title']
                url = li['pageurl']
                date_Today = li['addtimeStr'][:10]
                if 'http' not in url:
                    url = 'http://www.zycg.gov.cn' + url
                # print(title, url, date_Today)
                # time.sleep(666)
                if tool.Transformation(date) <= tool.Transformation(date_Today):
                    # if tool.removal(title, date):
                        self.parse_detile(title, url, date_Today)
                    # else:
                    #     print('【existence】', url)
                    #     continue
                else:
                    print('日期不符, 正在切换类型...', date_Today)
                    self.url = self.url_code.pop(0)
                    page = 0
                    break


    def parse_detile(self, title, url, date):
        print(url)
        try:
            url_text = tool.requests_get(url, self.headers)
            url_html = etree.HTML(url_text)
            detail = url_html.xpath('//*[@id="printArea"]')[0]
            detail_html = etree.tostring(detail, method='HTML')
            detail_html = html.unescape(detail_html.decode())
            detail_text = url_html.xpath('string(//*[@id="printArea"])').replace('\xa0', '').replace('\n',
                                                                                                               '').replace(
                '\r', '').replace('\t',
                                  '').replace(
                ' ', '').replace('\xa5', '').replace('市辖区', '')
        except:
            try:
                u = 'https://mkt.zycg.gov.cn/proxy/platform/platform/notice/queryMallNoticeById?platformId=20&id=' +\
                    url.replace('http://mkt.zycg.gov.cn/mall-view/information/detail?noticeId=', '')
                url_text = json.loads(tool.requests_get(u, self.headers))
                detail_html = url_text['data']['contentStr']
                detail_text = ''.join(re.findall('>(.*?)<', detail_html,re.S)).replace('\xa0', '').replace('\n',
                                                                                                         '').replace(
                    '\r', '').replace('\t',
                                      '').replace(
                    ' ', '').replace('\xa5', '').replace('市辖区', '')
            except:
                return
        item = {}
        item['title'] = title.replace('\u2022', '')
        item['url'] = url
        item['date'] = date
        item['typeid'] = tool.get_typeid(item['title'])
        item['senddate'] = int(time.time())
        item['mid'] = 867
        item['nativeplace'] = float(tool.get_title_city(item['title']))
        if item['nativeplace'] == 0:
            item['nativeplace'] = float(tool.more(item['title']+detail_text))
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
        item['winner'] = tool.get_winner(detail_text)
        item['address'] = tool.get_address(detail_text)
        item['linkman'] = tool.get_linkman(detail_text)
        item['function'] = tool.get_function(detail_text)
        item['resource'] = '中央政府采购网'
        item["shi"] = int(item["nativeplace"])
        if len(str(item["nativeplace"])) == 4:
            item['sheng'] = int(str(item["nativeplace"])[:2] + '00')
        elif len(str(item["nativeplace"])) == 5:
            item['sheng'] = int(str(item["nativeplace"])[:3] + '00')
        else:
            item['sheng'] = 0
        item['removal']= title
        process_item(item)
        # print(item['nativeplace'], item['title'])

if __name__ == '__main__':
    import traceback, os
    try:
        jl = alashan_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
