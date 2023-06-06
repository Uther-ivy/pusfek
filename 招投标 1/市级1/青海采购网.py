# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 青海采购网
class baoshan_ggzy:
    def __init__(self):
        self.url = 'http://www.ccgp-qinghai.gov.cn/front/search/category'

        self.data_list=[
            {"pageNo": 1, "pageSize": 30, "categoryCode": "ZcyAnnouncement11", "utm": "sites_group_front.51ecbdd.0.0.5f90dc709e5511ebafccab935e1ed893"},
            {"pageNo":1,"pageSize":30,"categoryCode":"ZcyAnnouncement1","utm":"sites_group_front.26a79a93.0.0.333a3e809e6611eb9dedc598238d70a8"},
            {"pageNo":1,"pageSize":30,"categoryCode":"ZcyAnnouncement2","utm":"sites_group_front.26a79a93.0.0.333a3e809e6611eb9dedc598238d70a8"},
            {"pageNo":1,"pageSize":30,"categoryCode":"ZcyAnnouncement4","utm":"sites_group_front.26a79a93.0.0.333a3e809e6611eb9dedc598238d70a8"},
            {"pageNo":1,"pageSize":30,"categoryCode":"ZcyAnnouncement3","utm":"sites_group_front.26a79a93.0.0.333a3e809e6611eb9dedc598238d70a8"},
            {"pageNo":1,"pageSize":30,"categoryCode":"ZcyAnnouncement9999","utm":"sites_group_front.26a79a93.0.0.333a3e809e6611eb9dedc598238d70a8"},
            {"pageNo": 1, "pageSize": 30, "categoryCode": "ZcyAnnouncement8888","utm": "sites_group_front.26a79a93.0.0.333a3e809e6611eb9dedc598238d70a8"},
            {"pageNo": 1, "pageSize": 30, "categoryCode": "ZcyAnnouncement5","utm": "sites_group_front.26a79a93.0.0.333a3e809e6611eb9dedc598238d70a8"},
            {"pageNo": 1, "pageSize": 30, "categoryCode": "ZcyAnnouncement8","utm": "sites_group_front.26a79a93.0.0.333a3e809e6611eb9dedc598238d70a8"}
        ]
        self.data = self.data_list.pop(0)
        self.headers = {
            # 'Cookie': 'homeid=1a444a31-e460-47ff-9931-1c075c0f3cd8',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        }

    def parse(self):

            date = tool.date
            # date='2021-04-13'
            text = tool.requests_post_to(url=self.url,data=self.data,headers=self.headers)
            # print(text)
            # html = HTML(text)
            detail = json.loads(text)['hits']['hits']

            # print(de)
            for li in detail:
                # print(html.xpath('(//table[@id="dataTable"]//tr//@id)[1]'))
                url = li['_source']['url']
                title = li['_source']['title']
                #
                date_Today = int(li['_source']['publishDate']/1000)
                # print(li+1,url,title,date_Today)
                # if '发布' in date_Today:
                #     continue
                # month=re.findall('(\d*)-\d*-\d*',date_Today)
                # day=re.findall('\d*-(\d*)-\d*',date_Today)
                # print(month,day)
                if '测试' in title:
                    continue
                # urls=re.findall("(.*?)\(\'(.*?)\'\)",url)[0]
                url="http://www.ccgp-qinghai.gov.cn"+url
                print(title, url, date_Today)
                if tool.Transformation(date) >= tool.Transformation(tool.Time_stamp_to_date(date_Today)):
                    if tool.removal(title, date):
                        self.parse_detile(title, url, tool.Time_stamp_to_date(date_Today))
                    else:
                        print('【existence】', url)
                        continue
                else:
                    # print(tool.Transformation(date),self.Transformation(date_Today))
                    print('日期不符, 正在切换类型', date_Today, self.url)
                    return


    def parse_detile(self, title, url, date):
        t = tool.requests_get(url, self.headers)
        url_html = etree.HTML(t)
        detail = json.loads(url_html.xpath('//input[@name="articleDetail"]//@value')[0])['content']
        detail=etree.HTML(detail)
        detail=detail.xpath('//div[@id="template-center-mark"]')[0]
        # print(detail)
        # print(detail)
        detail_html = etree.tostring(detail, method='HTML')
        detail_html = html.unescape(detail_html.decode())
        detail_text = url_html.xpath('string(//div[@id="template-center-mark"])').replace('\xa0', '').replace('\n', ''). \
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
        item['resource'] = '青海采购网'
        if '.' in str(item["nativeplace"]):
            item["shi"] = int(float(str(item["nativeplace"]).replace("['","").split('.')[0]))
        else:
            item["shi"] = int(float(item["nativeplace"]))
        item['sheng'] = 15000
        # print(item)
        item['removal']= title
        process_item(item)

    def get_nativeplace(self, addr):
        city = ''
        city_list = [['15001', '西宁'], ['15001.001', '城东'], ['15001.002', '城中'], ['15001.003', '城西'], ['15001.004', '城北'], ['15001.005', '大通回族土族自治'], ['15001.006', '湟中'], ['15001.007', '湟源'], ['15002', '海东地'], ['15002.001', '平安'], ['15002.002', '民和回族土族自治'], ['15002.003', '乐都'], ['15002.004', '互助土族自治'], ['15002.005', '化隆回族自治'], ['15002.006', '循化撒拉族自治'], ['15003', '海北藏族自治州'], ['15003.001', '门源回族自治'], ['15003.002', '祁连'], ['15003.003', '海晏'], ['15003.004', '刚察'], ['15004', '黄南藏族自治州'], ['15004.001', '同仁'], ['15004.002', '尖扎'], ['15004.003', '泽库'], ['15004.004', '河南蒙古族自治'], ['15005', '海南藏族自治州'], ['15005.001', '共和'], ['15005.002', '同德'], ['15005.003', '贵德'], ['15005.004', '兴海'], ['15005.005', '贵南'], ['15006', '果洛藏族自治州'], ['15006.001', '玛沁'], ['15006.002', '班玛'], ['15006.003', '甘德'], ['15006.004', '达日'], ['15006.005', '久治'], ['15006.006', '玛多'], ['15007', '玉树藏族自治州'], ['15007.001', '玉树'], ['15007.002', '杂多'], ['15007.003', '称多'], ['15007.004', '治多'], ['15007.005', '囊谦'], ['15007.006', '曲麻莱'], ['15008', '海西蒙古族藏族自治州'], ['15008.001', '格尔木'], ['15008.002', '德令哈'], ['15008.003', '乌兰'], ['15008.004', '都兰']]

        for i in city_list:
            if i[1] in addr:
                city = float(i[0])
                break
        if city == '':
            city = 15000
        return city

if __name__ == '__main__':

    import traceback, os
    try:
        jl = baoshan_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
