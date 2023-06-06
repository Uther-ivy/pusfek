# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 厦门市公共资源交易中心
class wenshan_ggzy:
    def __init__(self):
        self.url_list = [
            'http://120.41.36.88:7100/prod-api/api/trade/project/quaInqueryAnnList',
            'http://117.25.161.110/prod-api/api/trade/project/qaList',
            'http://117.25.161.110/prod-api/api/trade/project/winResultList',
            ]
        self.url = self.url_list.pop(0)
        self.headers = {
            'Accept': '*/*',
            'Content-Type': 'application/json;charset=UTF-8',
            # 'Cookie': 'JSESSIONID=662863FD2199FBD1672A04A290868047; _CSRFCOOKIE=73F3D7A1BCDCA9001D7B1483A214C4E98DE2528B; EPTOKEN=73F3D7A1BCDCA9001D7B1483A214C4E98DE2528B; oauthClientId=demoClient; oauthPath=http://172.16.5.21:8080/EpointWebBuilder; oauthLoginUrl=http://172.16.5.21:8080/EpointWebBuilder/rest/oauth2/authorize?client_id=demoClient&state=a&response_type=code&scope=user&redirect_uri=; oauthLogoutUrl=http://172.16.5.21:8080/EpointWebBuilder/rest/oauth2/logout?redirect_uri=; noOauthRefreshToken=986d4fe7e5dd29b64c9e7b7a6d66e089; noOauthAccessToken=77c09e0bf98b6220b544961097eed84a; sub_domain_cokie=TiG5CMD9KQ41mmsARPTuAg%3D%3D; region_name=%E4%B9%8C%E9%B2%81%E6%9C%A8%E9%BD%90%E5%B8%82',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',

        }

    def parse(self):
        date = tool.date
        # date = '2020-09-22'
        page = 0
        while True:
            page += 1
            data = {'pageNum': page, 'pageSize': 10, 'isXmStrack': "", 'dataType': "", 'showRange': "", 'proName': ""}
            resp = tool.requests_post_to(url=self.url, data=data, headers=self.headers)
            print('*' * 20, page, '*' * 20)
            # print(11, text)
            # time.sleep(6666)
            html=json.loads(resp)
            detail = html['data']
            for li in detail:
                title = li['tenderProjectName']
                pcodeTprojectUniqueId = li['pcodeTprojectUniqueId']
                url =f'http://www.xmzyjy.cn/data/static/master/zyjy/tradeproject/projectinfo_{pcodeTprojectUniqueId}.json'
                date_Today = li['noticeSendTime'].replace('\xa0', '').replace('\n', '').\
                    replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
                # print(title, url, date_Today)
                # time.sleep(666)
                if tool.Transformation(date) <= tool.Transformation(date_Today):
                    if tool.removal(title, date):
                        self.parse_detile(title, url, date, pcodeTprojectUniqueId)
                    else:
                        print('【existence】', url)
                        continue
                else:
                    print('日期不符, 正在切换类型', date_Today, self.url)
                    return


    def parse_detile(self, title, url, date,pcodeTprojectUniqueId ):
        print(url)
        url_to = f'http://www.xmzyjy.cn/data/static/master/zyjy/tradeproject/projectinfo_{pcodeTprojectUniqueId}.json'
        t = 'http://120.41.36.88:7294/' + json.loads(tool.requests_get(url_to, self.headers))['data'][0]['detailFileObjList'][0]['fileUrl']
        print(t)
        # print(t)
        # time.sleep(2222)
        detail_html = '<embed src="{}" width="800" height="600" ></embed>'.format(t)
        item = {}
        item['title'] = title.replace('\u2022', '')
        item['url'] = url
        item['date'] = date
        item['typeid'] = tool.get_typeid(item['title'])
        item['senddate'] = int(time.time())
        item['mid'] = 867
        item['nativeplace'] = self.get_nativeplace(item['title'])
        item['infotype'] = tool.get_infotype(item['title'])
        item['body'] = detail_html
        item['endtime'] = 0
        item['tel'] = ''
        item['email'] = ''
        item['address'] = ''
        item['linkman'] = ''
        item['function'] = ''
        item['resource'] = '厦门市公共资源交易中心'
        item['shi'] = 7002
        item['sheng'] = 7000
        item['removal']= title
        # print(item)
        # process_item(item)

    def get_nativeplace(self, addr):
        city = ''
        city_list = [['7002.001', '思明区'], ['7002.002', '海沧区'], ['7002.003', '湖里区'], ['7002.004', '集美区'],
                     ['7002.005', '同安区'],
                     ['7002.006', '翔安区']]
        for i in city_list:
            if i[1] in addr:
                city = float(i[0])
                break
        if city == '':
            city = 7002
        return city

if __name__ == '__main__':
    import traceback,os
    try:
        jl = wenshan_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
        tool.send_error('报错文件：'+str(os.path.basename(__file__))+'报错信息：'+str(e))


