# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 广东省招标投标监管网
class xinyang_ggzy:
    def __init__(self):
        self.url_list = [
            'http://zbtb.gd.gov.cn/bid/listZbgcxx?createDate=1&draw=1&columns%5B0%5D%5Bdata%5D=id&columns%5B0%5D%5Bname%5D=&columns%5B0%5D%5Bsearchable%5D=true&columns%5B0%5D%5Borderable%5D=false&columns%5B0%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B0%5D%5Bsearch%5D%5Bregex%5D=false&start=0&length=20&search%5Bvalue%5D=&search%5Bregex%5D=false&page={}&type=&xmmc=&rows=20',
            'http://zbtb.gd.gov.cn/bid/listZbhxrgs?draw=1&columns%5B0%5D%5Bdata%5D=id&columns%5B0%5D%5Bname%5D=&columns%5B0%5D%5Bsearchable%5D=true&columns%5B0%5D%5Borderable%5D=false&columns%5B0%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B0%5D%5Bsearch%5D%5Bregex%5D=false&start=0&length=20&search%5Bvalue%5D=&search%5Bregex%5D=false&page={}&type=zbhxrgs&xmmc=&rows=20'
        ]
        self.url = self.url_list.pop(0)
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        }

    def parse(self):
        date = tool.date
        # date = '2020-07-06'
        page = 0
        while True:
            page += 1
            text = tool.requests_get(self.url.format(page), self.headers)
            # print(text)
            # time.sleep(666)
            print('*' * 20, page, '*' * 20)
            detail = json.loads(text)['data']
            for li in detail:
                title = li['title']
                url = 'http://zbtb.gd.gov.cn/platform/attach/getAttachList?parentId={}&parentType=GGNR&rows=999999&page=1'.format(str(li['id']))
                date_Today = li['publishdate']
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
        tt = json.loads(tool.requests_get(url, self.headers))
        item = {}
        item['title'] = title.replace('\u2022', '')
        item['url'] = url
        item['date'] = date
        item['typeid'] = tool.get_typeid(item['title'])
        item['senddate'] = int(time.time())
        item['mid'] = 867
        item['infotype'] = tool.get_infotype(item['title'])
        try:
            item['body'] = '<embed width="100%" height="100%" src="http://zbtb.gd.gov.cn/platform/attach/viewPdf?id={}" >'.format(tt['data'][0]['id'])
        except:
            return 
        # print(detail_html)
        # time.sleep(666)
        item['endtime'] = 0
        item['tel'] = 0
        item['email'] = ''
        item['address'] = ''
        item['nativeplace'] = self.get_nativeplace(item['title'])
        item['linkman'] = ''
        item['function'] = 0
        item['resource'] = '广东省招标投标监管网'
        item["shi"] = int(str(item["nativeplace"]).split('.')[0])
        item['sheng'] = 10000
        item['removal']= title
        process_item(item)
        # print(item)

    def get_nativeplace(self, addr):
        city_list = [['10001', '广州市'], ['10001.001', '东山区'], ['10001.01', '花都区'], ['10001.011', '增城市'],
                     ['10001.012', '从化市'], ['10001.002', '荔湾区'], ['10001.003', '越秀区'], ['10001.004', '海珠区'],
                     ['10001.005', '天河区'], ['10001.006', '芳村区'], ['10001.007', '白云区'], ['10001.008', '黄埔区'],
                     ['10001.009', '番禺区'], ['10001.013', '南沙区'], ['10001.014', '开发区'], ['10002', '韶关市'],
                     ['10002.001', '武江区'], ['10002.01', '南雄市'], ['10002.002', '浈江区'], ['10002.003', '曲江区'],
                     ['10002.004', '始兴县'], ['10002.005', '仁化县'], ['10002.006', '翁源县'], ['10002.007', '乳源瑶族自治县'],
                     ['10002.008', '新丰县'], ['10002.009', '乐昌市'], ['10003', '深圳市'], ['10003.001', '罗湖区'],
                     ['10003.002', '福田区'], ['10003.003', '南山区'], ['10003.004', '宝安区'], ['10003.005', '龙岗区'],
                     ['10003.006', '盐田区'], ['10003.007', '坪山区'], ['10004', '珠海市'], ['10004.001', '洲区'],
                     ['10004.002', '斗门区'], ['10004.003', '金湾区'], ['10005', '汕头市'], ['10005.001', '龙湖区'],
                     ['10005.002', '金平区'], ['10005.003', '濠江区'], ['10005.004', '潮阳区'], ['10005.005', '潮南区'],
                     ['10005.006', '澄海区'], ['10005.007', '南澳县'], ['10006', '佛山市'], ['10006.001', '禅城区'],
                     ['10006.002', '南海区'], ['10006.003', '顺德区'], ['10006.004', '三水区'], ['10006.005', '高明区'],
                     ['10007', '江门市'], ['10007.001', '蓬江区'], ['10007.002', '江海区'], ['10007.003', '新会区'],
                     ['10007.004', '台山市'], ['10007.005', '开平市'], ['10007.006', '鹤山市'], ['10007.007', '恩平市'],
                     ['10008', '湛江市'], ['10008.001', '赤坎区'], ['10008.002', '霞山区'], ['10008.003', '坡头区'],
                     ['10008.004', '麻章区'], ['10008.005', '遂溪县'], ['10008.006', '徐闻县'], ['10008.007', '廉江市'],
                     ['10008.008', '雷州市'], ['10008.009', '吴川市'], ['10009', '茂名市'], ['10009.001', '茂南区'],
                     ['10009.002', '茂港区'], ['10009.003', '电白县'], ['10009.004', '高州市'], ['10009.005', '化州市'],
                     ['10009.006', '信宜市'], ['10010', '肇庆市'], ['10010.001', '端州区'], ['10010.002', '鼎湖区'],
                     ['10010.003', '广宁县'], ['10010.004', '怀集县'], ['10010.005', '封开县'], ['10010.006', '德庆县'],
                     ['10010.007', '高要市'], ['10010.008', '四会市'], ['10011', '惠州市'], ['10011.001', '惠城区'],
                     ['10011.002', '惠阳区'], ['10011.003', '博罗县'], ['10011.004', '惠东县'], ['10011.005', '龙门县'],
                     ['10012', '梅州市'], ['10012.001', '梅江区'], ['10012.002', '梅县'], ['10012.003', '大埔县'],
                     ['10012.004', '丰顺县'], ['10012.005', '五华县'], ['10012.006', '平远县'], ['10012.007', '蕉岭县'],
                     ['10012.008', '兴宁市'], ['10013', '汕尾市'], ['10013.001', '城区'], ['10013.002', '海丰县'],
                     ['10013.003', '陆河县'], ['10013.004', '陆丰市'], ['10014', '河源市'], ['10014.001', '源城区'],
                     ['10014.002', '紫金县'], ['10014.003', '龙川县'], ['10014.004', '连平县'], ['10014.005', '和平县'],
                     ['10014.006', '东源县'], ['10015', '阳江市'], ['10015.001', '江城区'], ['10015.002', '阳西县'],
                     ['10015.003', '阳东县'], ['10015.004', '阳春市'], ['10016', '清远市'], ['10016.001', '清城区'],
                     ['10016.002', '佛冈县'], ['10016.003', '阳山县'], ['10016.004', '连山壮族瑶族自治县'], ['10016.005', '连南瑶族自治县'],
                     ['10016.006', '清新县'], ['10016.007', '英德市'], ['10016.008', '连州市'], ['10016.009', '连南县'],
                     ['10017', '东莞市'], ['10018', '中山市'], ['10019', '潮州市'], ['10019.001', '潮安县'], ['10019.002', '饶平县'],
                     ['10020', '揭阳市'], ['10020.001', '榕城区'], ['10020.002', '揭东县'], ['10020.003', '揭西县'],
                     ['10020.004', '惠来县'], ['10020.005', '普宁市'], ['10021', '云浮市'], ['10021.001', '云城区'],
                     ['10021.002', '新兴县'], ['10021.003', '郁南县'], ['10021.004', '云安县'], ['10021.005', '罗定市']]

        for i in city_list:
            if i[1] in addr:
                return i[0]

        for i in city_list:
            shi = i[1].replace('市', '')
            if shi in addr:
                return i[0]
        return 10000

if __name__ == '__main__':
    jl = xinyang_ggzy()
    jl.parse()


