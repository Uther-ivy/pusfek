# -*- coding: utf-8 -*-
import datetime
import random
import re
import time

import pymysql
import requests
from scrapy import Selector
import ssl
import tool
from save_database import save_db
from proxies import proxise
pro = proxise()

ssl._create_default_https_context = ssl._create_unverified_context
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
}

def get_nativeplace(addr):
    city = ''
    city_list = [['8001', '济南市'], ['8001.001', '历下区'], ['8001.01', '章丘市'], ['8001.002', '市中区'], ['8001.003', '槐荫区'],
                 ['8001.004', '天桥区'], ['8001.005', '历城区'], ['8001.006', '长清区'], ['8001.007', '平阴县'],
                 ['8001.008', '济阳县'], ['8001.009', '商河县'], ['8002', '青岛市'], ['8002.001', '市南区'], ['8002.01', '平度市'],
                 ['8002.011', '胶南市'], ['8002.012', '莱西市'], ['8002.002', '市北区'], ['8002.003', '四方区'],
                 ['8002.004', '黄岛区'], ['8002.005', '崂山区'], ['8002.006', '李沧区'], ['8002.007', '城阳区'],
                 ['8002.008', '胶州市'], ['8002.009', '即墨市'], ['8003', '淄博市'], ['8003.001', '淄川区'], ['8003.002', '张店区'],
                 ['8003.003', '博山区'], ['8003.004', '临淄区'], ['8003.005', '周村区'], ['8003.006', '桓台县'],
                 ['8003.007', '高青县'], ['8003.008', '沂源县'], ['8004', '枣庄市'], ['8004.001', '市中区'], ['8004.002', '薛城区'],
                 ['8004.003', '峄城区'], ['8004.004', '台儿庄区'], ['8004.005', '山亭区'], ['8004.006', '滕州市'], ['8005', '烟台市'],
                 ['8005.001', '芝罘区'], ['8005.01', '招远市'], ['8005.011', '栖霞市'], ['8005.012', '海阳市'], ['8005.002', '福山区'],
                 ['8005.003', '牟平区'], ['8005.004', '莱山区'], ['8005.005', '长岛县'], ['8005.006', '龙口市'],
                 ['8005.007', '莱阳市'], ['8005.008', '莱州市'], ['8005.009', '蓬莱市'], ['8006', '潍坊市'], ['8006.001', '潍城区'],
                 ['8006.01', '安丘市'], ['8006.011', '高密市'], ['8006.012', '昌邑市'], ['8006.002', '寒亭区'], ['8006.003', '坊子区'],
                 ['8006.004', '奎文区'], ['8006.005', '临朐县'], ['8006.006', '昌乐县'], ['8006.007', '青州市'],
                 ['8006.008', '诸城市'], ['8006.009', '寿光市'], ['8007', '济宁市'], ['8007.001', '市中区'], ['8007.01', '曲阜市'],
                 ['8007.011', '兖州市'], ['8007.012', '邹城市'], ['8007.002', '任城区'], ['8007.003', '微山县'],
                 ['8007.004', '鱼台县'], ['8007.005', '金乡县'], ['8007.006', '嘉祥县'], ['8007.007', '汶上县'],
                 ['8007.008', '泗水县'], ['8007.009', '梁山县'], ['8008', '泰安市'], ['8008.001', '泰山区'], ['8008.002', '岱岳区'],
                 ['8008.003', '宁阳县'], ['8008.004', '东平县'], ['8008.005', '新泰市'], ['8008.006', '肥城市'], ['8009', '威海市'],
                 ['8009.001', '环翠区'], ['8009.002', '文登市'], ['8009.003', '荣成市'], ['8009.004', '乳山市'], ['8010', '日照市'],
                 ['8010.001', '东港区'], ['8010.002', '岚山区'], ['8010.003', '五莲县'], ['8010.004', '莒县'], ['8011', '莱芜市'],
                 ['8011.001', '莱城区'], ['8011.002', '钢城区'], ['8012', '临沂市'], ['8012.001', '兰山区'], ['8012.01', '莒南县'],
                 ['8012.011', '蒙阴县'], ['8012.012', '临沭县'], ['8012.002', '罗庄区'], ['8012.003', '河东区'],
                 ['8012.004', '沂南县'], ['8012.005', '郯城县'], ['8012.006', '沂水县'], ['8012.007', '苍山县'], ['8012.008', '费县'],
                 ['8012.009', '平邑县'], ['8013', '德州市'], ['8013.001', '德城区'], ['8013.01', '乐陵市'], ['8013.011', '禹城市'],
                 ['8013.002', '陵县'], ['8013.003', '宁津县'], ['8013.004', '庆云县'], ['8013.005', '临邑县'], ['8013.006', '齐河县'],
                 ['8013.007', '平原县'], ['8013.008', '夏津县'], ['8013.009', '武城县'], ['8014', '聊城市'], ['8014.001', '东昌府区'],
                 ['8014.002', '阳谷县'], ['8014.003', '莘县'], ['8014.004', '茌平县'], ['8014.005', '东阿县'], ['8014.006', '冠县'],
                 ['8014.007', '高唐县'], ['8014.008', '临清市'], ['8015', '滨州市'], ['8015.001', '滨城区'], ['8015.002', '惠民县'],
                 ['8015.003', '阳信县'], ['8015.004', '无棣县'], ['8015.005', '沾化县'], ['8015.006', '博兴县'],
                 ['8015.007', '邹平县'], ['8016', '荷泽市'], ['8016.001', '牡丹区'], ['8016.002', '曹县'], ['8016.003', '单县'],
                 ['8016.004', '成武县'], ['8016.005', '巨野县'], ['8016.006', '郓城县'], ['8016.007', '鄄城县'],
                 ['8016.008', '定陶县'], ['8016.009', '东明县'], ['8017', '东营市'], ['8017.001', '东营区'], ['8017.002', '河口区'],
                 ['8017.003', '利津县'], ['8017.004', '垦利县'], ['8017.005', '广饶县']]

    for i in city_list:
        if i[1] in addr:
            city = float(i[0])
            break
    if city == '':
        city = 8000
    return city

def get_zhaobiao_info(title,zhao_time,info_url):
    resp = requests.get(info_url, headers=headers,proxies=pro,timeout=20)
    resp.encoding = "utf8"
    sel = Selector(resp)
    item = {}
    item['zhao_time'] = zhao_time
    item['title'] = title
    item['info_url'] = info_url
    item['body'] = sel.xpath('//div[@class="newsArow textP"]').extract_first()
    if item['body'] == None:
        item['body'] = sel.xpath('//div[@class="newsArow"]').extract_first()
    item['detail'] = item['body'].replace('\n', '').replace("\t", '').replace("\r", '').replace('\xa0', '').replace('\xc2', '').replace(' ', '')
    item['senddate'] = int(time.time())
    item['mid'] = 1403
    item['typeid'] = tool.get_typeid(title)
    item['endtime'] = tool.get_endtime(item['detail'])
    if item['endtime'] == '':
        item['endtime'] = int(time.mktime(time.strptime(zhao_time, "%Y-%m-%d")))
    else:
        try:
            item['endtime'] = int(time.mktime(time.strptime(item['endtime'], "%Y-%m-%d")))
        except:
            item['endtime'] = int(time.mktime(time.strptime(zhao_time, "%Y-%m-%d")))
    item['nativeplace'] = get_nativeplace(title + item['detail'])
    item['infotype'] = tool.get_infotype(title)
    item['shi'] = int(item['nativeplace'])
    item['sheng'] = 8000
    item['email'] = ''
    item['tel'] = tool.get_tel(item['detail'])
    item['address'] = tool.get_address(item['detail'])
    item['linkman'] = tool.get_linkman(item['detail'])
    item['function'] = tool.get_function(item['detail'])  # detail["projectBudget"]
    item['click'] = random.randint(500, 1000)
    item['resource'] = "菏泽市公共服务与监管平台"
    save_db(item)

def get_project(url):
    resp = requests.get(url, headers=headers,proxies=pro,timeout=20)
    resp.encoding="utf8"
    sel = Selector(resp)
    titles = sel.xpath('//div[@class="contents"]/div/div/ul/li')
    now_time = tool.date
    # print(resp.text)
    for ti in titles:
        title = ti.xpath('./a/h2/text()').extract_first()
        zhao_time = ti.xpath('./a/div/div[2]/span[2]/em/text()').extract_first()
        info_url = "http://hzsggzyjy.gov.cn/" +  ti.xpath('./a/@href').extract_first()
        # print(title,zhao_time,info_url)
        if tool.Transformation(now_time) <= tool.Transformation(zhao_time):
            get_zhaobiao_info(title,zhao_time,info_url)
        print(zhao_time)

if __name__ == '__main__':
    requests.adapters.DEFAULT_RETRIES = 5  # 增加重连次数
    s = requests.session()
    s.keep_alive = False  # 关闭多余连接
    requests.packages.urllib3.disable_warnings()
    url = "http://hzsggzyjy.gov.cn/cityInfoList.aspx?s=1&t=1"# 网站失效，503
    get_project(url)