# -*- coding: utf-8 -*-
import json
import re
import time, html
from lxml import etree
import tool
from save_database import process_item

# 中国节能环保集团有限公司电子采购平台
class alashan_ggzy:
    def __init__(self):
        self.url_code = [
            'https://www.ebidding.cecep.cn/jyxx/001006/001006004/{}.html',
        ]
        self.url = self.url_code.pop(0)
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Cookie': '5nENl3yanoW7O=5SQDF_A5ORIYTBkVJDmB.9Oxj6F2K7FLeMjG1yn1yuGGwDd3F77dhqiOIQI5pF7x6e1Gg3iP1rCTX6B89hZjolA; 5nENl3yanoW7P=9DEdwbGkiCxBeGVXJBgc3AyO7EywmxBNXWLRROZzkMpzBUN2i4SNmFPM8Mbgi.2LqYRuscELsqYHvakWSCnI4vlyjlhLQ7CY8QeHduoprEFlJCUxtypNNO_1VjTfjptVydv_k4I6M5bIJYsbunAfEwIitkcTLNHI_iOppJkS5e7CH0J6wPKh3mke9CxqO91u94VZTR6ibaWjSu3yGQP11j8WlWIVTKGy2Lof_D.bUs.yV9D7ALbLuTCIMgGK3zgAbsMQOJkIStgWNauXKZrqjwfXoIViOPYTtXjAkanRMNGefVtnwosepBB9QIq3rqFzgLfHXws2Huo.Sc0_.LiHN6_cvuM822GuLPPGM95IXlg',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
        }

    def parse(self):
        date = tool.date
        # date = '2021-05-08'
        page = 99
        while True:
            page += 1
            print('*' * 20, page, '*' * 20)
            if page == 1:
                text = tool.requests_get(self.url.format('bidinfo'), self.headers)
            else:
                text = tool.requests_get(self.url.format(page), self.headers)
            # print(111, text)
            # time.sleep(666)
            detail = etree.HTML(text).xpath('//*[@class="go-items"]/li')
            for li in detail:
                try:
                    title = li.xpath('./a/div[1]/span[1]/text()')[0].replace("\r", '').replace("\n", '').replace("\t", '').replace(" ", '')
                    url = 'https://www.ebidding.cecep.cn' + li.xpath('./a/@href')[0]
                    date_Today = li.xpath('./a/div[1]/span[2]/text()')[0]
                    # print(title, url, date_Today)
                    # time.sleep(666)
                    if tool.Transformation(date) <= tool.Transformation(date_Today):
                        # if tool.removal(title, date):
                            self.parse_detile(title, url, date_Today)
                    else:
                            print('日期不符', url)
                            return
                except Exception as e:
                    traceback.print_exc()


    def parse_detile(self, title, url, date):
        print(url)
        url_text = tool.requests_get(url, self.headers)
        url_html = etree.HTML(url_text)

        detail = url_html.xpath('//*[@class="ewb-look"]')[0]
        detail_html = etree.tostring(detail, method='HTML')
        detail_html = html.unescape(detail_html.decode())

        detail_ = url_html.xpath('//*[@class="ewb-look ggcontent"]')[0]
        detail_html_ = etree.tostring(detail_, method='HTML')
        detail_html_ = html.unescape(detail_html_.decode())

        detail_html = detail_html+detail_html_
        detail_text = url_html.xpath('string(//*[@id="newinfo"])').replace('\xa0', '').replace('\n',
                                                                                                           '').replace(
            '\r', '').replace('\t',
                              '').replace(
            ' ', '').replace('\xa5', '')
        item = {}
        item['title'] = title.replace('\u2022', '')
        item['url'] = url
        item['date'] = date
        item['typeid'] = tool.get_typeid(item['title'])
        item['senddate'] = int(time.time())
        item['mid'] = 867
        item['nativeplace'] = float(tool.get_title_city(item['title']))
        if item['nativeplace'] == 0:
            item['nativeplace'] = float(tool.more(item['title']+ detail_text))
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
        item['resource'] = '中国节能环保集团有限公司电子采购平台'
        item["shi"] = int(item["nativeplace"])
        if len(str(item["nativeplace"])) == 4:
            item['sheng'] = int(str(item["nativeplace"])[:2] + '00')
        elif len(str(item["nativeplace"])) == 5:
            item['sheng'] = int(str(item["nativeplace"])[:3] + '00')
        else:
            item['sheng'] = 0
        item['removal']= title
        process_item(item)
        # print(item['nativeplace'], item['title'])

if __name__ == '__main__':
    import traceback, os
    try:
        jl = alashan_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
        tool.send_error('报错文件：'+str(os.path.basename(__file__))+'报错信息：'+str(e))

