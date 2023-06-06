# -*- coding: utf-8 -*-
import json
import re
import time, html
import traceback,os

import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 山东省政府采购网
class xinyang_ggzy:
    def __init__(self):
        self.url_list = [
            ['0301', '2102', '0305', '0302', '0306'],
            ['0303', '2106', '0305', '0304', '0306']
        ]
        self.i = self.url_list.pop(0)
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
            'Cookie': 'JSESSIONID=49F3DC0CDDFB1255B9077A6A56A3D269; insert_cookie=35333146'
            # 'Cookie': 'JSESSIONID=6cf5cad7-9e11-4d3d-9efd-70e2f5bc0d11'
        }

    def parse(self):
        date = tool.date
        grade = 'province'
        url_ = self.i.pop(0)
        page = 0
        url_to = 'http://www.ccgp-shandong.gov.cn/sdgp2017/site/listnew.jsp'
        while True:
            page += 1
            print('*'*50, page)
            data = '?subject=&pdate=&kindof=&areacode=&unitname=&projectname=&projectcode=&colcode={}&curpage={}&grade={}&firstpage=1'
            text = tool.requests_get(url_to + data.format(url_, page, grade), self.headers)
            detail = HTML(text).xpath('//*[@id="preform"]/div[1]/div[3]/div[2]/div[1]/ul/li')
            for li in detail:
                title = li.xpath('./span/span[1]/a/@title')[0]
                try:
                    date_Today = li.xpath('./span[2]/text()')[0].replace('\xa0', '').replace('\n', '')
                except:
                    date_Today = li.xpath('./span/span[2]/text()')[0].replace('\xa0', '').replace('\n', '')
                url = li.xpath('./span/span[1]/a/@href')[0]
                if 'http' not in url:
                    url = 'http://www.ccgp-shandong.gov.cn' + url
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
                    if len(self.i) == 0:
                        self.i = self.url_list.pop(0)
                        url_ = self.i.pop(0)
                        page = 0
                        grade = 'city'
                        break
                    url_ = self.i.pop(0)
                    page = 0
                    break
            if page == 20:
                if len(self.i) == 0:
                    self.i = self.url_list.pop(0)
                    url_ = self.i.pop(0)
                    page = 0
                    grade = 'city'
                    break
                url_ = self.i.pop(0)
                break

    def parse_detile(self, title, url, date):
        print(url)
        t = tool.requests_get(url, self.headers)
        url_html = etree.HTML(t)
        try:
            detail = url_html.xpath('//*[@id="textarea"]/table')[0]
        except:
            return
        detail_html = etree.tostring(detail, method='HTML')
        detail_html = html.unescape(detail_html.decode()).replace('\xa0', '').replace('\ufeff', '')
        detail_text = ''.join(re.findall('>(.*?)<', detail_html)) \
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
        item['winner'] = tool.get_winner(detail_text)
        item['address'] = tool.get_address(detail_text)
        item['nativeplace'] = self.get_nativeplace(item['title'])
        item['linkman'] = tool.get_linkman(detail_text)
        item['function'] = tool.get_function(detail_text)
        item['resource'] = '山东省政府采购网'
        item["shi"] = int(str(item["nativeplace"]).split('.')[0])
        item['sheng'] = 8000
        item['removal']= title
        process_item(item)

    def get_nativeplace(self, addr):
        city = ''
        city_list = [['8001', '济南'], ['8001.001', '历下'], ['8001.01', '章丘'], ['8001.002', '中'], ['8001.003', '槐荫'], ['8001.004', '天桥'], ['8001.005', '历城'], ['8001.006', '长清'], ['8001.007', '平阴'], ['8001.008', '济阳'], ['8001.009', '商河'], ['8002', '青岛'], ['8002.001', '南'], ['8002.01', '平度'], ['8002.011', '胶南'], ['8002.012', '莱西'], ['8002.002', '北'], ['8002.003', '四方'], ['8002.004', '黄岛'], ['8002.005', '崂山'], ['8002.006', '李沧'], ['8002.007', '城阳'], ['8002.008', '胶州'], ['8002.009', '即墨'], ['8003', '淄博'], ['8003.001', '淄川'], ['8003.002', '张店'], ['8003.003', '博山'], ['8003.004', '临淄'], ['8003.005', '周村'], ['8003.006', '桓台'], ['8003.007', '高青'], ['8003.008', '沂源'], ['8004', '枣庄'], ['8004.001', '中'], ['8004.002', '薛城'], ['8004.003', '峄城'], ['8004.004', '台儿庄'], ['8004.005', '山亭'], ['8004.006', '滕州'], ['8005', '烟台'], ['8005.001', '芝罘'], ['8005.01', '招远'], ['8005.011', '栖霞'], ['8005.012', '海阳'], ['8005.002', '福山'], ['8005.003', '牟平'], ['8005.004', '莱山'], ['8005.005', '长岛'], ['8005.006', '龙口'], ['8005.007', '莱阳'], ['8005.008', '莱州'], ['8005.009', '蓬莱'], ['8006', '潍坊'], ['8006.001', '潍城'], ['8006.01', '安丘'], ['8006.011', '高密'], ['8006.012', '昌邑'], ['8006.002', '寒亭'], ['8006.003', '坊子'], ['8006.004', '奎文'], ['8006.005', '临朐'], ['8006.006', '昌乐'], ['8006.007', '青州'], ['8006.008', '诸城'], ['8006.009', '寿光'], ['8007', '济宁'], ['8007.001', '中'], ['8007.01', '曲阜'], ['8007.011', '兖州'], ['8007.012', '邹城'], ['8007.002', '任城'], ['8007.003', '微山'], ['8007.004', '鱼台'], ['8007.005', '金乡'], ['8007.006', '嘉祥'], ['8007.007', '汶上'], ['8007.008', '泗水'], ['8007.009', '梁山'], ['8008', '泰安'], ['8008.001', '泰山'], ['8008.002', '岱岳'], ['8008.003', '宁阳'], ['8008.004', '东平'], ['8008.005', '新泰'], ['8008.006', '肥城'], ['8009', '威海'], ['8009.001', '环翠'], ['8009.002', '文登'], ['8009.003', '荣成'], ['8009.004', '乳山'], ['8010', '日照'], ['8010.001', '东港'], ['8010.002', '岚山'], ['8010.003', '五莲'], ['8010.004', '莒'], ['8011', '莱芜'], ['8011.001', '莱城'], ['8011.002', '钢城'], ['8012', '临沂'], ['8012.001', '兰山'], ['8012.01', '莒南'], ['8012.011', '蒙阴'], ['8012.012', '临沭'], ['8012.002', '罗庄'], ['8012.003', '河东'], ['8012.004', '沂南'], ['8012.005', '郯城'], ['8012.006', '沂水'], ['8012.007', '苍山'], ['8012.008', '费'], ['8012.009', '平邑'], ['8013', '德州'], ['8013.001', '德城'], ['8013.01', '乐陵'], ['8013.011', '禹城'], ['8013.002', '陵'], ['8013.003', '宁津'], ['8013.004', '庆云'], ['8013.005', '临邑'], ['8013.006', '齐河'], ['8013.007', '平原'], ['8013.008', '夏津'], ['8013.009', '武城'], ['8014', '聊城'], ['8014.001', '东昌府'], ['8014.002', '阳谷'], ['8014.003', '莘'], ['8014.004', '茌平'], ['8014.005', '东阿'], ['8014.006', '冠'], ['8014.007', '高唐'], ['8014.008', '临清'], ['8015', '滨州'], ['8015.001', '滨城'], ['8015.002', '惠民'], ['8015.003', '阳信'], ['8015.004', '无棣'], ['8015.005', '沾化'], ['8015.006', '博兴'], ['8015.007', '邹平'], ['8016', '菏泽'], ['8016.001', '牡丹'], ['8016.002', '曹'], ['8016.003', '单'], ['8016.004', '成武'], ['8016.005', '巨野'], ['8016.006', '郓城'], ['8016.007', '鄄城'], ['8016.008', '定陶'], ['8016.009', '东明'], ['8017', '东营'], ['8017.001', '东营'], ['8017.002', '河口'], ['8017.003', '利津'], ['8017.004', '垦利']]

        for i in city_list:
            if i[1] in addr:
                city = float(i[0])
                break
        if city == '':
            city = 8000
        return city

if __name__ == '__main__':
    try:
        jl = xinyang_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
        tool.send_error('报错文件：'+str(os.path.basename(__file__))+'报错信息：'+str(e))


