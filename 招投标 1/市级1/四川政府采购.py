# -*- coding: utf-8 -*-
import json
import re
import time, html
import traceback

import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 四川政府采购
class xinyang_ggzy:
    def __init__(self):
        self.url_list = [
            'https://zfcg.scsczt.cn/freecms/rest/v1/notice/selectInfoMoreChannel.do?&siteId=94c965cc-c55d-4f92-8469-d5875c68bd04&channel=c5bff13f-21ca-4dac-b158-cb40accd3035&currPage={}&pageSize=10&noticeType=00101&regionCode=&purchaseManner=&title=&openTenderCode=&purchaser=&agency=&purchaseNature=&operationStartTime=&operationEndTime=&selectTimeName=noticeTime&cityOrArea=',
            'https://zfcg.scsczt.cn/freecms/rest/v1/notice/selectInfoMoreChannel.do?&siteId=94c965cc-c55d-4f92-8469-d5875c68bd04&channel=c5bff13f-21ca-4dac-b158-cb40accd3035&currPage={}&pageSize=10&noticeType=00102&regionCode=&purchaseManner=&title=&openTenderCode=&purchaser=&agency=&purchaseNature=&operationStartTime=&operationEndTime=&selectTimeName=noticeTime&cityOrArea=',
            'https://zfcg.scsczt.cn/freecms/rest/v1/notice/selectInfoMoreChannel.do?&siteId=94c965cc-c55d-4f92-8469-d5875c68bd04&channel=c5bff13f-21ca-4dac-b158-cb40accd3035&currPage={}&pageSize=10&noticeType=00103&regionCode=&purchaseManner=&title=&openTenderCode=&purchaser=&agency=&purchaseNature=&operationStartTime=&operationEndTime=&selectTimeName=noticeTime&cityOrArea=',
            'https://zfcg.scsczt.cn/freecms/rest/v1/notice/selectInfoMoreChannel.do?&siteId=94c965cc-c55d-4f92-8469-d5875c68bd04&channel=c5bff13f-21ca-4dac-b158-cb40accd3035&currPage={}&pageSize=10&noticeType=001004,001006&regionCode=&purchaseManner=&title=&openTenderCode=&purchaser=&agency=&purchaseNature=&operationStartTime=&operationEndTime=&selectTimeName=noticeTime&cityOrArea=',
        ]
        self.url = self.url_list.pop(0)
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        }

    def parse(self):
        date = tool.date
        # date = '2020-07-10'
        page = 0
        while True:
            page += 1
            text = tool.requests_get(self.url.format(page), self.headers)
            # detail = HTML(text).xpath("//div[@class='info']/ul/li")
            detail = json.loads(text)['data']
            print('*' * 20, page, '*' * 20)
            for li in detail:
                title = li['title']
                #?noticeType=001004,001006
                code = re.findall('noticeType=(.*?)&regionCode', self.url)[0]
                url = 'https://zfcg.scsczt.cn' + li['pageurl'] + '?noticeType=' + code
                if 'http' not in url and 'HTTP' not in url:
                    url = "http://www.ccgp-sichuan.gov.cn" + url
                date_Today = li['addtimeStr'][:10]
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
        # print(t)
        # time.sleep(6666)
        url_html = etree.HTML(t)
        detail = url_html.xpath('//*[@id="content"]')[0]
        detail_html = etree.tostring(detail, method='HTML')
        detail_html = html.unescape(detail_html.decode()).replace('\xa0', '').replace('\ufeff', '')
        detail_text = url_html.xpath('string(//*[@id="content"])') \
            .replace('\xa0', '').replace('\n', '').replace('\r', '').replace('\t', '') \
            .replace(' ', '').replace('\xa5', '').replace('\ufeff', '')
        item = {}
        item['title'] = title.replace('\u2022', '')
        item['url'] = url
        item['date'] = date
        item['typeid'] = tool.get_typeid(item['title'])
        item['senddate'] = int(time.time())
        item['mid'] = 867
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
        item['nativeplace'] = self.get_nativeplace(item['title'])
        item['linkman'] = tool.get_linkman(detail_text)
        item['function'] = tool.get_function(detail_text)
        item['resource'] = '四川政府采购'
        item["shi"] = int(str(item["nativeplace"]).split('.')[0])
        item['sheng'] = 12000
        item['removal']= title
        process_item(item)
        # print(item['body'])

    def get_nativeplace(self, addr):
        city = ''
        city_list = [['12001', '成都'], ['12001.001', '锦江'], ['12001.01', '金堂'], ['12001.011', '双流'], ['12001.012', '郫'], ['12001.013', '大邑'], ['12001.014', '蒲江'], ['12001.015', '新津'], ['12001.016', '都江堰'], ['12001.017', '彭州'], ['12001.018', '邛崃'], ['12001.019', '崇州'], ['12001.002', '青羊'], ['12001.003', '金牛'], ['12001.004', '武侯'], ['12001.005', '成华'], ['12001.006', '龙泉驿'], ['12001.007', '青白江'], ['12001.008', '新都'], ['12001.009', '温江'], ['12002', '自贡'], ['12002.001', '自流井'], ['12002.002', '贡井'], ['12002.003', '大安'], ['12002.004', '沿滩'], ['12002.005', '荣'], ['12002.006', '富顺'], ['12003', '攀枝花'], ['12003.001', '东'], ['12003.002', '西'], ['12003.003', '仁和'], ['12003.004', '米易'], ['12003.005', '盐边'], ['12004', '泸州'], ['12004.001', '江阳'], ['12004.002', '纳溪'], ['12004.003', '龙马潭'], ['12004.004', '泸'], ['12004.005', '合江'], ['12004.006', '叙永'], ['12004.007', '古蔺'], ['12005', '德阳'], ['12005.001', '旌阳'], ['12005.002', '中江'], ['12005.003', '罗江'], ['12005.004', '广汉'], ['12005.005', '什邡'], ['12005.006', '绵竹'], ['12006', '绵阳'], ['12006.001', '涪城'], ['12006.002', '游仙'], ['12006.003', '三台'], ['12006.004', '盐亭'], ['12006.005', '安'], ['12006.006', '梓潼'], ['12006.007', '北川羌族自治'], ['12006.008', '平武'], ['12006.009', '江油'], ['12007', '广元'], ['12007.001', '中'], ['12007.002', '元坝'], ['12007.003', '朝天'], ['12007.004', '旺苍'], ['12007.005', '青川'], ['12007.006', '剑阁'], ['12007.007', '苍溪'], ['12008', '遂宁'], ['12008.001', '船山'], ['12008.002', '安居'], ['12008.003', '蓬溪'], ['12008.004', '射洪'], ['12008.005', '大英'], ['12009', '内江'], ['12009.001', '中'], ['12009.002', '东兴'], ['12009.003', '威远'], ['12009.004', '资中'], ['12009.005', '隆昌'], ['12010', '乐山'], ['12010.001', '中'], ['12010.01', '马边彝族自治'], ['12010.011', '峨眉山'], ['12010.002', '沙湾'], ['12010.003', '五通桥'], ['12010.004', '金口河'], ['12010.005', '犍为'], ['12010.006', '井研'], ['12010.007', '夹江'], ['12010.008', '沐川'], ['12010.009', '峨边彝族自治'], ['12011', '南充'], ['12011.001', '顺庆'], ['12011.002', '高坪'], ['12011.003', '嘉陵'], ['12011.004', '南部'], ['12011.005', '营山'], ['12011.006', '蓬安'], ['12011.007', '仪陇'], ['12011.008', '西充'], ['12011.009', '阆中'], ['12012', '眉山'], ['12012.001', '东坡'], ['12012.002', '仁寿'], ['12012.003', '彭山'], ['12012.004', '洪雅'], ['12012.005', '丹棱'], ['12012.006', '青神'], ['12013', '宜宾'], ['12013.001', '翠屏'], ['12013.01', '屏山'], ['12013.002', '宜宾'], ['12013.003', '南溪'], ['12013.004', '江安'], ['12013.005', '长宁'], ['12013.006', '高'], ['12013.007', '珙'], ['12013.008', '筠连'], ['12013.009', '兴文'], ['12014', '广安'], ['12014.001', '广安'], ['12014.002', '岳池'], ['12014.003', '武胜'], ['12014.004', '邻水'], ['12014.005', '华莹'], ['12015', '达州'], ['12015.001', '通川'], ['12015.002', '达'], ['12015.003', '宣汉'], ['12015.004', '开江'], ['12015.005', '大竹'], ['12015.006', '渠'], ['12015.007', '万源'], ['12016', '雅安'], ['12016.001', '雨城'], ['12016.002', '名山'], ['12016.003', '荥经'], ['12016.004', '汉源'], ['12016.005', '石棉'], ['12016.006', '天全'], ['12016.007', '芦山'], ['12016.008', '宝兴'], ['12017', '巴中'], ['12017.001', '巴州'], ['12017.002', '通江'], ['12017.003', '南江'], ['12017.004', '平昌'], ['12018', '资阳'], ['12018.001', '雁江'], ['12018.002', '安岳'], ['12018.003', '乐至'], ['12018.004', '简阳'], ['12019', '阿坝藏族羌族自治州'], ['12019.001', '汶川'], ['12019.01', '壤塘'], ['12019.011', '阿坝'], ['12019.012', '若尔盖'], ['12019.013', '红原'], ['12019.002', '理'], ['12019.003', '茂'], ['12019.004', '松潘'], ['12019.005', '九寨沟'], ['12019.006', '金川'], ['12019.007', '小金'], ['12019.008', '黑水'], ['12019.009', '马尔康'], ['12020', '甘孜藏族自治州'], ['12020.001', '康定'], ['12020.01', '德格'], ['12020.011', '白玉'], ['12020.012', '石渠'], ['12020.013', '色达'], ['12020.014', '理塘'], ['12020.015', '巴塘'], ['12020.016', '乡城'], ['12020.017', '稻城'], ['12020.018', '得荣'], ['12020.002', '泸定'], ['12020.003', '丹巴'], ['12020.004', '九龙'], ['12020.005', '雅江'], ['12020.006', '道孚'], ['12020.007', '炉霍'], ['12020.008', '甘孜'], ['12020.009', '新龙'], ['12021', '凉山彝族自治州'], ['12021.001', '西昌'], ['12021.01', '金阳'], ['12021.011', '昭觉'], ['12021.012', '喜德'], ['12021.013', '冕宁'], ['12021.014', '越西'], ['12021.015', '甘洛'], ['12021.016', '美姑'], ['12021.017', '雷波'], ['12021.002', '木里藏族自治'], ['12021.003', '盐源'], ['12021.004', '德昌'], ['12021.005', '会理'], ['12021.006', '会东'], ['12021.007', '宁南'], ['12021.008', '普格']]

        for i in city_list:
            if i[1] in addr:
                city = float(i[0])
                break
        if city == '':
            city = 12000
        return city

if __name__ == '__main__':
    import traceback, os
    try:
        jl = xinyang_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
