# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 云阳县公共资源交易中心
class wenshan_ggzy:
    def __init__(self):
        self.domain_name = 'http://www.yunyang.gov.cn'
        self.url_list = [
            'https://www.cqggzy.com/interface/rest/esinteligentsearch/getFullTextDataNew'
        ]
        self.url = self.url_list.pop(0)
        self.headers = {
'Accept': 'application/json, text/javascript, */*; q=0.01',
'Accept-Encoding': 'gzip, deflate, br',
'Accept-Language': 'zh-CN,zh;q=0.9',
# 'Cache-Control': 'max-age=0',
'Connection': 'keep-alive',
'Referer': 'https://www.cqggzy.com/yunyangweb/xxhz/014001/014001001/transactionInfo6.html',
'Cookie': 'cookie_www=19398923; __jsluid_s=f82cd3335e61d10bef4294e1724780e6; Hm_lvt_3b83938a8721dadef0b185225769572a=1678514589; Hm_lpvt_3b83938a8721dadef0b185225769572a=1678514589',
'Host': 'www.cqggzy.com',
# 'Upgrade-Insecure-Requests': '1',
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
        }
    def parse(self):
        date = tool.date
        # date = '2020-12-17'
        page = 0
        while True:
            data = {"token": "", "pn": page, "rn": 18, "sdt": "", "edt": "", "wd": "", "inc_wd": "", "exc_wd": "",
                    "fields": "", "cnum": "010",
                    "sort": "{\"istop\":0,\"ordernum\":0,\"webdate\":0,\"pubinwebdate\":0}", "ssort": "", "cl": 10000,
                    "terminal": "", "condition": [
                    {"fieldName": "categorynum", "equal": "014001001", "notEqual": None, "equalList": None,
                     "notEqualList": ["014001018", "014002014", "014005015"], "isLike": True, "likeType": 2}],
                    "time": None, "highlights": "", "statistics": None, "unionCondition": None, "accuracy": "",
                    "noParticiple": "1", "searchRange": None, "noWd": True}
            page += 1
            resp = tool.requests_post_to(self.url, data=data, headers=self.headers)
            print('*' * 20, page, '*' * 20)
            html=json.loads(resp)
            detail = html["result"]["records"]
    # def requests_get(self, url, headers):
    #     num = 0
    #     while True:
    #         try:
    #             rst = requests.get(url, headers=headers, timeout=30, verify=False)
    #             rst.encoding = rst.apparent_encoding
    #             return rst.text
    #         except Exception as e:
    #             # traceback.print_exc()
    #             print('请求错误', e.args)
    #             num += 1
    #             if num == 10:
    #                 int('a')
    #             time.sleep(5)
    #             continue


    # def parse(self):
    #     date = tool.date
    #     # date = '2021-07-26'
    #     page = 0
    #     while True:
    #         page += 1
    #         if page == 1:
    #             te = self.requests_get(self.url.format('list'), self.headers)
    #         else:
    #             te = self.requests_get(self.url.format('list_' + str(page-1)), self.headers)
    #         html = HTML(te)
    #         print('*' * 20, page, '*' * 20
            for li in detail:
                try:
                    title = li["title"]
                    date_Today = li['pubinwebdate'].split(' ')[0]
                    enddate=date_Today.replace('-','')
                    infoid=li['infoid']
                    url=f'https://www.cqggzy.com/yunyangweb/xxhz/014001/014001001/014001001002/{enddate}/{infoid}.html'

                except:
                    continue
                if 'http' not in url:
                    url = 'http://www.yunyang.gov.cn/zwgk_257/zfxxgkml' + url[1:]
                print(title, url, date_Today)
                time.sleep(666)
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
        t = tool.requests_get(url, self.headers).replace('\xa9', '').replace('<br>&nbsp;&nbsp;', '')
        # print(t)
        # time.sleep(2222)
        url_html = etree.HTML(t)
        # try:
        detail = url_html.xpath('//div[@class="detail-block"]')[0]
        detail_html = etree.tostring(detail,method='HTML')
        detail_html = html.unescape(detail_html.decode()).replace("display: none", '').replace("\u2022", '').replace('\xa0', '')
        detail_text = url_html.xpath('string(//div[@class="detail-block"])').replace('\xa0', '').replace('\n',''). \
            replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
        if len(detail_html) < 200:
            int('a')
        # except:
        #     try:
        #         detail = url_html.xpath('//*[@class="view TRS_UEDITOR trs_paper_default trs_word"]/table')[0]
        #         detail_html = etree.tostring(detail, method='HTML')
        #         detail_html = html.unescape(detail_html.decode()).replace("display: none", '').replace("\u2022",
        #                                                                                                '').replace('\xa0',
        #                                                                                                            '')
        #         detail_text = url_html.xpath('string(//*[@class="view TRS_UEDITOR trs_paper_default trs_word"]/table)').replace('\xa0',
        #                                                                                                                         '').replace(
        #             '\n',
        #             ''). \
        #             replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
        #         if len(detail_html) < 200:
        #             int('a')
        #     except:
        #         detail = url_html.xpath('//*[@class="zwxl-article"]')[0]
        #         detail_html = etree.tostring(detail, method='HTML')
        #         detail_html = html.unescape(detail_html.decode()).replace("display: none", '').replace("\u2022",
        #                                                                                                '').replace(
        #             '\xa0',
        #             '')
        #         detail_text = url_html.xpath(
        #             'string(//*[@class="zwxl-article"])').replace('\xa0',
        #                                                                                                '').replace(
        #             '\n',
        #             ''). \
        #             replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
        #         if len(detail_html) < 200:
        #             int('a')
        item = {}
        item['title'] = title.replace('\u2022', '')
        item['url'] = url
        item['date'] = date
        item['typeid'] = tool.get_typeid(item['title'])
        item['senddate'] = int(time.time())
        item['mid'] = 867
        item['nativeplace'] = 11529
        item['infotype'] = tool.get_infotype(item['title'])
        item['body'] = tool.qudiao_width(detail_html)
        item['endtime'] = tool.get_endtime(detail_html)
        if item['endtime'] == '':
            item['endtime'] = int(time.mktime(time.strptime(date, "%Y-%m-%d")))
        else:
            try:
                item['endtime'] = int(time.mktime(time.strptime(item['endtime'], "%Y-%m-%d")))
            except:
                item['endtime'] = int(time.mktime(time.strptime(date, "%Y-%m-%d")))
        item['tel'] = tool.get_tel(detail_html)
        item['email'] = ''
        item['address'] = tool.get_address(detail_html)
        item['linkman'] = tool.get_linkman(detail_html)
        item['function'] = tool.get_function(detail_html)
        item['resource'] = '云阳县公共资源交易中心'
        item['shi'] = 11529
        item['sheng'] = 11500
        item['removal']= title
        process_item(item)
        # print(item)

    def get_nativeplace(self, addr):
        city = ''
        city_list = [['6505.001', '金家庄区'], ['6505.002', '花山区'], ['6505.003', '雨山区'], ['6505.004', '当涂县']]

        for i in city_list:
            if i[1] in addr:
                city = float(i[0])
                break
        if city == '':
            city = 6505
        return city

if __name__ == '__main__':
    import traceback,os
    try:
        jl = wenshan_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
        tool.send_error('报错文件：'+str(os.path.basename(__file__))+'报错信息：'+str(e))


