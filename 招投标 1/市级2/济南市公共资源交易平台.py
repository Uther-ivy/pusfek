# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 济南市公共资源交易平台
class jinan_ggzy:
    def __init__(self):
        self.url_list = [
            # 市本级
            #   工程建设
            #       招标公告
            'http://jnggzy.jinan.gov.cn/jnggzyztb/front/search.do?area=&type=0&xuanxiang=%E6%8B%9B%E6%A0%87%E5%85%AC%E5%91%8A&subheading=&pagenum={}',
            #       中标公示
            'http://jnggzy.jinan.gov.cn/jnggzyztb/front/search.do?area=&type=0&xuanxiang=%E4%B8%AD%E6%A0%87%E5%85%AC%E5%91%8A&subheading=&pagenum={}',
            #   政府采购
            #       采购公告
            'http://jnggzy.jinan.gov.cn/jnggzyztb/front/search.do?area=&type=1&xuanxiang=%E6%8B%9B%E6%A0%87%E5%85%AC%E5%91%8A&subheading=&pagenum={}',
            #       中标公告
            'http://jnggzy.jinan.gov.cn/jnggzyztb/front/search.do?area=&type=1&xuanxiang=%E4%B8%AD%E6%A0%87%E5%85%AC%E5%91%8A&subheading=&pagenum={}',
            #       变更公告
            'http://jnggzy.jinan.gov.cn/jnggzyztb/front/search.do?area=&type=1&xuanxiang=%E5%8F%98%E6%9B%B4%E5%85%AC%E5%91%8A&subheading=&pagenum={}',
            #       废标公示
            'http://jnggzy.jinan.gov.cn/jnggzyztb/front/search.do?area=&type=1&xuanxiang=%E5%BA%9F%E6%A0%87%E5%85%AC%E5%91%8A&subheading=&pagenum={}'
        ]
        self.url = self.url_list.pop(0)
        self.headers = {
            'Cookie': 'ASP.NET_SessionId=sgciv2y0q2cmcycy1o5nsnep; _gscu_381646434=86586121w36f2x70; _gscbrs_381646434=1; _gscs_381646434=t86591829gen3ym70|pv:8',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        }

    def parse(self):
        date = tool.date
        # date = '2020-04-10'
        page = 0
        while True:
            page += 1
            text = tool.requests_get(self.url.format(page), self.headers)
            print('*' * 20, page, '*' * 20)
            text = json.loads(text)['params']['str']
            html = HTML(text)
            # print(11, text)
            # time.sleep(6666)
            detail = html.xpath('//ul/li')
            for li in detail:
                title = li.xpath('./a/@title')[0]
                try:
                    url = 'http://jnggzy.jinan.gov.cn/jnggzyztb/front/showNotice.do?iid=' + li.xpath('./a/@onclick')[0].replace("showview('",
                        '').replace("',1)", '').replace("',1,'招标公告')", '') + '&xuanxiang=' + re.findall('xuanxiang=(.*?)&subheading', self.url)[0] + '&isnew=1'
                except:
                    url = 'http://jnggzy.jinan.gov.cn' + li.xpath('./a/@href')[0]
                try:
                    date_Today = li.xpath('./span[2]/text()')[0].replace('\n', '').replace('\r', '')\
                        .replace('\t', '').replace(' ', '').replace('[', '').replace(']', '')
                except:
                    date_Today = li.xpath('./span[2]/span[2]/text()')[0].replace('\n', '').replace('\r', '') \
                        .replace('\t', '').replace(' ', '').replace('[', '').replace(']', '')
                if '测试' in title:
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
        detail = url_html.xpath('//*[@class="main"]/div')[0]
        detail_html = etree.tostring(detail, method='HTML')
        detail_html = html.unescape(detail_html.decode())
        detail_text = url_html.xpath('string(//*[@class="main"]/div)').replace('\xa0', '').replace(
            '\n', ''). \
            replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
        # print(detail_text.replace('\xa0','').replace('\xa5',''))
        # time.sleep(6666)
        if len(detail_text) < 100:
            return ''
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
        try:
            item['body'] = item['body'].replace(re.findall('<div class="close".*?</div>', item['body'], re.S)[0], '')\
                .replace('\xa0', '')
        except:
            pass
        # tr_list = re.findall('<td.*?>', item['body'])
        # for i in tr_list:
        #     j = i[:-1] + '; colspan="2"; align="center"; height="30">'
        #     item['body'] = item['body'].replace(i, j)
        # print(item['body'])
        # time.sleep(6666)
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
        item['resource'] = '济南市公共资源交易网'
        item['shi'] = 8001
        item['sheng'] = 8000
        item['removal']= title
        process_item(item)

    def get_nativeplace(self, addr):
        city = ''
        city_list = [['8001.001', '历下区'], ['8001.01', '章丘市'], ['8001.002', '市中区'], ['8001.003', '槐荫区'], ['8001.004', '天桥区'], ['8001.005', '历城区'], ['8001.006', '长清区'], ['8001.007', '平阴县'], ['8001.008', '济阳县'], ['8001.009', '商河县']]
        for i in city_list:
            if i[1] in addr:
                city = float(i[0])
                break
        if city == '':
            city = 8001
        return city

if __name__ == '__main__':

    import traceback, os
    try:
        jl = jinan_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
        tool.send_error('报错文件：'+str(os.path.basename(__file__))+'报错信息：'+str(e))


