# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 中国电信阳光采购
class baoshan_ggzy:
    def __init__(self):
        self.url_list = [
            # 'https://caigou.chinatelecom.com.cn/MSS-PORTAL/prequalfication/listForAd.do',
            'https://caigou.chinatelecom.com.cn/MSS-PORTAL/resultannounc/listForAd.do',
            # 'https://caigou.chinatelecom.com.cn/MSS-PORTAL/announcementjoin/list.do?provinceJT=',
        ]
        self.url = self.url_list.pop(0)
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Host': 'caigou.chinatelecom.com.cn',
            'Origin': 'https://caigou.chinatelecom.com.cn',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Referer': 'https://caigou.chinatelecom.com.cn/MSS-PORTAL/resultannounc/listForAd.do',
            'Cookie': 'name=value; JSESSIONID=0000mjC_dGLtWNh79ZT7HAs_JTJ:18djc0j4k; CaiGouServiceInfo=!/nkKjdWZl/2is8KU9I+YAUGJNqjObGZU18zt9QbTWNcNBBlAYRlGPK7MBQ1NHtg7OTLxNqsZGa7JzJM=',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        }

    def parse(self):
        date = tool.date
        page = 1900
        while True:
            page += 1
            print('-'*50, page)
            if 'prequalfication' in self.url:
                data = 'provinceCodeNew=&prequalficationName=&prequalficationCode=&creatorTimeStart=&creatorTimeEnd=&provinceCode=&provinceNames=&pn=01&pn=03&pn=11&pn=22&pn=16&pn=18&pn=09&pn=10&pn=08&pn=06&pn=05&pn=04&pn=23&pn=31&pn=17&pn=19&pn=15&pn=14&pn=02&pn=13&pn=20&pn=21&pn=27&pn=28&pn=30&pn=29&pn=24&pn=26&pn=25&pn=07&pn=12&pn=54&pn=34&pn=EA&pn=EB&pn=EC&pn=ED&pn=EE&pn=EF&pn=EG&pn=EH&pn=EI&pn=EJ&pn=EK&pn=EL&pn=EM&pn=EN&pn=EO&pn=EP&pn=EQ&pn=ER&pn=ES&pn=ET&pn=EU&pn=EV&pn=EW&pn=EX&pn=EY&pn=EZ&pn=RA&pn=RB&pn=RC&pn=RD&pn=RE&pn=RG&pn=RH&pn=32&pn=CA&pn=CB&pn=CC&pn=CD&pn=CE&pn=CF&pn=CG&pn=CH&pn=CI&pn=CJ&pn=CK&pn=CL&pn=CM&pn=RP&pn=CO&pn=CP&pn=CR&pn=CS&pn=CT&pn=CU&pn=CV&pn=CW&pn=CX&pn=CY&pn=CZ&pn=RI&pn=RJ&pn=RK&pn=RL&pn=RM&pn=RN&pn=60&pn=33&pn=DA&pn=DB&pn=DC&pn=DD&pn=DE&pn=DF&pn=DG&pn=DH&pn=66&pn=53&pn=FA&pn=65&pn=67&pn=FB&pn=FC&pn=FD&pn=FF&pn=FE&pn=42&pn=62&pn=FG&pn=61&pn=68&pn=69&pn=70&pn=72&pn=73&pn=71&pn=78&pn=74&pn=75&pn=76&pn=79&pn=VX&pn=HJ&paging.start={}&paging.pageSize=10&pageNum=10&goPageNum={}&paging.start={}&paging.pageSize=10&pageNum=10&goPageNum={}'
            elif 'resultannounc' in self.url:
                data ='provinceJT=&resultAnnounceName=&startDate=&endDate=&paging.start={}&paging.pageSize=10&pageNum=10&goPageNum={}&paging.start={}&paging.pageSize=10&pageNum=10&goPageNum={}'
            else:
                data = 'provinceJT=&docTitle=&docCode=&provinceCode=&provinceNames=&pn=01&pn=03&pn=11&pn=22&pn=16&pn=18&pn=09&pn=10&pn=08&pn=06&pn=05&pn=04&pn=23&pn=31&pn=17&pn=19&pn=15&pn=14&pn=02&pn=13&pn=20&pn=21&pn=27&pn=28&pn=30&pn=29&pn=24&pn=26&pn=25&pn=07&pn=12&pn=54&pn=34&pn=EA&pn=EB&pn=EC&pn=ED&pn=EE&pn=EF&pn=EG&pn=EH&pn=EI&pn=EJ&pn=EK&pn=EL&pn=EM&pn=EN&pn=EO&pn=EP&pn=EQ&pn=ER&pn=ES&pn=ET&pn=EU&pn=EV&pn=EW&pn=EX&pn=EY&pn=EZ&pn=RA&pn=RB&pn=RC&pn=RD&pn=RE&pn=RG&pn=RH&pn=32&pn=CA&pn=CB&pn=CC&pn=CD&pn=CE&pn=CF&pn=CG&pn=CH&pn=CI&pn=CJ&pn=CK&pn=CL&pn=CM&pn=RP&pn=CO&pn=CP&pn=CR&pn=CS&pn=CT&pn=CU&pn=CV&pn=CW&pn=CX&pn=CY&pn=CZ&pn=RI&pn=RJ&pn=RK&pn=RL&pn=RM&pn=RN&pn=60&pn=33&pn=DA&pn=DB&pn=DC&pn=DD&pn=DE&pn=DF&pn=DG&pn=DH&pn=66&pn=53&pn=FA&pn=65&pn=67&pn=FB&pn=FC&pn=FD&pn=FF&pn=FE&pn=42&pn=62&pn=FG&pn=61&pn=68&pn=69&pn=70&pn=72&pn=73&pn=71&pn=78&pn=74&pn=75&pn=76&pn=79&pn=VX&pn=HJ&startDate=&endDate=&docType=&paging.start={}&paging.pageSize=10&pageNum=10&goPageNum={}&paging.start={}&paging.pageSize=10&pageNum=10&goPageNum={}'
            if page == 1:
                text = tool.requests_get(self.url, self.headers)
            else:
                text = tool.requests_post(self.url, data.format((page-1)*10+1,page-1,(page-2)*10+1,page-1), self.headers)
            html = HTML(text)
            detail = html.xpath('//*[@class="table_data"]/tr')
            for li in detail:
                try:
                    if 'prequalfication' in self.url:
                        try:
                            urls = li.xpath('./td[4]/a/@onclick')[0]
                        except:
                            continue
                        urls_ = re.findall("view\('(.*?)','(.*?)'\);", urls)
                        title = li.xpath('./td[4]/a/text()')[0]
                        date_Today = li.xpath('./td[9]/text()')[0][:10]
                        url = f'https://caigou.chinatelecom.com.cn/MSS-PORTAL/prequalfication/viewForAd.do?id={urls_[0][0]}&encryCode={urls_[0][1]}'
                    elif 'resultannounc' in self.url:
                        try:
                            urls = li.xpath('./td[3]/a/@onclick')[0]
                        except:
                            continue
                        urls_ = re.findall("view\('(.*?)','(.*?)','(.*?)'\)", urls)
                        title = li.xpath('./td[3]/a/text()')[0]
                        date_Today = li.xpath('./td[4]/text()')[0][:10]
                        url = f'https://caigou.chinatelecom.com.cn/MSS-PORTAL/resultannounc/viewHome.do?id={urls_[0][0]}&encryCode={urls_[0][1]}&noticeType={urls_[0][2]}'
                    else:
                        try:
                            urls = li.xpath('./td[3]/a/@onclick')[0]
                        except:
                            continue
                        urls_ = re.findall("view\('(.*?)','(.*?)','(.*?)'\)", urls)
                        title = li.xpath('./td[3]/a/text()')[0]
                        date_Today = li.xpath('./td[6]/text()')[0][:10]
                        url = f'https://caigou.chinatelecom.com.cn/MSS-PORTAL/purchaseannouncebasic/viewHome.do?encryCode={urls_[0][2]}&noticeType=0&id={urls_[0][0]}'
                    if '发布' in date_Today:
                        continue
                    if '测试' in title:
                        continue
                    # print(title, url, date_Today)
                    # time.sleep(666)
                    if tool.Transformation(date) <= tool.Transformation(date_Today):
                            self.parse_detile(title, url, date_Today)
                    else:
                        print('日期不符, 正在切换类型', date_Today, self.url)
                        return
                except Exception:
                    traceback.print_exc()

    def parse_detile(self, title, url, date):
        print(url)
        t = tool.requests_get(url, self.headers)
        url_html = etree.HTML(t)
        try:
            detail = url_html.xpath('//*[@class="universal_two_content"]')[0]
        except:
            return
        # print(detail)
        detail_html = etree.tostring(detail, method='HTML')
        detail_html = html.unescape(detail_html.decode())
        detail_text = url_html.xpath('string(//*[@class="universal_two_content"])').replace('\xa0', '').replace('\n', ''). \
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
        item['resource'] = '中国电信阳光采购'
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
