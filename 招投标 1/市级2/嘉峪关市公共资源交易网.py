# -*- coding: utf-8 -*-
import json
import re
import time, html, base64
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 嘉峪关市公共资源交易网
class baoshan_ggzy:
    def __init__(self):
        self.url_list = [
            'http://www.jygzyjy.gov.cn/f/newtrade/tenderannquainqueryanns/getListByProjectType?projectType=A',
            'http://www.jygzyjy.gov.cn/f/newtrade/tenderannquainqueryanns/getListByProjectType?projectType=D'
                         ]
        self.url = self.url_list.pop(0)
        self.headers = {
            'Cookie': 'homeid=1a444a31-e460-47ff-9931-1c075c0f3cd8',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        }

    def parse(self):
        date = tool.date
        # date = '2021-07-23'
        page = 0
        while True:
            page += 1
            text = tool.requests_get(self.url, self.headers)
            print('*' * 20, page, '*' * 20)
            html = HTML(text)
            # print(11, text)
            # time.sleep(6666)
            # http://www.jygzyjy.gov.cn/f/newtrade/tenderprojects/NTA1Nw==/flowpage?annogoodsId=NDYxMA==&pageIndex=MQ==
            detail = html.xpath('//a')
            for li in detail:
                title = li.xpath('./div/p/text()')[0].replace('\n', '').replace('\r', '')\
                    .replace('\t', '').replace(' ', '').replace('<spanstyle="color:red">', '').replace('</span>', '')
                url = li.xpath('./@onclick')[0].replace('loadTender(', '').replace(')', '').replace("'", '').split(',')
                if 'http' not in url:
                    # 提取出来的code 先经过base64加密 在转成utf-8
                    url = 'http://www.jygzyjy.gov.cn/f/newtrade/tenderprojects/{}/flowpage?annogoodsId={}&pageIndex=MQ=='\
                        .format(str(base64.b64encode(url[0].encode('utf-8')), 'utf8'), str(base64.b64encode(url[1].encode('utf-8')), 'utf8'))
                date_Today = li.xpath('./div/span/text()')[0].replace('\n', '').replace('\r', '') \
                    .replace('\t', '').replace(' ', '').replace('(', '').replace(')', '')
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
                    break
            self.url = self.url_list.pop(0)
            if page ==10:
                break

    def parse_detile(self, title, url, date):
        print(url)
        url_html = etree.HTML(tool.requests_get(url, self.headers))
        detail = url_html.xpath('//a[@class="pdf"]/@href')[0]
        detail_html = '<embed width="100%" height="100%" src="{}">'.format(detail)
        # 内容为PDF
        detail_text = ''
        # print(detail_html.replace('\xa0','').replace('\xa5',''))
        # time.sleep(6666)
        item = {}
        item['title'] = title.replace('\u2022', '')
        item['url'] = url
        item['date'] = date
        item['typeid'] = tool.get_typeid(item['title'])
        item['senddate'] = int(time.time())
        item['mid'] = 867
        item['nativeplace'] = 14502
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
        item['resource'] = '嘉峪关市公共资源交易网'
        item['shi'] = 14502
        item['sheng'] = 14500
        item['removal']= title
        process_item(item)

if __name__ == '__main__':
    import traceback,os
    try:
        jl = baoshan_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
        tool.send_error('报错文件：'+str(os.path.basename(__file__))+'报错信息：'+str(e))


