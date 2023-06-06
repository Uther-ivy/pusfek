# -*- coding: utf-8 -*-
import json
import re
import time, html
import traceback
from selenium import webdriver
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 宁夏政府采购网
class xinyang_ggzy:
    def __init__(self):
        self.url_list = [
            'http://www.ccgp-ningxia.gov.cn/site/InteractionQuestion_findVNotice.do?type=&date=&page={}&regionId=640000&tab=Q&dateq1=&dateq2=&keyword=&authCode='
        ]
        self.url = self.url_list.pop(0)
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
            # 'Cookie': 'Hm_lvt_9f8bda7a6bb3d1d7a9c7196bfed609b5=1599470991; JSESSIONID=43A6BC1727D4599F0C3A3EB15DB5D71E; SERVERID=774344e5cd57d247cbf64415edf9f183|1600242924|1600242442'
            'Cookie': 'JJSESSIONID=4B7D634FEF88231B8AC71FF97C577072; SERVERID=a9266b1ad8740cb3434c0066781eae59|1624502596|1624502592'
        }

    # 列表页 需刷新下页面 才可能会出现数据
    def selenium_get(self, url):
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--disable-infobars')
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        options.add_argument(
            '--user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"')
        driver = webdriver.Chrome(options=options)
        driver.get(url)
        while True:
            time.sleep(5)
            if 'reload' in driver.page_source:
                driver.refresh()
            else:
                break
        text = driver.page_source
        driver.close()
        return text

    def parse(self):
        date = tool.date
        page = 0
        while True:
            page += 1
            if page == 30:
                self.url = self.url_list.pop(0)
                page = 0
            text = self.selenium_get(self.url.format(page))
            if 'reload' in text:
                print('reload')
                time.sleep(5)
                page -= 1
                continue
            detail = re.findall("noticeId.*?}", text, re.S)
            for li in detail:
                li = json.loads('{"' + li.replace('\\', '').replace('&amp;', '&'))
                title = li['name']
                # http://www.ccgp-ningxia.gov.cn/public/NXGPPNEW/dynamic/contents/HTGS/content.jsp?id=2c9fd38e7a3853b3017a3bc120601221&cid=308&sid=1
                url = 'http://www.ccgp-ningxia.gov.cn/public/NXGPPNEW/dynamic/{}'.format(li['url'])
                date_Today = li['date'].replace('\n', '').replace('\r', '') \
                    .replace('\t', '').replace(' ', '')
                if '测试' in title:
                    continue
                # print(title, url, date_Today)
                # time.sleep(2222)
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

    def parse_detile(self, title, url, date):
        print(url)
        t = tool.requests_get(url, self.headers)
        url_html = etree.HTML(t)
        try:
            detail = url_html.xpath('//*[@id="form"]')[0]
            detail_html = etree.tostring(detail, method='HTML')
            detail_html = html.unescape(detail_html.decode()).replace('\xa0', '').replace('\ufeff', '')
            detail_text = url_html.xpath('string(//*[@id="form"])') \
                .replace('\xa0', '').replace('\n', '').replace('\r', '').replace('\t', '') \
                .replace(' ', '').replace('\xa5', '').replace('\ufeff', '')
        except:
            detail = url_html.xpath('//*[@id="createForm"]')[0]
            detail_html = etree.tostring(detail, method='HTML')
            detail_html = html.unescape(detail_html.decode()).replace('\xa0', '').replace('\ufeff', '')
            detail_text = url_html.xpath('string(//*[@id="createForm"])') \
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
        item['resource'] = '宁夏政府采购网'
        item["shi"] = int(str(item["nativeplace"]).split('.')[0])
        item['sheng'] = 15500
        item['removal']= title
        process_item(item)

    def get_nativeplace(self, addr):
        city = ''
        city_list = [['15501', '银川'], ['15501.001', '兴庆'], ['15501.002', '西夏'], ['15501.003', '金凤'], ['15501.004', '永宁'], ['15501.005', '贺兰'], ['15501.006', '灵武'], ['15502', '石嘴山'], ['15502.001', '大武口'], ['15502.002', '惠农'], ['15502.003', '平罗'], ['15503', '吴忠'], ['15503.001', '利通'], ['15503.002', '盐池'], ['15503.003', '同心'], ['15503.004', '青铜峡'], ['15503.005', '红寺堡'], ['15504', '固原'], ['15504.001', '原州'], ['15504.002', '西吉'], ['15504.003', '隆德'], ['15504.004', '泾源'], ['15504.005', '彭阳'], ['15505', '中卫'], ['15505.001', '沙坡头'], ['15505.002', '中宁']]

        for i in city_list:
            if i[1] in addr:
                city = float(i[0])
                break
        if city == '':
            city = 15500
        return city

if __name__ == '__main__':
    import traceback,os
    try:
        jl = xinyang_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
        # tool.send_error('报错文件：'+str(os.path.basename(__file__))+'报错信息：'+str(e))



