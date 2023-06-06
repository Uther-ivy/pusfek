# -*- coding: utf-8 -*-
import datetime
import json
import random
import re
import time
import pymysql
import requests
from redis import StrictRedis
from scrapy import Selector
import ssl
import tool
from save_database import save_db
from proxies import proxise
pro = proxise()

ssl._create_default_https_context = ssl._create_unverified_context
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
}

# city_list
def get_nativeplace(addr):
    city = ''
    # 某省/自治区所有的地级市县
    city_list = [['9000', '湖北省'], ['9001', '武汉市'], ['9001.001', '江岸区'], ['9001.01', '蔡甸区'], ['9001.011', '江夏区'],
                 ['9001.012', '黄陂区'], ['9001.013', '新洲区'], ['9001.002', '江汉区'], ['9001.003', '乔口区'],
                 ['9001.004', '汉阳区'], ['9001.005', '武昌区'], ['9001.006', '青山区'], ['9001.007', '洪山区'],
                 ['9001.008', '东西湖区'], ['9001.009', '汉南区'], ['9002', '黄石市'], ['9002.001', '黄石港区'], ['9002.002', '西塞山区'],
                 ['9002.003', '下陆区'], ['9002.004', '铁山区'], ['9002.005', '阳新县'], ['9002.006', '大冶市'], ['9003', '十堰市'],
                 ['9003.001', '茅箭区'], ['9003.002', '张湾区'], ['9003.003', '郧　县'], ['9003.004', '郧西县'],
                 ['9003.005', '竹山县'], ['9003.006', '竹溪县'], ['9003.007', '房　县'], ['9003.008', '丹江口市'], ['9004', '宜昌市'],
                 ['9004.001', '西陵区'], ['9004.01', '五峰土家族自治县'], ['9004.011', '宜都市'], ['9004.012', '当阳市'],
                 ['9004.013', '枝江市'], ['9004.002', '伍家岗区'], ['9004.003', '点军区'], ['9004.004', '?亭区'],
                 ['9004.005', '夷陵区'], ['9004.006', '远安县'], ['9004.007', '兴山县'], ['9004.008', '秭归县'],
                 ['9004.009', '长阳土家族自治县'], ['9005', '襄樊市'], ['9005.001', '襄城区'], ['9005.002', '樊城区'],
                 ['9005.003', '襄阳区'], ['9005.004', '南漳县'], ['9005.005', '谷城县'], ['9005.006', '保康县'],
                 ['9005.007', '老河口市'], ['9005.008', '枣阳市'], ['9005.009', '宜城市'], ['9006', '鄂州市'], ['9006.001', '梁子湖区'],
                 ['9006.002', '华容区'], ['9006.003', '鄂城区'], ['9007', '荆门市'], ['9007.001', '钟祥市'], ['9007.002', '沙洋县'],
                 ['9007.003', '京山县'], ['9007.004', '掇刀区'], ['9007.005', '东宝区'], ['9008', '孝感市'], ['9008.001', '安陆市'],
                 ['9008.002', '应城市'], ['9008.003', '云梦县'], ['9008.004', '大悟县'], ['9008.005', '孝昌县'],
                 ['9008.006', '孝南区'], ['9008.007', '汉川市'], ['9009', '荆州市'], ['9009.001', '沙市区'], ['9009.002', '荆州区'],
                 ['9009.003', '公安县'], ['9009.004', '监利县'], ['9009.005', '江陵县'], ['9009.006', '石首市'],
                 ['9009.007', '洪湖市'], ['9009.008', '松滋市'], ['9010', '黄冈市'], ['9010.001', '州区'], ['9010.01', '武穴市'],
                 ['9010.002', '团风县'], ['9010.003', '红安县'], ['9010.004', '罗田县'], ['9010.005', '英山县'],
                 ['9010.006', '浠水县'], ['9010.007', '蕲春县'], ['9010.008', '黄梅县'], ['9010.009', '麻城市'], ['9011', '咸宁市'],
                 ['9011.001', '咸安区'], ['9011.002', '嘉鱼县'], ['9011.003', '通城县'], ['9011.004', '崇阳县'],
                 ['9011.005', '通山县'], ['9011.006', '赤壁市'], ['9012', '随州市'], ['9012.001', '曾都区'], ['9012.002', '广水市'],
                 ['9013', '恩施土家族苗族自治州'], ['9013.001', '恩施市'], ['9013.002', '利川市'], ['9013.003', '建始县'],
                 ['9013.004', '巴东县'], ['9013.005', '宣恩县'], ['9013.006', '咸丰县'], ['9013.007', '来凤县'],
                 ['9013.008', '鹤峰县'], ['9014', '省直辖行政单位'], ['9014.001', '仙桃市'], ['9014.002', '潜江市'],
                 ['9014.003', '天门市'], ['9014.004', '神农架林区']]
    for i in city_list:
        if i[1] in addr:
            city = float(i[0])
            break
    if city == '':
        city = 9010
    return city


def get_info(infourl,title,zhao_time):
    resp = requests.get(infourl, headers=headers,proxies=pro,timeout=20)
    resp.encoding = resp.apparent_encoding
    sel = Selector(resp)
    item = {}
    item['zhao_time'] = zhao_time
    item['title'] = title
    item['info_url'] = infourl
    item['body'] = sel.xpath('//div').extract_first()
    item['detail'] = item['body'].replace('\n', '').replace("\t", '').replace("\r", '').replace('\xa0', '').replace('\xc2','').replace(' ', '')
    item['senddate'] = int(time.time())
    item['mid'] = 1403
    item['email'] = ''
    item['resource'] = '黄冈市公共资源交易中心'
    item['typeid'] = tool.get_typeid(title)
    list = re.findall('width="(.*?)"', item['body'])
    for i in list:
        item['body'] = item['body'].replace('width="{}"'.format(i), '')
    item['endtime'] = tool.get_endtime(item['detail'])
    if item['endtime'] == '':
        item['endtime'] = int(time.mktime(time.strptime(zhao_time, "%Y-%m-%d")))
    else:
        try:
            item['endtime'] = int(time.mktime(time.strptime(item['endtime'], "%Y-%m-%d")))
        except:
            item['endtime'] = int(time.mktime(time.strptime(zhao_time, "%Y-%m-%d")))
    item['nativeplace'] = get_nativeplace(title + item['detail'])
    item['infotype'] = tool.get_infotype(title)
    item['shi'] = int(item['nativeplace'])  # 4502
    item['sheng'] = 9000
    item['email'] = ''
    item['tel'] = tool.get_tel(item['detail'])
    item['address'] = tool.get_address(item['detail'])
    item['linkman'] = tool.get_linkman(item['detail'])
    item['function'] = tool.get_function(item['detail'])  # detail["projectBudget"]
    item['click'] = random.randint(500, 1000)
    save_db(item)

def get_find_info(zhao_url,title):
    resp = requests.get(zhao_url, headers=headers,proxies=pro,timeout=20)
    resp.encoding = "gbk"
    sel = Selector(resp)
    info_urls = "http://www.hgggzy.com" + sel.xpath('//*[@id="frmBestwordHtml"]/@src').extract_first()
    now_time = tool.date
    # now_time = '2021-07-20'
    if sel.xpath('//*[@id="lblWriteDate"]/text()').extract_first() != None:
        zhao_time = sel.xpath('//*[@id="lblWriteDate"]/text()').extract_first()
    else:
        try:
            zhao_time = sel.xpath('//*[@id="lbltbbmwzksjsdate"]/text()').extract_first().split(" ")[0]
        except:
            zhao_time = sel.xpath('//*[@id="lblZbgsWzDate"]/text()').extract_first().split("至")[0]
    if tool.Transformation(now_time) <= tool.Transformation(zhao_time):
        resp1 = requests.get(info_urls, headers=headers)
        resp1.encoding="gbk"
        sel1 = Selector(resp1)
        infourl = sel1.xpath('//script/text()').extract_first().replace("location.href='..","http://www.hgggzy.com").replace("';","")
        print(infourl)
        print("==========================")
        get_info(infourl,title,zhao_time)
    else:
        print(zhao_time)

def get_zhaobiao_urls(url):
    resp = requests.get(url,headers=headers,proxies=pro,timeout=20)
    resp.encoding="gbk"
    sel = Selector(resp)
    zhaobiaourls = sel.xpath('//*[@class="myGVClass "]/tr')
    for zhaobiao_url in zhaobiaourls:
        try:
            title = zhaobiao_url.xpath('./td[2]/a/text()').extract_first()
            if title != None:
                title = title.replace(' ','')
                zhao_url = zhaobiao_url.xpath('./td[2]/a/@href').extract_first()
                if zhao_url != None:
                    if "[查看公告]"or "[查看结果]" in title:
                        zhaourl = "http://www.hgggzy.com/ceinwz/" + zhao_url
                        try:
                            # print(zhaourl + ",=======zhaobiao_urls")
                            get_find_info(zhaourl,title)
                        except Exception as e:
                            print(e)
                            print(zhaourl)
                            get_find_info1(zhaourl,title)
        except Exception as e:
            print(e)
            print(zhaobiao_url)
            continue


def get_find_info1(zhaourl,title):
    resp = requests.get(zhaourl, headers=headers,proxies=pro,timeout=20)
    resp.encoding = "gbk"
    sel = Selector(resp)
    zhao_time = sel.xpath('//*[@id="ctl00_ContentPlaceHolder1_TimeLabel"]/text()').extract_first()
    now_time = tool.date
    list2 = []
    if tool.Transformation(now_time) <= tool.Transformation(zhao_time):
        item = {}
        item['zhao_time'] = zhao_time
        item['title'] = title
        item['info_url'] = zhaourl
        # print("get_find_info1,url: " + zhaourl)
        item['body'] = sel.xpath('//div[@class="newsImage"]/table/tr').extract_first()
        item['detail'] = item['body'].replace('\n', '').replace("\t", '').replace("\r", '').replace('\xa0', '').replace('\xc2','').replace(' ', '')
        item['senddate'] = int(time.time())
        item['mid'] = 1403
        item['resource'] = '黄冈市公共资源交易中心'
        item['typeid'] = tool.get_typeid(title)
        list = re.findall('width:"(.*?)"', item['body'])
        for i in list:
            item['body'] = item['body'].replace('width="{}"'.format(i), '')
        item['endtime'] = tool.get_endtime(item['detail'])
        if item['endtime'] == '':
            item['endtime'] = int(time.mktime(time.strptime(zhao_time, "%Y-%m-%d")))
        else:
            try:
                item['endtime'] = int(time.mktime(time.strptime(item['endtime'], "%Y-%m-%d")))
            except:
                item['endtime'] = int(time.mktime(time.strptime(zhao_time, "%Y-%m-%d")))
        item['nativeplace'] = get_nativeplace(title + item['detail'])
        item['infotype'] = tool.get_infotype(title)
        item['shi'] = int(item['nativeplace'])  # 4502
        item['sheng'] = 9000
        item['email'] = ''
        item['tel'] = tool.get_tel(item['detail'])
        item['address'] = tool.get_address(item['detail'])
        item['linkman'] = tool.get_linkman(item['detail'])
        item['function'] = tool.get_function(item['detail'])  # detail["projectBudget"]
        item['click'] = random.randint(500, 1000)
        save_db(item)

if __name__ == '__main__':
    import traceback, os
    try:
        url_list = [
            "http://www.hgggzy.com/ceinwz/WebInfo_List.aspx?&newsid=700&jsgc=0100000&zbdl=1&FromUrl=jygg",
            "http://www.hgggzy.com/ceinwz/WebInfo_List.aspx?&newsid=400&zfcg=0100000&FromUrl=jygg",
            "http://www.hgggzy.com/ceinwz/WebInfo_List.aspx?&newsid=701&jsgc=0000010&FromUrl=zbgs",
            "http://www.hgggzy.com/ceinwz/WebInfo_List.aspx?&newsid=401&zfcg=0000010&FromUrl=jygg&FromUrl=jygg&FromUrl=zbgs",
        ]
        for url in url_list:
            get_zhaobiao_urls(url)
    except Exception as e:
        traceback.print_exc()
        # tool.send_error('报错文件：'+str(os.path.basename(__file__))+'报错信息：'+str(e))
