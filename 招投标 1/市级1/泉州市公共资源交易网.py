# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 泉州市公共资源交易中心
class wenshan_ggzy:
    def __init__(self):
        self.url_list = [
            'http://ggzyjy.quanzhou.gov.cn/project/getProjPage_project.do',
            'http://ggzyjy.quanzhou.gov.cn/project/getwinBulletinPage_project.do'#结果
            ]
        self.url = self.url_list.pop(0)
        self.headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
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
            if 'getProjPage_project' in self.url:
                data = {"pageIndex":page,"pageSize":10,"classId":0,"centerId":0,"projNo":"","projName":"","ownerDeptName":""}
            else:
                data = {"pageIndex":page,"pageSize":10,"keyword":"","centerId":0}
            text = tool.requests_post_to(self.url, data, self.headers)
            print('*' * 20, page, '*' * 20)
            # print(11, text)
            # time.sleep(6666)
            detail = json.loads(text)['data']['dataList']
            for li in detail:
                if 'getProjPage_project' in self.url:
                    title = li['projName']
                    url = 'http://ggzyjy.quanzhou.gov.cn/project/projectInfo.do?projId={}'.format(li['projId'])
                    date_Today = li['auditDate'].replace('\xa0', '').replace('\n', ''). \
                        replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
                else:
                    title = li['bltTitle']
                    url = li['linkStr']
                    date_Today = li['pubDate'].replace('\xa0', '').replace('\n', ''). \
                        replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
                code = li['projId']
                # print(title, url, date_Today)
                # time.sleep(666)
                if tool.Transformation(date) <= tool.Transformation(date_Today):
                    if tool.removal(title, date):
                        self.parse_detile(title, url, date, code)
                    else:
                        print('【existence】', url)
                        continue
                else:
                    print('日期不符, 正在切换类型', date_Today)
                    self.url = self.url_list.pop(0)
                    page=0
                    break


            if page == 20:
                print('日期不符, 正在切换类型')
                self.url = self.url_list.pop(0)
                break

    def parse_detile(self, title, url, date, code):
        print(url)
        if 'getProjPage_project' in self.url:
            url_to = 'http://ggzyjy.quanzhou.gov.cn/UiForWeb/project/getProjBulletin_project.do'
            data = {"projId":code,"fileType":"F001"}
        else:
            url_to = 'http://ggzyjy.quanzhou.gov.cn/project/getProjBulletin_project.do'
            data = {"projId": code, "fileType": "F004"}
        t = json.loads(tool.requests_post_to(url_to, data, self.headers))['data'][0]['fileUrl']
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
        # item['body'] = item['body'].replace('''<a href="http://www.hfztb.cn" target="_blank"><img src="../Template/Default/images/wybm.png"></a>''', '')
        # print(item['body'].replace('\xa0', '').replace('\xa5', '').replace('\xb3', ''))
        # time.sleep(6666)
        item['endtime'] = 0
        item['tel'] = ''
        item['email'] = ''
        item['address'] = ''
        item['linkman'] = ''
        item['function'] = ''
        item['resource'] = '泉州市公共资源交易中心'
        item['shi'] = 7005
        item['sheng'] = 7000
        item['removal']= title
        process_item(item)

    def get_nativeplace(self, addr):
        city = ''
        city_list = [['7005.001','鲤城区'],['7005.01','石狮市'],['7005.011','晋江市'],['7005.012','南安市'],['7005.002','丰泽区'],
    ['7005.003','洛江区'],['7005.004','泉港区'],['7005.005','惠安县'],['7005.006','安溪县'],['7005.007','永春县'],['7005.008','德化县'],
                     ['7005.009','金门县']]
        for i in city_list:
            if i[1] in addr:
                city = float(i[0])
                break
        if city == '':
            city = 7005
        return city

if __name__ == '__main__':
    import traceback,os
    try:
        jl = wenshan_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
        tool.send_error('报错文件：'+str(os.path.basename(__file__))+'报错信息：'+str(e))


