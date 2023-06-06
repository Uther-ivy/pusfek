# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 铜仁市公共资源交易平台
class tongren_ggzy:
    def __init__(self):
        self.url_list = [
            # 市本级
            #   工程建设
            #       招标公告
            'http://jyzx.trs.gov.cn/gcjs/zbgg/index.html',
            #       中标公示
            'http://jyzx.trs.gov.cn/gcjs/zbjggg/index.html',
            #       中标候选人
            'http://jyzx.trs.gov.cn/gcjs/zbgs/index.html',
            #       流标公告
            'http://jyzx.trs.gov.cn/gcjs/lbgs/index.html',
            #   政府采购
            #       采购公告
            'http://jyzx.trs.gov.cn/zfcg/cgxqgs/index.html',
            #       中标公告
            'http://jyzx.trs.gov.cn/zfcg/jggszgysjggs/index.html',
            #       更正公告
            'http://jyzx.trs.gov.cn/zfcg/bggg_5230297/index.html',
            #       流标公告
            'http://jyzx.trs.gov.cn/zfcg/fbgg/index.html'
        ]
        self.url = self.url_list.pop(0)
        self.headers = {
            'Cookie': 'userGuid=-254005787; oauthClientId=54652760-49c6-47f9-ae7a-83e5693cdaf3; oauthPath=http://jyyw.changde.gov.cn/TPFrame; oauthLoginUrl=http://jyyw.changde.gov.cn/TPFrame/rest/oauth2/authorize?client_id=54652760-49c6-47f9-ae7a-83e5693cdaf3&state=a&response_type=code&scope=user&redirect_uri=; oauthLogoutUrl=http://jyyw.changde.gov.cn/TPFrame/rest/oauth2/logout?redirect_uri=; noOauthRefreshToken=0e68bbd2754ae85b634637df6e5cdf19; noOauthAccessToken=46d04a7103255628c9ca1cd27b95c712',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        }

    def parse(self):
        date = tool.date
        # date = '2020-04-10'
        while True:
            text = tool.requests_get(self.url, self.headers)
            detail = HTML(text).xpath('//*[@id="right"]/div[1]/table/tbody/tr')
            for li in detail:
                title = li.xpath('./td[2]/a/@title')[0]
                url = li.xpath('./td[2]/a/@href')[0]
                date_Today = li.xpath('./td[3]/text()')[0].replace('\r', '').replace('\n', '').replace('\t', '').replace(' ', '')
                if '测试' in title:
                    continue
                print(title, url, date_Today)
                # time.sleep(666)
                if tool.Transformation(date) <= tool.Transformation(date_Today):
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
        url_html = etree.HTML(tool.requests_get(url, self.headers))
        detail = url_html.xpath('//*[@id="TDContent"]/div[1]')[0]
        detail_html = etree.tostring(detail, method='HTML')
        detail_html = html.unescape(detail_html.decode())
        detail_text = url_html.xpath('string(//*[@id="TDContent"]/div[1])').replace('\xa0', '').replace(
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
        item['resource'] = '铜仁市公共资源交易网'
        item['shi'] = 12505
        item['sheng'] = 12500
        item['removal']= title
        process_item(item)

    def get_nativeplace(self, addr):
        city = ''
        city_list = [['12505.001', '铜仁市'], ['12505.01', '万山特区'], ['12505.002', '江口县'], ['12505.003', '玉屏侗族自治县'], ['12505.004', '石阡县'], ['12505.005', '思南县'], ['12505.006', '印江土家族苗族自治县'], ['12505.007', '德江县'], ['12505.008', '沿河土家族自治县'], ['12505.009', '松桃苗族自治县']]
        for i in city_list:
            if i[1] in addr:
                city = float(i[0])
                break
        if city == '':
            city = 12505
        return city

if __name__ == '__main__':
    import traceback, os
    try:
        jl = tongren_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
        tool.send_error('报错文件：'+str(os.path.basename(__file__))+'报错信息：'+str(e))

