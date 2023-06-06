# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 中国铁建物资采购网
class baoshan_ggzy:
    def __init__(self):
        self.url_list=[
            'https://www.crccep.com/crcc-purportal-manage/portal/specialtopic/findNoticesBynotices',
        ]
        self.url = self.url_list.pop(0)
        self.headers = {
            # 'Cookie': 'homeid=1a444a31-e460-47ff-9931-1c075c0f3cd8',
            'Accept': '*/*',
            # 'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'
        }
        self.data={
            'likeKey': "",
            'noticeType': "5,3",
            'orgLevel':"" ,
            'pageNum': {},
            'pageSize': 15,
            'publishTimeBegin': "",
            'publishTimeEnd': "",
            'purCompanyName': "",
            'sourcingModeID':"",
      }
    def parse(self):
        date = tool.date
        page=0
        while True:
            page+=1
            self.data['pageNum'] = page
            resp = tool.requests_post_to(self.url,self.data,self.headers)
            html = json.loads(resp)
            # text = json.loads(tool.requests_get(self.url,self.headers).text)
            # https://www.crccep.com/crcc-purportal-manage/portal/specialtopic/findNoticesDetails?id=178876750825091072
            detail = html['list']
            print(detail)
            for li in detail:
                #https://ecm.crcc.cn/unlogin/queryPurchaseTenderDetailInit.jhtml?model=1&id=7fd83d6e38574f94bd00b63a42846fd7
                url='https://www.crccep.com/crcc-purportal-manage/portal/specialtopic/findNoticesDetails?id=' +li['id']
                title = li['noticeTitle']
                # date_Today = li['publishTime']
                date_Today = li['publishTime'].split(' ')[0]
                if '测试' in title:
                    continue
                if tool.Transformation(date) <= tool.Transformation(date_Today):
                    # if tool.removal(title, date):
                        self.parse_detile(title, url, date_Today)
                    # else:
                        # print('【existence】', url)
                        # continue
                else:
                    print('日期不符, 正在切换类型', date_Today, self.url)
                    return


    def parse_detile(self, title, url, date):
        print(url)
        t = tool.requests_get(url, self.headers)
        # url_html = etree.HTML(t)
        url_html = json.loads(t)
        detail = url_html["noticeContent"]
        # detail_html = etree.tostring(detail, method='HTML')
        # detail_html = html.unescape(detail_html.decode())
        # detail_text = url_html.xpath('string((//div[@class="container"]//div)[2])').replace('\xa0', '').replace('\n', '').replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
        item = {}
        item['title'] = title.replace('\u2022', '')
        item['url'] = url
        item['date'] = date
        item['typeid'] = tool.get_typeid(item['title'])
        item['senddate'] = int(time.time())
        item['mid'] = 867
        item['infotype'] = tool.get_infotype(item['title'])
        item['body'] = tool.qudiao_width(detail)
        item['endtime'] = tool.get_endtime(detail)
        item['nativeplace'] = tool.get_title_city(item['title'])
        if item['nativeplace'] == 0:
            item['nativeplace'] = tool.more(item['title']+detail)
        if item['endtime'] == '':
            item['endtime'] = int(time.mktime(time.strptime(date, "%Y-%m-%d")))
        else:
            try:
                item['endtime'] = int(time.mktime(time.strptime(item['endtime'], "%Y-%m-%d")))
            except:
                item['endtime'] = int(time.mktime(time.strptime(date, "%Y-%m-%d")))
        item['tel'] = tool.get_tel(detail)
        item['email'] = ''
        item['winner'] = tool.get_winner(detail)
        item['address'] = tool.get_address(detail)
        item['linkman'] = tool.get_linkman(detail)
        item['function'] = tool.get_function(detail)
        item['resource'] = '中国铁建物资采购网'
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
