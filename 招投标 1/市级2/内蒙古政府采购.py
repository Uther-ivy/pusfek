# -*- coding: utf-8 -*-
import datetime
import json
import random
import re
import time

import pymysql
import requests
from scrapy import Selector
from redis import StrictRedis
import ssl
import tool
from save_database import save_db
from proxies import proxise
pro = proxise()

ssl._create_default_https_context = ssl._create_unverified_context
headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Host': 'www.ccgp-neimenggu.gov.cn',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
}

def get_nativeplace(place):
    city = ''
    citys = [['3000','内蒙古自治区'],['3001','呼和浩特市'],['3001.001','新城区'],['3001.002','回民区'],['3001.003','玉泉区'],['3001.004','赛罕区'],['3001.005','土默特左旗'],['3001.006','托克托县'],['3001.007','和林格尔县'],['3001.008','清水河县'],['3001.009','武川县'],['3002','包头市'],['3002.001','东河区'],['3002.002','昆都仑区'],['3002.003','青山区'],['3002.004','石拐区'],['3002.005','白云矿区'],['3002.006','九原区'],['3002.007','土默特右旗'],['3002.008','固阳县'],['3002.009','达尔罕茂明安联合旗'],['3003','乌海市'],['3003.001','海勃湾区'],['3003.002','海南区'],['3003.003','乌达区'],['3004','赤峰市'],['3004.001','红山区'],['3004.01','喀喇沁旗'],['3004.011','宁城县'],['3004.012','敖汉旗'],['3004.002','元宝山区'],['3004.003','松山区'],['3004.004','阿鲁科尔沁旗'],['3004.005','巴林左旗'],['3004.006','巴林右旗'],['3004.007','林西县'],['3004.008','克什克腾旗'],['3004.009','翁牛特旗'],['3005','通辽市'],['3005.001','科尔沁区'],['3005.002','科尔沁左翼中旗'],['3005.003','科尔沁左翼后旗'],['3005.004','开鲁县'],['3005.005','库伦旗'],['3005.006','奈曼旗'],['3005.007','扎鲁特旗'],['3005.008','霍林郭勒市'],['3006','鄂尔多斯市'],['3006.001','东胜区'],['3006.002','达拉特旗'],['3006.003','准格尔旗'],['3006.004','鄂托克前旗'],['3006.005','鄂托克旗'],['3006.006','杭锦旗'],['3006.007','乌审旗'],['3006.008','伊金霍洛旗'],['3007','呼伦贝尔市'],['3007.001','海拉尔区'],['3007.01','牙克石市'],['3007.011','扎兰屯市'],['3007.012','额尔古纳市'],['3007.013','根河市'],['3007.002','阿荣旗'],['3007.003','莫力达瓦达斡尔族自治旗'],['3007.004','鄂伦春自治旗'],['3007.005','鄂温克族自治旗'],['3007.006','陈巴尔虎旗'],['3007.007','新巴尔虎左旗'],['3007.008','新巴尔虎右旗'],['3007.009','满洲里市'],['3008','巴彦淖尔市'],['3008.001','临河区'],['3008.002','五原县'],['3008.003','磴口县'],['3008.004','乌拉特前旗'],['3008.005','乌拉特中旗'],['3008.006','乌拉特后旗'],['3008.007','杭锦后旗'],['3009','乌兰察布市'],['3009.001','集宁区'],['3009.01','四子王旗'],['3009.011','丰镇市'],['3009.002','卓资县'],['3009.003','化德县'],['3009.004','商都县'],['3009.005','兴和县'],['3009.006','凉城县'],['3009.007','察哈尔右翼前旗'],['3009.008','察哈尔右翼中旗'],['3009.009','察哈尔右翼后旗'],['3010','兴安盟'],['3010.001','乌兰浩特市'],['3010.002','阿尔山市'],['3010.003','科尔沁右翼前旗'],['3010.004','科尔沁右翼中旗'],['3010.005','扎赉特旗'],['3010.006','突泉县'],['3011','锡林郭勒盟'],['3011.001','二连浩特市'],['3011.01','正镶白旗'],['3011.011','正蓝旗'],['3011.012','多伦县'],['3011.002','锡林浩特市'],['3011.003','阿巴嘎旗'],['3011.004','苏尼特左旗'],['3011.005','苏尼特右旗'],['3011.006','东乌珠穆沁旗'],['3011.007','西乌珠穆沁旗'],['3011.008','太仆寺旗'],['3011.009','镶黄旗'],['3012','阿拉善盟'],['3012.001','阿拉善左旗'],['3012.002','阿拉善右旗'],['3012.003','额济纳旗']]
    for i in citys:
        if i[1] in place:
            city = float(i[0])
            break
    if city == '':
        city = 3000
    return city

def get_zhaobiaoinfo(infourl,title,data):
    print(infourl)
    time.sleep(2)
    resp = requests.get(infourl, headers=headers,proxies=pro,timeout=20)
    resp.encoding = "utf-8"
    sel = Selector(resp)
    item = {}
    item['zhao_time'] = data
    item['title'] = title
    item['info_url'] = infourl
    item['body'] = sel.xpath('//*[@id="center"]').extract_first()
    item['detail'] = item['body'].replace('\n', '').replace("\t", '').replace("\r", '').replace('\xa0', '').replace('\xc2', '').replace(' ', '')
    item['senddate'] = int(time.time())
    item['mid'] = 1403
    item['resource'] = '内蒙古政府采购'
    item['typeid'] = tool.get_typeid(title)
    list = re.findall('width:"(.*?)"', item['body'])
    for i in list:
        item['body'] = item['body'].replace('width:"{}"'.format(i), '')
    item['endtime'] = tool.get_endtime(item['detail'])
    if item['endtime'] == '':
        item['endtime'] = int(time.mktime(time.strptime(item['zhao_time'], "%Y-%m-%d")))
    else:
        try:
            item['endtime'] = int(time.mktime(time.strptime(item['endtime'], "%Y-%m-%d")))
        except:
            item['endtime'] = int(time.mktime(time.strptime(item['zhao_time'], "%Y-%m-%d")))
    item['nativeplace'] = get_nativeplace(title + item['detail'])
    item['infotype'] = tool.get_infotype(title)
    item['shi'] = int(item['nativeplace'])  # 4502
    item['sheng'] = 3000
    item['email'] = ''
    item['tel'] = tool.get_tel(item['detail'])
    item['address'] = tool.get_address(item['detail'])
    item['linkman'] = tool.get_linkman(item['detail'])
    item['function'] = tool.get_function(item['detail'])  # detail["projectBudget"]
    item['click'] = random.randint(500, 1000)
    save_db(item)

def get_project(url):
    for a in range(1,4):
        for i in range(1,8):
            data = {
                'type_name': str(i),
                'annstartdate_S': '',
                'annstartdate_E': '',
                'byf_page': str(a),
                'fun': 'cggg',
                'page_size': '18',
                }
            resp = tool.requests_post_(url, data, headers)
            print(resp.text)
            results = json.loads(resp.text)
            project_info = results[0]
            for pro_info in project_info:
                now_time = tool.date
                zhaobiao_time = pro_info['SUBDATE'].split("：")[1].replace("]", "")
                if zhaobiao_time >= now_time:
                    info_url = "http://www.ccgp-neimenggu.gov.cn/category/cgggg?tb_id=" + pro_info['ay_table_tag'] + "&p_id=" + pro_info['wp_mark_id'] + "&type=" + pro_info['type']
                    title = pro_info['TITLE'].replace(' ','')
                    # print(info_url,title,data)
                    try:
                        get_zhaobiaoinfo(info_url,title,zhaobiao_time)
                    except Exception as e:
                        print(e)
                        continue
                else:
                    print('日期不符', zhaobiao_time)
                    break

if __name__ == '__main__':
    url = "https://www.ccgp-neimenggu.gov.cn/zfcgwslave/web/index.php?r=pro%2Fanndata"
    requests.adapters.DEFAULT_RETRIES = 5  # 增加重连次数
    s = requests.session()
    s.keep_alive = False  # 关闭多余连接
    requests.packages.urllib3.disable_warnings()
    try:
        get_project(url)
    except:
        import traceback
        traceback.print_exc()
