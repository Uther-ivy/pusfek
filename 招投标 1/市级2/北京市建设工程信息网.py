# -*- coding: utf-8 -*-
import json
import math
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 北京市建设工程信息网
class beijing_gcjs:
    def __init__(self):
        self.url_code = [
            # 勘察设计
                # 中标候选人
            'http://www.bcactc.com/home/gcxx/now_kcsjzbgs.aspx',
            # 施工
            'http://www.bcactc.com/home/gcxx/now_sgzbgs.aspx',
                # 中标结果
            'http://www.bcactc.com/home/gcxx/now_zbjggs.aspx?type=sg',
            # 监理
            'http://www.bcactc.com/home/gcxx/now_jlzbgs.aspx',
            'http://www.bcactc.com/home/gcxx/now_zbjggs.aspx?type=jl',
            # 专业
            'http://www.bcactc.com/home/gcxx/now_zyzbgs.aspx',
            'http://www.bcactc.com/home/gcxx/now_zbjggs.aspx?type=zy',
            # 材料设备
            'http://www.bcactc.com/home/gcxx/now_clsbzbgs.aspx',
            'http://www.bcactc.com/home/gcxx/now_zbjggs.aspx?type=clsb',
            # 铁路
        ]
        self.url = self.url_code.pop(0)
        self.headers = {
            'Cookie': '_d_id=c4bb88508b01ffcc9b09377d666bca; Hm_lvt_ae3702a0997d560bba5902699c6cf1cc=1578537946,1578624317,1578877261; Hm_lpvt_ae3702a0997d560bba5902699c6cf1cc=1578893220',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
        }

    def requests_get(self, url, headers):
        num = 0
        while True:
            try:
                p = tool.process_request()
                proxies = {
                    'http': p,
                    'https': p
                }
                rst = requests.get(url, headers=headers, timeout=30, verify=False, proxies=proxies)
                rst.encoding = rst.apparent_encoding
                return rst.text
            except Exception as e:
                print('请求错误', e.args)
                num += 1
                if num == 10:
                    int('a')
                time.sleep(5)
                continue

    def parse(self):
        date = tool.date
        # date = '2020-01-02'
        page = 0
        while True:
            # page += 1
            text = self.requests_get(self.url, self.headers)
            html = HTML(text)
            print('*' * 20, page, '*' * 20)
            detail = html.xpath('//*[@id="MyGridView1"]/tr')
            for i in range(1, len(detail)):
                try:
                    title = html.xpath('//*[@id="MyGridView1"]/tr[{}]/td[2]/a/text()'.format(i + 1))[0]
                except:
                    title = html.xpath('//*[@id="MyGridView1"]/tr[{}]/td[1]/a/text()'.format(i + 1))[0]
                try:
                    url = 'http://www.bcactc.com/home/gcxx/' + \
                          html.xpath('//*[@id="MyGridView1"]/tr[{}]/td[2]/a/@href'.format(i + 1))[0]
                except:
                    url = 'http://www.bcactc.com/home/gcxx/' + \
                          html.xpath('//*[@id="MyGridView1"]/tr[{}]/td[1]/a/@href'.format(i + 1))[0]
                try:
                    date_Today = html.xpath('//*[@id="MyGridView1"]/tr[{}]/td[5]/text()'.format(i + 1))[0][:10]
                    if '-' not in date_Today:
                        int('a')
                except:
                    try:
                        date_Today = html.xpath('//*[@id="MyGridView1"]/tr[{}]/td[3]/text()'.format(i + 1))[0][:10]
                        if '-' not in date_Today:
                            int('a')
                    except:
                        try:
                            date_Today = html.xpath('//*[@id="MyGridView1"]/tr[{}]/td[2]/text()'.format(i + 1))[0][:10]
                            if '-' not in date_Today:
                                int('a')
                        except:
                            date_Today = html.xpath('//*[@id="MyGridView1"]/tr[{}]/td[4]/text()'.format(i + 1))[0][:10]
                title = title.replace('\u30fb', '')
                date_Today = date_Today.replace(' ', '').replace('\r', '').replace('\t', '')
                # print(title, url, date_Today)
                # time.sleep(666)
                if tool.Transformation(date) > tool.Transformation(date_Today):
                    continue
                if tool.Transformation(date) <= tool.Transformation(date_Today):
                    if tool.removal(title, date):
                        self.parse_detile(title, url, date_Today)
                        # print(title, url, date_Today)
                    else:
                        self.url = self.url_code.pop(0)
                        print('【existence】', url)
                else:
                    self.url = self.url_code.pop(0)
                    print('日期不符, 正在切换类型...', date_Today, self.url)
                    page = 0
                    break
            if page == 20:
                self.url = self.url_code.pop(0)
                break
            else:
                page+=1

    def parse_detile(self, title, url, date):
        print(url)
        # print(self.requests_get(url).replace('\ufffd', ''))
        # time.sleep(6666)
        url_html = etree.HTML(self.requests_get(url, self.headers))
        try:
            detail = url_html.xpath('//*[@class="hei_text"]')[0]
            detail_html = etree.tostring(detail, method='HTML')
            detail_html = html.unescape(detail_html.decode())
            detail_text = url_html.xpath('string(//*[@class="hei_text"])').replace('\xa0', '')\
                .replace('\n', '').replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')\
                .replace('\ufffd', '')
        except:
            detail = url_html.xpath('//*[@class="context"]')[0]
            detail_html = etree.tostring(detail, method='HTML')
            detail_html = html.unescape(detail_html.decode())
            detail_text = url_html.xpath('string(//*[@class="context"])').replace('\xa0', '') \
                .replace('\n', '').replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '') \
                .replace('\ufffd', '')
        # print(detail_text)
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
        item['resource'] = '北京市建设工程信息网'
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
        jl = beijing_gcjs()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
        tool.send_error('报错文件：'+str(os.path.basename(__file__))+'报错信息：'+str(e))

