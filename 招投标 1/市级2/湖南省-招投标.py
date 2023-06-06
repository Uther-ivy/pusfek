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

def get_nativeplace(place):
    city = ''
    citys = [['9500','湖南省'],['9501','长沙市'],['9501.001','芙蓉区'],['9501.002','天心区'],['9501.003','岳麓区'],['9501.004','开福区'],['9501.005','雨花区'],['9501.006','长沙县'],['9501.007','望城县'],['9501.008','宁乡县'],['9501.009','浏阳市'],['9502','株洲市'],['9502.001','荷塘区'],['9502.002','芦淞区'],['9502.003','石峰区'],['9502.004','天元区'],['9502.005','株洲县'],['9502.006','攸　县'],['9502.007','茶陵县'],['9502.008','炎陵县'],['9502.009','醴陵市'],['9503','湘潭市'],['9503.001','雨湖区'],['9503.002','岳塘区'],['9503.003','湘潭县'],['9503.004','湘乡市'],['9503.005','韶山市'],['9504','衡阳市'],['9504.001','珠晖区'],['9504.01','祁东县'],['9504.011','耒阳市'],['9504.012','常宁市'],['9504.002','雁峰区'],['9504.003','石鼓区'],['9504.004','蒸湘区'],['9504.005','南岳区'],['9504.006','衡阳县'],['9504.007','衡南县'],['9504.008','衡山县'],['9504.009','衡东县'],['9505','邵阳市'],['9505.001','双清区'],['9505.01','新宁县'],['9505.011','城步苗族自治县'],['9505.012','武冈市'],['9505.002','大祥区'],['9505.003','北塔区'],['9505.004','邵东县'],['9505.005','新邵县'],['9505.006','邵阳县'],['9505.007','隆回县'],['9505.008','洞口县'],['9505.009','绥宁县'],['9506','岳阳市'],['9506.001','岳阳楼区'],['9506.002','云溪区'],['9506.003','君山区'],['9506.004','岳阳县'],['9506.005','华容县'],['9506.006','湘阴县'],['9506.007','平江县'],['9506.008','汨罗市'],['9506.009','临湘市'],['9507','常德市'],['9507.001','武陵区'],['9507.002','鼎城区'],['9507.003','安乡县'],['9507.004','汉寿县'],['9507.005','澧　县'],['9507.006','临澧县'],['9507.007','桃源县'],['9507.008','石门县'],['9507.009','津市市'],['9508','张家界市'],['9508.001','永定区'],['9508.002','武陵源区'],['9508.003','慈利县'],['9508.004','桑植县'],['9509','益阳市'],['9509.001','资阳区'],['9509.002','赫山区'],['9509.003','南　县'],['9509.004','桃江县'],['9509.005','安化县'],['9509.006','沅江市'],['9510','郴州市'],['9510.001','北湖区'],['9510.01','安仁县'],['9510.011','资兴市'],['9510.002','苏仙区'],['9510.003','桂阳县'],['9510.004','宜章县'],['9510.005','永兴县'],['9510.006','嘉禾县'],['9510.007','临武县'],['9510.008','汝城县'],['9510.009','桂东县'],['9511','永州市'],['9511.001','芝山区'],['9511.01','新田县'],['9511.011','江华瑶族自治县'],['9511.002','冷水滩区'],['9511.003','祁阳县'],['9511.004','东安县'],['9511.005','双牌县'],['9511.006','道　县'],['9511.007','江永县'],['9511.008','宁远县'],['9511.009','蓝山县'],['9512','怀化市'],['9512.001','鹤城区'],['9512.01','靖州苗族侗族自治县'],['9512.011','通道侗族自治县'],['9512.012','洪江市'],['9512.002','中方县'],['9512.003','沅陵县'],['9512.004','辰溪县'],['9512.005','溆浦县'],['9512.006','会同县'],['9512.007','麻阳苗族自治县'],['9512.008','新晃侗族自治县'],['9512.009','芷江侗族自治县'],['9513','娄底市'],['9513.001','娄星区'],['9513.002','双峰县'],['9513.003','新化县'],['9513.004','冷水江市'],['9513.005','涟源市'],['9514','湘西土家族苗族自治州'],['9514.001','吉首市'],['9514.002','泸溪县'],['9514.003','凤凰县'],['9514.004','花垣县'],['9514.005','保靖县'],['9514.006','古丈县'],['9514.007','永顺县'],['9514.008','龙山县']]
    for i in citys:
        if i[1] in place:
            city = float(i[0])
            break
    if city == '':
        city = 9500
    return city

def get_zhaobiaoinfo(infourl,title,data,pdfpath):
    print(infourl)
    item = {}
    item['zhao_time'] = data
    item['title'] = title
    item['info_url'] = infourl
    item['body'] = '<embed width="100%" height="100%"  src="http://218.76.24.90/ztbPdf/' + pdfpath + '"></embed>'
    item['detail'] = item['body'].replace('\n', '').replace("\t", '').replace("\r", '').replace('\xa0', '').replace('\xc2', '').replace(' ', '')
    item['senddate'] = int(time.time())
    item['mid'] = 1403
    item['resource'] = '湖南省招标投标监管网'
    item['typeid'] = tool.get_typeid(title)
    list = re.findall('width:"(.*?)"', item['body'])
    for i in list:
        item['body'] = item['body'].replace('width:"{}"'.format(i), '')
    item['endtime'] = tool.get_endtime(item['detail'])
    if item['endtime'] == '':
        item['endtime'] = int(time.mktime(time.strptime(data, "%Y-%m-%d")))
    else:
        try:
            item['endtime'] = int(time.mktime(time.strptime(item['endtime'], "%Y-%m-%d")))
        except:
            item['endtime'] = int(time.mktime(time.strptime(data, "%Y-%m-%d")))
    item['nativeplace'] = get_nativeplace(title + item['detail'])
    item['infotype'] = tool.get_infotype(title)
    item['shi'] = int(item['nativeplace'])  # 4502
    item['sheng'] = 9500
    item['email'] = ''
    item['tel'] = tool.get_tel(item['detail'])
    item['address'] = tool.get_address(item['detail'])
    item['linkman'] = tool.get_linkman(item['detail'])
    item['function'] = tool.get_function(item['detail'])  # detail["projectBudget"]
    item['click'] = random.randint(500, 1000)
    save_db(item)

def get_project(url):
    resp = tool.requests_get(url, headers)
    results = json.loads(resp)
    project_info =results['page']['list']
    now_time = tool.date
    # now_time = '2021-08-02'
    print('-'*50, 1)
    for pro_info in project_info:
        if pro_info['publishDate'].split(" ")[0] == now_time:
            pdfpath = pro_info['pdfPath']
            title = pro_info['title'].replace(' ','')
            data = pro_info['publishDate'].split(" ")[0]
            infourl = "http://bidding.hunan.gov.cn/bidding/notice/{}?isdetail=1".format(pro_info['id'])
            time.sleep(2)
            get_zhaobiaoinfo(infourl,title,data,pdfpath)
        else:
            print(pro_info['publishDate'].split(" ")[0], '日期不符')
            break

if __name__ == '__main__':
    urls = ['http://218.76.24.90/ztb/ztbcms/getBiddingList?limit=10&page=1&categoryId=92&areaNo=',
            'http://218.76.24.90/ztb/ztbcms/getBiddingList?limit=10&page=1&categoryId=88&areaNo=',
            'http://218.76.24.90/ztb/ztbcms/getBiddingList?limit=10&page=1&categoryId=91&areaNo=',
            'http://218.76.24.90/ztb/ztbcms/getBiddingList?limit=10&page=1&categoryId=90&areaNo=',
            'http://218.76.24.90/ztb/ztbcms/getBiddingList?limit=10&page=1&categoryId=89&areaNo='
            ]
    requests.adapters.DEFAULT_RETRIES = 5  # 增加重连次数
    s = requests.session()
    s.keep_alive = False  # 关闭多余连接
    requests.packages.urllib3.disable_warnings()
    for url in urls:
        get_project(url)