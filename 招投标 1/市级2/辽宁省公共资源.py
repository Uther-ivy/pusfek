# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 辽宁省公共资源交易平台
class liaoning_ggzy:
    def __init__(self):
        self.url_list = [
            # 建设工程
            'http://ggzy.ln.gov.cn/jyfb/gcjs/zbgg/{}.html',
            'http://ggzy.ln.gov.cn/jyfb/gcjs/bggg/{}.html',
            'http://ggzy.ln.gov.cn/jyfb/gcjs/zbhxrgs/{}.html',
            'http://ggzy.ln.gov.cn/jyfb/gcjs/zbjggg/{}.html',
            'http://ggzy.ln.gov.cn/jyfb/zfcg/cggg/{}.html',
            'http://ggzy.ln.gov.cn/jyfb/zfcg/cggg_153368/{}.html',
            'http://ggzy.ln.gov.cn/jyfb/zfcg/jggg1/{}.html',
        ]
        self.url = self.url_list.pop(0)
        self.headers = {
            'Cookie': 'ASP.NET_SessionId=0l4fcwjpwyfyunjd5iv55inb',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        }

    def parse(self):
        date = tool.date
        # date = '2020-02-12'
        page = 0
        while True:
            page += 1
            print('*' * 20, page, '*' * 20)
            if page == 1:
                text = tool.requests_get(self.url.format('index'), self.headers)
            else:
                text = tool.requests_get(self.url.format('_' + str(page-1)), self.headers)
            html = HTML(text)
            # print(11, text)
            # time.sleep(6666)
            detail = html.xpath('//*[@class="dlist_rul"]/li')
            for li in detail:
                title = li.xpath('./a/@title')[0].strip()
                url = li.xpath('./a/@href')[0]
                date_Today = li.xpath('./span/text()')[0].replace(' ', '')
                if 'http' not in url:
                    if '../../' in url:
                        url = '/'.join(self.url.split('/')[:3]) + '/' + url.replace('../', '')
                    elif '../' in url:
                        url = '/'.join(self.url.split('/')[:5]) + '/' + url.replace('../', '')
                    elif url[0] == '/':
                        url = '/'.join(self.url.split('/')[:3]) + url.replace('./', '')
                    else:
                        url = '/'.join(self.url.split('/')[:-1]) + '/' + url.replace('./', '')
                # print(title, url, date_Today)
                # time.sleep(666)
                if tool.Transformation(date) <= tool.Transformation(date_Today):
                    if tool.removal(title, date):
                        if self.parse_detile(title, url, date_Today) == '':
                            print('网站正在维护中，请稍后访问!')
                            continue
                    else:
                        print('【existence】', url)
                        continue
                else:
                    print('日期不符, 正在切换类型...', date_Today)
                    self.url = self.url_list.pop(0)
                    page = 0
                    break

    def parse_detile(self, title, url, date):
        print(url)
        text = tool.requests_get(url, self.headers)
        if '网站正在维护中，请稍后访问' in text:
            return ''
        url_html = etree.HTML(text)
        detail = url_html.xpath('//*[@id="Zoom"]')[0]
        detail_html = etree.tostring(detail, method='HTML')
        detail_html = html.unescape(detail_html.decode())
        detail_text = url_html.xpath('string(//*[@id="Zoom"])').replace('\xa0', '').replace('\n', '').\
            replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
        # print(detail_text.replace('\xa0','').replace('\xa5',''))
        # time.sleep(6666)
        item = {}
        item['title'] = title.replace('\u2022', '').replace(' ','')
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
        item['resource'] = '辽宁省公共资源'
        item['shi'] = int(str(item["nativeplace"]).split('.')[0])
        item['sheng'] = 3500
        item['removal']= title
        process_item(item)

    def get_nativeplace(self, addr):
        city = ''
        city_list = [['3501', '沈阳市'], ['3501.001', '和平区'], ['3501.01', '辽中县'], ['3501.011', '康平县'], ['3501.012', '法库县'], ['3501.013', '新民市'], ['3501.014', '沈北新区'], ['3501.002', '沈河区'], ['3501.003', '大东区'], ['3501.004', '皇姑区'], ['3501.005', '铁西区'], ['3501.006', '苏家屯区'], ['3501.007', '东陵区'], ['3501.008', '新城子区'], ['3501.009', '于洪区'], ['3502', '大连市'], ['3502.001', '中山区'], ['3502.01', '庄河市'], ['3502.002', '西岗区'], ['3502.003', '沙河口区'], ['3502.004', '甘井子区'], ['3502.005', '旅顺口区'], ['3502.006', '金州区'], ['3502.007', '长海县'], ['3502.008', '瓦房店市'], ['3502.009', '普兰店市'], ['3503', '鞍山市'], ['3503.001', '铁东区'], ['3503.002', '铁西区'], ['3503.003', '立山区'], ['3503.004', '千山区'], ['3503.005', '台安县'], ['3503.006', '岫岩满族自治县'], ['3503.007', '海城市'], ['3504', '抚顺市'], ['3504.001', '新抚区'], ['3504.002', '东洲区'], ['3504.003', '望花区'], ['3504.004', '顺城区'], ['3504.005', '抚顺县'], ['3504.006', '新宾满族自治县'], ['3504.007', '清原满族自治县'], ['3505', '本溪市'], ['3505.001', '平山区'], ['3505.002', '溪湖区'], ['3505.003', '明山区'], ['3505.004', '南芬区'], ['3505.005', '本溪满族自治县'], ['3505.006', '桓仁满族自治县'], ['3506', '丹东市'], ['3506.001', '元宝区'], ['3506.002', '振兴区'], ['3506.003', '振安区'], ['3506.004', '宽甸满族自治县'], ['3506.005', '东港市'], ['3506.006', '凤城市'], ['3507', '锦州市'], ['3507.001', '古塔区'], ['3507.002', '凌河区'], ['3507.003', '太和区'], ['3507.004', '黑山县'], ['3507.005', '义县'], ['3507.006', '凌海市'], ['3507.007', '北宁市'], ['3508', '营口市'], ['3508.001', '站前区'], ['3508.002', '西市区'], ['3508.003', '鲅鱼圈区'], ['3508.004', '老边区'], ['3508.005', '盖州市'], ['3508.006', '大石桥市'], ['3509', '阜新市'], ['3509.001', '海州区'], ['3509.002', '新邱区'], ['3509.003', '太平区'], ['3509.004', '清河门区'], ['3509.005', '细河区'], ['3509.006', '阜新蒙古族自治县'], ['3509.007', '彰武县'], ['3510', '辽阳市'], ['3510.001', '白塔区'], ['3510.002', '文圣区'], ['3510.003', '宏伟区'], ['3510.004', '弓长岭区'], ['3510.005', '太子河区'], ['3510.006', '辽阳县'], ['3510.007', '灯塔市'], ['3511', '盘锦市'], ['3511.001', '双台子区'], ['3511.002', '兴隆台区'], ['3511.003', '大洼县'], ['3511.004', '盘山县'], ['3512', '铁岭市'], ['3512.001', '银州区'], ['3512.002', '清河区'], ['3512.003', '铁岭县'], ['3512.004', '西丰县'], ['3512.005', '昌图县'], ['3512.006', '调兵山市'], ['3512.007', '开原市'], ['3513', '朝阳市'], ['3513.001', '双塔区'], ['3513.002', '龙城区'], ['3513.003', '朝阳县'], ['3513.004', '建平县'], ['3513.005', '喀喇沁左翼蒙古族自治县'], ['3513.006', '北票市'], ['3513.007', '凌源市'], ['3514', '葫芦岛市'], ['3514.001', '连山区'], ['3514.002', '龙港区'], ['3514.003', '南票区'], ['3514.004', '绥中县'], ['3514.005', '建昌县'], ['3514.006', '兴城市']]
        for i in city_list:
            if i[1] in addr:
                city = float(i[0])
                break
        if city == '':
            city = 3500
        return city

if __name__ == '__main__':
    jl = liaoning_ggzy()
    jl.parse()


