# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 盐城市公共资源交易平台
class baoshan_ggzy:
    def __init__(self):
        self.url_list = [
            'http://ggzy.yancheng.gov.cn/EpointWebBuilder/xyxxInfoListAction.action?cmd=getInfolist&categorynum=003&city=&title=&pageSize=20&pageIndex={}&verificationCode=&verificationGuid=',
                         ]
        self.url = self.url_list.pop(0)
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Host': 'ggzy.yancheng.gov.cn',
            'If-Modified-Since': 'Mon, 07 Dec 2020 08:56:39 GMT',
            'If-None-Match': 'W/"5fcdee47-6eab"',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36',
        }

    def parse(self):
        date = tool.date
        # date = '2020-12-11'
        page = 0
        while True:
            text = tool.requests_get(self.url.format(page), self.headers)
            page += 1
            print('*' * 20, page, '*' * 20)
            # print(11, text)
            # time.sleep(6666)
            detail = json.loads(json.loads(text)['custom'])['Table']
            for li in detail:
                title = li['title'].replace('\n', '').replace('\r', '')\
                    .replace('\t', '').replace(' ', '')
                url = li['href']
                if 'http' not in url:
                    url = 'http://ggzy.yancheng.gov.cn' + url
                date_Today = li['infodate'].replace('\n', '').replace('\r', '') \
                    .replace('\t', '').replace(' ', '').replace('(', '').replace(')', '').replace('.', '-')\
                    .replace('[', '').replace(']', '').replace('.', '-')
                if '测试' in title or 'http://ggzy.yancheng.gov.cn' not in url:
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
                    return


    def parse_detile(self, title, url, date):
        print(url)
        t = tool.requests_get(url, self.headers)
        url_html = etree.HTML(t)
        try:
            detail = url_html.xpath('//*[@id="Table0"]')[0]
            detail_html = etree.tostring(detail, method='HTML')
            detail_html = html.unescape(detail_html.decode())
            detail_text = url_html.xpath('string(//*[@id="Table0"])').replace('\xa0', '').replace('\n',
                                                                                                      ''). \
                replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
            if len(detail_html) < 300:
                return
        except:
            try:
                detail = url_html.xpath('//*[@id="_Sheet1"]')[0]
                detail_html = etree.tostring(detail, method='HTML')
                detail_html = html.unescape(detail_html.decode())
                detail_text = url_html.xpath('string(//*[@id="_Sheet1"])').replace('\xa0', '').replace('\n',
                                                                                                      ''). \
                    replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
                if len(detail_html) < 300:
                    return
            except:
                try:
                    detail = url_html.xpath('//*[@id="Table1"]')[0]
                    detail_html = etree.tostring(detail, method='HTML')
                    detail_html = html.unescape(detail_html.decode())
                    detail_text = url_html.xpath('string(//*[@id="Table1"])').replace('\xa0', '').replace('\n',
                                                                                                           ''). \
                        replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
                    if len(detail_html) < 300:
                        return
                except:
                    try:
                        detail = url_html.xpath('//*[@class="Section0"]')[0]
                        detail_html = etree.tostring(detail, method='HTML')
                        detail_html = html.unescape(detail_html.decode())
                        detail_text = url_html.xpath('string(//*[@class="Section0"])').replace('\xa0', '').replace('\n',
                                                                                                              ''). \
                            replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
                        if len(detail_html) < 300:
                            return
                    except:
                        detail = url_html.xpath('//*[@class="con"]')[0]
                        detail_html = etree.tostring(detail, method='HTML')
                        detail_html = html.unescape(detail_html.decode())
                        detail_text = url_html.xpath('string(//*[@class="con"])').replace('\xa0', '').replace('\n',
                                                                                                                   ''). \
                            replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
                        if len(detail_html) < 300:
                            return
        if '没有相关公告' in detail_text:
            int('a')
        # print(111, detail_text.replace('\xa0','').replace('\xa5',''))
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
        item['resource'] = '盐城市公共资源交易平台'
        item['shi'] = 5509
        item['sheng'] = 5500
        item['removal']= title
        process_item(item)

    def get_nativeplace(self, addr):
        city = ''
        city_list = [['5509.001', '亭湖区'], ['5509.002', '盐都区'], ['5509.003', '响水县'], ['5509.004', '滨海县'], ['5509.005', '阜宁县'], ['5509.006', '射阳县'], ['5509.007', '建湖县'], ['5509.008', '东台市'], ['5509.009', '大丰市']]

        for i in city_list:
            if i[1] in addr:
                city = float(i[0])
                break
        if city == '':
            city = 5509
        return city

if __name__ == '__main__':
    import traceback, os
    try:
        jl = baoshan_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
        tool.send_error('报错文件：'+str(os.path.basename(__file__))+'报错信息：'+str(e))


