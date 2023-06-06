# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 黔南州公共资源交易平台
class qiannan_ggzy:
    def __init__(self):
        self.url_list = [
            # 市本级
            #   工程建设
            #       招标公告
            # 'http://ggzy.qiannan.gov.cn/gcjs_500203/zbgg/{}.html',
            #       中标公示
            # 'http://ggzy.qiannan.gov.cn/gcjs_500203/zbgs/{}.html',
            #       更正公告
            # 'http://ggzy.qiannan.gov.cn/gcjs_500203/bgdycq/{}.html',
            #       流标公告
            # 'http://ggzy.qiannan.gov.cn/gcjs_500203/lbgs/{}.html',
            #   政府采购
            #       采购公告
            # 'http://ggzy.qiannan.gov.cn/zfcg_500203/zbgg_5060411/{}.html',
            #       中标公告
            'http://ggzy.qiannan.gov.cn/zfcg_500203/zbgs_5060412/{}.html',
            #       更正公告
            # 'http://ggzy.qiannan.gov.cn/zfcg_500203/bggg/{}.html',
            #       流标公告
            # 'http://ggzy.qiannan.gov.cn/zfcg_500203/fbgs/{}.html'
        ]
        self.url = self.url_list.pop(0)
        self.headers = {
            'Cookie': 'userGuid=-254005787; oauthClientId=54652760-49c6-47f9-ae7a-83e5693cdaf3; oauthPath=http://jyyw.changde.gov.cn/TPFrame; oauthLoginUrl=http://jyyw.changde.gov.cn/TPFrame/rest/oauth2/authorize?client_id=54652760-49c6-47f9-ae7a-83e5693cdaf3&state=a&response_type=code&scope=user&redirect_uri=; oauthLogoutUrl=http://jyyw.changde.gov.cn/TPFrame/rest/oauth2/logout?redirect_uri=; noOauthRefreshToken=0e68bbd2754ae85b634637df6e5cdf19; noOauthAccessToken=46d04a7103255628c9ca1cd27b95c712',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        }

    def parse(self):
        date = tool.date
        # date = '2020-04-10'
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
            detail = html.xpath('//*[@class="NewsList"]/ul/li')
            for li in detail:
                try:
                    try:
                        title = li.xpath('./a/@title')[0]
                        url = li.xpath('./a/@href')[0]
                        date_Today = li.xpath('./span/text()')[0].replace('\n', '').replace('\r', '')\
                            .replace('\t', '').replace(' ', '')
                    except:
                        continue
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
                        print('日期不符, 正在切换类型', date_Today)
                        return
                except Exception as e:
                    traceback.print_exc()

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
        item['winner'] = tool.get_winner(detail_text)
        item['address'] = tool.get_address(detail_text)
        item['linkman'] = tool.get_linkman(detail_text)
        item['function'] = tool.get_function(detail_text)
        item['resource'] = '黔南州公共资源交易网'
        item['shi'] = 12509
        item['sheng'] = 12500
        item['removal']= title
        process_item(item)

    def get_nativeplace(self, addr):
        city = ''
        city_list = [['12509.001', '都匀市'], ['12509.01', '龙里县'], ['12509.011', '惠水县'], ['12509.012', '三都水族自治县'], ['12509.002', '福泉市'], ['12509.003', '荔波县'], ['12509.004', '贵定县'], ['12509.005', '瓮安县'], ['12509.006', '独山县'], ['12509.007', '平塘县'], ['12509.008', '罗甸县'], ['12509.009', '长顺县']]
        for i in city_list:
            if i[1] in addr:
                city = float(i[0])
                break
        if city == '':
            city = 12509
        return city

if __name__ == '__main__':

    import traceback, os
    try:
        jl = qiannan_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
        tool.send_error('报错文件：'+str(os.path.basename(__file__))+'报错信息：'+str(e))


