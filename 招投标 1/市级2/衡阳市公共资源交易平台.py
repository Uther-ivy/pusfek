# -*- coding: utf-8 -*-
import json
import re
import time, html
from lxml import etree
import tool
from save_database import process_item

# 衡阳市公共资源交易平台
class alashan_ggzy:
    def __init__(self):
        self.url_code = [
            'https://hengyang.hnsggzy.com/gczb/index_{}.jhtml',
            'https://hengyang.hnsggzy.com/jygkzfcg/index_{}.jhtml'
        ]
        self.url = self.url_code.pop(0)
        self.headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Cookie': 'isInitAreaCode=null; _gscu_653689772=78282348u2bs1g18; _gscbrs_653689772=1; UM_distinctid=16f78f570621fa-0e76a94f9f3d2d-e343166-1fa400-16f78f570631fc; _gscs_653689772=t782895054fvlkv12|pv:14; CNZZDATA1260595804=985342442-1578282342-%7C1578291895',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
        }

    def parse(self):
        date = tool.date
        # date = '2021-07-05'
        page = 0
        while True:
            page += 1
            print('*' * 20, page, '*' * 20)
            text = tool.requests_get(self.url.format(page), self.headers)
            # print(111, text)
            # time.sleep(666)
            detail = etree.HTML(text).xpath('//*[@class="article-list2"]/li')
            for li in detail:
                title = li.xpath('string(./div[1]/a)')
                url = li.xpath('./div[1]/a/@href')[0]
                date_Today = li.xpath('./div[1]/div/text()')[0].replace('\r', '').replace('\t', '').replace(' ', '')
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
            if page == 5:
                self.url = self.url_code.pop(0)
                page = 0

    def parse_detile(self, title, url, date):
        print(url)
        url_text = tool.requests_get(url, self.headers)
        url_html = etree.HTML(url_text)
        try:
            detail = url_html.xpath('/html/body/div[4]/div[2]/div[3]/div[2]/table')[0]
            detail_html = etree.tostring(detail, method='HTML')
            detail_html = html.unescape(detail_html.decode())
            detail_text = url_html.xpath('string(/html/body/div[4]/div[2]/div[3]/div[2]/table)').replace('\xa0', '').replace('\n', '').replace('\r', '').replace('\t',
                                                                                                                      '').replace(
                ' ', '').replace('\xa5', '')
        except:
            try:
                detail = url_html.xpath('/html/body/div[4]/div[2]/div[3]/div[3]/table')[0]
                detail_html = etree.tostring(detail, method='HTML')
                detail_html = html.unescape(detail_html.decode())
                detail_text = url_html.xpath('string(/html/body/div[4]/div[2]/div[3]/div[3]/table)').replace('\xa0', '').replace(
                    '\n', '').replace('\r', '').replace('\t',
                                                        '').replace(
                    ' ', '').replace('\xa5', '')
            except:
                return
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
        item['resource'] = '衡阳市公共资源交易平台'
        item['shi'] = 9504
        item['sheng'] = 9500
        item['removal']= title
        process_item(item)
        # print(item['nativeplace'], item['title'])

    def get_nativeplace(self, addr):
        city_list = [['9504.001', '珠晖区'], ['9504.01', '祁东县'], ['9504.011', '耒阳市'], ['9504.012', '常宁市'], ['9504.002', '雁峰区'], ['9504.003', '石鼓区'], ['9504.004', '蒸湘区'], ['9504.005', '南岳区'], ['9504.006', '衡阳县'], ['9504.007', '衡南县'], ['9504.008', '衡山县'], ['9504.009', '衡东县']]

        for i in city_list:
            if i[1] in addr:
                return float(i[0])
        return 9504

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

