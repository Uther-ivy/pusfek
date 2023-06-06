# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 湖南公共资源交易网
class xinyang_ggzy:
    def __init__(self):
        self.url_list = ['https://www.hnsggzy.com/jygk/{}.jhtml',
                         'https://www.hnsggzy.com/jygkzfcg/{}.jhtml']
        self.url = self.url_list.pop(0)
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
            # 'Cookie': 'JSESSIONID=Jhs7fR6dYN1sfp2nr6qwFFyJzQGyyxJY4DbWnkT0FvTx1DR6hH3y!-1581166878'
        }

    def parse(self):
        # print(headers)
        # time.sleep(6666)
        date = tool.date
        # date = '2020-07-10'
        page = 0
        while True:
            page += 1
            if page == 1:
                text = tool.requests_get(self.url.format('index'), self.headers)
            else:
                text = tool.requests_get(self.url.format('index_' + str(page)), self.headers)
            # print(text)
            # time.sleep(6666)
            detail = HTML(text).xpath('//*[@class="article-list2"]/li')
            print('*' * 20, page, '*' * 20)
            for tr in detail:
                title = tr.xpath('string(./div[1]/a)')
                date_Today = tr.xpath('./div[1]/div/text()')[0]
                url = tr.xpath('./div[1]/a/@href')[0]
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
        url_html = etree.HTML(tool.requests_get(url, self.headers))
        try:
            detail = url_html.xpath('//*[@class="div-article2"]')[0]
            detail_html = etree.tostring(detail, method='HTML')
            detail_html = html.unescape(detail_html.decode()).replace('\xa0', '').replace('\ufeff', '')
            detail_text = url_html.xpath('string(//*[@class="div-article2"])') \
                .replace('\xa0', '').replace('\n', '').replace('\r', '').replace('\t', '') \
                .replace(' ', '').replace('\xa5', '').replace('\ufeff', '')
        except:
            detail = url_html.xpath('//*[@class="content-article"]')[0]
            detail_html = etree.tostring(detail, method='HTML')
            detail_html = html.unescape(detail_html.decode()).replace('\xa0', '').replace('\ufeff', '')
            detail_text = url_html.xpath('string(//*[@class="content-article"])') \
                .replace('\xa0', '').replace('\n', '').replace('\r', '').replace('\t', '') \
                .replace(' ', '').replace('\xa5', '').replace('\ufeff', '')
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
        item['resource'] = '湖南公共资源交易网'
        item["shi"] = int(str(item["nativeplace"]).split('.')[0])
        item['sheng'] = 9500
        item['removal']= title
        process_item(item)
        # print(item['body'])

    def get_nativeplace(self, addr):
        city = ''
        city_list = [['9501', '长沙'], ['9501.001', '芙蓉'], ['9501.002', '天心'], ['9501.003', '岳麓'], ['9501.004', '开福'], ['9501.005', '雨花'], ['9501.006', '长沙'], ['9501.007', '望城'], ['9501.008', '宁乡'], ['9501.009', '浏阳'], ['9502', '株洲'], ['9502.001', '荷塘'], ['9502.002', '芦淞'], ['9502.003', '石峰'], ['9502.004', '天元'], ['9502.005', '株洲'], ['9502.006', '攸'], ['9502.007', '茶陵'], ['9502.008', '炎陵'], ['9502.009', '醴陵'], ['9503', '湘潭'], ['9503.001', '雨湖'], ['9503.002', '岳塘'], ['9503.003', '湘潭'], ['9503.004', '湘乡'], ['9503.005', '韶山'], ['9504', '衡阳'], ['9504.001', '珠晖'], ['9504.01', '祁东'], ['9504.011', '耒阳'], ['9504.012', '常宁'], ['9504.002', '雁峰'], ['9504.003', '石鼓'], ['9504.004', '蒸湘'], ['9504.005', '南岳'], ['9504.006', '衡阳'], ['9504.007', '衡南'], ['9504.008', '衡山'], ['9504.009', '衡东'], ['9505', '邵阳'], ['9505.001', '双清'], ['9505.01', '新宁'], ['9505.011', '城步苗族自治'], ['9505.012', '武冈'], ['9505.002', '大祥'], ['9505.003', '北塔'], ['9505.004', '邵东'], ['9505.005', '新邵'], ['9505.006', '邵阳'], ['9505.007', '隆回'], ['9505.008', '洞口'], ['9505.009', '绥宁'], ['9506', '岳阳'], ['9506.001', '岳阳楼'], ['9506.002', '云溪'], ['9506.003', '君山'], ['9506.004', '岳阳'], ['9506.005', '华容'], ['9506.006', '湘阴'], ['9506.007', '平江'], ['9506.008', '汨罗'], ['9506.009', '临湘'], ['9507', '常德'], ['9507.001', '武陵'], ['9507.002', '鼎城'], ['9507.003', '安乡'], ['9507.004', '汉寿'], ['9507.005', '澧'], ['9507.006', '临澧'], ['9507.007', '桃源'], ['9507.008', '石门'], ['9507.009', '津'], ['9508', '张家界'], ['9508.001', '永定'], ['9508.002', '武陵源'], ['9508.003', '慈利'], ['9508.004', '桑植'], ['9509', '益阳'], ['9509.001', '资阳'], ['9509.002', '赫山'], ['9509.003', '南'], ['9509.004', '桃江'], ['9509.005', '安化'], ['9509.006', '沅江'], ['9510', '郴州'], ['9510.001', '北湖'], ['9510.01', '安仁'], ['9510.011', '资兴'], ['9510.002', '苏仙'], ['9510.003', '桂阳'], ['9510.004', '宜章'], ['9510.005', '永兴'], ['9510.006', '嘉禾'], ['9510.007', '临武'], ['9510.008', '汝城'], ['9510.009', '桂东'], ['9511', '永州'], ['9511.001', '芝山'], ['9511.01', '新田'], ['9511.011', '江华瑶族自治'], ['9511.002', '冷水滩'], ['9511.003', '祁阳'], ['9511.004', '东安'], ['9511.005', '双牌'], ['9511.006', '道'], ['9511.007', '江永'], ['9511.008', '宁远'], ['9511.009', '蓝山'], ['9512', '怀化'], ['9512.001', '鹤城'], ['9512.01', '靖州苗族侗族自治'], ['9512.011', '通道侗族自治'], ['9512.012', '洪江'], ['9512.002', '中方'], ['9512.003', '沅陵'], ['9512.004', '辰溪'], ['9512.005', '溆浦'], ['9512.006', '会同'], ['9512.007', '麻阳苗族自治'], ['9512.008', '新晃侗族自治'], ['9512.009', '芷江侗族自治'], ['9513', '娄底'], ['9513.001', '娄星'], ['9513.002', '双峰'], ['9513.003', '新化'], ['9513.004', '冷水江'], ['9513.005', '涟源'], ['9514', '湘西土家族苗族自治州'], ['9514.001', '吉首'], ['9514.002', '泸溪'], ['9514.003', '凤凰'], ['9514.004', '花垣'], ['9514.005', '保靖'], ['9514.006', '古丈'], ['9514.007', '永顺']]

        for i in city_list:
            if i[1] in addr:
                city = float(i[0])
                break
        if city == '':
            city = 9500
        return city

if __name__ == '__main__':
    import traceback, os
    try:
        jl = xinyang_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
        tool.send_error('报错文件：'+str(os.path.basename(__file__))+'报错信息：'+str(e))


