# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 张掖市公共资源交易网
class baoshan_ggzy:
    def __init__(self):
        self.url_list = [
            'http://60.165.196.18:8090/EpointWebBuilder/jyxxInfoListAction.action?cmd=getInfolist&siteguid=7eb5f7f1-9041-43ad-8e13-8fcb82ea831a&daytime=&jyfrom=&xxtype=001001&jytype=&jyfs=&title=&pageSize=16&pageIndex={}',

            'http://60.165.196.18:8090/EpointWebBuilder/jyxxInfoListAction.action?cmd=getInfolist&siteguid=7eb5f7f1-9041-43ad-8e13-8fcb82ea831a&daytime=&jyfrom=&xxtype=001002&jytype=&jyfs=&title=&pageSize=16&pageIndex={}'

                         ]
        self.url = self.url_list.pop(0)
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36',
        }

    def parse(self):
        date = tool.date
        # date = '2020-12-04'
        page = 0
        while True:
            text = tool.requests_get(self.url.format(page), self.headers)
            page += 1
            print('*' * 20, page, '*' * 20)
            # html = HTML(text)
            # print(11, text)
            # time.sleep(6666)
            detail = json.loads(json.loads(text)['custom'])['Table']
            for li in detail:
                title = li['realtitle'].replace('\n', '').replace('\r', '')\
                    .replace('\t', '').replace(' ', '').replace('<spanstyle="color:red">', '').replace('</span>', '')
                url = li['href']
                if 'http' not in url:
                    url = 'http://60.165.196.18:8090' + url
                date_Today = li['date'].replace('\n', '').replace('\r', '') \
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
        print(url)
        t = tool.requests_get(url, self.headers)
        url_html = etree.HTML(t)
        try:
            detail = url_html.xpath('//*[@id="tab-1"]')[0]
            detail_html = etree.tostring(detail, method='HTML')
            detail_html = html.unescape(detail_html.decode())
            detail_text = url_html.xpath('string(//*[@id="tab-1"])').replace('\xa0', '').replace('\n',
                                                                                                              ''). \
                replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
            if len(detail_html) < 300:
                return
        except:
            detail = url_html.xpath('//*[@class="ewb-info-con"]')[0]
            detail_html = etree.tostring(detail, method='HTML')
            detail_html = html.unescape(detail_html.decode())
            detail_text = url_html.xpath('string(//*[@class="ewb-info-con"])').replace('\xa0', '').replace('\n',
                                                                                                 ''). \
                replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
            if len(detail_html) < 300:
                return
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
        item['resource'] = '张掖市公共资源交易网'
        item['shi'] = 14507
        item['sheng'] = 14500
        item['removal']= title
        process_item(item)

    def get_nativeplace(self, addr):
        city = ''
        city_list = [['14507.001', '甘州区'], ['14507.002', '肃南裕固族自治县'], ['14507.003', '民乐县'], ['14507.004', '临泽县'], ['14507.005', '高台县'], ['14507.006', '山丹县']]

        for i in city_list:
            if i[1] in addr:
                city = float(i[0])
                break
        if city == '':
            city = 14507
        return city

if __name__ == '__main__':
    import traceback, os
    try:
        jl = baoshan_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
        tool.send_error('报错文件：'+str(os.path.basename(__file__))+'报错信息：'+str(e))


