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
        self.domain_name = 'https://www.nbzfcg.cn'
        self.url_list = [


        ]

        self.headers = {
            'Cookie': 'ASP.NET_SessionId=pzzlrjy3yqyrlv55ubxd4dvn',
'Host': 'www.nbzfcg.cn',
'Content-Type': 'application/x-www-form-urlencoded',
# 'Referer': url,
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'

        }

    def parse(self):
        date = tool.date
        # date = '2020-09-27'
        page = 1
        url=f'https://www.nbzfcg.cn/project/zcyNotice.aspx?noticetype=13'
        payload = {
            '__EVENTTARGET': 'gdvNotice3$ctl18$AspNetPager1',
            '__EVENTARGUMENT': page,
            'ddlRegion': '',
            'txtNoticeTitle': '',
            'txtNoticeDate1': '',
            'txtNoticeDate2': '',
            'gdvNotice3$ctl18$AspNetPager1_input': 1
            }
        text = tool.requests_post(url , json.dumps(payload),self.headers)
        print('*' * 20, page, '*' * 20)
        html = HTML(text)
        # print(11, text.replace('\ufffd', ' ').replace('\u30fb', ' '))
        # time.sleep(6666)
        detail = html.xpath("//table[@id='gdvNotice3']//tr")
        for num in range(2,len(detail)+1):
            title = html.xpath(f"//table[@id='gdvNotice3']//tr[{num}]/td[3]/a/text()")[0].replace('\xa0', '').replace('\n', ''). \
                replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
            url = html.xpath(f"//table[@id='gdvNotice3']//tr[{num}]/td[3]/a/@href")[0]
            date_Today = html.xpath(f"//table[@id='gdvNotice3']//tr[{num}]/td[4]/text()")[0].replace('\xa0', '').replace('\n', ''). \
                replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '').replace('开标时间：', '')
            if 'http' not in url:
                url = self.domain_name +'/project/'+ url
            print(title, url, date_Today)
            # time.sleep(666)
            # endtime=re.findall(r'\d{4}-\d{2}-\d{2}', li['tovEnd'])[0]
            date_Today = re.findall(r'\d{4}-\d{2}-\d{2}', date_Today)[0]
            if tool.Transformation(date) <= tool.Transformation(date_Today):
                if tool.removal(title, date):
                    self.parse_detile(title, url, date_Today)
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

    def parse_detile(self, title, url, date):
        print(url)
        t = tool.requests_get(url, self.headers).replace('\xa9', '').replace('<br>&nbsp;&nbsp;', '')\
            .replace('</o:p><', '').replace('<o:p><', '')
        html_=etree.HTML(t)
        detail=html_.xpath("//div[@class='frame_list01']//td")[0]
        # time.sleep(2222)
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

        item['endtime'] = tool.get_endtime(date)
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
        item['resource'] = '宁波政府采购网'
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


