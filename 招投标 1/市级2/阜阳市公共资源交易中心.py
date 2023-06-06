# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 阜阳市公共资源交易中心
class wenshan_ggzy:
    def __init__(self):
        self.domain_name = 'http://jyzx.fy.gov.cn'
        self.url_list = [
            ["Z1", "ZC_PURCHASE_BULLETIN"], # 采购公告
            ["Z1", "ZC_WINBIDBULLETINFO"], #中保结果公示
            ["Z1", "ZC_CHANGEBULLETIN"], # 更正公告
            ["Z1", "ZC_SINGLE_SOURCE"],  # 单一来源

            ["Z2", "ZC_PURCHASE_BULLETIN"],
            ["Z2", "ZC_WINBIDBULLETINFO"],
            ["Z2", "ZC_CHANGEBULLETIN"],

            ["G1", "GC_NOTICE"], # 招标公告
            ["G1", "GC_CHANGEBULLETIN"], # 更正公告
            ["G1", "GC_BIDCANDIDATE_POST"], # 中标候选人
            ["G1", "GC_BIDPUBLICITY"], #中标结果公示

            ["G2", "GC_NOTICE"],
            ["G2", "GC_CHANGEBULLETIN"],
            ["G2", "GC_BIDCANDIDATE_POST"],
            ["G2", "GC_BIDPUBLICITY"],

            ["G3", "GC_NOTICE"],
            ["G3", "GC_CHANGEBULLETIN"],
            ["G3", "GC_BIDCANDIDATE_POST"],
            ["G3", "GC_BIDPUBLICITY"],

            ["G4", "GC_NOTICE"],
            ["G4", "GC_CHANGEBULLETIN"],
            ["G4", "GC_BIDCANDIDATE_POST"],
            ["G4", "GC_BIDPUBLICITY"],
        ]
        self.url = self.url_list.pop(0)
        self.headers = {
            'Accept': 'application/json, text/plain, */*',
            'Content-Type': 'application/json;charset=UTF-8',
            'Cookie': 'JSESSIONID=662863FD2199FBD1672A04A290868047; _CSRFCOOKIE=73F3D7A1BCDCA9001D7B1483A214C4E98DE2528B; EPTOKEN=73F3D7A1BCDCA9001D7B1483A214C4E98DE2528B; oauthClientId=demoClient; oauthPath=http://172.16.5.21:8080/EpointWebBuilder; oauthLoginUrl=http://172.16.5.21:8080/EpointWebBuilder/rest/oauth2/authorize?client_id=demoClient&state=a&response_type=code&scope=user&redirect_uri=; oauthLogoutUrl=http://172.16.5.21:8080/EpointWebBuilder/rest/oauth2/logout?redirect_uri=; noOauthRefreshToken=986d4fe7e5dd29b64c9e7b7a6d66e089; noOauthAccessToken=77c09e0bf98b6220b544961097eed84a; sub_domain_cokie=TiG5CMD9KQ41mmsARPTuAg%3D%3D; region_name=%E4%B9%8C%E9%B2%81%E6%9C%A8%E9%BD%90%E5%B8%82',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',

        }

    def parse(self):
        date = tool.date
        # date = '2021-12-17'
        page = 0
        url_ = 'https://jyzx.fy.gov.cn/fyggfwpt-api-home-web/menhuJyxx/list'
        data = {"pageNo":1,"pageSize":10,"tableName":"ZC_PURCHASE_BULLETIN","projectType":"Z1","publishTimeStart":"","areaCode":"","title":""}
        while True:
            page += 1
            data['pageNo'] = page
            data['tableName'] = self.url[1]
            data['projectType'] = self.url[0]
            text = tool.requests_post_to(url_, data, self.headers)
            print('*' * 20, page, '*' * 20)
            detail = json.loads(text)['data']['list']
            for li in detail:
                title = li['title'].replace('\xa0', '').replace('\n', ''). \
                    replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '').replace("<fontstyle='color:red'>(网)</font>", '')
                if 'Z' in li['projectType']:
                    if li['tableName'] == 'ZC_PURCHASE_BULLETIN':
                        code = '&nav=政府采购&nav=采购公告&isNewSp=' + li['flag']
                    elif li['tableName'] == 'ZC_WINBIDBULLETINFO':
                        code = '&nav=政府采购&nav=中标结果公示&isNewSp=' + li['flag']
                    elif li['tableName'] == 'ZC_CHANGEBULLETIN':
                        code = '&nav=政府采购&nav=更正公告&isNewSp=' + li['flag']
                    else:
                        code = '&nav=政府采购&nav=单一来源&isNewSp=' + li['flag']
                else:
                    if li['tableName'] == 'GC_NOTICE':
                        code = '&nav=工程建设&nav=招标公告&isNewSp=' + li['flag']
                    elif li['tableName'] == 'GC_CHANGEBULLETIN':
                        code = '&nav=工程建设&nav=更正公告&isNewSp=' + li['flag']
                    elif li['tableName'] == 'GC_BIDCANDIDATE_POST':
                        code = '&nav=工程建设&nav=中标候选人公示&isNewSp=' + li['flag']
                    else:
                        code = '&nav=工程建设&nav=中标结果公示&isNewSp=' + li['flag']
                url = 'http://jyzx.fy.gov.cn/#/newTradeDetail?guid=' + li['guid']+code
                date_Today = li['publishTime'][:10].replace('\xa0', '').replace('\n', ''). \
                    replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '') \
                    .replace('[', '').replace(']', '').replace('/', '-')
                if 'http' not in url:
                    url = self.domain_name + url
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
        xq_url = 'http://jyzx.fy.gov.cn/fyggfwpt-api-home-web/menhuJyxx/detail?_t=1624343886&guid=' + url.replace('http://jyzx.fy.gov.cn/#/newTradeDetail?guid=', '').split('&nav=')[0]
        while True:
            try:
                t = tool.requests_get(xq_url, self.headers).replace('\xa9', '').replace('<br>&nbsp;&nbsp;', '')
                detail_html = json.loads(t)['data']['content']
                break
            except:
                print('详情内容获取失败')
                time.sleep(2)
                continue
        if detail_html is None:
            try:
                detail_html = json.loads(t)['dataList']['bg'][0]['gonggaocontent']
            except:
                try:
                    detail_html = json.loads(t)['dataList']['bg'][0]['noticecontent']
                except:
                    try:
                        detail_html = json.loads(t)['dataList']['zbjg'][0]['winbidbulletincontent']
                    except:
                        try:
                            detail_html = json.loads(t)['dataList']['lb'][0]['exceptioncontent']
                        except:
                            try:
                                detail_html = json.loads(t)['dataList'][0]['biddercontent']
                            except:
                                try:
                                    detail_html = json.loads(t)['dataList']['zbjg_bg'][0]['winbidbulletincontent']
                                except:
                                    try:
                                        detail_html = json.loads(t)['dataList']['zbjg'][0]['publicitycontent']
                                    except:
                                        return

        detail_text = ''.join(re.findall('>(.*?)<', detail_html, re.S)).replace('\xa0', '').replace('\n',
                                                                                                             ''). \
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
        item['resource'] = '阜阳市公共资源交易中心'
        item['shi'] = 6511
        item['sheng'] = 6500
        item['removal']= title
        process_item(item)

    def get_nativeplace(self, addr):
        city = ''
        city_list = [['6511.001', '颍州区'], ['6511.002', '颍东区'], ['6511.003', '颍泉区'], ['6511.004', '临泉县'], ['6511.005', '太和县'], ['6511.006', '阜南县'], ['6511.007', '颍上县'], ['6511.008', '界首']]

        for i in city_list:
            if i[1] in addr:
                city = float(i[0])
                break
        if city == '':
            city = 6511
        return city

if __name__ == '__main__':
    import os,traceback
    try:
        jl = wenshan_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
        tool.send_error('报错文件：'+str(os.path.basename(__file__))+'报错信息：'+str(e))



