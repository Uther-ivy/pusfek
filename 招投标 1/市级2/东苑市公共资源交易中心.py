# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 东苑市公共资源交易中心
class wenshan_ggzy:
    def __init__(self):
        self.url_list = [
            'http://ggzy.dg.gov.cn/ggzy/website/WebPagesManagement/findListByPage?fcInfotype=1&tenderkind=All&projecttendersite=SS&orderFiled=fcInfostartdate&orderValue=desc&fcInfotitle=&currentPage={}',
            'http://ggzy.dg.gov.cn/ggzy/website/WebPagesManagement/findListByPage?fcInfotype=4&tenderkind=All&projecttendersite=SS&fcInfotitle=&currentPage={}',
            'http://ggzy.dg.gov.cn/ggzy/website/WebPagesManagement/findListByPage?fcInfotype=7&tenderkind=All&projecttendersite=SS&orderFiled=fcInfostartdate&orderValue=desc&fcInfotitle=&extType=0&fcInfotype=7&currentPage={}',
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
            detail = json.loads(text)['ls']
            for li in detail:
                title = li['fcInfotitle']
                if 'TradeInfo/GovProcurement' not in self.url:
                    if 'fcInfotype=1' in self.url:
                        url = 'http://ggzy.dg.gov.cn/ggzy/website/WebPagesManagement/jsdetail?publishId={}&fcInfotype=1'.format(li['id'])
                    elif 'fcInfotype=4' in self.url:
                        url = 'http://ggzy.dg.gov.cn/ggzy/website/WebPagesManagement/jsdetail?publishId={}&fcInfotype=4'.format(
                            li['id'])
                    else:
                        url = 'http://ggzy.dg.gov.cn/ggzy/website/WebPagesManagement/jsdetail?publishId={}&fcInfotype=7'.format(
                            li['id'])
                else:
                    if 'fcInfotype=1' in self.url:
                        url = 'http://ggzy.dg.gov.cn/ggzy/website/WebPagesManagement/TradeInfo/GovProcurement/govdetail?publishinfoid={}&fcInfotype=1'.format(li['publishinfoid'])
                    elif 'fcInfotype=4' in self.url:
                        url = 'http://ggzy.dg.gov.cn/ggzy/website/WebPagesManagement/TradeInfo/GovProcurement/govdetail?publishinfoid={}&fcInfotype=4'.format(li['publishinfoid'])
                    else:
                        url = 'http://ggzy.dg.gov.cn/ggzy/website/WebPagesManagement/TradeInfo/GovProcurement/govdetail?publishinfoid={}&fcInfotype=7'.format(li['publishinfoid'])
                try:
                    date_Today = li['fcInfostartdate'][:10].replace('\xa0', '').replace('\n', '').\
                        replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
                except:
                    date_Today = li['fdPublishtime'][:10].replace('\xa0', '').replace('\n', ''). \
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
        t = tool.requests_get(url, self.headers).replace('\xa9', '')
        # print(t)
        # time.sleep(2222)
        url_html = etree.HTML(t)
        try:
            detail = url_html.xpath('//*[@class="content"]')[0]
        except:
            return
        detail_html = etree.tostring(detail, method='HTML')
        detail_html = html.unescape(detail_html.decode()).replace("display: none", '')
        detail_text = url_html.xpath('string(//*[@class="content"])').replace('\xa0', '').replace('\n', '').\
            replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
        if '补充通知详见附件！' in detail_html:
            print('补充通知详见附件！')
            return
        item = {}
        item['title'] = title.replace('\u2022', '')
        item['url'] = url
        item['date'] = date
        item['typeid'] = tool.get_typeid(item['title'])
        item['senddate'] = int(time.time())
        item['mid'] = 867
        item['nativeplace'] = 10017
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
        item['resource'] = '东苑市公共资源交易中心'
        item['shi'] = 10017
        item['sheng'] = 10000
        item['removal']= title
        process_item(item)

    def get_nativeplace(self, addr):
        city = ''
        city_list = [['14009.001', '汉滨区'], ['14009.01', '白河县'], ['14009.002', '汉阴县'], ['14009.003', '石泉县'], ['14009.004', '宁陕县'], ['14009.005', '紫阳县'], ['14009.006', '岚皋县'], ['14009.007', '平利县'], ['14009.008', '镇坪县'], ['14009.009', '旬阳县']]

        for i in city_list:
            if i[1] in addr:
                city = float(i[0])
                break
        if city == '':
            city = 14009
        return city

if __name__ == '__main__':
    import os, traceback
    try:
        jl = wenshan_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
        tool.send_error('报错文件：'+str(os.path.basename(__file__))+'报错信息：'+str(e))


