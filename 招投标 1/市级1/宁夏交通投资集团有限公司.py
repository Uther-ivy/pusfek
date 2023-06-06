# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item
# 宁夏交通投资集团有限公司
class xinyang_ggzy:
    def __init__(self):
        self.url_list = [
            'http://www.nxcig.com/module/web/jpage/dataproxy.jsp?page=1&webid=1&path=http://www.nxcig.com/&columnid=39&unitid=141&webname=%25E5%25AE%2581%25E5%25A4%258F%25E4%25BA%25A4%25E9%2580%259A%25E6%258A%2595%25E8%25B5%2584%25E9%259B%2586%25E5%259B%25A2%25E6%259C%2589%25E9%2599%2590%25E5%2585%25AC%25E5%258F%25B8&permissiontype=0',

        ]
        self.url = self.url_list.pop(0)
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        }

    def parse(self):
        date = tool.date
        # date = '2021-07-26'
        page = 0
        while True:
            page += 1
            text = tool.requests_get(self.url, self.headers)
            # html = HTML(text)
            print('*' * 20, page, '*' * 20)
            title_list = re.findall('title="(.*?)"\s*href=',text)
            url_list = re.findall('href="http://www.nxcig.com/art(.*?)">',text)
            print(url_list)
            date_list = re.findall('</a><span>(.*?)</span></li>',text)
            for title,url,date_Today in zip(title_list,url_list,date_list):
                # try:
                #     title = html.xpath('//table[@class="table_text"]//tr//a//@title')[li].replace('\xa0', '').replace(' ', '')
                #     url=str(html.xpath('//table[@class="table_text"]//tr//a//@href')[li]).replace("javascript:urlOpen('","").replace("')","").strip()
                #
                #     date_Today = html.xpath('//table[@class="table_text"]//tr//td[last()-1]//text()')[li].replace('月', '-').replace('日', '').replace('\n','').replace('\t', '').replace('年', '-').strip()
                #     if date_Today=='发布工具':
                #         date_Today = html.xpath('//table[@class="table_text"]//tr//td[last()]//text()')[li].replace('月', '-').replace('日', '').replace('\n', '').replace('\t', '').replace('年', '-').strip()
                #
                #     print(title,url,date_Today)
                # except:
                #     continue
                url='http://www.nxcig.com/art'+url
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
        t = tool.requests_get(url, self.headers)
        # print(t)
        url_html = etree.HTML(t)
        detail = url_html.xpath('//div[@id="zoom"]')[0]
        # print(detail)
        # print(detail)
        detail_html = etree.tostring(detail, method='HTML')
        detail_html = html.unescape(detail_html.decode())
        detail_text = url_html.xpath('string(//div[@id="zoom"])').replace('\xa0', '').replace('\n', ''). \
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
        item['resource'] = '宁夏交通投资集团有限公司'
        item["shi"] = int(float(item["nativeplace"]))
        item['sheng'] = 15500
        # print(item)
        item['removal']= title
        process_item(item)

    def get_nativeplace(self, addr):
        city = ''
        city_list = [['15501', '银川'], ['15501.001', '兴庆'], ['15501.002', '西夏'], ['15501.003', '金凤'], ['15501.004', '永宁'], ['15501.005', '贺兰'], ['15501.006', '灵武'], ['15502', '石嘴山'], ['15502.001', '大武口'], ['15502.002', '惠农'], ['15502.003', '平罗'], ['15503', '吴忠'], ['15503.001', '利通'], ['15503.002', '盐池'], ['15503.003', '同心'], ['15503.004', '青铜峡'], ['15503.005', '红寺堡'], ['15504', '固原'], ['15504.001', '原州'], ['15504.002', '西吉'], ['15504.003', '隆德'], ['15504.004', '泾源'], ['15504.005', '彭阳'], ['15505', '中卫'], ['15505.001', '沙坡头'], ['15505.002', '中宁']]

        for i in city_list:
            if i[1] in addr:
                city = float(i[0])
                break
        if city == '':
            city = 15500
        return city

if __name__ == '__main__':
    import traceback,os
    try:
        jl = xinyang_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
