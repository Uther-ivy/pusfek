# -*- coding: utf-8 -*-
import json
import random
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 上海公共资源交易中心
class shanghai_ggzy:
    def __init__(self):
        self.url_list = [
            # 'https://www.shggzy.com/jyxxgc',
            # 'https://www.shggzy.com/jyxxzc',
            'https://www.shggzy.com/search/{}'
        ]
        self.url = self.url_list.pop(0)
        self.code = ''
        self.headers = {
            'Cookie': 'Hm_lvt_ddd51655888df4f02c24c55810416e80=1658213467; _site_id_cookie=1; JSESSIONID=3e1235f9-eea6-421e-81e4-a44b94d37f89; SESSION=M2UxMjM1ZjktZWVhNi00MjFlLTgxZTQtYTQ0Yjk0ZDM3Zjg5; JIDENTITY=db70ffdb-05da-4145-9f21-823ecb595474; Hm_lpvt_ddd51655888df4f02c24c55810416e80=1658213920',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        }

    def parse(self):
        date = tool.date
        # date = '2021-06-18'
        page = 5000
        code=  HTML(tool.requests_get('https://www.shggzy.com/jyxxgc',self.headers)).xpath('//*[@id="cExt"]/@value')[0]
        while True:
            page += 1
            if page == 1:
                text = tool.requests_get(self.url.format(f'queryContents.jhtml?title=&channelId=33&origin=&inDates=&ext=&timeBegin=&timeEnd=&ext1=&ext2=&cExt={code}'), self.headers)

            else:
                text = tool.requests_get(self.url.format(f'queryContents_{page}.jhtml?title=&channelId=33&origin=&inDates=&ext=&timeBegin=&timeEnd=&ext1=&ext2=&cExt={self.code}'),self.headers)

            if '<div>本栏目暂无信息</div>' in text:
                print('#' * 20, 'channel is  None', '#' * 20)
                time.sleep(10 + random.random() * 10)
            #     text = tool.requests_get(self.url.format(page), self.headers)
            print(text)
            detail = HTML(text).xpath('//*[@id="content"]/div/div/div/div[2]/div[3]/div/ul/li')
            self.code = HTML(text).xpath('//*[@id="cExt"]/@value')[0]
            print('*' * 20, page, '*' * 20)
            # time.sleep(6666)
            for li in detail:
                try:
                    title = li.xpath('./span[2]/text()')[0].strip()
                    url = li.xpath('./@onclick')[0].replace("window.open('", '').replace("')", '')
                    date_Today = li.xpath('./span[4]/text()')[0].strip().replace('.', '-')
                    if 'http' not in url:
                        url = 'https://www.shggzy.com' + url
                    print(title, url, date_Today)
                    # time.sleep(666)
                    if tool.Transformation(date) <= tool.Transformation(date_Today):
                        # if tool.removal(title, date):
                            self.parse_detile(title, url, date_Today)
                        # else:
                        #     print('【existence】', url)
                        #     continue
                    else:
                        print('时间不符，正在切换类型', date_Today)
                        return
                except Exception:
                    traceback.print_exc()
            if not detail:
                print('last page')
                return
            # self.url = self.url_list.pop(0)
            # page = 0
    #
    def parse_detile(self, title, url, date):
        print(url)
        url_html = etree.HTML(tool.requests_get(url, self.headers))
        try:
            detail = url_html.xpath('//*[@class="table_1"]')[0]
            detail_html = etree.tostring(detail, method='HTML')
            detail_html = html.unescape(detail_html.decode())
            detail_text = url_html.xpath('string(//*[@class="table_1"])').replace('\xa0',
                                                                                                         '').replace(
                '\n', ''). \
                replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
        except:
            return
        # print(detail_html)
        # time.sleep(6666)
        item = {}
        item['title'] = title.replace('\u2022', '').replace(' ','')
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
        item['winner'] = tool.get_winner(detail_text)
        item['address'] = tool.get_address(detail_text)
        item['linkman'] = tool.get_linkman(detail_text)
        item['function'] = tool.get_function(detail_text)
        item['resource'] = '上海公共资源交易中心'
        item['shi'] = int(str(item["nativeplace"]).split('.')[0])
        item['sheng'] = 5000
        item['removal']= title
        process_item(item)
        
    def get_nativeplace(self, addr):
        city = ''
        city_list = [['5001', '黄浦区'], ['5002', '卢湾区'], ['5003', '徐汇区'], ['5004', '长宁区'], ['5005', '静安区'], ['5006', '普陀区'], ['5007', '闸北区'], ['5008', '虹口区'], ['5009', '杨浦区'], ['5010', '闵行区'], ['5011', '宝山区'], ['5012', '嘉定区'], ['5013', '浦东新区'], ['5014', '金山区'], ['5015', '松江区'], ['5016', '青浦区'], ['5017', '南汇区'], ['5018', '奉贤区'], ['5019', '崇明县']]

        for i in city_list:
            if i[1] in addr:
                city = float(i[0])
                break
        if city == '':
            city = 5000
        return city

if __name__ == '__main__':
    import traceback, os
    try:
        jl = shanghai_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
