# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 德州市公共资源交易网
class baoshan_ggzy:
    def __init__(self):
        self.url_list = [
            'http://ggzyjy.dezhou.gov.cn/TPFront/xmxx/004001/moreinfo3.html',
            'http://ggzyjy.dezhou.gov.cn/TPFront/xmxx/004002/moreinfo4.html'
                         ]
        self.url = self.url_list.pop(0)
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36',
        }

    def parse(self):
        headers = {
            'X-Requested-With': 'XMLHttpRequest',
            'Cookie': 'JSESSIONID=EE9EEA3039139A93B9CBD7C5C1EE7AE2; oauthClientId=demoClient; oauthPath=http://10.2.129.27:8080/EpointWebBuilder; oauthLoginUrl=http://10.2.129.27:8080/EpointWebBuilder/rest/oauth2/authorize?client_id=demoClient&state=a&response_type=code&scope=user&redirect_uri=; oauthLogoutUrl=http://10.2.129.27:8080/EpointWebBuilder/rest/oauth2/logout?redirect_uri=; noOauthRefreshToken=8bd2d30fd631dc551d08f2de52a3a8d9; noOauthAccessToken=a71666fe5919732927887d397a4cd13b',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36',
        }
        date = tool.date
        # date = '2021-07-29'
        page = 0
        while True:
            text = tool.requests_get(self.url, self.headers)
            page += 1
            print('*' * 20, page, '*' * 20)
            html = HTML(text)
            # print(11, text)
            # time.sleep(6666)
            detail = html.xpath('//*[@id="categorypagingcontent"]/div/div//li')
            for li in detail:
                title = li.xpath('./a/@title')[0].replace('\n', '').replace('\r', '')\
                    .replace('\t', '').replace(' ', '').replace('<spanstyle="color:red">', '').replace('</span>', '')
                try:
                    url = li.xpath('./a/@href')[0]
                    code = re.findall('infoid=(.*?)&categorynum=(.*?)&', url)[0]
                    data = 'params=%7B%22siteGuid%22%3A%227eb5f7f1-9041-43ad-8e13-8fcb82ea831a%22%2C%22infoid%22%3A%22{}%22%2C%22categorynum%22%3A%22{}%22%7D'.format(code[0],code[1])
                    u = tool.requests_post('http://ggzyjy.dezhou.gov.cn:8086/EpointWebBuilder/rest/frontAppCustomAction/getInfoUrlByInfoid', data, headers)
                    url = 'http://ggzyjy.dezhou.gov.cn/TPFront' + json.loads(u)['custom']['infourl']
                except:
                    url = li.xpath('./a/@href')[0]
                    if 'http' not in url:
                        url = 'http://ggzyjy.dezhou.gov.cn' + url
                date_Today = date[:5] + li.xpath('./span/text()')[0].replace('\n', '').replace('\r', '') \
                    .replace('\t', '').replace(' ', '').replace('(', '').replace(')', '')
                if '测试' in title:
                    continue
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
                    continue
            self.url = self.url_list.pop(0)
            page = 0

    def parse_detile(self, title, url, date):
        print(url)
        t = tool.requests_get(url, self.headers)
        url_html = etree.HTML(t)
        try:
            detail = url_html.xpath('//*[@id="mainContent"]')[0]
            detail_html = etree.tostring(detail, method='HTML')
            detail_html = html.unescape(detail_html.decode())
            detail_text = url_html.xpath('string(//*[@id="mainContent"])').replace('\xa0', '').replace('\n',
                                                                                                              ''). \
                replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
        except:
            return
        # print(t.replace('\xa0','').replace('\xa5',''))
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
        item['resource'] = '德州市公共资源交易网'
        item['shi'] = 8013
        item['sheng'] = 8000
        item['removal']= title
        process_item(item)

    def get_nativeplace(self, addr):
        city = ''
        city_list = [['8013.001', '德城区'], ['8013.01', '乐陵市'], ['8013.011', '禹城市'], ['8013.002', '陵县'], ['8013.003', '宁津县'], ['8013.004', '庆云县'], ['8013.005', '临邑县'], ['8013.006', '齐河县'], ['8013.007', '平原县'], ['8013.008', '夏津县'], ['8013.009', '武城县']]

        for i in city_list:
            if i[1] in addr:
                city = float(i[0])
                break
        if city == '':
            city = 8013
        return city

if __name__ == '__main__':
    import traceback, os
    try:
        jl = baoshan_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
        tool.send_error('报错文件：'+str(os.path.basename(__file__))+'报错信息：'+str(e))


