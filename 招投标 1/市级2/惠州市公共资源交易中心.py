# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 惠州市公共资源交易中心
class wenshan_ggzy:
    def __init__(self):
        self.domain_name = 'https://zyjy.huizhou.gov.cn'
        self.url_list = [
            'http://zyjy.huizhou.gov.cn/ggfw/jyxx/zfcg/xqgs/index{}.html',
            'http://zyjy.huizhou.gov.cn/ggfw/jyxx/zfcg/cgzgysgg/index{}.html',
            'http://zyjy.huizhou.gov.cn/ggfw/jyxx/zfcg/cqbggg/index{}.html',
            'http://zyjy.huizhou.gov.cn/ggfw/jyxx/zfcg/zbgg/index{}.html',
            'http://zyjy.huizhou.gov.cn/ggfw/jyxx/zfcg/sbgg/index{}.html',
            'http://zyjy.huizhou.gov.cn/ggfw/jyxx/jsgc/zbzgysgg/index{}.html',
            'http://zyjy.huizhou.gov.cn/ggfw/jyxx/jsgc/zbzgysjggs/index{}.html',
            'http://zyjy.huizhou.gov.cn/ggfw/jyxx/jsgc/zbgg/index{}.html',
            'http://zyjy.huizhou.gov.cn/ggfw/jyxx/jsgc/tzgg/index{}.html',
            ]
        self.url = self.url_list.pop(0)
        self.headers = {
            'Cookie': 'JSESSIONID=662863FD2199FBD1672A04A290868047; _CSRFCOOKIE=73F3D7A1BCDCA9001D7B1483A214C4E98DE2528B; EPTOKEN=73F3D7A1BCDCA9001D7B1483A214C4E98DE2528B; oauthClientId=demoClient; oauthPath=http://172.16.5.21:8080/EpointWebBuilder; oauthLoginUrl=http://172.16.5.21:8080/EpointWebBuilder/rest/oauth2/authorize?client_id=demoClient&state=a&response_type=code&scope=user&redirect_uri=; oauthLogoutUrl=http://172.16.5.21:8080/EpointWebBuilder/rest/oauth2/logout?redirect_uri=; noOauthRefreshToken=986d4fe7e5dd29b64c9e7b7a6d66e089; noOauthAccessToken=77c09e0bf98b6220b544961097eed84a; sub_domain_cokie=TiG5CMD9KQ41mmsARPTuAg%3D%3D; region_name=%E4%B9%8C%E9%B2%81%E6%9C%A8%E9%BD%90%E5%B8%82',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        }

    def parse(self):
        date = tool.date
        page = 0
        while True:
            page += 1
            if page == 1:
                text = tool.requests_get(self.url.format(''), self.headers)
            else:
                text = tool.requests_get(self.url.format('_'+str(page)), self.headers)
            print('*' * 20, page, '*' * 20)
            # print(11, text)
            # time.sleep(6666)
            detail = HTML(text).xpath('//*[@id="result"]/tr')
            for li in detail:
                title = li.xpath('string(./td[1]/span/a)').replace('\xa0', '').replace('\n', '').\
                    replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
                url = li.xpath('./td[1]/span/a/@href')[0]
                date_Today = li.xpath('./td[2]/text()')[0].replace('\xa0', '').replace('\n', '').\
                    replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
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
                print('日期不符, 正在切换类型')
                self.url = self.url_list.pop(0)
                break

    def parse_detile(self, title, url, date):
        print(url)
        url_html = etree.HTML(tool.requests_get(url, self.headers))
        detail = url_html.xpath('//*[@id="content"]')[0]
        detail_html = etree.tostring(detail, method='HTML')
        detail_html = html.unescape(detail_html.decode())
        detail_text = url_html.xpath('string(//*[@id="content"])').replace('\xa0', '').replace(
            '\n', ''). \
            replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
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
        # item['body'] = tool.update_img(self.domain_name, item['body'])
        # item['body'] = item['body'].replace('''<a href="http://www.hfztb.cn" target="_blank"><img src="../Template/Default/images/wybm.png"></a>''', '')
        # print(item['body'].replace('\xa0', '').replace('\xa5', '').replace('\xb3', ''))
        # time.sleep(6666)
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
        item['resource'] = '惠州市公共资源交易中心'
        item['shi'] = 10011
        item['sheng'] = 10000
        item['removal']= title
        process_item(item)

    def get_nativeplace(self, addr):
        city = ''
        city_list = [['10011.001', '惠城区'], ['10011.002', '惠阳区'], ['10011.003', '博罗县'], ['10011.004', '惠东县'], ['10011.005', '龙门县']]

        for i in city_list:
            if i[1] in addr:
                city = float(i[0])
                break
        if city == '':
            city = 10011
        return city

if __name__ == '__main__':
    import traceback, os
    try:
        jl = wenshan_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
        tool.send_error('报错文件：'+str(os.path.basename(__file__))+'报错信息：'+str(e))


