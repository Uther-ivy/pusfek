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

# 陕西政府采购
class xinyang_ggzy:
    def __init__(self):
        self.url_list = [
            'http://www.ccgp-shaanxi.gov.cn/freecms/rest/v1/notice/selectInfoMoreChannel.do?&siteId=a7a15d60-de5b-42f2-b35a-7e3efc34e54f&channel=1eb454a2-7ff7-4a3b-b12c-12acc2685bd1&currPage={}&pageSize=10&noticeType=00101,001011&regionCode=610001&purchaseManner=&title=&openTenderCode=&purchaseNature=&operationStartTime=&operationEndTime=&selectTimeName=noticeTime&cityOrArea=',
            'http://www.ccgp-shaanxi.gov.cn/freecms/rest/v1/notice/selectInfoMoreChannel.do?&siteId=a7a15d60-de5b-42f2-b35a-7e3efc34e54f&channel=1eb454a2-7ff7-4a3b-b12c-12acc2685bd1&currPage={}&pageSize=10&noticeType=001021,001022,001023,001024,001025,001026,001029,001006&regionCode=610001&purchaseManner=&title=&openTenderCode=&purchaseNature=&operationStartTime=&operationEndTime=&selectTimeName=noticeTime&cityOrArea=',
            'http://www.ccgp-shaanxi.gov.cn/freecms/rest/v1/notice/selectInfoMoreChannel.do?&siteId=a7a15d60-de5b-42f2-b35a-7e3efc34e54f&channel=1eb454a2-7ff7-4a3b-b12c-12acc2685bd1&currPage={}&pageSize=10&noticeType=001031,001032&regionCode=610001&purchaseManner=&title=&openTenderCode=&purchaseNature=&operationStartTime=&operationEndTime=&selectTimeName=noticeTime&cityOrArea=',
            'http://www.ccgp-shaanxi.gov.cn/freecms/rest/v1/notice/selectInfoMoreChannel.do?&siteId=a7a15d60-de5b-42f2-b35a-7e3efc34e54f&channel=1eb454a2-7ff7-4a3b-b12c-12acc2685bd1&currPage={}&pageSize=10&noticeType=001004,001006&regionCode=610001&purchaseManner=&title=&openTenderCode=&purchaseNature=&operationStartTime=&operationEndTime=&selectTimeName=noticeTime&cityOrArea='
        ]
        self.url = self.url_list.pop(0)
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
            # 'Cookie': 'JSESSIONID=Jhs7fR6dYN1sfp2nr6qwFFyJzQGyyxJY4DbWnkT0FvTx1DR6hH3y!-1581166878'
            # 'Cookie': 'JSESSIONID=6cf5cad7-9e11-4d3d-9efd-70e2f5bc0d11'
        }

    def parse(self):
        date = tool.date
        # date = '2020-07-10'
        page = 0
        while True:
            page += 1
            text = tool.requests_get(self.url.format(page), self.headers)
            # print(text)
            # time.sleep(2222)
            detail = json.loads(text)['data']
            print('*' * 20, page, '*' * 20)
            for li in detail:
                title = li['title']
                date_Today = li['noticeTime'][:10]
                url = 'http://www.ccgp-shaanxi.gov.cn{}?noticeType={}&noticeId={}'.format(li['pageurl'], li['noticeType'], li['noticeId'])
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
        item['resource'] = '陕西政府采购'
        item["shi"] = int(str(item["nativeplace"]).split('.')[0])
        item['sheng'] = 14000
        item['removal']= title
        process_item(item)
        # print(item['body'])

    def get_nativeplace(self, addr):
        city = ''
        city_list = [['14001', '西安'], ['14001.001', '新城'], ['14001.01', '蓝田'], ['14001.011', '周至'], ['14001.012', '户'], ['14001.013', '高陵'], ['14001.002', '碑林'], ['14001.003', '莲湖'], ['14001.004', '灞桥'], ['14001.005', '未央'], ['14001.006', '雁塔'], ['14001.007', '阎良'], ['14001.008', '临潼'], ['14001.009', '长安'], ['14002', '铜川'], ['14002.001', '王益'], ['14002.002', '印台'], ['14002.003', '耀州'], ['14002.004', '宜君'], ['14003', '宝鸡'], ['14003.001', '滨'], ['14003.01', '麟游'], ['14003.011', '凤'], ['14003.012', '太白'], ['14003.002', '金台'], ['14003.003', '陈仓'], ['14003.004', '凤翔'], ['14003.005', '岐山'], ['14003.006', '扶风'], ['14003.007', '眉'], ['14003.008', '陇'], ['14003.009', '千阳'], ['14004', '咸阳'], ['14004.001', '秦都'], ['14004.01', '长武'], ['14004.011', '旬邑'], ['14004.012', '淳化'], ['14004.013', '武功'], ['14004.014', '兴平'], ['14004.002', '杨凌'], ['14004.003', '渭城'], ['14004.004', '三原'], ['14004.005', '泾阳'], ['14004.006', '乾'], ['14004.007', '礼泉'], ['14004.008', '永寿'], ['14004.009', '彬'], ['14005', '渭南'], ['14005.001', '临渭'], ['14005.01', '韩城'], ['14005.011', '华阴'], ['14005.002', '华'], ['14005.003', '潼关'], ['14005.004', '大荔'], ['14005.005', '合阳'], ['14005.006', '澄城'], ['14005.007', '蒲城'], ['14005.008', '白水'], ['14005.009', '富平'], ['14006', '延安'], ['14006.001', '宝塔'], ['14006.01', '洛川'], ['14006.011', '宜川'], ['14006.012', '黄龙'], ['14006.013', '黄陵'], ['14006.002', '延长'], ['14006.003', '延川'], ['14006.004', '子长'], ['14006.005', '安塞'], ['14006.006', '志丹'], ['14006.007', '吴旗'], ['14006.008', '甘泉'], ['14006.009', '富'], ['14007', '汉中'], ['14007.001', '汉台'], ['14007.01', '留坝'], ['14007.011', '佛坪'], ['14007.002', '南郑'], ['14007.003', '城固'], ['14007.004', '洋'], ['14007.005', '西乡'], ['14007.006', '勉'], ['14007.007', '宁强'], ['14007.008', '略阳'], ['14007.009', '镇巴'], ['14008', '榆林'], ['14008.001', '榆阳'], ['14008.01', '吴堡'], ['14008.011', '清涧'], ['14008.012', '子洲'], ['14008.002', '神木'], ['14008.003', '府谷'], ['14008.004', '横山'], ['14008.005', '靖边'], ['14008.006', '定边'], ['14008.007', '绥德'], ['14008.008', '米脂'], ['14008.009', '佳'], ['14009', '安康'], ['14009.001', '汉滨'], ['14009.01', '白河'], ['14009.002', '汉阴'], ['14009.003', '石泉'], ['14009.004', '宁陕'], ['14009.005', '紫阳'], ['14009.006', '岚皋'], ['14009.007', '平利'], ['14009.008', '镇坪'], ['14009.009', '旬阳'], ['14010', '商洛'], ['14010.001', '商州'], ['14010.002', '洛南'], ['14010.003', '丹凤'], ['14010.004', '商南'], ['14010.005', '山阳'], ['14010.006', '镇安']]

        for i in city_list:
            if i[1] in addr:
                city = float(i[0])
                break
        if city == '':
            city = 14000
        return city

if __name__ == '__main__':
    jl = xinyang_ggzy()
    jl.parse()


