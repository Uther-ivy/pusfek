# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 湖北省政府采购网
class baoshan_ggzy:
    def __init__(self):
        self.url_list = [
            'http://www.ccgp-hubei.gov.cn/contract/sjzfcght/index_{}.html',
            'http://www.ccgp-hubei.gov.cn/contract/cxzfcght/index_{}.html',
            'http://www.ccgp-hubei.gov.cn/notice/cggg/pzbgg/index_{}.html',
            'http://www.ccgp-hubei.gov.cn/notice/cggg/pzhbgg/index_{}.html',
            'http://www.ccgp-hubei.gov.cn/notice/cggg/pgzgg/index_{}.html',
            'http://www.ccgp-hubei.gov.cn/notice/cggg/pfbgg/index_{}.html',
            'http://www.ccgp-hubei.gov.cn/notice/cggg/pdylygg/index_{}.html',
            'http://www.ccgp-hubei.gov.cn/notice/cggg/czgysgg/index_{}.html',
            'http://www.ccgp-hubei.gov.cn/notice/cggg/czbgg/index_{}.html',
            'http://www.ccgp-hubei.gov.cn/notice/cggg/czhbgg/index_{}.html',
            'http://www.ccgp-hubei.gov.cn/notice/cggg/cgzgg/index_{}.html',
            'http://www.ccgp-hubei.gov.cn/notice/cggg/cfbgg/index_{}.html',
            'http://www.ccgp-hubei.gov.cn/notice/cggg/cdylygg/index_{}.html',
            'http://www.ccgp-hubei.gov.cn/notice/cggg/cxqgsgg/index_{}.html',

        ]
        self.url = self.url_list.pop(0)
        self.headers = {
            # 'Cookie': 'homeid=1a444a31-e460-47ff-9931-1c075c0f3cd8',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        }

    def parse(self):
        page = 0
        while True:
            page += 1
            print(self.url,'111')
            date = tool.date
            text = tool.requests_get(url=self.url.format(page), headers=self.headers)
            html = HTML(text)
            detail = html.xpath('//*[@class="news-list list-page"]/ul/li')
            for li in detail:
                url = li.xpath('./a/@href')[0]
                title = li.xpath('./a/text()')[1].strip().replace('\n', '').replace(' ', '')\
                    .replace('\t', '').replace(']', '')
                date_Today = li.xpath('./span/text()')[0]
                if '测试' in title:
                    continue
                url_domain = 'http://www.ccgp-hubei.gov.cn'
                if 'http' not in url:
                    if '../../' in url:
                        url = url_domain + url[5:]
                    elif '../' in url:
                        url = url_domain + url[2:]
                    elif './' in url:
                        url = url_domain + url[1:]
                    else:
                        url = url_domain + url
                # print(title, url, date_Today)
                # time.sleep(666)
                if tool.Transformation(date) <= tool.Transformation(date_Today):
                    if tool.removal(title, date):
                        self.parse_detile(title, url, date_Today)
                    else:
                        print('【existence】', url)
                        # self.url = self.url_list.pop(0)
                        continue
                else:
                    print('日期不符, 正在切换类型', date_Today, self.url)
                    self.url = self.url_list.pop(0)
                    page = 0
                    break
            if page == 5:
                self.url = self.url_list.pop(0)
                page = 0


    def parse_detile(self, title, url, date):
        t = tool.requests_get(url, self.headers)
        url_html = etree.HTML(t)
        detail = url_html.xpath('//div[@style="margin: 0 22px;"]')[0]
        # print(detail)
        detail_html = etree.tostring(detail, method='HTML')
        detail_html = html.unescape(detail_html.decode())
        detail_text = url_html.xpath('string(//div[@style="margin: 0 22px;"])').replace('\xa0', '').replace('\n', ''). \
            replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
        # if len(detail_text) < 100:
        #     return
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
        item['nativeplace'] = self.get_nativeplace(title)
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
        item['resource'] = '湖北省政府采购网'
        if '.' in str(item["nativeplace"]):
            item["shi"] = int(float(str(item["nativeplace"]).replace("['","").split('.')[0]))
        else:
            item["shi"] = int(float(item["nativeplace"]))
        item['sheng'] = 9000
        # print(item)
        item['removal']= title
        process_item(item)

    def get_nativeplace(self, addr):
        city_list = [['9001', '武汉市'], ['9001.001', '江岸区'], ['9001.01', '蔡甸区'], ['9001.011', '江夏区'], ['9001.012', '黄陂区'], ['9001.013', '新洲区'], ['9001.002', '江汉区'], ['9001.003', '乔口区'], ['9001.004', '汉阳区'], ['9001.005', '武昌区'], ['9001.006', '青山区'], ['9001.007', '洪山区'], ['9001.008', '东西湖区'], ['9001.009', '汉南区'], ['9002', '黄石市'], ['9002.001', '黄石港区'], ['9002.002', '西塞山区'], ['9002.003', '下陆区'], ['9002.004', '铁山区'], ['9002.005', '阳新县'], ['9002.006', '大冶市'], ['9003', '十堰市'], ['9003.001', '茅箭区'], ['9003.002', '张湾区'], ['9003.003', '郧县'], ['9003.004', '郧西县'], ['9003.005', '竹山县'], ['9003.006', '竹溪县'], ['9003.007', '房县'], ['9003.008', '丹江口市'], ['9004', '宜昌市'], ['9004.001', '西陵区'], ['9004.01', '五峰土家族自治县'], ['9004.011', '宜都市'], ['9004.012', '当阳市'], ['9004.013', '枝江市'], ['9004.002', '伍家岗区'], ['9004.003', '点军区'], ['9004.004', '?亭区'], ['9004.005', '夷陵区'], ['9004.006', '远安县'], ['9004.007', '兴山县'], ['9004.008', '秭归县'], ['9004.009', '长阳土家族自治县'], ['9005', '襄樊市'], ['9005.001', '襄城区'], ['9005.002', '樊城区'], ['9005.003', '襄阳区'], ['9005.004', '南漳县'], ['9005.005', '谷城县'], ['9005.006', '保康县'], ['9005.007', '老河口市'], ['9005.008', '枣阳市'], ['9005.009', '宜城市'], ['9006', '鄂州市'], ['9006.001', '梁子湖区'], ['9006.002', '华容区'], ['9006.003', '鄂城区'], ['9007', '荆门市'], ['9007.001', '钟祥市'], ['9007.002', '沙洋县'], ['9007.003', '京山县'], ['9007.004', '掇刀区'], ['9007.005', '东宝区'], ['9008', '孝感市'], ['9008.001', '安陆市'], ['9008.002', '应城市'], ['9008.003', '云梦县'], ['9008.004', '大悟县'], ['9008.005', '孝昌县'], ['9008.006', '孝南区'], ['9008.007', '汉川市'], ['9009', '荆州市'], ['9009.001', '沙市区'], ['9009.002', '荆州区'], ['9009.003', '公安县'], ['9009.004', '监利县'], ['9009.005', '江陵县'], ['9009.006', '石首市'], ['9009.007', '洪湖市'], ['9009.008', '松滋市'], ['9010', '黄冈市'], ['9010.001', '州区'], ['9010.01', '武穴市'], ['9010.002', '团风县'], ['9010.003', '红安县'], ['9010.004', '罗田县'], ['9010.005', '英山县'], ['9010.006', '浠水县'], ['9010.007', '蕲春县'], ['9010.008', '黄梅县'], ['9010.009', '麻城市'], ['9011', '咸宁市'], ['9011.001', '咸安区'], ['9011.002', '嘉鱼县'], ['9011.003', '通城县'], ['9011.004', '崇阳县'], ['9011.005', '通山县'], ['9011.006', '赤壁市'], ['9012', '随州市'], ['9012.001', '曾都区'], ['9012.002', '广水市'], ['9013', '恩施土家族苗族自治州'], ['9013.001', '恩施市'], ['9013.002', '利川市'], ['9013.003', '建始县'], ['9013.004', '巴东县'], ['9013.005', '宣恩县'], ['9013.006', '咸丰县'], ['9013.007', '来凤县'], ['9013.008', '鹤峰县'], ['9014', '省直辖行政单位'], ['9014.001', '仙桃市'], ['9014.002', '潜江市'], ['9014.003', '天门市'], ['9014.004', '神农架林区']]
        for i in city_list:
            shi = i[1].replace('市', '')
            if shi in addr:
                return i[0]
        return 9000

if __name__ == '__main__':

    import traceback, os
    try:
        jl = baoshan_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
