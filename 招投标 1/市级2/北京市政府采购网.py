# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item


# 北京市政府采购网
class baoshan_ggzy:
    def __init__(self):
        self.url_list = [
            'http://www.ccgp-beijing.gov.cn/xxgg/sjzfcggg/sjzbgg/{}.html',
            'http://www.ccgp-beijing.gov.cn/xxgg/sjzfcggg/sjzbjggg/{}.html',
            'http://www.ccgp-beijing.gov.cn/xxgg/sjzfcggg/sjhtgg/{}.html',
            'http://www.ccgp-beijing.gov.cn/xxgg/sjzfcggg/sjgzgg/{}.html',
            'http://www.ccgp-beijing.gov.cn/xxgg/sjzfcggg/sjfbgg/{}.html',
            'http://www.ccgp-beijing.gov.cn/xxgg/sjzfcggg/sjdygg/{}.html',
            'http://www.ccgp-beijing.gov.cn/xxgg/sjzfcggg/sjqtgg/{}.html',
            'http://www.ccgp-beijing.gov.cn/xxgg/qjzfcggg/qjzbgg/{}.html',
            'http://www.ccgp-beijing.gov.cn/xxgg/qjzfcggg/qjzbjggg/{}.html',
            'http://www.ccgp-beijing.gov.cn/xxgg/qjzfcggg/qjhtgg/{}.html',
            'http://www.ccgp-beijing.gov.cn/xxgg/qjzfcggg/qjgzgg/{}.html',
            'http://www.ccgp-beijing.gov.cn/xxgg/qjzfcggg/qjfbgg/{}.html',
            'http://www.ccgp-beijing.gov.cn/xxgg/qjzfcggg/qjdygg/{}.html',
            'http://www.ccgp-beijing.gov.cn/xxgg/qjzfcggg/qjqtgg/{}.html',
        ]
        self.url = self.url_list.pop(0)
        self.headers = {
            'Cookie': 'homeid=1a444a31-e460-47ff-9931-1c075c0f3cd8',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        }

    def parse(self):
        date = tool.date
        # date = '2020-12-11'
        page = 0
        while True:
            page += 1
            if page == 1:
                text = tool.requests_get_bm(self.url.format('index'), self.headers)
            else:
                text = tool.requests_get_bm(self.url.format('index_' + str(page)), self.headers)
            print('*' * 20, page, '*' * 20)
            html = HTML(text)
            # print(11, res)
            # time.sleep(6666)
            detail = html.xpath('//*[@class="inner-ul"]/li')
            for li in detail:
                title = li.xpath('./a/text()')[0].replace('\n', '').replace('\r', '') \
                    .replace('\t', '').replace(' ', '')
                url = li.xpath('./a/@href')[0]
                if 'http' not in url:
                    url = self.url.replace('/{}.html', '') + url[1:]
                    # if 'sjzfcggg' in self.url:
                    #     url = 'http://www.ccgp-beijing.gov.cn/xxgg/sjzfcggg' + url[1:]
                    # else:
                    #     url = 'http://www.ccgp-beijing.gov.cn/xxgg/qjzfcggg' + url[1:]
                date_Today = li.xpath('./span/text()')[0].replace('\n', '').replace('\r', '') \
                    .replace('\t', '').replace(' ', '')
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
                    print('日期不符, 正在切换类型', date_Today)
                    self.url = self.url_list.pop(0)
                    print(self.url)
                    page = 0

                    break
            if page == 20:
                self.url = self.url_list.pop(0)
                break

    def parse_detile(self, title, url, date):
        print(url)
        url_html = etree.HTML(tool.requests_get_bm(url, self.headers))
        try:
            detail = url_html.xpath('//*[@id="mainText"]')[0]
            detail_html = etree.tostring(detail, method='HTML')
            detail_html = html.unescape(detail_html.decode())
            detail_text = url_html.xpath('string(//*[@id="mainText"])').replace('\xa0', '').replace('\n', ''). \
                replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
            if len(detail_html) < 500:
                int('a')
        except:
            try:
                detail = url_html.xpath('//*[@class="content_2020"]')[0]
                detail_html = etree.tostring(detail, method='HTML')
                detail_html = html.unescape(detail_html.decode())
                detail_text = url_html.xpath('string(//*[@class="content_2020"])').replace('\xa0', '').replace('\n',
                                                                                                               ''). \
                    replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
                if len(detail_html) < 500:
                    int('a')
            except:
                detail = url_html.xpath('/html/body/div[2]/div[3]')[0]
                detail_html = etree.tostring(detail, method='HTML')
                detail_html = html.unescape(detail_html.decode())
                detail_text = url_html.xpath('string(/html/body/div[2]/div[3])').replace('\xa0', '').replace('\n',
                                                                                                             ''). \
                    replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
                if len(detail_html) < 500:
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
        item['address'] = tool.get_address(detail_text)
        item['linkman'] = tool.get_linkman(detail_text)
        item['function'] = tool.get_function(detail_text)
        item['resource'] = '北京市政府采购网'
        item['shi'] = int(item['nativeplace'])
        item['sheng'] = 1000
        item['removal'] = title
        process_item(item)

    def get_nativeplace(self, addr):
        city = ''
        city_list = [['1001', '东城区'], ['1002', '西城区'], ['1003', '崇文区'], ['1004', '宣武区'], ['1005', '朝阳区'],
                     ['1006', '丰台区'], ['1007', '石景山区'], ['1008', '海淀区'], ['1009', '门头沟区'], ['1010', '房山区'],
                     ['1011', '通州区'], ['1012', '顺义区'], ['1013', '昌平区'], ['1014', '大兴区'], ['1015', '怀柔区'],
                     ['1016', '平谷区'], ['1017', '密云县'], ['1018', '延庆县']]

        for i in city_list:
            if i[1] in addr:
                city = float(i[0])
                break
        if city == '':
            city = 1000
        return city


if __name__ == '__main__':
    import traceback, os

    try:
        jl = baoshan_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
        tool.send_error('报错文件：' + str(os.path.basename(__file__)) + '报错信息：' + str(e))
