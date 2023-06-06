# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 青海项目信息网
class wenshan_ggzy:
    def __init__(self):
        self.domain_name = 'http://www.qhei.net.cn'
        self.url_list = [
            'http://www.qhei.net.cn/html/zbcg/list_1698.html',
            'http://www.qhei.net.cn/html/zbcg/list_1696.html',
            'http://www.qhei.net.cn/html/zbcg/list_1695.html',
            'http://www.qhei.net.cn/html/zbcg/list_1694.html',
            'http://www.qhei.net.cn/html/zbcg/list_1692.html',
            'http://www.qhei.net.cn/html/zbcg/list_1691.html'
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
        while True:
            page += 1
            text = tool.requests_get(self.url, self.headers)
            html = HTML(text)
            print('*' * 20, page, '*' * 20)
            # print(11, text.replace('\ufffd', ' ').replace('\u30fb', ' '))
            # time.sleep(6666)
            detail = html.xpath('/html/body/div[6]/div[2]/ul/li')
            for li in detail:
                title = li.xpath('./a/@title')[0].replace('\xa0', '').replace('\n', ''). \
                    replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '').replace(
                    "<fontstyle='color:red'>(网)</font>", '')
                url = li.xpath('./a/@href')[0]
                try:
                    date_Today = li.xpath('./font/text()')[0].replace('\xa0', '').replace('\n', ''). \
                        replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '') \
                        .replace('[', '').replace(']', '').replace('/', '-')
                except:
                    date_Today = li.xpath('./text()')[0].replace('\xa0', '').replace('\n', ''). \
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
                    print('日期不符, 正在切换...', date_Today, self.url)
                    self.url = self.url_list.pop(0)
                    page = 0
                    break
            if page==5:
                break



    def parse_detile(self, title, url, date):
        print(url)
        t = tool.requests_get(url, self.headers).replace('\xa9', '').replace('<br>&nbsp;&nbsp;', '')
        # print(t)
        # time.sleep(2222)
        url_html = etree.HTML(t)
        try:
            detail = url_html.xpath('//*[@id="MyContent"]')[0]
        except:
            return
        detail_html = etree.tostring(detail, method='HTML')
        detail_html = html.unescape(detail_html.decode()).replace("display: none", '').replace("\u2022", '').replace('\xa0', '')
        detail_text = url_html.xpath('string(//*[@id="MyContent"])').replace('\xa0', '').replace('\n',
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
        item['winner'] = tool.get_winner(detail_text)
        item['address'] = tool.get_address(detail_text)
        item['linkman'] = tool.get_linkman(detail_text)
        item['function'] = tool.get_function(detail_text)
        item['resource'] = '青海项目信息网'
        item['shi'] = int(item['nativeplace'])
        item['sheng'] = 15000
        item['removal']= title
        process_item(item)

    def get_nativeplace(self, addr):
        city = ''
        city_list = [['15001', '西宁'], ['15001.001', '城东区'], ['15001.002', '城中区'], ['15001.003', '城西区'], ['15001.004', '城北区'], ['15001.005', '大通回族土族自治县'], ['15001.006', '湟中县'], ['15001.007', '湟源县'], ['15002', '海东地区'], ['15002.001', '平安县'], ['15002.002', '民和回族土族自治县'], ['15002.003', '乐都县'], ['15002.004', '互助土族自治县'], ['15002.005', '化隆回族自治县'], ['15002.006', '循化撒拉族自治县'], ['15003', '海北藏族自治州'], ['15003.001', '门源回族自治县'], ['15003.002', '祁连县'], ['15003.003', '海晏县'], ['15003.004', '刚察县'], ['15004', '黄南藏族自治州'], ['15004.001', '同仁县'], ['15004.002', '尖扎县'], ['15004.003', '泽库县'], ['15004.004', '河南蒙古族自治县'], ['15005', '海南藏族自治州'], ['15005.001', '共和县'], ['15005.002', '同德县'], ['15005.003', '贵德县'], ['15005.004', '兴海县'], ['15005.005', '贵南县'], ['15006', '果洛藏族自治州'], ['15006.001', '玛沁县'], ['15006.002', '班玛县'], ['15006.003', '甘德县'], ['15006.004', '达日县'], ['15006.005', '久治县'], ['15006.006', '玛多县'], ['15007', '玉树藏族自治州'], ['15007.001', '玉树县'], ['15007.002', '杂多县'], ['15007.003', '称多县'], ['15007.004', '治多县'], ['15007.005', '囊谦县'], ['15007.006', '曲麻莱县'], ['15008', '海西蒙古族藏族自治州'], ['15008.001', '格尔木'], ['15008.002', '德令哈'], ['15008.003', '乌兰县'], ['15008.004', '都兰县'], ['15008.005', '天峻县']]

        for i in city_list:
            if i[1] in addr:
                city = float(i[0])
                break
        if city == '':
            city = 15000
        return city

if __name__ == '__main__':
    import traceback, os
    try:
        jl = wenshan_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
        tool.send_error('报错文件：'+str(os.path.basename(__file__))+'报错信息：'+str(e))


