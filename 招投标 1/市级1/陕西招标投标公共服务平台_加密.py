# -*- coding: utf-8 -*-
import datetime
import json
import random
import re
import time

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
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
}

def get_nativeplace(addr):
    city = ''
    city_list = [['14000', '陕西省'], ['14001', '西安'], ['14001.001', '新城区'],
                 ['14001.01', '蓝田县'], ['14001.011', '周至县'], ['14001.012', '户县'], ['14001.013', '高陵县'],
                 ['14001.002', '碑林区'], ['14001.003', '莲湖区'], ['14001.004', '灞桥区'], ['14001.005', '未央区'],
                 ['14001.006', '雁塔区'], ['14001.007', '阎良区'], ['14001.008', '临潼区'], ['14001.009', '长安区'],
                 ['14002', '铜川'], ['14002.001', '王益区'], ['14002.002', '印台区'], ['14002.003', '耀州区'],
                 ['14002.004', '宜君县'], ['14003', '宝鸡'], ['14003.001', '滨区'], ['14003.01', '麟游县'], ['14003.011', '凤县'],
                 ['14003.012', '太白县'], ['14003.002', '金台区'], ['14003.003', '陈仓区'], ['14003.004', '凤翔县'],
                 ['14003.005', '岐山县'], ['14003.006', '扶风县'], ['14003.007', '眉县'], ['14003.008', '陇县'],
                 ['14003.009', '千阳县'], ['14004', '咸阳'], ['14004.001', '秦都区'], ['14004.01', '长武县'], ['14004.011', '旬邑县'],
                 ['14004.012', '淳化县'], ['14004.013', '武功县'], ['14004.014', '兴平'], ['14004.002', '杨凌区'],
                 ['14004.003', '渭城区'], ['14004.004', '三原县'], ['14004.005', '泾阳县'], ['14004.006', '乾县'],
                 ['14004.007', '礼泉县'], ['14004.008', '永寿县'], ['14004.009', '彬县'], ['14005', '渭南'], ['14005.001', '临渭区'],
                 ['14005.01', '韩城'], ['14005.011', '华阴'], ['14005.002', '华县'], ['14005.003', '潼关县'],
                 ['14005.004', '大荔县'], ['14005.005', '合阳县'], ['14005.006', '澄城县'], ['14005.007', '蒲城县'],
                 ['14005.008', '白水县'], ['14005.009', '富平县'], ['14006', '延安'], ['14006.001', '宝塔区'], ['14006.01', '洛川县'],
                 ['14006.011', '宜川县'], ['14006.012', '黄龙县'], ['14006.013', '黄陵县'], ['14006.002', '延长县'],
                 ['14006.003', '延川县'], ['14006.004', '子长县'], ['14006.005', '安塞县'], ['14006.006', '志丹县'],
                 ['14006.007', '吴旗县'], ['14006.008', '甘泉县'], ['14006.009', '富县'], ['14007', '汉中'], ['14007.001', '汉台区'],
                 ['14007.01', '留坝县'], ['14007.011', '佛坪县'], ['14007.002', '南郑县'], ['14007.003', '城固县'],
                 ['14007.004', '洋县'], ['14007.005', '西乡县'], ['14007.006', '勉县'], ['14007.007', '宁强县'],
                 ['14007.008', '略阳县'], ['14007.009', '镇巴县'], ['14008', '榆林'], ['14008.001', '榆阳区'], ['14008.01', '吴堡县'],
                 ['14008.011', '清涧县'], ['14008.012', '子洲县'], ['14008.002', '神木县'], ['14008.003', '府谷县'],
                 ['14008.004', '横山县'], ['14008.005', '靖边县'], ['14008.006', '定边县'], ['14008.007', '绥德县'],
                 ['14008.008', '米脂县'], ['14008.009', '佳县'], ['14009', '安康'], ['14009.001', '汉滨区'], ['14009.01', '白河县'],
                 ['14009.002', '汉阴县'], ['14009.003', '石泉县'], ['14009.004', '宁陕县'], ['14009.005', '紫阳县'],
                 ['14009.006', '岚皋县'], ['14009.007', '平利县'], ['14009.008', '镇坪县'], ['14009.009', '旬阳县'],
                 ['14010', '商洛'], ['14010.001', '商州区'], ['14010.002', '洛南县'], ['14010.003', '丹凤县'],
                 ['14010.004', '商南县'], ['14010.005', '山阳县'], ['14010.006', '镇安县'], ['14010.007', '柞水县'],
                 ]
    for i in city_list:
        if i[1] in addr:
            city = float(i[0])
            break
    if city == "":
        return 14000
    else:
        return city


def get_zhaobiao_info(title,zhao_time,info_url):
    resp = requests.get(info_url, headers=headers,proxies=pro,timeout=20)
    resp.encoding = "utf8"
    sel = Selector(resp)
    item = {}
    item['zhao_time'] = zhao_time
    item['title'] = title
    item['info_url'] = info_url
    bd = sel.xpath('//div[@class="mian_list"]').extract_first()
    pdf_url = bd.split("escape('")[1].split("'),")[0]
    item['body'] = bd.replace("</script>","</script>\n              <div class='block'><a href='{}' id='oDownLoad'  onclick='pdf()'><span class='pdfflash'>PDF下载</span></a></div>".format(pdf_url)).replace('<a id="viewerPlaceHolder" style="width: 100%; height: 660px; display: block"></a>','')
    item['detail'] = item['body'].replace('\n', '').replace("\t", '').replace("\r", '').replace('\xa0', '').replace('\xc2', '').replace(' ', '')
    item['senddate'] = int(time.time())
    item['mid'] = 1403
    item['typeid'] = tool.get_typeid(title)
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
    item['shi'] = int(item['nativeplace'])
    item['sheng'] = 14000
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
    item['resource'] = "陕西招投标公共服务平台"
    time.sleep(2)
    save_db(item)

def get_project(url):
    print(url)
    resp = requests.get(url,headers=headers,proxies=pro,timeout=20)
    resp.encoding = 'utf8'
    sel = Selector(resp)
    titles = sel.xpath('//table[@class="table_text"]/tr')
    now_time = tool.date
    for ti in titles:
        title = ti.xpath('./td[1]/a/@title').extract_first()
        zhao_time = ti.xpath('string(./td[5]/text())').extract_first().strip()
        info_url = ti.xpath('./td[1]/a/@href').extract_first()
        if zhao_time == '':
            zhao_time = ti.xpath('string(./td[4]/text())').extract_first().strip()
        if info_url == None:
            continue
        else:
            info_url = info_url.replace("javascript:urlOpen('","").replace("')","")
        if tool.Transformation(now_time) <= tool.Transformation(zhao_time):
            get_zhaobiao_info(title,zhao_time,info_url)
        else:
            print('日期不符', zhao_time)
            break

if __name__ == '__main__':
    requests.adapters.DEFAULT_RETRIES = 5  # 增加重连次数
    s = requests.session()
    s.keep_alive = False  # 关闭多余连接
    requests.packages.urllib3.disable_warnings()
    urls = ['http://bulletin.sntba.com/xxfbcmses/search/bulletin.html?searchDate=1995-07-09&dates=300&categoryId=88&industryName=&area=&status=&publishMedia=&sourceInfo=&showStatus=&page={}',
            'http://bulletin.sntba.com/xxfbcmses/search/qualify.html?searchDate=1995-07-09&dates=300&categoryId=92&industryName=&area=&status=&publishMedia=&sourceInfo=&showStatus=&page={}',
            'http://bulletin.sntba.com/xxfbcmses/search/candidate.html?searchDate=1995-07-09&dates=300&categoryId=91&industryName=&area=&status=&publishMedia=&sourceInfo=&showStatus=&page={}',
            'http://bulletin.sntba.com/xxfbcmses/search/result.html?searchDate=1995-07-09&dates=300&categoryId=90&industryName=&area=&status=&publishMedia=&sourceInfo=&showStatus=&page={}',
            'http://bulletin.sntba.com/xxfbcmses/search/change.html?searchDate=1995-07-09&dates=300&word=&categoryId=89&industryName=&area=&status=&publishMedia=&sourceInfo=&showStatus=&page={}']
    for i in range(1,2):
        for url in urls:
            # print(url.format(str(i)))
            get_project(url.format(str(i)))