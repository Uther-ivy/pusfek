# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 鄂州市公共资源交易平台
class ezhou_ggzy:
    def __init__(self):
        self.url_list = [
            # 市本级
            #   工程建设
            #       招标公告
            'http://www.ezggzy.cn/jiaoyixinxi/queryJiaoYiXinXiPagination.do?bianHao=&gongChengLeiBie=&gongChengType=&gongShiType=10&page={}&rows=15&title=&type=10',
            #       评标结果
            'http://www.ezggzy.cn/jiaoyixinxi/queryJiaoYiXinXiPagination.do?bianHao=&gongChengLeiBie=&gongChengType=&gongShiType=180&page={}&rows=15&title=&type=10',
            #       中标结果
            'http://www.ezggzy.cn/jiaoyixinxi/queryJiaoYiXinXiPagination.do?bianHao=&gongChengLeiBie=&gongChengType=&gongShiType=50&page={}&rows=15&title=&type=10',
            #       变更公告
            'http://www.ezggzy.cn/jiaoyixinxi/queryJiaoYiXinXiPagination.do?bianHao=&gongChengLeiBie=&gongChengType=&gongShiType=130&page={}&rows=15&title=&type=10',
            #   政府采购
            #       采购公告
            'http://www.ezggzy.cn/jiaoyixinxi/queryJiaoYiXinXiPagination.do?bianHao=&gongChengLeiBie=&gongChengType=&gongShiType=70&page={}&rows=15&title=&type=20',
            #       变更公告
            'http://www.ezggzy.cn/jiaoyixinxi/queryJiaoYiXinXiPagination.do?bianHao=&gongChengLeiBie=&gongChengType=&gongShiType=130&page={}&rows=15&title=&type=20',
        ]
        self.url = self.url_list.pop(0)
        self.headers = {
            'Cookie': 'ASP.NET_SessionId=sgciv2y0q2cmcycy1o5nsnep; _gscu_381646434=86586121w36f2x70; _gscbrs_381646434=1; _gscs_381646434=t86591829gen3ym70|pv:8',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        }

    def parse(self):
        date = tool.date
        # date = '2020-04-10'
        page = 0
        while True:
            page += 1
            text = tool.requests_get(self.url.format(page), self.headers)
            print('*' * 20, page, '*' * 20)
            text = json.loads(text)['rows']
            for li in text:
                title = li['title']
                if li['gongShiTypeText'] == '招标公告':
                    url = 'http://www.ezggzy.cn/jyw/jyw/showGongGao.do?ggGuid=' + li['yuanXiTongId']
                elif li['gongShiTypeText'] == '中标候选人公示':
                    url = 'http://www.ezggzy.cn/jiaoyixingxi/pbjg_view.html?guid=' + li['yuanXiTongId']
                elif li['gongShiTypeText'] == '中标公示':
                    url = 'http://www.ezggzy.cn/jiaoyixingxi/zbgs_view.html?guid=' + li['yuanXiTongId']
                elif li['gongShiTypeText'] == '失败公告':
                    url = 'http://www.ezggzy.cn/jiaoyixingxi/ycxx_view.html?guid=' + li['yuanXiTongId']
                date_Today = li['faBuShortTimeText'].replace('\n', '').replace('\r', '') \
                    .replace('\t', '').replace(' ', '').replace('[', '').replace(']', '')
                code = li['gongShiTypeText']
                if '测试' in title:
                    continue
                # print(title, url, date_Today)
                # time.sleep(666)
                if tool.Transformation(date) <= tool.Transformation(date_Today):
                    if tool.removal(title, date):
                        self.parse_detile(title, url, date, code)
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

    def parse_detile(self, title, url, date, code):
        print(url)
        if code == '招标公告':
            detail_html = json.loads(tool.requests_get(url, self.headers))['html']
            detail_text = ''.join(re.findall('>(.*?)<', detail_html)).replace('\xa0', '').replace(
                '\n', ''). \
                replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
        else:

            url_html = HTML(tool.requests_get(url,self.headers))
            # time.sleep(6666)
            try:
                detail = url_html.xpath('//*[@class="xmmc_bt"]')[0]
                detail_html = etree.tostring(detail, method='HTML')
                detail_html = html.unescape(detail_html.decode())
                detail_text = url_html.xpath('string(//*[@class="xmmc_bt"])').replace('\xa0', '').replace(
                    '\n', ''). \
                    replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
                if len(detail_text) < 100:
                    int('a')
            except:
                detail = url_html.xpath('//*[@id="nr"]/div[1]')[0]
                detail_html = etree.tostring(detail, method='HTML')
                detail_html = html.unescape(detail_html.decode())
                detail_text = url_html.xpath('string(//*[@id="nr"]/div[1])').replace('\xa0', '').replace(
                    '\n', ''). \
                    replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
            if '{{' in detail_html:
                xq_url = 'http://www.ezggzy.cn/jyw/jyw/queryYiChangXXById.do?guid=' + url.split('guid=')[1]
                data = json.loads(tool.requests_get(xq_url, self.headers))
                ycxx = re.findall('\{\{.*?}}', detail_html, re.S)
                print(data)
                for i in ycxx:
                    if 'data' not in i:
                        continue
                    bd = i[2:-2].split('.')
                    print(bd)
                    if len(bd) == 3:
                        if bd[2] == 'yichangleixing':
                            yiChangLeiXing = data[bd[1]]['yiChangLeiXing']
                            if yiChangLeiXing == 1:
                                detail_html = detail_html.replace(i, '招标终止')
                            elif yiChangLeiXing == 2:
                                detail_html = detail_html.replace(i, '重新招标')
                            elif yiChangLeiXing == 9:
                                detail_html = detail_html.replace(i, '变更招标方式')
                            else:
                                detail_html = detail_html.replace(i, '')
                        elif bd[2] == 'gongShiStartDate':
                            detail_html = detail_html.replace(i, tool.Time_stamp_to_date_to(data[bd[1]]['shenPiTime']))
                        elif bd[2] == 'gongShiEndDate':
                            detail_html = detail_html.replace(i, tool.Time_stamp_to_date_to(data[bd[1]]['shenPiTime'] + 3*24*60*60*1000))
                        else:
                            detail_html = detail_html.replace(i, data[bd[1]][bd[2]])
                    elif len(bd) == 4:
                        try:
                            detail_html = detail_html.replace(i, data[bd[1]][bd[2]][bd[3]])
                        except:
                            return
                    elif len(bd) == 5:
                        detail_html = detail_html.replace(i, data[bd[1]][bd[2]][bd[3]][bd[4]])
            # print(detail_text.replace('\xa0','').replace('\xa5',''))
            # time.sleep(6666)
            if len(detail_text) < 100:
                return ''
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
        item['resource'] = '鄂州市公共资源交易网'
        item['shi'] = 9006
        item['sheng'] = 9000
        # print(item)
        item['removal']= title
        process_item(item)

    def get_nativeplace(self, addr):
        city = ''
        city_list = [['9006.001', '梁子湖区'], ['9006.002', '华容区'], ['9006.003', '鄂城区']]
        for i in city_list:
            if i[1] in addr:
                city = float(i[0])
                break
        if city == '':
            city = 9006
        return city

if __name__ == '__main__':
    import traceback, os
    try:
        jl = ezhou_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
