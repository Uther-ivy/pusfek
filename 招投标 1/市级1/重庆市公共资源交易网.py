# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 重庆市公共资源交易网
class xinyang_ggzy:
    def __init__(self):
        self.url_list = ["https://www.cqggzy.com/interface/rest/esinteligentsearch/getFullTextDataNew"]
        self.url = self.url_list.pop(0)
        self.headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Origin': 'https://www.cqggzy.com',
            'Referer': 'https://www.cqggzy.com/jyjg/transaction_detail.html',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
        
        }

    def parse(self):
        date = tool.date
        date_str = time.strftime('%Y-%m-%d', time.localtime(time.time()-86400*9))
        # date = '2020-07-10'
        page = 0
        data = {"token":"","pn":0,"rn":20,"sdt":"","edt":"","wd":" ","inc_wd":"","exc_wd":"","fields":"title;projectno;","cnum":"001","sort":"{\"webdate\":\"0\"}","ssort":"title","cl":200,"terminal":"","condition":[{"fieldName":"categorynum","equal":"014","notEqual":None,"equalList":None,"notEqualList":["014001018","004002005","014001015","014005014","014008011"],"isLike":True,"likeType":2}],"time":[{"fieldName":"webdate","startTime":"2021-06-13 00:00:00","endTime":"2021-06-22 23:59:59"}],"highlights":"title","statistics":None,"unionCondition":[],"accuracy":"","noParticiple":"0","searchRange":None,"isBusiness":"1"}
        while True:
            data['pn'] = page * 20
            data['time'][0]['startTime'] = date_str + ' 00:00:00'
            data['time'][0]['endTime'] = date + ' 23:59:59'
            page += 1
            text = tool.requests_post_to(self.url, data, self.headers)
            detail = json.loads(text)['result']['records']
            print('*' * 20, page, '*' * 20)
            for li in detail:
                date_Today = li["infodate"][:10].replace('\n', '').replace('\t', '').replace('\r', '').replace(' ', '')\
                    .replace('[', '').replace(']', '')
                title = li["title"]
                if len(li["categorynum"]) == 12:
                    url = f'https://www.cqggzy.com/xxhz/{li["categorynum"][:-6]}/{li["categorynum"][:-3]}/{li["categorynum"]}/{date_Today.replace("-", "")}/{li["infoid"]}.html'
                else:
                    url = f'https://www.cqggzy.com/xxhz/{li["categorynum"][:-3]}/{li["categorynum"]}/{date_Today.replace("-", "")}/{li["infoid"]}.html'
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
            if page == 30:
                self.url = self.url_list.pop(0)
                break

    def parse_detile(self, title, url, date):
        print(url)
        t = tool.requests_get(url, self.headers)
        url_html = etree.HTML(t)
        try:
            detail = url_html.xpath('//*[@id="mainContent"]')[0]
        except:
            return
        detail_html = etree.tostring(detail, method='HTML')
        detail_html = html.unescape(detail_html.decode()).replace('\xa0', '').replace('\ufeff', '')
        detail_text = url_html.xpath('string(//*[@id="mainContent"])') \
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
        item['endtime'] = int(time.mktime(time.strptime(date, "%Y-%m-%d")))
        item['tel'] = tool.get_tel(detail_text)
        item['email'] = ''
        item['address'] = tool.get_address(detail_text)
        item['nativeplace'] = self.get_nativeplace(item['title'])
        item['linkman'] = tool.get_linkman(detail_text)
        item['function'] = tool.get_function(detail_text)
        item['resource'] = '重庆市公共资源交易网'
        item["shi"] = int(str(item["nativeplace"]).split('.')[0])
        item['sheng'] = 11500
        item['removal']= title
        process_item(item)
        # print(item['body'])

    def get_nativeplace(self, addr):
        city = ''
        city_list = [['11501', '万州'], ['11502', '涪陵'], ['11503', '渝中'], ['11504', '大渡口'], ['11505', '江北'], ['11506', '沙坪坝'], ['11507', '九龙坡'], ['11508', '南岸'], ['11509', '北碚'], ['11510', '万盛'], ['11511', '双桥'], ['11512', '渝北'], ['11513', '巴南'], ['11514', '黔江'], ['11515', '长寿'], ['11516', '綦江'], ['11517', '潼南'], ['11518', '铜梁'], ['11519', '大足'], ['11520', '荣昌'], ['11521', '璧山'], ['11522', '梁平'], ['11523', '城口'], ['11524', '丰都'], ['11525', '垫江'], ['11526', '武隆'], ['11527', '忠'], ['11528', '开'], ['11529', '云阳'], ['11530', '奉节'], ['11531', '巫山'], ['11532', '巫溪'], ['11533', '石柱土家族自治'], ['11534', '秀山土家族苗族自治'], ['11535', '酉阳土家族苗族自治'], ['11536', '彭水苗族土家族自治'], ['11537', '江津'], ['11538', '合川'], ['11539', '永川']]

        for i in city_list:
            if i[1] in addr:
                city = float(i[0])
                break
        if city == '':
            city = 11500
        return city

if __name__ == '__main__':
    jl = xinyang_ggzy()
    jl.parse()


