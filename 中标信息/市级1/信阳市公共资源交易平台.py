# -*- coding: utf-8 -*-
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 信阳市公共资源交易平台
class xinyang_ggzy:
    def __init__(self):
        self.url_list = [
            # 建设工程
            # 招标公告
            # 'http://www.xyggzyjy.cn/jyxx/002001/002001001/{}.html',
            # 变更公告
            # 'http://www.xyggzyjy.cn/jyxx/002001/002001002/{}.html',
            # 中标结果
            'http://www.xyggzyjy.cn/jyxx/002001/002001003/{}.html',
            # 政府采购
            # 采购公告
            # 'http://www.xyggzyjy.cn/jyxx/002002/002002001/{}.html',
            # 变更公告
            # 'http://www.xyggzyjy.cn/jyxx/002002/002002002/{}.html',
            # 中标结果
            'http://www.xyggzyjy.cn/jyxx/002002/002002003/{}.html'
        ]
        self.url = self.url_list.pop(0)
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        }

    def parse(self):
        date = tool.date
        # date = '2020-03-20'
        page =80
        for i in range(1,20):
            page += 1
            if page == 1:
                text = tool.requests_get(self.url.format('moreinfo'), self.headers)
            else:
                text = tool.requests_get(self.url.format(page), self.headers)
            print('*' * 20, page, '*' * 20)
            html = HTML(text)
            # print(11, text)
            # time.sleep(6666)
            detail = html.xpath('//*[@id="showList"]/li')
            for li in detail:
                try:
                    try:
                        title = li.xpath('./span[2]/a/text()')[0]
                        url = 'http://www.xyggzyjy.cn' + li.xpath('./span[2]/a/@href')[0]
                        date_Today = li.xpath('./span[1]/text()')[0].replace('\n', '').replace('\t', '').replace('\r', '')\
                            .replace(' ', '').replace('[', '').replace(']', '')
                    except:
                        title = li.xpath('./a/div[1]/@title')[0]
                        url = 'http://www.xyggzyjy.cn' + li.xpath('./a/@href')[0]
                        date_Today = li.xpath('./a/div[2]/text()')[0].replace('\n', '').replace('\t', '').replace('\r', '') \
                            .replace(' ', '').replace('[', '').replace(']', '')
                    # print(title, url, date_Today)
                    # time.sleep(666)
                    if '测试' in title:
                        continue
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
        try:
            detail = url_html.xpath('//*[@id="mainContent"]')[0]
            detail_html = etree.tostring(detail, method='HTML')
            detail_html = html.unescape(detail_html.decode()).replace('\xa0', '').replace('\ufeff', '')
            detail_text = url_html.xpath('string(//*[@id="mainContent"])') \
                .replace('\xa0', '').replace('\n', '').replace('\r', '').replace('\t', '') \
                .replace(' ', '').replace('\xa5', '').replace('\ufeff', '')
        except:
            try:
                detail = url_html.xpath('//*[@class="ewb-article-info"]')[0]
                detail_html = etree.tostring(detail, method='HTML')
                detail_html = html.unescape(detail_html.decode()).replace('\xa0', '').replace('\ufeff', '')
                detail_text = url_html.xpath('string(//*[@class="ewb-article-info"])') \
                    .replace('\xa0', '').replace('\n', '').replace('\r', '').replace('\t', '') \
                    .replace(' ', '').replace('\xa5', '').replace('\ufeff', '')
            except:
                detail = url_html.xpath('//*[@class="detail-infos"]')[0]
                detail_html = etree.tostring(detail, method='HTML')
                detail_html = html.unescape(detail_html.decode()).replace('\xa0', '').replace('\ufeff', '')
                detail_text = url_html.xpath('string(//*[@class="detail-infos"])') \
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
        item['resource'] = '信阳市公共资源交易平台'
        item['shi'] = 8515
        item['sheng'] = 8500
        item['removal']= title
        process_item(item)
        # print(item['body'])

    def get_nativeplace(self, addr):
        city = ''
        city_list = [['8515.001', '师河区'], ['8515.01', '息县'], ['8515.002', '平桥区'], ['8515.003', '罗山县'], ['8515.004', '光山县'], ['8515.005', '新县'], ['8515.006', '商城县'], ['8515.007', '固始县'], ['8515.008', '潢川县'], ['8515.009', '淮滨县']]
        for i in city_list:
            if i[1] in addr:
                city = float(i[0])
                break
        if city == '':
            city = 8515
        return city

if __name__ == '__main__':
    import traceback, os
    try:
        jl = xinyang_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
        tool.send_error('报错文件：'+str(os.path.basename(__file__))+'报错信息：'+str(e))


