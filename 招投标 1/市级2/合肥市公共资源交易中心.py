# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 合肥市公共资源交易中心
class wenshan_ggzy:
    def __init__(self):
        self.url_list = [
            'http://ggzy.hefei.gov.cn/jyxx/002001/002001001/{}.html',
            'http://ggzy.hefei.gov.cn/jyxx/002002/002002001/{}.html',
            'http://ggzy.hefei.gov.cn/jyxx/002001/002001002/{}.html',
            'http://ggzy.hefei.gov.cn/jyxx/002002/002002002/{}.html',
            'http://ggzy.hefei.gov.cn/jyxx/002001/002001003/{}.html',
            'http://ggzy.hefei.gov.cn/jyxx/002002/002002004/{}.html',
            'http://ggzy.hefei.gov.cn/jyxx/002001/002001004/{}.html'
            ]
        self.url = self.url_list.pop(0)
        self.headers = {
            'Cookie': 'homeid=1a444a31-e460-47ff-9931-1c075c0f3cd8',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        }

    def parse(self):
        date = tool.date
        # date = '2020-09-16'
        page = 0
        while True:
            page += 1
            if page == 1:
                if '002002004' in self.url:
                    text = tool.requests_get(self.url.format('moreinfo_jyxxzfcggs'), self.headers)
                elif '002001004' in self.url:
                    text = tool.requests_get(self.url.format('moreinfo_jyxx4'), self.headers)
                elif '002001003' in self.url:
                    text = tool.requests_get(self.url.format('moreinfo_jyxxgs2'), self.headers)
                else:
                    text = tool.requests_get(self.url.format('moreinfo_jyxxgg2'), self.headers)
            else:
                text = tool.requests_get(self.url.format(page), self.headers)
            print('*' * 20, page, '*' * 20)
            html = HTML(text)
            # print(11, text)
            # time.sleep(6666)
            detail = html.xpath('/html/body/ul/li')
            for li in detail:
                title = li.xpath('./a/@title')[0]
                url = 'http://ggzy.hefei.gov.cn' + li.xpath('./a/@href')[0]
                date_Today = li.xpath('./span/text()')[0][:10]
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
        url_html = etree.HTML(tool.requests_get(url, self.headers))
        try:
            detail = url_html.xpath('//*[@id="container"]/div[3]/div[2]/div[2]/div[2]/div[1]/div[2]/div[4]')[0]
            detail_html = etree.tostring(detail, method='HTML')
            detail_html = html.unescape(detail_html.decode())
            detail_text = url_html.xpath('string(//*[@id="container"]/div[3]/div[2]/div[2]/div[2]/div[1]/div[2]/div[4])').replace('\xa0', '').replace('\n', '').\
                replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
            if len(detail_html) < 200:
                int('a')
        except:
            try:
                detail = url_html.xpath('//*[@id="container"]/div[3]/div[2]/div[2]/div[2]/div[1]/div[2]')[0]
                detail_html = etree.tostring(detail, method='HTML')
                detail_html = html.unescape(detail_html.decode())
                detail_text = url_html.xpath(
                    'string(//*[@id="container"]/div[3]/div[2]/div[2]/div[2]/div[1]/div[2])').replace('\xa0',
                                                                                                             '').replace(
                    '\n', ''). \
                    replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
                if len(detail_html) < 200:
                    int('a')
            except:
                try:
                    detail = url_html.xpath('//*[@id="container"]/div[3]/div[2]/div[1]/div[1]')[0]
                    detail_html = etree.tostring(detail, method='HTML')
                    detail_html = html.unescape(detail_html.decode())
                    detail_text = url_html.xpath(
                        'string(//*[@id="container"]/div[3]/div[2]/div[1]/div[1])').replace('\xa0',
                                                                                                          '').replace(
                        '\n', ''). \
                        replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
                    if len(detail_html) < 200:
                        int('a')
                except:
                    detail = url_html.xpath('//*[@class="ewb-info-main news-article-para"]')[0]
                    detail_html = etree.tostring(detail, method='HTML')
                    detail_html = html.unescape(detail_html.decode())
                    detail_text = url_html.xpath(
                        'string(//*[@class="ewb-info-main news-article-para"])').replace('\xa0',
                                                                                            '').replace(
                        '\n', ''). \
                        replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
                    if len(detail_html) < 200:
                        int('a')
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
        item['resource'] = '合肥市公共资源交易中心'
        item['shi'] = 6501
        item['sheng'] = 6500
        item['removal']= title
        process_item(item)
    def get_nativeplace(self, addr):
        city = ''
        city_list = [['6501.001', '瑶海区'], ['6501.002', '庐阳区'], ['6501.003', '蜀山区'], ['6501.004', '包河区'], ['6501.005', '长丰县'], ['6501.006', '肥东县'], ['6501.007', '肥西县']]

        for i in city_list:
            if i[1] in addr:
                city = float(i[0])
                break
        if city == '':
            city = 6501
        return city

if __name__ == '__main__':
    import traceback, os
    try:
        jl = wenshan_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
        tool.send_error('报错文件：'+str(os.path.basename(__file__))+'报错信息：'+str(e))

