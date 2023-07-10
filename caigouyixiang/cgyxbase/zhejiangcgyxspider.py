import json
import logging
import os
import random
import threading
import time
import traceback
import urllib.parse

import requests as requests
from lxml import etree

import ip_proxys
from caigouyixiang.cgyxdata.sql import serversql, rundb


class cgyxspider(object):
    def __init__(self):
        self._session=requests.session()
        self.proxys = {
            'http': '',
            'https': ''
        }
        self.headers= {
# 'Accept-Encoding':'gzip, deflate',
# 'Accept-Language':'zh-CN,zh;q=0.9',
# 'Connection':'keep-alive',
'Accept':'application/json, text/plain, */*',
# 'Cookie':'zcy_im_uuid=2fb1b8f7-9924-4cb1-a14b-e8ee88f2f9f3; _zcy_log_client_uuid=5db294f0-1c9a-11ee-9457-ab947b2c379e; arialoadData=false;',
           #zcy_im_uuid=2fb1b8f7-9924-4cb1-a14b-e8ee88f2f9f3; _zcy_log_client_uuid=5db294f0-1c9a-11ee-9457-ab947b2c379e; arialoadData=false; acw_tc=ac11000116887178747912968e2396b5c1f6c77eca56903402fc6bc211bb22
           #zcy_im_uuid=2fb1b8f7-9924-4cb1-a14b-e8ee88f2f9f3; _zcy_log_client_uuid=5db294f0-1c9a-11ee-9457-ab947b2c379e; arialoadData=false; acw_tc=ac11000116887782405287523e249ff51ead83ed5ed36d95451b151cf94bd7
'Content-Type': "application/json;charset=utf-8",
# 'Host':'www.ccgp-zhejiang.gov.cn',
# 'Origin':'http://www.ccgp-zhejiang.gov.cn',
# 'Referer':'http://www.ccgp-zhejiang.gov.cn/luban/category?parentId=600007&childrenCode=ZcyAnnouncement&utm=',
'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
'X-Requested-With':'XMLHttpRequest',


         }
        self.errors=0

    def replace_ip(self):

        proxy = ip_proxys.replace_ip()
        self.proxys = {
            'http': proxy,
            'https': proxy
        }
        print(self.proxys)

    def article_field(self):
        data_dict = {
            'districtName': '',
            'articleId': '',
            'publishDate': '',
            'procurement':'',
            'title': '',

            'detail': {}

        }
        return data_dict

    def req_(self, url, method, data=None, param=None):
        time.sleep(5+random.random()*5)
        prox = self.proxys
        if method == 'get':
            res = self._session.get(url=url, headers=self.headers, data=data, params=param, proxies=prox, verify=False,
                                    timeout=60)
        else:
            res = self._session.post(url=url, headers=self.headers, data=data, params=param, proxies=prox, verify=False,
                                     timeout=60)
        if res.status_code == requests.codes.ok:
            res_data = res.content.decode()
            return res_data

    def request_(self, url, method, data=None, param=None):
        try:
            res = self.req_(url, method, data, param)
        except Exception as e:
            print(e)
            logging.info("proxy disabled！！！ change proxy")
            time.sleep(random.random() * 10)
            self.replace_ip()
            res = self.req_(url, method, data, param)
        return res

    def get_data_detail(self, url):
        detail_list=list()
        print(url)
        res = self.request_(url, method='get')
        if res:
            content=json.loads(res)['result']['data']['content']
            # print(html)
            detail = etree.HTML(content)
            # size= detail.xpath("//td[@class='code-purchaseProjectName']")
            # for num in range(1,len(size)+1):
            #     detail_dict = {}
            #     proname = detail.xpath(f"//tr[{num}]/td[@class='code-purchaseProjectName']/text()")
            #     if proname:
            #         proname = proname[0].replace('\u3000','')
            #     require = detail.xpath(f"//tr[{num}]/td[@class='code-purchaseRequirementDetail']/text()")
            #     if require:
            #         require = require[0]
            price = detail.xpath(f"//td[@class='code-budgetPrice']/text()")
            if price :
                    price = float(price[0].replace(',',''))
            futher = detail.xpath(f"//td[@class='code-estimatedPurchaseTime']/text()")
            if futher:
                    futher=futher[0]
                    if '年' in futher:
                        futher = int(time.mktime(time.strptime(futher.strip(), "%Y年%m月")))  #
                    else:
                        futher = int(time.mktime(time.strptime(futher.strip(), "%Y-%m")))  #
                # comment = detail.xpath(f"//tr[{num}]/td[@class='code-remark']/text()")
                # if comment:
                #     comment = comment[0]
                # detail_dict['proname'] = proname
                # detail_dict['price'] = price
                # detail_dict['require'] = require
                # detail_dict['futher'] = futher
                # detail_dict['comment'] = comment
                # detail_list.append(detail_dict)
                # print( proname,price,require,futher,comment)
            return content,futher,price
        # except Exception as e:
        #     logging.error(f"list获取失败{e}\n{traceback.format_exc()}")



    def get_data_list(self, times,page):
        url = f'http://www.ccgp-zhejiang.gov.cn/portal/category'
        print(url)
        payload ={"pageNo":page,
                  "pageSize":15,
                  "categoryCode":"110-600268","isGov":
                      'true',"excludeDistrictPrefix":"90","_t":int(time.time())*1000}
        print(payload)
        data=None
        data_list = self.request_(url,  method='post',data=json.dumps(payload))
        print(data_list)
        if data_list:
            # return data_list
            jsondata=json.loads(data_list)
            for lis in jsondata.get('result').get('data').get('data'):
                # releasetime = int(time.mktime(time.strptime(lis['noticePubDate'], "%Y-%m-%d %H:%M:%s")))
                releasetime = int(lis['publishDate'])/1000
                todaytime = int(time.mktime(time.strptime(times, "%Y-%m-%d")))
                print(releasetime,todaytime)
                if releasetime >= todaytime:
                    districtName = lis['districtName'].replace('本级','')
                    articleId=lis['articleId']
                    title=lis['title']
                    procurement=lis['author']
                    href=f'http://www.ccgp-zhejiang.gov.cn/portal/detail?articleId={urllib.parse.quote(articleId)}&timestamp={int(time.time())}'
                    showurl=f'http://www.ccgp-zhejiang.gov.cn/luban/detail?parentId=600007&articleId={urllib.parse.quote(articleId)}&utm='
                    yield districtName,releasetime,articleId,title,href,showurl,procurement
                else:
                    print(f'{times}获取完毕{page}页')
                    self.err()
        else:
            print(f'{times}获取完毕{page}页')
            self.err()
    def write_data(self,file,data):
        with open(file,'a',encoding='utf-8') as w:
            w.write(data)
            w.close()

    def err(self):
        self.errors=1
def run(page,spider,times,file):

    for lis in spider.get_data_list(times,page):
        districtName,releasetime,articleId,title,href,showurl,procurement=lis
        prodict = spider.article_field()
        prodict['procurement'] = procurement
        prodict['districtName'] = districtName
        prodict['articleId'] =int(str(int(time.time() * 100000 + random.random() * 200))[-6:])
        prodict['publishDate'] = releasetime
        prodict['title'] = title
        prodict['detailurl'] = showurl
        prodict['detail'],prodict['futher'],prodict['price'] = spider.get_data_detail(href)
        print(prodict)
        # spider.write_data(file,str(prodict)+"\n")
        mysqldb = serversql()
        rundb(mysqldb, prodict)


def main(page, times, file):
    threads = []
    spider = cgyxspider()
    spider.replace_ip()
    for num in range(1, page):
        # print(num)
        if spider.errors == 1:
            break
        t = threading.Thread(target=run, args=(num,),
                             kwargs={'spider': spider, 'times': times, 'file': file})
        time.sleep(5 + random.random() * 5)
        # print(spider.errors)
        threads.append(t)
        t.start()

    for thread in threads:
        thread.join()



if __name__ == '__main__':
    times = time.time()
    file = os.path.basename('../unit.txt')
    with open(file, 'r') as f:
        if os.path.exists(file):
            read = f.readline()
            f.close()
            base = json.loads(read)
            print(base['time'])
            main(base['page'], base['time'], base['file'])
    print(time.time() - times)

