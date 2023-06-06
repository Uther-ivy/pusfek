# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 张家界市公共资源交易平台
class zhangjiajie_ggzy:
    def __init__(self):
        self.url_list = [
            # 市本级
            #   工程建设
            #       招标公告
            'http://www.zjjsggzy.gov.cn/TenderProject/GetTpList?page={}&records=15&name=&category=%E6%88%BF%E5%BB%BA%'
            'E5%B8%82%E6%94%BF%2C%E6%B0%B4%E5%88%A9%2C%E4%BA%A4%E9%80%9A%E8%BF%90%E8%BE%93%2C%E5%9C%9F%E5%9C%B0%E5%BC%'
            '80%E5%8F%91%E6%95%B4%E7%90%86%2C%E5%85%B6%E4%BB%96%2C%E9%9D%9E%E6%94%BF%E5%BA%9C%E9%87%87%E8%B4%AD%2C%E5%8'
            'C%BB%E8%8D%AF%E9%87%87%E8%B4%AD&method=&publishbegintime=&publishendtime=&bpType=&IsShowOld=true',
            #       补充通知
            'http://www.zjjsggzy.gov.cn/tenderproject/GetClarificationNotice?page={}&records=15&name=&category=%E6%88%BF'
            '%E5%BB%BA%E5%B8%82%E6%94%BF%2C%E6%B0%B4%E5%88%A9%2C%E4%BA%A4%E9%80%9A%E8%BF%90%E8%BE%93%2C%E5%9C%9F%E5%9C%'
            'B0%E5%BC%80%E5%8F%91%E6%95%B4%E7%90%86%2C%E5%85%B6%E4%BB%96%2C%E9%9D%9E%E6%94%BF%E5%BA%9C%E9%87%87%E8%B4%'
            'AD%2C%E5%8C%BB%E8%8D%AF%E9%87%87%E8%B4%AD&method=&publishbegintime=&publishendtime=&bpType=&IsShowOld=true',
            #       中标候选人公示
            'http://www.zjjsggzy.gov.cn/TenderProject/GetBidderList?page={}&records=15&name=&category=%E6%88%BF%E5%BB%BA'
            '%E5%B8%82%E6%94%BF%2C%E6%B0%B4%E5%88%A9%2C%E4%BA%A4%E9%80%9A%E8%BF%90%E8%BE%93%2C%E5%9C%9F%E5%9C%B0%E5%BC'
            '%80%E5%8F%91%E6%95%B4%E7%90%86%2C%E5%85%B6%E4%BB%96%2C%E9%9D%9E%E6%94%BF%E5%BA%9C%E9%87%87%E8%B4%AD%2C%E5'
            '%8C%BB%E8%8D%AF%E9%87%87%E8%B4%AD&method=&publishbegintime=&publishendtime=&bpType=%E4%B8%AD%E6%A0%87%E5%'
            '85%AC%E7%A4%BA%2C%E4%B8%AD%E6%A0%87%E5%80%99%E9%80%89%E4%BA%BA%E5%85%AC%E7%A4%BA&IsShowOld=true',
            # 结果公示
            'http://www.zjjsggzy.gov.cn/TenderProject/GetBidderList?page={}&records=15&name=&category=%E6%88%BF%E5%BB'
            '%BA%E5%B8%82%E6%94%BF%2C%E6%B0%B4%E5%88%A9%2C%E4%BA%A4%E9%80%9A%E8%BF%90%E8%BE%93%2C%E5%9C%9F%E5%9C%B0%E5'
            '%BC%80%E5%8F%91%E6%95%B4%E7%90%86%2C%E5%85%B6%E4%BB%96%2C%E9%9D%9E%E6%94%BF%E5%BA%9C%E9%87%87%E8%B4%AD%2'
            'C%E5%8C%BB%E8%8D%AF%E9%87%87%E8%B4%AD&method=&publishbegintime=&publishendtime=&bpType=%E6%B5%81%E6%A0%'
            '87%E5%85%AC%E7%A4%BA%2C%E5%BA%9F%E6%A0%87%E5%85%AC%E7%A4%BA%2C%E4%B8%AD%E6%A0%87%E7%BB%93%E6%9E%9C%E5%85'
            '%AC%E7%A4%BA&IsShowOld=true',
            #   政府采购
            #       采购公告
            'http://www.zjjsggzy.gov.cn/TenderProject/GetTpList?page={}&records=15&name=&category=%E6%94%BF%E5%BA%9C%E9'
            '%87%87%E8%B4%AD&method=%E5%85%AC%E5%BC%80%E6%8B%9B%E6%A0%87&publishbegintime=&publishendtime=&bpType=&'
            'IsShowOld=true',
            # 补充公告
            'http://www.zjjsggzy.gov.cn/tenderproject/GetClarificationNotice?page={}&records=15&name=&category=%E6%94%B'
            'F%E5%BA%9C%E9%87%87%E8%B4%AD&method=%E5%85%AC%E5%BC%80%E6%8B%9B%E6%A0%87&publishbegintime=&publishendtim'
            'e=&bpType=&IsShowOld=true',
            #       结果公示
            'http://www.zjjsggzy.gov.cn/TenderProject/GetBidderList?page=1&records=15&name=&category=%E6%94%BF%E5%BA%9'
            'C%E9%87%87%E8%B4%AD&method=%E5%85%AC%E5%BC%80%E6%8B%9B%E6%A0%87&publishbegintime=&publishendtime=&bpType='
            '&IsShowOld=true'
        ]
        self.url = self.url_list.pop(0)
        self.headers = {
            # 'Cookie': 'HttpOnly; VISIT_UV=202004081515232746039586; HttpOnly; HttpOnly; HttpOnly; VISIT_UV=202004081515232746039586',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        }

    def parse(self):
        date = tool.date
        # date = '2020-04-08'
        page = 0
        while True:
            page += 1
            print('*' * 20, page, '*' * 20)
            text = tool.requests_get(self.url.format(page), self.headers)
            print(11, text)
            time.sleep(6666)
            detail = json.loads(text)['json']
            if 'tenderproject' in self.url:
                detail = json.loads(text)['json']['list']
            for i in detail:
                title = i['Title']
                if 'TpId' in i:
                    code = i['TpId']
                else:
                    code = i['id']
                try:
                    date_Today = str(i['time'])[:10]
                except:
                    date_Today = str(i['PublishTime'])[:10]
                if '测试' in title:
                    continue
                # print(title, url, date_Today, code)
                # time.sleep(666)
                if tool.Transformation(date) <= tool.Transformation(date_Today):
                    self.parse_detile(title, code, date)
                else:
                    print('日期不符, 正在切换类型', date_Today)
                    self.url = self.url_list.pop(0)
                    page = 0
                    break

            if page == 20:
                self.url = self.url_list.pop(0)
                break

    def parse_detile(self, title, code, date):
        url_list = [
            # 补充
            'http://www.zjjsggzy.gov.cn/supplenotice/GetInfosByTpId?tpId={}',
            # 招标
            'http://www.zjjsggzy.gov.cn/TenderFlow/GetTpInfo?tpId={}',
            # 中标结果
            'http://www.zjjsggzy.gov.cn/BidderPublic/GetInfosByTpId?tpId={}',
            # 中标候选人
            'http://www.zjjsggzy.gov.cn/BidderPublic/GetInfosByTpId?tpId={}&d=1586415860050&b'
            'pType=%E4%B8%AD%E6%A0%87%E5%80%99%E9%80%89%E4%BA%BA%E5%85%AC%E7%A4%BA%2C%E6%B5%81%E6%A0%87%E5%85%AC%E7%A'
            '4%BA%2C%E5%BA%9F%E6%A0%87%E5%85%AC%E7%A4%BA'
            ]
        for i in url_list:
            url = i.format(code)
            url_json = tool.requests_get(url, self.headers)
            json_text = json.loads(url_json)
            try:
                if len(json_text['json']) == 0:
                    continue
            except:
                continue
            print(url)
            title_list = []
            detail_list = []
            url_list_to = []
            if '招标内容' in json_text['json']:
                title_list.append(json_text['json']['招标标题'])
                detail_list.append(json_text['json']['招标内容'])
                url_list_to.append(i.format(json_text['json']['TdjId']))
            else:
                for j in json_text['json']:
                    if 'supplenotice' in url:
                        title_list.append(j['detail']['标题'])
                        try:
                            detail_list.append(j['detail']['修改文本'])
                        except:
                            print('时间不对')
                            continue
                        url_list_to.append(i.format(j['id']))
                    elif 'BidderPublic' in url:
                        title_list.append(j['detail']['公示标题'])
                        try:
                            detail_list.append(j['detail']['内容'])
                        except:
                            print('时间不对')
                            continue
                        url_list_to.append(i.format(j['id']))
            # print(title_list, url_list_to, detail_list)
            # time.sleep(6666)
            for o in range(len(url_list_to)):
                title = title_list[o]
                detail = detail_list[o]
                url = url_list_to[o]
                if tool.removal(title, date) is False:
                    print('【existence】', url)
                    continue
                detail_text = ''.join(re.findall('>(.*?)<', detail)).replace('\xa0', '').replace('\n', '').\
                    replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
                item = {}
                item['title'] = title.replace('\u2022', '')
                item['url'] = url
                item['date'] = date
                item['typeid'] = tool.get_typeid(item['title'])
                item['senddate'] = int(time.time())
                item['mid'] = 867
                item['nativeplace'] = self.get_nativeplace(item['title'])
                item['infotype'] = tool.get_infotype(item['title'])
                item['body'] = detail
                width_list = re.findall('width="(.*?)"', item["body"])
                for i in width_list:
                    item["body"] = item["body"].replace('width="{}"'.format(i), '')
                width_list = re.findall('WIDTH: (.*?)pt;', item["body"])
                for i in width_list:
                    item["body"] = item["body"].replace('WIDTH: {}pt;'.format(i), '')
                width_list = re.findall('width: (.*?)', item["body"])
                for i in width_list:
                    item["body"] = item["body"].replace('width: {}'.format(i), '')
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
                item['resource'] = '张家界市公共资源交易平台'
                item['shi'] = 9508
                item['sheng'] = 9500
                item['removal']= title
        process_item(item)

    def get_nativeplace(self, addr):
        city = ''
        city_list = [['9508.001', '永定区'], ['9508.002', '武陵源区'], ['9508.003', '慈利县'], ['9508.004', '桑植县']]
        for i in city_list:
            if i[1] in addr:
                city = float(i[0])
                break
        if city == '':
            city = 9508
        return city

if __name__ == '__main__':
    jl = zhangjiajie_ggzy()
    jl.parse()


