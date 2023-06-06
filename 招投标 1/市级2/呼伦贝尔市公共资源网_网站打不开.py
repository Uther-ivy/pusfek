# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 呼和浩特公共资源网
class wenshan_ggzy:
    def __init__(self):
        self.url_list = [
            'http://www.hlbeggzyjy.org.cn/EpointWebBuilderService_New/EpointWebBuilderService/jyxxlistaction.action?cmd=getNewInfolist&pageIndex={}&pageSize=10&siteGuid=7eb5f7f1-9041-43ad-8e13-8fcb82ea831a&keywords=&categoryzhu=021001&fbsj=&dqfb=&xxlx=&jylx=',
            'http://www.hlbeggzyjy.org.cn/EpointWebBuilderService_New/EpointWebBuilderService/jyxxlistaction.action?cmd=getNewInfolist&pageIndex={}&pageSize=10&siteGuid=7eb5f7f1-9041-43ad-8e13-8fcb82ea831a&keywords=&categoryzhu=021002&fbsj=&dqfb=&xxlx=&jylx=',

                    ]
        self.url = self.url_list.pop(0)
        self.headers = {
            'Cookie': 'homeid=1a444a31-e460-47ff-9931-1c075c0f3cd8',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        }

    def parse(self):
        date = tool.date
        # date = '2020-04-02'
        page = 0
        while True:
            page += 1
            text = tool.requests_get(self.url.format(page), self.headers)
            print('*' * 20, page, '*' * 20)
            detail = json.loads(json.loads(text)['custom'])['Table']
            for li in detail:
                title = li['title']
                url = 'http://www.hlbeggzyjy.org.cn' + li['href']
                date_Today = li['date'].replace('[', '').replace(']', '').replace('\r',
                                                                                                     '').replace(
                    '\n', '').replace('\t', '').replace(' ', '')
                code = li['infoid']
                if '招标文件' in title or '澄清补疑' in title or '测试' in title:
                    continue
                # print(title, url, date_Today)
                # time.sleep(666)
                if tool.Transformation(date) <= tool.Transformation(date_Today):
                    if tool.removal(title, date):
                        self.parse_detile(title, url, date, code)
                    else:
                        print('【existence】', url)
                        continue
                else:
                    print('日期不符, 正在切换类型', date_Today, self.url)
                    self.url = self.url_list.pop(0)
                    page = 0
                    break
            if page == 20:
                self.url = self.url_list.pop(0)
                break

    def parse_detile(self, title, url, date, code):
        print(url)
        t = tool.requests_get(url, self.headers)
        url_html = etree.HTML(t)
        detail = url_html.xpath('//*[@id="hideDeil"]')[0]
        detail_html = etree.tostring(detail, method='HTML')
        detail_html = html.unescape(detail_html.decode()).replace('display:none;', '')
        detail_text = url_html.xpath('string(//*[@id="hideDeil"])').replace('\xa0',
                                                                              '').replace(
            '\n', ''). \
            replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
        if '请查看附件中文件详细内容！' in detail_html:
            return
        # print(detail_html.replace('\xa0','').replace('\xa5','').replace('\u2022', ''))
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
        item['address'] = tool.get_address(detail_text)
        item['linkman'] = tool.get_linkman(detail_text)
        item['function'] = tool.get_function(detail_text)
        item['resource'] = '呼伦贝尔市公共资源网'
        item['shi'] = 3007
        item['sheng'] = 3000
        item['removal']= title
        process_item(item)
    def get_nativeplace(self, addr):
        city = ''
        city_list = [['3007.001', '海拉尔区'], ['3007.01', '牙克石'], ['3007.011', '扎兰屯'], ['3007.012', '额尔古纳'], ['3007.013', '根河'], ['3007.002', '阿荣旗'], ['3007.003', '莫力达瓦达斡尔族自治旗'], ['3007.004', '鄂伦春自治旗'], ['3007.005', '鄂温克族自治旗'], ['3007.006', '陈巴尔虎旗'], ['3007.007', '新巴尔虎左旗'], ['3007.008', '新巴尔虎右旗'], ['3007.009', '满洲里']]

        for i in city_list:
            if i[1] in addr:
                city = float(i[0])
                break
        if city == '':
            city = 3007
        return city

if __name__ == '__main__':
    import os,traceback
    try:
        jl = wenshan_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
        tool.send_error('报错文件：'+str(os.path.basename(__file__))+'报错信息：'+str(e))



