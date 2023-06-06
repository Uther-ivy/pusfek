# -*- coding: utf-8 -*-
import json
import re
import time, html
import traceback
import scrapy

import base64
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 浙江招标投标网
class xinyang_ggzy:
    def __init__(self):
        self.url_list = ['001001001', '001001005', '001001009']
        self.url = self.url_list.pop(0)
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
            'Cookie': 'ASP.NET_SessionId=uqgwmy3kjyil0k45mz1h21vt'
        }

    def parse(self):
        date = tool.date
        # date = '2020-07-10'
        page = 0
        num = 1
        data = {
            '__VIEWSTATE': '',
            '__EVENTTARGET': 'MoreInfoListGG$Pager',
            '__EVENTARGUMENT': str(page)
        }
        while True:
            page += 1
            url_to = 'http://www.zjbid.cn/zjwz/template/default/GGInfo.aspx?CategoryNum={}'.format(self.url)
            if page == 1:
                text = requests.get(url_to, headers=self.headers).text
            else:
                text = tool.requests_post(url_to, data, self.headers)
            data['__VIEWSTATE'] = HTML(text).xpath('//*[@id="__VIEWSTATE"]/@value')[0]
            data['__EVENTARGUMENT'] = str(page)
            detail = HTML(text).xpath('//*[@id="MoreInfoListGG_tdcontent"]/table/tr')
            # print(text)
            # time.sleep(666)
            print('*' * 20, page, '*' * 20)
            for li in detail:
                title = li.xpath('./td[2]/a/@title')[0]
                date_Today = str(li.xpath('./td[3]/text()')[0]).strip().replace('[', '').replace(']', '')
                url = 'http://www.zjbid.cn' + li.xpath('./td[2]/a/@href')[0]
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
                    if num == 3:
                        self.url = self.url_list.pop(0)
                        page = 0
                        break
                    num += 1

                    break
            if page == 30:
                self.url = self.url_list.pop(0)
                break


    def parse_detile(self, title, url, date):
        print(url)
        t = tool.requests_get(url, self.headers)
        # print(t)
        # time.sleep(6666)
        url_html = etree.HTML(t)
        try:
            detail = url_html.xpath("//*[@id='tblInfo']")[0]
        except:
            return
        detail_html = etree.tostring(detail, method='HTML')
        detail_html = html.unescape(detail_html.decode()).replace('\xa0', '').replace('\ufeff', '')
        detail_text = url_html.xpath('string(//*[@id="tblInfo"])') \
            .replace('\xa0', '').replace('\n', '').replace('\r', '').replace('\t', '') \
            .replace(' ', '').replace('\xa5', '').replace('\ufeff', '')
        item = {}
        item['title'] = title.replace('\u2022', '')
        item['url'] = url
        item['date'] = date
        item['typeid'] = tool.get_typeid(item['title'])
        item['senddate'] = int(time.time())
        item['mid'] = 867
        item['infotype'] = tool.get_infotype(item['title'])
        item['body'] = tool.qudiao_width(detail_html)
        # b = re.findall('''<p class="news-article-info">.*?</p>''', item['body'])[0]
        # item['body'] = item['body'].replace(b, '')
        # print(item['body'])
        # time.sleep(666)
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
        item['resource'] = '浙江招标投标网'
        item["shi"] = int(str(item["nativeplace"]).split('.')[0])
        item['sheng'] = 6000
        item['removal']= title
        process_item(item)
        # print(item['body'])

    def get_nativeplace(self, addr):
        city = ''
        city_list = [['6001', '杭州'], ['6001.001', '上城'], ['6001.01', '淳安'], ['6001.011', '建德'], ['6001.012', '富阳'], ['6001.013', '临安'], ['6001.002', '下城'], ['6001.003', '江干'], ['6001.004', '拱墅'], ['6001.005', '西湖'], ['6001.006', '滨江'], ['6001.007', '萧山'], ['6001.008', '余杭'], ['6001.009', '桐庐'], ['6002', '宁波'], ['6002.001', '海曙'], ['6002.01', '慈溪'], ['6002.011', '奉化'], ['6002.002', '江东'], ['6002.003', '江北'], ['6002.004', '北仑'], ['6002.005', '镇海'], ['6002.006', '鄞州'], ['6002.007', '象山'], ['6002.008', '宁海'], ['6002.009', '余姚'], ['6003', '温州'], ['6003.001', '鹿城'], ['6003.01', '瑞安'], ['6003.011', '乐清'], ['6003.002', '龙湾'], ['6003.003', '瓯海'], ['6003.004', '洞头'], ['6003.005', '永嘉'], ['6003.006', '平阳'], ['6003.007', '苍南'], ['6003.008', '文成'], ['6003.009', '泰顺'], ['6004', '嘉兴'], ['6004.001', '秀城'], ['6004.002', '秀洲'], ['6004.003', '嘉善'], ['6004.004', '海盐'], ['6004.005', '海宁'], ['6004.006', '平湖'], ['6004.007', '桐乡'], ['6005', '湖州'], ['6005.001', '吴兴'], ['6005.002', '南浔'], ['6005.003', '德清'], ['6005.004', '长兴'], ['6005.005', '安吉'], ['6006', '绍兴'], ['6006.001', '越城'], ['6006.002', '绍兴'], ['6006.003', '新昌'], ['6006.004', '诸暨'], ['6006.005', '上虞'], ['6006.006', '嵊州'], ['6007', '金华'], ['6007.001', '婺城'], ['6007.002', '金东'], ['6007.003', '武义'], ['6007.004', '浦江'], ['6007.005', '磐安'], ['6007.006', '兰溪'], ['6007.007', '义乌'], ['6007.008', '东阳'], ['6007.009', '永康'], ['6008', '衢州'], ['6008.001', '柯城'], ['6008.002', '衢江'], ['6008.003', '常山'], ['6008.004', '开化'], ['6008.005', '龙游'], ['6008.006', '江山'], ['6009', '舟山'], ['6009.001', '定海'], ['6009.002', '普陀'], ['6009.003', '岱山'], ['6009.004', '嵊泗'], ['6010', '台州'], ['6010.001', '椒江'], ['6010.002', '黄岩'], ['6010.003', '路桥'], ['6010.004', '玉环'], ['6010.005', '三门'], ['6010.006', '天台'], ['6010.007', '仙居'], ['6010.008', '温岭'], ['6010.009', '临海'], ['6011', '丽水'], ['6011.001', '莲都'], ['6011.002', '青田'], ['6011.003', '缙云'], ['6011.004', '遂昌'], ['6011.005', '松阳'], ['6011.006', '云和'], ['6011.007', '庆元'], ['6011.008', '景宁畲族自治']]

        for i in city_list:
            if i[1] in addr:
                city = float(i[0])
                break
        if city == '':
            city = 6000
        return city

if __name__ == '__main__':
    jl = xinyang_ggzy()
    jl.parse()


