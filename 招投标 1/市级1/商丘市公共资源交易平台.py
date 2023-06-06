# -*- coding: utf-8 -*-
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 商丘市公共资源交易平台
class shangqiu_ggzy:
    def __init__(self):
        self.url_list = [
            'https://ggzyjy.shangqiu.gov.cn/HNSQ/TradeCenter/ColTableInfo.do?projectName=&date=1month&begin_time=&end_time=&begin_time2=&end_time2=&dealType=Deal_Type1&noticType=1+&area=&huanJie=NOTICE&pageIndex={}',
            'https://ggzyjy.shangqiu.gov.cn/HNSQ/TradeCenter/ColTableInfo.do?projectName=&date=1month&begin_time=&end_time=&begin_time2=&end_time2=&dealType=Deal_Type1&noticType=PUBLICITY&area=&huanJie=NOTICE&pageIndex={}',
            'https://ggzyjy.shangqiu.gov.cn/HNSQ/TradeCenter/ColTableInfo.do?projectName=&date=1month&begin_time=&end_time=&begin_time2=&end_time2=&dealType=Deal_Type1&noticType=RESULT_NOTICE&area=&huanJie=NOTICE&pageIndex={}',
            'https://ggzyjy.shangqiu.gov.cn/HNSQ/TradeCenter/ColTableInfo.do?projectName=&date=1month&begin_time=&end_time=&begin_time2=&end_time2=&dealType=Deal_Type1&noticType=WEB_JY_NOTICE&area=&huanJie=NOTICE&pageIndex={}',
            'https://ggzyjy.shangqiu.gov.cn/HNSQ/TradeCenter/ColTableInfo.do?projectName=&date=1month&begin_time=&end_time=&begin_time2=&end_time2=&dealType=Deal_Type4&noticType=NOTICE&area=&huanJie=NOTICE&pageIndex={}',
            'https://ggzyjy.shangqiu.gov.cn/HNSQ/TradeCenter/ColTableInfo.do?projectName=&date=1month&begin_time=&end_time=&begin_time2=&end_time2=&dealType=Deal_Type4&noticType=RESULT_NOTICE&area=&huanJie=NOTICE&pageIndex={}',
            'https://ggzyjy.shangqiu.gov.cn/HNSQ/TradeCenter/ColTableInfo.do?projectName=&date=1month&begin_time=&end_time=&begin_time2=&end_time2=&dealType=Deal_Type4&noticType=WEB_JY_NOTICE&area=&huanJie=NOTICE&pageIndex={}',
        ]

        self.url = self.url_list.pop(0)
        self.headers = {
            'Cookie': 'JSESSIONID=008A73ECF729ACCCD55326D2CCE9D2EB; JSESSIONID=B227EE91F081C0116EEDC31344A5C3C0; UM_distinctid=1748a3021c536e-03bb6ec16bbda-3f385a04-1fa400-1748a3021c61b6; CNZZDATA1279203355=1342576410-1600045352-null%7C1600045352',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        }

    def parse(self):
        date = tool.date
        # date = '2020-03-20'
        page = 0
        while True:
            page += 1
            text = tool.requests_get(self.url.format(page), self.headers)
            print('*' * 20, page, '*' * 20)
            html = HTML(text)
            detail = html.xpath('//tr')
            for li in detail[1:]:
                title = li.xpath('./td[2]/a/@title')[0]
                url = 'https://ggzyjy.shangqiu.gov.cn/' + li.xpath('./td[2]/a/@href')[0]
                date_Today = li.xpath('./td[3]/span[1]/text()')[0].replace('\n', '').replace(
                    '\t', '') \
                    .replace('\r', '').replace(' ', '').replace('发布时间:', '')
                # print(title, url, date_Today)
                # time.sleep(666)
                if '测试' in title:
                    continue
                if tool.Transformation(date) <= tool.Transformation(date_Today):
                    if tool.removal(title, date):
                        self.parse_detile(title, url, date_Today)
                    else:
                        print('【existence】', url)
                        continue
                else:
                    print('日期不符, 正在切换类型', date_Today)
                    self.url = self.url_list.pop(0)
                    page = 0

                    break

            if page == 20:
                self.url = self.url_list.pop(0)
                break

    def parse_detile(self, title, url, date):
        print(url)
        url_html = etree.HTML(tool.requests_get(url, self.headers))
        detail = url_html.xpath('//*[@id="content-box-id"]')[0]
        detail_html = etree.tostring(detail, method='HTML')
        detail_html = html.unescape(detail_html.decode()).replace('\xa0', '').replace('\ufeff', '')
        detail_text = url_html.xpath('string(//*[@id="content-box-id"])') \
            .replace('\xa0', '').replace('\n', '').replace('\r', '').replace('\t', '') \
            .replace(' ', '').replace('\xa5', '').replace('\ufeff', '')
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
        item['winner'] = tool.get_winner(detail_text)
        item['address'] = tool.get_address(detail_text)
        item['linkman'] = tool.get_linkman(detail_text)
        item['function'] = tool.get_function(detail_text)
        item['resource'] = '商丘市公共资源交易平台'
        item['shi'] = 8514
        item['sheng'] = 8500
        item['removal']= title
        process_item(item)
        # print(item['body'])
    def get_nativeplace(self, addr):
        city = ''
        city_list = [['8514.001', '梁园区'], ['8514.002', '睢阳区'], ['8514.003', '民权县'], ['8514.004', '睢县'], ['8514.005', '宁陵县'], ['8514.006', '柘城县'], ['8514.007', '虞城县'], ['8514.008', '夏邑县'], ['8514.009', '永城']]

        for i in city_list:
            if i[1] in addr:
                city = float(i[0])
                break
        if city == '':
            city = 8514
        return city

if __name__ == '__main__':
    import traceback, os
    try:
        jl = shangqiu_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
        tool.send_error('报错文件：'+str(os.path.basename(__file__))+'报错信息：'+str(e))


