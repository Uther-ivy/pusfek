# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item


# 益阳市公共资源交易平台
class yiyang_ggzy:
    def __init__(self):
        self.url_list = [
            # 市本级
            #   工程建设
            'http://jyzx.yiyang.gov.cn/ggzyjy/31065/31081/31109/{}',
            'http://jyzx.yiyang.gov.cn/ggzyjy/31065/31081/31110/{}',
            'http://jyzx.yiyang.gov.cn/ggzyjy/31065/31081/31111/{}',
            'http://jyzx.yiyang.gov.cn/ggzyjy/31065/31081/31112/{}',
            #   政府采购
            'http://jyzx.yiyang.gov.cn/ggzyjy/31065/31082/31113/31132/{}',
            'http://jyzx.yiyang.gov.cn/ggzyjy/31065/31082/31113/31133/{}',
            'http://jyzx.yiyang.gov.cn/ggzyjy/31065/31082/31113/31134/{}',
            'http://jyzx.yiyang.gov.cn/ggzyjy/31065/31082/31113/31135/{}',
        ]
        self.url = self.url_list.pop(0)
        self.headers = {
            'Cookie': 'userGuid=-254005787; oauthClientId=54652760-49c6-47f9-ae7a-83e5693cdaf3; oauthPath=http://jyyw.changde.gov.cn/TPFrame; oauthLoginUrl=http://jyyw.changde.gov.cn/TPFrame/rest/oauth2/authorize?client_id=54652760-49c6-47f9-ae7a-83e5693cdaf3&state=a&response_type=code&scope=user&redirect_uri=; oauthLogoutUrl=http://jyyw.changde.gov.cn/TPFrame/rest/oauth2/logout?redirect_uri=; noOauthRefreshToken=0e68bbd2754ae85b634637df6e5cdf19; noOauthAccessToken=46d04a7103255628c9ca1cd27b95c712',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        }

    def parse(self):
        date = tool.date
        # date = '2020-04-08'
        page = 0
        while True:
            page += 1
            if page == 1:
                text = tool.requests_get_bm(self.url.format('index.htm'), self.headers)
            else:
                text = tool.requests_get_bm(self.url.format('index_' + str(page - 1) + '.htm'), self.headers)
            print('*' * 20, page, '*' * 20)
            html = HTML(text)
            # print(11, text)
            # time.sleep(6666)
            detail = html.xpath('//*[@class="tllb_rg_con"]/ul')
            for i in detail:
                for li in i.xpath('./li'):
                    title = li.xpath('./a/@title')[0]
                    url = self.url.format(li.xpath('./a/@href')[0])
                    date_Today = li.xpath('./span/text()')[0]
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
        print(url)
        url_html = etree.HTML(tool.requests_get_bm(url, self.headers))
        try:
            detail = url_html.xpath('//*[@class="ewb-info-bd"]/div')[0]
            detail_html = etree.tostring(detail, method='HTML')
            detail_html = html.unescape(detail_html.decode())
            detail_text = url_html.xpath('string(//*[@class="ewb-info-bd"]/div)').replace('\xa0', '').replace(
                '\n', ''). \
                replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
        except:
            detail = url_html.xpath('//*[@id="zoom"]')[0]
            detail_html = etree.tostring(detail, method='HTML')
            detail_html = html.unescape(detail_html.decode())
            detail_text = url_html.xpath('string(//*[@id="zoom"])').replace('\xa0', '').replace(
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
        try:
            t = re.findall('<div class="kbsj" id="showtime">.*?</div>', item["body"], re.S)[0]
            item["body"] = item["body"].replace(t, '')
        except:
            pass
        try:
            e = re.findall('<!--二维码-->.*?<!--二维码 /-->', item["body"], re.S)[0]
            item["body"] = item["body"].replace(e, '')
        except:
            pass
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
        item['resource'] = '益阳市公共资源交易网'
        item['shi'] = 9509
        item['sheng'] = 9500
        item['removal'] = title
        process_item(item)

    def get_nativeplace(self, addr):
        city = ''
        city_list = [['9509.001', '资阳区'], ['9509.002', '赫山区'], ['9509.003', '南县'], ['9509.004', '桃江县'],
                     ['9509.005', '安化县'], ['9509.006', '沅江市']]
        for i in city_list:
            if i[1] in addr:
                city = float(i[0])
                break
        if city == '':
            city = 9509
        return city


if __name__ == '__main__':
    import traceback, os

    try:
        jl = yiyang_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
        tool.send_error('报错文件：' + str(os.path.basename(__file__)) + '报错信息：' + str(e))
