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
        self.domain_name = 'https://zfcgmanager.czt.zj.gov.cn'
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
            url=f'https://zfcgmanager.czt.zj.gov.cn/cms/api/cors/remote/results?pageSize=15&pageNo={page}&sourceAnnouncementType=10016%2C3012%2C1002%2C1003%2C3014%2C3013%2C3009%2C4004%2C3008%2C2001%2C3001%2C3020%2C3003%2C3002%2C3011%2C3017%2C3018%2C3005%2C3006%2C3004%2C4005%2C4006%2C3007%2C3015%2C3010%2C3016%2C6003%2C4002%2C4001%2C4003%2C8006%2C1995%2C1996%2C1997%2C8008%2C8009%2C8013%2C8014%2C9002%2C9003%2C808030100%2C7003%2C7004%2C7005%2C7006%2C7007%2C7008%2C7009&isGov=true&url=notice'

            text = tool.requests_get(url , self.headers)
            print('*' * 20, page, '*' * 20)
            # print(11, text.replace('\ufffd', ' ').replace('\u30fb', ' '))
            # time.sleep(6666)
            detail = json.loads(text)['articles']
            for li in detail:
                title = li['title']
                id= li['id']
                url = li['url']
                date_Today = int(int(li['pubDate'])/1000)
                if 'http' not in url:
                    url = self.domain_name + url
                print(title, url, date_Today)
                # time.sleep(666)
                # endtime=re.findall(r'\d{4}-\d{2}-\d{2}', li['endtime'])[0]
                # date_Today = re.findall(r'\d{4}-\d{2}-\d{2}', date_Today)[0]
                if tool.Transformation(date) >= date_Today:
                    if tool.removal(title, date):
                        self.parse_detile(title, url, date_Today,id)
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
                break

    def parse_detile(self, title, url, date,id):
        print(url)


        jsonurl=f'https://zfcgmanager.czt.zj.gov.cn/cms/api/cors/remote/results?noticeId={id}%26utm&url=noticeDetail'
        t = tool.requests_get(jsonurl, self.headers).replace('\xa9', '').replace('<br>&nbsp;&nbsp;', '')\
            .replace('</o:p><', '').replace('<o:p><', '')
        data=json.loads(t)
        # print(data)

            # print(data)
        # time.sleep(2222)
        detail = etree.HTML(data['noticeContent'])
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
        item['body'] = tool.qudiao_width(detail_text)

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
        item['resource'] = '浙江政府采购网'
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


