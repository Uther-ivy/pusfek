# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 湖北省公共资源交易平台
class baoshan_ggzy:
    def __init__(self):
        self.url_list = [
            'https://www.hbggzyfwpt.cn/jyxx/jsgcXmba?currentPage=1&scrollValue=0&projectName=&projectType=0&publishTimeType=1&publishTimeStart=&publishTimeEnd=',
            'https://www.hbggzyfwpt.cn/jyxx/jsgcZbgg?currentPage={}&area=000&industriesTypeCode=0&scrollValue=0&bulletinName=&publishTimeType=1&publishTimeStart=&publishTimeEnd=',
            'https://www.hbggzyfwpt.cn/jyxx/jsgcpbjggs?currentPage={}&area=000&indusTriesTypeCode=0&scrollValue=0&publiCityName=&publishTimeType=1&publishTimeStart=&publishTimeEnd=',
            'https://www.hbggzyfwpt.cn/jyxx/jsgcZbjggs?currentPage={}&area=000&industriesTypeCode=0&scrollValue=0&bulletinName=&publishTimeType=1&publishTimeStart=&publishTimeEnd=',
            'https://www.hbggzyfwpt.cn/jyxx/zfcg/cggg?currentPage={}&area=000&industriesTypeCode=&scrollValue=0&bulletinTitle=&purchaserMode=99&purchaserModeType=0&publishTimeType=2&publishTimeStart=&publishTimeEnd=',
            'https://www.hbggzyfwpt.cn/jyxx/zfcg/gzsxs?currentPage={}&area=000&scrollValue=0&title=&publishTimeType=2&publishTimeStart=&publishTimeEnd='
        ]
        self.url = self.url_list.pop(0)
        self.headers = {
            'Cookie': 'homeid=1a444a31-e460-47ff-9931-1c075c0f3cd8',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        }

    def parse(self):
        date = tool.date
        # date = '2021-08-02'
        page = 0
        while True:
            page += 1
            text = tool.requests_get(self.url.format(page), self.headers)
            print('*' * 20, page, '*' * 20)
            html = HTML(text)
            # print(11, text)
            # time.sleep(6666)
            detail = html.xpath('//*[@class="newListwenzi"]/table//tr')
            if len(detail) == 0:
                print('列表为空..', self.url)
                self.url = self.url_list.pop(0)
                page = 0
                continue
            for li in detail:
                title = li.xpath('./td[1]/a/text()')[0].replace('\n', '').replace('\r', '')\
                    .replace('\t', '').replace(' ', '')
                url = li.xpath('./td[1]/a/@href')[0]
                if 'http' not in url:
                    if '../../' in url:
                        url = 'https://www.hbggzyfwpt.cn' + url[5:]
                    elif '../' in url:
                        url = 'https://www.hbggzyfwpt.cn' + url[2:]
                    elif './' in url:
                        url = 'https://www.hbggzyfwpt.cn' + url[1:]
                    else:
                        url = 'https://www.hbggzyfwpt.cn' + url
                date_Today = li.xpath('./td[2]/text()')[0].replace('\n', '').replace('\r', '')\
                    .replace('\t', '').replace(' ', '').replace('.', '-')
                if '测试' in title:
                    continue
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
                    self.url = self.url_list.pop(0)
                    page = 0
                    break
            if page == 20:
                self.url = self.url_list.pop(0)
                break

    def parse_detile(self, title, url, date):
        print(url)
        t = tool.requests_get(url, self.headers)
        if 'jsgc' in self.url:
            if 'jsgcXmxx' in self.url:
                try:
                    url_html = etree.HTML(t)
                    detail = url_html.xpath('//*[@id="projectDiv"]')[0]
                    detail_html = etree.tostring(detail, method='HTML')
                    detail_html = html.unescape(detail_html.decode())
                    detail_text = url_html.xpath('string(//*[@id="projectDiv"])').replace(
                        '\xa0',
                        '').replace(
                        '\n', ''). \
                        replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
                except:
                    detail_html = re.findall('html."项目编号：.*?".;', t, re.S)
                    if len(detail_html) != 0:
                        detail_html = '<div class="detailNeirong" id="detailNeirong">' + detail_html[0].replace(
                            'html("', '') \
                            .replace('");', '').replace('+', '').replace('"', '') + '</div>'
                    detail_text = ''.join(re.findall('>(.*?)<', detail_html, re.S)).replace('\xa0', '').replace('\n',
                                                                                                                ''). \
                        replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
            else:
                try:
                    url_html = etree.HTML(t)
                    code = url_html.xpath('//*[@id="projectCode"]/@value')[0]
                except:
                    return
                if 'jsgcZbgg' in self.url:
                    url_ = 'https://www.hbggzyfwpt.cn/jyxxAjax/jsgcZbggLiDetail?projectCode=' + code
                elif 'jsgcpbjggs' in self.url:
                    url_ = 'https://www.hbggzyfwpt.cn/jyxxAjax/jsgcZbhxrDetail?projectCode=' + code
                elif 'jsgcZbjggs' in self.url:
                    url_ = 'https://www.hbggzyfwpt.cn/jyxxAjax/jsgcZbjgDetail?projectCode=' + code
                t = tool.requests_get(url_, self.headers)
                try:
                    detail_html = json.loads(t)['list'][0]['publiCityContent']
                except:
                    try:
                        detail_html = json.loads(t)['list'][0]['bulletincontent']
                    except:
                        detail_html = json.loads(t)['list'][0]['bulletinContent']
                detail_text = ''.join(re.findall('>(.*?)<', detail_html, re.S)).replace('\xa0', '').replace('\n', ''). \
                    replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
        else:
            url_html = etree.HTML(t)
            code = url_html.xpath('//*[@id="purchaseProjectCode"]/@value')[0]
            if 'cggg' in self.url:
                url_ = 'https://www.hbggzyfwpt.cn/jyxxAjax/zfcg/zfcgCgggLiDetail?purchaseProjectCode=' + code
            else:
                url_ = 'https://www.hbggzyfwpt.cn/jyxxAjax/zfcg/zfcgGzsxLiDetail?purchaseProjectCode=' + code
            t = tool.requests_get(url_, self.headers)
            try:
                detail_html = json.loads(t)['list'][0]['bulletinContent']
            except:
                detail_html = json.loads(t)['list'][0]['terminationBulletinContent']
            detail_text = ''.join(re.findall('>(.*?)<', detail_html, re.S)).replace('\xa0', '').replace('\n', ''). \
                replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
            if len(detail_html) < 100:
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
        # print(item['body'])
        # time.sleep(2222)
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
        item['resource'] = '湖北省公共资源交易平台'
        item['shi'] = int(item['nativeplace'])
        item['sheng'] = 9000
        item['removal']= title
        process_item(item)

    def get_nativeplace(self, addr):
        city = ''
        city_list = [['9001', '武汉市'], ['9001.001', '江岸区'], ['9001.01', '蔡甸区'], ['9001.011', '江夏区'], ['9001.012', '黄陂区'], ['9001.013', '新洲区'], ['9001.002', '江汉区'], ['9001.003', '乔口区'], ['9001.004', '汉阳区'], ['9001.005', '武昌区'], ['9001.006', '青山区'], ['9001.007', '洪山区'], ['9001.008', '东西湖区'], ['9001.009', '汉南区'], ['9002', '黄石市'], ['9002.001', '黄石港区'], ['9002.002', '西塞山区'], ['9002.003', '下陆区'], ['9002.004', '铁山区'], ['9002.005', '阳新县'], ['9002.006', '大冶市'], ['9003', '十堰市'], ['9003.001', '茅箭区'], ['9003.002', '张湾区'], ['9003.003', '郧县'], ['9003.004', '郧西县'], ['9003.005', '竹山县'], ['9003.006', '竹溪县'], ['9003.007', '房县'], ['9003.008', '丹江口市'], ['9004', '宜昌市'], ['9004.001', '西陵区'], ['9004.01', '五峰土家族自治县'], ['9004.011', '宜都市'], ['9004.012', '当阳市'], ['9004.013', '枝江市'], ['9004.002', '伍家岗区'], ['9004.003', '点军区'], ['9004.004', '?亭区'], ['9004.005', '夷陵区'], ['9004.006', '远安县'], ['9004.007', '兴山县'], ['9004.008', '秭归县'], ['9004.009', '长阳土家族自治县'], ['9005', '襄樊市'], ['9005.001', '襄城区'], ['9005.002', '樊城区'], ['9005.003', '襄阳区'], ['9005.004', '南漳县'], ['9005.005', '谷城县'], ['9005.006', '保康县'], ['9005.007', '老河口市'], ['9005.008', '枣阳市'], ['9005.009', '宜城市'], ['9006', '鄂州市'], ['9006.001', '梁子湖区'], ['9006.002', '华容区'], ['9006.003', '鄂城区'], ['9007', '荆门市'], ['9007.001', '钟祥市'], ['9007.002', '沙洋县'], ['9007.003', '京山县'], ['9007.004', '掇刀区'], ['9007.005', '东宝区'], ['9008', '孝感市'], ['9008.001', '安陆市'], ['9008.002', '应城市'], ['9008.003', '云梦县'], ['9008.004', '大悟县'], ['9008.005', '孝昌县'], ['9008.006', '孝南区'], ['9008.007', '汉川市'], ['9009', '荆州市'], ['9009.001', '沙市区'], ['9009.002', '荆州区'], ['9009.003', '公安县'], ['9009.004', '监利县'], ['9009.005', '江陵县'], ['9009.006', '石首市'], ['9009.007', '洪湖市'], ['9009.008', '松滋市'], ['9010', '黄冈市'], ['9010.001', '州区'], ['9010.01', '武穴市'], ['9010.002', '团风县'], ['9010.003', '红安县'], ['9010.004', '罗田县'], ['9010.005', '英山县'], ['9010.006', '浠水县'], ['9010.007', '蕲春县'], ['9010.008', '黄梅县'], ['9010.009', '麻城市'], ['9011', '咸宁市'], ['9011.001', '咸安区'], ['9011.002', '嘉鱼县'], ['9011.003', '通城县'], ['9011.004', '崇阳县'], ['9011.005', '通山县'], ['9011.006', '赤壁市'], ['9012', '随州市'], ['9012.001', '曾都区'], ['9012.002', '广水市'], ['9013', '恩施土家族苗族自治州'], ['9013.001', '恩施市'], ['9013.002', '利川市'], ['9013.003', '建始县'], ['9013.004', '巴东县'], ['9013.005', '宣恩县'], ['9013.006', '咸丰县'], ['9013.007', '来凤县'], ['9013.008', '鹤峰县'], ['9014', '省直辖行政单位'], ['9014.001', '仙桃市'], ['9014.002', '潜江市'], ['9014.003', '天门市'], ['9014.004', '神农架林区']]

        for i in city_list:
            if i[1] in addr:
                city = float(i[0])
                break
        if city == '':
            city = 9000
        return city

if __name__ == '__main__':
    import traceback, os
    try:
        jl = baoshan_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
        tool.send_error('报错文件：'+str(os.path.basename(__file__))+'报错信息：'+str(e))


