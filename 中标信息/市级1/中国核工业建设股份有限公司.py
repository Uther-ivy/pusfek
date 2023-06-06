# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item


# 中国核工业建设股份有限公司
class baoshan_ggzy:
    def __init__(self):
        self.url_list = [
            # 'https://gys.cnecc.com/portal/list.do?chnlcode=tender',
            # 'https://gys.cnecc.com/portal/list.do?chnlcode=n_tender', 打不开
            'https://gys.cnecc.com/portal/list.do?chnlcode=result',

        ]
        self.url = self.url_list.pop(0)
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            # 'Cookie': '__jsluid_s=75a9551d0d4fb851b32df394002dbcc2; UM_distinctid=1809c5d63991e0-0574aaba66736f-977173c-1fa400-1809c5d639a64d; __jsluid_h=dcc53e1c3e6585c98ac1a380d4cbc673; JSESSIONID=89B2CB33FE2A0A61BCE7BFCFFBD474F2; Hm_lvt_08b83e0a890d50d974cce624ab6ea6a4=1651890846,1653277444; Hm_lpvt_08b83e0a890d50d974cce624ab6ea6a4=1653277625',
            'Host': 'gys.cnecc.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        }

    def parse(self):
        page=1
        date = tool.date
        while True:
            page+=1# date='2021-04-14'
            print('*' * 20, page, '*' * 20)
            data={
                'chnlcode': 'result',
                'kw': '',
              'chnlvo.pagestr': page
            }
            text = tool.requests_post_param(self.url, self.headers,param=data)
            # print(text)
            html = HTML(text)
            detail = html.xpath('//*[@class="listUl"]/li')
            for li in detail:
                try:
                    url = 'https://gys.cnecc.com/' + li.xpath('./span[1]/a/@href')[0]
                    title = li.xpath('./span[1]/a/@title')[0]
                    date_Today = li.xpath('./span[3]/script/text()')[0].split("write('")[1][:10]
                except:
                    continue
                if '发布' in date_Today:
                    continue
                if '测试' in title:
                    continue
                print(title, url, date_Today)
                # time.sleep(666)
                if tool.Transformation(date) <= tool.Transformation(date_Today):
                        self.parse_detile(title, url, date_Today)
                else:
                    print('日期不符, 正在切换类型', date_Today, self.url)
                    return


    def parse_detile(self, title, url, date):
        print(url)
        t = tool.requests_get(url, self.headers)
        url_html = etree.HTML(t)
        try:
            detail = url_html.xpath('//div[@id="div_content"]')[0]
            detail_html = etree.tostring(detail, method='HTML')
            detail_html = html.unescape(detail_html.decode())
            detail_text = url_html.xpath('string(//div[@id="div_content"])').replace('\xa0', '').replace('\n', ''). \
                replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
        except:
            try:
                detail = url_html.xpath('/html/body/div[3]/div/div[2]/div')[0]
                detail_html = etree.tostring(detail, method='HTML')
                detail_html = html.unescape(detail_html.decode())
                d = re.findall('<div class="time">.*?</div>', detail_html, re.S)
                if len(d) != 0:
                    detail_html = detail_html.replace(d[0], '')
                detail_text = url_html.xpath('string(/html/body/div[3]/div/div[2]/div)').replace('\xa0', '').replace(
                    '\n', ''). \
                    replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
            except:
                try:
                    detail = url_html.xpath('/html/body/div[3]/div[2]/div/div/table')[0]
                    detail_html = etree.tostring(detail, method='HTML')
                    detail_html = html.unescape(detail_html.decode())
                    d = re.findall('<div class="time">.*?</div>', detail_html, re.S)
                    if len(d) != 0:
                        detail_html = detail_html.replace(d[0], '')
                    detail_text = url_html.xpath('string(/html/body/div[3]/div[2]/div/div/table)').replace('\xa0',
                                                                                                           '').replace(
                        '\n', ''). \
                        replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
                except:
                    try:
                        detail = url_html.xpath('//*[@class="WordSection1"]')[0]
                        detail_html = etree.tostring(detail, method='HTML')
                        detail_html = html.unescape(detail_html.decode())
                        d = re.findall('<div class="time">.*?</div>', detail_html, re.S)
                        if len(d) != 0:
                            detail_html = detail_html.replace(d[0], '')
                        detail_text = url_html.xpath('string(//*[@class="WordSection1"])').replace('\xa0',
                                                                                                               '').replace(
                            '\n', ''). \
                            replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
                    except:
                        return
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
        if item['endtime'] == '':
            item['endtime'] = int(time.mktime(time.strptime(date, "%Y-%m-%d")))
        else:
            try:
                item['endtime'] = int(time.mktime(time.strptime(item['endtime'], "%Y-%m-%d")))
            except:
                item['endtime'] = int(time.mktime(time.strptime(date, "%Y-%m-%d")))
        item['nativeplace'] = tool.get_title_city(item['title'])
        if item['nativeplace'] == 0:
            item['nativeplace'] = tool.more(item['title']+detail_text)
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
        item['resource'] = '中国核工业建设股份有限公司'
        if '.' in str(item["nativeplace"]):
            item["shi"] = int(float(str(item["nativeplace"]).replace("['", "").split('.')[0]))
        else:
            item["shi"] = int(float(item["nativeplace"]))
        if len(str(int(item["shi"]))) == 4:
            item['sheng'] = int(str(item["shi"])[:2] + '00')
        elif len(str(int(item["shi"]))) == 5:
            item['sheng'] = int(str(item["shi"])[:3] + '00')
        else:
            item['sheng'] = 0
        # print(item)
        item['removal'] = title
        process_item(item)


if __name__ == '__main__':
    import traceback, os
    try:
        jl = baoshan_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
