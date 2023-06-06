# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 朝阳市公共资源交易信息网
class chaoyang_ggzy:
    def __init__(self):
        self.code = '0'
        self.url_code = [
            # 建设工程
            'http://218.60.2.98/EpointWebBuilder/rest/frontAppCustomAction/getPageInfoListNew?' \
            'params= {"siteGuid":"abd5e1e1-ba0a-46d2-8af8-34b45279d94b","categoryNum":"003001","kw":"","pageIndex":%s,"pageSize":16}',
            # 政府采购
            'http://218.60.2.98/EpointWebBuilder/rest/frontAppCustomAction/getPageInfoListNew?' \
              'params= {"siteGuid":"abd5e1e1-ba0a-46d2-8af8-34b45279d94b","categoryNum":"003002","kw":"","pageIndex":%s,"pageSize":16}'
        ]
        self.url = self.url_code.pop(0)
        self.headers = {
            'Cookie': 'JSESSIONID=AE65016F3197EE42172066ECE3DD53E1; userGuid=-254005787; oauthClientId=demoClient; oauthPath=http://172.16.121.236:8080/EpointWebBuilder; oauthLoginUrl=http://172.16.121.236:8080/EpointWebBuilder/rest/oauth2/authorize?client_id=demoClient&state=a&response_type=code&scope=user&redirect_uri=; oauthLogoutUrl=http://172.16.121.236:8080/EpointWebBuilder/rest/oauth2/logout?redirect_uri=; noOauthRefreshToken=3d3b4b23b11ab74969eb304fcc6dbf17; noOauthAccessToken=0a8c2376efc7353efa85e1ad2420c40f; Secure',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
            'Accept': 'application/json, text/javascript, */*; q=0.01'
        }

    def parse(self):
        date = tool.date
        # date = '2020-01-17'
        page = 0
        while True:
            page += 1
            self.code = str(page-1)
            data = {}
            text = tool.requests_post_to(self.url % self.code, data, self.headers)
            print('*' * 20, page, '*' * 20)
            detail = json.loads(text)['custom']['infodata']
            for li in detail:
                title = li['title'].replace("<font color='#0066FF'>", '').replace("</font>", '')
                if 'http' in li['infourl']:
                    continue
                url = 'http://218.60.2.98' + li['infourl']
                date_Today = li['infodate']
                if tool.Transformation(date) <= tool.Transformation(date_Today):
                    if tool.removal(title, date):
                        self.parse_detile(title, url, date_Today)
                    else:
                        print('【existence】', url)
                        continue
                else:
                    print('日期不符, 正在切换类型...', date_Today)
                    self.url = self.url_code.pop(0)
                    page = 0
                    break
            if page == 20:
                self.url = self.url_code.pop(0)
                page = 0


    def parse_detile(self, title, url, date):
        print(url)
        url_html = etree.HTML(tool.requests_get(url, self.headers))
        try:
            detail = url_html.xpath('/html/body/div[2]/div[2]/div/div[3]')[0]
        except:
            return
        detail_html = etree.tostring(detail, method='HTML')
        detail_html = html.unescape(detail_html.decode())
        detail_text = url_html.xpath('string(/html/body/div[2]/div[2]/div/div[3])').replace('\xa0', '').replace('\n', '').\
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
        item['resource'] = '朝阳市公共资源交易信息网'
        item['shi'] = 3513
        item['sheng'] = 3500
        item['removal']= title
        process_item(item)

    def get_nativeplace(self, addr):
        city = ''
        city_list = [['3513.001', '双塔区'], ['3513.002', '龙城区'], ['3513.003', '朝阳县'], ['3513.004', '建平县'],
                     ['3513.005', '喀喇沁左翼蒙古族自治县'], ['3513.006', '北票市'], ['3513.007', '凌源市']]
        for i in city_list:
            if i[1] in addr:
                city = float(i[0])
                break
        if city == '':
            city = 3513
        return city

if __name__ == '__main__':
    import traceback, os
    try:
        jl = chaoyang_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
        tool.send_error('报错文件：'+str(os.path.basename(__file__))+'报错信息：'+str(e))


