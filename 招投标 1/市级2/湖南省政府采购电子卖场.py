# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 湖南省政府采购电子卖场
class baoshan_ggzy:
    def __init__(self):
        self.url_list = [
            {"pageSize":10,"pageNo":2,"announcementTypes":[10017,8018,8023,8024],"district":"439900"},
            {"pageSize":10,"pageNo":1,"announcementTypes":[8020,8025,8026,8013],"district":"439900"},
            {"pageSize":10,"pageNo":1,"announcementTypes":[8016,8021],"district":"439900"},
            {"pageSize":10,"pageNo":1,"announcementTypes":[8022],"district":"439900"},
            {"pageSize":10,"pageNo":1,"announcementTypes":[8015],"district":"439900"},
        ]
        self.url = self.url_list.pop(0)
        self.headers = {
            'Content-Type': 'application/json;charset=UTF-8',
            'Cookie': 'SESSION=f0b05999-e533-4ae0-96dc-5fa0ca9e2f40; JSESSIONID=8419CC7C9C27842543849F570722B4F5.32node2',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        }

    def parse(self):
        date = tool.date
        # date = '2021-08-02'
        page = 0
        url_ = 'https://hunan.zcygov.cn/announcement/lobby/queryPage'
        while True:
            page += 1
            self.url['pageNo'] = page
            text = tool.requests_post_to(url_, self.url, self.headers).replace('\u2022', '')
            print('*' * 20, page, '*' * 20)
            detail = json.loads(text)['result']['data']
            for li in detail:
                title = li['title'].replace('\n', '').replace('\t', '').replace(' ', '').replace('\r', '')
                url = 'https://hunan.zcygov.cn/luban/announcement/detail?encryptId='+li['encryptId']
                date_Today = tool.Time_stamp_to_date_to(li['releasedAt'])[:10]
                cont = li['content']
                if '测试' in title:
                    continue
                # print(title, url, date_Today)
                # time.sleep(666)
                if tool.Transformation(date) <= tool.Transformation(date_Today):
                    if tool.removal(title, date):
                        self.parse_detile(title, url, date, cont)
                    else:
                        print('【existence】', url)
                        continue
                else:
                    print('日期不符, 正在切换类型', date_Today, self.url)
                    self.url = self.url_list.pop(0)
                    page = 0
                    break
            if page == 5:
                self.url = self.url_list.pop(0)
                page = 0

    def parse_detile(self, title, url, date, cont):
        print(url)
        detail_html = cont
        detail_text = ''.join(re.findall('>(.*?)<', cont, re.S)).replace('\xa0', '').replace('\n', ''). \
            replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
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
        item['linkman'] = tool.get_linkman(detail_text)
        item['function'] = tool.get_function(detail_text)
        item['resource'] = '湖南省政府采购电子卖场'
        item['sheng'] = 9500
        item['nativeplace'] = self.get_nativeplace(title)
        item['shi'] = int(str(item['nativeplace']).split('.')[0])
        item['removal']= title
        process_item(item)

    def get_nativeplace(self, addr):
        city = ''
        city_list = [['9501', '长沙市'], ['9501.001', '芙蓉区'], ['9501.002', '天心区'], ['9501.003', '岳麓区'], ['9501.004', '开福区'], ['9501.005', '雨花区'], ['9501.006', '长沙县'], ['9501.007', '望城县'], ['9501.008', '宁乡县'], ['9501.009', '浏阳市'], ['9502', '株洲市'], ['9502.001', '荷塘区'], ['9502.002', '芦淞区'], ['9502.003', '石峰区'], ['9502.004', '天元区'], ['9502.005', '株洲县'], ['9502.006', '攸县'], ['9502.007', '茶陵县'], ['9502.008', '炎陵县'], ['9502.009', '醴陵市'], ['9503', '湘潭市'], ['9503.001', '雨湖区'], ['9503.002', '岳塘区'], ['9503.003', '湘潭县'], ['9503.004', '湘乡市'], ['9503.005', '韶山市'], ['9504', '衡阳市'], ['9504.001', '珠晖区'], ['9504.01', '祁东县'], ['9504.011', '耒阳市'], ['9504.012', '常宁市'], ['9504.002', '雁峰区'], ['9504.003', '石鼓区'], ['9504.004', '蒸湘区'], ['9504.005', '南岳区'], ['9504.006', '衡阳县'], ['9504.007', '衡南县'], ['9504.008', '衡山县'], ['9504.009', '衡东县'], ['9505', '邵阳市'], ['9505.001', '双清区'], ['9505.01', '新宁县'], ['9505.011', '城步苗族自治县'], ['9505.012', '武冈市'], ['9505.002', '大祥区'], ['9505.003', '北塔区'], ['9505.004', '邵东县'], ['9505.005', '新邵县'], ['9505.006', '邵阳县'], ['9505.007', '隆回县'], ['9505.008', '洞口县'], ['9505.009', '绥宁县'], ['9506', '岳阳市'], ['9506.001', '岳阳楼区'], ['9506.002', '云溪区'], ['9506.003', '君山区'], ['9506.004', '岳阳县'], ['9506.005', '华容县'], ['9506.006', '湘阴县'], ['9506.007', '平江县'], ['9506.008', '汨罗市'], ['9506.009', '临湘市'], ['9507', '常德市'], ['9507.001', '武陵区'], ['9507.002', '鼎城区'], ['9507.003', '安乡县'], ['9507.004', '汉寿县'], ['9507.005', '澧县'], ['9507.006', '临澧县'], ['9507.007', '桃源县'], ['9507.008', '石门县'], ['9507.009', '津市市'], ['9508', '张家界市'], ['9508.001', '永定区'], ['9508.002', '武陵源区'], ['9508.003', '慈利县'], ['9508.004', '桑植县'], ['9509', '益阳市'], ['9509.001', '资阳区'], ['9509.002', '赫山区'], ['9509.003', '南县'], ['9509.004', '桃江县'], ['9509.005', '安化县'], ['9509.006', '沅江市'], ['9510', '郴州市'], ['9510.001', '北湖区'], ['9510.01', '安仁县'], ['9510.011', '资兴市'], ['9510.002', '苏仙区'], ['9510.003', '桂阳县'], ['9510.004', '宜章县'], ['9510.005', '永兴县'], ['9510.006', '嘉禾县'], ['9510.007', '临武县'], ['9510.008', '汝城县'], ['9510.009', '桂东县'], ['9511', '永州市'], ['9511.001', '芝山区'], ['9511.01', '新田县'], ['9511.011', '江华瑶族自治县'], ['9511.002', '冷水滩区'], ['9511.003', '祁阳县'], ['9511.004', '东安县'], ['9511.005', '双牌县'], ['9511.006', '道县'], ['9511.007', '江永县'], ['9511.008', '宁远县'], ['9511.009', '蓝山县'], ['9512', '怀化市'], ['9512.001', '鹤城区'], ['9512.01', '靖州苗族侗族自治县'], ['9512.011', '通道侗族自治县'], ['9512.012', '洪江市'], ['9512.002', '中方县'], ['9512.003', '沅陵县'], ['9512.004', '辰溪县'], ['9512.005', '溆浦县'], ['9512.006', '会同县'], ['9512.007', '麻阳苗族自治县'], ['9512.008', '新晃侗族自治县'], ['9512.009', '芷江侗族自治县'], ['9513', '娄底市'], ['9513.001', '娄星区'], ['9513.002', '双峰县'], ['9513.003', '新化县'], ['9513.004', '冷水江市'], ['9513.005', '涟源市'], ['9514', '湘西土家族苗族自治州'], ['9514.001', '吉首市'], ['9514.002', '泸溪县'], ['9514.003', '凤凰县'], ['9514.004', '花垣县'], ['9514.005', '保靖县'], ['9514.006', '古丈县'], ['9514.007', '永顺县'], ['9514.008', '龙山县']]

        for i in city_list:
            if i[1] in addr:
                city = float(i[0])
                break
        if city == '':
            city = 9500
        return city

if __name__ == '__main__':
    import traceback,os
    try:
        jl = baoshan_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()



