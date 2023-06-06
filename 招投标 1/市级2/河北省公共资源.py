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
from proxies import proxise
from tool import get_city
from tool import more
pro = proxise()

ssl._create_default_https_context = ssl._create_unverified_context
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
}

def get_nativeplace(text):
    if '长安区' in text:
        nativeplace = 2001.001
    elif '行唐县' in text:
        nativeplace = 2001.01
    elif '灵寿县' in text:
        nativeplace = 2001.012
    elif '高邑县' in text:
        nativeplace = 2001.012
    elif '深泽县' in text:
        nativeplace = 2001.013
    elif '赞皇县' in text:
        nativeplace = 2001.014
    elif '无极县' in text:
        nativeplace = 2001.015
    elif '平山县' in text:
        nativeplace = 2001.016
    elif '元氏县' in text:
        nativeplace = 2001.017
    elif '赵县' in text:
        nativeplace = 2001.018
    elif '辛集市' in text:
        nativeplace = 2001.019
    elif '东开发区' in text:
        nativeplace = 2001.020
    elif '桥东区' in text:
        nativeplace = 2001.002
    elif '藁城市' in text:
        nativeplace = 2001.02
    elif '晋州市' in text:
        nativeplace = 2001.021
    elif '新乐市' in text:
        nativeplace = 2001.022
    elif '鹿泉市' in text:
        nativeplace = 2001.023
    elif '桥西区' in text and "石家庄" in text:
        nativeplace = 2001.003
    elif '新华区' in text:
        nativeplace = 2001.004
    elif '井陉矿区' in text:
        nativeplace = 2001.005
    elif '裕华区' in text:
        nativeplace = 2001.006
    elif '井陉县' in text:
        nativeplace = 2001.007
    elif '正定县' in text:
        nativeplace = 2001.008
    elif '栾城县' in text:
        nativeplace = 2001.009
    elif '石家庄' in text:
        nativeplace = 2001
    elif '路南区' in text:
        nativeplace = 2002.001
    elif '迁西县' in text:
        nativeplace = 2002.01
    elif '玉田县' in text:
        nativeplace = 2002.011
    elif '唐海县' in text:
        nativeplace = 2002.012
    elif '遵化市' in text:
        nativeplace = 2002.013
    elif '迁安市' in text:
        nativeplace = 2002.014
    elif '曹妃甸区' in text:
        nativeplace = 2002.015
    elif '海港开发区' in text:
        nativeplace = 2002.016
    elif '路北区' in text:
        nativeplace = 2002.002
    elif '古冶区' in text:
        nativeplace = 2002.003
    elif '开平区' in text:
        nativeplace = 2002.004
    elif '丰南区' in text:
        nativeplace = 2002.005
    elif '丰润区' in text:
        nativeplace = 2002.006
    elif '滦县' in text:
        nativeplace = 2002.007
    elif '滦南县' in text:
        nativeplace = 2002.008
    elif '乐亭县' in text:
        nativeplace = 2002.009
    elif '唐山市' in text:
        nativeplace = 2002
    elif '海港区' in text:
        nativeplace = 2003.001
    elif '山海关区' in text:
        nativeplace = 2003.002
    elif '北戴河区' in text:
        nativeplace = 2003.003
    elif '青龙满族自治县' in text:
        nativeplace = 2003.004
    elif '昌黎县' in text:
        nativeplace = 2003.005
    elif '抚宁县' in text:
        nativeplace = 2003.006
    elif '卢龙县' in text:
        nativeplace = 2003.007
    elif '秦皇岛市' in text:
        nativeplace = 2003
    elif '市辖区' in text:
        nativeplace = 2004.001
    elif '涉县' in text:
        nativeplace = 2004.01
    elif '磁县' in text:
        nativeplace = 2004.011
    elif '肥乡县' in text:
        nativeplace = 2004.012
    elif '永年县' in text:
        nativeplace = 2004.013
    elif '邱县' in text:
        nativeplace = 2004.014
    elif '鸡泽县' in text:
        nativeplace = 2004.015
    elif '广平县' in text:
        nativeplace = 2004.016
    elif '馆陶县' in text:
        nativeplace = 2004.017
    elif '魏县' in text:
        nativeplace = 2004.018
    elif '曲周县' in text:
        nativeplace = 2004.019
    elif '邯山区' in text:
        nativeplace = 2004.002
    elif '武安市' in text:
        nativeplace = 2004.02
    elif '丛台区' in text:
        nativeplace = 2004.003
    elif '复兴区' in text:
        nativeplace = 2004.004
    elif '峰峰矿区' in text:
        nativeplace = 2004.005
    elif '邯郸县' in text:
        nativeplace = 2004.006
    elif '临漳县' in text:
        nativeplace = 2004.007
    elif '成安县' in text:
        nativeplace = 2004.008
    elif '大名县' in text:
        nativeplace = 2004.009
    elif '邯郸市' in text:
        nativeplace = 2004
    elif '桥东区' in text:
        nativeplace = 2005.001
    elif '宁晋县' in text:
        nativeplace = 2005.01
    elif '巨鹿县' in text:
        nativeplace = 2005.011
    elif '新河县' in text:
        nativeplace = 2005.012
    elif '广宗县' in text:
        nativeplace = 2005.013
    elif '平乡县' in text:
        nativeplace = 2005.014
    elif '威县' in text:
        nativeplace = 2005.015
    elif '清河县' in text:
        nativeplace = 2005.016
    elif '临西县' in text:
        nativeplace = 2005.017
    elif '南宫市' in text:
        nativeplace = 2005.018
    elif '沙河市' in text:
        nativeplace = 2005.019
    elif '桥西区' in text and '邢台市' in text:
        nativeplace = 2005.002
    elif '邢台县' in text:
        nativeplace = 2005.003
    elif '临城县' in text:
        nativeplace = 2005.004
    elif '内丘县' in text:
        nativeplace = 2005.005
    elif '柏乡县' in text:
        nativeplace = 2005.006
    elif '隆尧县' in text:
        nativeplace = 2005.007
    elif '任县' in text:
        nativeplace = 2005.008
    elif '南和县' in text:
        nativeplace = 2005.009
    elif '邢台市' in text:
        nativeplace = 2005
    elif '新市区' in text:
        nativeplace = 2006.001
    elif '唐县' in text:
        nativeplace = 2006.01
    elif '高阳县' in text:
        nativeplace = 2006.011
    elif '容城县' in text:
        nativeplace = 2006.012
    elif '涞源县' in text:
        nativeplace = 2006.013
    elif '望都县' in text:
        nativeplace = 2006.014
    elif '安新县' in text:
        nativeplace = 2006.015
    elif '易县' in text:
        nativeplace = 2006.016
    elif '曲阳县' in text:
        nativeplace = 2006.017
    elif '蠡县' in text:
        nativeplace = 2006.018
    elif '顺平县' in text:
        nativeplace = 2006.019
    elif '北市区' in text:
        nativeplace = 2006.002
    elif '博野县' in text:
        nativeplace = 2006.02
    elif '雄县' in text:
        nativeplace = 2006.021
    elif '涿州市' in text:
        nativeplace = 2006.022
    elif '定州市' in text:
        nativeplace = 2006.023
    elif '安国市' in text:
        nativeplace = 2006.024
    elif '高碑店市' in text:
        nativeplace = 2006.025
    elif '竞秀区' in text:
        nativeplace = 2006.026
    elif '莲池区' in text:
        nativeplace = 2006.027
    elif '南市区' in text:
        nativeplace = 2006.003
    elif '满城县' in text:
        nativeplace = 2006.004
    elif '清苑县' in text:
        nativeplace = 2006.005
    elif '涞水县' in text:
        nativeplace = 2006.006
    elif '阜平县' in text:
        nativeplace = 2006.007
    elif '徐水县' in text:
        nativeplace = 2006.008
    elif '定兴县' in text:
        nativeplace = 2006.009
    elif '保定市' in text:
        nativeplace = 2006
    elif '桥东区' in text:
        nativeplace = 2007.001
    elif '蔚县' in text:
        nativeplace = 2007.01
    elif '阳原县' in text:
        nativeplace = 2007.011
    elif '怀安县' in text:
        nativeplace = 2007.012
    elif '万全县' in text:
        nativeplace = 2007.013
    elif '怀来县' in text:
        nativeplace = 2007.014
    elif '涿鹿县' in text:
        nativeplace = 2007.015
    elif '赤城县' in text:
        nativeplace = 2007.016
    elif '崇礼县' in text:
        nativeplace = 2007.017
    elif '桥西区' in text and "张家口" in text:
        nativeplace = 2007.002
    elif '宣化区' in text:
        nativeplace = 2007.003
    elif '张北县' in text:
        nativeplace = 2007.006
    elif '康保县' in text:
        nativeplace = 2007.007
    elif '沽源县' in text:
        nativeplace = 2007.008
    elif '尚义县' in text:
        nativeplace = 2007.009
    elif '张家口市' in text:
        nativeplace = 2007
    elif '双桥区' in text:
        nativeplace = 2008.001
    elif '宽城满族自治' in text:
        nativeplace = 2008.01
    elif '围场满族蒙古族自治县' in text:
        nativeplace = 2008.011
    elif '双滦区' in text:
        nativeplace = 2008.002
    elif '鹰手营子矿区' in text:
        nativeplace = 2008.003
    elif '承德县' in text:
        nativeplace = 2008.004
    elif '兴隆县' in text:
        nativeplace = 2008.005
    elif '平泉县' in text:
        nativeplace = 2008.006
    elif '滦平县' in text:
        nativeplace = 2008.007
    elif '丰宁满族自治县' in text:
        nativeplace = 2008.009
    elif '承德市' in text:
        nativeplace = 2008
    elif '安次区' in text:
        nativeplace = 2009.001
    elif '三河市' in text:
        nativeplace = 2009.01
    elif '广阳区' in text:
        nativeplace = 2009.002
    elif '固安县' in text:
        nativeplace = 2009.003
    elif '永清县' in text:
        nativeplace = 2009.004
    elif '香河县' in text:
        nativeplace = 2009.005
    elif '大城县' in text:
        nativeplace = 2009.006
    elif '文安县' in text:
        nativeplace = 2009.007
    elif '大厂回族自治县' in text:
        nativeplace = 2009.008
    elif '霸州市' in text:
        nativeplace = 2009.009
    elif '廊坊市' in text:
        nativeplace = 2009
    elif '桃城区' in text:
        nativeplace = 2010.001
    elif '冀州市' in text:
        nativeplace = 2010.01
    elif '深州市' in text:
        nativeplace = 2010.011
    elif '枣强县' in text:
        nativeplace = 2010.002
    elif '武邑县' in text:
        nativeplace = 2010.003
    elif '武强县' in text:
        nativeplace = 2010.004
    elif '饶阳县' in text:
        nativeplace = 2010.005
    elif '安平县' in text:
        nativeplace = 2010.006
    elif '故城县' in text:
        nativeplace = 2010.007
    elif '景县' in text:
        nativeplace = 2010.008
    elif '阜城县' in text:
        nativeplace = 2010.00
    elif '衡水市' in text:
        nativeplace = 2010
    elif '新华区' in text:
        nativeplace = 2011.001
    elif '吴桥县' in text:
        nativeplace = 2011.01
    elif '献县' in text:
        nativeplace = 2011.011
    elif '孟村回族自治县' in text:
        nativeplace = 2011.012
    elif '泊头市' in text:
        nativeplace = 2011.013
    elif '任丘市' in text:
        nativeplace = 2011.014
    elif '黄骅市' in text:
        nativeplace = 2011.015
    elif '运河区' in text:
        nativeplace = 2011.012
    elif '沧县' in text:
        nativeplace = 2011.013
    elif '青县' in text:
        nativeplace = 2011.004
    elif '东光县' in text:
        nativeplace = 2011.005
    elif '海兴县' in text:
        nativeplace = 2011.006
    elif '盐山县' in text:
        nativeplace = 2011.007
    elif '肃宁县' in text:
        nativeplace = 2011.008
    elif '南皮县' in text:
        nativeplace = 2011.009
    elif '沧州市' in text:
        nativeplace = 2011
    else:
        nativeplace = 2000
    return nativeplace

def get_zhaobiaoinfo(info_url,title,zhao_time):
    print(info_url)
    time.sleep(2)
    resp = requests.get(info_url,headers=headers,proxies=pro, timeout=60)
    resp.encoding = 'utf8'
    sel = Selector(resp)
    item = {}
    item['zhao_time'] = zhao_time
    item['title'] = title
    item['info_url'] = info_url
    item['body'] = sel.xpath('//*[@class="ewb-copy"]').extract_first()
    detail = sel.xpath('string(//div[@class="div-article2"])').extract_first()
    item['detail'] = detail.replace('\n', '').replace("\t", '').replace("\r", '').replace('\xa0', '').replace('\xc2','').replace(' ', '')
    item['senddate'] = int(time.time())
    item['mid'] = 1403
    item['resource'] = '河北省公共资源网'
    item['typeid'] = tool.get_typeid(title)
    list = re.findall('width:"(.*?)"', item['body'])
    for i in list:
        item['body'] = item['body'].replace('width:"{}"'.format(i), '')
    item['endtime'] = tool.get_endtime(detail)
    if item['endtime'] == '':
        item['endtime'] = int(time.mktime(time.strptime(item['zhao_time'], "%Y-%m-%d")))
    else:
        try:
            item['endtime'] = int(time.mktime(time.strptime(item['endtime'], "%Y-%m-%d")))
        except:
            item['endtime'] = int(time.mktime(time.strptime(item['zhao_time'], "%Y-%m-%d")))
    # print(title + str(item['detail']))
    item['nativeplace'] = get_nativeplace(item['title'])
    item['infotype'] = tool.get_infotype(title)
    item['shi'] = int(float(item['nativeplace']))  # 4502
    item['sheng'] = 2000
    item['email'] = ''
    item['tel'] = tool.get_tel(detail)
    item['address'] = tool.get_address(detail)
    item['linkman'] = tool.get_linkman(detail)
    item['function'] = tool.get_function(detail)  # detail["projectBudget"]
    item['click'] = random.randint(500, 1000)
    save_db(item)
    # print(item['title'], item['info_url'], item['nativeplace'])

def get_project(url):
    for i in range(1,50):
        data = {"token": "", "pn": 10, "rn": 10, "sdt": "", "edt": "", "wd": " ", "inc_wd": "", "exc_wd": "",
                "fields": "title",
                "cnum": "001", "sort": "{\"webdate\":0}", "ssort": "title", "cl": 200, "terminal": "", "condition": [
                {"fieldName": "categorynum", "equal": "003001", "notEqual": None, "equalList": None,
                 "notEqualList": None,
                 "isLike": True, "likeType": 2}], "time": None, "highlights": "title", "statistics": None,
                "unionCondition": None, "accuracy": "", "noParticiple": "0", "searchRange": None, "isBusiness": "1"}
        data['pn'] = (i-1)*10
        resp = requests.post(url, json=data, headers=headers, proxies=pro, timeout=20)
        resp.encoding='utf8'
        titles = json.loads(resp.text)['result']['records']
        now_time = tool.date
        for ti in titles:
            title = ti['title']
            info_url = 'http://ggzy.hebei.gov.cn/hbggfwpt' + ti['linkurl']
            zhao_time = ti['webdate'][:10]
            # print(title,info_url,zhao_time)
            if tool.Transformation(now_time) <= tool.Transformation(zhao_time):
                get_zhaobiaoinfo(info_url,title,zhao_time)
            else:
                print('日期不符', zhao_time)

if __name__ == '__main__':
    requests.adapters.DEFAULT_RETRIES = 5  # 增加重连次数
    s = requests.session()
    s.keep_alive = False  # 关闭多余连接
    requests.packages.urllib3.disable_warnings()
    get_project('http://ggzy.hebei.gov.cn/inteligentsearchfw/rest/inteligentSearch/getFullTextData')