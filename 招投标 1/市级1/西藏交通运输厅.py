# -*- coding: utf-8 -*-
import datetime
import json
import random
import re
import time

import pymysql
import requests
from scrapy import Selector
import json
import ssl
import tool
from save_database import save_db
from proxiesssss import proxise
pro = proxise()

ssl._create_default_https_context = ssl._create_unverified_context
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
}

# city_list
def get_nativeplace(addr):
    city = ''
    # 某省/自治区所有的地级市县
    city_list = [['13500', '西藏自治区'], ['13501', '拉萨市'], ['13501.001', '城关区'], ['13501.002', '林周县'], ['13501.003', '当雄县'],
                 ['13501.004', '尼木县'], ['13501.005', '曲水县'], ['13501.006', '堆龙德庆县'], ['13501.007', '达孜县'],
                 ['13501.008', '墨竹工卡县'], ['13502', '昌都地区'], ['13502.001', '昌都县'], ['13502.01', '洛隆县'],
                 ['13502.011', '边坝县'], ['13502.002', '江达县'], ['13502.003', '贡觉县'], ['13502.004', '类乌齐县'],
                 ['13502.005', '丁青县'], ['13502.006', '察雅县'], ['13502.007', '八宿县'], ['13502.008', '左贡县'],
                 ['13502.009', '芒康县'], ['13503', '山南地区'], ['13503.001', '乃东县'], ['13503.01', '隆子县'],
                 ['13503.011', '错那县'], ['13503.012', '浪卡子县'], ['13503.002', '扎囊县'], ['13503.003', '贡嘎县'],
                 ['13503.004', '桑日县'], ['13503.005', '琼结县'], ['13503.006', '曲松县'], ['13503.007', '措美县'],
                 ['13503.008', '洛扎县'], ['13503.009', '加查县'], ['13504', '日喀则地区'], ['13504.001', '日喀则市'],
                 ['13504.01', '仁布县'], ['13504.011', '康马县'], ['13504.012', '定结县'], ['13504.013', '仲巴县'],
                 ['13504.014', '亚东县'], ['13504.015', '吉隆县'], ['13504.016', '聂拉木县'], ['13504.017', '萨嘎县'],
                 ['13504.018', '岗巴县'], ['13504.002', '南木林县'], ['13504.003', '江孜县'], ['13504.004', '定日县'],
                 ['13504.005', '萨迦县'], ['13504.006', '拉孜县'], ['13504.007', '昂仁县'], ['13504.008', '谢通门县'],
                 ['13504.009', '白朗县'], ['13505', '那曲地区'], ['13505.001', '那曲县'], ['13505.01', '尼玛县'],
                 ['13505.002', '嘉黎县'], ['13505.003', '比如县'], ['13505.004', '聂荣县'], ['13505.005', '安多县'],
                 ['13505.006', '申扎县'], ['13505.007', '索县'], ['13505.008', '班戈县'], ['13505.009', '巴青县'],
                 ['13506', '阿里地区'], ['13506.001', '普兰县'], ['13506.002', '札达县'], ['13506.003', '噶尔县'],
                 ['13506.004', '日土县'], ['13506.005', '革吉县'], ['13506.006', '改则县'], ['13506.007', '措勤县'],
                 ['13507', '林芝地区'], ['13507.001', '林芝县'], ['13507.002', '工布江达县'], ['13507.003', '米林县'],
                 ['13507.004', '墨脱县'], ['13507.005', '波密县'], ['13507.006', '察隅县'], ['13507.007', '朗县']]
    for i in city_list:
        if i[1] in addr:
            city = float(i[0])
            break
    if city == '':
        city = 13500
    return city


def get_zhaobiao_info(zhao_time, info_url, title):
    print(info_url)
    resp = tool.requests_(info_url, headers)
    resp.encoding = "utf8"
    sel = Selector(resp)
    if resp.status_code == 200:
        item = {}
        item['zhao_time'] = zhao_time
        item['title'] = title
        item['info_url'] = info_url
        item['body'] = sel.xpath('//div[@class="dfz-xl-container"]/div[2]').extract_first()
        detail = sel.xpath('string(//div[@class="dfz-xl-container"]/div[2])').extract_first()
        item['detail'] = detail.replace('\n', '').replace("\t", '').replace("\r", '').replace('\xa0', '').replace('\xc2','').replace(' ', '')
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
        item['shi'] = int(item['nativeplace'])  # 4502
        item['sheng'] = 13500
        item['email'] = ''
        item['tel'] = tool.get_tel(item['detail'])
        item['address'] = tool.get_address(item['detail'])
        item['linkman'] = tool.get_linkman(item['detail'])
        item['function'] = tool.get_function(item['detail'])  # detail["projectBudget"]
        item['click'] = random.randint(500, 1000)
        item['resource'] = "西藏自治区交通运输厅"
        time.sleep(2)
        save_db(item)


def get_project(url):
    resp = tool.requests_(url, headers)
    resp.encoding = 'uft8'
    sel = Selector(resp)
    titles = sel.xpath('//*[@class="cm-news-list no-btop"]/li')
    now_time = tool.date
    # now_time = '2021-07-21'
    for ti in titles:
        title = ti.xpath('./a/text()').extract_first().strip()
        info_url = url + ti.xpath('./a/@href').extract_first().replace("./","")
        zhao_time = ti.xpath('./span/text()').extract_first().strip()
        if tool.Transformation(now_time) <= tool.Transformation(zhao_time):
            get_zhaobiao_info(zhao_time, info_url, title)
        else:
            print('日期不符', zhao_time)
            break

if __name__ == '__main__':
    requests.adapters.DEFAULT_RETRIES = 5  # 增加重连次数
    s = requests.session()
    s.keep_alive = False  # 关闭多余连接
    requests.packages.urllib3.disable_warnings()
    url_list = [
        "https://jtt.xizang.gov.cn/xxgk/fdzdgknr/zbgg/",
        "https://jtt.xizang.gov.cn/xxgk/fdzdgknr/zbgg_4482/"
    ]
    try:
        for url in url_list:
            print(url)
            get_project(url)
    except:
        import traceback
        traceback.print_exc()
