# -*- coding: utf-8 -*-
import datetime
import random
import re
import time
import json
import pymysql
import requests
from scrapy import Selector
import ssl
import tool
from save_database import save_db
from proxiesssss import proxise
pro = proxise()

ssl._create_default_https_context = ssl._create_unverified_context
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Connection': 'keep-alive',
    'Cookie': 'JSESSIONID=99978B7ECCCD937563CD0DB4EB1D79D4; 2OILMA7BaBK2S=5oTaVa8i_mgS_LbtsT4KwTfkGcC9BdEDS4WGGKe4SQfG4MdNQJz1F5ym0KIeALksgUjUQ17aQSTEuH00Au5wgla; 2OILMA7BaBK2T=537eP_DhH36EcqGJgElNlQa3jaDXlBTt0Ru_bn0C_9fSP6zTxmJ_3BY_syJ56QKrkzO8SM_9Wk8qTNaj07UtoZB6AqUeP2AIoRrMFIr26klSGmIXQ6leRLBDmbJDY0C4NT81TggjW0JOrPGerAuX7qDwoz4dr0sY578Agl0a6r74Yu2dA0K0PalKDFDOHqRBP.MQUB7pOlR_brkHqnjNoappEVGMxDGmqBPg.zRs6Bx3rTyeZyPf.FVVJGTpLGZxINUVtl3p2e3QRDBFdndg_CHE8ZXvYwobqIa4RUwtYV5xmOZ_I1hd9UuBZARWh76FALBiZYh6ne..o5ND8AFi4XP',
    'Host': 'www.cpeinet.com.cn',
    'Referer': 'http://www.cpeinet.com.cn/cpcec/bul/bul_list.jsp?&PageIndex=1&type=1&beginTime=2021-06-19&endTime=2021-06-19',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
}



def get_zhaobiao_info(title,zhao_time,info_url):
    print(info_url)
    time.sleep(2)
    resp = requests.get(info_url, headers=headers,proxies=pro,timeout=20)
    resp.encoding = "utf8"
    sel = Selector(resp)
    item = {}
    item['zhao_time'] = zhao_time
    item['title'] = title
    item['info_url'] = info_url
    item['body'] = sel.xpath('//div[@class="article_xl"]').extract_first()
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
    item['nativeplace'] = tool.more(item['title'])
    if item['nativeplace'] == 0:
        item['nativeplace'] = tool.more(item['detail'])
    item['infotype'] = tool.get_infotype(item['title'])
    item['shi'] = int(item['nativeplace'])
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
    item['resource'] = "中国电力设备信息网"
    save_db(item)

def get_project(url):
    print(url)
    resp = requests.get(url,headers=headers,proxies=pro,timeout=20)
    resp.encoding = 'utf8'
    print(resp.text)
    sel = Selector(resp)
    titles = sel.xpath('//div[@class="article_list_lb"]/ul//li')
    for ti in titles:
        title = ti.xpath('./span/a/@title').extract_first()
        zhao_time = ti.xpath('./i/text()').extract_first()
        info_url = "http://www.cpeinet.com.cn/cpcec/bul/bulletin_show.jsp?id=" + ti.xpath('./span/a/@onclick').extract_first().replace("goNewPage(","").split(",")[0]
        print(info_url)
        if tool.Transformation(tool.date) <= tool.Transformation(zhao_time):
            get_zhaobiao_info(title,zhao_time,info_url)
        else:
            print('日期不符', zhao_time)

if __name__ == '__main__':
    # import traceback, os
    # try:
    #     requests.adapters.DEFAULT_RETRIES = 5  # 增加重连次数
    #     s = requests.session()
    #     s.keep_alive = False  # 关闭多余连接
    #     requests.packages.urllib3.disable_warnings()
    #     now_time = tool.date
    #     for i in range(1, 3):
    #         url = 'http://www.cpeinet.com.cn/cpcec/bul/bul_list.jsp?&PageIndex={}&type=1&beginTime={}&endTime={}'.format(
    #             str(i), now_time, now_time)
    #         get_project(url)
    # except Exception as e:
    #     traceback.print_exc()
        # tool.send_error('报错文件：'+str(os.path.basename(__file__))+'报错信息：'+str(e))
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        # 'Accept-Encoding': 'gzip, deflate',
        # 'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        # 'Connection': 'keep-alive',
        'Cookie': 'JSESSIONID=99978B7ECCCD937563CD0DB4EB1D79D4; 2OILMA7BaBK2S=5oTaVa8i_mgS_LbtsT4KwTfkGcC9BdEDS4WGGKe4SQfG4MdNQJz1F5ym0KIeALksgUjUQ17aQSTEuH00Au5wgla; 2OILMA7BaBK2T=537eP_DhH36EcqGJgElNlQa3jaDXlBTt0Ru_bn0C_9fSP6zTxmJ_3BY_syJ56QKrkzO8SM_9Wk8qTNaj07UtoZB6AqUeP2AIoRrMFIr26klSGmIXQ6leRLBDmbJDY0C4NT81TggjW0JOrPGerAuX7qDwoz4dr0sY578Agl0a6r74Yu2dA0K0PalKDFDOHqRBP.MQUB7pOlR_brkHqnjNoappEVGMxDGmqBPg.zRs6Bx3rTyeZyPf.FVVJGTpLGZxINUVtl3p2e3QRDBFdndg_CHE8ZXvYwobqIa4RUwtYV5xmOZ_I1hd9UuBZARWh76FALBiZYh6ne..o5ND8AFi4XP',
        'Host': 'www.cpeinet.com.cn',
        # 'Referer': 'http://www.cpeinet.com.cn/cpcec/bul/bul_list.jsp?&PageIndex=1&type=1&beginTime=2021-06-19&endTime=2021-06-19',
        # 'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
    }
    url = 'http://www.cpeinet.com.cn/cpcec/bul/bul_list.jsp?type=1&invitetype=&name=&beginTime=2021-06-19&endTime=2021-06-19&area='
    rst = requests.get(url, headers=headers).text
    print(rst)



