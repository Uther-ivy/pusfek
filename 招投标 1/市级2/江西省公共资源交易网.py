# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 江西省公共资源交易网
class baoshan_ggzy:
    def __init__(self):
        self.url_list = [
            'https://www.jxsggzy.cn/web/jyxx/002001/002001001/{}.html',
            'https://www.jxsggzy.cn/web/jyxx/002001/002001004/{}.html',
            'https://www.jxsggzy.cn/web/jyxx/002002/002002002/{}.html',
            'https://www.jxsggzy.cn/web/jyxx/002002/002002005/{}.html',
            'https://www.jxsggzy.cn/web/jyxx/002006/002006001/{}.html',
            'https://www.jxsggzy.cn/web/jyxx/002006/002006002/{}.html',
            'https://www.jxsggzy.cn/web/jyxx/002006/002006004/{}.html',
            'https://www.jxsggzy.cn/web/jyxx/002006/002006005/{}.html'
                         ]
        self.url = self.url_list.pop(0)
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Host': 'www.jxsggzy.cn',
            'If-Modified-Since': 'Mon, 07 Dec 2020 08:56:39 GMT',
            'If-None-Match': 'W/"5fcdee47-6eab"',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36',
        }

    def parse(self):
        date = tool.date
        # date = '2020-11-03'
        page = 0
        while True:
            page += 1
            text = tool.requests_get(self.url.format(page), self.headers)
            print('*' * 20, page, '*' * 20)
            html = HTML(text)
            # print(11, self.url.format(page), text)
            # time.sleep(6666)
            detail = html.xpath('//*[@id="gengerlist"]/div[1]/ul/li')
            for li in detail:
                title = li.xpath('./a/text()')[0].replace('\n', '').replace('\r', '')\
                    .replace('\t', '').replace(' ', '').replace('<spanstyle="color:red">', '').replace('</span>', '')
                url = li.xpath('./a/@href')[0]
                if 'http' not in url:
                    url = 'https://www.jxsggzy.cn' + url
                date_Today = li.xpath('./span/text()')[0].replace('\n', '').replace('\r', '') \
                    .replace('\t', '').replace(' ', '').replace('(', '').replace(')', '').replace('.', '-')\
                    .replace('[', '').replace(']', '')
                if '测试' in title:
                    continue
                # print(title, url, date_Today)
                # time.sleep(666)
                if tool.Transformation(date_Today) >= tool.Transformation(date):
                    if tool.removal(title, date):
                        self.parse_detile(title, url, date_Today)
                    else:
                        print('【existence】', url)
                        continue
                else:
                    print('日期不符, 正在切换类型', date_Today, self.url)
                    self.url = self.url_list.pop(0)
                    page = 0
                    break
            if page == 20:
                self.url = self.url_list.pop(0)
                break

    def parse_detile(self, title, url, date):
        print(url)
        t = tool.requests_get(url, self.headers)
        url_html = etree.HTML(t)
        try:
            detail = url_html.xpath('//*[@class="con"]')[0]
            detail_html = etree.tostring(detail, method='HTML')
            detail_html = html.unescape(detail_html.decode())
            detail_text = url_html.xpath('string(//*[@class="con"])').replace('\xa0', '').replace('\n',
                                                                                                         ''). \
                replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
            if len(detail_html) < 300:
                return
        except:
            return
        # print(111, detail_text.replace('\xa0','').replace('\xa5',''))
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
        item['linkman'] = tool.get_linkman(detail_text)
        item['function'] = tool.get_function(detail_text)
        item['resource'] = '江西省公共资源交易网'
        item['shi'] = int(item['nativeplace'])
        item['sheng'] = 7500
        item['removal']= title
        process_item(item)

    def get_nativeplace(self, addr):
        city = ''
        city_list = [['7501.001', '东湖区'], ['7501.002', '西湖区'], ['7501.003', '青云谱区'], ['7501.004', '湾里区'], ['7501.005', '青山湖区'], ['7501.006', '南昌县'], ['7501.007', '新建县'], ['7501.008', '安义县'], ['7501.009', '进贤县'], ['7502.001', '昌江区'], ['7502.002', '珠山区'], ['7502.003', '浮梁县'], ['7502.004', '乐平市'], ['7503.001', '安源区'], ['7503.002', '湘东区'], ['7503.003', '莲花县'], ['7503.004', '上栗县'], ['7503.005', '芦溪县'], ['7504.001', '庐山区'], ['7504.01', '湖口县'], ['7504.011', '彭泽县'], ['7504.012', '瑞昌市'], ['7504.013', '柴桑区'], ['7504.014', '濂溪区'], ['7504.002', '浔阳区'], ['7504.003', '九江县'], ['7504.004', '武宁县'], ['7504.005', '修水县'], ['7504.006', '永修县'], ['7504.007', '德安县'], ['7504.008', '星子县'], ['7504.009', '都昌县'], ['7505.001', '渝水区'], ['7505.002', '分宜县'], ['7506.001', '月湖区'], ['7506.002', '余江县'], ['7506.003', '贵溪市'], ['7507.001', '章贡区'], ['7507.01', '全南县'], ['7507.011', '宁都县'], ['7507.012', '于都县'], ['7507.013', '兴国县'], ['7507.014', '会昌县'], ['7507.015', '寻乌县'], ['7507.016', '石城县'], ['7507.017', '瑞金市'], ['7507.018', '南康市'], ['7507.002', '赣县'], ['7507.003', '信丰县'], ['7507.004', '大余县'], ['7507.005', '上犹县'], ['7507.006', '崇义县'], ['7507.007', '安远县'], ['7507.008', '龙南县'], ['7507.009', '定南县'], ['7508.001', '吉州区'], ['7508.01', '万安县'], ['7508.011', '安福县'], ['7508.012', '永新县'], ['7508.013', '井冈山市'], ['7508.002', '青原区'], ['7508.003', '吉安县'], ['7508.004', '吉水县'], ['7508.005', '峡江县'], ['7508.006', '新干县'], ['7508.007', '永丰县'], ['7508.008', '泰和县'], ['7508.009', '遂川县'], ['7509.001', '袁州区'], ['7509.01', '高安市'], ['7509.002', '奉新县'], ['7509.003', '万载县'], ['7509.004', '上高县'], ['7509.005', '宜丰县'], ['7509.006', '靖安县'], ['7509.007', '铜鼓县'], ['7509.008', '丰城市'], ['7509.009', '樟树市'], ['7510.001', '临川区'], ['7510.01', '东乡县'], ['7510.011', '广昌县'], ['7510.002', '南城县'], ['7510.003', '黎川县'], ['7510.004', '南丰县'], ['7510.005', '崇仁县'], ['7510.006', '乐安县'], ['7510.007', '宜黄县'], ['7510.008', '金溪县'], ['7510.009', '资溪县'], ['7511.001', '信州区'], ['7511.01', '万年县'], ['7511.011', '婺源县'], ['7511.012', '德兴市'], ['7511.002', '上饶县'], ['7511.003', '广丰县'], ['7511.004', '玉山县'], ['7511.005', '铅山县'], ['7511.006', '横峰县'], ['7511.007', '弋阳县'], ['7511.008', '余干县'], ['7511.009', '鄱阳县']]

        for i in city_list:
            if i[1] in addr:
                city = float(i[0])
                break
        if city == '':
            city = 7500
        return city

if __name__ == '__main__':
    import traceback, os
    try:
        jl = baoshan_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
        tool.send_error('报错文件：'+str(os.path.basename(__file__))+'报错信息：'+str(e))



