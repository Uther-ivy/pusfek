# -*- coding: utf-8 -*-
import json
import re
import time, html
import traceback
# import scrapy
# from Crypto.Cipher import AES
import base64
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 新疆公共资源
class xinyang_ggzy:
    def __init__(self):
        self.url_list = ["004001/004001002/", "004001/004001003/", "004001/004001004/", "004001/004001005/", "004002/004002002/", "004002/004002003/",
                     "004002/004002004/", "004002/004002005/", "004002/004002007/"]
        self.url = self.url_list.pop(0)
        self.headers = {
                # "Accept": "*/*",
                # "Accept-Encoding": "gzip, deflate",
                # "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
                # "Connection": "keep-alive",
                # "Content-Type": "application/json",
                "Cookie": "ASP.NET_SessionId=a0rpktqemoxrh31gba1dwrwh",
                # "Host": "www.ccgp-xinjiang.gov.cn",
                # "Origin": "http://www.ccgp-xinjiang.gov.cn",
                # "Referer": "http://www.ccgp-xinjiang.gov.cn/ZcyAnnouncement/ZcyAnnouncement9/index.html",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36",
                # "X-Requested-With": "XMLHttpRequest"
            }

    def parse(self):
        date = tool.date
        # date = '2021-07-30'
        page = 0
        url_to = 'http://ggzy.xjbt.gov.cn/TPFront/jyxx/{}?Paging={}'
        while True:
            page += 1
            try:
                text = tool.requests_get(url_to.format(self.url, page),self.headers)
                print('*' * 20, page, '*' * 20)
                detail = HTML(text).xpath('//tr[@height="30"]')
            except Exception as e:
                page -= 1
                print('url_to 请求错误, 重新请求...', e)
                time.sleep(2)
            for li in detail:
                try:
                    title = li.xpath('./td[2]/a/@title')[0]
                    url = "http://ggzy.xjbt.gov.cn" + li.xpath('./td[2]/a/@href')[0]
                    date_Today = li.xpath('./td[3]/text()')[0].replace('[', '').replace(']', '')
                except:
                    continue
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
                    print('日期不符, 正在切换类型', date_Today, self.url)
                    return


    def parse_detile(self, title, url, date):
        print(url)
        t = tool.requests_get(url, self.headers)
        url_html = etree.HTML(t)
        try:
            detail = url_html.xpath('//*[@id="tblInfo"]')[0]
        except:
            return
        detail_html = etree.tostring(detail, method='HTML')
        detail_html = html.unescape(detail_html.decode()).replace('\xa0', '').replace('\ufeff', '')
        detail_text = url_html.xpath('string(//*[@id="tblInfo"])') \
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
        # b = re.findall('''<p class="news-article-info">.*?</p>''', item['body'])[0]
        # item['body'] = item['body'].replace(b, '')
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
        item['nativeplace'] = self.get_nativeplace(item['title'])
        item['linkman'] = tool.get_linkman(detail_text)
        item['function'] = tool.get_function(detail_text)
        item['resource'] = '新疆公共资源'
        item["shi"] = int(str(item["nativeplace"]).split('.')[0])
        item['sheng'] = 16000
        item['removal']= title
        process_item(item)
        # print(item['body'])

    def get_nativeplace(self, addr):
        city = ''
        city_list = [['16001', '乌鲁木齐'], ['16001.001', '天山'], ['16001.002', '沙依巴克'], ['16001.003', '新'], ['16001.004', '水磨沟'], ['16001.005', '头屯河'], ['16001.006', '达坂城'], ['16001.007', '东山'], ['16001.008', '乌鲁木齐'], ['16002', '克拉玛依'], ['16002.001', '独山子'], ['16002.002', '克拉玛依'], ['16002.003', '白碱滩'], ['16002.004', '乌尔禾'], ['16003', '吐鲁番地'], ['16003.001', '吐鲁番'], ['16003.002', '鄯善'], ['16003.003', '托克逊'], ['16004', '哈密地'], ['16004.001', '哈密'], ['16004.002', '巴里坤哈萨克自治'], ['16004.003', '伊吾'], ['16005', '昌吉回族自治州'], ['16005.001', '昌吉'], ['16005.002', '阜康'], ['16005.003', '米泉'], ['16005.004', '呼图壁'], ['16005.005', '玛纳斯'], ['16005.006', '奇台'], ['16005.007', '吉木萨尔'], ['16005.008', '木垒哈萨克自治'], ['16006', '博尔塔拉蒙古自治州'], ['16006.001', '博乐'], ['16006.002', '精河'], ['16006.003', '温泉'], ['16007', '巴音郭楞蒙古自治州'], ['16007.001', '库尔勒'], ['16007.002', '轮台'], ['16007.003', '尉犁'], ['16007.004', '若羌'], ['16007.005', '且末'], ['16007.006', '焉耆回族自治'], ['16007.007', '和静'], ['16007.008', '和硕'], ['16007.009', '博湖'], ['16008', '阿克苏地'], ['16008.001', '阿克苏'], ['16008.002', '温宿'], ['16008.003', '库车'], ['16008.004', '沙雅'], ['16008.005', '新和'], ['16008.006', '拜城'], ['16008.007', '乌什'], ['16008.008', '阿瓦提'], ['16008.009', '柯坪'], ['16009', '克孜勒苏柯尔克孜自治州'], ['16009.001', '阿图什'], ['16009.002', '阿克陶'], ['16009.003', '阿合奇'], ['16009.004', '乌恰'], ['16010', '喀什地'], ['16010.001', '喀什'], ['16010.01', '伽师'], ['16010.011', '巴楚'], ['16010.012', '塔什库尔干塔吉克自治'], ['16010.002', '疏附'], ['16010.003', '疏勒'], ['16010.004', '英吉沙'], ['16010.005', '泽普'], ['16010.006', '莎车'], ['16010.007', '叶城'], ['16010.008', '麦盖提'], ['16010.009', '岳普湖'], ['16011', '和田地'], ['16011.001', '和田'], ['16011.002', '和田'], ['16011.003', '墨玉'], ['16011.004', '皮山'], ['16011.005', '洛浦'], ['16011.006', '策勒'], ['16011.007', '于田'], ['16011.008', '民丰'], ['16012', '伊犁哈萨克自治州'], ['16012.001', '伊宁'], ['16012.01', '尼勒克'], ['16012.002', '奎屯'], ['16012.003', '伊宁'], ['16012.004', '察布查尔锡伯自治'], ['16012.005', '霍城'], ['16012.006', '巩留'], ['16012.007', '新源'], ['16012.008', '昭苏'], ['16012.009', '特克斯'], ['16013', '塔城地'], ['16013.001', '塔城'], ['16013.002', '乌苏'], ['16013.003', '额敏'], ['16013.004', '沙湾'], ['16013.005', '托里'], ['16013.006', '裕民'], ['16013.007', '和布克赛尔蒙古自治'], ['16014', '阿勒泰地'], ['16014.001', '阿勒泰'], ['16014.002', '布尔津'], ['16014.003', '富蕴'], ['16014.004', '福海'], ['16014.005', '哈巴河'], ['16014.006', '青河'], ['16014.007', '吉木乃'], ['16015', '直辖行政单位'], ['16015.001', '石河子'], ['16015.002', '阿拉尔']]

        for i in city_list:
            if i[1] in addr:
                city = float(i[0])
                break
        if city == '':
            city = 16000
        return city

if __name__ == '__main__':
    import traceback, os
    try:
        jl = xinyang_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
        tool.send_error('报错文件：'+str(os.path.basename(__file__))+'报错信息：'+str(e))


