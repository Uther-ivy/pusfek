import certifi
import requests
import urllib3

from 四库一平台.spider.ip_proxys import replace_ip

url='https://whsggj.wuhu.gov.cn/wuhu/site/label/8888?_=0.7481193359407712&labelName=publicInfoList&siteId=6787891' \
    '&pageSize=15&pageIndex=2&action=list&isDate=true&dateFormat=yyyy-MM-dd&length=50&organId=6596831&type=4&catId' \
    '=6736391&cId=&result=%E6%9A%82%E6%97%A0%E7%9B%B8%E5%85%B3%E4%BF%A1%E6%81%AF&file=%2Fc1%2Fwuhu' \
    '%2FpublicInfoList_newes'
res=requests.session()
header={
# 'Accept': 'text/html, */*; q=0.01',
# 'Accept-Encoding': 'gzip, deflate, br',
# 'Accept-Language': 'zh-CN,zh;q=0.9',
# 'Connection': 'keep-alive',
# 'Cookie': 'wh_gova_SHIROJSESSIONID=4bc1210c-81e7-4160-9f58-58052dd8a6f2; wh_govd_SHIROJSESSIONID=671081f6-98a0-41e5-8b94-61dcecab0587; wzaConfigTime=1685325500623',
# 'Host': 'whsggj.wuhu.gov.cn',
# 'Ls-Language': 'zh',
# 'Referer': 'https://whsggj.wuhu.gov.cn/public/column/6596831?type=4&action=list&nav=3&sub=&catId=6736391',
# 'Sec-Fetch-Dest': 'empty',
# 'Sec-Fetch-Mode': 'cors',
# 'Sec-Fetch-Site': 'same-origin',
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
'X-Requested-With': 'XMLHttpRequest',
# 'sec-ch-ua': '"Google Chrome";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
# 'sec-ch-ua-mobile': '?0',
# 'sec-ch-ua-platform': '"Windows"',
}
http=replace_ip()
proxy={'http':http,'https':http}
# from requests.packages.urllib3.exceptions import InsecureRequestWarning
    # 禁用安全请求警告
# requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
# htt= urllib3.PoolManager(cert_reqs = 'CERT_REQUIRED', ca_certs = certifi.where('whsggj.wuhu.gov.cn.crt'))
# ress=urllib3.util.ssl_.sha256('')
# print(ress)
rext=res.get(url=url,
             headers=header,
             proxies=proxy,
             cert=('whsggj.wuhu.gov.cn.crt')
             )
print(rext)