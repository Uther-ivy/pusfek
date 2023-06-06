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
        self.domain_name = 'http://ebid.okap.com'
        self.url_list = []
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        }

    def parse(self):
        date = tool.date
        # date = '2020-09-27'
        page = 0
        while True:
            page += 1
            url=f'http://ebid.okap.com/api/ebidproject/listProject'
            payload = {
                'projectClass':  '',
                'projectName': '',
                'sort':1,
                'pageSize':5,
                'pageNum': page


                }
            text = tool.requests_post(url ,payload, self.headers)
            print('*' * 20, page, '*' * 20)
            # print(11, text.replace('\ufffd', ' ').replace('\u30fb', ' '))
            # time.sleep(6666)
            detail = json.loads(text)['result']['list']
            for li in detail:
                title = li['V_PROJECT_NAME']
                cid= li['V_PROJECTID']
                date_Today = li['V_TIME']
                url=f'http://ebid.okap.com/#/front/tradingContent?id={cid}&tabSelectedIndex=0&classification=cg'
               # city=li['area']
                if 'http' not in url:
                    url = self.domain_name + url
                print(title, url, date_Today)
                endtime=re.findall(r'\d{4}-\d{2}-\d{2}', li['V_BUY_ENDTIME'])[0]
                date_Today = re.findall(r'\d{4}-\d{2}-\d{2}', date_Today)[0]
                if tool.Transformation(date) <= tool.Transformation(date_Today):
                    if tool.removal(title, date):
                        self.parse_detile(title, url, date_Today,cid,endtime)
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

    def parse_detile(self, title, url, date,cid,endtime):
        print(url)
        pdfurl = 'http://ebid.okap.com/api/ebidproject/infoProject'
        pdfdata = {'projectId': f'{cid}'}
        pdftext = tool.requests_post(pdfurl, pdfdata, self.headers)
        pdfhref = json.loads(pdftext)['result']['infoTime'][0]['V_FILE_URL']
        print(pdfhref)
        url = f'http://ebid.okap.com/static/pdf/web/viewer.html?file={pdfhref}'

        print(url)
        # time.sleep(666)
        html_data=f"<a href = '{url}'>{title}.pdf</a>"
            # print(data)
        # time.sleep(2222)
        detail = etree.HTML(html_data)
        detail_html = etree.tostring(detail, method='HTML')
        detail_html = html.unescape(detail_html.decode()).replace("display: none", '').replace("\u2022", '').replace('\xa0', '')
        detail_text = detail_html.replace('\xa0', '').replace('\n','').replace('\r', '').replace('\t', '').replace('\xa5', '')
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
        item['body'] = tool.qudiao_width(detail_text)

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
        item['resource'] = 'E共享'
        item["shi"] = int(item["nativeplace"])
        if len(str(item["nativeplace"])) == 4:
            item['sheng'] = int(str(item["nativeplace"])[:2] + '00')
        elif len(str(item["nativeplace"])) == 5:
            item['sheng'] = int(str(item["nativeplace"])[:3] + '00')
        else:
            item['sheng'] = 0
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


