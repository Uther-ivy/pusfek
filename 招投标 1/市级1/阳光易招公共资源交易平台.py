# -*- coding: utf-8 -*-
import json
import re
import time, html
from lxml import etree
import tool
from save_database import process_item

# 阳光易招公共资源交易平台
class alashan_ggzy:
    def __init__(self):
        self.url_code = []
        self.headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Cookie': 'isInitAreaCode=null; _gscu_653689772=78282348u2bs1g18; _gscbrs_653689772=1; UM_distinctid=16f78f570621fa-0e76a94f9f3d2d-e343166-1fa400-16f78f570631fc; _gscs_653689772=t782895054fvlkv12|pv:14; CNZZDATA1260595804=985342442-1578282342-%7C1578291895',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
        }
        u = 'http://www.sunbidding.com/jyxx/index.jhtml'
        r = etree.HTML(tool.requests_g(u, self.headers)).xpath('/html/body/div[9]/div[1]/div[1]/dl')
        for i in r:
            for j in i.xpath('./dd'):
                self.url_code.append('http://www.sunbidding.com'+j.xpath('./a/@href')[0])
        self.url = self.url_code.pop(0)

    def parse(self):
        date = tool.date
        # date = '2020-01-06'
        page = 0
        while True:
            page += 1
            print('*' * 20, page, '*' * 20)
            if page == 1:
                text = tool.requests_g(self.url, self.headers)
            else:
                text = tool.requests_g(self.url.replace('index', 'index_'+str(page)), self.headers)
            # print(111, text)
            # time.sleep(666)
            detail = etree.HTML(text).xpath('/html/body/div/div[5]/div[2]/div/div[2]/ul/li')
            if len(detail) == 0:
                print('内容为空, 正在切换类型...', self.url)
                self.url = self.url_code.pop(0)
                page = 0
                continue
            for li in detail:
                title = li.xpath('./a/@title')[0]
                url = 'http://www.sunbidding.com' + li.xpath('./a/@href')[0]
                date_Today = li.xpath('./a/em/text()')[0].replace('\r', '').replace('\t', '').replace(' ', '')
                # print(title, url, date_Today)
                # time.sleep(666)
                if tool.Transformation(date) <= tool.Transformation(date_Today):
                    if tool.removal(title, date):
                        self.parse_detile(title, url, date_Today)
                    else:
                        print('【existence】', url)
                        continue
                else:
                    print('日期不符, 正在切换类型...', date_Today, self.url)
                    self.url = self.url_code.pop(0)
                    page = 0
                    break


    def parse_detile(self, title, url, date):
        print(url)
        url_text = tool.requests_get(url, self.headers)
        url_html = etree.HTML(url_text)
        detail = url_html.xpath('/html/body/div/div[5]/div[2]/div')[0]
        detail_html = etree.tostring(detail, method='HTML')
        detail_html = html.unescape(detail_html.decode())
        detail_text = url_html.xpath('string(/html/body/div/div[5]/div[2]/div)').replace('\xa0', '').replace('\n', '').replace('\r', '').replace('\t',
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
        item['winner'] = tool.get_winner(detail_text)
        item['address'] = tool.get_address(detail_text)
        item['linkman'] = tool.get_linkman(detail_text)
        item['function'] = tool.get_function(detail_text)
        item['resource'] = '阳光易招公共资源交易平台'
        item['shi'] = int(str(item['nativeplace']).split('.')[0])
        item['sheng'] = 8500
        item['removal']= title
        process_item(item)
        # print(item['nativeplace'], item['title'])

    def get_nativeplace(self, addr):
        city_list = [['8501', '郑州市'], ['8501.001', '中原区'], ['8501.01', '新密市'], ['8501.011', '新郑市'], ['8501.012', '登封市'], ['8501.002', '二七区'], ['8501.003', '管城回族区'], ['8501.004', '金水区'], ['8501.005', '上街区'], ['8501.006', '邙山区'], ['8501.007', '中牟县'], ['8501.008', '巩义市'], ['8501.009', '荥阳市'], ['8502', '开封市'], ['8502.001', '龙亭区'], ['8502.01', '兰考县'], ['8502.002', '顺河回族区'], ['8502.003', '鼓楼区'], ['8502.004', '南关区'], ['8502.005', '郊区'], ['8502.006', '杞县'], ['8502.007', '通许县'], ['8502.008', '尉氏县'], ['8502.009', '开封县'], ['8503', '洛阳市'], ['8503.001', '老城区'], ['8503.01', '嵩县'], ['8503.011', '汝阳县'], ['8503.012', '宜阳县'], ['8503.013', '洛宁县'], ['8503.014', '伊川县'], ['8503.015', '偃师市'], ['8503.002', '西工区'], ['8503.003', '廛河回族区'], ['8503.004', '涧西区'], ['8503.005', '吉利区'], ['8503.006', '洛龙区'], ['8503.007', '孟津县'], ['8503.008', '新安县'], ['8503.009', '栾川县'], ['8504', '平顶山市'], ['8504.001', '新华区'], ['8504.01', '汝州市'], ['8504.002', '卫东区'], ['8504.003', '石龙区'], ['8504.004', '湛河区'], ['8504.005', '宝丰县'], ['8504.006', '叶县'], ['8504.007', '鲁山县'], ['8504.008', '郏县'], ['8504.009', '舞钢市'], ['8505', '安阳市'], ['8505.001', '文峰区'], ['8505.002', '北关区'], ['8505.003', '殷都区'], ['8505.004', '龙安区'], ['8505.005', '安阳县'], ['8505.006', '汤阴县'], ['8505.007', '滑县'], ['8505.008', '内黄县'], ['8505.009', '林州市'], ['8506', '鹤壁市'], ['8506.001', '鹤山区'], ['8506.002', '山城区'], ['8506.003', '淇滨区'], ['8506.004', '浚县'], ['8506.005', '淇县'], ['8507', '新乡市'], ['8507.001', '红旗区'], ['8507.01', '长垣县'], ['8507.011', '卫辉市'], ['8507.012', '辉县市'], ['8507.002', '卫滨区'], ['8507.003', '凤泉区'], ['8507.004', '牧野区'], ['8507.005', '新乡县'], ['8507.006', '获嘉县'], ['8507.007', '原阳县'], ['8507.008', '延津县'], ['8507.009', '封丘县'], ['8508', '焦作市'], ['8508.001', '解放区'], ['8508.01', '沁阳市'], ['8508.011', '孟州市'], ['8508.002', '中站区'], ['8508.003', '马村区'], ['8508.004', '山阳区'], ['8508.005', '修武县'], ['8508.006', '博爱县'], ['8508.007', '武陟县'], ['8508.008', '温县'], ['8508.009', '济源市'], ['8509', '濮阳市'], ['8509.001', '华龙区'], ['8509.002', '清丰县'], ['8509.003', '南乐县'], ['8509.004', '范县'], ['8509.005', '台前县'], ['8509.006', '濮阳县'], ['8510', '许昌市'], ['8510.001', '魏都区'], ['8510.002', '许昌县'], ['8510.003', '鄢陵县'], ['8510.004', '襄城县'], ['8510.005', '禹州市'], ['8510.006', '长葛市'], ['8511', '漯河市'], ['8511.001', '源汇区'], ['8511.002', '郾城区'], ['8511.003', '召陵区'], ['8511.004', '舞阳县'], ['8511.005', '临颍县'], ['8512', '三门峡市'], ['8512.001', '湖滨区'], ['8512.002', '渑池县'], ['8512.003', '陕县'], ['8512.004', '卢氏县'], ['8512.005', '义马市'], ['8512.006', '灵宝市'], ['8513', '南阳市'], ['8513.001', '宛城区'], ['8513.01', '唐河县'], ['8513.011', '新野县'], ['8513.012', '桐柏县'], ['8513.013', '邓州市'], ['8513.002', '卧龙区'], ['8513.003', '南召县'], ['8513.004', '方城县'], ['8513.005', '西峡县'], ['8513.006', '镇平县'], ['8513.007', '内乡县'], ['8513.008', '淅川县'], ['8513.009', '社旗县'], ['8514', '商丘市'], ['8514.001', '梁园区'], ['8514.002', '睢阳区'], ['8514.003', '民权县'], ['8514.004', '睢县'], ['8514.005', '宁陵县'], ['8514.006', '柘城县'], ['8514.007', '虞城县'], ['8514.008', '夏邑县'], ['8514.009', '永城市'], ['8515', '信阳市'], ['8515.001', '师河区'], ['8515.01', '息县'], ['8515.002', '平桥区'], ['8515.003', '罗山县'], ['8515.004', '光山县'], ['8515.005', '新县'], ['8515.006', '商城县'], ['8515.007', '固始县'], ['8515.008', '潢川县'], ['8515.009', '淮滨县'], ['8516', '周口市'], ['8516.001', '川汇区'], ['8516.01', '项城市'], ['8516.002', '扶沟县'], ['8516.003', '西华县'], ['8516.004', '商水县'], ['8516.005', '沈丘县'], ['8516.006', '郸城县'], ['8516.007', '淮阳县'], ['8516.008', '太康县'], ['8516.009', '鹿邑县'], ['8517', '驻马店市'], ['8517.001', '驿城区'], ['8517.01', '新蔡县'], ['8517.002', '西平县'], ['8517.003', '上蔡县'], ['8517.004', '平舆县'], ['8517.005', '正阳县'], ['8517.006', '确山县'], ['8517.007', '泌阳县'], ['8517.008', '汝南县'], ['8517.009', '遂平县']]

        for i in city_list:
            if i[1] in addr:
                return float(i[0])
        return 8500

if __name__ == '__main__':
    import traceback, os
    try:
        jl = alashan_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
