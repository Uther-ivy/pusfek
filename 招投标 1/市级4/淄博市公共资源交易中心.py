# -*- coding: utf-8 -*-
import json
import re
import time,html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 淄博市公共资源交易中心
class wenshan_ggzy:
    def __init__(self):
        self.domain_name = 'http://ggzyjy.zibo.gov.cn'
        self.url_list = [
            'http://ggzyjy.zibo.gov.cn:8082/EpointWebBuilder_zbggzy/rest/frontAppCustomAction/getPageInfoListNew',
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
        # date = '2020-09-27'
        page = 0

        while True:
            data ='params={"siteGuid":"7eb5f7f1-9041-43ad-8e13-8fcb82ea831a","categoryNum":"002001001","kw":"","startDate":"","endDate":"","jystauts":"","areacode":"","pageIndex":' + f'"{page}"' + ',"pageSize":14}'
            page += 1
            texts = requests.post(url=self.url, params=data, headers=self.headers)
            text=texts.text
            page_text = json.loads(text)
            detail = page_text['custom']['infodata']
            print('*' * 20, page, '*' * 20)
            # print(11, text.replace('\ufffd', ' ').replace('\u30fb', ' '))
            # time.sleep(6666)
            for li in detail:
                title = li["title"].split('</font>')[1]
                infoid = li["infoid"]
                url2 = f'http://ggzyjy.zibo.gov.cn:8082/jyxx/002001/002001001/20230316/{infoid}.html'
                date_Today = li["infodate"]
                # print(title, url, date_Today)
                # time.sleep(666)
                if tool.Transformation(date) <= tool.Transformation(date_Today):
                    if tool.removal(title, date):
                        self.parse_detile(title, url2, date_Today)
                    else:
                        print('【existence】', url2)
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
        # print(t)
        # time.sleep(2222)
        url_html = etree.HTML(t)
        detail = url_html.xpath('//*[@class="article-content"]')[0]
        detail_html = etree.tostring(detail, method='HTML')
        detail_html = html.unescape(detail_html.decode()).replace("display: none", '').replace("\u2022", '').replace('\xa0', '')
        detail_text = url_html.xpath('string(//*[@class="article-content"])').replace('\xa0', '').replace('\n',
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
        # d = re.findall('''<td align='center' style='border:0;'>.*?</td>''', item['body'], re.S)
        # if len(d) != 0:
        #     item['body'] = item['body'].replace(d[0], '').replace('\xa0', '')
        # d = re.findall('''<td align="center" style="border:0;">.*?</td>''', item['body'], re.S)
        # if len(d) != 0:
        #     item['body'] = item['body'].replace(d[0], '').replace('\xa0', '')
        # print(item['body'])
        # time.sleep(2222)
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
        item['resource'] = '淄博市公共资源交易中心'
        item['shi'] = 8003
        item['sheng'] = 8000
        item['removal']= title
        process_item(item)
        # print(item)

    def get_nativeplace(self, addr):
        city = ''
        city_list = [['8003.001', '淄川区'], ['8003.002', '张店区'], ['8003.003', '博山区'], ['8003.004', '临淄区'], ['8003.005', '周村区'], ['8003.006', '桓台县'], ['8003.007', '高青县'], ['8003.008', '沂源县']]

        for i in city_list:
            if i[1] in addr:
                city = float(i[0])
                break
        if city == '':
            city = 8003
        return city

if __name__ == '__main__':
    import os,traceback
    try:
        jl = wenshan_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
        tool.send_error('报错文件：'+str(os.path.basename(__file__))+'报错信息：'+str(e))



