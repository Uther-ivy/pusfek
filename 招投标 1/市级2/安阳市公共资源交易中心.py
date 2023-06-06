# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 安阳市公共资源交易中心
class baoshan_ggzy:
    def __init__(self):
        self.url_list = [
            'http://ggzy.anyang.gov.cn/ayggfwpt-home-api/jyxx/jsgcZbgg?_t=1640570286&currentPage={}&pageSize=10&secondArea=001',
            'http://ggzy.anyang.gov.cn/ayggfwpt-home-api/jyxx/jsgcBgtz?_t=1640570713&currentPage={}&pageSize=10&secondArea=001',
            'http://ggzy.anyang.gov.cn/ayggfwpt-home-api/jyxx/jsgcPbjg?_t=1640570785&currentPage={}&pageSize=10&secondArea=001',
            'http://ggzy.anyang.gov.cn/ayggfwpt-home-api/jyxx/jsgcZbjggs?_t=1640570805&currentPage={}&pageSize=10&secondArea=001',
            'http://ggzy.anyang.gov.cn/ayggfwpt-home-api/jyxx/zfcg/cggg?_t=1640570833&currentPage={}&pageSize=10&secondArea=001',
            'http://ggzy.anyang.gov.cn/ayggfwpt-home-api/jyxx/zfcg/gzsx?_t=1640570862&currentPage={}&pageSize=10&secondArea=001',
            'http://ggzy.anyang.gov.cn/ayggfwpt-home-api/jyxx/zfcg/zbjggs?_t=1640570942&currentPage={}&pageSize=10&secondArea=001',

        ]
        self.url = self.url_list.pop(0)
        self.headers = {
            # 'Cookie': 'homeid=1a444a31-e460-47ff-9931-1c075c0f3cd8',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        }

    def parse(self):
        page = 0
        while True:
            page+=1
            date = tool.date
            # date='2021-12-20'
            print('-'*50, page)
            text = tool.requests_get(self.url.format(page),self.headers)
            detail = json.loads(text)['data']['rows']
            for li in detail:
                if 'jsgcZbgg' in self.url:
                    url = "http://ggzy.anyang.gov.cn/#/tradeInfoDetail?guid={}&apiName=gcjsDetail&type=0".format(
                        li['tenderBulletinGuid'])
                    title = li['bulletinName'].strip()
                    date_Today = li['bulletinIssueTime']
                elif 'jsgcBgtz' in self.url:
                    url = "http://ggzy.anyang.gov.cn/#/tradeInfoDetail?guid={}&apiName=gcjsDetail&type=1".format(
                        li['guid'])
                    title = li['changeTitle'].strip()
                    date_Today = li['fabuTime']
                elif 'jsgcPbjg' in self.url:
                    url = "http://ggzy.anyang.gov.cn/#/tradeInfoDetail?guid={}&apiName=gcjsDetail&type=2".format(
                        li['winBidBulletinGuid'])
                    title = li['bulletinName'].strip()
                    date_Today = li['bulletinIssueTime']
                elif 'jsgcZbjggs' in self.url:
                    url = "http://ggzy.anyang.gov.cn/#/tradeInfoDetail?guid={}&apiName=gcjsDetail&type=3".format(
                        li['winBidBulletinGuid'])
                    title = li['bulletinName'].strip()
                    date_Today = li['bulletinIssueTime']

                elif 'zfcg/cggg' in self.url:
                    url = "http://ggzy.anyang.gov.cn/#/tradeInfoDetail?guid={}&apiName=zfcgDetail&type=1".format(
                        li['guid'])
                    title = li['bulletinTitle'].strip()
                    date_Today = li['bulletinStartTime']
                elif 'zfcg/gzsx' in self.url:
                    url = "http://ggzy.anyang.gov.cn/#/tradeInfoDetail?guid={}&apiName=zfcgDetail&type=2".format(
                        li['guid'])
                    title = li['terminationBulletinTitle'].strip()
                    date_Today = li['modificationStartTime']
                else:
                    url = "http://ggzy.anyang.gov.cn/#/tradeInfoDetail?guid={}&apiName=zfcgDetail&type=3".format(
                        li['guid'])
                    title = li['winBidBulletinTitle'].strip()
                    date_Today = li['winBidBulletinStartTime']
                if '发布' in date_Today:
                    continue
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
                    self.url = self.url_list.pop(0)
                    page = 0
                    break
            if page==20:
                self.url = self.url_list.pop(0)
                page = 0

    def parse_detile(self, title, url, date):
        print(url)
        code = re.findall('guid=(.*?)&apiName', url)[0]
        c = url.split('type=')[1]
        if 'zfcg' in self.url:
            xq_url = 'http://ggzy.anyang.gov.cn/ayggfwpt-home-api/jyxx/zfcg/zfcgDetail?_t=1640572947&isOther=false&junk={}&guid={}'.format(c, code)
        else:
            xq_url = 'http://ggzy.anyang.gov.cn/ayggfwpt-home-api/jyxx/gcjsDetail?_t=1640573096&isOther=false&junk={}&guid={}'.format(c, code)
        xq_text = tool.requests_get(xq_url, self.headers)
        try:
            detail_html = json.loads(xq_text)['data']['tender']['bulletinContent']
        except:
            detail_html = json.loads(xq_text)['data']['winBid']['winBidBulletinContent']
        detail_text = ''.join(re.findall('>(.*?)<', detail_html, re.S)).replace('\xa0', '').replace('\n', ''). \
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
        item['resource'] = '安阳市公共资源交易中心'
        item["shi"] = 8505
        item['sheng'] = 8500
        # print(item)
        item['removal']= title
        process_item(item)

    def get_nativeplace(self, addr):
        city = ''
        city_list = [['8505.001', '文峰区'], ['8505.002', '北关区'], ['8505.003', '殷都区'], ['8505.004', '龙安区'], ['8505.005', '安阳县'], ['8505.006', '汤阴县'], ['8505.007', '滑县'], ['8505.008', '内黄县'], ['8505.009', '林州市']]

        for i in city_list:
            if i[1] in addr:
                city = float(i[0])
                break
        if city == '':
            city = 8505
        return city

if __name__ == '__main__':

    import traceback, os
    try:
        jl = baoshan_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
