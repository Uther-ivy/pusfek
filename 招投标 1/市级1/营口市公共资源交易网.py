# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 营口市公共资源交易网
class yingkou_ggzy:
    def __init__(self):
        self.url_code = [
            # 建设工程
            'http://ccgp.yingkou.gov.cn/Html/NewsList.asp?SortID=98&SortPath=0,98,&Page={}'
        ]
        self.url = self.url_code.pop(0)
        self.headers = {
            'Cookie': 'ASPSESSIONIDQABDRBRQ=DENFLCAAJKBPGHJCIBHGFEEF; safedog-flow-item=6CB76529A3E03DC0C471FB51B14848D9',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
        }

    def parse(self):
        date = tool.date
        # date = '2020-01-10'
        page = 0
        while True:
            page += 1
            text = tool.requests_get(self.url.format(page), self.headers).replace("<td width='680'", "<tr><td width='680'")
            html = HTML(text)
            detail = html.xpath('//*[@class="page_r_mid_v"]/table/tr[2]/td[2]/table/tr')
            for li in detail[:-1]:
                title = li.xpath('./td[1]/a/@title')[0]
                url = 'http://ccgp.yingkou.gov.cn/Html/' + li.xpath('./td[1]/a/@href')[0]
                date_Today = li.xpath('./td[2]/text()')[0]
                # print(11, title, url, date_Today)
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
        url_html = etree.HTML(tool.requests_get(url, self.headers))
        detail = url_html.xpath('/html/body/div[1]/div[2]/div/div/div[2]/div[2]/div')[0]
        detail_html = etree.tostring(detail, method='HTML')
        detail_html = html.unescape(detail_html.decode())
        detail_text = url_html.xpath('string(/html/body/div[1]/div[2]/div/div/div[2]/div[2]/div)').replace('\xa0', '').replace('\n', '').\
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
        item['body']=re.sub('<div class="page_r_mid_v">[\s\S]*?<td>&nbsp;</td>',"",item['body'])
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
        item['resource'] = '营口市公共资源交易网'
        item['shi'] = 3508
        item['sheng'] = 3500
        item['removal']= title
        process_item(item)

    def get_nativeplace(self, addr):
        city = ''
        city_list = [['3508.001', '站前区'], ['3508.002', '西市区'], ['3508.003', '鲅鱼圈区'], ['3508.004', '老边区'], ['3508.005', '盖州市'], ['3508.006', '大石桥市']]
        for i in city_list:
            if i[1] in addr:
                city = float(i[0])
                break
        if city == '':
            city = 3508
        return city
if __name__ == '__main__':
    import traceback, os
    try:
        jl = yingkou_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
        tool.send_error('报错文件：'+str(os.path.basename(__file__))+'报错信息：'+str(e))


