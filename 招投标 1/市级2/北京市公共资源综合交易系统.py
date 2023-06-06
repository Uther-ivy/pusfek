# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
import tool
from save_database import process_item

# 北京市公共资源综合交易系统
class beijing_ggzy:
    def __init__(self):
        self.url_code = [
            # 招标公告
            'https://www.bjggzyzhjy.cn/G2/public-notice!noticeList.do?',
        ]
        self.url = self.url_code.pop(0)
        self.headers = {
            # 'Cookie': 'JSESSIONID=BB8D321058D5382A4B16104492F9D231',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
        }

    def parse(self):
        date = tool.date
        # date = '2020-01-09'
        page = 0
        while True:
            # print(self.url)
            time.sleep(0.1)
            page += 1
            data = {
                'data': '',
                'defined_operations_': '',
                'nocheck_operations_': '',
                'gridSearch': 'false',
                'nd': str(time.time()).replace(".","")[:13],
                'PAGESIZE': '10',
                'PAGE': page,
                'sortField': '',
                'sortDirection': 'asc'
            }
            print('*' * 20, page, '*' * 20)
            if 'noticeList' in self.url:
                data['filter_params_'] = 'bidNoticeId,packageId,projectId,enrollId,reviewWay,noticePublishWay,tenderNoticeNo,tenderCategory,enrollEntId,bidSectionNameAndCode,packageName,rowNum,uniformProjectCode,systemType,projectName,projectType,applyTimeStart,applyTimeEnd'
            elif 'noticePubList' in self.url:
                data['filter_params_'] = 'resultPubGatherId,projectId,packageId,resultPubId,publicityType,packageName,rowNum,systemType,bidSectionNameAndCode,uniformProjectCode,projectName,projectType,tenderCategory'
            text = tool.requests_post(self.url, data, self.headers)
            # print(111, text)
            # time.sleep(666)
            detail = json.loads(text)['data']
            for i in detail:
                # print(i)
                title = i['packageName']
                code = i['projectName']
                if '水利工程' in code:
                    url = 'https://www.bjggzyzhjy.cn/G2/pubnotice/sw-tender-notice!previewNoticeSingle.do?flag=toLogin&view' \
                          'Flag=false&projectId='
                elif '交通工程' in code:
                    url = 'https://www.bjggzyzhjy.cn/G2/pubnotice/jt-tender-notice!previewNotice.do?flag=toLogin&viewFlag=' \
                          'false&projectId='
                elif '勘察设计' in code:
                    url = 'https://www.bjggzyzhjy.cn/G2/pubnotice/kb-enroll!previewNotice.do?flag=toLogin&viewFlag=false&' \
                          'projectId=ff8080816f6b494e016f784c5dc10b84&bidNoticeId='
                else:
                    url = 'https://www.bjggzyzhjy.cn/G2/pubnotice/ty-tender-notice!previewNotice.do?flag=toLogin&viewFlag=' \
                          'false&projectId='
                url += i['projectId']
                date_Today = i['applyTimeStart'][:10]
                date_Today_end = i['applyTimeEnd'][:10]
                # print(title, url, date_Today, date_Today_end)
                # time.sleep(666)
                if tool.Transformation(date) <= tool.Transformation(date_Today):
                    if tool.removal(title, date):
                        if self.parse_detile(title, url, date, date_Today_end) == '2':
                            return
                    else:
                        print('【existence】', url)
                        continue
                else:
                    print('日期不符, 正在切换类型...', date_Today)
                    continue
            if page == 2:
                self.url = self.url_code.pop(0)
                break

    def parse_detile(self, title, url, date, date_Today_end):
        print(url)
        url_html = etree.HTML(tool.requests_get(url, self.headers))
        try:
            detail = url_html.xpath('//*[@id="main-container"]/div/div/div[3]/table')[0]
            xpa = '//*[@id="main-container"]/div/div/div[3]/table'
        except:
            detail = url_html.xpath('//*[@id="main-container"]/div')[0]
            xpa = '//*[@id="main-container"]/div'
        detail_html = etree.tostring(detail, method='HTML')
        detail_html = html.unescape(detail_html.decode())
        # print(url_text)
        # time.sleep(6666)
        detail_text = url_html.xpath('string('+xpa+')').replace('\xa0', '').replace('\n', '').replace('\r', '').replace('\t',
                                                                                                                  '').replace(
            ' ', '').replace('\xa5', '')
        # print(detail_text.replace('\xa0','').replace('\xa5',''))
        # time.sleep(6666)
        item = {}
        item['title'] = title.replace('\u2022', '')
        item['url'] = url
        item['date'] = date
        item['typeid'] = tool.get_typeid(item['title'])
        item['senddate'] = tool.Transformation(date)
        if date_Today_end == '':
            try:
                date_start = url_html.xpath('//*[@id="main-container"]/div/div/div[4]/table/tr/td[1]/span'
                                        '/text()')[0].replace('\r', '').replace('\n', '').replace('\t', '')\
                                                        .replace(' ', '')[:10]
            except:
                try:
                    date_start = url_html.xpath('//*[@id="main-container"]/div/div/div[3]/table/tr[8]/td/span[2]'
                                                '/text()')[0].replace('\r', '').replace('\n', '').replace('\t', '') \
                                     .replace(' ', '')[:10]
                except:
                    return '2'
            if tool.Transformation(date) > tool.Transformation(date_start):
                return '2'
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
        if date_Today_end != '':
            item['endtime'] = tool.Transformation(date_Today_end)
        else:
            try:
                item['endtime'] = url_html.xpath('//*[@id="main-container"]/div/div/div[4]/table/tr/td[2]/span/'
                                                 'text()')[0].replace('\r', '').replace('\n', '').replace('\t', '')\
                                                    .replace(' ', '')[:10]
                item['endtime'] = tool.Transformation(item['endtime'])
            except:
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
        item['resource'] = '北京市公共资源综合交易系统'
        item['shi'] = 1000
        item['sheng'] = 1000
        item['removal']= title
        process_item(item)

    def get_nativeplace(self, addr):
        city = ''
        city_list = [['1001', '东城区'], ['1002', '西城区'], ['1003', '崇文区'], ['1004', '宣武区'], ['1005', '朝阳区'], ['1006', '丰台区'], ['1007', '石景山区'], ['1008', '海淀区'], ['1009', '门头沟区'], ['1010', '房山区'], ['1011', '通州区'], ['1012', '顺义区'], ['1013', '昌平区'], ['1014', '大兴区'], ['1015', '怀柔区'], ['1016', '平谷区'], ['1017', '密云县'], ['1018', '延庆县']]

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
        jl = beijing_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
