# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 淄博市公共资源交易中心
class wenshan_ggzy:
    def __init__(self):
        self.domain_name = 'http://ggzyjy.zibo.gov.cn'
        self.url_list = [
            'http://ggzyjy.zibo.gov.cn/TPFront/jyxx/002001/002001001/002001001001/MoreInfo.aspx?CategoryNum=268698113',
            'http://ggzyjy.zibo.gov.cn/TPFront/jyxx/002001/002001001/002001001002/MoreInfo.aspx?CategoryNum=268698114',
            'http://ggzyjy.zibo.gov.cn/TPFront/jyxx/002001/002001001/002001001013/MoreInfo.aspx?CategoryNum=268698123',
            'http://ggzyjy.zibo.gov.cn/TPFront/jyxx/002001/002001001/002001001009/MoreInfo.aspx?CategoryNum=2001001009',
            'http://ggzyjy.zibo.gov.cn/TPFront/jyxx/002001/002001001/002001001010/MoreInfo.aspx?CategoryNum=268698120',
            'http://ggzyjy.zibo.gov.cn/TPFront/jyxx/002001/002001001/002001001007/MoreInfo.aspx?CategoryNum=268698119',
            'http://ggzyjy.zibo.gov.cn/TPFront/jyxx/002001/002001001/002001001008/MoreInfo.aspx?CategoryNum=2001001008',

            'http://ggzyjy.zibo.gov.cn/TPFront/jyxx/002001/002001002/002001002001/MoreInfo.aspx?CategoryNum=268698625',
            'http://ggzyjy.zibo.gov.cn/TPFront/jyxx/002001/002001002/002001002002/MoreInfo.aspx?CategoryNum=268698626',
            'http://ggzyjy.zibo.gov.cn/TPFront/jyxx/002001/002001002/002001002009/MoreInfo.aspx?CategoryNum=2001002009',
            'http://ggzyjy.zibo.gov.cn/TPFront/jyxx/002001/002001002/002001002010/MoreInfo.aspx?CategoryNum=268698632',
            'http://ggzyjy.zibo.gov.cn/TPFront/jyxx/002001/002001002/002001002007/MoreInfo.aspx?CategoryNum=268698631',

            'http://ggzyjy.zibo.gov.cn/TPFront/jyxx/002002/002002001/002002001001/MoreInfo.aspx?CategoryNum=268960257',
            'http://ggzyjy.zibo.gov.cn/TPFront/jyxx/002002/002002001/002002001002/MoreInfo.aspx?CategoryNum=268960258',
            'http://ggzyjy.zibo.gov.cn/TPFront/jyxx/002002/002002001/002002001011/MoreInfo.aspx?CategoryNum=268960265',
            'http://ggzyjy.zibo.gov.cn/TPFront/jyxx/002002/002002001/002002001007/MoreInfo.aspx?CategoryNum=268960263',
            'http://ggzyjy.zibo.gov.cn/TPFront/jyxx/002002/002002001/002002001012/MoreInfo.aspx?CategoryNum=268960266',
            'http://ggzyjy.zibo.gov.cn/TPFront/jyxx/002002/002002001/002002001009/MoreInfo.aspx?CategoryNum=2002001009',

            'http://ggzyjy.zibo.gov.cn/TPFront/jyxx/002002/002002002/002002002001/MoreInfo.aspx?CategoryNum=268960769',
            'http://ggzyjy.zibo.gov.cn/TPFront/jyxx/002002/002002002/002002002002/MoreInfo.aspx?CategoryNum=268960770',
            'http://ggzyjy.zibo.gov.cn/TPFront/jyxx/002002/002002002/002002002011/MoreInfo.aspx?CategoryNum=268960777',

            'http://ggzyjy.zibo.gov.cn/TPFront/jyxx/002002/002002005/002002005001/MoreInfo.aspx?CategoryNum=268962305'
        ]
        self.url = self.url_list.pop(0)
        self.headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Cookie': 'JSESSIONID=662863FD2199FBD1672A04A290868047; _CSRFCOOKIE=73F3D7A1BCDCA9001D7B1483A214C4E98DE2528B; EPTOKEN=73F3D7A1BCDCA9001D7B1483A214C4E98DE2528B; oauthClientId=demoClient; oauthPath=http://172.16.5.21:8080/EpointWebBuilder; oauthLoginUrl=http://172.16.5.21:8080/EpointWebBuilder/rest/oauth2/authorize?client_id=demoClient&state=a&response_type=code&scope=user&redirect_uri=; oauthLogoutUrl=http://172.16.5.21:8080/EpointWebBuilder/rest/oauth2/logout?redirect_uri=; noOauthRefreshToken=986d4fe7e5dd29b64c9e7b7a6d66e089; noOauthAccessToken=77c09e0bf98b6220b544961097eed84a; sub_domain_cokie=TiG5CMD9KQ41mmsARPTuAg%3D%3D; region_name=%E4%B9%8C%E9%B2%81%E6%9C%A8%E9%BD%90%E5%B8%82',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',

        }

    def parse(self):
        date = tool.date
        # date = '2020-09-27'
        page = 0
        data = {
            # '__CSRFTOKEN': '',
            '__VIEWSTATE': '',
            '__VIEWSTATEGENERATOR': '86E82E3C',
            '__EVENTTARGET': 'MoreInfoList1$Pager',
            '__EVENTARGUMENT': page,
            '__VIEWSTATEENCRYPTED': '',
            'MoreInfoList1$Pager_input': '1'
        }
        while True:
            page += 1
            if page == 1:
                text = tool.requests_get(self.url, self.headers)
            else:
                text = tool.requests_post(self.url, data, self.headers)
            html = HTML(text)
            data['__VIEWSTATE'] = html.xpath('//*[@id="__VIEWSTATE"]/@value')[0]
            # data['__CSRFTOKEN'] = html.xpath('//*[@id="__CSRFTOKEN"]/@value')[0]
            data['__EVENTARGUMENT'] = str(page)
            print('*' * 20, page, '*' * 20)
            # print(11, text.replace('\ufffd', ' ').replace('\u30fb', ' '))
            # time.sleep(6666)
            detail = html.xpath('//*[@id="MoreInfoList1_DataGrid1"]/tr')
            for li in detail:
                title = li.xpath('./td[2]/a/@title')[0].replace('\xa0', '').replace('\n', ''). \
                    replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '').replace("<fontstyle='color:red'>(网)</font>", '')
                url = li.xpath('./td[2]/a/@href')[0]
                date_Today = li.xpath('./td[3]/text()')[0].replace('\xa0', '').replace('\n', ''). \
                    replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '') \
                    .replace('[', '').replace(']', '').replace('/', '-')
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
                    return


    def parse_detile(self, title, url, date):
        print(url)
        t = tool.requests_get(url, self.headers).replace('\xa9', '').replace('<br>&nbsp;&nbsp;', '')
        # print(t)
        # time.sleep(2222)
        url_html = etree.HTML(t)
        detail = url_html.xpath('//*[@id="TDContent"]')[0]
        detail_html = etree.tostring(detail, method='HTML')
        detail_html = html.unescape(detail_html.decode()).replace("display: none", '').replace("\u2022", '').replace('\xa0', '')
        detail_text = url_html.xpath('string(//*[@id="TDContent"])').replace('\xa0', '').replace('\n',
                                                                                                             ''). \
            replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
        if len(detail_html) < 200:
            int('a')
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
        # d = re.findall('''<td align='center' style='border:0;'>.*?</td>''', item['body'], re.S)
        # if len(d) != 0:
        #     item['body'] = item['body'].replace(d[0], '').replace('\xa0', '')
        # d = re.findall('''<td align="center" style="border:0;">.*?</td>''', item['body'], re.S)
        # if len(d) != 0:
        #     item['body'] = item['body'].replace(d[0], '').replace('\xa0', '')
        # print(item['body'])
        # time.sleep(2222)
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
        item['resource'] = '淄博市公共资源交易中心'
        item['shi'] = 8003
        item['sheng'] = 8000
        item['removal']= title
        process_item(item)

    def get_nativeplace(self, addr):
        city = ''
        city_list = [['8003.001', '淄川区'], ['8003.002', '张店区'], ['8003.003', '博山区'], ['8003.004', '临淄区'], ['8003.005', '周村区'], ['8003.006', '桓台县'], ['8003.007', '高青县'], ['8003.008', '沂源县']]

        for i in city_list:
            if i[1] in addr:
                city = float(i[0])
                break
        if city == '':
            city = 8003
        return city

if __name__ == '__main__':
    import os,traceback
    try:
        jl = wenshan_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
        tool.send_error('报错文件：'+str(os.path.basename(__file__))+'报错信息：'+str(e))



