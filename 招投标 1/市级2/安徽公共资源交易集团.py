# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 安徽公共资源交易集团
class xinyang_ggzy:
    def __init__(self):
        self.url_list = [
            'http://www.ahggzyjt.com/jyxx/002001/002001001/{}.html',
            'http://www.ahggzyjt.com/jyxx/002002/002002001/{}.html',
            'http://www.ahggzyjt.com/jyxx/002003/002003001/{}.html'
        ]
        self.url = self.url_list.pop(0)
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        }

    def parse(self):
        date = tool.date
        # date = '2020-07-10'
        page = 0
        while True:
            page += 1
            if page == 1:
                text = tool.requests_get(self.url.format('secondPage'), self.headers)
            else:
                text = tool.requests_get(self.url.format(page), self.headers)
            html = HTML(text)
            # print(11, text)
            # time.sleep(666)
            detail = html.xpath('//*[@id="right"]/ul/li')
            print('*' * 20, page, '*' * 20)
            for li in detail:
                title = li.xpath('./a/text()')[0]
                url = 'http://www.ahggzyjt.com' + li.xpath('./a/@href')[0]
                date_Today = li.xpath('./span/text()')[0].replace('\n', '').replace('\t', '').replace('\r', '').replace(' ', '')
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
        url_html = etree.HTML(tool.requests_get(url, self.headers))
        detail = url_html.xpath('/html/body/div[2]/div[2]/div/div/div')[0]
        detail_html = etree.tostring(detail, method='HTML')
        detail_html = html.unescape(detail_html.decode()).replace('\xa0', '').replace('\ufeff', '')
        detail_text = url_html.xpath('string(/html/body/div[2]/div[2]/div/div/div)') \
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
        item['nativeplace'] = self.get_nativeplace(item['title'])
        item['linkman'] = tool.get_linkman(detail_text)
        item['function'] = tool.get_function(detail_text)
        item['resource'] = '安徽公共资源交易集团'
        item["shi"] = int(str(item["nativeplace"]).split('.')[0])
        item['sheng'] = 6500
        item['removal']= title
        process_item(item)
        # print(item['body'])

    def get_nativeplace(self, city):
        a = ''
        ls = [['6501', '合肥'], ['6501.001', '瑶海区'], ['6501.002', '庐阳区'], ['6501.003', '蜀山区'], ['6501.004', '包河区'], ['6501.005', '长丰县'], ['6501.006', '肥东县'], ['6501.007', '肥西县'], ['6502', '芜湖'], ['6502.001', '镜湖区'], ['6502.002', '马塘区'], ['6502.003', '新芜区'], ['6502.004', '鸠江区'], ['6502.005', '芜湖县'], ['6502.006', '繁昌县'], ['6502.007', '南陵县'], ['6503', '蚌埠'], ['6503.001', '龙子湖区'], ['6503.002', '蚌山区'], ['6503.003', '禹会区'], ['6503.004', '淮上区'], ['6503.005', '怀远县'], ['6503.006', '五河县'], ['6503.007', '固镇县'], ['6504', '淮南'], ['6504.001', '大通区'], ['6504.002', '田家庵区'], ['6504.003', '谢家集区'], ['6504.004', '八公山区'], ['6504.005', '潘集区'], ['6504.006', '凤台县'], ['6505', '马鞍山'], ['6505.001', '金家庄区'], ['6505.002', '花山区'], ['6505.003', '雨山区'], ['6505.004', '当涂县'], ['6506', '淮北'], ['6506.001', '杜集区'], ['6506.002', '相山区'], ['6506.003', '烈山区'], ['6506.004', '濉溪县'], ['6507', '铜陵'], ['6507.001', '铜官山区'], ['6507.002', '狮子山区'], ['6507.003', '郊区'], ['6507.004', '铜陵县'], ['6508', '安庆'], ['6508.001', '迎江区'], ['6508.01', '岳西县'], ['6508.011', '桐城'], ['6508.002', '大观区'], ['6508.003', '郊区'], ['6508.004', '怀宁县'], ['6508.005', '枞阳县'], ['6508.006', '潜山县'], ['6508.007', '太湖县'], ['6508.008', '宿松县'], ['6508.009', '望江县'], ['6509', '黄山'], ['6509.001', '屯溪区'], ['6509.002', '黄山区'], ['6509.003', '徽州区'], ['6509.004', '歙县'], ['6509.005', '休宁县'], ['6509.006', '黟县'], ['6509.007', '祁门县'], ['6510', '滁州'], ['6510.001', '琅琊区'], ['6510.002', '南谯区'], ['6510.003', '来安县'], ['6510.004', '全椒县'], ['6510.005', '定远县'], ['6510.006', '凤阳县'], ['6510.007', '天长'], ['6510.008', '明光'], ['6511', '阜阳'], ['6511.001', '颍州区'], ['6511.002', '颍东区'], ['6511.003', '颍泉区'], ['6511.004', '临泉县'], ['6511.005', '太和县'], ['6511.006', '阜南县'], ['6511.007', '颍上县'], ['6511.008', '界首'], ['6512', '宿州'], ['6512.001', '墉桥区'], ['6512.002', '砀山县'], ['6512.003', '萧县'], ['6512.004', '灵璧县'], ['6512.005', '泗县'], ['6513', '巢湖'], ['6513.001', '居巢区'], ['6513.002', '庐江县'], ['6513.003', '无为县'], ['6513.004', '含山县'], ['6513.005', '和县'], ['6514', '六安'], ['6514.001', '金安区'], ['6514.002', '裕安区'], ['6514.003', '寿县'], ['6514.004', '霍邱县'], ['6514.005', '舒城县'], ['6514.006', '金寨县'], ['6514.007', '霍山县'], ['6515', '亳州'], ['6515.001', '谯城区'], ['6515.002', '涡阳县'], ['6515.003', '蒙城县'], ['6515.004', '利辛县'], ['6516', '池州'], ['6516.001', '贵池区'], ['6516.002', '东至县'], ['6516.003', '石台县'], ['6516.004', '青阳县'], ['6517', '宣城'], ['6517.001', '宣州区'], ['6517.002', '郎溪县'], ['6517.003', '广德县'], ['6517.004', '泾县'], ['6517.005', '绩溪县'], ['6517.006', '旌德县'], ['6517.007', '宁国']]
        for i in ls:
            if i[1] in city:
                a = i[0]
                break
        if a == '':
            return 6500
        else:
            return a

if __name__ == '__main__':
    import traceback, os
    try:
        jl = xinyang_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
        tool.send_error('报错文件：'+str(os.path.basename(__file__))+'报错信息：'+str(e))



