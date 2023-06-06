# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 乌兰察布公共资源交易中心
class wenshan_ggzy:
    def __init__(self):
        self.url_list = [
            'http://ggzy.wulanchabu.gov.cn/jyxx/jsgcZbjggs',  #工程建设
             # 'http://ggzy.wulanchabu.gov.cn/jyxx/zfcg/zbjggs',
             # 'http://ggzy.wulanchabu.gov.cn/jyxx/jsgczbhxrgs',  # 工程建设
             # 'http://ggzy.wulanchabu.gov.cn/jyxx/jsgcZbgg',
             # 'http://ggzy.wulanchabu.gov.cn/jyxx/zfcg/cggg',  # 政府采购
             # 'http://ggzy.wulanchabu.gov.cn/jyxx/zfcg/gzsx'
                         ]
        self.url = self.url_list.pop(0)
        self.headers = {
            'Cookie': 'homeid=1a444a31-e460-47ff-9931-1c075c0f3cd8',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        }

    def parse(self):
        date = tool.date
        # date = '2020-04-02'
        page =230
        while True:
            page += 1
            data = {
                'currentPage': str(page),
                'area': '004',
                'secondArea': '000',
                'industriesTypeCode': '000',
                'bulletinName': ''
            }
            if page == 1:
                text = tool.requests_get(self.url, self.headers)
            else:
                text = tool.requests_post(self.url, data, self.headers)
            print('*' * 20, page, '*' * 20)
            html = HTML(text)
            # print(11, text)
            # time.sleep(6666)
            detail = html.xpath('//*[@id="p2"]/tr')
            for li in detail:
                try:
                    try:
                        title = li.xpath('./td[2]/a/@title')[0]
                        url = 'http://ggzy.wulanchabu.gov.cn' + li.xpath('./td[2]/a/@href')[0]
                        date_Today = li.xpath('./td[3]/text()')[0]
                    except:
                        try:
                            title = li.xpath('./td[3]/a/@title')[0]
                            url = 'http://ggzy.wulanchabu.gov.cn' + li.xpath('./td[3]/a/@href')[0]
                            date_Today = li.xpath('./td[4]/text()')[0]
                        except:
                            continue
                    print(title, url, date_Today)
                    # time.sleep(666)
                    if tool.Transformation(date) <= tool.Transformation(date_Today):
                        # if tool.removal(title, date):
                            self.parse_detile(title, url, date_Today)
                        # else:
                        #     print('【existence】', url)
                        #     continue
                    else:
                        print('日期不符, 正在切换类型', date_Today)
                        return
                except Exception as e:
                    traceback.print_exc()

    def parse_detile(self, title, url, date):
        print(url)
        url_html = etree.HTML(tool.requests_get(url, self.headers))
        detail = url_html.xpath('/html/body/div[3]/div[2]/div/div[3]')[0]
        detail_html = etree.tostring(detail, method='HTML')
        detail_html = html.unescape(detail_html.decode())
        detail_text = url_html.xpath('string(/html/body/div[3]/div[2]/div/div[3])').replace('\xa0', '').replace('\n', '').\
            replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
        if len(detail_html) < 200:
            int('a')
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
        item['resource'] = '乌兰察布公共资源交易中心'
        item['shi'] = 3009
        item['sheng'] = 3000
        item['removal']= title
        process_item(item)
    def get_nativeplace(self, addr):
        city = ''
        city_list = [['3009.001', '集宁区'], ['3009.01', '四子王旗'], ['3009.011', '丰镇'], ['3009.002', '卓资县'], ['3009.003', '化德县'], ['3009.004', '商都县'], ['3009.005', '兴和县'], ['3009.006', '凉城县'], ['3009.007', '察哈尔右翼前旗'], ['3009.008', '察哈尔右翼中旗'], ['3009.009', '察哈尔右翼后旗']]

        for i in city_list:
            if i[1] in addr:
                city = float(i[0])
                break
        if city == '':
            city = 3009
        return city

if __name__ == '__main__':
    import traceback,os
    try:
        jl = wenshan_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
        tool.send_error('报错文件：'+str(os.path.basename(__file__))+'报错信息：'+str(e))



