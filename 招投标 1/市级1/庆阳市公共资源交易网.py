# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 庆阳市公共资源交易网
class baoshan_ggzy:
    def __init__(self):
        self.url_list = [
            'http://www.qysggzyjy.cn/f/newtrade/tenderannquainqueryanns/getListByProjectTypePage?projectType=all&purchaseCode=&gsPlatformNavActive=1&projectName=&tradePlatformId=1&tenderMode=1&pageNo={}',
                         ]
        self.url = self.url_list.pop(0)
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36',
            'Cookie': '57316358-5b93-41e5-84e0-c7c5edc5a34d=4873b8813097634064ed5386efdcc37a; _gscu_1294440987=78754415pk8bs914; wafatcltime=1678756449108; wafatclconfirm=cSq+1xuI6ew5XWMj6MHsqLh3ZQnsJy7fM09sKPd6U/reJ8Lh+AT20UKwDHQdGYKkERIdFuI1QV2944XKbxRunvpH3k1A6kt1i2B9ZjhF78k24zZiP2DHszEMgLoY8oYO39SAfqMYOHMiWVlaGTIpcWX9lJPoBHzaL9N+6plKMkDb9TSPF2RCa6pf/sfQXEjW1q5CMMT4qaUMuaS4RDVP0drl/6OMY2XjhQzjxmrEQ3F3GujYut1X6oGGgVFJ21hENcMtyqzD45IhWYxXhH97+E1jjDxEExp5ocnZIJZiAVMdEefUdioNQKPBwv4UlDD6wMvOgZbZrOQSxSYEmVve7PrxTZ0Um3N6tSmvHdV+uTcVIVxSDQtvUyfgcgmjH2Nj3jxsJgU0XuUQOZKOjz9Gbitj3d6cjHufBoVPxqHj+AFxeQSjFgYJQnLpDFVelDPTPpGrs9bIEou/ElzqhHQki+Z8UFe+TcPz8apb29xxftkz9SG5EmTIZh0P+XfjAM2G3WnooUklZrXJ+aMqjkPDu8/5CIx3IgSKQSFb2MQQsPhd+SR/E6uRVxzrAEKbNUdjIMuk7xMBZEa3zGmnvjqiEc8DB6FLYr4clYzKE8hTDmESp9ikF8p8Jy1VnaQ0LWGwzAXm628vWh3K1KwkOdukqKohg+DJsxVEgp7RX9mi/bVRZEg28FEneyXvFfcYHGLIiV4nXftbK6QuzZkRLQTPOBegj5X2fNwyYRIG2R3f6CnjNdjd5IYVLoMBsG7LErxN; wafatcltoken=9a5bbca1d127ddc02f765a80d5988887; HWWAFSESID=531e09a7f1ee6933be; HWWAFSESTIME=1678756446390; Hm_lvt_b8d6f1a9842a0d2ecd4feb373d794987=1678754414,1678756491; _gscbrs_1294440987=1; Hm_lpvt_b8d6f1a9842a0d2ecd4feb373d794987=1678756740; _gscs_1294440987=78756491vltt0e14|pv:6'
        }
        self.data={'projectType': 'A',
'purchaseCode':"",
'gsPlatformNavActive': 1,
'projectName': "",
'tradePlatformId': 1,
'tenderMode': 'all'
}

    def parse(self):
        date = tool.date
        # date = '2021-07-27'
        page = 0
        while True:
            page += 1
            text = tool.requests_post_to(self.url.format(page),data=self.data,headers=self.headers)
            print('*' * 20, page, '*' * 20)
            html = HTML(text)
            # print(11, text)
            # time.sleep(6666)
            detail = html.xpath('//a[@class="gsPropertyBox"]')

            for li in detail:
                title = li.xpath('./li/p/@title')[0].replace('\n', '').replace('\r', '') \
                    .replace('\t', '').replace(' ', '').replace('<spanstyle="color:red">', '').replace('</span>', '')
                url1 = li.xpath('./@href')[0]

                # if 'http' not in url:
                url = 'http://www.qysggzyjy.cn' + url1

                date_Today = li.xpath('./li/span/text()')[0].replace('\n', '').replace('\r', '') \
                    .replace('\t', '').replace(' ', '').replace('(', '').replace(')', '')
                if '测试' in title:
                    continue
                # print(title, url, date_Today)
                # time.sleep(666)
                if tool.Transformation(date) <= tool.Transformation(date_Today):
                    if tool.removal(title, date):
                        self.parse_detile(title, url, date_Today)
                    else:
                        print('【existence】', url)
                        continue
                else:
                    print('日期不符, 正在切换类型', date_Today, self.url)
                    return


    def parse_detile(self, title, url, date):
        # print(url2)
        t = tool.requests_get(url, self.headers)

        url_html = etree.HTML(t)
        # if 'pageIndex=5' in url:
        #     try:
        detail = url_html.xpath('//div[@class="jxTradingPublic"]/div')[0]
        detail_html = etree.tostring(detail, method='HTML')
        detail_html = html.unescape(detail_html.decode())
        detail_text = url_html.xpath('string(//div[@class="jxTradingPublic"]/div/span/text())').replace('\xa0', '').replace('\n',
                                                                                                          ''). \
            replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
        if len(detail_html) < 300:
            return
        # detail = url_html.xpath('//div[@class="jxTradingPublic"]/div/span/text()')
        # detail_html = '<embed width="100%" height="100%" src="{}">'.format(detail)
        # detail_text = ''
        #     except:
        #         detail = url_html.xpath('//*[@class="jxTradingPublic"]/div/a/@href')[0]
        #         detail_html = '<embed width="100%" height="100%" src="{}">'.format(detail)
        #         detail_text = ''
        # else:
        #     try:
        #         detail = url_html.xpath('//*[@class="jxTradingPublic"]')[0]
        #         detail_html = etree.tostring(detail, method='HTML')
        #         detail_html = html.unescape(detail_html.decode())
        #         detail_text = url_html.xpath('string(//*[@class="jxTradingPublic"])').replace('\xa0', '').replace('\n',
        #                                                                                                           ''). \
        #             replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
        #         if len(detail_html) < 300:
        #             return
        #     except:
        #         detail = url_html.xpath('//*[@class="layui-collapse"]')[0]
        #         detail_html = etree.tostring(detail, method='HTML')
        #         detail_html = html.unescape(detail_html.decode())
        #         detail_text = url_html.xpath('string(//*[@class="layui-collapse"])').replace('\xa0', '').replace('\n',
        #                                                                                                          ''). \
        #             replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
        #         if len(detail_html) < 300:
        #             return
        # print(t.replace('\xa0','').replace('\xa5',''))
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
        item['resource'] = '庆阳市公共资源交易网'
        item['shi'] = 14510
        item['sheng'] = 14500
        item['removal']= title
        # print(item)
        process_item(item)

    def get_nativeplace(self, addr):
        city = ''
        city_list = [['14510.001', '西峰区'], ['14510.002', '庆城县'], ['14510.003', '环县'], ['14510.004', '华池县'], ['14510.005', '合水县'], ['14510.006', '正宁县'], ['14510.007', '宁县'], ['14510.008', '镇原县']]

        for i in city_list:
            if i[1] in addr:
                city = float(i[0])
                break
        if city == '':
            city = 14510
        return city

if __name__ == '__main__':
    import traceback, os
    try:
        jl = baoshan_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
        tool.send_error('报错文件：'+str(os.path.basename(__file__))+'报错信息：'+str(e))


