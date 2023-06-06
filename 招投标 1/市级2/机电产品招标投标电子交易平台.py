# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 机电产品招标投标电子交易平台  出现错误时需重新运行
class baoshan_ggzy:
    def __init__(self):
        self.url_list = [
            'fullText=&pubDate=&infoClassCodes=0105&normIndustry=&zoneCode=&fundSourceCodes=&poClass=&rangeType=&currentPage={}',
            'fullText=&pubDate=&infoClassCodes=0106&normIndustry=&zoneCode=&fundSourceCodes=&poClass=BidChange&rangeType=&currentPage={}',
            'fullText=&pubDate=&infoClassCodes=0107&normIndustry=&zoneCode=&fundSourceCodes=&poClass=BidResult&rangeType=&currentPage={}',
            'fullText=&pubDate=&infoClassCodes=0108&normIndustry=&zoneCode=&fundSourceCodes=&poClass=BidResult&rangeType=&currentPage={}',
        ]
        self.url = self.url_list.pop(0)
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Host': 'www.chinabidding.com',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Cookie': '__yjs_duid=1_dfb7304e913df8d8505d2224f668264b1629249512861; yjs_js_security_passport=b9e80f8a5dc1729be30ba5286942045134580ac0_1641281038_js; JSESSIONID=E9AB4115517AFAB3495DCA1EDDF91892; Hm_lvt_3e8bc71035a13d1213b8be00baf17f95=1641281040; Hm_lpvt_3e8bc71035a13d1213b8be00baf17f95=1641281040',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        }

    def parse(self):
        date = tool.date
        # date = '2021-08-19'
        page = 0
        u = 'https://www.chinabidding.com/search/proj.htm'
        while True:
            page += 1
            if page == 20:
                self.url = self.url_list.pop(0)
                break
                continue
            while True:
                text = tool.requests_post(u, self.url.format(page), self.headers).replace('\u2022', '')
                print('*' * 20, page, '*' * 20)
                html = HTML(text)
                detail = html.xpath('//*[@class="as-pager-body"]/li')
                if len(detail) == 0:
                    print('列表出错')
                    time.sleep(5)
                    continue
                break
            for li in detail:
                title = li.xpath('./a/h5/span[2]/text()')[0].replace('\n', '').replace('\t', '').replace(' ', '').replace('\r', '')
                url = li.xpath('./a/@href')[0]
                url_domain = 'https://www.chinabidding.com'
                if 'http' not in url:
                    if '../../' in url:
                        url = url_domain + url[5:]
                    elif '../' in url:
                        url = url_domain + url[2:]
                    elif './' in url:
                        url = url_domain + url[1:]
                    else:
                        url = url_domain + url
                date_Today = li.xpath('./a/h5/span[3]/text()')[0]\
                    .replace('\n', '').replace('\t', '').replace(' ', '').replace('\r', '')\
                    .replace('[', '').replace(']', '').replace('发布时间：', '')
                try:
                    city = li.xpath('./a/div/dl/dd/span[2]/strong/text()')[0]
                except:
                    city = ''
                if '测试' in title or '物流服务' in title:
                    continue
                # print(title, url, date_Today)
                # time.sleep(666)
                if tool.Transformation(date) <= tool.Transformation(date_Today):
                    if tool.removal(title, date):
                        self.parse_detile(title, url, date, city)
                    else:
                        print('【existence】', url)
                        continue
                else:
                    print('日期不符, 正在切换类型', date_Today, self.url)
                    self.url = self.url_list.pop(0)
                    page = 0
                    break


    def parse_detile(self, title, url, date, city):
        print(url)
        while True:
            t = tool.requests_get(url, self.headers)
            if '网关错误，连接源站失败' in t:
                print('网关错误，连接源站失败')
                time.sleep(5)
                continue
            url_html = etree.HTML(t)
            try:
                detail = url_html.xpath('//div[@class="as-article-body table-article"]')[0]
                detail_html = etree.tostring(detail, method='HTML')
                detail_html = html.unescape(detail_html.decode()).replace('浏览次数：', '').replace('原文链接', '')
                detail_text = url_html.xpath('string(//*[@class="as-article-body table-article"])').replace('\xa0',
                                                                                                            '').replace(
                    '\n', ''). \
                    replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
            except:
                try:
                    detail = url_html.xpath('//*[@id="lab-show"]/div[2]/div[1]/div/div[2]')[0]
                    detail_html = etree.tostring(detail, method='HTML')
                    detail_html = html.unescape(detail_html.decode()).replace('浏览次数：', '').replace('原文链接', '')
                    detail_text = url_html.xpath('string(//*[@id="lab-show"]/div[2]/div[1]/div/div[2])').replace('\xa0',
                                                                                                                 '').replace(
                        '\n', ''). \
                        replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
                except:
                    try:
                        detail = url_html.xpath('//*[@id="myPrintArea"]')[0]
                        detail_html = etree.tostring(detail, method='HTML')
                        detail_html = html.unescape(detail_html.decode()).replace('浏览次数：', '').replace('原文链接', '')
                        detail_text = url_html.xpath('string(//*[@id="myPrintArea"])').replace('\xa0',
                                                                                               '').replace(
                            '\n', ''). \
                            replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
                    except:
                        print('body 出错')
                        time.sleep(5)
                        continue
            break


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
        item['tel'] = tool.get_tel(detail_text)
        item['email'] = ''
        item['address'] = tool.get_address(detail_text)
        item['linkman'] = tool.get_linkman(detail_text)
        item['function'] = tool.get_function(detail_text)
        item['resource'] = '机电产品招标投标电子交易平台'
        item['nativeplace'] = tool.get_title_city(title)
        if item['nativeplace'] == 0:
            item['nativeplace'] = tool.more(item['title']+detail_text)
        item["shi"] = int(str(item["nativeplace"]).split('.')[0])
        if len(str(item["shi"])) == 4:
            item['sheng'] = int(str(item["shi"])[:2] + '00')
        elif len(str(item["shi"])) == 5:
            item['sheng'] = int(str(item["shi"])[:3] + '00')
        else:
            item['sheng'] = 0
        print(city, item['nativeplace'], item['sheng'], item['shi'])
        item['removal']= title
        process_item(item)

if __name__ == '__main__':
    import traceback,os
    try:
        jl = baoshan_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()



