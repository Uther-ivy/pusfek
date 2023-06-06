# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 吉林省政府采购中心
class baoshan_ggzy:
    def __init__(self):
        self.url_list = [
            'http://www.ggzyzx.jl.gov.cn/jygg/zcjz/zbgg/{}.html',
            'http://www.ggzyzx.jl.gov.cn/jygg/zcjz/bggg/{}.html',
            'http://www.ggzyzx.jl.gov.cn/jygg/zcjz/zbjggg/{}.html',
            'http://www.ggzyzx.jl.gov.cn/jygg/zcjz/fbgg/{}.html',
            'http://www.ggzyzx.jl.gov.cn/jygg/zcfjz/cgzxzbgg/{}.html',
            'http://www.ggzyzx.jl.gov.cn/jygg/zcfjz/cgzxbggg/{}.html',
            'http://www.ggzyzx.jl.gov.cn/jygg/zcfjz/cgzxzbjggg/{}.html',
            'http://www.ggzyzx.jl.gov.cn/jygg/zcfjz/cgzxfbgg/{}.html',
            'http://www.ggzyzx.jl.gov.cn/jygg/cgzxgcjs/cgzxzbgg/{}.html',
            'http://www.ggzyzx.jl.gov.cn/jygg/cgzxgcjs/cgzxbggg/{}.html',
            'http://www.ggzyzx.jl.gov.cn/jygg/cgzxgcjs/zbgg/{}.html',
        ]
        self.url = self.url_list.pop(0)
        self.headers = {
            'Cookie': 'homeid=1a444a31-e460-47ff-9931-1c075c0f3cd8',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        }

    def parse(self):
        date = tool.date
        # date = '2020-12-11'
        page = 0
        while True:
            page += 1
            if page == 1:
                text = tool.requests_get(self.url.format('index'), self.headers).replace('result(', '').replace(');', '')
            else:
                text = tool.requests_get(self.url.format('index_' + str(page)), self.headers).replace('result(', '').replace(');', '')
            print('*' * 20, page, '*' * 20)
            html = HTML(text)
            # print(11, text)
            # time.sleep(6666)
            detail = html.xpath('//*[@class="content_r_main"]/ul')
            for ul in detail:
                for li in ul.xpath('./li'):
                    title = li.xpath('./a/text()')[0].replace('\n', '').replace('\r', '')\
                        .replace('\t', '').replace(' ', '')
                    url = li.xpath('./a/@href')[0]
                    if 'http' not in url:
                        url = '/'.join(self.url.split('/')[:-1]) + url[1:]
                    date_Today = li.xpath('./div/text()')[0].replace('\n', '').replace('\r', '')\
                        .replace('\t', '').replace(' ', '').replace('.', '-')
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
        detail = url_html.xpath('/html/body/div[3]/div/div/div[2]/div[2]/div[1]')[0]
        detail_html = etree.tostring(detail, method='HTML')
        detail_html = html.unescape(detail_html.decode())
        detail_text = url_html.xpath('string(/html/body/div[3]/div/div/div[2]/div[2]/div[1])').replace('\xa0', '').replace('\n', '').\
            replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
        if len(detail_html) < 500:
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
        item['resource'] = '吉林省政府采购中心'
        item['shi'] = int(item['nativeplace'])
        item['sheng'] = 4000
        item['removal']= title
        process_item(item)

    def get_nativeplace(self, addr):
        city = ''
        city_list = [['4001', '长春市'], ['4001.001', '南关区'], ['4001.01', '德惠市'], ['4001.002', '宽城区'], ['4001.003', '朝阳区'], ['4001.004', '二道区'], ['4001.005', '绿园区'], ['4001.006', '双阳区'], ['4001.007', '农安县'], ['4001.008', '九台市'], ['4001.009', '榆树市'], ['4002', '吉林市'], ['4002.001', '昌邑区'], ['4002.002', '龙潭区'], ['4002.003', '船营区'], ['4002.004', '丰满区'], ['4002.005', '永吉开发区'], ['4002.006', '蛟河市'], ['4002.007', '桦甸市'], ['4002.008', '舒兰市'], ['4002.009', '磐石市'], ['4002.010', '经开区'], ['4003', '四平市'], ['4003.001', '铁西区'], ['4003.002', '铁东区'], ['4003.003', '梨树县'], ['4003.004', '伊通满族自治县'], ['4003.005', '公主岭市'], ['4003.006', '双辽市'], ['4004', '辽源市'], ['4004.001', '龙山区'], ['4004.002', '西安区'], ['4004.003', '东丰县'], ['4004.004', '东辽县'], ['4005', '通化市'], ['4005.001', '东昌区'], ['4005.002', '二道江区'], ['4005.003', '通化县'], ['4005.004', '辉南县'], ['4005.005', '柳河县'], ['4005.006', '梅河口市'], ['4005.007', '集安市'], ['4006', '白山市'], ['4006.001', '八道江区'], ['4006.002', '抚松县'], ['4006.003', '靖宇县'], ['4006.004', '长白朝鲜族自治县'], ['4006.005', '江源县'], ['4006.006', '临江市'], ['4007', '松原市'], ['4007.001', '宁江区'], ['4007.002', '前郭尔罗斯蒙古族自治县'], ['4007.003', '长岭县'], ['4007.004', '乾安县'], ['4007.005', '扶余县'], ['4008', '白城市'], ['4008.001', '洮北区'], ['4008.002', '镇赉县'], ['4008.003', '通榆县'], ['4008.004', '洮南市'], ['4008.005', '大安市'], ['4009', '延边朝鲜族自治州'], ['4009.001', '延吉市'], ['4009.002', '图们市'], ['4009.003', '敦化市'], ['4009.004', '珲春市'], ['4009.005', '龙井市'], ['4009.006', '和龙市'], ['4009.007', '汪清县'], ['4009.008', '安图县']]

        for i in city_list:
            if i[1] in addr:
                city = float(i[0])
                break
        if city == '':
            city = 4000
        return city

if __name__ == '__main__':
    import traceback, os
    try:
        jl = baoshan_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
        tool.send_error('报错文件：'+str(os.path.basename(__file__))+'报错信息：'+str(e))


