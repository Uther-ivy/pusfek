# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 内蒙古招标投标公共服务平台
class xinyang_ggzy:
    def __init__(self):
        self.url_list = [
            'http://zbgg.nmgztb.com.cn/xxfbcms/category/bulletinList.html?searchDate=1996-07-29&dates=300&word=&categoryId=88&industryName=&area=&status=&publishMedia=&sourceInfo=&showStatus=1&page={}',
            'http://zbgg.nmgztb.com.cn/xxfbcms/category/candidateBulletinList.html?searchDate=1996-07-29&dates=300&word=&categoryId=91&industryName=&area=&status=&publishMedia=&sourceInfo=&showStatus=&page={}',
            'http://zbgg.nmgztb.com.cn/xxfbcms/category/resultBulletinList.html?searchDate=1996-07-29&dates=300&word=&categoryId=90&industryName=&area=&status=&publishMedia=&sourceInfo=&showStatus=&page={}',
            'http://zbgg.nmgztb.com.cn/xxfbcms/category/resultBulletinList.html?searchDate=1996-07-29&dates=300&word=&categoryId=90&industryName=&area=&status=&publishMedia=&sourceInfo=&showStatus=&page={}',
            'http://zbgg.nmgztb.com.cn/xxfbcms/category/qualifyBulletinList.html?searchDate=1996-07-29&dates=300&word=&categoryId=92&industryName=&area=&status=&publishMedia=&sourceInfo=&showStatus=&page={}',

        ]
        self.url = self.url_list.pop(0)
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        }

    def parse(self):
        date = tool.date
        # date = '2021-03-31'
        page = 0
        while True:
            page += 1
            text = tool.requests_get(self.url.format(page), self.headers)
            html = HTML(text)
            print('*' * 20, page, '*' * 20)
            detail = html.xpath('//table[@class="table_text"]//tr')
            for li in detail:
                try:
                    title = li.xpath('./td[1]/a/@title')[0].replace('\xa0', '').replace(' ', '')
                    url = li.xpath('./td[1]/a/@href')[0].replace("javascript:urlOpen('","").replace("')","").strip()

                    date_Today = li.xpath('./td[5]/text()')[0].replace('月', '-').replace('日', '').replace('\n','').replace('\t', '').replace('年', '-').strip()
                except:
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
        t = tool.requests_get(url, self.headers)
        try:
            u = re.findall("escape\('(.*?)'\),", t)[0].replace('(', '').replace(')', '').replace("'", '')
        except:
            return
        detail_html = '''<embed style="width: 100%; height: 1060px; display: block" src='{}'> </embed>'''.format(u)
        # print(detail_html)
        # print(detail_text.replace('\xa0','').replace('\xa5',''))
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
        item['endtime'] = 0
        item['tel'] = 0
        item['email'] = ''
        item['address'] = ''
        item['nativeplace'] = self.get_nativeplace(title)
        item['linkman'] = ''
        item['function'] = 0
        item['resource'] = '内蒙古招标投标公共服务平台'
        item["shi"] = int(str(item["nativeplace"]).split('.')[0])
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
    import traceback,os
    try:
        jl = xinyang_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
