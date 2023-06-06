# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 长春市公共资源交易网
class changchun_ggzy:
    def __init__(self):
        self.url_code = [
            # 政府采购
                # 采购公告
            'http://www.ccggzy.com.cn/ccggzy/getxxgkAction.action?cmd=getCityZfcgInfo&pageIndex={}&pageSize=16&siteGuid=7eb5f7f1-9041-43ad-8e13-8fcb82ea831a&categorynum=002001&xiaqucode=220101&jyfl=%E5%85%A8%E9%83%A8',
                # 更正公告
            'http://www.ccggzy.com.cn/ccggzy/getxxgkAction.action?cmd=getCityZfcgInfo&pageIndex={}&pageSize=16&siteGuid=7eb5f7f1-9041-43ad-8e13-8fcb82ea831a&categorynum=002001003&xiaqucode=220101&jyfl=%E5%85%A8%E9%83%A8',
                # 中标公告
            'http://www.ccggzy.com.cn/ccggzy/getxxgkAction.action?cmd=getCityZfcgInfo&pageIndex={}&pageSize=16&siteGuid='
            '7eb5f7f1-9041-43ad-8e13-8fcb82ea831a&categorynum=002001004&xiaqucode=220101&jyfl=%E5%85%A8%E9%83%A8',
            # 工程建设
                # 招标公告
            'http://www.ccggzy.com.cn/ccggzy/getxxgkAction.action?cmd=getCityTradeInfo&categorynum=002002001&xiaqucode=220101&pageSize=18&pageIndex={}&siteguid=7eb5f7f1-9041-43ad-8e13-8fcb82ea831a',
                # 中标候选人
            'http://www.ccggzy.com.cn/ccggzy/getxxgkAction.action?cmd=getCityTradeInfo&categorynum=002002002&xiaqucode=220101&pageSize=18&pageIndex={}&siteguid=7eb5f7f1-9041-43ad-8e13-8fcb82ea831a',
            'http://www.ccggzy.com.cn/ccggzy/getxxgkAction.action?cmd=getCityTradeInfo&categorynum=002002003&xiaqucode=220101&pageSize=18&pageIndex={}&siteguid=7eb5f7f1-9041-43ad-8e13-8fcb82ea831a',
                # 中标结果
            'http://www.ccggzy.com.cn/ccggzy/getxxgkAction.action?cmd=getCityTradeInfo&categorynum=002002004&xiaqucode=220101&pageSize=18&pageIndex={}&siteguid=7eb5f7f1-9041-43ad-8e13-8fcb82ea831a'
        ]
        self.url = self.url_code.pop(0)
        self.headers = {
            'Cookie': 'JSESSIONID=630881DD9E28250A99DD0C4D2AA24365; UM_distinctid=16fa86dbd022fc-0c1b10c8f91237-e3'
                      '43166-1fa400-16fa86dbd0544e; CNZZDATA1253551100=435007633-1579073534-http%253A%252F%252Fwww.cc'
                      'ggzy.gov.cn%252F%7C1579073534',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75'
                          '.0.3770.100 Safari/537.36'
        }
    def parse(self):
        date = tool.date
        # date = '2020-01-10'
        page = 0
        while True:
            page += 1
            text = tool.requests_get(self.url.format(page), self.headers)
            detail = json.loads(json.loads(text)['custom'])['Table']
            for li in detail:
                title = li['title']
                url = 'http://www.ccggzy.com.cn' + li['href']
                date_Today = li['infodate']
                # print(title, url, date_Today)
                # time.sleep(666)
                if tool.Transformation(date) <= tool.Transformation(date_Today):
                    if tool.removal(title, date):
                        self.parse_detile(title, url, date_Today)
                    else:
                        print('【existence】', url)
                        continue
                else:
                    print('日期不符, 正在切换类型...', date_Today)
                    self.url = self.url_code.pop(0)
                    page = 0
                    break


    def parse_detile(self, title, url, date):
        print(url)
        t = tool.requests_get(url,self.headers)
        # print(t)
        # time.sleep(2222)
        url_html = etree.HTML(t)
        try:
            detail = url_html.xpath('//*[@id="print"]')[0]
            detail_html = etree.tostring(detail, method='HTML')
            detail_html = html.unescape(detail_html.decode())
            detail_text = url_html.xpath('string(//*[@id="print"])').replace('\xa0', '').replace('\n', ''). \
                replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
        except:
            try:
                detail = url_html.xpath('//*[@class="ewb-text-content ewb-row"]')[0]
                detail_html = etree.tostring(detail, method='HTML')
                detail_html = html.unescape(detail_html.decode())
                detail_text = url_html.xpath('string(//*[@class="ewb-text-content ewb-row"])').replace('\xa0', '').replace('\n', ''). \
                    replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
            except:
                return
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
        item['resource'] = '长春市公共资源交易网'
        item['shi'] = 4001
        item['sheng'] = 4000
        # print(item)
        item['removal']= title
        process_item(item)

    def get_nativeplace(self, addr):
        city = ''
        city_list = [['4001.001', '南关区'], ['4001.01', '德惠市'], ['4001.002', '宽城区'], ['4001.003', '朝阳区'], ['4001.004', '二道区'], ['4001.005', '绿园区'], ['4001.006', '双阳区'], ['4001.007', '农安县'], ['4001.008', '九台市'], ['4001.009', '榆树市']]
        for i in city_list:
            if i[1] in addr:
                city = float(i[0])
                break
        if city == '':
            city = 4001
        return city
if __name__ == '__main__':
    import traceback, os
    try:
        jl = changchun_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
        tool.send_error('报错文件：'+str(os.path.basename(__file__))+'报错信息：'+str(e))


