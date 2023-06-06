# -*- coding: utf-8 -*-
import json
import re
import time, html
import traceback
import requests
from lxml import etree
from lxml.etree import HTML
from redis import StrictRedis
from selenium import webdriver

import tool
from save_database import process_item

# 四川政府采购
class xinyang_ggzy:
    def __init__(self):
        self.url_list = [
            'http://www.ccgp-fujian.gov.cn/3500/noticelist/e8d2cd51915e4c338dc1c6ee2f02b127/?page=1'
        ]
        self.url = self.url_list.pop(0)
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Cookie': 'sessionid=n5udi68ma06i56095cupaesyuxhnw0df;csrftoken=QgJOedO5a9Zf6e1Jn2DcaCFdbngqSjQ5jYAS34gkvX3eQt9FAFCCnew37kH3Pa2W',
            'Host': 'www.ccgp-fujian.gov.cn',
            'Referer': 'http://www.ccgp-fujian.gov.cn/3500/noticelist/e8d2cd51915e4c338dc1c6ee2f02b127/?csrfmiddlewaretoken=KNgJGDrwrW6E4Ej1DnhbC2hKXhD8PzVadI9R37GM27GTqxwoytJuOUKHSKcY6TYJ&zone_code=&zone_name=&croporgan_name=&project_no=&fromtime=&endtime=&gpmethod=&agency_name=&title=&notice_type=&open_type=&verifycode=%E4%BB%AA%E5%A4%B1%E4%BB%99%E5%8D%B0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
        }

    def process_request(self):
        redisconn = StrictRedis(host='192.168.2.57', db=7, port=6379, password='1214')
        return json.loads(redisconn.get("ip"))['http']

    # 通过selenium 获取cookies
    def selenium_get(self, url):
        proxy = self.process_request().replace('http://', '')
        options = webdriver.ChromeOptions()
        # options.add_argument('--headless')
        options.add_argument('--disable-infobars')
        options.add_argument('--proxy-server=%s' % proxy)
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        options.add_argument(
            '--user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"')
        # options.add_argument(
        #     '--Cookie="Hm_lvt_9f8bda7a6bb3d1d7a9c7196bfed609b5=1599470991; JSESSIONID=43A6BC1727D4599F0C3A3EB15DB5D71E; SERVERID=774344e5cd57d247cbf64415edf9f183|1600242924|1600242442"')
        driver = webdriver.Chrome(options=options)
        driver.maximize_window()
        print(proxy)
        # driver.get('https://www.baidu.com/s?ie=UTF-8&wd=ip')
        # time.sleep(2222)
        driver.get(url)
        num = 20
        for i in range(num):
            print(num-i)
            time.sleep(1)
        cookie = ''
        for i in driver.get_cookies():
            cookie = cookie + i['name'] + '=' + i['value'] + ';'
        driver.quit()
        return cookie

    def parse(self):
        date = tool.date
        # date = '2020-07-10'
        page = 0
        self.headers['Cookie'] = self.selenium_get(self.url.format(page))[:-1]
        # print(self.headers['Cookie'])
        # time.sleep(6666)
        while True:
            page += 1
            text = tool.requests_get(self.url.format(page),self.headers)
            # text.encoding = text.apparent_encoding
            detail = HTML(text).xpath("/html/body/div[2]/div/div/div[3]/div[2]/table/tbody/tr")
            print('*' * 20, page, '*' * 20)
            for li in detail:
                title = li.xpath('./td[4]/a/text()')[0]
                url = 'http://www.ccgp-fujian.gov.cn' + li.xpath("./td[4]/a/@href")[0]
                date_Today = li.xpath("./td[5]/text()")[0].replace('\n',
                                                                                                             '').replace(
                    '\t', '').replace('\r', '').replace(' ', '')
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
            if page == 30:
                self.url = self.url_list.pop(0)
                page = 0


    def parse_detile(self, title, url, date):
        print(url)
        t = tool.requests_get(url, self.headers)
        # print(t)
        # time.sleep(6666)
        url_html = etree.HTML(t)
        detail = url_html.xpath('//*[@id="print-content"]')[0]
        detail_html = etree.tostring(detail, method='HTML')
        detail_html = html.unescape(detail_html.decode()).replace('\xa0', '').replace('\ufeff', '')
        detail_text = url_html.xpath('string(//*[@id="print-content"])') \
            .replace('\xa0', '').replace('\n', '').replace('\r', '').replace('\t', '') \
            .replace(' ', '').replace('\xa5', '').replace('\ufeff', '')
        item = {}
        item['title'] = title.replace('\u2022', '')
        item['url'] = url
        item['date'] = date
        item['typeid'] = tool.get_typeid(item['title'])
        item['senddate'] = int(time.time())
        item['mid'] = 867
        item['infotype'] = tool.get_infotype(item['title'])
        item['body'] = tool.qudiao_width(detail_html)
        # b = re.findall('''<p class="news-article-info">.*?</p>''', item['body'])[0]
        # item['body'] = item['body'].replace(b, '')
        # print(item['body'])
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
        item['address'] = tool.get_address(detail_text)
        item['nativeplace'] = self.get_nativeplace(item['title'])
        item['linkman'] = tool.get_linkman(detail_text)
        item['function'] = tool.get_function(detail_text)
        item['resource'] = '福建政府采购网'
        item["shi"] = int(str(item["nativeplace"]).split('.')[0])
        item['sheng'] = 7000
        item['removal']= title
        process_item(item)
        # print(item['body'])

    def get_nativeplace(self, addr):
        city = ''
        city_list = [['7001', '福州'], ['7001.001', '鼓楼'], ['7001.01', '永泰'], ['7001.011', '平潭'], ['7001.012', '福清'], ['7001.013', '长乐'], ['7001.002', '台江'], ['7001.003', '仓山'], ['7001.004', '马尾'], ['7001.005', '晋安'], ['7001.006', '闽侯'], ['7001.007', '连江'], ['7001.008', '罗源'], ['7001.009', '闽清'], ['7002', '厦门'], ['7002.001', '思明'], ['7002.002', '海沧'], ['7002.003', '湖里'], ['7002.004', '集美'], ['7002.005', '同安'], ['7002.006', '翔安'], ['7003', '莆田'], ['7003.001', '城厢'], ['7003.002', '涵江'], ['7003.003', '荔城'], ['7003.004', '秀屿'], ['7003.005', '仙游'], ['7004', '三明'], ['7004.001', '梅列'], ['7004.01', '泰宁'], ['7004.011', '建宁'], ['7004.012', '永安'], ['7004.002', '三元'], ['7004.003', '明溪'], ['7004.004', '清流'], ['7004.005', '宁化'], ['7004.006', '大田'], ['7004.007', '尤溪'], ['7004.008', '沙'], ['7004.009', '将乐'], ['7005', '泉州'], ['7005.001', '鲤城'], ['7005.01', '石狮'], ['7005.011', '晋江'], ['7005.012', '南安'], ['7005.002', '丰泽'], ['7005.003', '洛江'], ['7005.004', '泉港'], ['7005.005', '惠安'], ['7005.006', '安溪'], ['7005.007', '永春'], ['7005.008', '德化'], ['7005.009', '金门'], ['7006', '漳州'], ['7006.001', '芗城'], ['7006.01', '华安'], ['7006.011', '龙海'], ['7006.002', '龙文'], ['7006.003', '云霄'], ['7006.004', '漳浦'], ['7006.005', '诏安'], ['7006.006', '长泰'], ['7006.007', '东山'], ['7006.008', '南靖'], ['7006.009', '平和'], ['7007', '南平'], ['7007.001', '延平'], ['7007.01', '建阳'], ['7007.002', '顺昌'], ['7007.003', '浦城'], ['7007.004', '光泽'], ['7007.005', '松溪'], ['7007.006', '政和'], ['7007.007', '邵武'], ['7007.008', '武夷山'], ['7007.009', '建瓯'], ['7008', '龙岩'], ['7008.001', '新罗'], ['7008.002', '长汀'], ['7008.003', '永定'], ['7008.004', '上杭'], ['7008.005', '武平'], ['7008.006', '连城'], ['7008.007', '漳平'], ['7009', '宁德'], ['7009.001', '蕉城'], ['7009.002', '霞浦'], ['7009.003', '古田'], ['7009.004', '屏南'], ['7009.005', '寿宁'], ['7009.006', '周宁'], ['7009.007', '柘荣'], ['7009.008', '福安']]

        for i in city_list:
            if i[1] in addr:
                city = float(i[0])
                break
        if city == '':
            city = 7000
        return city

if __name__ == '__main__':
    import traceback, os
    try:
        jl = xinyang_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
        tool.send_error('报错文件：'+str(os.path.basename(__file__))+'报错信息：'+str(e))


