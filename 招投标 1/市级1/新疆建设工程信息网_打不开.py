# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 新疆建设工程信息网
class wenshan_ggzy:
    def __init__(self):
        self.domain_name = 'http://ztb.xjjs.gov.cn'
        self.url_list = [
            'http://ztb.xjjs.gov.cn/xjweb/jyxx/004001/004001001/MoreInfo.aspx?CategoryNum=004001001&Paging={}',
            'http://ztb.xjjs.gov.cn/xjweb/jyxx/004001/004001002/MoreInfo.aspx?CategoryNum=004001002&Paging={}',
            'http://ztb.xjjs.gov.cn/xjweb/jyxx/004001/004001003/MoreInfo.aspx?CategoryNum=004001003&Paging={}',
            'http://ztb.xjjs.gov.cn/xjweb/jyxx/004001/004001006/004001006001/MoreInfo.aspx?CategoryNum=004001006001&Paging={}',
            'http://ztb.xjjs.gov.cn/xjweb/jyxx/004001/004001006/004001006002/MoreInfo.aspx?CategoryNum=004001006002&Paging={}',
            'http://ztb.xjjs.gov.cn/xjweb/jyxx/004001/004001006/004001006003/MoreInfo.aspx?CategoryNum=004001006003&Paging={}',
            'http://ztb.xjjs.gov.cn/xjweb/jyxx/004002/004002001/MoreInfo.aspx?CategoryNum=004002001&Paging={}',
            'http://ztb.xjjs.gov.cn/xjweb/jyxx/004002/004002002/MoreInfo.aspx?CategoryNum=004002002&Paging={}',
            'http://ztb.xjjs.gov.cn/xjweb/jyxx/004002/004002003/MoreInfo.aspx?CategoryNum=004002003&Paging={}',
            'http://ztb.xjjs.gov.cn/xjweb/jyxx/004002/004002006/004002006001/MoreInfo.aspx?CategoryNum=004002006001&Paging={}',
            'http://ztb.xjjs.gov.cn/xjweb/jyxx/004002/004002006/004002006002/MoreInfo.aspx?CategoryNum=004002006002&Paging={}',
            'http://ztb.xjjs.gov.cn/xjweb/jyxx/004002/004002006/004002006003/MoreInfo.aspx?CategoryNum=004002006003&Paging={}'
        ]
        self.url = self.url_list.pop(0)
        self.headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Cookie': 'JSESSIONID=662863FD2199FBD1672A04A290868047; _CSRFCOOKIE=73F3D7A1BCDCA9001D7B1483A214C4E98DE2528B; EPTOKEN=73F3D7A1BCDCA9001D7B1483A214C4E98DE2528B; oauthClientId=demoClient; oauthPath=http://172.16.5.21:8080/EpointWebBuilder; oauthLoginUrl=http://172.16.5.21:8080/EpointWebBuilder/rest/oauth2/authorize?client_id=demoClient&state=a&response_type=code&scope=user&redirect_uri=; oauthLogoutUrl=http://172.16.5.21:8080/EpointWebBuilder/rest/oauth2/logout?redirect_uri=; noOauthRefreshToken=986d4fe7e5dd29b64c9e7b7a6d66e089; noOauthAccessToken=77c09e0bf98b6220b544961097eed84a; sub_domain_cokie=TiG5CMD9KQ41mmsARPTuAg%3D%3D; region_name=%E4%B9%8C%E9%B2%81%E6%9C%A8%E9%BD%90%E5%B8%82',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',

        }

    def parse(self):
        date = tool.date
        # date = '2020-09-24'
        page = 0
        while True:
            page += 1
            text = tool.requests_get(self.url.format(page), self.headers)
            print('*' * 20, page, '*' * 20)
            html = HTML(text)
            # print(11, text)
            # time.sleep(6666)
            detail = html.xpath('//*[@id="MoreInfoList1_DataGrid1"]/tr')
            for li in detail:
                title = li.xpath('./td[2]/a/@title')[0]
                url = li.xpath('./td[2]/a/@href')[0]
                date_Today = li.xpath('./td[3]/text()')[0].replace('\xa0', '').replace('\n', '').\
                    replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')\
                    .replace('[', '').replace(']', '')
                if 'http' not in url:
                    url = self.domain_name + url
                # print(title, url, date_Today)
                # time.sleep(666)
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
        t = tool.requests_get(url, self.headers).replace('\xa9', '').replace('<br>&nbsp;&nbsp;', '')
        # print(t)
        # time.sleep(2222)
        url_html = etree.HTML(t)
        detail = url_html.xpath('//*[@id="TDContent"]')[0]
        detail_html = etree.tostring(detail, method='HTML')
        detail_html = html.unescape(detail_html.decode()).replace("display: none", '')
        detail_text = url_html.xpath('string(//*[@id="TDContent"])').replace('\xa0', '').replace('\n',
                                                                                                             ''). \
            replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
        if len(detail_html) < 200:
            int('a')
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
        # item['body'] = tool.update_img(self.domain_name, item['body'])
        d = re.findall('<table id="tb_Line".*?</table>', item['body'], re.S)
        if len(d) != 0:
            item['body'] = item['body'].replace(d[0], '').replace('\xa0', '')
        # print(item['body'])
        # time.sleep(2222)
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
        item['linkman'] = tool.get_linkman(detail_text)
        item['function'] = tool.get_function(detail_text)
        item['resource'] = '新疆建设工程信息网'
        item['shi'] = int(item['nativeplace'])
        item['sheng'] = 16000
        item['removal']= title
        process_item(item)

    def get_nativeplace(self, addr):
        city = ''
        city_list = [['16001', '乌鲁木齐'], ['16001.001', '天山区'], ['16001.002', '沙依巴克区'], ['16001.003', '新区'], ['16001.004', '水磨沟区'], ['16001.005', '头屯河区'], ['16001.006', '达坂城区'], ['16001.007', '东山区'], ['16001.008', '乌鲁木齐县'], ['16002', '克拉玛依'], ['16002.001', '独山子区'], ['16002.002', '克拉玛依区'], ['16002.003', '白碱滩区'], ['16002.004', '乌尔禾区'], ['16003', '吐鲁番地区'], ['16003.001', '吐鲁番'], ['16003.002', '鄯善县'], ['16003.003', '托克逊县'], ['16004', '哈密地区'], ['16004.001', '哈密'], ['16004.002', '巴里坤哈萨克自治县'], ['16004.003', '伊吾县'], ['16005', '昌吉回族自治州'], ['16005.001', '昌吉'], ['16005.002', '阜康'], ['16005.003', '米泉'], ['16005.004', '呼图壁县'], ['16005.005', '玛纳斯县'], ['16005.006', '奇台县'], ['16005.007', '吉木萨尔县'], ['16005.008', '木垒哈萨克自治县'], ['16006', '博尔塔拉蒙古自治州'], ['16006.001', '博乐'], ['16006.002', '精河县'], ['16006.003', '温泉县'], ['16007', '巴音郭楞蒙古自治州'], ['16007.001', '库尔勒'], ['16007.002', '轮台县'], ['16007.003', '尉犁县'], ['16007.004', '若羌县'], ['16007.005', '且末县'], ['16007.006', '焉耆回族自治县'], ['16007.007', '和静县'], ['16007.008', '和硕县'], ['16007.009', '博湖县'], ['16008', '阿克苏地区'], ['16008.001', '阿克苏'], ['16008.002', '温宿县'], ['16008.003', '库车县'], ['16008.004', '沙雅县'], ['16008.005', '新和县'], ['16008.006', '拜城县'], ['16008.007', '乌什县'], ['16008.008', '阿瓦提县'], ['16008.009', '柯坪县'], ['16009', '克孜勒苏柯尔克孜自治州'], ['16009.001', '阿图什'], ['16009.002', '阿克陶县'], ['16009.003', '阿合奇县'], ['16009.004', '乌恰县'], ['16010', '喀什地区'], ['16010.001', '喀什'], ['16010.01', '伽师县'], ['16010.011', '巴楚县'], ['16010.012', '塔什库尔干塔吉克自治县'], ['16010.002', '疏附县'], ['16010.003', '疏勒县'], ['16010.004', '英吉沙县'], ['16010.005', '泽普县'], ['16010.006', '莎车县'], ['16010.007', '叶城县'], ['16010.008', '麦盖提县'], ['16010.009', '岳普湖县'], ['16011', '和田地区'], ['16011.001', '和田'], ['16011.002', '和田县'], ['16011.003', '墨玉县'], ['16011.004', '皮山县'], ['16011.005', '洛浦县'], ['16011.006', '策勒县'], ['16011.007', '于田县'], ['16011.008', '民丰县'], ['16012', '伊犁哈萨克自治州'], ['16012.001', '伊宁'], ['16012.01', '尼勒克县'], ['16012.002', '奎屯'], ['16012.003', '伊宁县'], ['16012.004', '察布查尔锡伯自治县'], ['16012.005', '霍城县'], ['16012.006', '巩留县'], ['16012.007', '新源县'], ['16012.008', '昭苏县'], ['16012.009', '特克斯县'], ['16013', '塔城地区'], ['16013.001', '塔城'], ['16013.002', '乌苏'], ['16013.003', '额敏县'], ['16013.004', '沙湾县'], ['16013.005', '托里县'], ['16013.006', '裕民县'], ['16013.007', '和布克赛尔蒙古自治县'], ['16014', '阿勒泰地区'], ['16014.001', '阿勒泰'], ['16014.002', '布尔津县'], ['16014.003', '富蕴县'], ['16014.004', '福海县'], ['16014.005', '哈巴河县'], ['16014.006', '青河县'], ['16014.007', '吉木乃县'], ['16015', '直辖行政单位'], ['16015.001', '石河子'], ['16015.002', '阿拉尔'], ['16015.003', '图木舒克']]

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
        jl = wenshan_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
        tool.send_error('报错文件：'+str(os.path.basename(__file__))+'报错信息：'+str(e))



