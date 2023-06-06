# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 浠水县公共资源交易网
class xinyang_ggzy:
    def __init__(self):
        self.url_list = [
            'http://www.xsggzy.org.cn/TPFront/jyxx/002002/002002001/MoreInfo.aspx?CategoryNum=002002001',
            'http://www.xsggzy.org.cn/TPFront/jyxx/002002/002002004/MoreInfo.aspx?CategoryNum=002002004'
        ]
        self.url = self.url_list.pop(0)
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
            'Cookie': 'ASP.NET_SessionId=dccrutdaruzetk3vikswh54o; __CSRFCOOKIE=7c0eb713-f7a5-4847-a01d-09b82f34d0aa'
        }

    def parse(self):
        date = tool.date
        # date = '2021-07-27'
        page = 0
        data = {
            '__CSRFTOKEN': '',
            '__VIEWSTATE': '',
            '__VIEWSTATEGENERATOR': '99CE51A5',
            '__EVENTTARGET': 'MoreInfoList1$Pager',
            '__EVENTARGUMENT': '2',
            '__VIEWSTATEENCRYPTED': '',
            'MoreInfoList1$Pager_input': '1'
        }
        while True:
            page += 1
            if page == 1:
                text = tool.requests_get_bm(self.url, self.headers)
            else:
                text = tool.requests_post(self.url, data, self.headers)
            html = HTML(text)
            # print(text)
            # time.sleep(6666)
            data['__CSRFTOKEN'] = html.xpath('//*[@id="__CSRFTOKEN"]/@value')[0]
            data['__VIEWSTATE'] = html.xpath('//*[@id="__VIEWSTATE"]/@value')[0]
            data['__VIEWSTATEGENERATOR'] = html.xpath('//*[@id="__VIEWSTATEGENERATOR"]/@value')[0]
            data['__EVENTARGUMENT'] = page+1
            data['MoreInfoList1$Pager_input'] = page
            # print(11, data)
            # time.sleep(666)
            detail = html.xpath('//*[@id="MoreInfoList1_DataGrid1"]/tr')
            print('*' * 20, page, '*' * 20)
            for li in detail:
                title = li.xpath('./td[2]/a/@title')[0]
                url = 'http://www.xsggzy.org.cn' + li.xpath('./td[2]/a/@href')[0]
                date_Today = li.xpath('./td[3]/text()')[0].replace('\n', '').replace('\r', '').replace('\t', '').replace(' ', '')
                # print(title, url, date_Today)
                # time.sleep(666)
                if '测试' in title:
                    continue
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
        detail = url_html.xpath('//*[@id="TDContent"]')[0]
        detail_html = etree.tostring(detail, method='HTML')
        detail_html = html.unescape(detail_html.decode()).replace('\xa0', '').replace('\ufeff', '')
        detail_text = url_html.xpath('string(//*[@id="TDContent"])') \
            .replace('\xa0', '').replace('\n', '').replace('\r', '').replace('\t', '') \
            .replace(' ', '').replace('\xa5', '').replace('\ufeff', '')
        # print(detail_text)
        # time.sleep(6666)
        item = {}
        item['title'] = title.replace('\u2022', '')
        item['url'] = url
        item['date'] = date
        item['typeid'] = tool.get_typeid(item['title'])
        item['senddate'] = int(time.time())
        item['mid'] = 867
        item['infotype'] = tool.get_infotype(item['title'])
        item['body'] = tool.qudiao_width(detail_html)
        # print(item['body'])
        # time.sleep(666)
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
        item['nativeplace'] = 9010.006
        item['linkman'] = tool.get_linkman(detail_text)
        item['function'] = tool.get_function(detail_text)
        item['resource'] = '浠水县公共资源交易网'
        item["shi"] = 9010
        item['sheng'] = 9000
        item['removal']= title
        process_item(item)
        # print(item['body'])

    def get_nativeplace_to(self, city):
        a = ''
        ls = [['11501', '万州区'], ['11502', '涪陵区'], ['11503', '渝中区'], ['11504', '大渡口区'], ['11505', '江北区'], ['11506', '沙坪坝区'], ['11507', '九龙坡区'], ['11508', '南岸区'], ['11509', '北碚区'], ['11510', '万盛区'], ['11511', '双桥区'], ['11512', '渝北区'], ['11513', '巴南区'], ['11514', '黔江区'], ['11515', '长寿区'], ['11516', '綦江县'], ['11517', '潼南县'], ['11518', '铜梁县'], ['11519', '大足县'], ['11520', '荣昌县'], ['11521', '璧山县'], ['11522', '梁平县'], ['11523', '城口县'], ['11524', '丰都县'], ['11525', '垫江县'], ['11526', '武隆县'], ['11527', '忠县'], ['11528', '开县'], ['11529', '云阳县'], ['11530', '奉节县'], ['11531', '巫山县'], ['11532', '巫溪县'], ['11533', '石柱土家族自治县'], ['11534', '秀山土家族苗族自治县'], ['11535', '酉阳土家族苗族自治县'], ['11536', '彭水苗族土家族自治县'], ['11537', '江津'], ['11538', '合川'], ['11539', '永川'], ['11540', '南川']]
        for i in ls:
            if i[1] in city:
                a = i[0]
                break
        if a == '':
            return 11500
        else:
            return a

if __name__ == '__main__':

    import traceback, os
    try:
        jl = xinyang_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
        tool.send_error('报错文件：'+str(os.path.basename(__file__))+'报错信息：'+str(e))


