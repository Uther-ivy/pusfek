import time

import requests

from spider.sikuyipingminspider import MinSpider
from jiemi.prase_code import webjiema

session=requests.session()

code_list= [
    [110000, '北京市'],
    [120000, '天津市'],
    [130000, '河北省'],
    [140000, '山西省'],
    [150000, '内蒙古自治区'],
    [210000, '辽宁省'],
    [220000, '吉林省'],
    [230000, '黑龙江省'],
    [310000, '上海市'],
    [320000, '江苏省'],
    [330000, '浙江省'],
    [340000, '安徽省'],
    [350000, '福建省'],
    [360000, '江西省'],
    [370000, '山东省'],
    [410000, '河南省'],
    [420000, '湖北省'],
    [430000, '湖南省'],
    [440000, '广东省'],
    [450000, '广西壮族自治区'],
    [460000, '海南省'],
    [500000, '重庆市'],
    [510000, '四川省'],
    [520000, '贵州省'],
    [530000, '云南省'],
    [540000, '西藏自治区'],
    [610000, '陕西省'],
    [620000, '甘肃省'],
    [630000, '青海省'],
    [640000, '宁夏回族自治区'],
    [650000, '新疆维吾尔自治区'],
    [650000, '新疆建设兵团'],
]
city_list=[]
for code in code_list:
    print(code)
    url = f'https://jzsc.mohurd.gov.cn/APi/webApi/asite/region/index?region_id={code[0]}'
    # url = f'https://jzsc.mohurd.gov.cn/APi/webApi/dataservice/query/comp/list?qy_region={420200}&pg=0&pgsz=15&total=0'
    print(url)
    headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
         }
    # data_list = session.get(url,headers=headers)
    ss=session.get(url, headers=headers,verify=False).content.decode()
    print(ss)
    data_list = webjiema(ss)['data']
    print(data_list)
    for nn in  data_list:
        city_list.append(nn)
        # time.sleep(2222)
print(city_list)


