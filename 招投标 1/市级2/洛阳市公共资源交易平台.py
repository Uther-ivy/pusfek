# -*- coding: utf-8 -*-
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 洛阳市公共资源交易平台
class luoyang_ggzy:
    def __init__(self):
        self.url_list = [
            # 建设工程
            # 招标公告
            'http://lyggzyjy.ly.gov.cn/TPFront/jyxx/009001/009001001/',
            # 变更公告
            'http://lyggzyjy.ly.gov.cn/TPFront/jyxx/009001/009001002/',
            # 中标公示
            'http://lyggzyjy.ly.gov.cn/TPFront/jyxx/009001/009001003/',
            # 中标候选人
            'http://lyggzyjy.ly.gov.cn/TPFront/jyxx/009001/009001004/',
            # 政府采购
            # 采购公告
            'http://lyggzyjy.ly.gov.cn/TPFront/jyxx/009002/009002001/',
            # 变更公告
            'http://lyggzyjy.ly.gov.cn/TPFront/jyxx/009002/009002002/',
            # 结果公告
            'http://lyggzyjy.ly.gov.cn/TPFront/jyxx/009002/009002003/'
        ]

        self.headers = {
            'Cookie': 'ASP.NET_SessionId=jygsrvd0pcmtlmm3xv424hc1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        }

    def parse(self):
        date = tool.date
        # date = '2020-03-20'
        for url in self.url_list:
            text = tool.requests_get(url, self.headers)
            html = HTML(text)
            detail = html.xpath('//*[@id="right"]/div/div')
            # print(detail)
            # time.sleep(666)
            for i in detail:
                for j in i.xpath('./ul/li'):
                    title = j.xpath('./div/a/@title')[0]
                    url = 'http://lyggzyjy.ly.gov.cn' + j.xpath('./div/a/@href')[0]
                    date_Today = j.xpath('./span/text()')[0]
                    # print(title, url, date_Today)
                    # time.sleep(666)
                    if '测试' in title:
                        continue
                    if tool.Transformation(date) <= tool.Transformation(date_Today):
                        if tool.removal(title, date):
                            self.parse_detile(title, url, date_Today)
                        else:
                            print('【existence】', url)
                            continue
                    else:
                        print('日期不符, 正在切换类型', date_Today)
                        break


    def parse_detile(self, title, url, date):
        print(url)
        url_html = etree.HTML(tool.requests_get(url, self.headers))
        try:
            detail = url_html.xpath('//*[@id="tblInfo"]/tr[3]')[0]
            detail_html = etree.tostring(detail, method='HTML')
            detail_html = html.unescape(detail_html.decode()).replace('\xa0', '').replace('\ufeff', '')
            detail_text = url_html.xpath('string(//*[@id="tblInfo"]/tr[3])') \
                .replace('\xa0', '').replace('\n', '').replace('\r', '').replace('\t', '') \
                .replace(' ', '').replace('\xa5', '').replace('\ufeff', '')
        except:
            return
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
        item['body'] = detail_html
        width_list = re.findall('width="(.*?)"', item["body"])
        for i in width_list:
            item["body"] = item["body"].replace('width="{}"'.format(i), '')
        width_list = re.findall('WIDTH: (.*?)pt;', item["body"])
        for i in width_list:
            item["body"] = item["body"].replace('WIDTH: {}pt;'.format(i), '')
        width_list = re.findall('width:(.*?)px;', item["body"])
        for i in width_list:
            item["body"] = item["body"].replace('width:{}px;'.format(i), '')
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
        item['resource'] = '洛阳市公共资源交易平台'
        item['shi'] = 8503
        item['sheng'] = 8500
        item['removal']= title
        process_item(item)
        # print(item['body'])
    def get_nativeplace(self, addr):
        city = ''
        city_list = [['8503.001', '老城区'], ['8503.01', '嵩县'], ['8503.011', '汝阳县'], ['8503.012', '宜阳县'], ['8503.013', '洛宁县'], ['8503.014', '伊川县'], ['8503.015', '偃师'], ['8503.002', '西工区'], ['8503.003', '廛河回族区'], ['8503.004', '涧西区'], ['8503.005', '吉利区'], ['8503.006', '洛龙区'], ['8503.007', '孟津县'], ['8503.008', '新安县'], ['8503.009', '栾川县']]

        for i in city_list:
            if i[1] in addr:
                city = float(i[0])
                break
        if city == '':
            city = 8503
        return city
if __name__ == '__main__':

    import traceback, os
    try:
        jl = luoyang_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
