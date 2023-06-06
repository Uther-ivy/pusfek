# -*- coding: utf-8 -*-
import json
import re
import time, html
from lxml import etree
from selenium import webdriver
import tool
from save_database import process_item

# 深圳阳光采购平台
class xinyang_ggzy:
    def __init__(self):
        self.url_list = [
            {"page":1,"rows":15,"xmLeiXing":"","caiGouType":0,"ggLeiXing":1,"isShiShuGuoQi":"","isZhanLueYingJiWuZi":"","keyWords":""},
            {"page": 1, "rows": 15, "xmLeiXing": "", "caiGouType": 0, "ggLeiXing": 2, "isShiShuGuoQi": "",
             "isZhanLueYingJiWuZi": "", "keyWords": ""},
            {"page": 1, "rows": 15, "xmLeiXing": "", "caiGouType": 0, "ggLeiXing": 3, "isShiShuGuoQi": "",
             "isZhanLueYingJiWuZi": "", "keyWords": ""},
            {"page": 1, "rows": 15, "xmLeiXing": "", "caiGouType": 0, "ggLeiXing": 4, "isShiShuGuoQi": "",
             "isZhanLueYingJiWuZi": "", "keyWords": ""},
            {"page": 1, "rows": 15, "xmLeiXing": "", "caiGouType": 0, "ggLeiXing": 5, "isShiShuGuoQi": "",
             "isZhanLueYingJiWuZi": "", "keyWords": ""}
        ]
        self.url = self.url_list.pop(0)
        self.headers = {
            'Accept': 'application/json, text/plain, */*',
            'Content-Type': 'application/json;charset=UTF-8',
            'Host': 'www.szygcgpt.com',
            'Origin': 'https://www.szygcgpt.com',
            'Cookie': 'UM_distinctid=17d279fbc86343-099044dba9bde6-4343363-1fa400-17d279fbc874b9; CNZZDATA1275781810=255059830-1637047317-https%253A%252F%252Fcgpt.sotcbb.com%252F%7C1637047317; aliyungf_tc=f90651b609fcb90b72a6ee3870c2f21fe1d3ee02c2599847c72f13a86e4d2f95; acw_tc=2f6fc12216397133151937361e0cb4941a0f2a5130cebc01da530a2a784f16; SERVERID=8df1eba110a0805071f493f2bfd8ec6a|1639713512|1639713315',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        }

    def parse(self):
        date = tool.date
        # date = '2021-06-11'
        page = 0
        index_url = 'https://www.szygcgpt.com/app/home/pageGGList.do'
        while True:
            page += 1
            self.url['page'] = page
            text = tool.requests_post_to(index_url, self.url, self.headers)
            detail = json.loads(text)['data']['list']
            print('*' * 20, page, '*' * 20)
            for li in detail:
                title = li['ggName']
                if li['ggXingZhi'] == 1:
                    code= 'Purchase'
                elif li['ggXingZhi'] == 2:
                    code = 'Change'
                elif li['ggXingZhi'] == 3:
                    code = 'Candidate'
                elif li['ggXingZhi'] == 4:
                    code = 'Result'
                else:
                    code = 'Invitation'
                url = 'https://www.szygcgpt.com/ygcg/detailTop?ggGuid={}&bdGuid={}&com={}&ggLeiXing={}&dataSource=0'.format(li['ggGuid'], li['bdGuid'],code, li['ggXingZhi'])
                date_Today = li['@timestamp'][:10]
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
                    page=0
                    break


            if page == 20:
                self.url = self.url_list.pop(0)
                break

    def get_html(self, url, num):
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        driver = webdriver.Chrome(options=options)
        driver.get(url)
        time.sleep(num)
        cont = driver.page_source
        driver.quit()
        return cont

    def parse_detile(self, title, url, date):
        print(url)
        try:
            t = self.get_html(url, 3)
            detail = etree.HTML(t)
            detail_html = detail.xpath('//*[@class="contentDetail"]')[0]
            detail_html = etree.tostring(detail_html, method='HTML')
            detail_html = html.unescape(detail_html.decode())
            detail_text = ''.join(re.findall('>(.*?)<', detail_html)).replace('\xa0', '').replace('\n', '').replace('\r', '').replace('\t', '') \
                .replace(' ', '').replace('\xa5', '').replace('\ufeff', '')
        except:
            try:
                t = self.get_html(url, 10)
                detail = etree.HTML(t)
                detail_html = detail.xpath('//*[@class="contentDetail"]')[0]
                detail_html = etree.tostring(detail_html, method='HTML')
                detail_html = html.unescape(detail_html.decode())
                detail_text = ''.join(re.findall('>(.*?)<', detail_html)).replace('\xa0', '').replace('\n', '').replace(
                    '\r', '').replace('\t', '') \
                    .replace(' ', '').replace('\xa5', '').replace('\ufeff', '')
            except:
                return
        # print(detail_text)
        # time.sleep(6666)
        item = {}
        item['title'] = title.replace('\u2022', '')
        item['url'] = url
        item['date'] = date
        item['typeid'] = tool.get_typeid(item['title'])
        item['senddate'] = int(time.time())
        item['mid'] = 867
        item['infotype'] = tool.get_infotype(item['title'])
        item['body'] = tool.qudiao_width(detail_html)
        # print(detail_html)
        # time.sleep(666)
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
        item['nativeplace'] = self.get_nativeplace(title)
        item['linkman'] = tool.get_linkman(detail_text)
        item['function'] = tool.get_function(detail_text)
        item['resource'] = '深圳阳光采购平台'
        item["shi"] = 10003
        item['sheng'] = 10000
        item['removal']= title
        process_item(item)
        # print(item['body'])

    def get_nativeplace(self, addr):
        city = ''
        city_list = [['10003.001', '罗湖区'], ['10003.002', '福田区'], ['10003.003', '南山区'], ['10003.004', '宝安区'], ['10003.005', '龙岗区'], ['10003.006', '盐田区'], ['10003.007', '坪山区']]

        for i in city_list:
            if i[1] in addr:
                city = float(i[0])
                break
        if city == '':
            city = 10003
        return city

if __name__ == '__main__':
    jl = xinyang_ggzy()
    jl.parse()


