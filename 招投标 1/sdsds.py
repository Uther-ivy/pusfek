# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
# from save_database import process_item

# 邯郸市交通运输局
class siping_ggzy:
    def __init__(self):
        self.url_code = [
            # 建设工
            'http://jtj.hd.gov.cn/zwgk/wjgg/{}.htm',
            # 政府采购
            # 'http://ggzy.siping.gov.cn/jyxx/004002/{}.html'
        ]
        self.url = self.url_code.pop(0)
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
# 'Accept-Encoding': 'gzip, deflate',
# 'Accept-Language': 'zh-CN,zh;q=0.9',
'Cache-Control': 'no-cache',
# 'Connection': 'keep-alive',
'Host': 'jtj.hd.gov.cn',
'Pragma': 'no-cache',
'Upgrade-Insecure-Requests': '1',
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.0.0 Safari/537.36'
        }

    def parse(self):
        date = tool.date
        # date = '2020-01-10'
        page = 0

        while True:
            page += 1
            # data = f'searchToTitle=&page.intPage={page}&page.pageInfoCount=20'
            if page == 1:
                text = tool.requests_get(self.url.format('index'), self.headers)
            else:
                text = tool.requests_get(self.url.format(f'index{page-1}'), self.headers)
            # text=tool.requests_get(url=self.url.format(page),headers=self.headers)
            # print(text)
            # break
            html = HTML(text)
            # html = json.loads(text)
            print('*' * 20, page, '*' * 20)
            detail = html.xpath('//div[@class="wjgg"]/ul/li')
            # print(len(detail))
            for li in detail:
                title = li.xpath('./a/text()')[0].strip()
                url = 'http://jtj.hd.gov.cn/zwgk/wjgg/'+li.xpath('./a/@href')[0]
                date_Today = li.xpath('./span/text()')[0][1:-1]
                print(title, url, date_Today)
                # break
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

    def parse_detile(self, title, url, date):
        # url1=f'https://ztb.hongshijt.com/api/bid/biddingShowMall/queryMyBidDetail?id={url}&_={int(time.time()*1000)}'
        print(url)
        session=requests.session()
        text= session.get(url=url, headers=self.headers,verify=False).content.decode()
        print(text)
        # url = 'http://jtj.hd.gov.cn/zwgk/wjgg/62259.htm'
        # text =requests.get(url, self.headers)
        # print(text)
        time.sleep(222222)
        url_html = etree.HTML(session)
        # url_html=json.loads(url_html)
        detail = url_html.xpath('//div[@class="art_con"]')[0]
        detail_html = etree.tostring(detail, method='HTML')
        detail_html = html.unescape(detail_html.decode())
        detail_text = url_html.xpath('string(//div[@class="art_con"])').replace('\xa0', '').replace('\n', ''). \
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
        item['nativeplace'] = tool.get_title_city(item['title'])
        if item['nativeplace'] == 0:
            item['nativeplace'] = tool.more(item['title']+detail_html)
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
        item['resource'] = '邯郸市交通运输局'
        item["shi"] = int(str(item["nativeplace"]).split('.')[0])
        if len(str(int(item["shi"]))) == 4:
            item['sheng'] = int(str(item["shi"])[:2] + '00')
        elif len(str(int(item["shi"]))) == 5:
            item['sheng'] = int(str(item["shi"])[:3] + '00')
        else:
            item['sheng'] = 0
        item['removal']= title
        print(item)
        # process_item(item)

    def get_nativeplace(self, addr):
        city = ''
        city_list = [['4003.001', '铁西区'], ['4003.002', '铁东区'], ['4003.003', '梨树县'], ['4003.004', '伊通满族自治县'], ['4003.005', '公主岭市'], ['4003.006', '双辽市']]
        for i in city_list:
            if i[1] in addr:
                city = float(i[0])
                break
        if city == '':
            city = 4003
        return city
if __name__ == '__main__':
    import traceback, os
    try:
        jl = siping_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
        tool.send_error('报错文件：'+str(os.path.basename(__file__))+'报错信息：'+str(e))


