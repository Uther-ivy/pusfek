# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 衡州市公共资源交易平台
class hengzhou_ggzy:
    def __init__(self):
        self.url_list = [
            # 工程建设
            # 招标公告
            'http://www.qzggzy.com/jyxx/002001/002001001/{}.html',
            # 变更
            'http://www.qzggzy.com/jyxx/002001/002001002/{}.html',
            # 开标结果
            'http://www.qzggzy.com/jyxx/002001/002001003/{}.html',
            # 中标候选人
            'http://www.qzggzy.com/jyxx/002001/002001004/{}.html',
            # 中标结果
            'http://www.qzggzy.com/jyxx/002001/002001005/{}.html',
            # 政府采购
            # 采购公告
            'http://www.qzggzy.com/jyxx/002002/002002001/{}.html',
            # 结果公告
            'http://www.qzggzy.com/jyxx/002002/002002002/{}.html',
        ]
        self.url = self.url_list.pop(0)
        self.headers = {
            'Cookie': 'userGuid=-254005787; oauthClientId=demoClient; oauthPath=http://10.27.160.93:8085/EWB-FRONT; oauthLoginUrl=http://127.0.0.1/membercenter/login.html?redirect_uri=; oauthLogoutUrl=; noOauthRefreshToken=dc35e16e1aed24a6bbe9a12ea4f6f8ea; noOauthAccessToken=62c70dd64ec2282be3dec779fa227993; Hm_lvt_49eb16f81255f9e335185e10838d3291=1582331455; SERVERID=dfe46d418da073a2a2f91876a644ba26|1582331875|1582331453; Hm_lpvt_49eb16f81255f9e335185e10838d3291=1582331876',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        }

    def parse(self):
        date = tool.date
        # date = '2020-02-21'
        page = 0
        while True:
            page += 1
            text = tool.requests_get(self.url.format(page), self.headers)
            if page == 1:
                text = tool.requests_get(self.url.format('trade'), self.headers)
            print('*' * 20, page, '*' * 20)
            html = HTML(text)
            # print(11, text)
            # time.sleep(6666)
            detail = html.xpath('/html/body/div[2]/div/div[2]/div/div[2]/ul/li')
            for li in detail:
                title = li.xpath('string(./div/a)').replace(' ', '').replace('\n', '').replace('\r', '').replace('\t', '')
                url = 'http://www.qzggzy.com' + li.xpath('./div/a/@href')[0]
                date_Today = li.xpath('./span/text()')[0]
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
                self.url = self.url_list.pop(0)
                break
    def parse_detile(self, title, url, date):
        print(url)
        url_html = etree.HTML(tool.requests_get(url, self.headers))
        try:
            detail = url_html.xpath('/html/body/div[2]/div[3]/div[2]/div[3]')[0]
            detail_html = etree.tostring(detail, method='HTML')
            detail_html = html.unescape(detail_html.decode())
            detail_text = url_html.xpath('string(/html/body/div[2]/div[3]/div[2]/div[3])').replace('\xa0', '').replace(
                '\n', ''). \
                replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
        except:
            try:
                detail = url_html.xpath('/html/body/div[2]/div[3]/div[2]/div[2]/div[1]/div[3]/div/div[1]/div[1]')[0]
                detail_html = etree.tostring(detail, method='HTML')
                detail_html = html.unescape(detail_html.decode())
                detail_text = url_html.xpath(
                    'string(/html/body/div[2]/div[3]/div[2]/div[2]/div[1]/div[3]/div/div[1]/div[1])').replace('\xa0',
                                                                                                              '').replace(
                    '\n', ''). \
                    replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
            except:
                try:
                    detail = url_html.xpath('/html/body/div[2]/div[3]/div[2]/div[2]/div[1]/div[3]')[0]
                    detail_html = etree.tostring(detail, method='HTML')
                    detail_html = html.unescape(detail_html.decode())
                    detail_text = url_html.xpath(
                        'string(/html/body/div[2]/div[3]/div[2]/div[2]/div[1]/div[3])').replace('\xa0',
                                                                                                                  '').replace(
                        '\n', ''). \
                        replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
                except:
                    detail = url_html.xpath('/html/body/div[2]/div[3]/div[2]/div[2]/div[1]')[0]
                    detail_html = etree.tostring(detail, method='HTML')
                    detail_html = html.unescape(detail_html.decode())
                    detail_text = url_html.xpath(
                        'string(/html/body/div[2]/div[3]/div[2]/div[2]/div[1])').replace('\xa0',
                                                                                                '').replace(
                        '\n', ''). \
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
        item['body'] = detail_html
        width_list = re.findall('width="(.*?)"', item["body"])
        for i in width_list:
            item["body"] = item["body"].replace('width="{}"'.format(i), '')
        width_list = re.findall('WIDTH: (.*?)pt;', item["body"])
        for i in width_list:
            item["body"] = item["body"].replace('WIDTH: {}pt;'.format(i), '')
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
        item['resource'] = '衡州市公共资源交易平台'
        item['shi'] = 6008
        item['sheng'] = 6000
        item['removal']= title
        process_item(item)

    def get_nativeplace(self, addr):
        city = ''
        city_list = [['6008.001', '柯城区'], ['6008.002', '衢江区'], ['6008.003', '常山县'], ['6008.004', '开化县'], ['6008.005', '龙游县'], ['6008.006', '江山市']]
        for i in city_list:
            if i[1] in addr:
                city = float(i[0])
                break
        if city == '':
            city = 6008
        return city
if __name__ == '__main__':

    import traceback, os
    try:
        jl = hengzhou_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
        tool.send_error('报错文件：'+str(os.path.basename(__file__))+'报错信息：'+str(e))


