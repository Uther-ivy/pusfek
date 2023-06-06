# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 甘肃经济信息网
class baoshan_ggzy:
    def __init__(self):
        self.url_list = [
            'http://www.gsei.com.cn/html/1336/',
            'http://www.gsei.com.cn/html/1337/',
            'http://www.gsei.com.cn/html/1662/',
            'http://www.gsei.com.cn/html/1657/',
            'http://www.gsei.com.cn/html/1656/',
            'http://www.gsei.com.cn/html/1663/',
            'http://www.gsei.com.cn/html/1664/',

        ]
        self.url = self.url_list.pop(0)
        self.headers = {
            # 'Cookie': 'homeid=1a444a31-e460-47ff-9931-1c075c0f3cd8',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        }


    def parse(self):
        page = 0
        date = tool.date
        while True:
            page += 1
            if page == 1:
                text = tool.requests_get(self.url,self.headers)
            else:
                text = tool.requests_get(self.url+'list-'+str(page)+'.html', self.headers)
            html = HTML(text)
            detail = html.xpath('//ul[@class="adaplist94"]/li')
            for li in detail:
                url= 'http://www.gsei.com.cn'+li.xpath('./a/@href')[0]
                title = li.xpath('./a/@title')[0]
                date_Today = li.xpath('./span/text()')[0]
                if '测试' in title or '.PDF' in url or '发布' in date_Today or '.doc' in url or '.pdf' in url:
                    continue
                # url='http://ggzy.qqhr.gov.cn'+url
                # print(title, url, date_Today)
                # time.sleep(666)
                if tool.Transformation(date) <= tool.Transformation(date_Today):
                    if tool.removal(title, date):
                        self.parse_detile(title, url, date_Today)
                    else:
                        print('【existence】', url)
                        continue
                else:
                    # print(tool.Transformation(date),self.Transformation(date_Today))
                    print('日期不符, 正在切换类型', date_Today, self.url)
                    self.url = self.url_list.pop(0)
                    page = 0
                    break

    def parse_detile(self, title, url, date):
        print(url)
        t = tool.requests_get(url, self.headers)
        url_html = etree.HTML(t)
        try:
            detail = url_html.xpath('//div[@class="artcon"]')[0]
        except:
            return
        # print(detail)
        detail_html = etree.tostring(detail, method='HTML')
        detail_html = html.unescape(detail_html.decode())
        detail_text = url_html.xpath('string(//div[@class="artcon"])').replace('\xa0', '').replace('\n', ''). \
            replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
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
        item['nativeplace'] = self.get_nativeplace(title)
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
        item['resource'] = '甘肃经济信息网'
        item["shi"] = int(float(item["nativeplace"]))
        item['sheng'] = 14500
        # print(item)
        item['removal']= title
        process_item(item)

    def get_nativeplace(self, city):
        a = ''
        ls = [['14501', '兰州'], ['14501.001', '城关区'], ['14501.002', '七里河区'], ['14501.003', '西固区'], ['14501.004', '安宁区'], ['14501.005', '红古区'], ['14501.006', '永登县'], ['14501.007', '皋兰县'], ['14501.008', '榆中县'], ['14502', '嘉峪关'], ['14503', '金昌'], ['14503.001', '金川区'], ['14503.002', '永昌县'], ['14504', '白银'], ['14504.001', '白银区'], ['14504.002', '平川区'], ['14504.003', '靖远县'], ['14504.004', '会宁县'], ['14504.005', '景泰县'], ['14505', '天水'], ['14505.001', '秦城区'], ['14505.002', '北道区'], ['14505.003', '清水县'], ['14505.004', '秦安县'], ['14505.005', '甘谷县'], ['14505.006', '武山县'], ['14505.007', '张家川回族自治县'], ['14506', '武威'], ['14506.001', '凉州区'], ['14506.002', '民勤县'], ['14506.003', '古浪县'], ['14506.004', '天祝藏族自治县'], ['14507', '张掖'], ['14507.001', '甘州区'], ['14507.002', '肃南裕固族自治县'], ['14507.003', '民乐县'], ['14507.004', '临泽县'], ['14507.005', '高台县'], ['14507.006', '山丹县'], ['14508', '平凉'], ['14508.001', '崆峒区'], ['14508.002', '泾川县'], ['14508.003', '灵台县'], ['14508.004', '崇信县'], ['14508.005', '华亭县'], ['14508.006', '庄浪县'], ['14508.007', '静宁县'], ['14509', '酒泉'], ['14509.001', '肃州区'], ['14509.002', '金塔县'], ['14509.003', '安西县'], ['14509.004', '肃北蒙古族自治县'], ['14509.005', '阿克塞哈萨克族自治县'], ['14509.006', '玉门'], ['14509.007', '敦煌'], ['14510', '庆阳'], ['14510.001', '西峰区'], ['14510.002', '庆城县'], ['14510.003', '环县'], ['14510.004', '华池县'], ['14510.005', '合水县'], ['14510.006', '正宁县'], ['14510.007', '宁县'], ['14510.008', '镇原县'], ['14511', '定西'], ['14511.001', '安定区'], ['14511.002', '通渭县'], ['14511.003', '陇西县'], ['14511.004', '渭源县'], ['14511.005', '临洮县'], ['14511.006', '漳县'], ['14511.007', '岷县'], ['14512', '陇南'], ['14512.001', '武都区'], ['14512.002', '成县'], ['14512.003', '文县'], ['14512.004', '宕昌县'], ['14512.005', '康县'], ['14512.006', '西和县'], ['14512.007', '礼县'], ['14512.008', '徽县'], ['14512.009', '两当县'], ['14513', '临夏回族自治州'], ['14513.001', '临夏'], ['14513.002', '临夏县'], ['14513.003', '康乐县'], ['14513.004', '永靖县'], ['14513.005', '广河县'], ['14513.006', '和政县'], ['14513.007', '东乡族自治县'], ['14513.008', '积石山保安族东乡族撒拉族自治县'], ['14514', '甘南藏族自治州'], ['14514.001', '合作'], ['14514.002', '临潭县'], ['14514.003', '卓尼县'], ['14514.004', '舟曲县'], ['14514.005', '迭部县'], ['14514.006', '玛曲县'], ['14514.007', '碌曲县'], ['14514.008', '夏河县']]
        for i in ls:
            if i[1] in city:
                a = i[0]
                break
        if a == '':
            return 14500
        else:
            return a

if __name__ == '__main__':

    import traceback, os
    try:
        jl = baoshan_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
