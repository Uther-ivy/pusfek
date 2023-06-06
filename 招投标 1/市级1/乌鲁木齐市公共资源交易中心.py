# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 乌鲁木齐市公共资源交易中心
class wenshan_ggzy:
    def __init__(self):
        self.url_list = [
            '001001',
            '001002'
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
        url_to = 'http://zwfw.wlmq.gov.cn/EWB-FRONT/rest/frontAppCustomAction/getPageInfoListNewYzm'
        while True:
            data = 'siteGuid=7eb5f7f1-9041-43ad-8e13-8fcb82ea831a&categoryNum=001001&pageIndex={}&pageSize=15&jyStatus=&kw='.format(page)
            page += 1
            text = tool.requests_post(url_to, data, self.headers)
            print('*' * 20, page, '*' * 20)
            # print(11, text)
            # time.sleep(6666)
            detail = json.loads(text)['custom']['infodata']
            for li in detail:
                title = li['title']
                url = 'http://zwfw.wlmq.gov.cn' + li['infourl']
                date_Today = li['infodate'].replace('\xa0', '').replace('\n', '').\
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
                    print('日期不符, 正在切换类型', date_Today)
                    self.url = self.url_list.pop(0)
                    page = 0
                    break
            if page == 20:
                print('日期不符, 正在切换类型')
                self.url = self.url_list.pop(0)
                break

    def parse_detile(self, title, url, date):
        print(url)
        t = tool.requests_get(url, self.headers)
        # print(t)
        # time.sleep(2222)
        url_html = etree.HTML(t)
        try:
            detail = url_html.xpath('/html/body/div[2]/div[2]/div/div[2]/div/table')[0]
            detail_html = etree.tostring(detail, method='HTML')
            detail_html = html.unescape(detail_html.decode()).replace("display: none", '')
            detail_text = url_html.xpath('string(/html/body/div[2]/div[2]/div/div[2]/div/table)').replace('\xa0', '').replace('\n', '').\
                replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
            if len(detail_html) < 200:
                int('a')
        except:
            try:
                detail = url_html.xpath('/html/body/div[2]/div[2]/div/div[2]/div/div/div[3]')[0]
                detail_html = etree.tostring(detail, method='HTML')
                detail_html = html.unescape(detail_html.decode()).replace("display: none", '')
                detail_text = url_html.xpath('string(/html/body/div[2]/div[2]/div/div[2]/div/div/div[3])').replace('\xa0',
                                                                                                                   '').replace(
                    '\n', ''). \
                    replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
                if len(detail_html) < 200:
                    int('a')
            except:
                try:
                    detail = url_html.xpath('/html/body/div[2]/div[2]/div/div[2]/div/div/table')[0]
                    detail_html = etree.tostring(detail, method='HTML')
                    detail_html = html.unescape(detail_html.decode()).replace("display: none", '')
                    detail_text = url_html.xpath('string(/html/body/div[2]/div[2]/div/div[2]/div/div/table)').replace(
                        '\xa0',
                        '').replace(
                        '\n', ''). \
                        replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
                    if len(detail_html) < 200:
                        int('a')
                except:
                    detail = url_html.xpath('//*[@class="ewb-cont"]')[0]
                    detail_html = etree.tostring(detail, method='HTML')
                    detail_html = html.unescape(detail_html.decode()).replace("display: none", '')
                    detail_text = url_html.xpath('string(//*[@class="ewb-cont"])').replace(
                        '\xa0',
                        '').replace(
                        '\n', ''). \
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
        item['resource'] = '乌鲁木齐市公共资源交易中心'
        item['shi'] = 16001
        item['sheng'] = 16000
        item['removal']= title
        process_item(item)
    def get_nativeplace(self, addr):
        city = ''
        city_list = [['16001.001', '天山区'], ['16001.002', '沙依巴克区'], ['16001.003', '新区'], ['16001.004', '水磨沟区'], ['16001.005', '头屯河区'], ['16001.006', '达坂城区'], ['16001.007', '东山区'], ['16001.008', '乌鲁木齐县']]

        for i in city_list:
            if i[1] in addr:
                city = float(i[0])
                break
        if city == '':
            city = 16001
        return city

if __name__ == '__main__':
    import traceback,os
    try:
        jl = wenshan_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
        tool.send_error('报错文件：'+str(os.path.basename(__file__))+'报错信息：'+str(e))


