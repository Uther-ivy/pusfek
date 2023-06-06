# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 朔州市公共资源交易信息网
class shuozhou_ggzy:
    def __init__(self):
        self.url_list = [
            'http://szggzy.shuozhou.gov.cn/moreInfoController.do?getMoreNoticeInfo&page={}&rows=10&dateFlag=&tableName=&projectRegion=&projectName=&beginReceivetime=&endReceivetime=',
            'http://szggzy.shuozhou.gov.cn/moreInfoController.do?getMoreResultNoticeInfo&page={}&rows=10&dateFlag=&tableName=&projectRegion=&projectName=&beginReceivetime=&endReceivetime='
        ]
        self.url = self.url_list.pop(0)
        self.headers = {
            'Cookie': 'JSESSIONID=237CC674F4F73C7E6F6922E8B16BDC0F; _gscu_1040449577=79487932kc82we45; _gscbrs_1040449577=1; _gscs_1040449577=794879320ckx4t45|pv:5',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        }

    def parse(self):
        date = tool.date
        # date = '2020-01-17'
        page = 0
        while True:
            page += 1
            text = tool.requests_get(self.url.format(page), self.headers)
            print('*' * 20, page, '*' * 20)
            # print(11, text)
            # time.sleep(6666)
            detail = json.loads(text)['obj']
            for li in detail:
                try:
                    title = li['PROJECTNAME']
                except:
                    title = li['PROJECT_NAME']
                try:
                    if 'noticeDetail' in li['HTTP_URL']:
                        code = 'getNoticeDetail'
                    else:
                        code = 'getResultNoticeDetail'
                except:
                    if 'noticeDetail' in li['HTTPURL']:
                        code = 'getNoticeDetail'
                    else:
                        code = 'getResultNoticeDetail'
                url = 'http://szggzy.shuozhou.gov.cn/moreInfoController.do?{}&url={}&id={}'.format(code, li['URL'], li['ID'])
                try:
                    date_Today = li['RECEIVETIME']
                except:
                    date_Today = tool.Time_stamp_to_date(int(str(li['RECEIVE_TIME'])[:-3]))
                # print(title, url, date_Today)
                # time.sleep(666)
                if tool.Transformation(date) <= tool.Transformation(date_Today):
                    if tool.removal(title, date):
                        self.parse_detile(title, url, date_Today)
                    else:
                        print('【existence】', url)
                        continue
                else:
                    print('日期不符, 正在切换类型...', date_Today)

                    return
            if page == 20:
                self.url = self.url_list.pop(0)
                break

    def parse_detile(self, title, url, date):
        print(url)
        url_html = etree.HTML(tool.requests_get(url, self.headers))
        detail = url_html.xpath('/html/body/div[3]/div[2]/div[3]')[0]
        detail_html = etree.tostring(detail, method='HTML')
        detail_html = html.unescape(detail_html.decode())
        detail_text = url_html.xpath('string(/html/body/div[3]/div[2]/div[3])').replace('\xa0', '').replace('\n', '').\
            replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
        # print(detail_text.replace('\xa0','').replace('\xa5',''))
        # time.sleep(6666)
        item = {}
        item['title'] = title.replace('\u2022', '')
        item['url'] = url
        item['date'] = date
        item['typeid'] = tool.get_typeid(item['title'])
        item['senddate'] = int(time.time())
        item['mid'] = 867
        item['nativeplace'] = self.get_nativeplace(item['title'])
        item['infotype'] = tool.get_infotype(item['title'])
        item['body'] = detail_html
        width_list = re.findall('width="(.*?)"', item["body"])
        for i in width_list:
            item["body"] = item["body"].replace('width="{}"'.format(i), '')
        width_list = re.findall('WIDTH: (.*?)pt;', item["body"])
        for i in width_list:
            item["body"] = item["body"].replace('WIDTH: {}pt;'.format(i), '')
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
        item['resource'] = '朔州市公共资源交易信息网'
        item['shi'] = 2506
        item['sheng'] = 2500
        item['removal']= title
        process_item(item)

    def get_nativeplace(self, addr):
        city = ''
        city_list = [['2506.001', '朔城区'], ['2506.002', '平鲁区'], ['2506.003', '山阴县'], ['2506.004', '应县'],
                     ['2506.005', '右玉县'], ['2506.006', '怀仁县']]
        for i in city_list:
            if i[1] in addr:
                city = float(i[0])
                break
        if city == '':
            city = 2506
        return city
if __name__ == '__main__':
    import traceback, os
    try:
        jl = shuozhou_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
        tool.send_error('报错文件：'+str(os.path.basename(__file__))+'报错信息：'+str(e))


