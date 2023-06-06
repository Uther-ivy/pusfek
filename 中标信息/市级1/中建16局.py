# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 中铁十六局集团有限公司
class baoshan_ggzy:
    def __init__(self):
        self.url_list = [
            # 'http://cr16g.crcc.cn/module/web/jpage/dataproxy.jsp?startrecord=1&endrecord=45&perpage=15&col=1&appid=1&webid=16&path=%2F&columnid=4529&sourceContentType=1&unitid=37458&webname=%E4%B8%AD%E9%93%81%E5%8D%81%E5%85%AD%E5%B1%80%E9%9B%86%E5%9B%A2%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8&permissiontype=0',
            # 'http://cr16g.crcc.cn/module/web/jpage/dataproxy.jsp?startrecord=1&endrecord=45&perpage=15&col=1&appid=1&webid=16&path=%2F&columnid=4527&sourceContentType=1&unitid=37458&webname=%E4%B8%AD%E9%93%81%E5%8D%81%E5%85%AD%E5%B1%80%E9%9B%86%E5%9B%A2%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8&permissiontype=0',
            # 'http://cr16g.crcc.cn/module/web/jpage/dataproxy.jsp?startrecord=1&endrecord=45&perpage=15&col=1&appid=1&webid=16&path=%2F&columnid=4530&sourceContentType=1&unitid=37458&webname=%E4%B8%AD%E9%93%81%E5%8D%81%E5%85%AD%E5%B1%80%E9%9B%86%E5%9B%A2%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8&permissiontype=0'
              'http://cr16g.crcc.cn/module/web/jpage/dataproxy.jsp?startrecord={}&endrecord={}&perpage=15col=1&appid=1&webid=16&path=%2F&columnid=4529&sourceContentType=1&unitid=37458&webname=%E4%B8%AD%E9%93%81%E5%8D%81%E5%85%AD%E5%B1%80%E9%9B%86%E5%9B%A2%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8&permissiontype=0'
        ]
        self.url = self.url_list.pop(0)
        self.headers = {
            # 'Cookie': 'homeid=1a444a31-e460-47ff-9931-1c075c0f3cd8',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        }

    def parse(self):
        date = tool.date
        page=0
        start=1
        stop=45
        while True:
            page+=1
            print('*'*30,page,'*'*30)
            # date='2021-07-26'
            url=self.url.format(start, stop)
            print(url)
            text = tool.requests_get(url,self.headers)
            url_list=re.findall(f'href="(.*?)"\s*title',text)
            title_list=re.findall(f'title="(.*?)"\s*>',text)
            date_list=re.findall(f'<span>(.*?)</span>',text)
            start+=45
            stop+=45
            # print(de)
            for url,title,date_Today in zip(url_list,title_list,date_list):
                try:
                    url="http://cr16g.crcc.cn"+url
                    if '发布' in date_Today:
                        continue
                    if '测试' in title:
                        continue
                    if tool.Transformation(date) <= tool.Transformation(date_Today):
                        # pass
                        # if tool.removal(title, date):
                        self.parse_detile(title, url, date_Today)
                    # else:
                    #     print('【existence】', url)
                    #     continue
                    else:
                        print('日期不符, 正在切换类型', date_Today, self.url)
                        return

                except Exception as e:
                    traceback.print_exc()

    def parse_detile(self, title, url, date):
        t = tool.requests_get(url, self.headers)
        url_html = etree.HTML(t)
        detail = url_html.xpath('//div[@class="wzy_content"]')[0]
        # print(detail)
        detail_html = etree.tostring(detail, method='HTML')
        detail_html = html.unescape(detail_html.decode())
        detail_text = url_html.xpath('string(//div[@class="wzy_content"])').replace('\xa0', '').replace('\n', ''). \
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
        item['resource'] = '中铁十六局集团有限公司'
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


