# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 新乡市公共资源交易平台
class xinxiang_ggzy:
    def __init__(self):
        self.url_list = [
            # 政府采购
            # 公告信息
            'http://www.xxggzy.cn/EpointWebBuilder_new/jyxxyzmAction.action?cmd=getList',
        ]
        self.url = self.url_list.pop(0)
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        }

    def parse(self):
        date = tool.date
        # date = '2021-07-27'
        page = 0
        while True:
            page += 1
            data = {'siteGuid': '7eb5f7f1-9041-43ad-8e13-8fcb82ea831a',
                    'categorynum': '089003001',
                    'content': "",
                    'pageIndex': page,
                    'pageSize': 10,
                    'gglx': "",
                    'cgfs': "",
                    'startdate': "",
                    'enddate': ""
                    }
            text = tool.requests_post(self.url,data=data, headers=self.headers)
            # text.encoding = 'utf-8'
            # page=text.json()
            print('*' * 20, page, '*' * 20)
            page=json.loads(text)
            # print(11, text)
            # time.sleep(6666)
            custom = page["custom"]
            cus = json.loads(custom)
            table = cus["Table"]
            for li in table:
                title = li["title"]
                t = etree.HTML(title)
                title1 = ''.join(t.xpath('//text()'))
                date_Today = li["postdate"]
                href = li["href"]
                url = 'http://www.xxggzy.cn' + href

                # print(title, url, date_Today)
                # time.sleep(666)
                # self.parse_detile(title, url, date_Today)
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
        detail = url_html.xpath('//div[@class="article-info"]')[0]
        detail_html = etree.tostring(detail, method='HTML')
        detail_html = html.unescape(detail_html.decode())
        detail_text = url_html.xpath('string(//div[@class="article-info"])').replace('\xa0', '').replace('\n', '').\
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
        item['winner'] = tool.get_winner(detail_text)
        item['address'] = tool.get_address(detail_text)
        item['linkman'] = tool.get_linkman(detail_text)
        item['function'] = tool.get_function(detail_text)
        item['resource'] = '新乡市公共资源交易平台'
        item['shi'] = 8507
        item['sheng'] = 8500
        item['removal']= title
        # print(item["body"])
        process_item(item)

    def get_nativeplace(self, addr):
        city = ''
        city_list = [['8507.001', '红旗区'], ['8507.01', '长垣县'], ['8507.011', '卫辉市'], ['8507.012', '辉县市'], ['8507.002', '卫滨区'], ['8507.003', '凤泉区'], ['8507.004', '牧野区'], ['8507.005', '新乡县'], ['8507.006', '获嘉县'], ['8507.007', '原阳县'], ['8507.008', '延津县'], ['8507.009', '封丘县']]
        for i in city_list:
            if i[1] in addr:
                city = float(i[0])
                break
        if city == '':
            city = 8507
        return city


if __name__ == '__main__':
    import traceback, os
    try:
        jl = xinxiang_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
        tool.send_error('报错文件：'+str(os.path.basename(__file__))+'报错信息：'+str(e))


