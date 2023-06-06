# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 黄山市公共资源交易中心
class wenshan_ggzy:
    def __init__(self):
        self.url_list = [
            'http://ggzy.huangshan.gov.cn/004/{}.html'
                    ]
        self.url = self.url_list.pop(0)
        self.headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Authorization': 'Bearer a13fbde57542726bfdf767df62db2215',
            'Host': 'ggzy.huangshan.gov.cn',
            'Cookie': 'userGuid=1047923792; oauthClientId=demoClient; oauthPath=http://172.18.15.23:8080/EpointWebBuilder; oauthLoginUrl=http://172.18.15.23:8080/EpointWebBuilder/rest/oauth2/authorize?client_id=demoClient&state=a&response_type=code&scope=user&redirect_uri=; oauthLogoutUrl=http://172.18.15.23:8080/EpointWebBuilder/rest/oauth2/logout?redirect_uri=; noOauthRefreshToken=321eb297b77af19006ecb02eda04cd48; noOauthAccessToken=a13fbde57542726bfdf767df62db2215',
            'Origin': 'http://ggzy.huangshan.gov.cn',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        }

    def parse(self):
        date = tool.date
        # date = '2020-04-02'
        page = 0
        while True:
            page += 1
            if page == 1:
                text = tool.requests_get(self.url.format('subSearch'), self.headers)
            else:
                text = tool.requests_get(self.url.format(page), self.headers)
            detail = HTML(text).xpath('//*[@id="xiangmubody"]/tr')
            for li in detail:
                title = li.xpath('./td[2]/a/div/text()')[0]
                code = li.xpath('./td[2]/a/@onclick')[0].replace('redirectDetail(', '').replace(')','').replace("'",'').split(',')
                # Authorization 时效性
                Authorization_url = 'http://ggzy.huangshan.gov.cn/EWB-FRONT/rest/getOauthInfoAction/getNoUserAccessToken'
                Authorization =json.loads(tool.requests_post(Authorization_url, '', self.headers))['custom']['access_token']
                self.headers['Authorization'] = 'Bearer ' + Authorization
                code_url = 'http://ggzy.huangshan.gov.cn/EWB-FRONT/rest/webbuilderserverforHeFZTB/pageredirect'
                code_data = {
                    'params': '{"infoid":"'+code[0]+'","siteGuid":"7eb5f7f1-9041-43ad-8e13-8fcb82ea831a",' \
                                                          '"categorynum":"'+code[1]+'"}'
                }
                url = 'http://ggzy.huangshan.gov.cn' + json.loads(tool.requests_post(code_url, code_data, self.headers))['infoUrl']
                try:
                    date_Today = li.xpath('./td[4]/text()')[0]
                except:
                    date_Today = li.xpath('./td[3]/text()')[0]
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
                    self.url = self.url_list.pop(0)
                    page = 0
                    break
            if page == 20:
                self.url = self.url_list.pop(0)
                break

    def parse_detile(self, title, url, date):
        print(url)
        try:
            xq_code = re.findall('infoid=(.*?)&categorynum=(.*?)&relationguid', url)[0]
            xa_url = 'http://ggzy.huangshan.gov.cn/{}/{}/{}/{}/{}.html?v=88'.format(xq_code[1][:3], xq_code[1][:6],xq_code[1],
                                                                                    date.replace('-', ''), xq_code[0])
            t= tool.requests_get(xa_url, self.headers)
            url_html = etree.HTML(t)
            detail = url_html.xpath('//body')[0]
            detail_html = etree.tostring(detail, method='HTML')
            detail_html = html.unescape(detail_html.decode())
            detail_text = url_html.xpath('string(//body)').replace('\xa0', '').replace('\n',
                                                                                                         ''). \
                replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
        except:
            t = tool.requests_get(url, self.headers)
            url_html = etree.HTML(t)
            try:
                detail = url_html.xpath('//*[@id="infoList"]')[0]
                detail_html = etree.tostring(detail, method='HTML')
                detail_html = html.unescape(detail_html.decode())
                detail_text = url_html.xpath('string(//*[@id="infoList"])').replace('\xa0', '').replace('\n',
                                                                                           ''). \
                    replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
            except:
                detail = url_html.xpath('//*[@class="ewb-tab-con"]')[0]
                detail_html = etree.tostring(detail, method='HTML')
                detail_html = html.unescape(detail_html.decode())
                detail_text = url_html.xpath('string(//*[@class="ewb-tab-con"])').replace('\xa0', '').replace('\n',
                                                                                                        ''). \
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
        item['resource'] = '黄山市公共资源交易中心'
        item['shi'] = 6509
        item['sheng'] = 6500
        item['removal']= title
        process_item(item)


    def get_nativeplace(self, addr):
        city = ''
        city_list = [['6509.001', '屯溪区'], ['6509.002', '黄山区'], ['6509.003', '徽州区'], ['6509.004', '歙县'], ['6509.005', '休宁县'], ['6509.006', '黟县'], ['6509.007', '祁门县']]

        for i in city_list:
            if i[1] in addr:
                city = float(i[0])
                break
        if city == '':
            city = 6509
        return city

if __name__ == '__main__':
    import os,traceback
    try:
        jl = wenshan_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
