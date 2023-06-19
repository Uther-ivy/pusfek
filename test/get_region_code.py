import time

import requests

from spider.sikuyipingminspider import MinSpider
from siku_jiemi.prase_code import webjiema

session=requests.session()

code_list= [
    {'region_id':'110000','region_fullname':'北京市'},
    {'region_id':'120000','region_fullname':'天津市'},
    {'region_id':'130000','region_fullname':'河北省'},
    {'region_id':'140000','region_fullname':'山西省'},
    {'region_id':'150000','region_fullname':'内蒙古自治区'},
    {'region_id':'210000','region_fullname':'辽宁省'},
    {'region_id':'220000','region_fullname':'吉林省'},
    {'region_id':'230000','region_fullname':'黑龙江省'},
    {'region_id':'310000','region_fullname':'上海市'},
    {'region_id':'320000','region_fullname':'江苏省'},
    {'region_id':'330000','region_fullname':'浙江省'},
    {'region_id':'340000','region_fullname':'安徽省'},
    {'region_id':'350000','region_fullname':'福建省'},
    {'region_id':'360000','region_fullname':'江西省'},
    {'region_id':'370000','region_fullname':'山东省'},
    {'region_id':'410000','region_fullname':'河南省'},
    {'region_id':'420000','region_fullname':'湖北省'},
    {'region_id':'430000','region_fullname':'湖南省'},
    {'region_id':'440000','region_fullname':'广东省'},
    {'region_id':'450000','region_fullname':'广西壮族自治区'},
    {'region_id':'460000','region_fullname':'海南省'},
    {'region_id':'500000','region_fullname':'重庆市'},
    {'region_id':'510000','region_fullname':'四川省'},
    {'region_id':'520000','region_fullname':'贵州省'},
    {'region_id':'530000','region_fullname':'云南省'},
    {'region_id':'540000','region_fullname':'西藏自治区'},
    {'region_id':'610000','region_fullname':'陕西省'},
    {'region_id':'620000','region_fullname':'甘肃省'},
    {'region_id':'630000','region_fullname':'青海省'},
    {'region_id':'640000','region_fullname':'宁夏回族自治区'},
    {'region_id':'650000','region_fullname':'新疆维吾尔自治区'},
    {'region_id':'650000','region_fullname':'新疆建设兵团'},
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


