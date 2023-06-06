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
    citys = [['10500','广西壮族自治区'],['10501','南宁市'],['10501.001','兴宁区'],['10501.01','上林县'],['10501.011','宾阳县'],['10501.012','横　县'],['10501.002','青秀区'],['10501.003','江南区'],['10501.004','西乡塘区'],['10501.005','良庆区'],['10501.006','邕宁区'],['10501.007','武鸣县'],['10501.008','隆安县'],['10501.009','马山县'],['10502','柳州市'],['10502.001','城中区'],['10502.01','三江侗族自治县'],['10502.002','鱼峰区'],['10502.003','柳南区'],['10502.004','柳北区'],['10502.005','柳江县'],['10502.006','柳城县'],['10502.007','鹿寨县'],['10502.008','融安县'],['10502.009','融水苗族自治县'],['10503','桂林市'],['10503.001','秀峰区'],['10503.01','兴安县'],['10503.011','永福县'],['10503.012','灌阳县'],['10503.013','龙胜各族自治县'],['10503.014','资源县'],['10503.015','平乐县'],['10503.016','荔蒲县'],['10503.017','恭城瑶族自治县'],['10503.002','叠彩区'],['10503.003','象山区'],['10503.004','七星区'],['10503.005','雁山区'],['10503.006','阳朔县'],['10503.007','临桂县'],['10503.008','灵川县'],['10503.009','全州县'],['10504','梧州市'],['10504.001','万秀区'],['10504.002','蝶山区'],['10504.003','长洲区'],['10504.004','苍梧县'],['10504.005','藤　县'],['10504.006','蒙山县'],['10504.007','岑溪市'],['10505','北海市'],['10505.001','海城区'],['10505.002','银海区'],['10505.003','铁山港区'],['10505.004','合浦县'],['10506','防城港市'],['10506.001','港口区'],['10506.002','防城区'],['10506.003','上思县'],['10506.004','东兴市'],['10507','钦州市'],['10507.001','钦南区'],['10507.002','钦北区'],['10507.003','灵山县'],['10507.004','浦北县'],['10508','贵港市'],['10508.001','港北区'],['10508.002','港南区'],['10508.003','覃塘区'],['10508.004','平南县'],['10508.005','桂平市'],['10509','玉林市'],['10509.001','玉州区'],['10509.002','容　县'],['10509.003','陆川县'],['10509.004','博白县'],['10509.005','兴业县'],['10509.006','北流市'],['10510','百色市'],['10510.001','右江区'],['10510.01','田林县'],['10510.011','西林县'],['10510.012','隆林各族自治县'],['10510.002','田阳县'],['10510.003','田东县'],['10510.004','平果县'],['10510.005','德保县'],['10510.006','靖西县'],['10510.007','那坡县'],['10510.008','凌云县'],['10510.009','乐业县'],['10511','贺州市'],['10511.001','八步区'],['10511.002','昭平县'],['10511.003','钟山县'],['10511.004','富川瑶族自治县'],['10512','河池市'],['10512.001','金城江区'],['10512.01','大化瑶族自治县'],['10512.011','宜州市'],['10512.002','南丹县'],['10512.003','天峨县'],['10512.004','凤山县'],['10512.005','东兰县'],['10512.006','罗城仫佬族自治县'],['10512.007','环江毛南族自治县'],['10512.008','巴马瑶族自治县'],['10512.009','都安瑶族自治县'],['10513','来宾市'],['10513.001','兴宾区'],['10513.002','忻城县'],['10513.003','象州县'],['10513.004','武宣县'],['10513.005','金秀瑶族自治县'],['10513.006','合山市'],['10514','崇左市'],['10514.001','江洲区'],['10514.002','扶绥县'],['10514.003','宁明县'],['10514.004','龙州县'],['10514.005','大新县'],['10514.006','天等县'],['10514.007','凭祥市']]
    for i in citys:
        if i[1] in place:
            city = float(i[0])
            break
    if city == '':
        city = 10500
    return city

def get_zhaobiaoinfo(infourl, title, zhaotime):
    resp = requests.get(infourl, headers=headers,proxies=pro,timeout=20)
    resp.encoding = "UTF-8"
    sel = Selector(resp)
    value = sel.xpath('//input[@name="articleDetail"]/@value').extract_first()
    data = json.loads(value)
    item = {}
    item['zhao_time'] = zhaotime
    item['title'] = title
    item['info_url'] = infourl
    item['body'] = data['content']
    item['detail'] = item['body'].replace('\n', '').replace("\t", '').replace("\r", '').replace('\xa0', '').replace('\xc2', '').replace(' ', '')
    item['senddate'] = int(time.time())
    item['mid'] = 1403
    item['typeid'] = tool.get_typeid(item['title'])
    list = re.findall('width="(.*?)"', item['body'])
    for i in list:
        item['body'] = item['body'].replace('width="{}"'.format(i), '')
    item['endtime'] = tool.get_endtime(item['detail'])
    if item['endtime'] == '':
        item['endtime'] = int(time.mktime(time.strptime(item['zhao_time'], "%Y-%m-%d")))
    else:
        try:
            item['endtime'] = int(time.mktime(time.strptime(item['endtime'], "%Y-%m-%d")))
        except:
            item['endtime'] = int(time.mktime(time.strptime(item['zhao_time'], "%Y-%m-%d")))
    item['nativeplace'] = get_nativeplace(item['title'] + item['detail'])
    item['infotype'] = tool.get_infotype(item['title'])
    item['shi'] = int(item['nativeplace'])  # 4502
    item['sheng'] = 10500
    item['email'] = ''
    item['tel'] = tool.get_tel(item['detail'])
    item['address'] = tool.get_address(item['detail'])
    item['linkman'] = tool.get_linkman(item['detail'])
    item['function'] = tool.get_function(item['detail'])  # detail["projectBudget"]
    item['click'] = random.randint(500, 1000)
    item['resource'] = "广西政府采购网"
    save_db(item)

def get_project(url):
    now_time = tool.date
    for i in range(1,3):
        for a in range(1,3):
            data = {
                'categoryCode': "ZcyAnnouncement{}".format(str(i)),
                'pageNo': str(a),
                'pageSize': '100' }
            resp = requests.post(url, json=data,headers=headers,proxies=pro,timeout=20)
            # print(resp.text)
            results = json.loads(resp.text)
            data = results['hits']['hits']
            for da in data:
                title = da['_source']['title'].replace(' ','')
                infourl = "http://www.ccgp-guangxi.gov.cn" + da['_source']['url']
                zhaotime = tool.get_time(da['_source']['publishDate'])
                # print(title,infourl,zhaotime)
                if zhaotime == now_time:
                    get_zhaobiaoinfo(infourl, title, zhaotime)

if __name__ == '__main__':
    url = "http://www.ccgp-guangxi.gov.cn/front/search/category"
    requests.adapters.DEFAULT_RETRIES = 5  # 增加重连次数
    s = requests.session()
    s.keep_alive = False  # 关闭多余连接
    requests.packages.urllib3.disable_warnings()
    get_project(url)
