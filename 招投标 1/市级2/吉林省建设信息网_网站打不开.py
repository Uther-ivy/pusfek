# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 吉林省建设信息网
class xinyang_ggzy:
    def __init__(self):
        self.url_list = [
            'http://www.jlsjsxxw.com:20001/web/bblistdata?sortOrder=desc&pageSize=14&pageNumber={}&_=1594114796684',
            'http://www.jlsjsxxw.com:20001/web/alterationShow/list?sortOrder=desc&pageSize=14&pageNumber={}&_=1594114936887',
            'http://www.jlsjsxxw.com:20001/web/candidateShow/list?sortOrder=desc&pageSize=14&pageNumber={}&_=1594114960508'
        ]
        self.url = self.url_list.pop(0)
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        }

    def parse(self):
        date = tool.date
        # date = '2020-07-06'
        page = 0
        while True:
            page += 1
            text = tool.requests_get(self.url.format(page), self.headers)
            # print(text)
            # time.sleep(666)
            print('*' * 20, page, '*' * 20)
            detail = json.loads(text)['rows']
            for li in detail:
                title = li['projectName']
                if 'bblistdata' in self.url:
                    url = 'http://www.jlsjsxxw.com/bblistdata/' + \
                          str(li['id'])
                    t = li['contents']
                elif 'candidateShow' in self.url:
                    url = 'http://www.jlsjsxxw.com:20001/web/candidateShow/detail/' + \
                          str(li['id'])
                    t = ''
                else:
                    url = 'http://www.jlsjsxxw.com:20001/web/alterationShow/detail/' + \
                          str(li['id'])
                    t = ''
                date_Today = li['releaseDate'].split(' ')[0].replace('/', '-')
                # print(title, url, date_Today)
                # time.sleep(666)
                if '测试' in title:
                    continue
                if tool.Transformation(date) <= tool.Transformation(date_Today):
                    if tool.removal(title, date):
                        self.parse_detile(title, url, date, t)
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

    def parse_detile(self, title, url, date, t):
        print(url)
        if 'bblistdata' in url:
            detail_html = t
            detail_text = ''.join(re.findall('>(.*?)<', detail_html)).replace('\xa0', '').replace('\n', '').replace('\r', '').replace('\t', '') \
                .replace(' ', '').replace('\xa5', '').replace('\ufeff', '').replace('&nbsp;', '')
        else:
            try:
                tt = tool.requests_get(url, self.headers)
                url_html = etree.HTML(tt)
                detail = url_html.xpath('//*[@id="contents"]')[0]
                detail_html = etree.tostring(detail, method='HTML')
                detail_html = html.unescape(detail_html.decode()).replace('\xa0', '').replace('\ufeff', '')
                detail_text = url_html.xpath('string(//*[@id="contents"])') \
                    .replace('\xa0', '').replace('\n', '').replace('\r', '').replace('\t', '') \
                    .replace(' ', '').replace('\xa5', '').replace('\ufeff', '')
            except:
                tt = tool.requests_get(url, self.headers)
                url_html = etree.HTML(tt)
                detail = url_html.xpath('//*[@id="candidateInfo"]/div[2]')[0]
                detail_html = etree.tostring(detail, method='HTML')
                detail_html = html.unescape(detail_html.decode()).replace('\xa0', '').replace('\ufeff', '')
                detail_text = url_html.xpath('string(//*[@id="candidateInfo"]/div[2])') \
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
        item['nativeplace'] = self.get_nativeplace_to(item['title'])
        item['linkman'] = tool.get_linkman(detail_text)
        item['function'] = tool.get_function(detail_text)
        item['resource'] = '吉林省建设信息网'
        item["shi"] = int(str(item["nativeplace"]).split('.')[0])
        item['sheng'] = 4000
        item['removal']= title
        process_item(item)
        # print(item['body'])

    def get_nativeplace_to(self, city):
        a = ''
        ls = [['4001', '长春'], ['4001.001', '南关区'], ['4001.01', '德惠'], ['4001.002', '宽城区'], ['4001.003', '朝阳区'], ['4001.004', '二道区'], ['4001.005', '绿园区'], ['4001.006', '双阳区'], ['4001.007', '农安县'], ['4001.008', '九台'], ['4001.009', '榆树'], ['4002', '吉林'], ['4002.001', '昌邑区'], ['4002.002', '龙潭区'], ['4002.003', '船营区'], ['4002.004', '丰满区'], ['4002.005', '永吉开发区'], ['4002.006', '蛟河'], ['4002.007', '桦甸'], ['4002.008', '舒兰'], ['4002.009', '磐石'], ['4002.010', '经开区'], ['4003', '四平'], ['4003.001', '铁西区'], ['4003.002', '铁东区'], ['4003.003', '梨树县'], ['4003.004', '伊通满族自治县'], ['4003.005', '公主岭'], ['4003.006', '双辽'], ['4004', '辽源'], ['4004.001', '龙山区'], ['4004.002', '西安区'], ['4004.003', '东丰县'], ['4004.004', '东辽县'], ['4005', '通化'], ['4005.001', '东昌区'], ['4005.002', '二道江区'], ['4005.003', '通化县'], ['4005.004', '辉南县'], ['4005.005', '柳河县'], ['4005.006', '梅河口'], ['4005.007', '集安'], ['4006', '白山'], ['4006.001', '八道江区'], ['4006.002', '抚松县'], ['4006.003', '靖宇县'], ['4006.004', '长白朝鲜族自治县'], ['4006.005', '江源县'], ['4006.006', '临江'], ['4007', '松原'], ['4007.001', '宁江区'], ['4007.002', '前郭尔罗斯蒙古族自治县'], ['4007.003', '长岭县'], ['4007.004', '乾安县'], ['4007.005', '扶余县'], ['4008', '白城'], ['4008.001', '洮北区'], ['4008.002', '镇赉县'], ['4008.003', '通榆县'], ['4008.004', '洮南'], ['4008.005', '大安'], ['4009', '延边朝鲜族自治州'], ['4009.001', '延吉'], ['4009.002', '图们'], ['4009.003', '敦化'], ['4009.004', '珲春'], ['4009.005', '龙井'], ['4009.006', '和龙'], ['4009.007', '汪清县'], ['4009.008', '安图县']]
        for i in ls:
            if i[1] in city:
                a = i[0]
                break
        if a == '':
            return 4000
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



