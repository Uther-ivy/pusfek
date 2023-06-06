# from tool import tool
# title='临沂市河东区利源街（智圣路-新东兴路）道路新建工程招标公告'
# a = tool.get_nativeplace(title)
# print(a)
import json
import time

import requests
from lxml import etree

import ip_proxys

url = f'https://www.youzhicai.com/nd/64488f8f-8c12-4a1c-a583-985a16a293b0-1.html'
# print('*' * 20, page, '*' * 20)
data = {
'pageIndex':2,
'id': '8312F123-CC36-F700-91DA-D7E911B8EB3D',
'type':1,
'companyId': '',
'title': '',
'ntype': '',
'start_time': '',
'end_time': '',
'child': ''

            }
headers = {
   
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
# 'Accept-Encoding': 'gzip, deflate, br',
# 'Accept-Language': 'zh-CN,zh;q=0.9',
# 'Cache-Control': 'max-age=0',
# 'Connection': 'keep-alive',
'Cookie': 'ASP.NET_SessionId=mpfod4jucjgt2ttfmutxfr1h; isPopUp=1; Hm_lvt_9511d505b6dfa0c133ef4f9b744a16da=1675414433; '
          '__root_domain_v=.youzhicai.com; _qddaz=QD.328070490722309; '
          '_qdda=3-1.3q5xdv; _qddab=3-lq4w77.lds5ba5u; '
          'spvrscode=e52b03bb7aef888a074f03e91f510c1fbed2dc8e79cd9b22a55f11ecd69bdf5bac71de3fed31666cc501ff00ec9e31f2ec3d2a2636b7291cdf84fd0c59923e9fb9c937f850fc81bac518465b8eac2a525739942db081972840b2091e8624331c04861c788682db54ba3c79a56aeb876f607ba05061b44771354f56d1ff38a710a327ff28ff0c5b72; '
          'Hm_lpvt_9511d505b6dfa0c133ef4f9b744a16da=1675647707',
'Host': 'www.youzhicai.com',
'Referer': 'https://www.youzhicai.com/nd/64488f8f-8c12-4a1c-a583-985a16a293b0-1.html',
# 'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
# 'sec-ch-ua-mobile': '?0',
# 'sec-ch-ua-platform': '"Windows"',
# 'Sec-Fetch-Dest': 'document',
# 'Sec-Fetch-Mode': 'navigate',
# 'Sec-Fetch-Site': 'same-origin',
# 'Sec-Fetch-User': '?1',
# 'Upgrade-Insecure-Requests': '1',
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
   
        }

# proxy=ip_proxys.replace_ip()
# proxies={'http':proxy,'https':proxy}
session=requests.session()
res =requests.get(url,headers=headers)
da=res.content.decode()
# print(res)
print(da)
# html=etree.HTML(data)
# title=html.xpath('//tr/td[3]/a/text()')
# print(title)

