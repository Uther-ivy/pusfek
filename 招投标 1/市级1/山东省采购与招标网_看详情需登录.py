# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 山东省采购与招标网
class wenshan_ggzy:
    def __init__(self):
        self.domain_name = 'https://www.sdbidding.org.cn'
        self.url_list = [
            'https://www.sdbidding.org.cn/bulletins;jsessionid=4D4235AAE29ABF6302007184DF9AA064?titleLike=&pageNo={}&pageSize=10&infoType=11',
            'https://www.sdbidding.org.cn/bulletins?titleLike=&pageNo={}&pageSize=10&infoType=12',
            'https://www.sdbidding.org.cn/bulletins?titleLike=&pageNo={}&pageSize=10&infoType=13',
            'https://www.sdbidding.org.cn/bulletins?titleLike=&pageNo={}&pageSize=10&infoType=14'
        ]
        self.url = self.url_list.pop(0)
        self.headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Cookie': 'JSESSIONID=688B4A6A5371E3F3B3324237530B7C3C; Hm_lvt_3bc19bf638a10bf839128052d35265ec=1614678182; x-token=eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJVc2VyIiwiZXhwIjoxNjE0Njk5ODQyLCJ1c2VySWQiOjI3ODk5NiwiaWF0IjoxNjE0Njc4MjQyLCJqdGkiOiJqd3QifQ.u6y-8yH3U1SyAdZponhFWDhJwymjf57nICKSmpheiFE; Hm_lpvt_3bc19bf638a10bf839128052d35265ec=1614678245',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',

        }

    def parse(self):
        date = tool.date
        # date = '2020-09-27'
        page = 0
        while True:
            page += 1
            text = tool.requests_get(self.url.format(page), self.headers)
            html = HTML(text)
            print('*' * 20, page, '*' * 20)
            # print(11, text.replace('\ufffd', ' ').replace('\u30fb', ' '))
            # time.sleep(6666)
            detail = html.xpath('/html/body/div[2]/div[2]/div[2]/div[1]/table/tr')
            for li in detail:
                try:
                    title = li.xpath('./td[2]/a/@title')[0].replace('\xa0', '').replace('\n', ''). \
                        replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '').replace("<fontstyle='color:red'>(网)</font>", '')
                    url = li.xpath('./td[2]/a/@href')[0]
                    date_Today = li.xpath('./td[5]/text()')[0].replace('\xa0', '').replace('\n', ''). \
                        replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '') \
                        .replace('[', '').replace(']', '').replace('/', '-')
                except:
                    continue
                if 'http' not in url:
                    url = self.domain_name + url
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
        t = tool.requests_get(url, self.headers).replace('\xa9', '').replace('<br>&nbsp;&nbsp;', '')
        # print(t)
        # time.sleep(2222)
        url_html = etree.HTML(t)
        detail = url_html.xpath('/html/body/div[2]/div[2]/div[2]')[0]
        detail_html = etree.tostring(detail, method='HTML')
        detail_html = html.unescape(detail_html.decode()).replace("display: none", '').replace("\u2022", '').replace('\xa0', '')
        detail_text = url_html.xpath('string(/html/body/div[2]/div[2]/div[2])').replace('\xa0', '').replace('\n',
                                                                                                             ''). \
            replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
        if len(detail_html) < 200:
            int('a')
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
        item['resource'] = '山东省采购与招标网'
        item['shi'] = int(item['nativeplace'])
        item['sheng'] = 8000
        item['removal']= title
        process_item(item)

    def get_nativeplace(self, addr):
        city = ''
        city_list = [['8001', '济南'], ['8001.001', '历下区'], ['8001.01', '章丘'], ['8001.002', '中区'], ['8001.003', '槐荫区'], ['8001.004', '天桥区'], ['8001.005', '历城区'], ['8001.006', '长清区'], ['8001.007', '平阴县'], ['8001.008', '济阳县'], ['8001.009', '商河县'], ['8002', '青岛'], ['8002.001', '南区'], ['8002.01', '平度'], ['8002.011', '胶南'], ['8002.012', '莱西'], ['8002.002', '北区'], ['8002.003', '四方区'], ['8002.004', '黄岛区'], ['8002.005', '崂山区'], ['8002.006', '李沧区'], ['8002.007', '城阳区'], ['8002.008', '胶州'], ['8002.009', '即墨'], ['8003', '淄博'], ['8003.001', '淄川区'], ['8003.002', '张店区'], ['8003.003', '博山区'], ['8003.004', '临淄区'], ['8003.005', '周村区'], ['8003.006', '桓台县'], ['8003.007', '高青县'], ['8003.008', '沂源县'], ['8004', '枣庄'], ['8004.001', '中区'], ['8004.002', '薛城区'], ['8004.003', '峄城区'], ['8004.004', '台儿庄区'], ['8004.005', '山亭区'], ['8004.006', '滕州'], ['8005', '烟台'], ['8005.001', '芝罘区'], ['8005.01', '招远'], ['8005.011', '栖霞'], ['8005.012', '海阳'], ['8005.002', '福山区'], ['8005.003', '牟平区'], ['8005.004', '莱山区'], ['8005.005', '长岛县'], ['8005.006', '龙口'], ['8005.007', '莱阳'], ['8005.008', '莱州'], ['8005.009', '蓬莱'], ['8006', '潍坊'], ['8006.001', '潍城区'], ['8006.01', '安丘'], ['8006.011', '高密'], ['8006.012', '昌邑'], ['8006.002', '寒亭区'], ['8006.003', '坊子区'], ['8006.004', '奎文区'], ['8006.005', '临朐县'], ['8006.006', '昌乐县'], ['8006.007', '青州'], ['8006.008', '诸城'], ['8006.009', '寿光'], ['8007', '济宁'], ['8007.001', '中区'], ['8007.01', '曲阜'], ['8007.011', '兖州'], ['8007.012', '邹城'], ['8007.002', '任城区'], ['8007.003', '微山县'], ['8007.004', '鱼台县'], ['8007.005', '金乡县'], ['8007.006', '嘉祥县'], ['8007.007', '汶上县'], ['8007.008', '泗水县'], ['8007.009', '梁山县'], ['8008', '泰安'], ['8008.001', '泰山区'], ['8008.002', '岱岳区'], ['8008.003', '宁阳县'], ['8008.004', '东平县'], ['8008.005', '新泰'], ['8008.006', '肥城'], ['8009', '威海'], ['8009.001', '环翠区'], ['8009.002', '文登'], ['8009.003', '荣成'], ['8009.004', '乳山'], ['8010', '日照'], ['8010.001', '东港区'], ['8010.002', '岚山区'], ['8010.003', '五莲县'], ['8010.004', '莒县'], ['8011', '莱芜'], ['8011.001', '莱城区'], ['8011.002', '钢城区'], ['8012', '临沂'], ['8012.001', '兰山区'], ['8012.01', '莒南县'], ['8012.011', '蒙阴县'], ['8012.012', '临沭县'], ['8012.002', '罗庄区'], ['8012.003', '河东区'], ['8012.004', '沂南县'], ['8012.005', '郯城县'], ['8012.006', '沂水县'], ['8012.007', '苍山县'], ['8012.008', '费县'], ['8012.009', '平邑县'], ['8013', '德州'], ['8013.001', '德城区'], ['8013.01', '乐陵'], ['8013.011', '禹城'], ['8013.002', '陵县'], ['8013.003', '宁津县'], ['8013.004', '庆云县'], ['8013.005', '临邑县'], ['8013.006', '齐河县'], ['8013.007', '平原县'], ['8013.008', '夏津县'], ['8013.009', '武城县'], ['8014', '聊城'], ['8014.001', '东昌府区'], ['8014.002', '阳谷县'], ['8014.003', '莘县'], ['8014.004', '茌平县'], ['8014.005', '东阿县'], ['8014.006', '冠县'], ['8014.007', '高唐县'], ['8014.008', '临清'], ['8015', '滨州'], ['8015.001', '滨城区'], ['8015.002', '惠民县'], ['8015.003', '阳信县'], ['8015.004', '无棣县'], ['8015.005', '沾化县'], ['8015.006', '博兴县'], ['8015.007', '邹平县'], ['8016', '菏泽'], ['8016.001', '牡丹区'], ['8016.002', '曹县'], ['8016.003', '单县'], ['8016.004', '成武县'], ['8016.005', '巨野县'], ['8016.006', '郓城县'], ['8016.007', '鄄城县'], ['8016.008', '定陶县'], ['8016.009', '东明县'], ['8017', '东营'], ['8017.001', '东营区'], ['8017.002', '河口区'], ['8017.003', '利津县'], ['8017.004', '垦利县'], ['8017.005', '广饶县']]

        for i in city_list:
            if i[1] in addr:
                city = float(i[0])
                break
        if city == '':
            city = 8000
        return city

if __name__ == '__main__':
    import os,traceback
    try:
        jl = wenshan_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
        # tool.send_error('报错文件：'+str(os.path.basename(__file__))+'报错信息：'+str(e))


