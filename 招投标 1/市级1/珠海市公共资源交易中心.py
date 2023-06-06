# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 珠海市公共资源交易中心
class wenshan_ggzy:
    def __init__(self):
        self.url_list = [
            'http://ggzy.zhuhai.gov.cn/exchangeinfo/govbuy/cggg/index_{}.jhtml',
            'http://ggzy.zhuhai.gov.cn/exchangeinfo/govbuy/zcjggs/index_{}.jhtml',
            'http://ggzy.zhuhai.gov.cn/exchangeinfo/govbuy/zcjggg/index_{}.jhtml',
            'http://ggzy.zhuhai.gov.cn/exchangeinfo/govbuy/gzgg/index_{}.jhtml',
            'http://ggzy.zhuhai.gov.cn/exchangeinfo/jsgc/zbgg/index_{}.jhtml',
            'http://ggzy.zhuhai.gov.cn/exchangeinfo/jsgc/zbwjdy/index_{}.jhtml',
            'http://ggzy.zhuhai.gov.cn/exchangeinfo/jsgc/kbjggg/index_{}.jhtml',
            'http://ggzy.zhuhai.gov.cn/exchangeinfo/jsgc/zgscjggs/index_{}.jhtml',
            'http://ggzy.zhuhai.gov.cn/exchangeinfo/jsgc/pbjggs/index_{}.jhtml',
            'http://ggzy.zhuhai.gov.cn/exchangeinfo/jsgc/zbgs/index_{}.jhtml',
            'http://ggzy.zhuhai.gov.cn/exchangeinfo/jsgc/zbjj/index_{}.jhtml',
            'http://ggzy.zhuhai.gov.cn/exchangeinfo/jsgc/xmyq/index_{}.jhtml',
            'http://ggzy.zhuhai.gov.cn/exchangeinfo/jsgc/JSGCZBSBGG/index_{}.jhtml',
            'http://ggzy.zhuhai.gov.cn/exchangeinfo/jsgc/xmtz/index_{}.jhtml',
            'http://ggzy.zhuhai.gov.cn/exchangeinfo/jsgc/zbzz/index_{}.jhtml',
            ]
        self.url = self.url_list.pop(0)
        self.headers = {
            'Cookie': 'homeid=1a444a31-e460-47ff-9931-1c075c0f3cd8',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        }

    def parse(self):
        date = tool.date
        # date = '2020-04-02'
        page = 0
        while True:
            page += 1
            text = tool.requests_get(self.url.format(page), self.headers)
            print('*' * 20, page, '*' * 20)
            html = HTML(text)
            detail = html.xpath('//*[@class="rl-box-right"]/ul/li')
            for li in detail:
                title = li.xpath('./a/@title')[0]
                url = li.xpath('./a/@href')[0]
                try:
                    date_Today = li.xpath('./a/span/text()')[0]
                except:
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
                    print('日期不符, 正在切换类型', date_Today, self.url)
                    return

    def parse_detile(self, title, url, date):
        print(url)
        url_html = etree.HTML(tool.requests_get(url, self.headers))
        try:
            detail = url_html.xpath('//*[@class="newsCon"]')[0]
            detail_html = etree.tostring(detail, method='HTML')
            detail_html = html.unescape(detail_html.decode())
            detail_text = url_html.xpath('string(//*[@class="newsCon"])').replace('\xa0', '').replace('\n', '').\
                replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
        except:
            try:
                detail = url_html.xpath('/html/body/div[4]/div[2]/div/div[4]')[0]
                detail_html = etree.tostring(detail, method='HTML')
                detail_html = html.unescape(detail_html.decode())
                detail_text = url_html.xpath('string(/html/body/div[4]/div[2]/div/div[4])').replace(
                    '\xa0', '').replace('\n', ''). \
                    replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
            except:
                try:
                    detail = url_html.xpath('/html/body/div[4]/div[2]/div/div[3]')[0]
                    detail_html = etree.tostring(detail, method='HTML')
                    detail_html = html.unescape(detail_html.decode())
                    detail_text = url_html.xpath('string(/html/body/div[4]/div[2]/div/div[3])').replace(
                        '\xa0', '').replace('\n', ''). \
                        replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
                except:
                    detail = url_html.xpath('/html/body/div[5]/div[2]/div[1]/div[4]/div/div/div[3]')[0]
                    detail_html = etree.tostring(detail, method='HTML')
                    detail_html = html.unescape(detail_html.decode())
                    detail_text = url_html.xpath('string(/html/body/div[5]/div[2]/div[1]/div[4]/div/div/div[3])').replace(
                        '\xa0', '').replace('\n', ''). \
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
        item['winner'] = tool.get_winner(detail_text)
        item['address'] = tool.get_address(detail_text)
        item['linkman'] = tool.get_linkman(detail_text)
        item['function'] = tool.get_function(detail_text)
        item['resource'] = '珠海市公共资源交易中心'
        item['shi'] = 10004
        item['sheng'] = 10000
        item['removal']= title
        process_item(item)
    def get_nativeplace(self, addr):
        city = ''
        city_list = [['10004.001', '洲区'], ['10004.002', '斗门区'], ['10004.003', '金湾区']]

        for i in city_list:
            if i[1] in addr:
                city = float(i[0])
                break
        if city == '':
            city = 10004
        return city

if __name__ == '__main__':
    import os,traceback
    try:
        jl = wenshan_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
        tool.send_error('报错文件：'+str(os.path.basename(__file__))+'报错信息：'+str(e))



