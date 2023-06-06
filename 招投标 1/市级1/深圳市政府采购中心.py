# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 深圳市政府采购中心
class shenzhen_zfcg:
    def __init__(self):
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            # 'Content-Type': 'application/x-www-form-urlencoded',
            'Cookie': 'JSESSIONID=twaUsEq1sstR4n-3Rgb9HQm2DbgABHQgMweO0WVP_FJ7oDFDwfqd!1147148637!-1400941006',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
        }

    def parse(self):
        date = tool.date
        # date = '2020-01-02'
        url_list = [
            'http://www.szzfcg.cn/portal/topicView.do?method=view&id=1660&agencyType=1',
            'http://www.szzfcg.cn/portal/topicView.do?method=view&id=1660&agencyType=2',
            'http://www.szzfcg.cn/portal/topicView.do?method=view&id=1660&agencyType=3',
            'http://www.szzfcg.cn/portal/topicView.do?method=view&id=2014&agencyType=1',
            'http://www.szzfcg.cn/portal/topicView.do?method=view&id=2014&agencyType=2',
            'http://www.szzfcg.cn/portal/topicView.do?method=view&id=2014&agencyType=3',
        ]
        for u in url_list:
            page = 0
            status = '1'
            while True:
                if status == '2':
                    break
                page += 1
                data = {
                    'ec_i': 'topicChrList_20070702',
                    'topicChrList_20070702_crd': '20',
                    'topicChrList_20070702_f_a': '',
                    'topicChrList_20070702_p': str(page),
                    'topicChrList_20070702_s_siteId': '',
                    'topicChrList_20070702_s_name': '',
                    'topicChrList_20070702_s_speciesCategory': '',
                    'id': u.replace('http://www.szzfcg.cn/portal/topicView.do?method=view&id=', ''),
                    'method': 'view',
                    '__ec_pages': '1',
                    'agencyType': '1',
                    'topicChrList_20070702_rd': '20',
                    'topicChrList_20070702_f_name': '',
                    'topicChrList_20070702_f_speciesCategory': '',
                    'topicChrList_20070702_f_ldate': ''
                }
                text = tool.requests_post(u, data, self.headers)
                html = HTML(text)
                print('*' * 20, page, '*' * 20)
                detail = html.xpath('//*[@id="topicChrList_20070702_table"]/tbody/tr')
                for tr in detail:
                    url = 'http://www.szzfcg.cn/portal/documentView.do?method=view&id=' + tr.xpath('./td[3]/a/@href')[0]\
                        .replace('/viewer.do?id=', '')
                    title = tr.xpath('./td[3]/a/text()')[0]
                    date_Today = tr.xpath('./td[5]/text()')[0][:10]
                    # print(11, title, url, date_Today)
                    # time.sleep(666)
                    if tool.Transformation(date) <= tool.Transformation(date_Today):
                        if tool.removal(title, date):
                            self.parse_detile(title, url, date_Today)
                        else:
                            print('【existence】', url)
                            continue
                    else:
                        print('日期不符, 正在切换类型...', date_Today)
                        status = '2'
                        break

                if page == 20:
                    status = '2'
                    break
    def parse_detile(self, title, url, date):
        print(url)
        url_html = etree.HTML(tool.requests_get(url, self.headers))
        try:
            detail = url_html.xpath('//*[@id="bulletinContent"]')[0]
            detail_html = etree.tostring(detail, method='HTML')
            detail_html = html.unescape(detail_html.decode())
            detail_text = url_html.xpath('string(//*[@id="bulletinContent"])').replace('\xa0', '').replace('\n', '').replace('\r',
                                                                                                                   '').replace(
                '\t',
                '').replace(
                ' ', '').replace('\xa5', '')
        except:
            try:
                detail = url_html.xpath('//*[@id="contentDiv"]/table')[0]
                detail_html = etree.tostring(detail, method='HTML')
                detail_html = html.unescape(detail_html.decode())
                detail_text = url_html.xpath('string(//*[@id="contentDiv"]/table)').replace('\xa0', '').replace('\n',
                                                                                                                '').replace(
                    '\r',
                    '').replace(
                    '\t',
                    '').replace(
                    ' ', '').replace('\xa5', '')
            except:
                try:
                    detail = url_html.xpath('//*[@id="main"]')[0]
                    detail_html = etree.tostring(detail, method='HTML')
                    detail_html = html.unescape(detail_html.decode())
                    detail_text = url_html.xpath('string(//*[@id="main"])').replace('\xa0', '').replace(
                        '\n',
                        '').replace(
                        '\r',
                        '').replace(
                        '\t',
                        '').replace(
                        ' ', '').replace('\xa5', '')
                except:
                    try:
                        detail = url_html.xpath('//*[@id="contentDiv"]')[0]
                        detail_html = etree.tostring(detail, method='HTML')
                        detail_html = html.unescape(detail_html.decode())
                        detail_text = url_html.xpath('string(//*[@id="contentDiv"])').replace('\xa0', '').replace(
                            '\n',
                            '').replace(
                            '\r',
                            '').replace(
                            '\t',
                            '').replace(
                            ' ', '').replace('\xa5', '')
                    except:
                        try:
                            detail = url_html.xpath('/html/body/table')[0]
                            detail_html = etree.tostring(detail, method='HTML')
                            detail_html = html.unescape(detail_html.decode())
                            detail_text = url_html.xpath(
                                'string(/html/body/table)').replace('\xa0',
                                                                                                     '').replace(
                                '\n',
                                '').replace(
                                '\r',
                                '').replace(
                                '\t',
                                '').replace(
                                ' ', '').replace('\xa5', '')
                        except:
                            detail = url_html.xpath('/html/body')[0]
                            detail_html = etree.tostring(detail, method='HTML')
                            detail_html = html.unescape(detail_html.decode())
                            detail_text = url_html.xpath(
                                'string(/html/body)').replace('\xa0',
                                                                    '').replace(
                                '\n',
                                '').replace(
                                '\r',
                                '').replace(
                                '\t',
                                '').replace(
                                ' ', '').replace('\xa5', '')
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
        item['winner'] = tool.get_winner(detail_text)
        item['address'] = tool.get_address(detail_text)
        item['linkman'] = tool.get_linkman(detail_text)
        item['function'] = tool.get_function(detail_text)
        item['resource'] = '深圳市政府采购中心'
        item['shi'] = 10003
        item['sheng'] = 10000
        item['removal']= title
        process_item(item)

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
    jl = shenzhen_zfcg()
    jl.parse()


