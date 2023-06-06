# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 重庆高速公路集团有限公司招投标
class baoshan_ggzy:
    def __init__(self):
        self.url_list = [
            'http://www.cegc.com.cn/gw/newsInfoMenu.html?id=42&key=2',
        ]
        self.url = self.url_list.pop(0)
        self.headers = {
            # 'Cookie': 'homeid=1a444a31-e460-47ff-9931-1c075c0f3cd8',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        }

    def parse(self):
        while True:
            date = tool.date
            # date='2021-07-27'
            text = tool.requests_get(self.url,self.headers)
            html = HTML(text)
            detail = html.xpath('//*[@id="alltitle"]/li')
            for li in detail:
                url = 'http://www.cegc.com.cn/gw/findArticle.html?id='+ li.xpath('./a/@id')[0]
                title = li.xpath('./a/@name')[0].strip()

                date_Today = li.xpath('./span/text()')[0][:10].replace('(','').replace(')','').strip()
                if '发布' in date_Today:
                    continue
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
                    return

    def parse_detile(self, title, url, date):
        print(url)
        t = tool.requests_get(url, self.headers)
        url_html = etree.HTML(t)
        detail = url_html.xpath('//*[@class="cont-p"]')[0]
        detail_html = etree.tostring(detail, method='HTML')
        detail_html = html.unescape(detail_html.decode())
        detail_text = url_html.xpath('string(//*[@class="cont-p"])').replace('\xa0', '').replace('\n', ''). \
            replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
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
        item['nativeplace'] = self.get_nativeplace(title)
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
        item['resource'] = '重庆高速公路集团有限公司招投标'
        if '.' in str(item["nativeplace"]):
            item["shi"] = int(float(str(item["nativeplace"]).replace("['","").split('.')[0]))
        else:
            item["shi"] = int(float(item["nativeplace"]))
        item['sheng'] = 11500
        item['removal']= title
        process_item(item)

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
    import traceback, os
    try:
        jl = baoshan_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
