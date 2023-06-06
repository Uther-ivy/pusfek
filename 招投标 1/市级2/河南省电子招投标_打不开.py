# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 河南省电子招投标
class xinyang_ggzy:
    def __init__(self):
        self.url_list = [
            'http://hndzzbtb.hndrc.gov.cn/services/hl/getSelect?response=application/json&pageIndex={}&pageSize=22&'
            'day=&sheng=x1&qu=&xian=&title=&timestart=&timeend=&categorynum=002001001&siteguid=3955b792-fb32-4dc1-8935-49ad516ae6db',
            'http://hndzzbtb.hndrc.gov.cn/services/hl/getSelect?response=application/json&pageIndex={}&pageSize=22'
            '&day=&sheng=x1&qu=&xian=&title=&timestart=&timeend=&categorynum=002002001&siteguid=3955b792-fb32-4dc1-8935-49ad516ae6db'
        ]
        self.url = self.url_list.pop(0)
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        }

    def parse(self):
        date = tool.date
        # date = '2021-07-19'
        page = 0
        while True:
            page += 1
            text = tool.requests_get(self.url.format(page), self.headers)
            print('*' * 20, page, '*' * 20)
            # print(html.xpath('//div[@class="AAA"]/div[1]/text()')[0])
            # print(11, data)
            # time.sleep(6666)
            detail = json.loads(json.loads(text)['return'])['Table']
            for li in detail:
                title = li['title']
                url = 'http://hndzzbtb.hndrc.gov.cn' + li['href']
                date_Today = li['infodate'].replace('\n', '').replace('\t', '').replace('\r', '')\
                    .replace(' ', '').replace('/', '-')
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
                page = 0

    def parse_detile(self, title, url, date):
        print(url)
        url_html = etree.HTML(tool.requests_get(url, self.headers))
        try:
            detail = url_html.xpath('/html/body/div[2]/div[2]/div[1]/div[2]')[0]
            detail_html = etree.tostring(detail, method='HTML')
            detail_html = html.unescape(detail_html.decode()).replace('\xa0', '').replace('\ufeff', '')
            detail_text = url_html.xpath('string(/html/body/div[2]/div[2]/div[1]/div[2])') \
                .replace('\xa0', '').replace('\n', '').replace('\r', '').replace('\t', '') \
                .replace(' ', '').replace('\xa5', '').replace('\ufeff', '')
            if len(detail_html) < 200:
                int('a')
        except:
            detail = url_html.xpath('//*[@class="ewb-left-bd"]')[0]
            detail_html = etree.tostring(detail, method='HTML')
            detail_html = html.unescape(detail_html.decode()).replace('\xa0', '').replace('\ufeff', '')
            detail_text = url_html.xpath('string(//*[@class="ewb-left-bd"])') \
                .replace('\xa0', '').replace('\n', '').replace('\r', '').replace('\t', '') \
                .replace(' ', '').replace('\xa5', '').replace('\ufeff', '')
            if len(detail_html) < 200:
                int('a')
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
        item['body'] = detail_html
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
        item['resource'] = '河南省电子招投标'
        item['shi'] = int(item['nativeplace'])
        item['sheng'] = 8500
        item['removal']= title
        process_item(item)
        # print(item['body'])

    def get_nativeplace(self, addr):
        city = ''
        city_list = [['8501', '郑州'], ['8501.001', '中原'], ['8501.01', '新密'], ['8501.011', '新郑'], ['8501.012', '登封'], ['8501.002', '二七'], ['8501.003', '管城回族'], ['8501.004', '金水'], ['8501.005', '上街'], ['8501.006', '邙山'], ['8501.007', '中牟'], ['8501.008', '巩义'], ['8501.009', '荥阳'], ['8502', '开封'], ['8502.001', '龙亭'], ['8502.01', '兰考'], ['8502.002', '顺河回族'], ['8502.003', '鼓楼'], ['8502.004', '南关'], ['8502.005', '郊'], ['8502.006', '杞'], ['8502.007', '通许'], ['8502.008', '尉氏'], ['8502.009', '开封'], ['8503', '洛阳'], ['8503.001', '老城'], ['8503.01', '嵩'], ['8503.011', '汝阳'], ['8503.012', '宜阳'], ['8503.013', '洛宁'], ['8503.014', '伊川'], ['8503.015', '偃师'], ['8503.002', '西工'], ['8503.003', '廛河回族'], ['8503.004', '涧西'], ['8503.005', '吉利'], ['8503.006', '洛龙'], ['8503.007', '孟津'], ['8503.008', '新安'], ['8503.009', '栾川'], ['8504', '平顶山'], ['8504.001', '新华'], ['8504.01', '汝州'], ['8504.002', '卫东'], ['8504.003', '石龙'], ['8504.004', '湛河'], ['8504.005', '宝丰'], ['8504.006', '叶'], ['8504.007', '鲁山'], ['8504.008', '郏'], ['8504.009', '舞钢'], ['8505', '安阳'], ['8505.001', '文峰'], ['8505.002', '北关'], ['8505.003', '殷都'], ['8505.004', '龙安'], ['8505.005', '安阳'], ['8505.006', '汤阴'], ['8505.007', '滑'], ['8505.008', '内黄'], ['8505.009', '林州'], ['8506', '鹤壁'], ['8506.001', '鹤山'], ['8506.002', '山城'], ['8506.003', '淇滨'], ['8506.004', '浚'], ['8506.005', '淇'], ['8507', '新乡'], ['8507.001', '红旗'], ['8507.01', '长垣'], ['8507.011', '卫辉'], ['8507.012', '辉'], ['8507.002', '卫滨'], ['8507.003', '凤泉'], ['8507.004', '牧野'], ['8507.005', '新乡'], ['8507.006', '获嘉'], ['8507.007', '原阳'], ['8507.008', '延津'], ['8507.009', '封丘'], ['8508', '焦作'], ['8508.001', '解放'], ['8508.01', '沁阳'], ['8508.011', '孟州'], ['8508.002', '中站'], ['8508.003', '马村'], ['8508.004', '山阳'], ['8508.005', '修武'], ['8508.006', '博爱'], ['8508.007', '武陟'], ['8508.008', '温'], ['8508.009', '济源'], ['8509', '濮阳'], ['8509.001', '华龙'], ['8509.002', '清丰'], ['8509.003', '南乐'], ['8509.004', '范'], ['8509.005', '台前'], ['8509.006', '濮阳'], ['8510', '许昌'], ['8510.001', '魏都'], ['8510.002', '许昌'], ['8510.003', '鄢陵'], ['8510.004', '襄城'], ['8510.005', '禹州'], ['8510.006', '长葛'], ['8511', '漯河'], ['8511.001', '源汇'], ['8511.002', '郾城'], ['8511.003', '召陵'], ['8511.004', '舞阳'], ['8511.005', '临颍'], ['8512', '三门峡'], ['8512.001', '湖滨'], ['8512.002', '渑池'], ['8512.003', '陕'], ['8512.004', '卢氏'], ['8512.005', '义马'], ['8512.006', '灵宝'], ['8513', '南阳'], ['8513.001', '宛城'], ['8513.01', '唐河'], ['8513.011', '新野'], ['8513.012', '桐柏'], ['8513.013', '邓州'], ['8513.002', '卧龙'], ['8513.003', '南召'], ['8513.004', '方城'], ['8513.005', '西峡'], ['8513.006', '镇平'], ['8513.007', '内乡'], ['8513.008', '淅川'], ['8513.009', '社旗'], ['8514', '商丘'], ['8514.001', '梁园'], ['8514.002', '睢阳'], ['8514.003', '民权'], ['8514.004', '睢'], ['8514.005', '宁陵'], ['8514.006', '柘城'], ['8514.007', '虞城'], ['8514.008', '夏邑'], ['8514.009', '永城'], ['8515', '信阳'], ['8515.001', '师河'], ['8515.01', '息'], ['8515.002', '平桥'], ['8515.003', '罗山'], ['8515.004', '光山'], ['8515.005', '新'], ['8515.006', '商城'], ['8515.007', '固始'], ['8515.008', '潢川'], ['8515.009', '淮滨'], ['8516', '周口'], ['8516.001', '川汇'], ['8516.01', '项城'], ['8516.002', '扶沟'], ['8516.003', '西华'], ['8516.004', '商水'], ['8516.005', '沈丘'], ['8516.006', '郸城'], ['8516.007', '淮阳'], ['8516.008', '太康'], ['8516.009', '鹿邑'], ['8517', '驻马店'], ['8517.001', '驿城'], ['8517.01', '新蔡'], ['8517.002', '西平'], ['8517.003', '上蔡'], ['8517.004', '平舆'], ['8517.005', '正阳'], ['8517.006', '确山'], ['8517.007', '泌阳'], ['8517.008', '汝南']]

        for i in city_list:
            if i[1] in addr:
                city = float(i[0])
                break
        if city == '':
            city = 8500
        return city

if __name__ == '__main__':

    import traceback, os
    try:
        jl = xinyang_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
        tool.send_error('报错文件：'+str(os.path.basename(__file__))+'报错信息：'+str(e))


