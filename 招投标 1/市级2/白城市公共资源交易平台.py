# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 白城市公共资源交易平台
class baicheng_ggzy:
    def __init__(self):
        self.url_code = [
            # 工程建设
            'http://ggzy.jlbc.gov.cn/jyxx/003001/{}.html',
            # 政府采购
            'http://ggzy.jlbc.gov.cn/jyxx/003002/{}.html'
        ]
        self.url = self.url_code.pop(0)
        self.headers = {
            'Cookie': 'bgm=1; _gscu_1728209423=79153648w57thj19; _gscbrs_1728209423=1; bgm=2; _gscs_1728209423='
                      '79153648czr3go19|pv:8',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75'
                          '.0.3770.100 Safari/537.36'
        }

    def parse(self):
        date = tool.date
        # date = '2020-01-10'
        page = 0
        while True:
            page += 1
            if page == 1:
                text = tool.requests_get(self.url.format('secondPage'), self.headers)
            else:
                text = tool.requests_get(self.url.format(str(page)), self.headers)
            html = HTML(text)
            print('*' * 20, page, '*' * 20)
            detail = html.xpath('//div[@class="ewb-info"]/ul/li')
            for li in detail:
                try:
                    title = li.xpath('./div/a/text()')[1].replace('\r', '').replace('\n', '').replace('\t','').replace(' ', '')
                except:
                    title = li.xpath('./div/a/text()')[0].replace('\r', '').replace('\n', '').replace('\t', '').replace(' ', '')
                url = 'http://ggzy.jlbc.gov.cn' + li.xpath('./div/a/@href')[0]
                date_Today = li.xpath('./span/text()')[0].replace('\r', '').replace('\n', '').replace('\t', '').replace(' ', '')
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
                    self.url = self.url_code.pop(0)
                    page = 0
                    break
            if page == 20:
                self.url = self.url_code.pop(0)
                page = 0
    def parse_detile(self, title, url, date):
        print(url)
        url_html = etree.HTML(tool.requests_get(url, self.headers))
        try:
            detail = url_html.xpath('//*[@id="commonarticle"]/div')[0]
            detail_html = etree.tostring(detail, method='HTML')
            detail_html = html.unescape(detail_html.decode())
            detail_text = url_html.xpath('string(//*[@id="commonarticle"]/div)').replace('\xa0', '').replace('\n', ''). \
                replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
        except:
            detail = url_html.xpath('//*[@class="news-article"]')[0]
            detail_html = etree.tostring(detail, method='HTML')
            detail_html = html.unescape(detail_html.decode())

            detail_ = url_html.xpath('//*[@class="news-article-info"]')[0]
            detail_html_ = etree.tostring(detail_, method='HTML')
            detail_html_ = html.unescape(detail_html_.decode())
            detail_html = detail_html.replace(detail_html_, '')
            detail_text = url_html.xpath('string(//*[@class="news-article"])').replace('\xa0', '').replace('\n', ''). \
                replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
        # print(detail_text.replace('\xa0','').replace('\xa5',''))
        # time.sleep(6666)
        width_list = re.findall('width="(.*?)"', detail_html)
        for i in width_list:
            detail_html = detail_html.replace(' width="{}"'.format(i), '')
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
        item['resource'] = '白城市公共资源交易平台'
        item['shi'] = 4008
        item['sheng'] = 4000
        # print(item)
        item['removal']= title
        process_item(item)

    def get_nativeplace(self, addr):
        city = ''
        city_list = [['4008.001', '洮北区'], ['4008.002', '镇赉县'], ['4008.003', '通榆县'], ['4008.004', '洮南市'], ['4008.005', '大安市']]
        for i in city_list:
            if i[1] in addr:
                city = float(i[0])
                break
        if city == '':
            city = 4008
        return city

if __name__ == '__main__':
    import traceback, os
    try:
        jl = baicheng_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
        tool.send_error('报错文件：'+str(os.path.basename(__file__))+'报错信息：'+str(e))


