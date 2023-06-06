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
ssl._create_default_https_context = ssl._create_unverified_context
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
}

# city_list
def get_nativeplace(addr):
    city = ''
    # 某省/自治区所有的地级市县
    city_list = [
        ['14500', '甘肃省'], ['14501', '兰州市'], ['14501.001', '城关区'], ['14501.002', '七里河区'], ['14501.003', '西固区'],
        ['14501.004', '安宁区'], ['14501.005', '红古区'], ['14501.006', '永登县'], ['14501.007', '皋兰县'],
        ['14501.008', '榆中县'],
        ['14502', '嘉峪关市'], ['14503', '金昌市'], ['14503.001', '金川区'], ['14503.002', '永昌县'], ['14504', '白银市'],
        ['14504.001', '白银区'], ['14504.002', '平川区'], ['14504.003', '靖远县'], ['14504.004', '会宁县'],
        ['14504.005', '景泰县'],
        ['14505', '天水市'], ['14505.001', '秦城区'], ['14505.002', '北道区'], ['14505.003', '清水县'], ['14505.004', '秦安县'],
        ['14505.005', '甘谷县'], ['14505.006', '武山县'], ['14505.007', '张家川回族自治县'], ['14506', '武威市'],
        ['14506.001', '凉州区'],
        ['14506.002', '民勤县'], ['14506.003', '古浪县'], ['14506.004', '天祝藏族自治县'], ['14507', '张掖市'],
        ['14507.001', '甘州区'],
        ['14507.002', '肃南裕固族自治县'], ['14507.003', '民乐县'], ['14507.004', '临泽县'], ['14507.005', '高台县'],
        ['14507.006', '山丹县'], ['14508', '平凉市'], ['14508.001', '崆峒区'], ['14508.002', '泾川县'], ['14508.003', '灵台县'],
        ['14508.004', '崇信县'], ['14508.005', '华亭县'], ['14508.006', '庄浪县'], ['14508.007', '静宁县'], ['14509', '酒泉市'],
        ['14509.001', '肃州区'], ['14509.002', '金塔县'], ['14509.003', '安西县'], ['14509.004', '肃北蒙古族自治县'],
        ['14509.005', '阿克塞哈萨克族自治县'], ['14509.006', '玉门市'], ['14509.007', '敦煌市'], ['14510', '庆阳市'],
        ['14510.001', '西峰区'],
        ['14510.002', '庆城县'], ['14510.003', '环县'], ['14510.004', '华池县'], ['14510.005', '合水县'], ['14510.006', '正宁县'],
        ['14510.007', '宁县'], ['14510.008', '镇原县'], ['14511', '定西市'], ['14511.001', '安定区'], ['14511.002', '通渭县'],
        ['14511.003', '陇西县'], ['14511.004', '渭源县'], ['14511.005', '临洮县'], ['14511.006', '漳县'], ['14511.007', '岷县'],
        ['14512', '陇南市'], ['14512.001', '武都区'], ['14512.002', '成县'], ['14512.003', '文县'], ['14512.004', '宕昌县'],
        ['14512.005', '康县'], ['14512.006', '西和县'], ['14512.007', '礼县'], ['14512.008', '徽县'], ['14512.009', '两当县'],
        ['14513', '临夏回族自治州'], ['14513.001', '临夏市'], ['14513.002', '临夏县'], ['14513.003', '康乐县'],
        ['14513.004', '永靖县'],
        ['14513.005', '广河县'], ['14513.006', '和政县'], ['14513.007', '东乡族自治县'], ['14513.008', '积石山保安族东乡族撒拉族自治县'],
        ['14514', '甘南藏族自治州'], ['14514.001', '合作市'], ['14514.002', '临潭县'], ['14514.003', '卓尼县'],
        ['14514.004', '舟曲县'],
        ['14514.005', '迭部县'], ['14514.006', '玛曲县'], ['14514.007', '碌曲县'], ['14514.008', '夏河县'],
    ]
    for i in city_list:
        if i[1] in addr:
            city = float(i[0])
            break
    if city == '':
        city = 14508
    return city

def get_zhaobiao_info(zhao_time,info_url,title):
    resp = tool.requests.get(info_url, headers=headers )
    resp.encoding = "utf8"
    sel = Selector(resp)
    if resp.status_code == 200:
        item = {}
        item['zhao_time'] = zhao_time
        item['title'] = title
        item['info_url'] = info_url
        #http://wrkj-tradeform-test.oss.aliyuncs.com/TP_AttachmentTest/c44756c1-3574-480d-8e04-d2298b48ef0b.pdf
        #http://wrkj-tradeform-test.oss.aliyuncs.com/TP_AttachmentTest/52d60976-9a9b-486c-8d31-1bdbe1f9f441.pdf
        # <iframe src="http://wrkj-tradeform-test.oss.aliyuncs.com/TP_AttachmentTest/535fYN2zDd.pdf" width="800" height="600"></iframe>
        # <a class="pdf" href="http://wrkj-tradeform-test.oss.aliyuncs.com/TP_AttachmentTest/535fYN2zDd.pdf"></a>
        item['body'] = sel.xpath('//a[@class="pdf"]/@href').getall()[0]
        item['detail'] = sel.xpath('string(//div[@class="signUpCorrect_Wrap"])').extract_first()
        item['detail'] = item['detail'].replace('\n', '').replace("\t", '').replace("\r", '').replace('\xa0', '').replace('\xc2', '').replace(' ', '')
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
        item['nativeplace'] = get_nativeplace(item['title'] + item['detail'])
        item['infotype'] = tool.get_infotype(item['title'])
        item['shi'] = int(item['nativeplace'])  # 4502
        item['sheng'] = 14500
        item['email'] = ''
        item['tel'] = tool.get_tel(item['detail'])
        item['address'] = tool.get_address(item['detail'])
        item['linkman'] = tool.get_linkman(item['detail'])
        item['function'] = tool.get_function(item['detail'])  # detail["projectBudget"]
        item['click'] = random.randint(500, 1000)
        item['resource'] = "平凉市公共资源交易网"
        save_db(item)
        # print(item["body"])

def get_project(url):
    now_time = tool.date
    # now_time = '2022-06-01'
    listTypes = ['21','22']
    for listType in listTypes:
        data = {'pageNo': 0,  # 页数
                'pageSize': 20,
                'listType': 21,
                'ataType': 0,
                'pageType': 'item',
                'projectType': "",
                'tradePlatformId': ""}
        resp = tool.requests.post(url, data=data, headers=headers)
        sel = Selector(resp)
        titles = sel.xpath('//div[@class="byTradingDetail-Con byTradingDetail-ConActive"]/dl/dd')
        for ti in titles:
            title = ti.xpath('./a/text()').extract_first().strip()
            info_url = "http://www.plsggzyjy.cn" + ti.xpath('./a/@href').extract_first()
            zhao_time = ti.xpath('./span/text()').extract_first()
            # print(title,info_url,zhao_time)
            if tool.Transformation(now_time) <= tool.Transformation(zhao_time):
                # print(title,info_url,zhao_time)
                get_zhaobiao_info(zhao_time, info_url, title)
            else:
                print(zhao_time)
                break


if __name__ == '__main__':
    import traceback, os
    try:
        requests.adapters.DEFAULT_RETRIES = 5  # 增加重连次数
        s = requests.session()
        s.keep_alive = False  # 关闭多余连接
        requests.packages.urllib3.disable_warnings()
        get_project(
            "http://www.plsggzyjy.cn/f/tenderannquainqueryanns/tenderannquainqueryanns/annquainList?projectDataSourceId=")
    except Exception as e:
        traceback.print_exc()
        tool.send_error('报错文件：'+str(os.path.basename(__file__))+'报错信息：'+str(e))
