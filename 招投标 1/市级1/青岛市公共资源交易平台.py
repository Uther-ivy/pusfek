# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 青岛市公共资源交易平台
class qingdao_ggzy:
    def __init__(self):
        self.url_list = [
            # 市本级
            #   工程建设
            #       招标公告
            'https://ggzy.qingdao.gov.cn/Tradeinfo-GGGSList/0-0-0?pageIndex={}',
            #       预中标
            'https://ggzy.qingdao.gov.cn/Tradeinfo-GGGSList/0-0-2?pageIndex={}',
            #       废标公告
            'https://ggzy.qingdao.gov.cn/Tradeinfo-GGGSList/0-0-3?pageIndex={}',
            #       中标公告
            'https://ggzy.qingdao.gov.cn/Tradeinfo-GGGSList/0-0-8?pageIndex={}',
            #   政府采购
            #       采购公告
            'https://ggzy.qingdao.gov.cn/Tradeinfo-GGGSList/1-1-0?pageIndex={}',
            #       变更公告
            'https://ggzy.qingdao.gov.cn/Tradeinfo-GGGSList/1-1-5?pageIndex={}',
            #       中标公告
            'https://ggzy.qingdao.gov.cn/Tradeinfo-GGGSList/1-1-2?pageIndex={}',
            #       废标公告
            'https://ggzy.qingdao.gov.cn/Tradeinfo-GGGSList/1-1-3?pageIndex={}'
        ]
        self.url = self.url_list.pop(0)
        self.headers = {
            'Cookie': 'ASP.NET_SessionId=sgciv2y0q2cmcycy1o5nsnep; _gscu_381646434=86586121w36f2x70; _gscbrs_381646434=1; _gscs_381646434=t86591829gen3ym70|pv:8',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        }

    def parse(self):
        date = tool.date
        # date = '2020-04-10'
        page = 0
        while True:
            page += 1
            text = tool.requests_get(self.url.format(page), self.headers)
            print('*' * 20, page, '*' * 20)
            detail = HTML(text).xpath('//*[@class="info_con"]/table/tr')
            for li in detail:
                title = li.xpath('./td[1]/a/@title')[0]
                url = 'https://ggzy.qingdao.gov.cn' + li.xpath('./td[1]/a/@href')[0]
                date_Today = li.xpath('./td[2]/text()')[0].replace('\n', '').replace('\r', '') \
                    .replace('\t', '').replace(' ', '').replace('[', '').replace(']', '')
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
                    print(self.url)
                    page = 0
                    break
            if page == 20:
                self.url = self.url_list.pop(0)
                break
    def parse_detile(self, title, url, date):
        print(url)
        url_html = HTML(tool.requests_get(url, self.headers))
        detail = url_html.xpath('//*[@id="htmlTable"]')[0]
        detail_html = etree.tostring(detail, method='HTML')
        detail_html = html.unescape(detail_html.decode()).replace('\xa0', '')
        detail_text = url_html.xpath('string(//*[@id="htmlTable"])').replace('\xa0', '').replace(
            '\n', ''). \
            replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
        # print(detail_text.replace('\xa0','').replace('\xa5',''))
        # time.sleep(6666)
        if len(detail_text) < 100:
            return ''
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
        item['resource'] = '青岛市公共资源交易网'
        item['shi'] = 8002
        item['sheng'] = 8000
        item['removal']= title
        process_item(item)

    def get_nativeplace(self, addr):
        city = ''
        city_list = [['8002.001', '市南区'], ['8002.01', '平度市'], ['8002.011', '胶南市'], ['8002.012', '莱西市'], ['8002.002', '市北区'], ['8002.003', '四方区'], ['8002.004', '黄岛区'], ['8002.005', '崂山区'], ['8002.006', '李沧区'], ['8002.007', '城阳区'], ['8002.008', '胶州市'], ['8002.009', '即墨市']]
        for i in city_list:
            if i[1] in addr:
                city = float(i[0])
                break
        if city == '':
            city = 8002
        return city

if __name__ == '__main__':

    import traceback, os
    try:
        jl = qingdao_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
        tool.send_error('报错文件：'+str(os.path.basename(__file__))+'报错信息：'+str(e))


