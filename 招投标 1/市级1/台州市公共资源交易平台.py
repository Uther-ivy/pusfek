# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 台州市公共资源交易平台
class taizhou_ggzy:
    def __init__(self):
        self.url_list = [
            # 市本级
            #   建设工程
            #       招标公告
            'https://tzztb.zjtz.gov.cn/tzcms/gcjyzhaobgg/index_{}.htm',
        ]
        self.url = self.url_list.pop(0)
        self.headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
            'Cookie': 'JSESSIONID=9657B4F63DA288A3441581ED27E213C3; clientlanguage=zh_CN; NBSESSIONID=91b97f77-e7dc-4294-8bb7-a0b6c868d426; SERVERID=57526053d080975751a9538d16dda0a7|1678679625|1678679623; arialoadData=false',
            'Host': 'tzztb.zjtz.gov.cn',
            'Referer': 'https://tzztb.zjtz.gov.cn/tzcms/gcjyzhaobgg/index.htm',
        }

    def parse(self):
        date = tool.date
        # date = '2020-01-22'
        page = 0
        while True:
            page += 1
            text = tool.requests_get(self.url.format(page), self.headers)
            print('*' * 20, page, '*' * 20)
            html = HTML(text)
            # print(11, text)
            # time.sleep(6666)
            detail = html.xpath('//table[@class="table-box"]/tr')
            for li in detail[1:]:
                title = li.xpath('./td[2]/a/@title')[0]
                url = 'https://tzztb.zjtz.gov.cn' + li.xpath('./td[2]/a/@href')[0]
                date_Today = li.xpath('./td[4]/text()')[0]
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
                    print('日期不符, 正在切换类型', date_Today, self.url)
                    return


    def parse_detile(self, title, url, date):
        print(url)
        url_html = etree.HTML(tool.requests_get(url, self.headers))
        pic = url_html.xpath('//div[@class="content-text"]//img/@src')[0]
        detail = url_html.xpath('//div[@class="content-box"]')[0]
        detail_html = etree.tostring(detail, method='HTML')
        detail_html = html.unescape(detail_html.decode())
        detail_text = url_html.xpath('string(//div[@class="content-box"])').replace('\xa0',
                                                                                                '').replace('\n',
                                                                                                              ''). \
                replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
        # except:
        #     try:
        #         detail = url_html.xpath('/html/body/div[5]/div/div[3]/div/img')[0]
        #         detail_html = etree.tostring(detail, method='HTML')
        #         detail_html = html.unescape(detail_html.decode())
        #         detail_text = url_html.xpath('string(/html/body/div[5]/div/div[3]/div/img)').replace('\xa0',
        #                                                                                           '').replace('\n',
        #                                                                                                       ''). \
        #             replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
        #     except:
        #         try:
        #             detail = url_html.xpath('/html/body/div[2]/div/img')[0]
        #             detail_html = etree.tostring(detail, method='HTML')
        #             detail_html = html.unescape(detail_html.decode())
        #             detail_text = url_html.xpath('string(/html/body/div[2]/div/img)').replace('\xa0',
        #                                                                                               '').replace('\n',
        #                                                                                                           ''). \
        #                 replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
        #         except:
        #             try:
        #                 detail = url_html.xpath('/html/body/div[2]/div/div')[0]
        #                 detail_html = etree.tostring(detail, method='HTML')
        #                 detail_html = html.unescape(detail_html.decode())
        #                 detail_text = url_html.xpath('string(/html/body/div[2]/div/div)').replace('\xa0',
        #                                                                                           '').replace('\n',
        #                                                                                                       ''). \
        #                     replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
        #             except:
        #                 detail = url_html.xpath('/html/body/div[2]/div')[0]
        #                 detail_html = etree.tostring(detail, method='HTML')
        #                 detail_html = html.unescape(detail_html.decode())
        #                 detail_text = url_html.xpath('string(/html/body/div[2]/div)').replace('\xa0',
        #                                                                                           '').replace('\n',
        #                                                                                                       ''). \
        #                     replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
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
        item['body']=pic
        # item['body'] = tool.qudiao_width(detail_html)
        # item['body'] = item['body'].replace('阅读:<span id="views"></span>次', '')
        # x = re.findall('''<td>上一条：.*?</a></td>
        #            </tr>''', item['body'], re.S)
        # if len(x) != 0:
        #     item['body'] = item['body'].replace(x[0], '')
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
        item['resource'] = '台州市公共资源交易平台'
        item['shi'] = 6010
        item['sheng'] = 6000
        item['removal']= title
        process_item(item)
        # print(item)
    def get_nativeplace(self, addr):
        city = ''
        city_list = [['6010.001', '椒江区'], ['6010.002', '黄岩区'], ['6010.003', '路桥区'], ['6010.004', '玉环县'], ['6010.005', '三门县'], ['6010.006', '天台县'], ['6010.007', '仙居县'], ['6010.008', '温岭'], ['6010.009', '临海']]

        for i in city_list:
            if i[1] in addr:
                city = float(i[0])
                break
        if city == '':
            city = 6010
        return city

if __name__ == '__main__':
    import traceback, os
    try:
        jl = taizhou_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
        tool.send_error('报错文件：'+str(os.path.basename(__file__))+'报错信息：'+str(e))


