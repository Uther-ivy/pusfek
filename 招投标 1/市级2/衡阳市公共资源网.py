# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 衡阳市公共资源交易平台
class hengyang_ggzy:
    def __init__(self):
        self.url_list = [
            # 市本级
            #   工程建设
            #       招标公告
            'http://ggzy.hengyang.gov.cn/jyxx/jsgcjy/zbgg/{}.html',
            #       其他公告
            'http://ggzy.hengyang.gov.cn/jyxx/jsgcjy/qtgg/{}.html',
            #       中标候选人公示
            'http://ggzy.hengyang.gov.cn/jyxx/jsgcjy/zbhxrgs/{}.html',
            #   政府采购
            #       采购公告
            'http://ggzy.hengyang.gov.cn/jyxx/zfcgjy/zbgg/{}.html',
            #       其他公告
            'http://ggzy.hengyang.gov.cn/jyxx/zfcgjy/qtgg/{}.html',
            #       结果公示
            'http://ggzy.hengyang.gov.cn/jyxx/zfcgjy/jggs/{}.html'
        ]
        self.url = self.url_list.pop(0)
        self.headers = {
            'Cookie': 'HttpOnly; VISIT_UV=202004081515232746039586; HttpOnly; HttpOnly; HttpOnly; VISIT_UV=202004081515232746039586',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        }

    def parse(self):
        date = tool.date
        # date = '2021-07-27'
        page = 0
        while True:
            page += 1
            if page == 1:
                text = tool.requests_get(self.url.format('index'), self.headers)
            else:
                text = tool.requests_get(self.url.format('pages/'+ str(page)), self.headers)
            print('*' * 20, page, '*' * 20)
            html = HTML(text)
            # print(11, text)
            # time.sleep(6666)
            detail = html.xpath('/html/body/div[2]/div/div/div[2]/div[3]/ul/li')
            for li in detail:
                title = li.xpath('./a/text()')[0]
                url = li.xpath('./a/@href')[0]
                date_Today = li.xpath('./span/text()')[0]
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
        detail = url_html.xpath('/html/body/div[2]/div/div[2]/div[2]')[0]
        detail_html = etree.tostring(detail, method='HTML')
        detail_html = html.unescape(detail_html.decode())
        detail_text = url_html.xpath('string(/html/body/div[2]/div/div[2]/div[2])').replace('\xa0', '').replace('\n', '').\
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
        width_list = re.findall('width: (.*?)', item["body"])
        for i in width_list:
            item["body"] = item["body"].replace('width: {}'.format(i), '')
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
        item['resource'] = '衡阳市公共资源交易平台'
        item['shi'] = 9504
        item['sheng'] = 9500
        item['removal']= title
        process_item(item)

    def get_nativeplace(self, addr):
        city = ''
        city_list = [['9504.001', '珠晖区'], ['9504.01', '祁东县'], ['9504.011', '耒阳市'], ['9504.012', '常宁市'], ['9504.002', '雁峰区'], ['9504.003', '石鼓区'], ['9504.004', '蒸湘区'], ['9504.005', '南岳区'], ['9504.006', '衡阳县'], ['9504.007', '衡南县'], ['9504.008', '衡山县'], ['9504.009', '衡东县']]
        for i in city_list:
            if i[1] in addr:
                city = float(i[0])
                break
        if city == '':
            city = 9504
        return city

if __name__ == '__main__':
    import traceback, os
    try:
        jl = hengyang_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
        tool.send_error('报错文件：'+str(os.path.basename(__file__))+'报错信息：'+str(e))



