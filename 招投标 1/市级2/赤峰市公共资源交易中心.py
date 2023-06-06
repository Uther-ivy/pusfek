# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 赤峰市公共资源交易中心
class wenshan_ggzy:
    def __init__(self):
        self.url_list = [
                    'http://ggzy.chifeng.gov.cn/EpointWeb_CF/jyxx_cf/003001/003001001/003001001001/?COLLCC=3495631849&',        #建设工程 招标公告
                    'http://ggzy.chifeng.gov.cn/EpointWeb_CF/jyxx_cf/003001/003001001/003001001002/?COLLCC=3495631849&',
                    'http://ggzy.chifeng.gov.cn/EpointWeb_CF/jyxx_cf/003001/003001001/003001001003/?COLLCC=3495631849&',
                    'http://ggzy.chifeng.gov.cn/EpointWeb_CF/jyxx_cf/003001/003001001/003001001004/?COLLCC=3495631849&',
                    'http://ggzy.chifeng.gov.cn/EpointWeb_CF/jyxx_cf/003001/003001001/003001001005/?COLLCC=3495631849&',
                    'http://ggzy.chifeng.gov.cn/EpointWeb_CF/jyxx_cf/003001/003001001/003001001006/?COLLCC=3495631849&',
                    'http://ggzy.chifeng.gov.cn/EpointWeb_CF/jyxx_cf/003001/003001003/003001003001/?COLLCC=3495631849&',        #中标公示
                    'http://ggzy.chifeng.gov.cn/EpointWeb_CF/jyxx_cf/003001/003001003/003001003002/?COLLCC=3495631849&',
                    'http://ggzy.chifeng.gov.cn/EpointWeb_CF/jyxx_cf/003001/003001003/003001003003/?COLLCC=3495631849&',
                    'http://ggzy.chifeng.gov.cn/EpointWeb_CF/jyxx_cf/003001/003001003/003001003004/?COLLCC=3495631849&',
                    'http://ggzy.chifeng.gov.cn/EpointWeb_CF/jyxx_cf/003001/003001003/003001003005/?COLLCC=3495631849&',
                    'http://ggzy.chifeng.gov.cn/EpointWeb_CF/jyxx_cf/003001/003001003/003001003006/?COLLCC=3495631849&',
                    'http://ggzy.chifeng.gov.cn/EpointWeb_CF/jyxx_cf/003001/003001005/003001005001/?COLLCC=3495631849&',        #结果公告
                    'http://ggzy.chifeng.gov.cn/EpointWeb_CF/jyxx_cf/003001/003001005/003001005002/?COLLCC=3495631849&',
                    'http://ggzy.chifeng.gov.cn/EpointWeb_CF/jyxx_cf/003001/003001005/003001005003/?COLLCC=3495631849&',
                    'http://ggzy.chifeng.gov.cn/EpointWeb_CF/jyxx_cf/003001/003001005/003001005004/?COLLCC=3495631849&',
                    'http://ggzy.chifeng.gov.cn/EpointWeb_CF/jyxx_cf/003001/003001005/003001005005/?COLLCC=3495631849&',
                    'http://ggzy.chifeng.gov.cn/EpointWeb_CF/jyxx_cf/003001/003001005/003001005006/?COLLCC=3495631849&',
                    'http://ggzy.chifeng.gov.cn/EpointWeb_CF/jyxx_cf/003001/003001006/003001006001/?COLLCC=3495631849&',         #开标结果
                    'http://ggzy.chifeng.gov.cn/EpointWeb_CF/jyxx_cf/003001/003001006/003001006002/?COLLCC=3495631849&',
                    'http://ggzy.chifeng.gov.cn/EpointWeb_CF/jyxx_cf/003001/003001006/003001006003/?COLLCC=3495631849&',
                    'http://ggzy.chifeng.gov.cn/EpointWeb_CF/jyxx_cf/003001/003001006/003001006004/?COLLCC=3495631849&',
                    'http://ggzy.chifeng.gov.cn/EpointWeb_CF/jyxx_cf/003001/003001006/003001006005/?COLLCC=3495631849&',
                    'http://ggzy.chifeng.gov.cn/EpointWeb_CF/jyxx_cf/003001/003001006/003001006006/?COLLCC=3495631849&'
                    ]
        self.url = self.url_list.pop(0)
        self.headers = {
            'Cookie': 'ASP.NET_SessionId=njryktrsd23lij35rymqqo0o',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        }

    def parse(self):
        date = tool.date
        # date = '2020-04-02'
        page = 0
        while True:
            page += 1
            print('*' * 20, page, '*' * 20, self.url)
            text = tool.requests_get(self.url, self.headers)
            detail = HTML(text).xpath('/html/body/div[2]/div/div[2]/div[2]/div/table/tr')
            for li in detail:
                try:
                    title = li.xpath('./td[2]/a/@title')[0]
                    url = 'http://ggzy.chifeng.gov.cn' + li.xpath('./td[2]/a/@href')[0]
                    date_Today = li.xpath('./td[3]/text()')[0].replace('[', '').replace(']', '')
                except:
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
                    self.url = self.url_list.pop(0)
                    page = 0
                    break
            if page == 20:
                self.url = self.url_list.pop(0)
                break
    def parse_detile(self, title, url, date):
        print(url)
        url_html = etree.HTML(tool.requests_get(url, self.headers))
        detail = url_html.xpath('//*[@id="contentA"]/table/tr/td/table/tr[3]/td/table/tr[3]/td/table')[0]
        detail_html = etree.tostring(detail, method='HTML')
        detail_html = html.unescape(detail_html.decode())
        detail_text = url_html.xpath('string(//*[@id="contentA"]/table/tr/td/table/tr[3]/td/table/tr[3]/td/table)').replace('\xa0', '').replace('\n', '').\
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
        item['resource'] = '赤峰市公共资源交易中心'
        item['shi'] = 3004
        item['sheng'] = 3000
        item['removal']= title
        process_item(item)
    def get_nativeplace(self, addr):
        city = ''
        city_list = [['3004.001', '红山区'], ['3004.01', '喀喇沁旗'], ['3004.011', '宁城县'], ['3004.012', '敖汉旗'], ['3004.002', '元宝山区'], ['3004.003', '松山区'], ['3004.004', '阿鲁科尔沁旗'], ['3004.005', '巴林左旗'], ['3004.006', '巴林右旗'], ['3004.007', '林西县'], ['3004.008', '克什克腾旗'], ['3004.009', '翁牛特旗']]

        for i in city_list:
            if i[1] in addr:
                city = float(i[0])
                break
        if city == '':
            city = 3004
        return city

if __name__ == '__main__':
    import os,traceback
    try:
        jl = wenshan_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
        tool.send_error('报错文件：'+str(os.path.basename(__file__))+'报错信息：'+str(e))



