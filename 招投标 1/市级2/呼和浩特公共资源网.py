# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 呼和浩特公共资源网
class wenshan_ggzy:#  cookies token 時效性
    def __init__(self):
        self.url_list = [
            '002001001',#建设工程
            '002001002',
            '002001003',
            '002001004',
            '002002001',
            '002002002',
            '002002003',
            '002002004',
                    ]
        self.url = self.url_list.pop(0)#"/EpointWebBuilder/rest/frontAppCustomAction/getPageInfoListNew"
        self.headers = {
            'Authorization': 'Bearer 57fae8a51c055f6aa48c1d7ed2d0bc50',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Cookie': 'userGuid=-254005787; oauthClientId=b140d011-5c07-4c50-89fe-f1bcc37977e1; oauthPath=http://42.123.92.182:9010/TPFrame; oauthLoginUrl=http://127.0.0.1/membercenter/login.html?redirect_uri=; oauthLogoutUrl=; noOauthRefreshToken=4573dcb0bbd9953d6b36841348597baa; noOauthAccessToken=7124c3b4025f2a3dc32fb469bd1ae43a; lastAccessTimestamp=1630572398856',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        }

    def parse(self):
        date = tool.date
        # date = '2020-04-02'
        page = 0
        url_ = 'http://42.123.92.182:9010/EpointWebBuilder/rest/frontAppCustomAction/getPageInfoListNew'
        while True:
            page += 1 # 获取 token 8efe319d3808b8a17e28c5b69d3402b2
            token_url = 'http://42.123.92.182:9010/EpointWebBuilder/rest/getOauthInfoAction/getNoUserAccessToken'
            token = json.loads(tool.requests_post(token_url, '', self.headers))['custom']['access_token']
            self.headers['Authorization'] = 'Bearer '+ token
            data = 'params=%7B%22siteGuid%22%3A%227eb5f7f1-9041-43ad-8e13-8fcb82ea831a%22%2C%22categoryNum%22%3A%22'+self.url+'%22%2C%22kw%22%3A%22%22%2C%22startDate%22%3A%22%22%2C%22endDate%22%3A%22%22%2C%22pageIndex%22%3A'+str(page-1)+'%2C%22pageSize%22%3A10%7D'
            text = tool.requests_post(url_, data, self.headers)
            detail = json.loads(text)['custom']['infodata']
            for li in detail:
                title = li['title']
                url = 'http://42.123.92.182:9010' + li['infourl']
                date_Today = li['infodate'].replace('[', '').replace(']', '').replace('\r',
                                                                                                     '').replace(
                    '\n', '').replace('\t', '').replace(' ', '')
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
                    page = 0
                    break
            self.url = self.url_list.pop(0)

    def parse_detile(self, title, url, date):
        print(url)
        t = tool.requests_get(url, self.headers)
        url_html = etree.HTML(t)
        try:
            detail = url_html.xpath('//*[@id="noticeArea"]')[0]
            detail_html = etree.tostring(detail, method='HTML')
            detail_html = html.unescape(detail_html.decode())
            detail_text = url_html.xpath('string(//*[@id="noticeArea"])').replace('\xa0', '').replace('\n', '').\
                replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
        except:
            detail = url_html.xpath('//*[@class="news-wrap tabview"]')[0]
            detail_html = etree.tostring(detail, method='HTML')
            detail_html = html.unescape(detail_html.decode())
            detail_text = url_html.xpath('string(//*[@class="news-wrap tabview"])').replace('\xa0', '').replace('\n', ''). \
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
        item['resource'] = '呼和浩特公共资源网'
        item['shi'] = 3001
        item['sheng'] = 3000
        item['removal']= title
        process_item(item)

    def get_nativeplace(self, addr):
        city = ''
        city_list = [['3001.001', '新城区'], ['3001.002', '回民区'], ['3001.003', '玉泉区'], ['3001.004', '赛罕区'], ['3001.005', '土默特左旗'], ['3001.006', '托克托县'], ['3001.007', '和林格尔县'], ['3001.008', '清水河县'], ['3001.009', '武川县']]

        for i in city_list:
            if i[1] in addr:
                city = float(i[0])
                break
        if city == '':
            city = 3001
        return city

if __name__ == '__main__':
    import traceback,os
    try:
        jl = wenshan_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
