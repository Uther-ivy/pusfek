# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 安徽省政府采购网
class xinyang_ggzy:
    def __init__(self):
        self.url_list = [
            {"leaf":"0","categoryCode":"ZcyAnnouncement2","pageSize":"15","pageNo":"2"},
            {"categoryCode": "ZcyAnnouncement4", "pageSize": 15, "pageNo": 1},
            {"categoryCode": "ZcyAnnouncement3", "pageSize": 15, "pageNo": 1},
            {"categoryCode": "ZcyAnnouncement7", "pageSize": 15, "pageNo": 1},
            {"categoryCode": "ZcyAnnouncement3012", "pageSize": 15, "pageNo": 1}

        ]
        self.url = self.url_list.pop(0)
        self.headers = {
            "Content-Type": "application/json",
            'Accept': '*/*',
            'Host': 'www.ccgp-anhui.gov.cn',
            'Origin': 'http://www.ccgp-anhui.gov.cn',
            'Referer': 'http://www.ccgp-anhui.gov.cn/ZcyAnnouncement/ZcyAnnouncement2/index.html',
            'Cookie': '__utma=18145579.375948443.1639703249.1639703249.1639703249.1; __utmc=18145579; __utmz=18145579.1639703249.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmb=18145579.1.10.1639703249; wzws_cid=f90d5cef1b89aa8674f790409ef5a372a5e1d16c5f602596860f5ad81d55c9e87839ee7d4e9865bc6aa02910a71115dcce5684d2d241a4cd929854408a76a87f18eebc850df6401c1d3803d0ed99b08f',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
        }

    def parse(self):
        date = tool.date
        # date = '2021-07-29'
        page = 0
        index_url= 'http://www.ccgp-anhui.gov.cn/front/search/category'
        while True:
            page += 1
            self.url['pageNo'] = page
            text = tool.requests_post_to(index_url, self.url, self.headers)
            try:
                detail = json.loads(text)['hits']['hits']
            except:
                print(text)
                time.sleep(2222)
            print('*' * 20, page, '*' * 20)
            for li in detail:
                url = 'http://www.ccgp-anhui.gov.cn' + li['_source']['url']
                title = li['_source']['title']
                date_Today = tool.Time_stamp_to_date_to(li['_source']['publishDate'])[:10].replace('\n', '').replace('\t', '').replace('\r', '').replace(' ', '')\
                    .replace('[', '').replace(']', '')
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
                break

    def parse_detile(self, title, url, date):
        print(url)
        url_html = etree.HTML(tool.requests_get(url, self.headers))
        url_json = url_html.xpath('//*[@name="articleDetail"]/@value')[0]
        detail_html = json.loads(url_json)['content']
        detail_text = ''.join(re.findall('>(.*?)<', detail_html, re.S)) \
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
        item['address'] = tool.get_address(detail_text)
        item['nativeplace'] = self.get_nativeplace(item['title'])
        item['linkman'] = tool.get_linkman(detail_text)
        item['function'] = tool.get_function(detail_text)
        item['resource'] = '安徽省政府采购网'
        item["shi"] = int(str(item["nativeplace"]).split('.')[0])
        item['sheng'] = 6500
        item['removal']= title
        process_item(item)
        # print(item['body'])

    def get_nativeplace(self, addr):
        city = ''
        city_list = [['6501', '合肥'], ['6501.001', '瑶海'], ['6501.002', '庐阳'], ['6501.003', '蜀山'], ['6501.004', '包河'], ['6501.005', '长丰'], ['6501.006', '肥东'], ['6501.007', '肥西'], ['6502', '芜湖'], ['6502.001', '镜湖'], ['6502.002', '马塘'], ['6502.003', '新芜'], ['6502.004', '鸠江'], ['6502.005', '芜湖'], ['6502.006', '繁昌'], ['6502.007', '南陵'], ['6503', '蚌埠'], ['6503.001', '龙子湖'], ['6503.002', '蚌山'], ['6503.003', '禹会'], ['6503.004', '淮上'], ['6503.005', '怀远'], ['6503.006', '五河'], ['6503.007', '固镇'], ['6504', '淮南'], ['6504.001', '大通'], ['6504.002', '田家庵'], ['6504.003', '谢家集'], ['6504.004', '八公山'], ['6504.005', '潘集'], ['6504.006', '凤台'], ['6505', '马鞍山'], ['6505.001', '金家庄'], ['6505.002', '花山'], ['6505.003', '雨山'], ['6505.004', '当涂'], ['6506', '淮北'], ['6506.001', '杜集'], ['6506.002', '相山'], ['6506.003', '烈山'], ['6506.004', '濉溪'], ['6507', '铜陵'], ['6507.001', '铜官山'], ['6507.002', '狮子山'], ['6507.003', '郊'], ['6507.004', '铜陵'], ['6508', '安庆'], ['6508.001', '迎江'], ['6508.01', '岳西'], ['6508.011', '桐城'], ['6508.002', '大观'], ['6508.003', '郊'], ['6508.004', '怀宁'], ['6508.005', '枞阳'], ['6508.006', '潜山'], ['6508.007', '太湖'], ['6508.008', '宿松'], ['6508.009', '望江'], ['6509', '黄山'], ['6509.001', '屯溪'], ['6509.002', '黄山'], ['6509.003', '徽州'], ['6509.004', '歙'], ['6509.005', '休宁'], ['6509.006', '黟'], ['6509.007', '祁门'], ['6510', '滁州'], ['6510.001', '琅琊'], ['6510.002', '南谯'], ['6510.003', '来安'], ['6510.004', '全椒'], ['6510.005', '定远'], ['6510.006', '凤阳'], ['6510.007', '天长'], ['6510.008', '明光'], ['6511', '阜阳'], ['6511.001', '颍州'], ['6511.002', '颍东'], ['6511.003', '颍泉'], ['6511.004', '临泉'], ['6511.005', '太和'], ['6511.006', '阜南'], ['6511.007', '颍上'], ['6511.008', '界首'], ['6512', '宿州'], ['6512.001', '墉桥'], ['6512.002', '砀山'], ['6512.003', '萧'], ['6512.004', '灵璧'], ['6512.005', '泗'], ['6513', '巢湖'], ['6513.001', '居巢'], ['6513.002', '庐江'], ['6513.003', '无为'], ['6513.004', '含山'], ['6513.005', '和'], ['6514', '六安'], ['6514.001', '金安'], ['6514.002', '裕安'], ['6514.003', '寿'], ['6514.004', '霍邱'], ['6514.005', '舒城'], ['6514.006', '金寨'], ['6514.007', '霍山'], ['6515', '亳州'], ['6515.001', '谯城'], ['6515.002', '涡阳'], ['6515.003', '蒙城'], ['6515.004', '利辛'], ['6516', '池州'], ['6516.001', '贵池'], ['6516.002', '东至'], ['6516.003', '石台'], ['6516.004', '青阳'], ['6517', '宣城'], ['6517.001', '宣州'], ['6517.002', '郎溪'], ['6517.003', '广德'], ['6517.004', '泾'], ['6517.005', '绩溪'], ['6517.006', '旌德']]

        for i in city_list:
            if i[1] in addr:
                city = float(i[0])
                break
        if city == '':
            city = 6500
        return city

if __name__ == '__main__':
    import traceback, os
    try:
        jl = xinyang_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
