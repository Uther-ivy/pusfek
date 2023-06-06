# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 甘南藏族自治州资源交易中心
class wenshan_ggzy:
    def __init__(self):
        self.domain_name = 'http://ggzyjy.gnzrmzf.gov.cn'
        self.url_list = [
            'http://ggzyjy.gnzrmzf.gov.cn/f/newtrade/annogoods/getAnnoList?pageNo={}&pageSize=20&tradeStatus=0&prjpropertycode=1%2C2%2C3%2C4%2C5%2C6%2C7%2C8%2C9%2C10%2C11&prjpropertycode=21%2C22%2C23%2C24&prjpropertycode=31&prjpropertycode=13%2C14%2C15%2C16%2C18%2C19%2C20&prjpropertycode=600&tradeArea=14&projectname=&tabType=2&tradeType=',
            'http://ggzyjy.gnzrmzf.gov.cn/f/newtrade/annogoods/getAnnoList?pageNo={}&pageSize=20&tradeStatus=0&prjpropertycode=1%2C2%2C3%2C4%2C5%2C6%2C7%2C8%2C9%2C10%2C11&prjpropertycode=21%2C22%2C23%2C24&prjpropertycode=31&prjpropertycode=13%2C14%2C15%2C16%2C18%2C19%2C20&prjpropertycode=600&tradeArea=14&projectname=&tabType=1&tradeType=',
            'http://ggzyjy.gnzrmzf.gov.cn/f/newtrade/annogoods/getAnnoList?pageNo={}&pageSize=20&tradeStatus=0&prjpropertycode=1%2C2%2C3%2C4%2C5%2C6%2C7%2C8%2C9%2C10%2C11&prjpropertycode=21%2C22%2C23%2C24&prjpropertycode=31&prjpropertycode=13%2C14%2C15%2C16%2C18%2C19%2C20&prjpropertycode=600&tradeArea=14&projectname=&tabType=3&tradeType='
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
        # date = '2020-09-25'
        page = 0
        while True:
            text = tool.requests_get(self.url.format(page), self.headers)
            page += 1
            print('*' * 20, page, '*' * 20)
            html = HTML(text)
            detail = html.xpath('//*[@class="byTradingDetail-Con byTradingDetail-ConActive"]/dl')
            for li in detail:
                title = li.xpath('string(./dd/a)').replace('\xa0', '').replace('\n', ''). \
                    replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
                url = li.xpath('./dd/a/@href')[0]
                url = 'http://ggzyjy.gnzrmzf.gov.cn/f/newtenderproject/flowBidpackage?tenderprojectid={}&projectType=H02'\
                    .format(url.replace('/f/newtenderproject/', '').replace('/flowpage', ''))
                date_Today = li.xpath('./dd/span/text()')[0].replace('\xa0', '').replace('\n', ''). \
                    replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '') \
                    .replace('[', '').replace(']', '').replace('/', '-')
                if date_Today == '':
                    date_Today = li.xpath('./dd/span[2]/text()')[0].replace('\xa0', '').replace('\n', ''). \
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
        t = tool.requests_get(url, '').replace('\xa9', '').replace('<br>&nbsp;&nbsp;', '')
        # print(t)
        # time.sleep(2222)
        url_html = etree.HTML(t)
        detail = url_html.xpath('/html/body')[0]
        detail_html = etree.tostring(detail, method='HTML')
        detail_html = html.unescape(detail_html.decode()).replace("display: none", '')
        detail_text = url_html.xpath('string(/html/body)').replace('\xa0', '').replace('\n',
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
        item['address'] = tool.get_address(detail_text)
        item['linkman'] = tool.get_linkman(detail_text)
        item['function'] = tool.get_function(detail_text)
        item['resource'] = '甘南藏族自治州资源交易中心'
        item['shi'] = 14514
        item['sheng'] = 14500
        item['removal']= title
        process_item(item)

    def get_nativeplace(self, addr):
        city = ''
        city_list = [['14514.001', '合作'], ['14514.002', '临潭县'], ['14514.003', '卓尼县'], ['14514.004', '舟曲县'], ['14514.005', '迭部县'], ['14514.006', '玛曲县'], ['14514.007', '碌曲县'], ['14514.008', '夏河县']]

        for i in city_list:
            if i[1] in addr:
                city = float(i[0])
                break
        if city == '':
            city = 14514
        return city

if __name__ == '__main__':
    import traceback, os
    try:
        jl = wenshan_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
        tool.send_error('报错文件：'+str(os.path.basename(__file__))+'报错信息：'+str(e))


