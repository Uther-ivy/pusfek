# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 重庆市政府采购网
class xinyang_ggzy:
    def __init__(self):
        self.url_list = [
            'https://www.ccgp-chongqing.gov.cn/gwebsite/api/v1/notices/stable/new?__platDomain__=www.ccgp-chongqing.gov.cn&endDate={}&pi={}&ps=20&startDate={}'
        ]
        self.url = self.url_list.pop(0)
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36",
        }

    def parse(self):
        date = tool.Time_stamp_to_date(tool.Transformation(tool.date) + 86400*3)
        date_str = tool.Time_stamp_to_date(tool.Transformation(tool.date) - 86400*7)
        page = 0
        while True:
            page += 1
            text = tool.requests_g(self.url.format(date, page, date_str), self.headers)
            detail = json.loads(text)['notices']
            print('*' * 20, page, '*' * 20)
            for li in detail:
                id = li["id"]
                date_Today = li["issueTime"][:10]
                url = "https://www.ccgp-chongqing.gov.cn/gwebsite/api/v1/notices/stable/{}".format(id)
                title = li['title']
                # print(title, url, date_Today)
                # time.sleep(666)
                if '测试' in title:
                    continue
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

            if page == 30:
                self.url = self.url_list.pop(0)
                break

    def parse_detile(self, title, url, date):
        print(url)
        url_html = json.loads(tool.requests_g(url, self.headers))
        detail_html = url_html['notice']['html']
        detail_text = ''.join(re.findall('>(.*?)<', detail_html)) \
            .replace('\xa0', '').replace('\n', '').replace('\r', '').replace('\t', '') \
            .replace(' ', '').replace('\xa5', '').replace('\ufeff', '')
        # print(detail_text)
        # time.sleep(6666)
        item = {}
        item['title'] = title.replace('\u2022', '')
        item['url'] = url
        item['date'] = date
        item['typeid'] = tool.get_typeid(item['title'])
        item['senddate'] = int(time.time())
        item['mid'] = 867
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
        item['nativeplace'] = self.get_nativeplace(item['title'])
        item['linkman'] = tool.get_linkman(detail_text)
        item['function'] = tool.get_function(detail_text)
        item['resource'] = '重庆市政府采购网'
        item["shi"] = int(str(item["nativeplace"]).split('.')[0])
        item['sheng'] = 11500
        item['removal']= title
        process_item(item)
        # print(item['body'])

    def get_nativeplace(self, addr):
        city = ''
        city_list = [['11501', '万州'], ['11502', '涪陵'], ['11503', '渝中'], ['11504', '大渡口'], ['11505', '江北'], ['11506', '沙坪坝'], ['11507', '九龙坡'], ['11508', '南岸'], ['11509', '北碚'], ['11510', '万盛'], ['11511', '双桥'], ['11512', '渝北'], ['11513', '巴南'], ['11514', '黔江'], ['11515', '长寿'], ['11516', '綦江'], ['11517', '潼南'], ['11518', '铜梁'], ['11519', '大足'], ['11520', '荣昌'], ['11521', '璧山'], ['11522', '梁平'], ['11523', '城口'], ['11524', '丰都'], ['11525', '垫江'], ['11526', '武隆'], ['11527', '忠'], ['11528', '开'], ['11529', '云阳'], ['11530', '奉节'], ['11531', '巫山'], ['11532', '巫溪'], ['11533', '石柱土家族自治'], ['11534', '秀山土家族苗族自治'], ['11535', '酉阳土家族苗族自治'], ['11536', '彭水苗族土家族自治'], ['11537', '江津'], ['11538', '合川'], ['11539', '永川']]

        for i in city_list:
            if i[1] in addr:
                city = float(i[0])
                break
        if city == '':
            city = 11500
        return city

if __name__ == '__main__':
    jl = xinyang_ggzy()
    jl.parse()


