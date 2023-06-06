# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 鹤壁市公共资源交易平台
class hebi_ggzy:
    def __init__(self):
        self.url_list = [
            # 建设工程
                # 招标公告
            'http://ggzy.hebi.gov.cn/TPFront/gcjs/013001/?Paging={}',
                # 变更公示
            'http://ggzy.hebi.gov.cn/TPFront/gcjs/013002/?Paging={}',
                # 中标候选人
            'http://ggzy.hebi.gov.cn/TPFront/gcjs/013003/?Paging={}',
                # 中标结果
            'http://ggzy.hebi.gov.cn/TPFront/gcjs/013004/?Paging={}',
            # 政府采购
                # 采购公告
            'http://ggzy.hebi.gov.cn/TPFront/zfcg/014002/?Paging={}',
                # 变更公告
            'http://ggzy.hebi.gov.cn/TPFront/zfcg/014003/?Paging={}',
                # 结果公告
            'http://ggzy.hebi.gov.cn/TPFront/zfcg/014004/?Paging={}'
        ]
        self.url = self.url_list.pop(0)
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
            # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3'
        }

    def parse(self):
        date = tool.date
        # date = '2020-03-02'
        page = 0
        while True:
            page += 1
            if page == 20:
                print('日期不符, 正在切换类型...')
                self.url = self.url_list.pop(0)
                page = 0
            text = tool.requests_get(self.url.format(page), self.headers)
            print('*' * 20, page, '*' * 20)
            html = HTML(text)
            # print(11, text)
            # time.sleep(6666)
            detail = html.xpath('/html/body/table[5]/tr/td[3]/table/tr[3]/td/table/tr')
            for li in detail:
                try:
                    title = li.xpath('./td[2]/a/@title')[0]
                    url = 'http://ggzy.hebi.gov.cn' + li.xpath('./td[2]/a/@href')[0]
                    date_Today = li.xpath('./td[4]/text()')[0].replace('[', '').replace(']', '')
                except:
                    continue
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
                    print('日期不符, 正在切换类型...', date_Today)
                    self.url = self.url_list.pop(0)
                    page = 0
                    break
            if page == 20:
                self.url = self.url_list.pop(0)
                break
    def parse_detile(self, title, url, date):
        print(url)
        url_html = etree.HTML(tool.requests_get(url, self.headers))
        try:
            detail = url_html.xpath('//*[@id="zbgg"]/table')[0]
            detail_html = etree.tostring(detail, method='HTML')
            detail_html = html.unescape(detail_html.decode())
            detail_text = url_html.xpath('string(//*[@id="zbgg"]/table)').replace('\xa0', '').replace('\n', '').\
                replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
        except:
            detail = url_html.xpath('/html/body/table[5]/tr[3]/td/table/tr/td/table/tr[2]/td/table')[0]
            detail_html = etree.tostring(detail, method='HTML')
            detail_html = html.unescape(detail_html.decode())
            detail_text = url_html.xpath('string(/html/body/table[5]/tr[3]/td/table/tr/td/table/tr[2]/td/table)').replace('\xa0', '').replace('\n', ''). \
                replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
        # print(detail_text.replace('\xa0','').replace('\xa5',''))
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
        width_list = re.findall('width="(.*?)"', item["body"])
        for i in width_list:
            item["body"] = item["body"].replace('width="{}"'.format(i), '')
        width_list = re.findall('WIDTH: (.*?)pt;', item["body"])
        for i in width_list:
            item["body"] = item["body"].replace('WIDTH: {}pt;'.format(i), '')
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
        item['resource'] = '鹤壁市公共资源交易平台'
        item['shi'] = 8506
        item['sheng'] = 8500
        item['removal']= title
        process_item(item)

    def get_nativeplace(self, addr):
        city = ''
        city_list = [['8506.001', '鹤山区'], ['8506.002', '山城区'], ['8506.003', '淇滨区'], ['8506.004', '浚县'], ['8506.005', '淇县']]
        for i in city_list:
            if i[1] in addr:
                city = float(i[0])
                break
        if city == '':
            city = 8506
        return city
if __name__ == '__main__':

    import traceback, os
    try:
        jl = hebi_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
        tool.send_error('报错文件：'+str(os.path.basename(__file__))+'报错信息：'+str(e))

