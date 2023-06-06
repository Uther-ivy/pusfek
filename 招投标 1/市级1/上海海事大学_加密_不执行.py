# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 上海海事大学
class baoshan_ggzy:
    def __init__(self):
        self.url_list = [
            'https://www.shmtu.edu.cn/zhaobiao',
            'https://www.shmtu.edu.cn/zhaobiao?field_zbgglx_tid=5',
            'https://www.shmtu.edu.cn/zhaobiao?field_zbgglx_tid=6',
            'https://www.shmtu.edu.cn/zhaobiao?field_zbgglx_tid=7',
            'https://www.shmtu.edu.cn/zhaobiao?field_zbgglx_tid=8',
        ]
        self.url = self.url_list.pop(0)
        self.headers = {
            # 'Cookie': 'homeid=1a444a31-e460-47ff-9931-1c075c0f3cd8',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        }

    def parse(self):
        while True:
            date = tool.date
            text = tool.requests_get(self.url,self.headers)
            html = HTML(text)
            detail = html.xpath('//div[@class="table-responsive"]//tbody//tr')
            for li in detail:
                url="https://www.shmtu.edu.cn"+li.xpath('./td[2]/a/@href')[0]
                title = li.xpath('./td[2]/a/text()').strip()
                date_Today = html.xpath(f'(//div[@class="table-responsive"]//tbody//tr//td[1])[{li+1}]//text()')[1].replace('年','-').replace('月','-').replace('日','').strip()
                if '发布' in date_Today:
                    continue
                if '测试' in title:
                    continue
                # print(title, url, date_Today)
                if tool.Transformation(date) <= tool.Transformation(date_Today):
                    if tool.removal(title, date):
                        self.parse_detile(title, url, date_Today)
                    else:
                        print('【existence】', url)
                        continue
                else:
                    print('日期不符, 正在切换类型', date_Today, self.url)
                    return

            self.url = self.url_list.pop(0)

    def parse_detile(self, title, url, date):
        t = tool.requests_get(url, self.headers)
        url_html = etree.HTML(t)
        detail = url_html.xpath('//div[@class="field-item even"]')[0]
        detail_html = etree.tostring(detail, method='HTML')
        detail_html = html.unescape(detail_html.decode())
        detail_text = url_html.xpath('string(//div[@class="field-item even"])').replace('\xa0', '').replace('\n', ''). \
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
        item['address'] = tool.get_address(detail_text)
        item['linkman'] = tool.get_linkman(detail_text)
        item['function'] = tool.get_function(detail_text)
        item['resource'] = '上海海事大学'
        if '.' in str(item["nativeplace"]):
            item["shi"] = int(float(str(item["nativeplace"]).replace("['","").split('.')[0]))
        else:
            item["shi"] = int(float(item["nativeplace"]))
        item['sheng'] = 5000
        # print(item)
        item['removal']= title
        process_item(item)

    def get_nativeplace(self, addr):
        city = ''
        city_list = [['5001', '黄浦区'], ['5002', '卢湾区'], ['5003', '徐汇区'], ['5004', '长宁区'], ['5005', '静安区'], ['5006', '普陀区'], ['5007', '闸北区'], ['5008', '虹口区'], ['5009', '杨浦区'], ['5010', '闵行区'], ['5011', '宝山区'], ['5012', '嘉定区'], ['5013', '浦东新区'], ['5014', '金山区'], ['5015', '松江区'], ['5016', '青浦区'], ['5017', '南汇区'], ['5018', '奉贤区'], ['5019', '崇明县']]

        for i in city_list:
            if i[1] in addr:
                city = float(i[0])
                break
        if city == '':
            city = 5000
        return city

if __name__ == '__main__':
    import traceback, os
    try:
        jl = baoshan_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
