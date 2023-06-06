# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 桂林市公共资源交易中心
class wenshan_ggzy:
    def __init__(self):
        self.domain_name = 'http://glggzy.org.cn'
        self.url_list = [
            'http://glggzy.org.cn/gxglzbw/jyxx/001001/001001001/?Paging={}',
            'http://glggzy.org.cn/gxglzbw/jyxx/001001/001001002/?Paging={}',
            'http://glggzy.org.cn/gxglzbw/jyxx/001001/001001004/?Paging={}',
            'http://glggzy.org.cn/gxglzbw/jyxx/001001/001001006/?Paging={}',#中标公告
            'http://glggzy.org.cn/gxglzbw/jyxx/001001/001001007/?Paging={}',#候选人
            'http://glggzy.org.cn/gxglzbw/jyxx/001001/001001008/?Paging={}',#结果

            'http://glggzy.org.cn/gxglzbw/jyxx/001004/001004001/?Paging={}',
            'http://glggzy.org.cn/gxglzbw/jyxx/001004/001004002/?Paging={}',#中标公告
            'http://glggzy.org.cn/gxglzbw/jyxx/001004/001004005/?Paging={}',#结果
            'http://glggzy.org.cn/gxglzbw/jyxx/001004/001004006/?Paging={}'
        ]
        self.url = self.url_list.pop(0)
        self.headers = {
            # 'Accept': 'application/json, text/javascript, */*; q=0.01',
            # 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Cookie': 'ASP.NET_SessionId=35z2fvq5lvv2beeme22crjin; __CSRFCOOKIE=b36f48c6-fa2d-4882-bd90-6012bef4acb3',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',

        }

    def parse(self):
        date = tool.date
        # date = '2020-09-25'
        page = 0
        while True:
            page += 1
            text = tool.requests_get(self.url.format(page), self.headers)
            html = HTML(text)
            print('*' * 20, page, '*' * 20)
            # print(11, text.replace('\ufffd', ' ').replace('\u30fb', ' '))
            # time.sleep(6666)
            detail = html.xpath('//*[@id="right"]/ul/li')
            for li in detail:
                title = li.xpath('./div/a/@title')[0].replace('\xa0', '').replace('\n', ''). \
                    replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
                url = li.xpath('./div/a/@href')[0]
                date_Today = li.xpath('./span/text()')[0].replace('\xa0', '').replace('\n', ''). \
                    replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '') \
                    .replace('[', '').replace(']', '').replace('/', '-')
                if 'http' not in url:
                    url = self.domain_name + url
                # print(title, url, date_Today)
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
                self.url = self.url_list.pop(0)
                break

    def parse_detile(self, title, url, date):
        print(url)
        t = tool.requests_get(url, self.headers).replace('\xa9', '').replace('<br>&nbsp;&nbsp;', '')
        # print(t)
        # time.sleep(2222)
        url_html = etree.HTML(t)
        try:
            detail = url_html.xpath('//*[@id="TDContent"]')[0]
        except:
            return
        detail_html = etree.tostring(detail, method='HTML')
        detail_html = html.unescape(detail_html.decode()).replace("display: none", '')
        detail_text = url_html.xpath('string(//*[@id="TDContent"])').replace('\xa0', '').replace('\n',

                                                                                                     ''). \
            replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
        if len(detail_html) < 200:
            int('a')
        item = {}
        item['title'] = title.replace('\u2022', '')
        item['url'] = url
        item['date'] = date
        item['typeid'] = tool.get_typeid(item['title'])
        item['senddate'] = int(time.time())
        item['mid'] = 867
        item['nativeplace'] = self.get_nativeplace(item['title'])
        item['infotype'] = tool.get_infotype(item['title'])
        item['body'] = tool.qudiao_width(detail_html)
        # item['body'] = tool.update_img(self.domain_name, item['body'])
        # d = re.findall('<div class="news-article-info">.*?</div>', item['body'], re.S)
        # if len(d) != 0:
        #     item['body'] = item['body'].replace(d[0], '').replace('\xa0', '')
        # print(item['body'])
        # time.sleep(2222)
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
        item['resource'] = '桂林市公共资源交易中心'
        item['shi'] = 10503
        item['sheng'] = 10500
        item['removal']= title
        process_item(item)

    def get_nativeplace(self, addr):
        city = ''
        city_list = [['10503.001', '秀峰区'], ['10503.01', '兴安县'], ['10503.011', '永福县'], ['10503.012', '灌阳县'], ['10503.013', '龙胜各族自治县'], ['10503.014', '资源县'], ['10503.015', '平乐县'], ['10503.016', '荔蒲县'], ['10503.017', '恭城瑶族自治县'], ['10503.002', '叠彩区'], ['10503.003', '象山区'], ['10503.004', '七星区'], ['10503.005', '雁山区'], ['10503.006', '阳朔县'], ['10503.007', '临桂县'], ['10503.008', '灵川县'], ['10503.009', '全州县']]

        for i in city_list:
            if i[1] in addr:
                city = float(i[0])
                break
        if city == '':
            city = 10503
        return city

if __name__ == '__main__':
    import traceback,os
    try:
        jl = wenshan_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
        tool.send_error('报错文件：'+str(os.path.basename(__file__))+'报错信息：'+str(e))


