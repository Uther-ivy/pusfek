# -*- coding: utf-8 -*-
import json
import re
import time, html
from lxml import etree
import tool
from save_database import process_item

# 福建榕卫招标有限公司
class alashan_ggzy:
    def __init__(self):
        self.url_code = [
            'http://www.fjrwzb.com/api/cmsplatform_SRW9QJJX/Biz_Q0AWQ8VG?columnId=68&page={}&row=15&keyWord=%E8%BE%93%E5%85%A5%E6%90%9C%E7%B4%A2%E5%85%B3%E9%94%AE%E8%AF%8D',
        ]
        self.url = self.url_code.pop(0)
        self.headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Cookie': 'isInitAreaCode=null; _gscu_653689772=78282348u2bs1g18; _gscbrs_653689772=1; UM_distinctid=16f78f570621fa-0e76a94f9f3d2d-e343166-1fa400-16f78f570631fc; _gscs_653689772=t782895054fvlkv12|pv:14; CNZZDATA1260595804=985342442-1578282342-%7C1578291895',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
        }

    def parse(self):
        date = tool.date
        # date = '2021-04-02'
        page = 0
        while True:
            page += 1
            print('*' * 20, page, '*' * 20)
            text = tool.requests_get(self.url.format(page), self.headers)
            # print(111, text)
            # time.sleep(666)
            detail = json.loads(text)['data']['list']
            for li in detail:
                title = li['title']
                url = 'http://www.fjrwzb.com/api/cmsplatform_DP7SUQGS/Biz_XCO794A6?contentId={}&columnId='.format(li['contentId'])
                date_Today = li['publishTime'][:10].replace('\r', '').replace('\t', '').replace(' ', '')
                # print(title, url, date_Today)
                # time.sleep(666)
                if tool.Transformation(date) <= tool.Transformation(date_Today):
                    if tool.removal(title, date):
                        self.parse_detile(title, url, date_Today)
                    else:
                        print('【existence】', url)
                        continue
                else:
                    print('日期不符, 正在切换类型...', date_Today)
                    self.url = self.url_code.pop(0)
                    page = 0
                    break
            if page == 20:
                self.url = self.url_code.pop(0)
                page = 0

    def parse_detile(self, title, url, date):
        print(url)
        url_text = tool.requests_get(url, self.headers)
        detail_html = json.loads(url_text)['data']['content']['content']
        detail_text = ''.join(re.findall('>(.*?)<', detail_html, re.S)).replace('\xa0', '').replace('\n', '').replace('\r', '').replace('\t',
                                                                                                                  '').replace(
            ' ', '').replace('\xa5', '')
        item = {}
        item['title'] = title.replace('\u2022', '')
        item['url'] = url
        item['date'] = date
        item['typeid'] = tool.get_typeid(item['title'])
        item['senddate'] = int(time.time())
        item['mid'] = 867
        item['nativeplace'] = self.get_nativeplace(item['title']+detail_text)
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
        item['resource'] = 'E招冀成'
        item['shi'] = int(str(item['nativeplace']).split('.')[0])
        item['sheng'] = 7000
        item['removal']= title
        process_item(item)
        # print(item['nativeplace'], item['title'])

    def get_nativeplace(self, addr):
        city_list = [['7001', '福州市'], ['7001.001', '鼓楼区'], ['7001.01', '永泰县'], ['7001.011', '平潭县'], ['7001.012', '福清市'], ['7001.013', '长乐市'], ['7001.002', '台江区'], ['7001.003', '仓山区'], ['7001.004', '马尾区'], ['7001.005', '晋安区'], ['7001.006', '闽侯县'], ['7001.007', '连江县'], ['7001.008', '罗源县'], ['7001.009', '闽清县'], ['7002', '厦门市'], ['7002.001', '思明区'], ['7002.002', '海沧区'], ['7002.003', '湖里区'], ['7002.004', '集美区'], ['7002.005', '同安区'], ['7002.006', '翔安区'], ['7003', '莆田市'], ['7003.001', '城厢区'], ['7003.002', '涵江区'], ['7003.003', '荔城区'], ['7003.004', '秀屿区'], ['7003.005', '仙游县'], ['7004', '三明市'], ['7004.001', '梅列区'], ['7004.01', '泰宁县'], ['7004.011', '建宁县'], ['7004.012', '永安市'], ['7004.002', '三元区'], ['7004.003', '明溪县'], ['7004.004', '清流县'], ['7004.005', '宁化县'], ['7004.006', '大田县'], ['7004.007', '尤溪县'], ['7004.008', '沙县'], ['7004.009', '将乐县'], ['7005', '泉州市'], ['7005.001', '鲤城区'], ['7005.01', '石狮市'], ['7005.011', '晋江市'], ['7005.012', '南安市'], ['7005.002', '丰泽区'], ['7005.003', '洛江区'], ['7005.004', '泉港区'], ['7005.005', '惠安县'], ['7005.006', '安溪县'], ['7005.007', '永春县'], ['7005.008', '德化县'], ['7005.009', '金门县'], ['7006', '漳州市'], ['7006.001', '芗城区'], ['7006.01', '华安县'], ['7006.011', '龙海市'], ['7006.002', '龙文区'], ['7006.003', '云霄县'], ['7006.004', '漳浦县'], ['7006.005', '诏安县'], ['7006.006', '长泰县'], ['7006.007', '东山县'], ['7006.008', '南靖县'], ['7006.009', '平和县'], ['7007', '南平市'], ['7007.001', '延平区'], ['7007.01', '建阳市'], ['7007.002', '顺昌县'], ['7007.003', '浦城县'], ['7007.004', '光泽县'], ['7007.005', '松溪县'], ['7007.006', '政和县'], ['7007.007', '邵武市'], ['7007.008', '武夷山市'], ['7007.009', '建瓯市'], ['7008', '龙岩市'], ['7008.001', '新罗区'], ['7008.002', '长汀县'], ['7008.003', '永定县'], ['7008.004', '上杭县'], ['7008.005', '武平县'], ['7008.006', '连城县'], ['7008.007', '漳平市'], ['7009', '宁德市'], ['7009.001', '蕉城区'], ['7009.002', '霞浦县'], ['7009.003', '古田县'], ['7009.004', '屏南县'], ['7009.005', '寿宁县'], ['7009.006', '周宁县'], ['7009.007', '柘荣县'], ['7009.008', '福安市'], ['7009.009', '福鼎市']]

        for i in city_list:
            if i[1] in addr:
                return float(i[0])
        return 7000

if __name__ == '__main__':
    import traceback, os
    try:
        jl = alashan_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
        if 'pop from empty list'!=str(e):
            print('报错')
            with open('error_name.txt', 'a+', encoding='utf-8')as f:
                f.write(str(os.path.basename(__file__)))
                f.write('\n')
                f.write(str(traceback.format_exc()))
                f.write('\n')
        else:
            with open('success.txt', 'a+', encoding='utf-8')as f:
                f.write(str(os.path.basename(__file__)))
                f.write('\n')
                f.write(str('无连接抓取'))
                f.write('\n')

