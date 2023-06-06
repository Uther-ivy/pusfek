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
    citys = [['12500','贵州省'],['12501','贵阳市'],['12501.001','南明区'],['12501.01','清镇市'],['12501.002','云岩区'],['12501.003','花溪区'],['12501.004','乌当区'],['12501.005','白云区'],['12501.006','小河区'],['12501.007','开阳县'],['12501.008','息烽县'],['12501.009','修文县'],['12502','六盘水市'],['12502.001','钟山区'],['12502.002','六枝特区'],['12502.003','水城县'],['12502.004','盘　县'],['12503','遵义市'],['12503.001','红花岗区'],['12503.01','湄潭县'],['12503.011','余庆县'],['12503.012','习水县'],['12503.013','赤水市'],['12503.014','仁怀市'],['12503.002','汇川区'],['12503.003','遵义县'],['12503.004','桐梓县'],['12503.005','绥阳县'],['12503.006','正安县'],['12503.007','道真仡佬族苗族自治县'],['12503.008','务川仡佬族苗族自治县'],['12503.009','凤冈县'],['12504','安顺市'],['12504.001','西秀区'],['12504.002','平坝县'],['12504.003','普定县'],['12504.004','镇宁布依族苗族自治县'],['12504.005','关岭布依族苗族自治县'],['12504.006','紫云苗族布依族自治县'],['12505','铜仁地区'],['12505.001','铜仁市'],['12505.01','万山特区'],['12505.002','江口县'],['12505.003','玉屏侗族自治县'],['12505.004','石阡县'],['12505.005','思南县'],['12505.006','印江土家族苗族自治县'],['12505.007','德江县'],['12505.008','沿河土家族自治县'],['12505.009','松桃苗族自治县'],['12506','黔西南布依族苗族自治州'],['12506.001','兴义市'],['12506.002','兴仁县'],['12506.003','普安县'],['12506.004','晴隆县'],['12506.005','贞丰县'],['12506.006','望谟县'],['12506.007','册亨县'],['12506.008','安龙县'],['12507','毕节地区'],['12507.001','毕节市'],['12507.002','大方县'],['12507.003','黔西县'],['12507.004','金沙县'],['12507.005','织金县'],['12507.006','纳雍县'],['12507.007','威宁彝族回族苗族自治县'],['12507.008','赫章县'],['12508','黔东南苗族侗族自治州'],['12508.001','凯里市'],['12508.01','台江县'],['12508.011','黎平县'],['12508.012','榕江县'],['12508.013','从江县'],['12508.014','雷山县'],['12508.015','麻江县'],['12508.002','黄平县'],['12508.003','施秉县'],['12508.004','三穗县'],['12508.005','镇远县'],['12508.006','岑巩县'],['12508.007','天柱县'],['12508.008','锦屏县'],['12508.009','剑河县'],['12509','黔南布依族苗族自治州'],['12509.001','都匀市'],['12509.01','龙里县'],['12509.011','惠水县'],['12509.012','三都水族自治县'],['12509.002','福泉市'],['12509.003','荔波县'],['12509.004','贵定县'],['12509.005','瓮安县'],['12509.006','独山县'],['12509.007','平塘县'],['12509.008','罗甸县'],['12509.009','长顺县']]
    for i in citys:
        if i[1] in place:
            city = float(i[0])
            break
    if city == '':
        city = 12500
    return city

def get_zhaobiaoinfo(infourl, title, zhaotime, cont):
    item = {}
    item['zhao_time'] = zhaotime
    item['title'] = title
    item['info_url'] = infourl
    item['body'] = cont
    item['detail'] = ''.join(re.findall('>(.*?)<', cont)).replace('\n', '').replace("\t", '').replace("\r", '').replace('\xa0', '').replace('\xc2', '').replace(' ', '')
    item['senddate'] = int(time.time())
    item['mid'] = 1403
    item['typeid'] = tool.get_typeid(title)
    list = re.findall('width="(.*?)"', item['body'])
    for i in list:
        item['body'] = item['body'].replace('width="{}"'.format(i), '')
    item['endtime'] = tool.get_endtime(item['detail'])
    if item['endtime'] == '':
        item['endtime'] = int(time.mktime(time.strptime(zhaotime, "%Y-%m-%d")))
    else:
        try:
            item['endtime'] = int(time.mktime(time.strptime(item['endtime'], "%Y-%m-%d")))
        except:
            item['endtime'] = int(time.mktime(time.strptime(zhaotime, "%Y-%m-%d")))
    item['nativeplace'] = get_nativeplace(title + item['detail'])
    item['infotype'] = tool.get_infotype(title)
    item['shi'] = int(item['nativeplace'])  # 4502
    item['sheng'] = 12500
    item['email'] = ''
    item['tel'] = tool.get_tel(item['detail'])
    item['address'] = tool.get_address(item['detail'])
    item['linkman'] = tool.get_linkman(item['detail'])
    item['function'] = tool.get_function(item['detail'])  # detail["projectBudget"]
    item['click'] = random.randint(500, 1000)
    item['resource'] = "贵州省公共资源交易云"
    time.sleep(2)
    save_db(item)

def get_project(url):
    now_time = tool.date
    resp = requests.get(url,headers=headers,proxies=pro,timeout=20)
    resp.encoding="utf8"
    data = json.loads(resp.text)
    data = data['page']['content']
    for da in data:
        title = da['docTitle'].replace(' ','')
        zhaotime = da['docRelTime'][:10]
        infourl = 'http://ggzy.guizhou.gov.cn/jyxx/view.html?meteIds=' + da['MetaDataId']
        cont = da['docContent']
        # print(title,zhao_time,infourl)
        if zhaotime == now_time:
            get_zhaobiaoinfo(infourl, title, zhaotime, cont)
        else:
            print('日期不符', zhaotime)

if __name__ == '__main__':
    urls = "http://ggzy.guizhou.gov.cn/igs/front/search/list.html?pageNumber={}&pageSize=10&siteId=500483&index=trades&type=infomation_v6&filter%5BchannelId%5D=5376927%2C5377100%2C5377337%2C5377101%2C5377103%2C5377338%2C5237520%2C5237521%2C5617491%2C5617492%2C5617493%2C5237523&orderProperty=docRelTime&orderDirection=desc&isPage=true"

    requests.adapters.DEFAULT_RETRIES = 5  # 增加重连次数
    s = requests.session()
    s.keep_alive = False  # 关闭多余连接
    requests.packages.urllib3.disable_warnings()
    for page in range(1, 5):
        get_project(urls.format(page))
