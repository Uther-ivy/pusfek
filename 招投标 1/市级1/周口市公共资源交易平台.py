# -*- coding: utf-8 -*-
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 周口市公共资源交易平台
class zhoukoushi_ggzy:
    def __init__(self):
        self.url_list = [
            # 建设工程
            # 招标公告
            'http://jyzx.zhoukou.gov.cn/TPFront/jyxx/002001/002001001/',
            # 变更公告
            'http://jyzx.zhoukou.gov.cn/TPFront/jyxx/002001/002001002/',
            # 中标公告
            'http://jyzx.zhoukou.gov.cn/TPFront/jyxx/002001/002001003/',
            # 政府采购
            # 采购公告
            'http://jyzx.zhoukou.gov.cn/TPFront/jyxx/002002/002002001/',
            # 变更公告
            'http://jyzx.zhoukou.gov.cn/TPFront/jyxx/002002/002002002/',
            # 中标结果
            'http://jyzx.zhoukou.gov.cn/TPFront/jyxx/002002/002002003/',
        ]
        self.url = self.url_list.pop(0)
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        }

    def parse(self):
        date = tool.date
        # date = '2020-01-21'
        page = 0
        while True:
            page += 1
            text = tool.requests_get(self.url, self.headers)
            print('*' * 20, page, '*' * 20)
            html = HTML(text)
            detail = html.xpath('/html/body/div/div[2]/table[2]/tr/td/table/tr/td[3]/table[3]/tr[2]/td/table/tr')
            for tr in detail[1:]:
                for li in tr.xpath('./td/table/tr[2]/td[2]/table/tr'):
                    title = li.xpath('./td[2]/a/@title')[0]
                    url = 'http://jyzx.zhoukou.gov.cn' + li.xpath('./td[2]/a/@href')[0]
                    date_Today = li.xpath('./td[3]/font/text()')[0]
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
                        return



    def parse_detile(self, title, url, date):
        print(url)
        url_html = etree.HTML(tool.requests_get(url, self.headers))
        detail = url_html.xpath('//*[@id="tblInfo"]/tr[3]')[0]
        detail_html = etree.tostring(detail, method='HTML')
        detail_html = html.unescape(detail_html.decode()).replace('\xa0', '').replace('\ufeff', '')
        detail_text = url_html.xpath('string(//*[@id="tblInfo"]/tr[3])') \
            .replace('\xa0', '').replace('\n', '').replace('\r', '').replace('\t', '') \
            .replace(' ', '').replace('\xa5', '').replace('\ufeff', '')
        # print(detail_html.replace('\xa0','').replace('\xa5',''))
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
        item['resource'] = '周口市公共资源交易平台'
        item['shi'] = 8516
        item['sheng'] = 8500
        item['removal']= title
        process_item(item)
        # print(item['body'])

    def get_nativeplace(self, addr):
        city = ''
        city_list = [['8516.001', '川汇区'], ['8516.01', '项城市'], ['8516.002', '扶沟县'], ['8516.003', '西华县'], ['8516.004', '商水县'], ['8516.005', '沈丘县'], ['8516.006', '郸城县'], ['8516.007', '淮阳县'], ['8516.008', '太康县'], ['8516.009', '鹿邑县']]
        for i in city_list:
            if i[1] in addr:
                city = float(i[0])
                break
        if city == '':
            city = 8516
        return city

if __name__ == '__main__':
    import traceback,os
    try:
        jl = zhoukoushi_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
        tool.send_error('报错文件：'+str(os.path.basename(__file__))+'报错信息：'+str(e))



