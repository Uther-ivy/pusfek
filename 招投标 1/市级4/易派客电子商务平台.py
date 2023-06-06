# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 易派客电子商务平台
class wenshan_ggzy:
    def __init__(self):
        self.url_list = [
            'https://gateway.epec.com/api/cms/announcement/queryAnnouncementPageInfo', #招标公告
                    ]
        self.url = self.url_list.pop(0)
        self.headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'}
    def parse(self):
        date = tool.date
        # date = '2020-09-21'
        page = 0
        while True:
            page += 1
            data = {
                "announcementFirstChannel": "tenderPurchaseAnnouncement",
                "announcementSecondChannel": "",
                "firstQuery": True,
                "keyWords": "",
                "operationType": False,
                "pageNum": page,
                "pageSize": 10
            }
            text = tool.requests_post_to(url=self.url, headers=self.headers,data=data)
            print('*' * 20, page, '*' * 20)
            html = json.loads(text)
            # print(11, text)
            # time.sleep(6666)
            detail = html["data"]["announcementDataList"]["records"]
            for li in detail:
                title = li["title"]
                date_Today = li["publishTime"].split(' ')[0]
                announcementId = li["announcementId"]
                product = li["product"]
                collectioned = li["collectioned"]
                url = 'https://gateway.epec.com/api/cms/announcement/queryIntegrateAnnouncementDetailInfo'
                # print(title, url, date_Today)
                # time.sleep(666)
                # self.parse_detile(title, url, date_Today,announcementId,product,collectioned)
                if tool.Transformation(date) <= tool.Transformation(date_Today):
                    if tool.removal(title, date):
                        self.parse_detile(title, url, date_Today,announcementId,product,collectioned)
                    else:
                        print('【existence】', url)
                        continue
                else:
                    print('日期不符, 正在切换类型', date_Today)
                    self.url = self.url_list.pop(0)
                    break
            if page == 20:
                print('日期不符, 正在切换类型')
                self.url = self.url_list.pop(0)
                break

    def parse_detile(self, title, url, date,announcementId,product,collectioned):
        print(url)
        data2={"announcementId":announcementId,"announcementSecondChannel":product,"announcementType":collectioned}
        t = tool.requests_post_to(url=url, headers=self.headers,data=data2)
        # print(t)
        # time.sleep(2222)
        url_html = json.loads(t)
        try:
            detail = url_html["data"]["announcementData"]["content"]
        except:
            return
        index_url=f'https://emall.epec.com/advisoryNotice/advisoryNoticeDetail?announcementId={announcementId}&announcementSecondChannel={product}&announcementType={collectioned}'
        # detail_html = etree.tostring(detail, method='HTML')
        # detail_html = html.unescape(detail_html.decode()).replace("display: none", '')
        # detail_text = url_html.xpath('string(//div[@class="detail-box"])').replace('\xa0', '').replace('\n', '').\
        #     replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
        if len(t) < 200:
            int('a')
        item = {}
        item['title'] = title.replace('\u2022', '')
        item['url'] = index_url
        item['date'] = date
        item['typeid'] = tool.get_typeid(item['title'])
        item['senddate'] = int(time.time())
        item['mid'] = 867
        item['nativeplace'] = self.get_nativeplace(item['title'])
        item['infotype'] = tool.get_infotype(item['title'])
        item['body'] = tool.qudiao_width(detail)
        item['body'] = item['body']
        # print(item['body'].replace('\xa0', '').replace('\xa5', '').replace('\xb3', ''))
        # time.sleep(6666)
        item['endtime'] = tool.get_endtime(detail)
        if item['endtime'] == '':
            item['endtime'] = int(time.mktime(time.strptime(date, "%Y-%m-%d")))
        else:
            try:
                item['endtime'] = int(time.mktime(time.strptime(item['endtime'], "%Y-%m-%d")))
            except:
                item['endtime'] = int(time.mktime(time.strptime(date, "%Y-%m-%d")))
        item['tel'] = tool.get_tel(detail)
        item['email'] = ''
        item['address'] = tool.get_address(detail)
        item['linkman'] = tool.get_linkman(detail)
        item['function'] = tool.get_function(detail)
        item['resource'] = '易派客电子商务平台'
        item['shi'] = 6507
        item['sheng'] = 6500
        item['removal'] = title
        # print(item)
        process_item(item)
    def get_nativeplace(self, addr):
        city = ''
        city_list = [['6507.001', '铜官山区'], ['6507.002', '狮子山区'], ['6507.003', '郊区'], ['6507.004', '铜陵县']]
        for i in city_list:
            if i[1] in addr:
                city = float(i[0])
                break
        if city == '':
            city = 6507
        return city

if __name__ == '__main__':
    import os,traceback
    try:
        jl = wenshan_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
        tool.send_error('报错文件：'+str(os.path.basename(__file__))+'报错信息：'+str(e))



