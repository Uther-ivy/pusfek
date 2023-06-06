# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 淮安市政府采购网
class baoshan_ggzy:
    def __init__(self):
        self.url_list = [
            'http://zfcgzx.huaian.gov.cn/col/7654_848212/list.html',
            'http://zfcgzx.huaian.gov.cn/col/17151_277885/list.html',
            'http://zfcgzx.huaian.gov.cn/col/17152_581125/list.html',
            'http://zfcgzx.huaian.gov.cn/col/17153_281535/list.html',
            'http://zfcgzx.huaian.gov.cn/col/17154_627865/list.html',
            'http://zfcgzx.huaian.gov.cn/col/17155_311183/list.html',
            'http://zfcgzx.huaian.gov.cn/col/17156_564768/list.html',
            'http://zfcgzx.huaian.gov.cn/col/17157_543355/list.html',
            'http://zfcgzx.huaian.gov.cn/col/7646_415211/list.html',
            'http://zfcgzx.huaian.gov.cn/col/17087_758155/list.html',
            'http://zfcgzx.huaian.gov.cn/col/17088_713786/list.html',
            'http://zfcgzx.huaian.gov.cn/col/17089_262412/list.html',
            'http://zfcgzx.huaian.gov.cn/col/17090_464532/list.html',
            'http://zfcgzx.huaian.gov.cn/col/17091_783853/list.html',
            'http://zfcgzx.huaian.gov.cn/col/17092_144688/list.html',
            'http://zfcgzx.huaian.gov.cn/col/17093_184578/list.html',
            'http://zfcgzx.huaian.gov.cn/col/7648_343742/list.html',
            'http://zfcgzx.huaian.gov.cn/col/17103_353228/list.html',
            'http://zfcgzx.huaian.gov.cn/col/17104_182424/list.html',
            'http://zfcgzx.huaian.gov.cn/col/17105_561732/list.html',
            'http://zfcgzx.huaian.gov.cn/col/17106_814714/list.html',
            'http://zfcgzx.huaian.gov.cn/col/17107_582661/list.html',
            'http://zfcgzx.huaian.gov.cn/col/17108_467778/list.html',
            'http://zfcgzx.huaian.gov.cn/col/17109_387863/list.html',
            'http://zfcgzx.huaian.gov.cn/zbcg/cggg/column7/list.html',
            'http://zfcgzx.huaian.gov.cn/col/7651_843614/list.html',
            'http://zfcgzx.huaian.gov.cn/col/17127_241613/list.html',
            'http://zfcgzx.huaian.gov.cn/col/17128_443644/list.html',
            'http://zfcgzx.huaian.gov.cn/col/17129_218728/list.html',
            'http://zfcgzx.huaian.gov.cn/col/17130_346846/list.html',
            'http://zfcgzx.huaian.gov.cn/col/17131_156461/list.html',
            'http://zfcgzx.huaian.gov.cn/col/17132_631725/list.html',
            'http://zfcgzx.huaian.gov.cn/col/17133_418251/list.html',
            'http://zfcgzx.huaian.gov.cn/col/7652_848872/list.html',
            'http://zfcgzx.huaian.gov.cn/col/17135_173775/list.html',
            'http://zfcgzx.huaian.gov.cn/col/17136_421323/list.html',
            'http://zfcgzx.huaian.gov.cn/col/17137_583375/list.html',
            'http://zfcgzx.huaian.gov.cn/col/17138_554738/list.html',
            'http://zfcgzx.huaian.gov.cn/col/17139_162856/list.html',
            'http://zfcgzx.huaian.gov.cn/col/17140_641487/list.html',
            'http://zfcgzx.huaian.gov.cn/col/17141_284284/list.html',
            'http://zfcgzx.huaian.gov.cn/zbcg/cggg/column10/list.html',
            'http://zfcgzx.huaian.gov.cn/zbcg/cggg/column12/list.html',
            'http://zfcgzx.huaian.gov.cn/zbcg/cggg/column13/list.html',
        ]
        self.url = self.url_list.pop(0)
        self.headers = {
            # 'Cookie': 'homeid=1a444a31-e460-47ff-9931-1c075c0f3cd8',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        }

    def parse(self):
        while True:
            date = tool.date
            # date='2021-03-31'
            text = tool.requests_get(url=self.url, headers=self.headers)
            html = HTML(text)
            detail = html.xpath("//div[@class='list-lb']//li")
            for li in range(len(detail)):
                url = html.xpath(f'(//div[@class="list-lb"]//li//a//@href)[{li+1}]')[0]
                title = html.xpath(f'(//div[@class="list-lb"]//li//a//text())[{li+1}]')[0]
                date_Today = html.xpath(f'(//div[@class="list-lb"]//li//span//text())[{li+1}]')[0]
                if '测试' in title:
                    continue
                url_domain = 'http://zfcgzx.huaian.gov.cn'
                if 'http' not in url:
                    if '../../' in url:
                        url = url_domain + url[5:]
                    elif '../' in url:
                        url = url_domain + url[2:]
                    elif './' in url:
                        url = url_domain + url[1:]
                    else:
                        url = url_domain + url
                # print(title, url, date_Today)
                # # time.sleep(666)
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


    def parse_detile(self, title, url, date):
        t = tool.requests_get(url, self.headers)
        url_html = etree.HTML(t)
        detail = url_html.xpath('//div[@class="nr-zw"]')[0]
        # print(detail)
        detail_html = etree.tostring(detail, method='HTML')
        detail_html = html.unescape(detail_html.decode())
        detail_text = url_html.xpath('string(//div[@class="nr-zw"]//p)').replace('\xa0', '').replace('\n', ''). \
            replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
        # if len(detail_text) < 100:
        #     return
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
        item['address'] = tool.get_address(detail_text)
        item['linkman'] = tool.get_linkman(detail_text)
        item['function'] = tool.get_function(detail_text)
        item['resource'] = '淮安市政府采购网'
        item["shi"] = 5508
        item['sheng'] = 5500
        # print(item)
        item['removal']= title
        process_item(item)

    def get_nativeplace(self, addr):
        city = ''
        city_list = [['5508.001', '清河区'], ['5508.002', '楚州区'], ['5508.003', '淮阴区'], ['5508.004', '清浦区'], ['5508.005', '涟水县'], ['5508.006', '洪泽县'], ['5508.007', '盱眙县'], ['5508.008', '金湖县']]

        for i in city_list:
            if i[1] in addr:
                city = float(i[0])
                break
        if city == '':
            city = 5508
        return city

if __name__ == '__main__':

    import traceback, os
    try:
        jl = baoshan_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
