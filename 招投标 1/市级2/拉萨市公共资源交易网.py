# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 拉萨市公共资源交易网
class lasa_ggzy:
    def __init__(self):
        self.url_list = [
            'http://ggzy.lasa.gov.cn/pub/jyxx/list-content?keyName=&term=3&areaCode=&menuCode=JYGCJS&typeCode=ZBGG&startTime=&endTime=&pageNo={}',
            'http://ggzy.lasa.gov.cn/pub/jyxx/list-content?keyName=&term=3&areaCode=&menuCode=JYGCJS&typeCode=PBJG&startTime=&endTime=&pageNo={}',
            'http://ggzy.lasa.gov.cn/pub/jyxx/list-content?keyName=&term=3&areaCode=&menuCode=JYGCJS&typeCode=TBTZ&startTime=&endTime=&pageNo={}',
            'http://ggzy.lasa.gov.cn/pub/jyxx/list-content?keyName=&term=3&areaCode=&menuCode=JYZFCG&typeCode=CGGG&startTime=&endTime=&pageNo={}',
            'http://ggzy.lasa.gov.cn/pub/jyxx/list-content?keyName=&term=3&areaCode=&menuCode=JYZFCG&typeCode=GZGG&startTime=&endTime=&pageNo={}',
            'http://ggzy.lasa.gov.cn/pub/jyxx/list-content?keyName=&term=3&areaCode=&menuCode=JYZFCG&typeCode=JGGG&startTime=&endTime=&typeCode=ZZGG&pageNo={}',
        ]
        self.url = self.url_list.pop(0)
        self.headers = {
            'Cookie': 'Hm_lvt_776eb6c6b51e3da5075c361337f94338=1584946762,1586936167; TS0161614b=01761419df1159ee5d0dc3cd6f5029798f9f5622ce83a1a6b58545a766632b4b2c2ba8a9c608459776a8aa67978b0cd44c6b44f253; Hm_lpvt_776eb6c6b51e3da5075c361337f94338=1586936490',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        }

    def parse(self):
        date = tool.date
        # date = '2021-07-27'
        page = 0
        while True:
            text = tool.requests_get(self.url.format(page), self.headers)
            page += 1
            print('*' * 20, page, '*' * 20)
            # print(11, text)
            # time.sleep(6666)
            detail = HTML(text).xpath('//*[@class="list-ul"]/li')
            for li in detail:
                title = li.xpath('./a/text()')[0]
                date_Today = li.xpath('./span/text()')[0]
                url = 'http://ggzy.lasa.gov.cn' + li.xpath('./a/@href')[0]
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
                    print('日期不符, 正在切换类型', date_Today)
                    self.url = self.url_list.pop(0)
                    page = 0
                    break
            if page == 20:
                self.url = self.url_list.pop(0)
                break
    def parse_detile(self, title, url, date):
        headers={
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            # 'Cookie': 'JSESSIONID=D7CBF44EAF74732929367005A592B99F',
            'Host': 'ggzy.lasa.gov.cn',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36 Edg/88.0.705.81',
        }
        # print(url)
        t = tool.requests_get(url,self.headers)
        projNO=re.findall("var projNO ='(.*?)';",t)[0]
        menuCode=re.findall("var menuCode ='(.*?)';",t)[0]
        typeCode=re.findall("var typeCode ='(.*?)';",t)[0]
        projContentId=re.findall("var projContentId = '(.*?)';",t)[0]
        url_1=f'http://ggzy.lasa.gov.cn/pub/indexContent_one?projNO={projNO}&projType={menuCode}&projTypeCode={typeCode}&projContentId={projContentId}'
        print(url_1)
        t=tool.requests_get(url_1,headers)
        url_html = etree.HTML(t)
        detail = url_html.xpath('//*[@id="content"]')[0]
        detail_html = etree.tostring(detail, method='HTML')
        detail_html = html.unescape(detail_html.decode())
        detail_text = url_html.xpath('string(//*[@id="content"])').replace('\xa0', '').replace(
            '\n', ''). \
            replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
        # print(detail_text.replace('\xa0','').replace('\xa5',''))
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
        item['resource'] = '拉萨市公共资源交易网'
        item['shi'] = 13501
        item['sheng'] = 13500
        # print(item)
        item['removal']= title
        process_item(item)

    def get_nativeplace(self, addr):
        city = ''
        city_list = [['13501.001', '城关区'], ['13501.002', '林周县'], ['13501.003', '当雄县'], ['13501.004', '尼木县'], ['13501.005', '曲水县'], ['13501.006', '堆龙德庆县'], ['13501.007', '达孜县'], ['13501.008', '墨竹工卡县']]
        for i in city_list:
            if i[1] in addr:
                city = float(i[0])
                break
        if city == '':
            city = 13501
        return city

if __name__ == '__main__':

    import traceback, os
    try:
        jl = lasa_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
        tool.send_error('报错文件：'+str(os.path.basename(__file__))+'报错信息：'+str(e))



