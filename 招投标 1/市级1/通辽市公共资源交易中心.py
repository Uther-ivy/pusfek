# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 通辽市公共资源交易中心
class wenshan_ggzy:
    def __init__(self):
        self.url_list = [
            'http://ggzy.tongliao.gov.cn/EpointWebBuilder_tlsggzy/jyxxInfoAction.action?cmd=getInfolist&fbdate=10&jyfrom=&xxtype=010&jytype=&title=&pageSize=12&pageIndex={}',        #工程建设
            'http://ggzy.tongliao.gov.cn/EpointWebBuilder_tlsggzy/jyxxInfoAction.action?cmd=getInfolist&fbdate=10&jyfrom=&xxtype=011&jytype=&title=&pageSize=12&pageIndex={}']       #政府采购

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
            text = tool.requests_get(self.url.format(page), self.headers)
            page += 1
            print('*' * 20, page, '*' * 20)
            detail = json.loads(json.loads(text)['custom'])['Table']['JyxxInfoList']
            # print(11, text)
            # time.sleep(6666)
            for li in detail:
                title = li['realtitle']
                url = 'http://ggzy.tongliao.gov.cn' + li['infourl']
                date_Today = li['infodate'].replace('[', '').replace(']', '').replace('\r',
                                                                                                     '').replace(
                    '\n', '').replace('\t', '').replace(' ', '')
                if '附件' in title:
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
        url_html = etree.HTML(tool.requests_get(url, self.headers))
        detail = url_html.xpath('//*[@class="ewb-article-info"]')[0]
        detail_html = etree.tostring(detail, method='HTML')
        detail_html = html.unescape(detail_html.decode())
        detail_text = url_html.xpath('string(//*[@class="ewb-article-info"])').replace('\xa0', '').replace('\n', '').\
            replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
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
        item['resource'] = '通辽市公共资源交易中心'
        item['shi'] = 3005
        item['sheng'] = 3000
        item['removal']= title
        process_item(item)
    def get_nativeplace(self, addr):
        city = ''
        city_list = [['3005.001', '科尔沁区'], ['3005.002', '科尔沁左翼中旗'], ['3005.003', '科尔沁左翼后旗'], ['3005.004', '开鲁县'], ['3005.005', '库伦旗'], ['3005.006', '奈曼旗'], ['3005.007', '扎鲁特旗'], ['3005.008', '霍林郭勒']]

        for i in city_list:
            if i[1] in addr:
                city = float(i[0])
                break
        if city == '':
            city = 3005
        return city

if __name__ == '__main__':
    import traceback, os
    try:
        jl = wenshan_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
        tool.send_error('报错文件：'+str(os.path.basename(__file__))+'报错信息：'+str(e))



