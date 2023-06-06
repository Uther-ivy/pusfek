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
        self.domain_name = 'http://www.yngp.com'
        self.url_list = [

        ]

        self.headers = {
            'Cookie': 'xincaigou=49737.2934.1035.0000; __jsluid_h=d5c38fed851dfd746142c833a2a3d61b; route=d9b0266c2b8d5ad36e751f051b0faf07; JSESSIONID=7VEoWBWU5tEUATRA8FfiZTJpBNnT4pDJbxHocgtkVYXoKgm6nyG8!-1189388391',
            'Referer': 'http://www.yngp.com/page/procurement/procurementList.html',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',

        }

    def parse(self):
        date = tool.date
        # date = '2020-09-27'
        page = 0
        while True:
            page += 1
            url=f'http://www.yngp.com/api/firstpage/firstpage.gghtlist.svc'
            for leve in range(1,3):
                data = {
                    'LEVEL': str(leve),
                    'TYPE': '1'

                }
                text = tool.requests_post(url,data,self.headers )
                # print('*' * 20, page, '*' * 20)
                # print(11, text.replace('\ufffd', ' ').replace('\u30fb', ' '))
                # time.sleep(6666)
                detail = json.loads(text)['data']
                for li in detail:
                    title = li['BULLETINTITLE']
                    id= li['BULLETIN_ID']
                    url = f'http://www.yngp.com/showBulletinInfo.html?bulletin_id={id}'
                    date_Today = li['FINISHDAY']
                    city=li['DISTRICTNAME']
                    if 'http' not in url:
                        url = self.domain_name + url
                    print(title, url, date_Today)
                    # time.sleep(666)
                    if tool.Transformation(date) <= tool.Transformation(date_Today):
                        if tool.removal(title, date):
                            self.parse_detile(title, url, date_Today,city)
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

    def parse_detile(self, title, url, date,city):
        print(url)
        t = tool.requests_get(url, self.headers).replace('\xa9', '').replace('<br>&nbsp;&nbsp;', '')\
            .replace('</o:p><', '').replace('<o:p><', '')
        # print(t)
        # time.sleep(2222)
        url_html = etree.HTML(t)
        detail = url_html.xpath("//table/tbody")[0]
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
        item['nativeplace'] =float(tool.get_title_city(city))
        item['infotype'] = tool.get_infotype(item['title'])
        item['body'] = tool.qudiao_width(detail_html)
        item['endtime'] = tool.get_endtime(detail_text)
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
        item['resource'] = '云南政府采购网'
        item["shi"] = int(item["nativeplace"])
        if len(str(item["nativeplace"])) == 4:
            item['sheng'] = int(str(item["nativeplace"])[:2] + '00')
        elif len(str(item["nativeplace"])) == 5:
            item['sheng'] = int(str(item["nativeplace"])[:3] + '00')
        else:
            item['sheng'] = 0
        item['removal'] = title
        item['removal']= title
        process_item(item)
        # print(item)

if __name__ == '__main__':
    import traceback,os
    try:
        jl = wenshan_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
        tool.send_error('报错文件：'+str(os.path.basename(__file__))+'报错信息：'+str(e))


