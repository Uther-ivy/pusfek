# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 深圳市公共资源交易中心
class wenshan_ggzy:
    def __init__(self):
        self.domain_name = 'https://www.szggzy.com'
        self.url_list = [
            'https://www.szggzy.com/jyxx/zfcg/zbgg_{}',
            'https://www.szggzy.com/jyxx/zfcg/zbgg1_{}',
            'https://www.szggzy.com/jyxx/zfcg/bggg_{}',
            'https://www.szggzy.com/jyxx/jsgc/zbgg2_{}',
            'https://www.szggzy.com/jyxx/jsgc/zbgg3_{}',
            'https://www.szggzy.com/jyxx/jsgc/bggg1_{}',
        ]
        self.url = self.url_list.pop(0)
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            # 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Host': 'www.szggzy.com',
            'Cookie': 'aliyungf_tc=b18802e498d5102e04b2a3d4b40692dda7bdb99d89874a09127ea93edc7c1791; acw_tc=707c9f7216474199145276859e0467c8c7d3c08ac77eb8c3aa41e8fab91557; SessionVerify={}; SERVERID=144538eef29e587ea688a87ce91a7e85|1647419914|1647419914',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',

        }

    def parse(self):
        date = tool.date
        # date = '2020-09-24'
        page = 0
        while True:
            page += 1
            text = tool.requests_get(self.url.format(page), self.headers)
            if len(text) < 200:
                cok = re.findall("SessionVerify=(.*?)';</script>", text)[0]
                self.headers['Cookie'] = self.headers['Cookie'].format(cok)
                page -= 1
                continue
            print('*' * 20, page, '*' * 20)
            html = HTML(text)
            detail = html.xpath('//*[@class="newsList"]/li')
            for li in detail:
                title = li.xpath('./a/text()')[0].replace('\n', '').\
                    replace('\r', '').replace('\t', '').replace(' ', '')
                url = li.xpath('./a/@href')[0]
                date_Today = li.xpath('./span[1]/text()')[0].replace('\xa0', '').replace('\n', '').\
                    replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
                if 'http' not in url:
                    url = self.domain_name + url
                if tool.Transformation(date) <= tool.Transformation(date_Today):
                    if tool.removal(title, date):
                        self.parse_detile(title, url, date_Today)
                    else:
                        print('【existence】', url)
                        continue
                else:
                    print('日期不符, 正在切换类型', date_Today, self.url)
                    return


    def parse_detile(self, title, url, date):
        print(url)
        t = tool.requests_get(url, self.headers).replace('\xa9', '').replace('<br>&nbsp;&nbsp;', '')
        url_html = etree.HTML(t)
        try:
            detail = url_html.xpath('//*[@class="conTxt conBorder"]')[0]
            detail_html = etree.tostring(detail, method='HTML')
            detail_html = html.unescape(detail_html.decode()).replace("display: none", '')
            detail_text = url_html.xpath('string(//*[@class="conTxt conBorder"])').replace('\xa0', '').replace('\n',
                                                                                                                 ''). \
                replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
        except:
            detail = url_html.xpath('//*[@class="conTxt"]')[0]
            detail_html = etree.tostring(detail, method='HTML')
            detail_html = html.unescape(detail_html.decode()).replace("display: none", '')
            detail_text = url_html.xpath('string(//*[@class="conTxt"])').replace('\xa0', '').replace('\n',
                                                                                                               ''). \
                replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
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
        # item['body'] = tool.update_img(self.domain_name, item['body'])
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
        item['resource'] = '深圳市公共资源交易平台'
        item['shi'] = 10003
        item['sheng'] = 10000
        item['removal']= title
        process_item(item)

    def get_nativeplace(self, addr):
        city = ''
        city_list = [['10003.001', '罗湖区'], ['10003.002', '福田区'], ['10003.003', '南山区'], ['10003.004', '宝安区'], ['10003.005', '龙岗区'], ['10003.006', '盐田区'], ['10003.007', '坪山区']]

        for i in city_list:
            if i[1] in addr:
                city = float(i[0])
                break
        if city == '':
            city = 10003
        return city

if __name__ == '__main__':
    import traceback,os
    try:
        jl = wenshan_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
        tool.send_error('报错文件：'+str(os.path.basename(__file__))+'报错信息：'+str(e))


