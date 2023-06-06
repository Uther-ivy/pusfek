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
        self.domain_name = 'http://www.tower.com.cn'
        self.url_list = [

        ]

        self.headers = {
        'Content-Type': 'application/json; charset=UTF-8',
        'Cookie': 'JSESSIONID=F6EBA8CF4D1E0B218F34BB431431A292; JSESSIONID=F717DAACAEFE84323FF8CBAFD766E45A',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',



        }

    def parse(self):
        date = tool.date
        # date = '2020-09-27'
        page = 0
        while True:
            page += 1
            url=f'http://www.tower.com.cn/default/main/index/cn.chinatowercom.obp.main.index.obphomepage.queryNoticeDetails.biz.ext'
            data={"noticeTitle":"","effectTime":"","failureTime":"","noticeType":"null","purchaseNoticeType":"2","resultsNoticeType":"2","level":"","provinceInput":"","cityInput":"","requestIp":"IP地址:123.150.72.113, CID:120000, 地区:天津市,浏览器版本:chrome/108.0.0.0","requestIpCode":"123.150.72.113","pageIndex":page,"pageSize":10,"sortField":"","sortOrder":"","page":{"begin":page*10,"length":10}}
            text = tool.requests_post(url ,json.dumps(data), self.headers)
            print('*' * 20, page, '*' * 20)
            # print(11, text.replace('\ufffd', ' ').replace('\u30fb', ' '))
            # time.sleep(6666)
            detail = json.loads(text)['obpNotice']
            for li in detail:
                title = li['notice_title']
                pid= li['id']
                url = f'http://www.tower.com.cn/default/main/index/noticedetail.jsp?_operation=notice&_notice=6&_id={pid}'
                date_Today = li['effect_time']
                if 'http' not in url:
                    url = self.domain_name + url
                print(title, url, date_Today)
                # time.sleep(666)
                endtime=re.findall(r'\d{4}-\d{2}-\d{2}', li['failure_time'])[0]
                date_Today = re.findall(r'\d{4}-\d{2}-\d{2}', date_Today)[0]
                if tool.Transformation(date) <= tool.Transformation(date_Today):
                    if tool.removal(title, date):
                        self.parse_detile(title, url, date_Today,endtime,pid)
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
        jsonurl='http://www.tower.com.cn/default/main/index/cn.chinatowercom.obp.portal.portal_notice.queryByNoticeType.biz.ext'
        print(jsonurl)
        data={
            'id': pid,
            '_notice': "6"
        }
        t = tool.requests_post(jsonurl,json.dumps(data), self.headers).replace('\xa9', '').replace('<br>&nbsp;&nbsp;', '')\
            .replace('</o:p><', '').replace('<o:p><', '')
        # print(t)
        for data in json.loads(t)['obpNotice']:
            # print(data)
        # time.sleep(2222)
            detail = etree.HTML(data['notice_content'])
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
            item['resource'] = '中国铁塔'
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


