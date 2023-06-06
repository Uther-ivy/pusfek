# -*- coding: utf-8 -*-
import json
import re
import time, html
from lxml import etree
import tool
from save_database import process_item

# 医合网
class alashan_ggzy:
    def __init__(self):
        self.url_code = [
            'http://jyzc.yihewanggpo.com/notice/list-tenderNotices.html?pageNo={}&pageSize=10',
            'http://jyzc.yihewanggpo.com/notice/list-changeNotice.html?pageNo={}&pageSize=10',
            'http://jyzc.yihewanggpo.com/notice/list-resultNotice.html?pageNo={}&pageSize=10',
            'http://jyzc.yihewanggpo.com/notice/list-clarifyNotice.html?pageNo={}&pageSize=10',
            'http://jyzc.yihewanggpo.com/notice/list-abandonedNotice.html?pageNo={}&pageSize=10'
        ]
        self.url = self.url_code.pop(0)
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            # 'Cookie': 'isInitAreaCode=null; _gscu_653689772=78282348u2bs1g18; _gscbrs_653689772=1; UM_distinctid=16f78f570621fa-0e76a94f9f3d2d-e343166-1fa400-16f78f570631fc; _gscs_653689772=t782895054fvlkv12|pv:14; CNZZDATA1260595804=985342442-1578282342-%7C1578291895',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
        }

    def parse(self):
        date = tool.date
        # date = '2021-04-08'
        page = 0
        while True:
            page += 1
            print('*' * 20, page, '*' * 20)
            text = tool.requests_get(self.url.format(page), self.headers)
            # print(111, self.url.format(page), text)
            # time.sleep(6666)
            detail = etree.HTML(text).xpath('/html/body/div/div[2]/div[1]/div[3]/div/div[2]/ul/a')
            for li in detail:
                title = li.xpath('./li/div[2]/p/text()')[0]
                url = 'http://jyzc.yihewanggpo.com' + li.xpath('./@href')[0]
                year = li.xpath('./li/div[1]/text()[3]')[0].replace('\r', '').replace('\t', '')\
                    .replace(' ', '').replace('\n', '').replace('.', '')
                yue = li.xpath('./li/div[1]/text()[2]')[0].replace('\r', '').replace('\t', '') \
                    .replace(' ', '').replace('月', '').replace('\n', '').replace('.', '')
                day = li.xpath('./li/div[1]/h1/text()')[0].replace('\r', '').replace('\t', '') \
                    .replace(' ', '').replace('\n', '').replace('.', '')
                yue_ls = {'一': '01', '二':'02', '三':'03', '四':'04', '五':'05', '六':'06', '七':'07', '八':'08', '九':'09', '十':'10', '十一':'11', '十二':'12'}
                date_Today = year+'-'+ yue_ls[yue] + '-' +day
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
                    self.url = self.url_code.pop(0)
                    page = 0
                    break



    def parse_detile(self, title, url, date):
        print(url)
        url_text = tool.requests_get(url, self.headers)
        url_html = etree.HTML(url_text)
        detail = url_html.xpath('/html/body/div[1]/div[2]/div/div[3]/div/div[2]/div')[0]
        detail_html = etree.tostring(detail, method='HTML')
        detail_html = html.unescape(detail_html.decode()).replace('\xa0', '')
        detail_text = url_html.xpath('string(/html/body/div[1]/div[2]/div/div[3]/div/div[2]/div)').replace('\xa0', '').replace('\n', '').replace('\r', '').replace('\t',
                                                                                                                  '').replace(
            ' ', '').replace('\xa5', '')
        item = {}
        item['title'] = title.replace('\u2022', '')
        item['url'] = url
        item['date'] = date
        item['typeid'] = tool.get_typeid(item['title'])
        item['senddate'] = int(time.time())
        item['mid'] = 867
        item['nativeplace'] = float(tool.get_city(item['title']))
        if item['nativeplace'] == 0:
            item['nativeplace'] = float(tool.more(detail_text))
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
        item['resource'] = '医合网'
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
        if 'pop from empty list'!=str(e):
            print('报错')
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

