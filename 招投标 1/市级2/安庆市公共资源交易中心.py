# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 安庆市公共资源交易中心
class wenshan_ggzy:
    def __init__(self):
        self.domain_name = 'http://aqggzy.anqing.gov.cn'
        self.url_list = [
            'http://aqggzy.anqing.gov.cn/inteligentsearch/rest/esinteligentsearch/getFullTextDataNew'
        ]
        self.url = self.url_list.pop(0)
        self.headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Host': 'aqggzy.anqing.gov.cn',
            'Referer': 'http://aqggzy.anqing.gov.cn/jyxx/trade_info.html',
            'Cookie': 'UM_distinctid=17c30386d3e17-02b3c22689962f-4343363-1fa400-17c30386d3f525; __jsluid_h=0720c5c31bf25097e17243c9d50856f7; userGuid=1047923792; oauthClientId=00f38d99-ce53-4d5c-b6ae-1f444ab9c369; oauthPath=http://220.179.5.14:90/PSPFrame/; oauthLoginUrl=http://127.0.0.1:1112/membercenter/login.html?redirect_uri=; oauthLogoutUrl=; noOauthRefreshToken=59030d3b1f8f330d13d7d346b72ce9db; noOauthAccessToken=bcb4c3b2a1628941c2f044fc63c29b2f; fontZoomState=0',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',

        }

    def parse(self):
        date = tool.date
        # date = '2020-09-25'
        page = 0
        while True:
            page += 1
            date_code = time.strftime('%Y-%m-%d', time.localtime(time.time() - 86400*30))
            data = {"token":"","pn":(page-1)*8,"rn":8,"sdt":"","edt":"","wd":"%20","inc_wd":"","exc_wd":"","fields":"title","cnum":"002","sort":"{\"webdate\":0}","ssort":"title","cl":200,"terminal":"","condition":[{"fieldName":"categorynum","equal":"003","notEqual":None,"equalList":None,"notEqualList":None,"isLike":True,"likeType":2}],"time":[{"fieldName":"webdate","startTime": date_code+" 00:00:00","endTime":"2999-12-31 23:59:59"}],"highlights":"citycode","statistics":None,"unionCondition":None,"accuracy":"","noParticiple":"1","searchRange":None,"isBusiness":"1"}
            text = tool.requests_post_to(self.url, data, self.headers)
            print('*' * 20, page, '*' * 20)
            # print(11, text.replace('\ufffd', ' ').replace('\u30fb', ' '))
            # time.sleep(6666)
            detail = json.loads(text)['result']['records']
            for li in detail:
                title = li['title'].replace('\xa0', '').replace('\n', ''). \
                    replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
                date_Today = li['infodate'][:10].replace('\xa0', '').replace('\n', ''). \
                    replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '') \
                    .replace('[', '').replace(']', '').replace('/', '-')
                url = 'http://aqggzy.anqing.gov.cn/jyxx/{}/{}/{}/{}.html'\
                    .format(li['categorynum'][:6], li['categorynum'], date_Today.replace('-', ''), li['linkurl'])
                if 'http' not in url:
                    url = self.domain_name + url
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
        tt = tool.requests_get(url, self.headers)
        url_html = etree.HTML(tt)
        try:
            detail = url_html.xpath('//*[@class="l notice-box"]')[0]
            detail_html = etree.tostring(detail, method='HTML')
            detail_html = html.unescape(detail_html.decode())
            detail_text = url_html.xpath('string(//*[@class="l notice-box"])').replace('\xa0', '').replace('\n',
                                                                                              ''). \
                replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
        except:
            detail = url_html.xpath('//*[@class="bid-box clearfix"]')[0]
            detail_html = etree.tostring(detail, method='HTML')
            detail_html = html.unescape(detail_html.decode())
            detail_text = url_html.xpath('string(//*[@class="bid-box clearfix"])').replace('\xa0', '').replace('\n',
                                                                                                           ''). \
                replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')

        if len(detail_html) < 200:
            url = 'http://aqggzy.anqing.gov.cn:7001/aqshop/proProjects/web_announcement.do?type=1&pkProProjectsId=' \
                  + url.split('/')[-1].replace('.html', '')[:-4]
            print('链接更改', url)
            tt = tool.requests_get(url, self.headers)
            url_html = etree.HTML(tt)
            detail = url_html.xpath('//*[@class="AreaR"]')[0]
            detail_html = etree.tostring(detail, method='HTML')
            detail_html = html.unescape(detail_html.decode())
            detail_text = url_html.xpath('string(//*[@class="AreaR"])').replace('\xa0', '').replace('\n',
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
        item['resource'] = '安庆市公共资源交易中心'
        item['shi'] = 6508
        item['sheng'] = 6500
        item['removal']= title
        process_item(item)

    def get_nativeplace(self, addr):
        city = ''
        city_list = [['6508.001', '迎江区'], ['6508.01', '岳西县'], ['6508.011', '桐城'], ['6508.002', '大观区'], ['6508.003', '郊区'], ['6508.004', '怀宁县'], ['6508.005', '枞阳县'], ['6508.006', '潜山县'], ['6508.007', '太湖县'], ['6508.008', '宿松县'], ['6508.009', '望江县']]

        for i in city_list:
            if i[1] in addr:
                city = float(i[0])
                break
        if city == '':
            city = 6508
        return city

if __name__ == '__main__':
    import traceback,os
    try:
        jl = wenshan_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
        tool.send_error('报错文件：'+str(os.path.basename(__file__))+'报错信息：'+str(e))


