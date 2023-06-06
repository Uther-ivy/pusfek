# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 六安市公共资源交易中心
class wenshan_ggzy:
    def __init__(self):
        self.domain_name = 'http://ggzy.luan.gov.cn'
        self.url_list = [
            'http://ggzy.luan.gov.cn/EpointWebBuilder/rest/GgSearchAction/getJyInfoList'
        ]
        self.url = self.url_list.pop(0)
        self.headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Cookie': 'Secure; userGuid=-254005787; oauthClientId=demoClient; oauthPath=http://10.20.48.12:8099/EpointWebBuilder; oauthLoginUrl=http://10.20.48.12:8099/EpointWebBuilder/rest/oauth2/authorize?client_id=demoClient&state=a&response_type=code&scope=user&redirect_uri=; oauthLogoutUrl=http://10.20.48.12:8099/EpointWebBuilder/rest/oauth2/logout?redirect_uri=; noOauthRefreshToken=8f39607b770ff644dffce2d6b89c3ec5; noOauthAccessToken=be712edb8604cd875168870656a769bf',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',

        }

    def parse(self):
        date = tool.date
        # date = '2020-09-25'
        page = 0
        while True:
            data = {
                'params': '{"siteGuid":"7eb5f7f1-9041-43ad-8e13-8fcb82ea831a","keywords":"","fbdate":"","jyly":"","categoryNum":"001","jyfs":"","pageIndex":'+str(page)+',"pageSize":10}'
            }
            page += 1
            text = tool.requests_post(self.url, data, self.headers)
            # html = HTML(text)
            print('*' * 20, page, '*' * 20)
            # print(11, text.replace('\ufffd', ' ').replace('\u30fb', ' '))
            # time.sleep(6666)
            detail = json.loads(text)['Table']
            for li in detail:
                title = li['title1'].replace('\xa0', '').replace('\n', ''). \
                    replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
                url = li['infourl']
                date_Today = li['infodate'].replace('\xa0', '').replace('\n', ''). \
                    replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '') \
                    .replace('[', '').replace(']', '').replace('/', '-')
                if 'http' not in url:
                    url = self.domain_name + url
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
        t = tool.requests_get(url, self.headers).replace('\xa9', '').replace('<br>&nbsp;&nbsp;', '')
        url_html = etree.HTML(t)
        try:
            detail = url_html.xpath('//*[@class="ewb-project-left"]')[0]
            detail_html = etree.tostring(detail, method='HTML')
            detail_html = html.unescape(detail_html.decode()).replace("display: none", '')
            detail_text = url_html.xpath('string(//*[@class="ewb-project-left"])').replace('\xa0', '').replace('\n',
                                                                                                                 ''). \
                replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
            if len(detail_html) < 200:
                int('a')
        except:
            detail = url_html.xpath('//*[@class="ewb-article-info"]')[0]
            detail_html = etree.tostring(detail, method='HTML')
            detail_html = html.unescape(detail_html.decode()).replace("display: none", '')
            detail_text = url_html.xpath('string(//*[@class="ewb-article-info"])').replace('\xa0', '').replace('\n',
                                                                                                               ''). \
                replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
            if len(detail_html) < 200:
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
        item['resource'] = '六安市公共资源交易中心'
        item['shi'] = 6514
        item['sheng'] = 6500
        item['removal']= title
        process_item(item)

    def get_nativeplace(self, addr):
        city = ''
        city_list = [['6514.001', '金安区'], ['6514.002', '裕安区'], ['6514.003', '寿县'], ['6514.004', '霍邱县'], ['6514.005', '舒城县'], ['6514.006', '金寨县'], ['6514.007', '霍山县']]

        for i in city_list:
            if i[1] in addr:
                city = float(i[0])
                break
        if city == '':
            city = 6514
        return city

if __name__ == '__main__':
    import traceback,os
    try:
        jl = wenshan_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
        # traceback.print_exc()
        tool.send_error('报错文件：'+str(os.path.basename(__file__))+'报错信息：'+str(e))


