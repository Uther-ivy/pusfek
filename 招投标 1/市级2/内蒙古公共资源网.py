# -*- coding: utf-8 -*-
import json
import re
import time, html
import traceback
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 内蒙古公共资源网
class xinyang_ggzy:
    def __init__(self):
        self.url_list = ['http://ggzyjy.nmg.gov.cn/jyxx/jsgcZbgg', 'http://ggzyjy.nmg.gov.cn/jyxx/jsgcGzsx', 'http://ggzyjy.nmg.gov.cn/jyxx/jsgcZbhxrgs', 'http://ggzyjy.nmg.gov.cn/jyxx/jsgcZbjggs',
                     # 政府采购
                  'http://ggzyjy.nmg.gov.cn/jyxx/zfcg/cggg', 'http://ggzyjy.nmg.gov.cn/jyxx/zfcg/gzsx', 'http://ggzyjy.nmg.gov.cn/jyxx/zfcg/zbjggs',
                    # 其他交易
                  'http://ggzyjy.nmg.gov.cn/jyxx/qtjy/jygg', 'http://ggzyjy.nmg.gov.cn/jyxx/qtjy/jyqr']
        self.url = self.url_list.pop(0)
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
            # 'Cookie': 'JSESSIONID=Jhs7fR6dYN1sfp2nr6qwFFyJzQGyyxJY4DbWnkT0FvTx1DR6hH3y!-1581166878'
            'Cookie': 'JSESSIONID=6cf5cad7-9e11-4d3d-9efd-70e2f5bc0d11'
        }

    def parse(self):
        # print(headers)
        # time.sleep(6666)
        date = tool.date
        # date = '2020-07-10'
        page = 0
        data = {
            'currentPage': '',
            'industriesTypeCode': '000',
            'time': '',
            'scrollValue': '1200',
            'bulletinName': '',
            'area': '001',
            'startTime': '',
            'endTime': ''
        }
        while True:
            page += 1
            if page == 1:
                text = tool.requests_get(self.url, self.headers)
            else:
                text = tool.requests_post(self.url, data, self.headers)
            data['currentPage'] = str(page)
            # print(text)
            # time.sleep(6666)
            detail = HTML(text).xpath('/html/body/div[2]/div[2]/div/div[4]/table/tr')
            print('*' * 20, page, '*' * 20)
            for tr in detail:
                if 'jsgcZbjggs' in self.url or 'jsgcZbhxrgs' in self.url:
                    try:
                        title = tr.xpath('./td[2]/a/@title')[0]
                        date_Today = tr.xpath('./td[3]/text()')[0].replace('\n', '').replace('\r',
                                                                                                                    '') \
                            .replace('\t', '').replace(' ', '')
                        url = 'http://ggzyjy.nmg.gov.cn' + tr.xpath('./td[2]/a/@href')[0].replace('\n', '').replace('\r',
                                                                                                                    '') \
                            .replace('\t', '').replace(' ', '')
                    except:
                        continue
                else:
                    try:
                        title = tr.xpath('./td[3]/a/@title')[0]
                        date_Today = tr.xpath('./td[4]/text()')[0].replace('\n', '').replace('\r',
                                                                                                                    '') \
                            .replace('\t', '').replace(' ', '')
                        url = 'http://ggzyjy.nmg.gov.cn' + tr.xpath('./td[3]/a/@href')[0].replace('\n', '').replace('\r', '')\
                            .replace('\t', '').replace(' ', '')
                    except:
                        # traceback.print_exc()
                        continue
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
        detail = url_html.xpath('/html/body/div[2]/div[2]/div[2]')[0]
        detail_html = etree.tostring(detail, method='HTML')
        detail_html = html.unescape(detail_html.decode()).replace('\xa0', '').replace('\ufeff', '')
        detail_text = url_html.xpath('string(/html/body/div[2]/div[2]/div[2])') \
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
        # b = re.findall('''<p class="news-article-info">.*?</p>''', item['body'])[0]
        # item['body'] = item['body'].replace(b, '')
        # print(item['body'])
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
        item['resource'] = '内蒙古公共资源网'
        item["shi"] = int(item['nativeplace'])
        item['sheng'] = 3000
        item['removal']= title
        process_item(item)
        # print(item['body'])

    def get_nativeplace(self, addr):
        city = ''
        city_list = [['3001', '呼和浩特'], ['3001.001', '新城'], ['3001.002', '回民'], ['3001.003', '玉泉'], ['3001.004', '赛罕'], ['3001.005', '土默特左旗'], ['3001.006', '托克托'], ['3001.007', '和林格尔'], ['3001.008', '清水河'], ['3001.009', '武川'], ['3002', '包头'], ['3002.001', '东河'], ['3002.002', '昆都仑'], ['3002.003', '青山'], ['3002.004', '石拐'], ['3002.005', '白云矿'], ['3002.006', '九原'], ['3002.007', '土默特右旗'], ['3002.008', '固阳'], ['3002.009', '达尔罕茂明安联合旗'], ['3003', '乌海'], ['3003.001', '海勃湾'], ['3003.002', '海南'], ['3003.003', '乌达'], ['3004', '赤峰'], ['3004.001', '红山'], ['3004.01', '喀喇沁旗'], ['3004.011', '宁城'], ['3004.012', '敖汉旗'], ['3004.002', '元宝山'], ['3004.003', '松山'], ['3004.004', '阿鲁科尔沁旗'], ['3004.005', '巴林左旗'], ['3004.006', '巴林右旗'], ['3004.007', '林西'], ['3004.008', '克什克腾旗'], ['3004.009', '翁牛特旗'], ['3005', '通辽'], ['3005.001', '科尔沁'], ['3005.002', '科尔沁左翼中旗'], ['3005.003', '科尔沁左翼后旗'], ['3005.004', '开鲁'], ['3005.005', '库伦旗'], ['3005.006', '奈曼旗'], ['3005.007', '扎鲁特旗'], ['3005.008', '霍林郭勒'], ['3006', '鄂尔多斯'], ['3006.001', '东胜'], ['3006.002', '达拉特旗'], ['3006.003', '准格尔旗'], ['3006.004', '鄂托克前旗'], ['3006.005', '鄂托克旗'], ['3006.006', '杭锦旗'], ['3006.007', '乌审旗'], ['3006.008', '伊金霍洛旗'], ['3007', '呼伦贝尔'], ['3007.001', '海拉尔'], ['3007.01', '牙克石'], ['3007.011', '扎兰屯'], ['3007.012', '额尔古纳'], ['3007.013', '根河'], ['3007.002', '阿荣旗'], ['3007.003', '莫力达瓦达斡尔族自治旗'], ['3007.004', '鄂伦春自治旗'], ['3007.005', '鄂温克族自治旗'], ['3007.006', '陈巴尔虎旗'], ['3007.007', '新巴尔虎左旗'], ['3007.008', '新巴尔虎右旗'], ['3007.009', '满洲里'], ['3008', '巴彦淖尔'], ['3008.001', '临河'], ['3008.002', '五原'], ['3008.003', '磴口'], ['3008.004', '乌拉特前旗'], ['3008.005', '乌拉特中旗'], ['3008.006', '乌拉特后旗'], ['3008.007', '杭锦后旗'], ['3009', '乌兰察布'], ['3009.001', '集宁'], ['3009.01', '四子王旗'], ['3009.011', '丰镇'], ['3009.002', '卓资'], ['3009.003', '化德'], ['3009.004', '商都'], ['3009.005', '兴和'], ['3009.006', '凉城'], ['3009.007', '察哈尔右翼前旗'], ['3009.008', '察哈尔右翼中旗'], ['3009.009', '察哈尔右翼后旗'], ['3010', '兴安盟'], ['3010.001', '乌兰浩特'], ['3010.002', '阿尔山'], ['3010.003', '科尔沁右翼前旗'], ['3010.004', '科尔沁右翼中旗'], ['3010.005', '扎赉特旗'], ['3010.006', '突泉'], ['3011', '锡林郭勒盟'], ['3011.001', '二连浩特'], ['3011.01', '正镶白旗'], ['3011.011', '正蓝旗'], ['3011.012', '多伦'], ['3011.002', '锡林浩特'], ['3011.003', '阿巴嘎旗'], ['3011.004', '苏尼特左旗'], ['3011.005', '苏尼特右旗'], ['3011.006', '东乌珠穆沁旗'], ['3011.007', '西乌珠穆沁旗'], ['3011.008', '太仆寺旗'], ['3011.009', '镶黄旗'], ['3012', '阿拉善盟'], ['3012.001', '阿拉善左旗'], ['3012.002', '阿拉善右旗']]

        for i in city_list:
            if i[1] in addr:
                city = float(i[0])
                break
        if city == '':
            city = 3000
        return city

if __name__ == '__main__':
    import traceback, os
    try:
        jl = xinyang_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
