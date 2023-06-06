# -*- coding: utf-8 -*-
import json
import re
import time, html
from lxml import etree
from lxml.etree import HTML

import tool
from save_database import process_item

# 上海地铁采购电子商务平台
class alashan_ggzy:
    def __init__(self):

        self.domain_name='https://bid.norincogroup-ebuy.com'

        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
        }

    def parse(self):
        date = tool.date
        # date = '2020-01-06'
        page = 0
        while True:
            page += 1
            url='https://bid.norincogroup-ebuy.com/retrieve.do'
            data={

'fl': '',
'hy': '',
'dq': '',
'es': 1,
'keyFlag': '',
'packtype': '',
'packtypeCode': '',
'packtypeValue': '',
'packtypeCodeValue': '',
'typflag': 1,
'fbdays': 0,
'esly': '',
'validityPeriodFlag': '' ,
'flag1': '',
'orderby': 1,
'keyConValue': '',
'keyCon': '',
'fbDateStart': '',
'fbDateEnd': '',
'radio': 'on',
'ggyxq_time': '2022-12-19 17:00:00',
'ggyxq_time': '2022-12-17 17:00:00',
'ggyxq_time': '2022-12-14 17:00:00',
'ggyxq_time': '2022-12-16 18:00:00',
'ggyxq_time': '2022-12-16 17:00:00',
'ggyxq_time': '2022-12-13 23:59:59',
'ggyxq_time': '2022-12-13 23:59:59',
'ggyxq_time': '2022-12-13 23:59:59',
'ggyxq_time': '2022-12-09 23:59:59',
'ggyxq_time': '2022-12-09 23:59:59',
'pageNumber': page,
'pageSize': 10,
'sortColumns': 'undefined'

            }
            print('*' * 20, page, '*' * 20)
            text = tool.requests_post_param(url ,self.headers,data).replace('&#x2f;', '/')
            html = HTML(text)
            # print(11, text)
            # time.sleep(6666)
            detail = html.xpath("//div[@class='item']")
            for li in detail:
                title = li.xpath(".//a[@class='sldivTitle']/span/text()")[0].replace('\xa0', '').replace('\n', ''). \
                    replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
                url = li.xpath(".//a[@class='sldivTitle']/@href")[0]
                anymore=li.xpath(".//span[@class='date']/text()")
                date_Today = anymore[0].replace('\xa0', '').replace('\n', ''). \
                    replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '').replace('发布日期:','')
                city=anymore[1]
                if 'http' not in url:
                    url = self.domain_name + url
                date_Today = re.findall(r'\d{4}-\d{2}-\d{2}', date_Today)[0]
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
                print('日期不符, 正在切换类型')
                self.url = self.url_list.pop(0)
                page = 0

    def parse_detile(self, title, url, date,city):
        if 'toZbggInfo' in url:
            pid=re.findall('probid=([\d\w]+)',url)[0]
            newurl=f'https://bidfile.norincogroup-ebuy.com/bdfileservice//upfile2009/bdsnapshot/zbgg/{pid}/{pid}.html'
            url_text = tool.requests_get(newurl, self.headers)
            url_html = etree.HTML(url_text)
            detail = url_html.xpath("//div[@class='zbztb_ggcont clearfix mlr20']")[0]
            # print(url_text)
            detail_html = etree.tostring(detail, method='HTML')
            detail_html = html.unescape(detail_html.decode())
            detail_text = detail_html
        else:
            newurl=url
            url_text = tool.requests_get(newurl, self.headers)
            url_html = etree.HTML(url_text)
            detail = url_html.xpath("//div[@class='zbztb_container mb50']//iframe")[0]
            # print(url_text)
            detail_html = etree.tostring(detail, method='HTML')
            detail_html = html.unescape(detail_html.decode())
            detail_text = detail_html
            # .replace('\xa0', '').replace('\n','').replace('\r', '').replace('\t','').replace(' ', '').replace('\xa5', '')
        item = {}
        item['title'] = title.replace('\u2022', '')
        item['url'] = url
        item['date'] = date
        item['typeid'] = tool.get_typeid(item['title'])
        item['senddate'] = int(time.time())
        item['mid'] = 867
        item['address'] = tool.get_address(detail_text)
        item['nativeplace'] = float(tool.get_title_city(city))
        item['infotype'] = tool.get_infotype(item['title'])
        item['body'] = tool.qudiao_width(detail_html)
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
        item['linkman'] = tool.get_linkman(detail_text)
        item['function'] = tool.get_function(detail_text)
        item['resource'] = '中国兵器'
        item["shi"] = int(item["nativeplace"])
        if len(str(item["nativeplace"])) == 4:
            item['sheng'] = int(str(item["nativeplace"])[:2] + '00')
        elif len(str(item["nativeplace"])) == 5:
            item['sheng'] = int(str(item["nativeplace"])[:3] + '00')
        else:
            item['sheng'] = 0
        item['removal']= title
        process_item(item)
        # print(item["nativeplace"],item['address'],item['sheng'],item["shi"])
        # print(item)



if __name__ == '__main__':
    import traceback, os
    try:
        jl = alashan_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
        if 'pop from empty list'!=str(e):
            print('报错')
            with open('error_name.txt', 'a+', encoding='utf-8')as f:
                f.write(str(os.path.basename(__file__)))
                f.write('\n')
                f.write(str(traceback.format_exc()))
                f.write('\n')
        else:
            with open('success.txt','a+',encoding='utf-8')as f:
                f.write(str(os.path.basename(__file__)))
                f.write('\n')
                f.write(str('无连接抓取'))
                f.write('\n')

