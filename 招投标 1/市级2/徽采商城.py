# -*- coding: utf-8 -*-
import json
import re
import time, html
from lxml import etree
import tool
from save_database import process_item

# 徽采商城
class alashan_ggzy:
    def __init__(self):
        self.url_code = [
            'http://www.huiemall.com/EpointMallHeFeiService/rest/system/getgonggaolist'
        ]
        self.url = self.url_code.pop(0)
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            # 'Cookie': 'isInitAreaCode=null; _gscu_653689772=78282348u2bs1g18; _gscbrs_653689772=1; UM_distinctid=16f78f570621fa-0e76a94f9f3d2d-e343166-1fa400-16f78f570631fc; _gscs_653689772=t782895054fvlkv12|pv:14; CNZZDATA1260595804=985342442-1578282342-%7C1578291895',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
        }

    def parse(self):
        date = tool.date
        # date = '2021-07-29'
        page = 0
        while True:
            page += 1
            try:
                data = {"keyword":"","page":""+str(page)+"","size":10,"type":"cj","url":"http://www.huiemall.com/HeFei/notice.html?type=cj&page="+str(page)+"&keyword=","referer":"http://www.huiemall.com/HeFei/notice.html?type=cj&page="+str(page)+"&keyword="}
                print('*' * 20, page, '*' * 20)
                text = tool.requests_post_to(self.url, data, self.headers)
                detail = json.loads(text)['userarea']['gonggaolist']
            except Exception as e:
                print('parse', e)
                time.sleep(5)
                page -= 1
                continue
            for li in detail:
                title = li['gonggaotitle'].replace('''<font style='color:#E8583C;'>''', '').replace('''</font>''', '')
                url_data = {
                    "type":"cj",
                    "gonggaoguid":li['gonggaoguid'],
                    "gonggaotype":"undefined",
                    "referer":"http://www.huiemall.com/HeFei/noticedetail.html?type=cj&gonggaoguid={}&gonggaotype=undefined".format(li['gonggaoguid'])
                }
                url = 'http://www.huiemall.com/EpointMallHeFeiService/rest/system/getgonggaodetail'
                date_Today = li['gonggaopubdate'][:10].replace('\r', '').replace('\t', '').replace(' ', '')
                # print(title, url, date_Today)
                # time.sleep(666)
                if tool.Transformation(date) <= tool.Transformation(date_Today):
                    if tool.removal(title, date):
                        self.parse_detile(title, url, date, url_data)
                    else:
                        print('【existence】', url_data['referer'])
                        continue
                else:
                    print('日期不符, 正在切换类型...', date_Today)
                    self.url = self.url_code.pop(0)
                    page = 0
                    break
            if page == 10:
                self.url = self.url_code.pop(0)
                page = 0

    def parse_detile(self, title, url, date, url_data):
        print(url_data['referer'])
        while True:
            try:
                url_text = tool.requests_post_to(url, url_data, self.headers)
                detail_html = json.loads(url_text)['userarea']['detail']['gonggaocontent']
                detail_text = ''.join(re.findall('>(.*?)<', detail_html, re.S)).replace('\xa0', '').replace('\n', '').replace('\r', '').replace('\t',
                                                                                                                          '').replace(
                    ' ', '').replace('\xa5', '')
                break
            except Exception as e:
                print('parse_detile', e)
                time.sleep(5)
                continue
        item = {}
        item['title'] = title.replace('\u2022', '')
        item['url'] = url_data['referer']
        item['date'] = date
        item['typeid'] = tool.get_typeid(item['title'])
        item['senddate'] = int(time.time())
        item['mid'] = 867
        item['nativeplace'] = float(tool.get_title_city(item['title']))
        if item['nativeplace'] == 0:
            item['nativeplace'] = float(tool.more(item['title']+detail_text))
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
        item['resource'] = '徽采商城'
        item["shi"] = int(item["nativeplace"])
        if len(str(item["nativeplace"])) == 4:
            item['sheng'] = int(str(item["nativeplace"])[:2] + '00')
        elif len(str(item["nativeplace"])) == 5:
            item['sheng'] = int(str(item["nativeplace"])[:3] + '00')
        else:
            item['sheng'] = 0
        item['removal']= title
        process_item(item)
        # print(item['nativeplace'], item['title'])

if __name__ == '__main__':
    import traceback, os
    try:
        jl = alashan_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()

