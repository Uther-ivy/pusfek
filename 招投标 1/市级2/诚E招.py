# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 诚E招
class xinyang_ggzy:
    def __init__(self):
        self.url_list = [
            'https://www.chengezhao.com/cms/categories/%E4%B8%9A%E5%8A%A1%E5%85%AC%E5%91%8A/%E9%A1%B9%E7%9B%AE%E5%85%AC%E5%91%8A/{}',
            'https://www.chengezhao.com/cms/categories/%E4%B8%9A%E5%8A%A1%E5%85%AC%E5%91%8A/%E5%8F%98%E6%9B%B4%E5%85%AC%E5%91%8A/{}',
            'https://www.chengezhao.com/cms/categories/%E4%B8%9A%E5%8A%A1%E5%85%AC%E5%91%8A/%E4%B8%AD%E6%A0%87%E5%85%AC%E7%A4%BA/{}',
            'https://www.chengezhao.com/cms/categories/%E4%B8%9A%E5%8A%A1%E5%85%AC%E5%91%8A/%E7%BB%93%E6%9E%9C%E5%85%AC%E5%91%8A/{}'
        ]
        self.url = self.url_list.pop(0)
        self.headers = {
            'Host': 'www.chengezhao.com',
            'Cookie': 'UM_distinctid=17ba5210c1869d-0fa2fe28443858-4343363-1fa400-17ba5210c194e6; CNZZDATA1272953841=2129441374-1630499149-%7C1630499149; __root_domain_v=.chengezhao.com; _qddaz=QD.591530563011911; _qdda=3-1.1; _qddab=3-4yp27l.kt2j487a; JSESSIONID=FFE8A18B09A3B9EC05778D2853C6B915',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        }

    def parse(self):
        date = tool.date
        # date = '2020-07-01'
        page = 0
        while True:
            page += 1
            if page == 1:
                text = tool.requests_get(self.url.format(''), self.headers)
            else:
                text = tool.requests_get(self.url.format('/page/'+str(page)+'/'), self.headers)
            html = HTML(text)
            print('*' * 20, page, '*' * 20)
            detail = html.xpath('//*[@class="cez-business-main__news"]/div')
            for li in detail:
                try:
                    title = li.xpath('./div[2]/h3/a/text()')[0].replace('\xa0', '').replace(' ', '')
                    url = 'https://www.chengezhao.com' + \
                          li.xpath('./div[2]/h3/a/@href')[0]
                    date_Today = li.xpath('./a/span[2]/text()')[0] + '-' + li.xpath('./a/span[1]/text()')[0]
                except:
                    continue
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
                    print('日期不符, 正在切换类型', date_Today)
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
            detail = url_html.xpath('/html/body/div[3]/div[1]/div[2]')[0]
            detail_html = etree.tostring(detail, method='HTML')
            detail_html = html.unescape(detail_html.decode()).replace('\xa0', '').replace('\ufeff', '')
            detail_text = url_html.xpath('string(/html/body/div[3]/div[1]/div[2])') \
                .replace('\xa0', '').replace('\n', '').replace('\r', '').replace('\t', '') \
                .replace(' ', '').replace('\xa5', '').replace('\ufeff', '')
        except:
            detail = url_html.xpath('/html/body/div[4]/div/div[2]/div[2]')[0]
            detail_html = etree.tostring(detail, method='HTML')
            detail_html = html.unescape(detail_html.decode()).replace('\xa0', '').replace('\ufeff', '')
            detail_text = url_html.xpath('string(/html/body/div[4]/div/div[2]/div[2])') \
                .replace('\xa0', '').replace('\n', '').replace('\r', '').replace('\t', '') \
                .replace(' ', '').replace('\xa5', '').replace('\ufeff', '')
        # print(detail_text.replace('\xa0','').replace('\xa5',''))
        # time.sleep(6666)
        item = {}
        item['title'] = title.replace('\u2022', '')
        item['url'] = url
        item['date'] = date
        item['typeid'] = tool.get_typeid(item['title'])
        item['senddate'] = int(time.time())
        item['mid'] = 867
        item['infotype'] = tool.get_infotype(item['title'])
        item['body'] = tool.qudiao_width(detail_html)
        try:
            rst = re.findall('<div class="article-bottom">.*?</div>', item['body'], re.S)[0]
            item['body'] = item['body'].replace(rst, '')
        except:
            pass
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
        item['nativeplace'] = tool.get_title_city(item['title'])
        if item['nativeplace'] == 0:
            item['nativeplace'] = tool.more(item['title']+detail_text)
        item['linkman'] = tool.get_linkman(detail_text)
        item['function'] = tool.get_function(detail_text)
        item['resource'] = '诚E招电子采购交易平台'
        item["shi"] = int(str(item["nativeplace"]).split('.')[0])
        if len(str(int(item["shi"]))) == 4:
            item['sheng'] = int(str(item["shi"])[:2] + '00')
        elif len(str(int(item["shi"]))) == 5:
            item['sheng'] = int(str(item["shi"])[:3] + '00')
        else:
            item['sheng'] = 0
        item['removal']= title
        process_item(item)
        # print(item['body'])

if __name__ == '__main__':
    import traceback, os
    try:
        jl = xinyang_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()


