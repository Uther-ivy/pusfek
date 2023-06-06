# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 宿州市公共资源交易中心
class wenshan_ggzy:
    def __init__(self):
        self.url_list = [
            'http://ggzyjy.ahsz.gov.cn/XZinteligentsearch/rest/esinteligentsearch/getFullTextDataNew'
        ]
        self.url = self.url_list.pop(0)
        self.headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Cookie': 'userGuid=-254005787; oauthClientId=demoClient; oauthPath=http://127.0.0.1:8080/EpointWebBuilder; oauthLoginUrl=http://127.0.0.1:8080/EpointWebBuilder/rest/oauth2/authorize?client_id=demoClient&state=a&response_type=code&scope=user&redirect_uri=; oauthLogoutUrl=http://127.0.0.1:8080/EpointWebBuilder/rest/oauth2/logout?redirect_uri=; noOauthRefreshToken=9542e0798050e20cbd14253cfbf1d74e; noOauthAccessToken=4bb67e8bc9a14e34d46cd30695c1a07e',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        }

    def parse(self):
        date = tool.date
        # date = '2022-05-20'
        page = 0
        while True:
            data = {"token":"","pn":page,"rn":10,"sdt":"","edt":"","wd":"","inc_wd":"","exc_wd":"","fields":"","cnum":"","sort":"{\"istop\":\"0\",\"ordernum\":\"0\",\"webdate\":\"0\",\"infoid\":\"0\"}","ssort":"title","cl":200,"terminal":"","condition":[{"fieldName":"categorynum","equal":"001","notEqual":None,"equalList":None,"notEqualList":None,"isLike":True,"likeType":2}],"time":None,"highlights":"","statistics":None,"unionCondition":[],"accuracy":"","noParticiple":"0","searchRange":None,"noWd":True,"searchEngine":"1"}
            page += 1
            text = tool.requests_post_to(self.url, data, self.headers)
            print('*' * 20, page, '*' * 20)
            # html = HTML(text)
            # print(11, text)
            # time.sleep(6666)
            detail = json.loads(text)['result']['records']
            for li in detail:
                title = li['title']
                date_Today = li['infodate'][:10]
                url_ = 'http://ggzyjy.ahsz.gov.cn' + li['linkurl']
                # print(title, url_, date_Today)
                # time.sleep(666)
                if tool.Transformation(date) <= tool.Transformation(date_Today):
                    if tool.removal(title, date):
                        self.parse_detile(title, url_, date)
                    else:
                        print('【existence】', url_)
                        continue
                else:
                    print('日期不符, 正在切换类型', date_Today)
                    self.url = self.url_list.pop(0)
                    page = 0

                    break
            if page == 20:
                print('日期不符, 正在切换类型')
                self.url = self.url_list.pop(0)
                break

    def parse_detile(self, title, url, date):
        print(url)
        t = tool.requests_get(url,self.headers)
        url_html = etree.HTML(t)
        detail = url_html.xpath('//*[@class="wrap-cont"]')[0]
        detail_html = etree.tostring(detail, method='HTML')
        detail_html = html.unescape(detail_html.decode())
        detail_text = url_html.xpath('string(//*[@class="wrap-cont"])').replace('\xa0', '').replace('\n', '').\
            replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
        if len(detail_html) < 200:
            int('a')
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
        item['resource'] = '宿州市公共资源交易中心'
        item['shi'] = 6512
        item['sheng'] = 6500
        item['removal']= title
        process_item(item)
    def get_nativeplace(self, addr):
        city = ''
        city_list = [['6512.001', '墉桥区'], ['6512.002', '砀山县'], ['6512.003', '萧县'], ['6512.004', '灵璧县'], ['6512.005', '泗县']]

        for i in city_list:
            if i[1] in addr:
                city = float(i[0])
                break
        if city == '':
            city = 6512
        return city

if __name__ == '__main__':
    import traceback,os
    try:
        jl = wenshan_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
        tool.send_error('报错文件：'+str(os.path.basename(__file__))+'报错信息：'+str(e))


