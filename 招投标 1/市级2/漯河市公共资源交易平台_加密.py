# -*- coding: utf-8 -*-
import time, html,re
import requests
from selenium import webdriver
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 漯河市公共资源交易平台  cookies加密
class luohe_ggzy:
    def __init__(self):
        self.url_list = [
            'https://www.lhjs.cn/Content/jyxx?pageIndex={}'
        ]
        self.url = self.url_list.pop(0)
        self.headers = {
            'Cookie': 'RiMl8hYUlmQHqb9https=K6pgKXEv9hE2V19CESoB0nnj6RAig9STjfEYEIns31lH_BpDuUeNNomO45XE1UjtH8ev_1jHdDLUtI31O_DOmu7UAqdORhRKMmJZZbmUQ80r3',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        }

    def selenium_get(self, url, code):
        options = webdriver.ChromeOptions()
        # options.add_argument('--headless')
        options.add_argument('--disable-infobars')
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        options.add_argument(
            '--user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"')
        driver = webdriver.Chrome(options=options)
        driver.get(url)
        time.sleep(5)
        if code == 0:
            cookie = ''
            for i in driver.get_cookies():
                cookie = cookie + i['name'] + '=' + i['value'] + ';'
            driver.close()
            return cookie
        else:
            text = driver.page_source
            driver.close()
            return text

    def parse(self):
        date = tool.date
        # date = '2021-08-02'
        coo = self.selenium_get(self.url.format(1), 0)
        self.headers['Cookie'] = coo[:-1]
        page = 0
        while True:
            page += 1
            text = tool.requests_get(self.url.format(page), self.headers)
            print('*' * 20, page, '*' * 20)
            html = HTML(text)
            detail = html.xpath('//*[@class="filter-content"]/ul/li')
            for li in detail:
                title = li.xpath('./a/@title')[0]
                url = 'https://www.lhjs.cn' + li.xpath('./a/@href')[0]
                date_Today = li.xpath('./a/span[1]/span[3]/text()')[0].replace('\r', '').replace('\t', '')\
                    .replace(' ', '').replace('\n', '').replace('发布时间：', '').replace('/', '-')
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
        if 'jsgc' in self.url:
            if 'zbgg' in self.url:
                xpath = '//*[@id="TabContent"]/ul/li[1]/div[2]'
            elif 'bggg' in self.url:
                xpath = '//*[@id="TabContent"]/ul/li[2]/div'
            elif 'kbqk' in self.url:
                xpath = '//*[@id="TabContent"]/ul/li[3]/div'
            elif 'zbhxrgs' in self.url:
                xpath = '//*[@id="TabContent"]/ul/li[4]/div'
            elif 'zbjggg' in self.url:
                xpath = '//*[@id="TabContent"]/ul/li[5]/div'
        elif 'zfcg' in self.url:
            if 'cggg' in self.url:
                xpath = '//*[@id="TabContent"]/ul/li[2]/div[2]'
            elif 'bggg' in self.url:
                xpath = '//*[@id="TabContent"]/ul/li[3]/div'
            elif 'zbjggg' in self.url:
                xpath = '//*[@id="TabContent"]/ul/li[5]/div'
        url_html = etree.HTML(tool.requests_get(url, self.headers))
        try:
            detail = url_html.xpath(xpath)[0]
            detail_html = etree.tostring(detail, method='HTML')
            detail_html = html.unescape(detail_html.decode()).replace('\xa0', '').replace('\ufeff', '')
            detail_text = url_html.xpath('string({})'.format(xpath)) \
                .replace('\xa0', '').replace('\n', '').replace('\r', '').replace('\t', '') \
                .replace(' ', '').replace('\xa5', '').replace('\ufeff', '')
        except:
            detail = url_html.xpath('/html/body/div[2]/div[3]/div[2]')[0]
            detail_html = etree.tostring(detail, method='HTML')
            detail_html = html.unescape(detail_html.decode()).replace('\xa0', '').replace('\ufeff', '')
            detail_text = url_html.xpath('string(/html/body/div[2]/div[3]/div[2])') \
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
        item['address'] = tool.get_address(detail_text)
        item['linkman'] = tool.get_linkman(detail_text)
        item['function'] = tool.get_function(detail_text)
        item['resource'] = '漯河市公共资源交易平台'
        item['shi'] = 8511
        item['sheng'] = 8500
        item['removal']= title
        process_item(item)
        # print(item['body'])

    def get_nativeplace(self, addr):
        city = ''
        city_list = [['8511.001', '源汇区'], ['8511.002', '郾城区'], ['8511.003', '召陵区'], ['8511.004', '舞阳县'],
                     ['8511.005', '临颍县']]
        for i in city_list:
            if i[1] in addr:
                city = float(i[0])
                break
        if city == '':
            city = 8511
        return city


if __name__ == '__main__':
    import traceback, os
    try:
        jl = luohe_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
        tool.send_error('报错文件：'+str(os.path.basename(__file__))+'报错信息：'+str(e))


