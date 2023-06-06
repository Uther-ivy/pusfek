# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 杭州市公共资源网
class xinyang_ggzy:
    def __init__(self):
        self.url_list = ['22', '465', '25', '28', '27', '29', '32', '34', '499', '37']
        self.url = self.url_list.pop(0)
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36"
                        }

    def parse(self):
        date = tool.date
        # date = '2020-07-10'
        page = 0
        data = {
            'area': '',
            'afficheType': '',
            'IsToday': '',
            'title': '',
            'proID': '',
            'number': '',
            '_search': 'false',
            'nd': '1573459629871',
            'rows': '10',
            'page': '1',
            'sidx': 'PublishStartTime',
            'sord': 'desc'
        }
        url_to = 'https://ggzy.hzctc.hangzhou.gov.cn/SecondPage/GetNotice'
        while True:
            page += 1
            data['afficheType'] = self.url
            data['page'] = str(page)
            text = tool.requests_post(url_to, data, self.headers)
            print(text)
            detail = json.loads(text)['rows']
            print('*' * 20, page, '*' * 20)
            for tr in detail:
                if self.url == '486':
                    url = "https://ggzy.hzctc.hangzhou.gov.cn/OpenBidRecord/Index?id={}&tenderID={}&ModuleID={}".format(tr['ID'], tr[
                        'TenderID'], self.url)
                    title = tr['TenderName']
                    date_Today = tr['PublishStartTime'][:10]
                elif self.url == '465':
                    url = "https://ggzy.hzctc.hangzhou.gov.cn/NewsShow/Home?id={}&ModuleID={}&AreadID=80".format(tr['id'], self.url)
                    title = tr['title']
                    date_Today = tr['news_entertime'][:10]
                else:
                    url = "https://ggzy.hzctc.hangzhou.gov.cn/AfficheShow/Home?AfficheID={}&IsInner=3&ModuleID={}".format(tr['ID'],
                                                                                                            self.url)
                    title = tr['TenderName']
                    date_Today = tr['PublishStartTime'][:10]
                print(title, url, date_Today)
                # time.sleep(666)
                if '测试' in title or '答疑' in title:
                    continue
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
            if page == 30:
                self.url = self.url_list.pop(0)
                page = 0

    def parse_detile(self, title, url, date):
        print(url)
        url_html = etree.HTML(tool.requests_get(url, self.headers))
        try:
            detail = url_html.xpath('/html/body/div[3]/div[2]/div[2]')[0]
            detail_html = etree.tostring(detail, method='HTML')
            detail_html = html.unescape(detail_html.decode()).replace('\xa0', '').replace('\ufeff', '')
            detail_text = url_html.xpath('string(/html/body/div[3]/div[2]/div[2])') \
                .replace('\xa0', '').replace('\n', '').replace('\r', '').replace('\t', '') \
                .replace(' ', '').replace('\xa5', '').replace('\ufeff', '')
        except:
            try:
                detail = url_html.xpath('//*[@class="WordSection1"]')[0]
                detail_html = etree.tostring(detail, method='HTML')
                detail_html = html.unescape(detail_html.decode()).replace('\xa0', '').replace('\ufeff', '')
                detail_text = url_html.xpath('string(//*[@class="WordSection1"])') \
                    .replace('\xa0', '').replace('\n', '').replace('\r', '').replace('\t', '') \
                    .replace(' ', '').replace('\xa5', '').replace('\ufeff', '')
            except:
                try:
                    detail = url_html.xpath('//*[@class="Section0"]')[0]
                    detail_html = etree.tostring(detail, method='HTML')
                    detail_html = html.unescape(detail_html.decode()).replace('\xa0', '').replace('\ufeff', '')
                    detail_text = url_html.xpath('string(//*[@class="Section0"])') \
                        .replace('\xa0', '').replace('\n', '').replace('\r', '').replace('\t', '') \
                        .replace(' ', '').replace('\xa5', '').replace('\ufeff', '')
                except:
                    try:
                        detail = url_html.xpath('//*[@class="MainList"]')[0]
                        detail_html = etree.tostring(detail, method='HTML')
                        detail_html = html.unescape(detail_html.decode()).replace('\xa0', '').replace('\ufeff', '')
                        detail_text = url_html.xpath('string(//*[@class="Section0"])') \
                            .replace('\xa0', '').replace('\n', '').replace('\r', '').replace('\t', '') \
                            .replace(' ', '').replace('\xa5', '').replace('\ufeff', '')
                    except:
                        data = {
                            'openID': re.findall('id=(.*?)&tenderID=', url)[0],
                            'tenderID': re.findall('&tenderID=(.*?)&ModuleID', url)[0]
                        }
                        url_html = etree.HTML(tool.requests_post('https://ggzy.hzctc.hangzhou.gov.cn/OpenBidRecord/main_reflesh', data, self.headers))
                        detail = url_html.xpath('//*[@id="Table1"]')[0]
                        detail_html = etree.tostring(detail, method='HTML')
                        detail_html = html.unescape(detail_html.decode()).replace('\xa0', '').replace('\ufeff', '')
                        detail_text = url_html.xpath('string(//*[@id="Table1"])') \
                            .replace('\xa0', '').replace('\n', '').replace('\r', '').replace('\t', '') \
                            .replace(' ', '').replace('\xa5', '').replace('\ufeff', '')
        # print(detail_text)
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
        item['resource'] = '杭州市公共资源网'
        item["shi"] = 6001
        item['sheng'] = 6000
        item['removal']= title
        process_item(item)
        # print(item['body'])

    def get_nativeplace(self, addr):
        city = ''
        city_list = [['6001', '杭州'], ['6001.001', '上城'], ['6001.01', '淳安'], ['6001.011', '建德'], ['6001.012', '富阳'], ['6001.013', '临安'], ['6001.002', '下城'], ['6001.003', '江干'], ['6001.004', '拱墅'], ['6001.005', '西湖'], ['6001.006', '滨江'], ['6001.007', '萧山'], ['6001.008', '余杭']]

        for i in city_list:
            if i[1] in addr:
                city = float(i[0])
                break
        if city == '':
            city = 6001
        return city

if __name__ == '__main__':
    import traceback,os
    try:
        jl = xinyang_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
        tool.send_error('报错文件：'+str(os.path.basename(__file__))+'报错信息：'+str(e))


