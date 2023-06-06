# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 广州市公共资源交易中心
class wenshan_ggzy:
    def __init__(self):
        self.domain_name = 'http://www.gzebpubservice.cn'
        self.url_list = [
            'http://www.gzebpubservice.cn/fjzbgg/index_{}.htm',
            'http://www.gzebpubservice.cn/fjzsjggs/index_{}.htm',#结果
            'http://www.gzebpubservice.cn/fjzbhxgs/index_{}.htm',
            'http://www.gzebpubservice.cn/fjzbxx/index_{}.htm',

            'http://www.gzebpubservice.cn/jtzbgg/index_{}.htm',
            'http://www.gzebpubservice.cn/jtysgg/index_{}.htm',
            'http://www.gzebpubservice.cn/jtzbhxgs/index_{}.htm',
            'http://www.gzebpubservice.cn/jtzbgs/index_{}.htm',  #交通 ==== ---->中标公告

            'http://www.gzebpubservice.cn/dlzbgg/index_{}.htm',
            'http://www.gzebpubservice.cn/dlzbhxgs/index_{}.htm',
            'http://www.gzebpubservice.cn/dlzbxx/index_{}.htm',

            'http://www.gzebpubservice.cn/tlzbgg/index_{}.htm',
            'http://www.gzebpubservice.cn/tlzbhxgs/index_{}.htm',
            'http://www.gzebpubservice.cn/tlzbxx/index_{}.htm',

            'http://www.gzebpubservice.cn/slzbgg/index_{}.htm',
            'http://www.gzebpubservice.cn/slzsjggs/index_{}.htm',
            'http://www.gzebpubservice.cn/slzbhxgs/index_{}.htm',
            'http://www.gzebpubservice.cn/slzbxx/index_{}.htm',

            'http://www.gzebpubservice.cn/ylzbgg/index_{}.htm',
            'http://www.gzebpubservice.cn/ylzsjggs/index_{}.htm',
            'http://www.gzebpubservice.cn/ylzbhxrgs/index_{}.htm',
            'http://www.gzebpubservice.cn/ylzbxx/index_{}.htm',

            'http://www.gzebpubservice.cn/mhzbgg/index_{}.htm',
            'http://www.gzebpubservice.cn/mhzbhxrgs/index_{}.htm',
            'http://www.gzebpubservice.cn/mhzbxx/index_{}.htm',
            'http://www.gzebpubservice.cn/qtzbgg/index_{}.htm',
            'http://www.gzebpubservice.cn/qtzsjggs/index_{}.htm',
            'http://www.gzebpubservice.cn/qtzbhxrgs/index_{}.htm',
            'http://www.gzebpubservice.cn/qtzbxx/index_{}.htm',
            'http://www.gzebpubservice.cn/xecbhxrgs/index_{}.htm',

            'http://www.gzebpubservice.cn/cggg/index_{}.htm',  #政府采购
            'http://www.gzebpubservice.cn/zfcgygg/index_{}.htm',
            'http://www.gzebpubservice.cn/gzgg/index_{}.htm',
            'http://www.gzebpubservice.cn/jggg/index_{}.htm',
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
        # date = '2020-09-22'
        page = 0
        while True:
            page += 1
            text = tool.requests_get(self.url.format(page), self.headers)
            print('*' * 20, page, '*' * 20)
            html = HTML(text)
            # print(11, text)
            # time.sleep(6666)
            detail = html.xpath('/html/body/div[4]/ul[3]/li')
            for li in detail:
                title = li.xpath('./p[1]/a/@title')[0]
                url = li.xpath('./p[1]/a/@href')[0]
                date_Today = li.xpath('./p[2]/text()')[0].replace('\xa0', '').replace('\n', '').\
                    replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
                print(title, url, date_Today)
                # time.sleep(666)
                if tool.Transformation(date) <= tool.Transformation(date_Today):
                    if tool.removal(title, date):
                        self.parse_detile(title, url, date_Today)
                    else:
                        print('【existence】', url)
                        continue
                else:
                    print('日期不符, 正在切换类型', date_Today)
                    self.url = self.url_list.pop(0)
                    page=0

                    break
            if page == 20:
                print('日期不符, 正在切换类型')
                self.url = self.url_list.pop(0)
                break

    def parse_detile(self, title, url, date):
        print(url)
        t = tool.requests_get(url, self.headers).replace('\xa9', '')
        # print(t)
        # time.sleep(2222)
        url_html = etree.HTML(t)
        try:
            detail = url_html.xpath('/html/body/div[3]/div[2]/div')[0]
            detail_html = etree.tostring(detail, method='HTML')
            detail_html = html.unescape(detail_html.decode()).replace("display: none", '')
            detail_text = url_html.xpath('string(/html/body/div[3]/div[2]/div)').replace('\xa0', '').replace('\n', '').\
                replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
            if len(detail_html) < 200:
                int('a')
        except:
            try:
                detail = url_html.xpath('/html/body/div[3]/div[2]/table')[0]
                detail_html = etree.tostring(detail, method='HTML')
                detail_html = html.unescape(detail_html.decode()).replace("display: none", '')
                detail_text = url_html.xpath('string(/html/body/div[3]/div[2]/table)').replace('\xa0', '').replace('\n', ''). \
                    replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
                if len(detail_html) < 200:
                    int('a')
            except:
                detail = url_html.xpath('//*[@class="content"]')[0]
                detail_html = etree.tostring(detail, method='HTML')
                detail_html = html.unescape(detail_html.decode()).replace("display: none", '')
                detail_text = url_html.xpath('string(//*[@class="content"])').replace('\xa0', '').replace('\n',
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
        item['resource'] = '广州市公共资源交易中心'
        item['shi'] = 10001
        item['sheng'] = 10000
        item['removal']= title
        print(item)
        # process_item(item)

    def get_nativeplace(self, addr):
        city = ''
        city_list = [['10001.001', '东山区'], ['10001.01', '花都区'], ['10001.011', '增城'], ['10001.012', '从化'], ['10001.002', '荔湾区'], ['10001.003', '越秀区'], ['10001.004', '海珠区'], ['10001.005', '天河区'], ['10001.006', '芳村区'], ['10001.007', '白云区'], ['10001.008', '黄埔区'], ['10001.009', '番禺区'], ['10001.013', '南沙区'], ['10001.014', '开发区']]

        for i in city_list:
            if i[1] in addr:
                city = float(i[0])
                break
        if city == '':
            city = 10001
        return city

if __name__ == '__main__':
    import traceback,os
    try:
        jl = wenshan_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
        tool.send_error('报错文件：'+str(os.path.basename(__file__))+'报错信息：'+str(e))



