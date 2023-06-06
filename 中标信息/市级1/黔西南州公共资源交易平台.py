# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 黔西南州公共资源交易平台
class qianxinan_ggzy:
    def __init__(self):
        self.url_list = [
            #       中标公示
            'https://ggzy.guizhou.gov.cn/tradeInfo/es/list'
        ]
        self.url = self.url_list.pop(0)
        self.headers = {
            'Content-Type': 'application/json;charset=UTF-8',
            'Referer': 'https://ggzy.guizhou.gov.cn/xxfw/gcjs/?gs=%E4%BA%A4%E6%98%93%E7%BB%93%E6%9E%9C%E5%85%AC%E7%A4%BA',
            # 'Cookie': 'ASP.NET_SessionId=sgciv2y0q2cmcycy1o5nsnep; _gscu_381646434=86586121w36f2x70; _gscbrs_381646434=1; _gscs_381646434=t86591829gen3ym70|pv:8',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest'
        }

    def parse(self):
        date = tool.date
        # date = '2020-04-10'
        page = 0
        while True:
            page += 1
            data={"channelId":"5904475","pageNum":page,"pageSize":20,"announcement":"交易结果公示","isPage":'true'}
            text = tool.requests_post_param(self.url, self.headers,data=json.dumps(data))
            print('*' * 20, page, '*' * 20)
            print(11, text)
            # time.sleep(6666)
            detail = json.loads(text)['list']
            for li in detail:
                try:
                    title = li.get('docTitle')
                    cid = li.get('id')
                    url = li.get('apiUrl')
                    showurl=f'https://ggzy.guizhou.gov.cn/tradeInfo/detailHtml?metaId={cid}'
                    date_Today = li.get('docRelTime')
                    if '测试' in title:
                        continue
                    # print(title, url, date_Today)
                    # time.sleep(666)
                    if tool.Transformation(date) <= date_Today:
                        # if tool.removal(title, date):
                            self.parse_detile(title, url, date_Today,showurl)
                        # else:
                        #     print('【existence】', url)
                        #     continue
                    else:
                        print('日期不符, 正在切换类型', date_Today)
                        self.url = self.url_list.pop(0)
                        return
                except Exception as e:
                    traceback.print_exc()
    def parse_detile(self, title, url, date,showurl):
        print(url)
        url_html = etree.HTML(tool.requests_get(url, self.headers))
        detail = url_html.xpath('//*[@id="Zoom"]')[0]
        detail_html = etree.tostring(detail, method='HTML')
        detail_html = html.unescape(detail_html.decode())
        detail_text = url_html.xpath('string(//*[@id="Zoom"])').replace('\xa0', '').replace(
            '\n', ''). \
            replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
        # print(detail_text.replace('\xa0','').replace('\xa5',''))
        # time.sleep(6666)
        if len(detail_text) < 100:
            return ''
        item = {}
        item['title'] = title.replace('\u2022', '')
        item['url'] = showurl
        item['date'] = date/1000
        item['typeid'] = tool.get_typeid(item['title'])
        item['senddate'] = int(time.time())
        item['mid'] = 867
        item['nativeplace'] = self.get_nativeplace(item['title'])
        item['infotype'] = tool.get_infotype(item['title'])
        item['body'] = tool.qudiao_width(detail_html)
        item['endtime'] = tool.get_endtime(detail_text)
        if item['endtime'] == '':
            item['endtime'] = date/1000#int(time.mktime(time.strptime(date, "%Y-%m-%d")))
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
        item['resource'] = '黔西南州公共资源交易网'
        item['shi'] = 12506
        item['sheng'] = 12500
        item['removal']= title
        process_item(item)

    def get_nativeplace(self, addr):
        city = ''
        city_list = [['12506.001', '兴义市'], ['12506.002', '兴仁县'], ['12506.003', '普安县'], ['12506.004', '晴隆县'], ['12506.005', '贞丰县'], ['12506.006', '望谟县'], ['12506.007', '册亨县'], ['12506.008', '安龙县']]
        for i in city_list:
            if i[1] in addr:
                city = float(i[0])
                break
        if city == '':
            city = 12506
        return city

if __name__ == '__main__':

    import traceback, os
    try:
        jl = qianxinan_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
        tool.send_error('报错文件：'+str(os.path.basename(__file__))+'报错信息：'+str(e))

