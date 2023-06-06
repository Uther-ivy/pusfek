# -*- coding: utf-8 -*-
import json
import re
import time, html
from lxml import etree
import tool
from save_database import process_item

# 湖北省电子招投标交易平台
class alashan_ggzy:
    def __init__(self):
        self.url_code = [
            'http://www.hbbidcloud.com/hubei/jyxx/{}.html'
        ]
        self.url = self.url_code.pop(0)
        self.headers = {
            'Accept': '*/*',
            'Cookie': 'isInitAreaCode=null; _gscu_653689772=78282348u2bs1g18; _gscbrs_653689772=1; UM_distinctid=16f78f570621fa-0e76a94f9f3d2d-e343166-1fa400-16f78f570631fc; _gscs_653689772=t782895054fvlkv12|pv:14; CNZZDATA1260595804=985342442-1578282342-%7C1578291895',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
        }

    def parse(self):
        date = tool.date
        # date = '2021-04-15'
        page = 0
        while True:
            page += 1
            print('*' * 20, page, '*' * 20)
            if page == 1:
                text = tool.requests_get(self.url.format('about'), self.headers)
            else:
                text = tool.requests_get(self.url.format(page), self.headers)
            # print(111, text)
            # time.sleep(666)
            detail = etree.HTML(text).xpath('//*[@id="main"]/div/div[2]/ul/li')
            for li in detail:
                title = li.xpath('./div/a/@title')[0]
                url = 'http://www.hbbidcloud.com/' + li.xpath('./div/a/@href')[0]
                date_Today = li.xpath('./span/text()')[0].replace('\r', '').replace('\t', '').replace(' ', '')
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
        url_html = etree.HTML(url_text)
        try:
            detail = url_html.xpath('//*[@id="infoContentM"]/table')[0]
            detail_html = etree.tostring(detail, method='HTML')
            detail_html = html.unescape(detail_html.decode())
            detail_text = url_html.xpath('string(//*[@id="infoContentM"]/table)').replace('\xa0', '').replace('\n',
                                                                                                                             '').replace(
                '\r', '').replace('\t',
                                  '').replace(
                ' ', '').replace('\xa5', '')
        except:
            detail = url_html.xpath('//*[@id="infoContentM"]')[0]
            detail_html = etree.tostring(detail, method='HTML')
            detail_html = html.unescape(detail_html.decode())
            detail_text = url_html.xpath('string(//*[@id="infoContentM"])').replace('\xa0', '').replace('\n',
                                                                                                              '').replace(
                '\r', '').replace('\t',
                                  '').replace(
                ' ', '').replace('\xa5', '')
        item = {}
        item['title'] = title.replace('\u2022', '')
        item['url'] = url
        item['date'] = date
        item['typeid'] = tool.get_typeid(item['title'])
        item['senddate'] = int(time.time())
        item['mid'] = 867
        item['nativeplace'] = float(self.get_nativeplace(item['title']+detail_text))
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
        item['resource'] = '湖北省电子招投标交易平台'
        item['shi'] = int(item['nativeplace'])
        item['sheng'] = 9000
        item['removal']= title
        process_item(item)
        # print(item['nativeplace'], item['title'])

    def get_nativeplace(self, addr):
        city_list = [['9001', '武汉市'], ['9001.001', '江岸区'], ['9001.01', '蔡甸区'], ['9001.011', '江夏区'], ['9001.012', '黄陂区'], ['9001.013', '新洲区'], ['9001.002', '江汉区'], ['9001.003', '乔口区'], ['9001.004', '汉阳区'], ['9001.005', '武昌区'], ['9001.006', '青山区'], ['9001.007', '洪山区'], ['9001.008', '东西湖区'], ['9001.009', '汉南区'], ['9002', '黄石市'], ['9002.001', '黄石港区'], ['9002.002', '西塞山区'], ['9002.003', '下陆区'], ['9002.004', '铁山区'], ['9002.005', '阳新县'], ['9002.006', '大冶市'], ['9003', '十堰市'], ['9003.001', '茅箭区'], ['9003.002', '张湾区'], ['9003.003', '郧县'], ['9003.004', '郧西县'], ['9003.005', '竹山县'], ['9003.006', '竹溪县'], ['9003.007', '房县'], ['9003.008', '丹江口市'], ['9004', '宜昌市'], ['9004.001', '西陵区'], ['9004.01', '五峰土家族自治县'], ['9004.011', '宜都市'], ['9004.012', '当阳市'], ['9004.013', '枝江市'], ['9004.002', '伍家岗区'], ['9004.003', '点军区'], ['9004.004', '?亭区'], ['9004.005', '夷陵区'], ['9004.006', '远安县'], ['9004.007', '兴山县'], ['9004.008', '秭归县'], ['9004.009', '长阳土家族自治县'], ['9005', '襄樊市'], ['9005.001', '襄城区'], ['9005.002', '樊城区'], ['9005.003', '襄阳区'], ['9005.004', '南漳县'], ['9005.005', '谷城县'], ['9005.006', '保康县'], ['9005.007', '老河口市'], ['9005.008', '枣阳市'], ['9005.009', '宜城市'], ['9006', '鄂州市'], ['9006.001', '梁子湖区'], ['9006.002', '华容区'], ['9006.003', '鄂城区'], ['9007', '荆门市'], ['9007.001', '钟祥市'], ['9007.002', '沙洋县'], ['9007.003', '京山县'], ['9007.004', '掇刀区'], ['9007.005', '东宝区'], ['9008', '孝感市'], ['9008.001', '安陆市'], ['9008.002', '应城市'], ['9008.003', '云梦县'], ['9008.004', '大悟县'], ['9008.005', '孝昌县'], ['9008.006', '孝南区'], ['9008.007', '汉川市'], ['9009', '荆州市'], ['9009.001', '沙市区'], ['9009.002', '荆州区'], ['9009.003', '公安县'], ['9009.004', '监利县'], ['9009.005', '江陵县'], ['9009.006', '石首市'], ['9009.007', '洪湖市'], ['9009.008', '松滋市'], ['9010', '黄冈市'], ['9010.001', '州区'], ['9010.01', '武穴市'], ['9010.002', '团风县'], ['9010.003', '红安县'], ['9010.004', '罗田县'], ['9010.005', '英山县'], ['9010.006', '浠水县'], ['9010.007', '蕲春县'], ['9010.008', '黄梅县'], ['9010.009', '麻城市'], ['9011', '咸宁市'], ['9011.001', '咸安区'], ['9011.002', '嘉鱼县'], ['9011.003', '通城县'], ['9011.004', '崇阳县'], ['9011.005', '通山县'], ['9011.006', '赤壁市'], ['9012', '随州市'], ['9012.001', '曾都区'], ['9012.002', '广水市'], ['9013', '恩施土家族苗族自治州'], ['9013.001', '恩施市'], ['9013.002', '利川市'], ['9013.003', '建始县'], ['9013.004', '巴东县'], ['9013.005', '宣恩县'], ['9013.006', '咸丰县'], ['9013.007', '来凤县'], ['9013.008', '鹤峰县'], ['9014', '省直辖行政单位'], ['9014.001', '仙桃市'], ['9014.002', '潜江市'], ['9014.003', '天门市'], ['9014.004', '神农架林区']]

        for i in city_list:
            if i[1] in addr:
                return float(i[0])
        return 9000


if __name__ == '__main__':
    import traceback, os
    try:
        jl = alashan_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
        if 'pop from empty list'!=str(e):
            print('报错')
            traceback.print_exc()
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

