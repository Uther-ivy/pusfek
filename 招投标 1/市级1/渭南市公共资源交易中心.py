# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 渭南市公共资源交易中心
class wenshan_ggzy:
    def __init__(self):
        self.domain_name = 'http://ggzy.weinan.gov.cn'
        self.url_list = [
            'http://ggzy.weinan.gov.cn/wnggzyweb/jyxx/002001/002001006/002001006002/?Paging={}',
            'http://ggzy.weinan.gov.cn/wnggzyweb/jyxx/002001/002001006/002001006001/?Paging={}',
            'http://ggzy.weinan.gov.cn/wnggzyweb/jyxx/002001/002001006/002001006003/?Paging={}',#结果
            'http://ggzy.weinan.gov.cn/wnggzyweb/jyxx/002001/002001007/002001007001/?Paging={}',
            'http://ggzy.weinan.gov.cn/wnggzyweb/jyxx/002001/002001007/002001007002/?Paging={}',
            'http://ggzy.weinan.gov.cn/wnggzyweb/jyxx/002001/002001007/002001007003/?Paging={}',#结果

            'http://ggzy.weinan.gov.cn/wnggzyweb/jyxx/002001/002001008/002001008001/?Paging={}',
            'http://ggzy.weinan.gov.cn/wnggzyweb/jyxx/002001/002001008/002001008002/?Paging={}',
            'http://ggzy.weinan.gov.cn/wnggzyweb/jyxx/002001/002001008/002001008003/?Paging={}',

            'http://ggzy.weinan.gov.cn/wnggzyweb/jyxx/002002/002002001/?Paging={}',
            'http://ggzy.weinan.gov.cn/wnggzyweb/jyxx/002002/002002003/?Paging={}',
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
        # date = '2021-07-22'
        page = 0
        while True:
            page += 1
            # text = requests.get(self.url.format(page), headers=self.headers).text
            text = tool.requests_get(self.url.format(page), self.headers)
            print('*' * 20, page, '*' * 20)
            html = HTML(text)
            # print(11, text.replace('\ufffd', ' ').replace('\u30fb', ' '))
            # time.sleep(6666)
            detail = html.xpath('/html/body/div[2]/div/div[2]/div[2]/div[2]/div[1]/table/tr')
            for li in detail:
                title = li.xpath('./td[2]/a/@title')[0]
                url = li.xpath('./td[2]/a/@href')[0]
                date_Today = li.xpath('./td[3]/span/text()')[0].replace('\xa0', '').replace('\n', '').\
                    replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')\
                    .replace('[', '').replace(']', '')
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
                    return


    def parse_detile(self, title, url, date):
        print(url)
        t = tool.requests_get(url, self.headers).replace('\xa9', '').replace('<br>&nbsp;&nbsp;', '')
        # print(t)
        # time.sleep(2222)
        url_html = etree.HTML(t)
        detail = url_html.xpath('/html/body/div[2]/div/table/tr[3]/td/table')[0]
        detail_html = etree.tostring(detail, method='HTML')
        detail_html = html.unescape(detail_html.decode()).replace("display: none", '')
        detail_text = url_html.xpath('string(/html/body/div[2]/div/table/tr[3]/td/table)').replace('\xa0', '').replace('\n',
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
        # d = re.findall('<table id="tb_Line".*?</table>', item['body'], re.S)
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
        item['winner'] = tool.get_winner(detail_text)
        item['address'] = tool.get_address(detail_text)
        item['linkman'] = tool.get_linkman(detail_text)
        item['function'] = tool.get_function(detail_text)
        item['resource'] = '渭南市公共资源交易中心'
        item['shi'] = 14005
        item['sheng'] = 14000
        item['removal']= title
        process_item(item)

    def get_nativeplace(self, addr):
        city = ''
        city_list = [['14005.001', '临渭区'], ['14005.01', '韩城'], ['14005.011', '华阴'], ['14005.002', '华县'], ['14005.003', '潼关县'], ['14005.004', '大荔县'], ['14005.005', '合阳县'], ['14005.006', '澄城县'], ['14005.007', '蒲城县'], ['14005.008', '白水县'], ['14005.009', '富平县']]

        for i in city_list:
            if i[1] in addr:
                city = float(i[0])
                break
        if city == '':
            city = 14005
        return city

if __name__ == '__main__':
    import traceback,os
    try:
        jl = wenshan_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
        tool.send_error('报错文件：'+str(os.path.basename(__file__))+'报错信息：'+str(e))


