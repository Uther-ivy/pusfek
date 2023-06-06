# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 中铁鲁班商务网
class baoshan_ggzy:
    def __init__(self):
        self.url_list = [
            {"timeType":"month","sTime":"2021-10-02 00:00:00","eTime":"2021-11-01 23:59:59","current":2,"size":10,"dirs":"desc","orders":"pub_time","title":""},
            {"timeType":"month","areaCode":"-1","mainType":"-1","purchaser":None,"information":None,"sTime":"","eTime":"","classify":"-1","region":"-1","level":"","selectedState":"","purchaseType":"-1","orders":"publish_time","dirs":"desc","current":2,"size":10,"page":{}},
        ]
        self.url = self.url_list.pop(0)
        self.headers = {
            'Accept': 'application/json, text/plain, */*',
            'Content-Type': 'application/json',
            'Cookie': 'Hm_lvt_ffa0230125bc68f1a6ef45cbcc9069c1=1635731382; qimo_seosource_2df5fcc0-f4f6-11eb-9edc-4f55385c0183=%E5%85%B6%E4%BB%96%E7%BD%91%E7%AB%99; qimo_seokeywords_2df5fcc0-f4f6-11eb-9edc-4f55385c0183=%E6%9C%AA%E7%9F%A5; qimo_xstKeywords_2df5fcc0-f4f6-11eb-9edc-4f55385c0183=; pageViewNum=4; Hm_lpvt_ffa0230125bc68f1a6ef45cbcc9069c1=1635731560',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        }

    def parse(self):
        page = 0
        while True:
            date = tool.date
            # date='2021-07-28'
            page += 1
            if 'areaCode' in self.url:
                index_url = 'https://eproport.crecgec.com/epu-portal/portal/project/listWithPage'
                self.url['current'] = page
            else:
                index_url = 'https://eproport.crecgec.com/epu-portal/portal/bid_notice/listWithPage'
                self.url['current'] = page
                self.url['sTime'] = time.strftime('%Y-%m-%d', time.localtime(time.time() - 86400*30)) + ' 00:00:00'
                self.url['eTime'] = date + ' 23:59:59'
            text = tool.requests_post_to(index_url, self.url,self.headers)
            detail = json.loads(text)['data']['records']
            for li in detail:
                url = li['']
                title = li['projectName']
                date_Today = li['createTime'][:10]
                if '发布' in date_Today:
                    continue
                if '测试' in title:
                    continue
                # print(title, url, date_Today)
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
        print(url)
        t = tool.requests_get(url, self.headers)
        if '请登录供方交易系统查看具体信息' in t:
            print('请登录供方交易系统查看具体信息')
            return False
        url_html = etree.HTML(t)
        try:
            detail = url_html.xpath('//*[@id="printTable"]')[0]
            detail_html = etree.tostring(detail, method='HTML')
            detail_html = html.unescape(detail_html.decode())
            detail_text = url_html.xpath('string(//*[@id="printTable"])').replace('\xa0', '').replace('\n', ''). \
                replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
        except:
            try:
                detail = url_html.xpath('//*[@class="allNoticCont displayNone"]')[0]
                detail_html = etree.tostring(detail, method='HTML')
                detail_html = html.unescape(detail_html.decode())
                detail_text = url_html.xpath('string(//*[@class="allNoticCont displayNone"])').replace('\xa0', '').replace('\n', ''). \
                    replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
            except:
                detail = url_html.xpath('//*[@class="allNoticCont"]')[0]
                detail_html = etree.tostring(detail, method='HTML')
                detail_html = html.unescape(detail_html.decode())
                detail_text = url_html.xpath('string(//*[@class="allNoticCont"])').replace('\xa0',
                                                                                                       '').replace('\n',
                                                                                                                   ''). \
                    replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
        item = {}
        item['title'] = title.replace('\u2022', '')
        item['url'] = url
        item['date'] = date
        item['typeid'] = tool.get_typeid(item['title'])
        item['senddate'] = int(time.time())
        item['mid'] = 867
        item['infotype'] = tool.get_infotype(item['title'])
        item['body'] = tool.qudiao_width(detail_html)
        item['endtime'] = tool.get_endtime(detail_text)
        item['nativeplace'] = tool.get_city(item['title'])
        if item['nativeplace'] == 0:
            item['nativeplace'] = tool.more(item['body'])
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
        item['resource'] = '中铁鲁班商务网'
        if '.' in str(item["nativeplace"]):
            item["shi"] = int(float(str(item["nativeplace"]).replace("['","").split('.')[0]))
        else:
            item["shi"] = int(float(item["nativeplace"]))
        if len(str(int(item["shi"]))) == 4:
            item['sheng'] = int(str(item["shi"])[:2] + '00')
        elif len(str(int(item["shi"]))) == 5:
            item['sheng'] = int(str(item["shi"])[:3] + '00')
        else:
            item['sheng'] = 0
        # print(item)
        item['removal']= title
        process_item(item)

if __name__ == '__main__':

    import traceback, os
    try:
        jl = baoshan_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
        tool.send_error('报错文件：'+str(os.path.basename(__file__))+'报错信息：'+str(e))


