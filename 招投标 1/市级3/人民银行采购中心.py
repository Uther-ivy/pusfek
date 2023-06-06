# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 玉林市公共资源交易中心
class wenshan_ggzy:
    def __init__(self):
        self.domain_name = 'https://jzcg.pbc.gov.cn'
        self.url_list = [

        ]

        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',

        }

    def parse(self):
        date = tool.date
        # date = '2020-09-27'
        page = 0
        while True:
            page += 1
            url=f'https://jzcg.pbc.gov.cn/freecms/rest/v1/notice/selectInfoMoreChannel.do?&siteId=9e9a312c-e98f-4516-95ff-74af73e2f6c4&channel=4081b14c-c0a5-4585-ae0f-60c72b29beb0&noticeType=&currPage=2&pageSize=10&operationStartTime=&operationEndTime=&title=&purchaseManner=&agency=%E4%B8%AD%E5%9B%BD%E4%BA%BA%E6%B0%91%E9%93%B6%E8%A1%8C%E9%9B%86%E4%B8%AD%E9%87%87%E8%B4%AD%E4%B8%AD%E5%BF%83&selectTimeName=noticeTime'

            text = tool.requests_get(url , self.headers)
            print('*' * 20, page, '*' * 20)
            # print(11, text.replace('\ufffd', ' ').replace('\u30fb', ' '))
            # time.sleep(6666)
            detail = json.loads(text)['data']
            for li in detail:
                title = li['shorttitle']
                cid= li['channel']
                pid= li['site']
                tendercode=li['fieldValues']['f_openTenderCode']
                url = li['pageurl']
                date_Today = li['addtimeStr']
                if 'http' not in url:
                    url = self.domain_name + url
                # print(title, url, date_Today)
                # time.sleep(666)
                endtime=re.findall(r'\d{4}-\d{2}-\d{2}', li['fieldValues']['f_openTenderTime'])[0]
                date_Today = re.findall(r'\d{4}-\d{2}-\d{2}', date_Today)[0]
                if tool.Transformation(date) <= tool.Transformation(date_Today):
                    if tool.removal(title, date):
                        self.parse_detile(title, url, date_Today,endtime,pid ,cid,tendercode)
                    else:
                        print('【existence】', url)
                        continue
                else:
                    print('日期不符, 正在切换类型', date_Today, self.url)
                    self.url = self.url_list.pop(0)
                    page = 0
                    break
            if page == 20:
                self.url = self.url_list.pop(0)
                page = 0

    def parse_detile(self, title, url, date,endtime, pid ,cid,tendercode):
        print(url)
        jsonurl=f'https://jzcg.pbc.gov.cn/freecms/rest/v1/notice/selectInfoByOpenTenderCode.do?&channel={cid}&site={pid}&openTenderCode={tendercode}'
        t = tool.requests_get(jsonurl, self.headers).replace('\xa9', '').replace('<br>&nbsp;&nbsp;', '')\
            .replace('</o:p><', '').replace('<o:p><', '')
        # print(t)
        data=json.loads(t)['data'][0]
            # print(data)
        # time.sleep(2222)
        detail = etree.HTML(data['content'])
        detail_html = etree.tostring(detail, method='HTML')
        detail_html = html.unescape(detail_html.decode()).replace("display: none", '').replace("\u2022", '').replace('\xa0', '')
        detail_text = detail_html.replace('\xa0', '').replace('\n',
                                                                                                             ''). \
            replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
        # if len(detail_html) < 200:
        #     int('a')
        item = {}
        item['title'] = title.replace('\u2022', '')
        item['url'] = url
        item['date'] = date
        item['typeid'] = tool.get_typeid(item['title'])
        item['senddate'] = int(time.time())
        item['mid'] = 867
        item['nativeplace'] = float(tool.get_title_city(item['title']))
        item['infotype'] = tool.get_infotype(item['title'])
        item['body'] = tool.qudiao_width(detail_html)

        item['endtime'] = tool.get_endtime(endtime)
        if item['endtime'] == '':
            print(date)
            item['endtime'] =date
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
        item['resource'] = '人民银行采购中心'
        item["shi"] = int(item["nativeplace"])
        if len(str(item["nativeplace"])) == 4:
            item['sheng'] = int(str(item["nativeplace"])[:2] + '00')
        elif len(str(item["nativeplace"])) == 5:
            item['sheng'] = int(str(item["nativeplace"])[:3] + '00')
        else:
            item['sheng'] = 0
        item['removal']= title
        process_item(item)
        print(item)


if __name__ == '__main__':
    import traceback,os
    try:
        jl = wenshan_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
        tool.send_error('报错文件：'+str(os.path.basename(__file__))+'报错信息：'+str(e))


