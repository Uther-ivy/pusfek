# -*- coding: utf-8 -*-
import json
import re
import time, html
from lxml import etree
import tool
from save_database import process_item

# 北京江河润泽工程管理咨询有限公司
class alashan_ggzy:
    def __init__(self):
        self.url_code = [
            'https://www.chinabrr.com/zhaobiao?page={}',
            'https://www.chinabrr.com/zhongbiao?page={}',
        ]
        self.url = self.url_code.pop(0)
        self.headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Cookie': 'isInitAreaCode=null; _gscu_653689772=78282348u2bs1g18; _gscbrs_653689772=1; UM_distinctid=16f78f570621fa-0e76a94f9f3d2d-e343166-1fa400-16f78f570631fc; _gscs_653689772=t782895054fvlkv12|pv:14; CNZZDATA1260595804=985342442-1578282342-%7C1578291895',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
        }

    def parse(self):
        date = tool.date
        # date = '2021-04-13'
        page = 0
        while True:
            page += 1
            print('*' * 20, page, '*' * 20)
            text = tool.requests_get(self.url.format(page), self.headers)
            # print(111, text)
            # time.sleep(666)
            detail = etree.HTML(text).xpath('//*[@class="trbox"]/li')
            for li in detail:
                title = li.xpath('./a//text()')[1].replace('\r', '').replace('\t', '').replace(' ', '').replace('\n', '')
                url = 'https://www.chinabrr.com' + li.xpath('./a/@href')[0].replace('show', 'content')
                date_Today = li.xpath('./span/text()')[0].replace('\r', '').replace('\t', '').replace(' ', '').replace('\n', '').replace('发布于', '')
                # print(title, url, date_Today)
                # time.sleep(666)
                if tool.Transformation(date) <= tool.Transformation(date_Today):
                    if tool.removal(title, date):
                        self.parse_detile(title, url, date_Today)
                    else:
                        print('【existence】', url)
                        continue
                else:
                    print('日期不符, 正在切换类型...', date_Today, self.url)
                    self.url = self.url_code.pop(0)
                    page = 0

                    break
            if page == 20:
                self.url = self.url_code.pop(0)
                break

    def parse_detile(self, title, url, date):
        print(url)
        url_text = tool.requests_get(url, self.headers)
        url_html = etree.HTML(url_text)
        detail = url_html.xpath('//*[@class="article_txt"]')[0]
        detail_html = etree.tostring(detail, method='HTML')
        detail_html = html.unescape(detail_html.decode())
        detail_text = url_html.xpath('string(//*[@class="article_txt"])').replace('\xa0', '').replace('\n', '').replace('\r', '').replace('\t',
                                                                                                                  '').replace(
            ' ', '').replace('\xa5', '')
        item = {}
        item['title'] = title.replace('\u2022', '')
        item['url'] = url
        item['date'] = date
        item['typeid'] = tool.get_typeid(item['title'])
        item['senddate'] = int(time.time())
        item['mid'] = 867
        item['nativeplace'] = self.get_nativeplace(item['title']+detail_text)
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
        item['resource'] = '北京江河润泽工程管理咨询有限公司'
        item['shi'] = int(str(item['nativeplace']).split('.')[0])
        item['sheng'] = 1000
        item['removal']= title
        process_item(item)
        # print(item['nativeplace'], item['title'])

    def get_nativeplace(self, addr):
        city_list = [['1001', '东城区'], ['1002', '西城区'], ['1003', '崇文区'], ['1004', '宣武区'], ['1005', '朝阳区'], ['1006', '丰台区'], ['1007', '石景山区'], ['1008', '海淀区'], ['1009', '门头沟区'], ['1010', '房山区'], ['1011', '通州区'], ['1012', '顺义区'], ['1013', '昌平区'], ['1014', '大兴区'], ['1015', '怀柔区'], ['1016', '平谷区'], ['1017', '密云县'], ['1018', '延庆县']]

        for i in city_list:
            if i[1] in addr:
                return float(i[0])
        return 1000

if __name__ == '__main__':
    import traceback, os
    try:
        jl = alashan_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
        if 'pop from empty list'!=str(e):
            print('报错')
            with open('../error_name.txt', 'a+', encoding='utf-8')as f:
                f.write(str(os.path.basename(__file__)))
                f.write('\n')
                f.write(str(traceback.format_exc()))
                f.write('\n')
        else:
            with open('../success.txt', 'a+', encoding='utf-8')as f:
                f.write(str(os.path.basename(__file__)))
                f.write('\n')
                f.write(str('无连接抓取'))
                f.write('\n')

