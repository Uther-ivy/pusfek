# -*- coding: utf-8 -*-
import datetime
import random
import re
import time
import requests
from scrapy import Selector
import json
import ssl
import tool
from save_database import save_db
from proxiesssss import proxise
pro = proxise

ssl._create_default_https_context = ssl._create_unverified_context
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
}

def get_zhaobiao_info(title,zhao_time,info_url):
    time.sleep(2)
    resp = tool.requests_(info_url, headers)
    resp.encoding = "utf8"
    sel = Selector(resp)
    item = {}
    item['zhao_time'] = zhao_time
    item['title'] = title
    item['info_url'] = info_url
    item['body'] = tool.qudiao_width(re.findall('<div class="cont_line">[\S\s]*?<div class="cont_line">',resp.text)[0])
    item['detail'] = item['body'].replace('\n', '').replace("\t", '').replace("\r", '').replace('\xa0', '').replace('\xc2', '').replace(' ', '')
    item['senddate'] = int(time.time())
    item['mid'] = 1403
    item['typeid'] = tool.get_typeid(item['title'])
    item['endtime'] = tool.get_endtime(item['detail'])
    if item['endtime'] == '':
        item['endtime'] = int(time.mktime(time.strptime(item['zhao_time'], "%Y-%m-%d")))
    else:
        try:
            item['endtime'] = int(time.mktime(time.strptime(item['endtime'], "%Y-%m-%d")))
        except:
            item['endtime'] = int(time.mktime(time.strptime(item['zhao_time'], "%Y-%m-%d")))
    item['nativeplace'] = tool.get_title_city(item['title'])
    if item['nativeplace'] == 0:
        item['nativeplace'] = tool.more(item['title']+ item['detail'])
    item['infotype'] = tool.get_infotype(item['title'])
    item['shi'] = int(str(item['nativeplace']).split('.')[0])
    item['sheng'] = tool.get_sheng(item['title'])
    if len(str(item['shi'])) == 4:
        item['sheng'] = str(item['shi'])[:2] + '00'
    elif len(str(item['shi'])) == 5:
        item['sheng'] = str(item['shi'])[:3] + '00'
    item['email'] = ''
    item['tel'] = tool.get_tel(item['detail'])
    item['address'] = tool.get_address(item['detail'])
    item['linkman'] = tool.get_linkman(item['detail'])
    item['function'] = tool.get_function(item['detail'])  # detail["projectBudget"]
    item['click'] = random.randint(500, 1000)
    item['resource'] = "东方电器集中采购管理平台"
    save_db(item)

def get_project(url):
    resp = tool.requests_(url, headers)
    resp.encoding='uft8'
    data = json.loads(resp.text)
    print(data)
    now_time = tool.date
    for da in data['result']['record']:
        title = da['bid_project_name']
        zhao_time = da['creation_date'].split(" ")[0]
        bulletin_type = da['bulletin_type']
        try:
            template_type = da['template_type']
        except:
            continue
        id = str(da['tplt_blt_id'])
        if bulletin_type == 'ZBGG':
            if template_type == 'YQZBGG':
                info_url = 'http://srm.dongfang.com/modules/blt/BLT1030/bid_invite_bulletin_view.screen?tplt_blt_id=' + id
            else:
                info_url = 'http://srm.dongfang.com/modules/blt/BLT1030/bid_tplt_bulletin_view.screen?tplt_blt_id=' + id
        elif bulletin_type == 'YSGG':
            info_url = 'http://srm.dongfang.com/modules/blt/BLT1061/bid_tplt_audit_bulletin_view.screen?tplt_blt_id=' + id
        elif bulletin_type == 'ZHBGG':
            info_url = 'http://srm.dongfang.com/modules/blt/BLT1060/bid_tplt_bidding_bulletin_view.screen?tplt_blt_id=' + id
        elif bulletin_type == 'YSGG':
            info_url = 'http://srm.dongfang.com/modules/blt/BLT1061/bid_tplt_audit_bulletin_view.screen?tplt_blt_id=' + id
        elif bulletin_type == 'QTGG(ZB)':
            if template_type == 'LBGGMB':
                info_url = 'http://srm.dongfang.com/modules/blt/BLT1062/bid_tplt_failure_bidding_bulletin_view.screen?tplt_blt_id=' + id
            elif template_type == 'LPGGMB':
                info_url = 'http://srm.dongfang.com/modules/blt/BLT1051/bid_tplt_reserveprice_view.screen?tplt_blt_id=' + id
            elif template_type == 'CJGGMB':
                info_url = 'http://srm.dongfang.com/modules/blt/BLT1050/bid_tplt_turnover_view.screen?tplt_blt_id=' + id
            elif template_type == 'YQZBGG':
                info_url = 'http://srm.dongfang.com/modules/blt/BLT1030/bid_invite_bulletin_view.screen?tplt_blt_id=' + id
        elif bulletin_type == 'QTGG(JJ)':
            if template_type == 'LBGGMB':
                info_url = 'http://srm.dongfang.com/modules/blt/BLT1062/bid_tplt_failure_bidding_bulletin_view.screen?tplt_blt_id=' + id
            elif template_type == 'LPGGMB':
                info_url = 'http://srm.dongfang.com/modules/blt/BLT1051/bid_tplt_reserveprice_view.screen?tplt_blt_id=' + id
            elif template_type == 'CJGGMB':
                info_url = 'http://srm.dongfang.com/modules/blt/BLT1050/bid_tplt_turnover_view.screen?tplt_blt_id=' + id
            elif template_type == 'YQZBGG':
                info_url = 'http://srm.dongfang.com/modules/blt/BLT1030/bid_invite_bulletin_view.screen?tplt_blt_id=' + id
            else:
                continue
        else:
            continue
        if tool.Transformation(now_time) <= tool.Transformation(zhao_time):
            print(info_url)
            get_zhaobiao_info(title,zhao_time,info_url)
        else:
            print('日期不符', zhao_time)

if __name__ == '__main__':
    requests.adapters.DEFAULT_RETRIES = 5  # 增加重连次数
    s = requests.session()
    s.keep_alive = False  # 关闭多余连接
    requests.packages.urllib3.disable_warnings()
    url = "http://srm.dongfang.com/autocrud/blt.BLT1030.bid_tplt_bulletin_home_list/query?pagesize=10&pagenum=1&_fetchall=true&_autocount=true"
    get_project(url)