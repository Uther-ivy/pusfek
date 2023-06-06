# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 广东中凯工程管理咨询有限公司
class xinyang_ggzy:
    def __init__(self):
        self.url_list = [
           'http://www.gdzkgc.com/index.php?s=index/category/index&id=4'
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
            text = tool.requests_get(self.url, self.headers)
            html = HTML(text)
            print('*' * 20, page, '*' * 20)
            detail = html.xpath('//*[@id="content1"]/div[1]/ul/li')
            for li in detail:
                title = li.xpath('./a/text()')[0].replace('\xa0', '').replace(' ', '')
                url = li.xpath('./a/@href')[0]
                if 'http' not in url:
                    url = 'http://www.gdzkgc.com' +url

                date_Today = li.xpath('./span/text()')[0].replace('\r', '').replace(' ', '').replace('\n', '').replace('\t', '').replace('发布时间：', '')
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
        t = tool.requests_get(url, self.headers)
        t = t.replace("""<DIV class='.wmain12"'>""", "<DIV class='.wmain12'>")
        url_html = etree.HTML(t)
        detail = url_html.xpath('//*[@id="content"]')[0]
        detail_html = etree.tostring(detail, method='HTML')
        detail_html = html.unescape(detail_html.decode()).replace('\xa0', '').replace('\ufeff', '')

        detail_ = url_html.xpath('//*[@class="pageNavi"]')[0]
        detail_html_ = etree.tostring(detail_, method='HTML')
        detail_html_ = html.unescape(detail_html_.decode()).replace('\xa0', '').replace('\ufeff', '')

        detail_html = detail_html.replace(detail_html_, '')
        detail_text = url_html.xpath('string(//*[@id="content"])') \
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
        item['address'] = tool.get_address(detail_text)
        item['nativeplace'] = self.get_nativeplace_to(item['title'])
        item['linkman'] = tool.get_linkman(detail_text)
        item['function'] = tool.get_function(detail_text)
        item['resource'] = '广东中凯工程管理咨询有限公司'
        item["shi"] = int(str(item["nativeplace"]).split('.')[0])
        item['sheng'] = 10000
        item['removal']= title
        process_item(item)
        # print(item['body'])

    def get_nativeplace_to(self, city):
        a = ''
        ls = [['10001', '广州'], ['10001.001', '东山区'], ['10001.01', '花都区'], ['10001.011', '增城'], ['10001.012', '从化'], ['10001.002', '荔湾区'], ['10001.003', '越秀区'], ['10001.004', '海珠区'], ['10001.005', '天河区'], ['10001.006', '芳村区'], ['10001.007', '白云区'], ['10001.008', '黄埔区'], ['10001.009', '番禺区'], ['10001.013', '南沙区'], ['10001.014', '开发区'], ['10002', '韶关'], ['10002.001', '武江区'], ['10002.01', '南雄'], ['10002.002', '浈江区'], ['10002.003', '曲江区'], ['10002.004', '始兴县'], ['10002.005', '仁化县'], ['10002.006', '翁源县'], ['10002.007', '乳源瑶族自治县'], ['10002.008', '新丰县'], ['10002.009', '乐昌'], ['10003', '深圳'], ['10003.001', '罗湖区'], ['10003.002', '福田区'], ['10003.003', '南山区'], ['10003.004', '宝安区'], ['10003.005', '龙岗区'], ['10003.006', '盐田区'], ['10003.007', '坪山区'], ['10004', '珠海'], ['10004.001', '洲区'], ['10004.002', '斗门区'], ['10004.003', '金湾区'], ['10005', '汕头'], ['10005.001', '龙湖区'], ['10005.002', '金平区'], ['10005.003', '濠江区'], ['10005.004', '潮阳区'], ['10005.005', '潮南区'], ['10005.006', '澄海区'], ['10005.007', '南澳县'], ['10006', '佛山'], ['10006.001', '禅城区'], ['10006.002', '南海区'], ['10006.003', '顺德区'], ['10006.004', '三水区'], ['10006.005', '高明区'], ['10007', '江门'], ['10007.001', '蓬江区'], ['10007.002', '江海区'], ['10007.003', '新会区'], ['10007.004', '台山'], ['10007.005', '开平'], ['10007.006', '鹤山'], ['10007.007', '恩平'], ['10008', '湛江'], ['10008.001', '赤坎区'], ['10008.002', '霞山区'], ['10008.003', '坡头区'], ['10008.004', '麻章区'], ['10008.005', '遂溪县'], ['10008.006', '徐闻县'], ['10008.007', '廉江'], ['10008.008', '雷州'], ['10008.009', '吴川'], ['10009', '茂名'], ['10009.001', '茂南区'], ['10009.002', '茂港区'], ['10009.003', '电白县'], ['10009.004', '高州'], ['10009.005', '化州'], ['10009.006', '信宜'], ['10010', '肇庆'], ['10010.001', '端州区'], ['10010.002', '鼎湖区'], ['10010.003', '广宁县'], ['10010.004', '怀集县'], ['10010.005', '封开县'], ['10010.006', '德庆县'], ['10010.007', '高要'], ['10010.008', '四会'], ['10011', '惠州'], ['10011.001', '惠城区'], ['10011.002', '惠阳区'], ['10011.003', '博罗县'], ['10011.004', '惠东县'], ['10011.005', '龙门县'], ['10012', '梅州'], ['10012.001', '梅江区'], ['10012.002', '梅县'], ['10012.003', '大埔县'], ['10012.004', '丰顺县'], ['10012.005', '五华县'], ['10012.006', '平远县'], ['10012.007', '蕉岭县'], ['10012.008', '兴宁'], ['10013', '汕尾'], ['10013.001', '城区'], ['10013.002', '海丰县'], ['10013.003', '陆河县'], ['10013.004', '陆丰'], ['10014', '河源'], ['10014.001', '源城区'], ['10014.002', '紫金县'], ['10014.003', '龙川县'], ['10014.004', '连平县'], ['10014.005', '和平县'], ['10014.006', '东源县'], ['10015', '阳江'], ['10015.001', '江城区'], ['10015.002', '阳西县'], ['10015.003', '阳东县'], ['10015.004', '阳春'], ['10016', '清远'], ['10016.001', '清城区'], ['10016.002', '佛冈县'], ['10016.003', '阳山县'], ['10016.004', '连山壮族瑶族自治县'], ['10016.005', '连南瑶族自治县'], ['10016.006', '清新县'], ['10016.007', '英德'], ['10016.008', '连州'], ['10016.009', '连南县'], ['10017', '东莞'], ['10018', '中山'], ['10019', '潮州'], ['10019.001', '潮安县'], ['10019.002', '饶平县'], ['10020', '揭阳'], ['10020.001', '榕城区'], ['10020.002', '揭东县'], ['10020.003', '揭西县'], ['10020.004', '惠来县'], ['10020.005', '普宁'], ['10021', '云浮'], ['10021.001', '云城区'], ['10021.002', '新兴县'], ['10021.003', '郁南县'], ['10021.004', '云安县'], ['10021.005', '罗定']]
        for i in ls:
            if i[1] in city:
                a = i[0]
                break
        if a == '':
            return 10000
        else:
            return a


if __name__ == '__main__':
    import traceback, os
    try:
        jl = xinyang_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
