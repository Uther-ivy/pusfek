# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 国家电网新一代电子商务平台
class baoshan_ggzy:
    def __init__(self):
        self.url='https://ecp.sgcc.com.cn/ecp2.0/ecpwcmcore//index/noteList'
        self.data_list = [
            {"index":2,"size":20,"firstPageMenuId":"20180502001","orgId":"","key":"","year":"","orgName":""},
        ]
        self.data = self.data_list.pop(0)
        self.headers = {
            'Accept': 'application/json, text/plain, */*',
            # 'Cookie': 'homeid=1a444a31-e460-47ff-9931-1c075c0f3cd8',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        }

    def parse(self):
        date = tool.date
        page = 0
        while True:
            page += 1
            self.data['index'] = page
            print('-'*50, page)
            # date = '2021-07-26'
            text = json.loads(tool.requests_post_to(self.url,self.data,self.headers))
            detail = text['resultValue']['noteList']
            for li in detail:
                url='https://ecp.sgcc.com.cn/ecp2.0/portal/#/doc/doci-change/' +str(li['id'])
                title = li['title']
                date_Today = li['noticePublishTime']
                doctype = li['doctype']
                if '测试' in title:
                    continue
                # print(title, url, date_Today)
                # time.sleep(666)
                if tool.Transformation(date) <= tool.Transformation(date_Today):
                    if tool.removal(title, date):
                        self.parse_detile(title, url, date, doctype)
                    else:
                        print('【existence】', url)
                        continue
                else:
                    print('日期不符, 正在切换类型', date_Today, self.url)
                    self.data = self.data_list.pop(0)
                    page = 0
                    continue
            if page==20:
                break

    def parse_detile(self, title, url, date, doctype):
        print(url)
        if 'bid' in doctype:
            t = tool.selenium_get_to(url)
            url_html = etree.HTML(t)
            try:
                detail = url_html.xpath('(//table[@class="tb"])[2]')[0]
                detail_html = etree.tostring(detail, method='HTML')
                detail_html = html.unescape(detail_html.decode())
                detail_text = url_html.xpath('string((//table[@class="tb"])[2])').replace('\xa0', '').replace('\n',
                                                                                                              '').replace(
                    '\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
            except:
                return

        elif 'win' in doctype:
            u = 'https://ecp.sgcc.com.cn/ecp2.0/ecpwcmcore//index/getNoticeWin'
            data = url.replace('https://ecp.sgcc.com.cn/ecp2.0/portal/#/doc/doci-change/', '')
            t = tool.requests_post_to(u, data, self.headers)
            detail_html = json.loads(t)['resultValue']['notice']['CONT']
            detail_text = ''.join(re.findall('>(.*?)<', detail_html, re.S)).replace('\xa0', '').replace('\n',
                                                                                                          '').replace(
                '\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
        else:
            return
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
        item['nativeplace'] = tool.get_title_city(item['title'])
        if item['nativeplace'] == 0:
            item['nativeplace'] = tool.more(item['title']+detail_text)
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
        item['resource'] = '国家电网新一代电子商务平台'
        if '.' in str(item["nativeplace"]):
            item["shi"] = int(float(str(item["nativeplace"]).replace("['","").split('.')[0]))
        else:
            item["shi"] = int(float(item["nativeplace"]))
        if len(str(int(item["shi"]))) == 4:
            item['sheng'] = int(str(item["shi"])[:2] + '00')
        elif len(str(int(item["shi"]))) == 5:
            item['sheng'] = int(str(item["shi"])[:3] + '00')
        else:
            item['sheng'] = 0
        # print(item)
        item['removal']= title
        process_item(item)

if __name__ == '__main__':

    import traceback, os
    try:
        jl = baoshan_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
