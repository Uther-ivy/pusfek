# -*- coding: utf-8 -*-
import json
import re
import time, html
from binascii import a2b_hex

from lxml import etree
from lxml.etree import HTML

import tool
from save_database import process_item

# 上海地铁采购电子商务平台
class alashan_ggzy:
    def __init__(self):

        self.domain_name='http://www.ccgp-qingdao.gov.cn'

        self.headers = {
            'Host': 'www.ccgp-qingdao.gov.cn',
            'Referer': 'http://www.ccgp-qingdao.gov.cn/sdgp2014/site/index370200.jsp',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
        }

    def parse(self):
        date = tool.date
        # date = '2020-01-06'
        page = 0
        while True:
            page += 1
            url='http://www.ccgp-qingdao.gov.cn/sdgp2014/dwr/call/plaincall/dwrmng.queryWithoutUi.dwr'
            print('*' * 20, page, '*' * 20)
            data={
                'callCount': 1,
                'nextReverseAjaxIndex': 0,
                'c0-scriptName': 'dwrmng',
                'c0-methodName': 'queryWithoutUi',
                'c0-id': 0,
                'c0-param0': 'number:7',
                'c0-e1': 'string:0401',
                'c0-e2': f'string:{page}',
                'c0-e3': 'number:10',
                'c0-e4': 'string:',
                'c0-param1': 'Object_Object:{_COLCODE:reference:c0-e1, _INDEX:reference:c0-e2, _PAGESIZE:reference:c0-e3, _REGION:reference:c0-e4}',
                'batchId': 1,
                'instanceId': 0,
                'page': '%2Fsdgp2014%2Fsite%2Fchannelall370200.jsp%3Fcolcode%3D0401%26flag%3D0401',
                'scriptSessionId': 'OR23ZKteoTcQH4Oo!oyR6qs9m6TuwCruEko/DDEDEko-7trG3VsI4',
            }
            text = tool.requests_post(url,data, self.headers).replace('&#x2f;', '/')
            list_data=re.findall(r'rsltStringValue:\"(.*)\"\,',text)[0]
            for lists in list_data.split('?'):
                li=lists.split(',')
                title = li[1].encode('utf-8').decode("unicode_escape")
                cid=li[0]
                url = f'http://www.ccgp-qingdao.gov.cn/sdgp2014/site/read370200.jsp?id={cid}&flag=0401'
                date_Today = li[2]
                if 'http' not in url:
                    url = self.domain_name + url
                print(title, url, date_Today)
                # time.sleep(666)
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
                print('日期不符, 正在切换类型')
                self.url = self.url_list.pop(0)
                page = 0

    def parse_detile(self, title, url, date):
        # guid=re.findall('guid=([\d\w\-]+)&',url)[0]
        # newurl=f'https://node.dzzb.ciesco.com.cn/xunjia-mh/gonggaoxinxi/gongGao_view_3.html?guid={guid}&callBackUrl=https://dzzb.ciesco.com.cn/html/crossDomainForFeiZhaoBiao.html'
        url_text = tool.requests_get(url, self.headers)
        url_html = etree.HTML(url_text)
        detail = url_html.xpath("//div[@class='cont']/div[3]")[0]
        detail_html = etree.tostring(detail, method='HTML')
        detail_html = html.unescape(detail_html.decode())
        detail_text = detail_html.replace('\xa0', '').replace('\n','').replace('\r', '').replace('\t','').replace(' ', '').replace('\xa5', '')
        item = {}
        item['title'] = title.replace('\u2022', '')
        item['url'] = url
        item['date'] = date
        item['typeid'] = tool.get_typeid(item['title'])
        item['senddate'] = int(time.time())
        item['mid'] = 867
        item['address'] = tool.get_address(detail_text)
        item['nativeplace'] = float(tool.get_title_city(item['title']))
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
        item['resource'] = '青岛政府采购网'
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
            with open('error_name.txt','a+',encoding='utf-8')as f:
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

