# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 五峰土家族公共资源交易中心
class wenshan_ggzy:
    def __init__(self):
        self.domain_name = 'http://ggzyjy.hbwf.gov.cn'
        self.url_list = [
            # 'http://ggzyjy.hbwf.gov.cn/wfSite/jyxx/003002/003002001/003002001003/?pageing={}',
            # 'http://ggzyjy.hbwf.gov.cn/wfSite/jyxx/003001/003001001/003001001001/?pageing={}',
            # 'http://ggzyjy.hbwf.gov.cn/wfSite/jyxx/003001/003001001/003001001002/?pageing={}',
            # 'http://ggzyjy.hbwf.gov.cn/wfSite/jyxx/003001/003001001/003001001003/?pageing={}',
            # 'http://ggzyjy.hbwf.gov.cn/wfSite/jyxx/003001/003001002/003001002001/?pageing={}',
            # 'http://ggzyjy.hbwf.gov.cn/wfSite/jyxx/003001/003001002/003001002002/?pageing={}',
            # 'http://ggzyjy.hbwf.gov.cn/wfSite/jyxx/003001/003001002/003001002003/?pageing={}',
            # 'http://ggzyjy.hbwf.gov.cn/wfSite/jyxx/003002/003002001/003002001001/?pageing={}',
            # 'http://ggzyjy.hbwf.gov.cn/wfSite/jyxx/003002/003002002/003002002001/?pageing={}',
            # 'http://ggzyjy.hbwf.gov.cn/wfSite/jyxx/003002/003002004/003002004001/?pageing={}',
            # 'http://ggzyjy.hbwf.gov.cn/wfSite/jyxx/003002/003002004/003002004003/?pageing={}'
            'http://ggzyjy.hbwf.gov.cn/wfSite/jyxx/003001/003001004/003001004001/?pageing={}',
            'http://ggzyjy.hbwf.gov.cn/wfSite/jyxx/003001/003001004/003001004002/?pageing={}',
            'http://ggzyjy.hbwf.gov.cn/wfSite/jyxx/003001/003001004/003001004003/?pageing={}',
            'http://ggzyjy.hbwf.gov.cn/wfSite/jyxx/003001/003001004/003001004004/?pageing={}'

        ]
        self.url = self.url_list.pop(0)
        self.headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Cookie': 'JSESSIONID=662863FD2199FBD1672A04A290868047; _CSRFCOOKIE=73F3D7A1BCDCA9001D7B1483A214C4E98DE2528B; EPTOKEN=73F3D7A1BCDCA9001D7B1483A214C4E98DE2528B; oauthClientId=demoClient; oauthPath=http://172.16.5.21:8080/EpointWebBuilder; oauthLoginUrl=http://172.16.5.21:8080/EpointWebBuilder/rest/oauth2/authorize?client_id=demoClient&state=a&response_type=code&scope=user&redirect_uri=; oauthLogoutUrl=http://172.16.5.21:8080/EpointWebBuilder/rest/oauth2/logout?redirect_uri=; noOauthRefreshToken=986d4fe7e5dd29b64c9e7b7a6d66e089; noOauthAccessToken=77c09e0bf98b6220b544961097eed84a; sub_domain_cokie=TiG5CMD9KQ41mmsARPTuAg%3D%3D; region_name=%E4%B9%8C%E9%B2%81%E6%9C%A8%E9%BD%90%E5%B8%82',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',

        }

    def parse(self):
        date = tool.date
        # date = '2021-07-21'
        page = 0
        while True:
            page += 1
            text = tool.requests_get(self.url.format(page), self.headers)
            html = HTML(text)
            print('*' * 20, page, '*' * 20)
            detail = html.xpath('//*[@class="list"]/li')
            for li in detail:
                title = li.xpath('./a/@title')[0].replace('\xa0', '').replace('\n', ''). \
                    replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
                url = li.xpath('./a/@href')[0]
                date_Today = li.xpath('./span/text()')[0].replace('\xa0', '').replace('\n', ''). \
                    replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '') \
                    .replace('[', '').replace(']', '').replace('/', '-')
                if 'http' not in url:
                    url = self.domain_name + url
                # print(title, url, date_Today)
                # time.sleep(666)
                if tool.Transformation(date) <= tool.Transformation(date_Today):
                    # if tool.removal(title, date):
                        self.parse_detile(title, url, date_Today)
                    # else:
                    #     print('【existence】', url)
                    #     continue
                else:
                    print('日期不符, 正在切换类型', date_Today, self.url)
                    self.url = self.url_list.pop(0)
                    page=0
                    break


    def parse_detile(self, title, url, date):
        print(url)
        t = tool.requests_get(url, self.headers).replace('\xa9', '').replace('<br>&nbsp;&nbsp;', '')
        # print(t)
        # time.sleep(2222)
        url_html = etree.HTML(t)
        try:
            detail = url_html.xpath('//*[@class="sdcbf3305"]')[0]
            detail_html = etree.tostring(detail, method='HTML')
            detail_html = html.unescape(detail_html.decode()).replace("display: none", '')
            detail_text = url_html.xpath('string(//*[@class="sdcbf3305"])').replace('\xa0', '').replace('\n',
                                                                                                                 ''). \
                replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
            if len(detail_html) < 200:
                int('a')
        except:
            detail = url_html.xpath('//*[@id="mainContent"]')[0]
            detail_html = etree.tostring(detail, method='HTML')
            detail_html = html.unescape(detail_html.decode()).replace("display: none", '')
            detail_text = url_html.xpath('string(//*[@id="mainContent"])').replace('\xa0', '').replace('\n',
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
        item['nativeplace'] = 9004.01
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
        item['resource'] = '五峰土家族公共资源交易中心'
        item['shi'] = 9004
        item['sheng'] = 9000
        item['removal']= title
        process_item(item)

    def get_nativeplace(self, addr):
        city = ''
        city_list = [['8508.001', '解放区'], ['8508.01', '沁阳'], ['8508.011', '孟州'], ['8508.002', '中站区'], ['8508.003', '马村区'], ['8508.004', '山阳区'], ['8508.005', '修武县'], ['8508.006', '博爱县'], ['8508.007', '武陟县'], ['8508.008', '温县'], ['8508.009', '济源']]

        for i in city_list:
            if i[1] in addr:
                city = float(i[0])
                break
        if city == '':
            city = 8508
        return city

if __name__ == '__main__':
    import traceback,os
    try:
        jl = wenshan_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
        tool.send_error('报错文件：'+str(os.path.basename(__file__))+'报错信息：'+str(e))


