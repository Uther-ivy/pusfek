# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 毕节市公共资源交易平台
class bijie_ggzy:
    def __init__(self):
        self.url_list = [
            # 市本级
            #   工程建设
            #       招标公告
            'https://ggzy.bijie.gov.cn/xxfw/gcjs/zbgg/{}.html',
            #       中标公示
            'https://ggzy.bijie.gov.cn/xxfw/gcjs/bggg/{}.html',
            #       更正公告
            'https://ggzy.bijie.gov.cn/xxfw/gcjs/zbgs/{}.html',
            #       流标公告
            'https://ggzy.bijie.gov.cn/xxfw/gcjs/lbgg/{}.html',
            #   政府采购
            #       采购公告
            'https://ggzy.bijie.gov.cn/xxfw/zfcg/cggg/{}.html',
            #       中标公告
            'https://ggzy.bijie.gov.cn/xxfw/zfcg/jggg/{}.html',
            #       更正公告
            'https://ggzy.bijie.gov.cn/xxfw/zfcg/bggg_5870651/{}.html',
            #       流标公告
            'https://ggzy.bijie.gov.cn/xxfw/zfcg/lbgg_5870653/{}.html'
        ]
        self.url = self.url_list.pop(0)
        self.headers = {
            'Cookie': 'userGuid=-254005787; oauthClientId=54652760-49c6-47f9-ae7a-83e5693cdaf3; oauthPath=http://jyyw.changde.gov.cn/TPFrame; oauthLoginUrl=http://jyyw.changde.gov.cn/TPFrame/rest/oauth2/authorize?client_id=54652760-49c6-47f9-ae7a-83e5693cdaf3&state=a&response_type=code&scope=user&redirect_uri=; oauthLogoutUrl=http://jyyw.changde.gov.cn/TPFrame/rest/oauth2/logout?redirect_uri=; noOauthRefreshToken=0e68bbd2754ae85b634637df6e5cdf19; noOauthAccessToken=46d04a7103255628c9ca1cd27b95c712',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        }

    def parse(self):
        date = tool.date
        # date = '2021-07-27'
        page = 0
        while True:
            page += 1
            if page == 1:
                text = tool.requests_get(self.url.format('index'), self.headers)
            else:
                text = tool.requests_get(self.url.format('index_' + str(page)), self.headers)
            print('*' * 20, page, '*' * 20)
            html = HTML(text)
            # print(11, text)
            # time.sleep(6666)
            detail = html.xpath('//*[@class="xxfw_list"]/ul/li')
            for li in detail:
                title = li.xpath('./a/@title')[0]
                url = li.xpath('./a/@href')[0]
                date_Today = li.xpath('./span/text()')[0][:10].replace('\n', '').replace('\r', '')\
                    .replace('\t', '').replace(' ', '')
                if '测试' in title:
                    continue
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
        url_html = etree.HTML(tool.requests_get(url, self.headers))
        detail = url_html.xpath('//*[@id="Zoom"]')[0]
        detail_html = etree.tostring(detail, method='HTML')
        detail_html = html.unescape(detail_html.decode())
        detail_text = url_html.xpath('string(//*[@id="Zoom"])').replace('\xa0', '').replace(
            '\n', ''). \
            replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
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
        item['resource'] = '毕节市公共资源交易网'
        item['shi'] = 12507
        item['sheng'] = 12500
        item['removal']= title
        process_item(item)

    def get_nativeplace(self, addr):
        city = ''
        city_list = [['12507.001', '毕节市'], ['12507.002', '大方县'], ['12507.003', '黔西县'], ['12507.004', '金沙县'], ['12507.005', '织金县'], ['12507.006', '纳雍县'], ['12507.007', '威宁彝族回族苗族自治县'], ['12507.008', '赫章县']]
        for i in city_list:
            if i[1] in addr:
                city = float(i[0])
                break
        if city == '':
            city = 12507
        return city

if __name__ == '__main__':
    import traceback, os
    try:
        jl = bijie_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
