# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 成都市公共资源交易网
class baoshan_ggzy:
    def __init__(self):
        self.url_list = [
            'https://www.cdggzy.com/site/JSGC/List.aspx',
            'https://www.cdggzy.com/site/Notice/ZFCG/NoticeVersionOneList.aspx'
                         ]
        self.url = self.url_list.pop(0)
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36',
        }

    def parse(self):
        date = tool.date
        # date = '2020-12-04'
        page = 0
        data = {}
        while True:
            page += 1
            if page == 1:
                text = tool.requests_get(self.url, self.headers)
            else:
                text = tool.requests_post(self.url, data, self.headers)
            # if page == 1:
            #     print(text)
            #     print(json.dumps(data))
            #     time.sleep(2222)
            print('*' * 20, page, '*' * 20)
            html = HTML(text)
            data['ctl00$ScriptManager1'] = 'ctl00$ContentPlaceHolder1$UpdatePanel1|ctl00$ContentPlaceHolder1$Pager'
            data['__EVENTTARGET'] = 'ctl00$ContentPlaceHolder1$Pager'
            data['__EVENTARGUMENT'] = page+1
            try:
                data['__VIEWSTATE'] = html.xpath('//*[@id="__VIEWSTATE"]/@value')[0]
            except:
                data['__VIEWSTATE'] = '/' + re.findall('wEPDw.*?__EVENTTARGET', text, re.S)[0]\
                    .replace('|0|hiddenField|__EVENTTARGET', '').replace('|8|hiddenField|__VIEWSTATEGENERATOR|9F052A18', '')
            data['__VIEWSTATEGENERATOR'] = '9F052A18'
            try:
                data['__EVENTVALIDATION'] = html.xpath('//*[@id="__EVENTVALIDATION"]/@value')[0]
            except:
                data['__EVENTVALIDATION'] = re.findall('__EVENTVALIDATION.*?asyncPostBackControlIDs', text, re.S)[0]\
                    .replace('__EVENTVALIDATION|', '').replace('|0|asyncPostBackControlIDs', '')
            data['ctl00$ContentPlaceHolder1$displaytypeval'] = '0'
            data['ctl00$ContentPlaceHolder1$displaystateval'] = '0'
            data['ctl00$ContentPlaceHolder1$dealaddressval'] = '0'
            data['ctl00$ContentPlaceHolder1$keyword'] = ''
            data['__ASYNCPOST'] = 'true'
            # print(11, text)
            # time.sleep(6666)
            detail = html.xpath('//*[@id="contentlist"]/div')
            for li in detail:
                title = li.xpath('./div[2]/a/text()')[0].replace('\n', '').replace('\r', '')\
                    .replace('\t', '').replace(' ', '').replace('<spanstyle="color:red">', '').replace('</span>', '')
                url = li.xpath('./div[2]/a/@href')[0]
                if 'http' not in url:
                    if 'ZFCG' not in self.url:
                        url = 'https://www.cdggzy.com' + url
                    else:
                        url = 'https://www.cdggzy.com/site/Notice/ZFCG/' + url
                date_Today = li.xpath('./div[3]/div[1]/text()')[0].replace('\n', '').replace('\r', '') \
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
                    self.url = self.url_list.pop(0)
                    page = 0
                    break
            if page == 20:
                self.url = self.url_list.pop(0)
                break

    def parse_detile(self, title, url, date):
        print(url)
        t = tool.requests_get(url, self.headers)
        if '暂无内容' in t:
            return
        url_html = etree.HTML(t)
        try:
            detail = url_html.xpath('//*[@id="noticecontent"]/table')[0]
            detail_html = etree.tostring(detail, method='HTML')
            detail_html = html.unescape(detail_html.decode())
            detail_text = url_html.xpath('string(//*[@id="noticecontent"]/table)').replace('\xa0', '').replace('\n',
                                                                                                              ''). \
                replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
            if len(detail_html) < 300:
                return
        except:
            try:
                detail = url_html.xpath('//*[@id="content_tab"]')[0]
                detail_html = etree.tostring(detail, method='HTML')
                detail_html = html.unescape(detail_html.decode())
                detail_text = url_html.xpath('string(//*[@id="content_tab"])').replace('\xa0', '').replace('\n',
                                                                                                                   ''). \
                    replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
                if len(detail_html) < 300:
                    return
            except:
                try:
                    detail = url_html.xpath('//*[@id="noticecontent"]')[0]
                    detail_html = etree.tostring(detail, method='HTML')
                    detail_html = html.unescape(detail_html.decode())
                    detail_text = url_html.xpath('string(//*[@id="noticecontent"])').replace('\xa0', '').replace('\n',
                                                                                                               ''). \
                        replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
                    if len(detail_html) < 300:
                        return
                except:
                    try:
                        detail = url_html.xpath('//*[@id="table1"]')[0]
                        detail_html = etree.tostring(detail, method='HTML')
                        detail_html = html.unescape(detail_html.decode())
                        detail_text = url_html.xpath('string(//*[@id="table1"])').replace('\xa0', '').replace('\n',
                                                                                                                     ''). \
                            replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
                        if len(detail_html) < 300:
                            return
                    except:
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
        item['address'] = tool.get_address(detail_text)
        item['linkman'] = tool.get_linkman(detail_text)
        item['function'] = tool.get_function(detail_text)
        item['resource'] = '成都市公共资源交易网'
        item['shi'] = 12001
        item['sheng'] = 12000
        item['removal']= title
        process_item(item)

    def get_nativeplace(self, addr):
        city = ''
        city_list = [['12001.001', '锦江区'], ['12001.01', '金堂县'], ['12001.011', '双流县'], ['12001.012', '郫县'], ['12001.013', '大邑县'], ['12001.014', '蒲江县'], ['12001.015', '新津县'], ['12001.016', '都江堰市'], ['12001.017', '彭州市'], ['12001.018', '邛崃市'], ['12001.019', '崇州市'], ['12001.002', '青羊区'], ['12001.003', '金牛区'], ['12001.004', '武侯区'], ['12001.005', '成华区'], ['12001.006', '龙泉驿区'], ['12001.007', '青白江区'], ['12001.008', '新都区'], ['12001.009', '温江区']]

        for i in city_list:
            if i[1] in addr:
                city = float(i[0])
                break
        if city == '':
            city = 12001
        return city

if __name__ == '__main__':
    import traceback, os
    try:
        jl = baoshan_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
        tool.send_error('报错文件：'+str(os.path.basename(__file__))+'报错信息：'+str(e))


