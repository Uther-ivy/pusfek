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
        self.domain_name = 'https://www.changanjyzx.com'
        self.url_list = [
            'https://www.changanjyzx.com/notice/pageNoticeByType'
        ]
        self.url = self.url_list.pop(0)
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',

        }

    def parse(self):
        date = tool.date
        # date = '2020-09-27'
        page = 0
        while True:
            page += 1
            for type in [0,9,12,15,20]:
                data = {
                    'projectCode': '',
                    'title': '',
                    'projectType': '',
                    'projectMethod': '',
                    'pageNumber': page,
                    'type': type,
                    'pageSize': 15,
                    'province': '',
                    'city': ''

                }
                text = tool.session_post(self.url, data)
                print('*' * 20, page, '*' * 20)
                # print(11, text.replace('\ufffd', ' ').replace('\u30fb', ' '))
                # time.sleep(6666)
                detail = json.loads(text)['data']
                for li in detail:
                    title = li['title']
                    pid= li['id']
                    url = f'https://www.changanjyzx.com/noticeDetail?type={type}&id={pid}'
                    date_Today =li['pulishDate']
                    if 'http' not in url:
                        url = self.domain_name + url
                    # print(title, url, date_Today)
                    # time.sleep(666)
                    endtime = re.findall(r'\d{4}-\d{2}-\d{2}', li['endDate'])[0]
                    date_Today = re.findall(r'\d{4}-\d{2}-\d{2}', date_Today)[0]
                    if tool.Transformation(date) <= tool.Transformation(date_Today):
                        if tool.removal(title, date):
                            self.parse_detile(title, url, date_Today,endtime,pid )
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

    def parse_detile(self, title, url, date,endtime,pid):
        print(url)
        data={
            'id': pid
        }
        jsonurl='https://www.changanjyzx.com/notice/getNoticeDetailById'
        t = tool.requests_post(jsonurl, data ,self.headers).replace('\xa9', '').replace('<br>&nbsp;&nbsp;', '')\
            .replace('</o:p><', '').replace('<o:p><', '')
        # print(t)
        # time.sleep(2222)
        content=json.loads(t)['data']
        detail = etree.HTML(content['content'])
        # print(detail)
        # detail = url_html.xpath("//div[@class='wrap']/div")[0]
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
        item['resource'] = '中国五矿'
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


