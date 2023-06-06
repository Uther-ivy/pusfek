# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
import tool
from save_database import process_item

# 乌海市公告资源交易中心
class wuhai_ggzy:
    def __init__(self):
        self.url_code = [
            # 招标公告
            # 'ZcyAnnouncement11',
            # 招标变更
            # 'ZcyAnnouncement12',
            # 单一来源
            # 'ZcyAnnouncement13',
            # 中标公告
            'ZcyAnnouncement14',
            # 'ZcyAnnouncement8031',
            # 'ZcyAnnouncement8032',
            # 'ZcyAnnouncement8033',
        ]
        self.code = self.url_code.pop(0)
        self.headers = {
            'Cookie': 'acw_tc=76b20ff515784467744165116e4c58ec75e56b05eabee53aef9aa6ae8d3485; _zcy_log_client_uuid=df2cfad0-31b5-11ea-8228-0161e58e2c92; _dg_playback.bbc15f7dfd2de351.46db=1; _dg_abtestInfo.bbc15f7dfd2de351.46db=1; _dg_check.bbc15f7dfd2de351.46db=-1; _dg_id.bbc15f7dfd2de351.46db=2c1470fe4a04f1fe%7C%7C%7C1578446780%7C%7C%7C5%7C%7C%7C1578447295%7C%7C%7C1578447295%7C%7C%7C%7C%7C%7C049bf02c06a5348b%7C%7C%7C%7C%7C%7C%7C%7C%7C1%7C%7C%7Cundefined',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
        }

    def parse(self):
        date = tool.date
        # date = '2021-07-26'
        page = 550
        while True:
            page += 1
            # data = '{"utm":"sites_group_front.2ef5001f.0.0.df31198031b511ea82280161e58e2c92","categoryCode":'+self.code+',"pageSize":15,"pageNo":'+str(page)+'}'
            data = {
                'categoryCode': self.code,
                'pageNo': str(page),
                'pageSize': '15',
                'utm': "sites_group_front.2ef5001f.0.0.df31198031b511ea82280161e58e2c92"
            }
            url = 'http://www.whggzy.com/front/search/category'
            print('*' * 20, page, '*' * 20)
            text = tool.requests_post_to(url, data, self.headers)
            # print(111, text)
            # time.sleep(666)
            detail = json.loads(text)['hits']['hits']
            for i in detail:
                try:
                    title = i['_source']['title']
                    url = 'http://www.whggzy.com' + i['_source']['url']
                    date_Today = tool.Time_stamp_to_date(int(str(i['_source']['publishDate'])[:-3]))
                    # print(title, url, date_Today)
                    # time.sleep(666)
                    if tool.Transformation(date) <= tool.Transformation(date_Today):
                        # if tool.removal(title, date):
                            self.parse_detile(title, url, date_Today)
                        # else:
                        #     print('【existence】', url)
                        #     continue
                    else:
                        print('日期不符, 正在切换类型...', date_Today)

                except Exception as e:
                    traceback.print_exc()


    def parse_detile(self, title, url, date):
        print(url)
        url_text = json.loads(etree.HTML(tool.requests_get(url, self.headers)).xpath('//input[@name="articleDetail"]/@value')[0])['content']
        url_html = etree.HTML(url_text)
        # print(url_text)
        # time.sleep(6666)
        detail_text = url_html.xpath('string(.)').replace('\xa0', '').replace('\n', '').replace('\r', '').replace('\t',
                                                                                                                  '').replace(
            ' ', '').replace('\xa5', '')
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
        item['body'] = url_text
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
        item['winner'] = tool.get_winner(detail_text)
        item['address'] = tool.get_address(detail_text)
        item['linkman'] = tool.get_linkman(detail_text)
        item['function'] = tool.get_function(detail_text)
        item['resource'] = '乌海市公共资源交易中心'
        item['shi'] = 3012
        item['sheng'] = 3000
        item['removal']= title
        process_item(item)

    def get_nativeplace(self, addr):
        city = ''
        city_list = [['3003.001', '海勃湾区'], ['3003.002', '海南区'], ['3003.003', '乌达区']]

        for i in city_list:
            if i[1] in addr:
                city = float(i[0])
                break
        if city == '':
            city = 3003
        return city


if __name__ == '__main__':
    import traceback, os
    try:
        jl = wuhai_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
