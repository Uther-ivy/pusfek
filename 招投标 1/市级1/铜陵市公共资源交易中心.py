# -*- coding: utf-8 -*-
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 铜陵市公共资源交易中心
class wenshan_ggzy:
    def __init__(self):
        self.url_list = [
            'https://ggzyjyzx.tl.gov.cn/tlsggzy/ShowInfo/Jysearch.aspx?zbfs=&fbdate=all&ywtype=006&jyly=&infotype=001&Eptr3=&Paging={}', #招标公告
            'https://ggzyjyzx.tl.gov.cn/tlsggzy/ShowInfo/Jysearch.aspx?zbfs=&fbdate=all&ywtype=007&jyly=&infotype=001&Eptr3=&Paging={}',
                    ]
        self.url = self.url_list.pop(0)
        self.headers = {
            # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            # 'Host': 'ggzyjyzx.tl.gov.cn',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
            'Cookie': '__jsluid_s=733c300b9fd39766355c8b2dff153c2a; __jsl_clearance_s=1678939772.683|0|tl3AzfGXdvfGJLchCuDCi4BXAKU%3D; ASP.NET_SessionId=ibzp0ke40d5zxas32hwt1mgf'
        }
        self.session = requests.session()
    def parse(self):
        date = tool.date
        # date = '2020-09-21'
        page = 0

        while True:
            page += 1
            text=self.session.get(self.url.format(page), headers=self.headers).content.decode()
            print('*' * 20, page, '*' * 20)
            # print(11, text)
            html = HTML(text)
            # time.sleep(6666)
            detail = html.xpath('//*[@class="ewb-list_bd"]//li')
            for li in detail:
                title = li.xpath('./div/a/text()')[0].replace('\n', '').\
                    replace('\r', '').replace('\t', '').replace(' ', '')
                url = 'https://ggzyjyzx.tl.gov.cn' + li.xpath('./div/a/@href')[0]
                date_Today = li.xpath('./span/text()')[0].replace('\xa0', '').replace('\n', '').\
                    replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
                print(title, url, date_Today)
                # time.sleep(666)
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
                print('日期不符, 正在切换类型')
                self.url = self.url_list.pop(0)
                break

    def parse_detile(self, title, url, date):
        print(url)
        t = self.session.get(url,headers=self.headers).content.decode()
        # print(t)
        # time.sleep(2222)
        url_html = etree.HTML(t)
        try:
            detail = url_html.xpath('//*[@id="mainContent"]')[0]
            detail_html = etree.tostring(detail, method='HTML')
            detail_html = html.unescape(detail_html.decode()).replace("display: none", '')
            detail_text = url_html.xpath('string(//*[@id="TDContent"])').replace('\xa0', '').replace('\n', '').\
                replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
            if len(detail_html) < 200:
                int('a')
        except:
            detail = url_html.xpath('//*[@id="mainContent"]')[0]
            detail_html = etree.tostring(detail, method='HTML')
            detail_html = html.unescape(detail_html.decode()).replace("display: none", '')
            detail_text = url_html.xpath('string(//*[@id="mainContent"])').replace('\xa0', '').replace('\n', ''). \
                replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
            if len(detail_html) < 200:
                int('a')
        item = {}
        item['title'] = title.replace('\u2022', '')
        item['url'] = url
        item['date'] = date
        item['typeid'] = tool.get_typeid(item['title'])
        item['senddate'] = int(time.time())
        item['mid'] = 867
        item['nativeplace'] = self.get_nativeplace(item['title'])
        item['infotype'] = tool.get_infotype(item['title'])
        item['body'] = tool.qudiao_width(detail_html)
        item['body'] = item['body'].replace('''<a href="http://www.hfztb.cn" target="_blank"><img src="../Template/Default/images/wybm.png"></a>''', '')
        # print(item['body'].replace('\xa0', '').replace('\xa5', '').replace('\xb3', ''))
        # time.sleep(6666)
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
        item['resource'] = '铜陵市公共资源交易中心'
        item['shi'] = 6507
        item['sheng'] = 6500
        item['removal']= title
        process_item(item)
    def get_nativeplace(self, addr):
        city = ''
        city_list = [['6507.001', '铜官山区'], ['6507.002', '狮子山区'], ['6507.003', '郊区'], ['6507.004', '铜陵县']]

        for i in city_list:
            if i[1] in addr:
                city = float(i[0])
                break
        if city == '':
            city = 6507
        return city

if __name__ == '__main__':
    import os,traceback
    try:
        jl = wenshan_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
        tool.send_error('报错文件：'+str(os.path.basename(__file__))+'报错信息：'+str(e))



