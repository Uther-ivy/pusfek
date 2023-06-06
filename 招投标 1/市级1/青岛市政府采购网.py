# -*- coding: utf-8 -*-
import json
import re
import time, html
from lxml import etree
import tool
from save_database import process_item

# 青岛市政府采购网
class alashan_ggzy:
    def __init__(self):
        self.url_code = [
            '0401', '0402', '0403', '0404', '0405'
        ]
        self.url = self.url_code.pop(0)
        self.headers = {
            'Accept': '*/*',
            'Content-Type': 'text/plain',
            'Cookie': 'JSESSIONID=D980623A7832F8A6ACC7BFF452E89D55; DWRSESSIONID=xzGTYIJ1XtAQg0rWY8ouhMDXwOoI~OVfkzn; JSESSIONID=D980623A7832F8A6ACC7BFF452E89D55; JSESSIONID=D980623A7832F8A6ACC7BFF452E89D55; DWRSESSIONID=xzGTYIJ1XtAQg0rWY8ouhMDXwOoI~OVfkzn',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
        }

    def parse(self):
        date = tool.date
        # date = '2020-01-06'
        page = 0
        url_to = 'http://zfcg.qingdao.gov.cn/sdgp2014/dwr/call/plaincall/dwrmng.queryWithoutUi.dwr'
        while True:
            page += 1
            data = 'callCount=1\nnextReverseAjaxIndex=0\nc0-scriptName=dwrmng\nc0-methodName=queryWithoutUi\nc0-id=0\nc0-param0=number:7\nc0-e1=string:'+self.url+'\nc0-e2=string:'+str(page)+'\nc0-e3=number:10\nc0-e4=string:\nc0-e5=string:undefined\nc0-param1=Object_Object:{_COLCODE:reference:c0-e1, _INDEX:reference:c0-e2, _PAGESIZE:reference:c0-e3, _REGION:reference:c0-e4, _KEYWORD:reference:c0-e5}\nbatchId=17\ninstanceId=0\npage=%2Fsdgp2014%2Fsite%2Fchannelall370200.jsp%3Fcolcode%3D0401%26flag%3D0401\nscriptSessionId=xzGTYIJ1XtAQg0rWY8ouhMDXwOoI~OVfkzn/7JMxjzn-3EUajdPx0'
            print('*' * 20, page, '*' * 20)
            text = tool.requests_post(url_to, data, self.headers)
            # print(text)
            detail = re.findall('rsltStringValue:"(.*?)",rsltType:null}', text, re.S)[0].encode('utf-8').decode('unicode_escape').split('?')
            # print(111, detail)
            # time.sleep(666)
            for li in detail:
                li = li.split(',')
                title = li[1].replace('\r', '').replace('\t', '').replace(' ', '').replace('\n', '')
                url = 'http://zfcg.qingdao.gov.cn/sdgp2014/site/read370200.jsp?id={}&flag=0401'.format(li[0])
                date_Today = li[2].replace('\r', '').replace('\t', '').replace(' ', '').replace('[', '').replace(']', '')
                if '-' not in date_Today:
                    continue
                # print(title, url, date_Today)
                # time.sleep(666)
                if tool.Transformation(date) <= tool.Transformation(date_Today):
                    if tool.removal(title, date):
                        self.parse_detile(title, url, date_Today)
                    else:
                        print('【existence】', url)
                        continue
                else:
                    print('日期不符, 正在切换类型...', date_Today, self.url)
                    self.url = self.url_code.pop(0)
                    page = 0
                    break



    def parse_detile(self, title, url, date):
        print(url)
        url_text = tool.requests_get(url, self.headers)
        url_html = etree.HTML(url_text)
        detail = url_html.xpath('/html/body/div[4]/div[2]/div[1]/div[3]')[0]
        detail_html = etree.tostring(detail, method='HTML')
        detail_html = html.unescape(detail_html.decode()).replace('\xa0', '')
        detail_text = url_html.xpath('string(/html/body/div[4]/div[2]/div[1]/div[3])').replace('\xa0', '').replace('\n', '').replace('\r', '').replace('\t',
                                                                                                                  '').replace(
            ' ', '').replace('\xa5', '')
        item = {}
        item['title'] = title.replace('\u2022', '')
        item['url'] = url
        item['date'] = date
        item['typeid'] = tool.get_typeid(item['title'])
        item['senddate'] = int(time.time())
        item['mid'] = 867
        item['nativeplace'] = self.get_nativeplace(item['title']+detail_text)
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
        item['address'] = tool.get_address(detail_text)
        item['linkman'] = tool.get_linkman(detail_text)
        item['function'] = tool.get_function(detail_text)
        item['resource'] = '青岛市政府采购网'
        item['shi'] = 8002
        item['sheng'] = 8000
        item['removal']= title
        process_item(item)
        # print(item['nativeplace'], item['title'])

    def get_nativeplace(self, addr):
        city_list = [['8002.001', '市南区'], ['8002.01', '平度市'], ['8002.011', '胶南市'], ['8002.012', '莱西市'], ['8002.002', '市北区'], ['8002.003', '四方区'], ['8002.004', '黄岛区'], ['8002.005', '崂山区'], ['8002.006', '李沧区'], ['8002.007', '城阳区'], ['8002.008', '胶州市'], ['8002.009', '即墨市']]

        for i in city_list:
            if i[1] in addr:
                return float(i[0])
        return 8002

if __name__ == '__main__':
    import traceback, os
    try:
        jl = alashan_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
        if 'pop from empty list'!=str(e):
            print('报错')
            traceback.print_exc()
            with open('../error_name.txt', 'a+', encoding='utf-8')as f:
                f.write(str(os.path.basename(__file__)))
                f.write('\n')
                f.write(str(traceback.format_exc()))
                f.write('\n')
        else:
            with open('../success.txt', 'a+', encoding='utf-8')as f:
                f.write(str(os.path.basename(__file__)))
                f.write('\n')
                f.write(str('无连接抓取'))
                f.write('\n')

