# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item
import json
# 中国石化物资招标投标网
class xinyang_ggzy:
    def __init__(self):
        self.url_list = [
            'https://bidding.sinopec.com/tpfront/CommonPages/searchmore.aspx?CategoryNum=004005',
        ]
        self.url = self.url_list.pop(0)
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
            'Cookie': 'tpfront=4788ee85d9fd8926ef48c20bb8dc4c43; ASP.NET_SessionId=2mo45khehzh2y2jgbn1fqtlz; BIGipServerPOOL_DZZBTB_234_80=3547920650.20480.0000; __CSRFCOOKIE=46671b1e-8828-4fbb-aa03-6d0898d33d91'
        }

    def parse(self):
        date = tool.date
        # date = '2020-07-10'
        page = 50
        data = {}
        while True:
            page += 1
            print('*' * 20, page, '*' * 20)
            if page == 1:
                text = tool.requests_get(self.url, self.headers)
            else:
                text = tool.requests_post(self.url, data, self.headers)

            html = HTML(text)
            data = {
                '__CSRFTOKEN': html.xpath('//*[@id="__CSRFTOKEN"]/@value')[0],
                '__VIEWSTATE': html.xpath('//*[@id="__VIEWSTATE"]/@value')[0],
                # '__VIEWSTATEGENERATOR': html.xpath('//*[@id="__VIEWSTATEGENERATOR"]/@value')[0],
                '__EVENTTARGET': 'MoreinfoListsearch1$Pager',
                '__EVENTARGUMENT': str(page),
                '__VIEWSTATEENCRYPTED': '',
                '__EVENTVALIDATION': html.xpath('//*[@id="__EVENTVALIDATION"]/@value')[0],
                'MoreinfoListsearch1$txtTitle': '',
                'MoreinfoListsearch1$slrq': '',
                'MoreinfoListsearch1$slrq2': '',
                'MoreinfoListsearch1$Pager_input': str(page+1)
            }
            detail = html.xpath('//td[@id="MoreinfoListsearch1_tdcontent"]//tr')
            for tr in detail[1:]:
                try:
                    title = tr.xpath('./td[2]/div/a/@title')[0]
                    url = 'https://bidding.sinopec.com' + tr.xpath('./td[2]/div/a/@href')[0]
                    date_Today = date[:5] + tr.xpath('./td[3]/text()')[0].replace('\n', '').replace('\r',
                                                                                                         '').replace(
                        '\t', '') \
                        .replace(' ', '')
                    if '测试' in title:
                        continue
                    if tool.Transformation(date) <= tool.Transformation(date_Today):
                            self.parse_detile(title, url, date_Today)
                    else:
                        print('日期不符, 正在切换类型', date_Today)
                        return
                except Exception:
                    traceback.print_exc()


    def parse_detile(self, title, url, date):

        t = tool.requests_get(url, self.headers)
        if '抱歉，系统发生了错误！' in t:
            print('抱歉，系统发生了错误！')
            return
        url_html = etree.HTML(t)
        # try:
        detail = url_html.xpath('//td[@class="border"]/table/tr/td/table')[0]
        detail_html = etree.tostring(detail, method='HTML')
        detail_html = html.unescape(detail_html.decode()).replace('\xa0', '').replace('\ufeff', '')
        detail_text = ''.join(url_html.xpath('//table[@id="tblInfo"]//td[not(@id)]//text()')) \
            .replace('\xa0', '').replace('\n', '').replace('\r', '').replace('\t', '') \
            .replace(' ', '').replace('\xa5', '').replace('\ufeff', '')
        # except:
        #     try:
        #         detail = url_html.xpath('//td[@class="border"]/table/tr/td/table')[0]
        #         detail_html = etree.tostring(detail, method='HTML')
        #         detail_html = html.unescape(detail_html.decode()).replace('\xa0', '').replace('\ufeff', '')
        #         detail_text = ''.join(url_html.xpath('//td[@class="border"]/table/tr/td/table/text()')) \
        #             .replace('\xa0', '').replace('\n', '').replace('\r', '').replace('\t', '') \
        #             .replace(' ', '').replace('\xa5', '').replace('\ufeff', '')
        #     except:
        #         detail = url_html.xpath('//td[@class="border"]/table/tr/td/table')[0]
        #         detail_html = etree.tostring(detail, method='HTML')
        #         detail_html = html.unescape(detail_html.decode()).replace('\xa0', '').replace('\ufeff', '')
        #         detail_text = ''.join(url_html.xpath('//td[@class="border"]/table/tr/td/table/text()')) \
        #             .replace('\xa0', '').replace('\n', '').replace('\r', '').replace('\t', '') \
        #             .replace(' ', '').replace('\xa5', '').replace('\ufeff', '')
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
        item['body'] = tool.qudiao_width(detail_text)
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
        item['winner'] = tool.get_winner(detail_text)
        item['address'] = tool.get_address(detail_text)
        item['nativeplace'] = tool.get_title_city(item['title'])
        if item['nativeplace'] == 0:
            item['nativeplace'] = tool.more(item['title']+detail_text)
        item['linkman'] = tool.get_linkman(detail_text)
        item['function'] = tool.get_function(detail_text)
        item['resource'] = '中国石化物资招标投标网'
        item["shi"] = int(str(item["nativeplace"]).split('.')[0])
        if len(str(int(item["shi"]))) == 4:
            item['sheng'] = int(str(item["shi"])[:2] + '00')
        elif len(str(int(item["shi"]))) == 5:
            item['sheng'] = int(str(item["shi"])[:3] + '00')
        else:
            item['sheng'] = 0
        item['removal']= title
        process_item(item)
        # print(item['body'])

if __name__ == '__main__':
    import traceback, os
    try:
        jl = xinyang_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
        tool.send_error('报错文件：'+str(os.path.basename(__file__))+'报错信息：'+str(e))




