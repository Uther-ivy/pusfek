# -*- coding: utf-8 -*-
import json
import re
import time, html

import requests
from lxml import etree
from lxml.etree import HTML

import tool
from save_database import process_item

# 上海地铁采购电子商务平台
class alashan_ggzy:
    def __init__(self):

        self.domain_name='http://www.chinaunicombidding.cn'

        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Host': 'www.chinaunicombidding.cn',
            'Origin': 'http://www.chinaunicombidding.cn',
            'Referer': 'http://www.chinaunicombidding.cn/jsp/cnceb/web/info1/infoList.jsp?type=4',
            'Cookie': 'isFir=false; jqmEwVYRfTEJS=57nnyxXypd3HH_wHVqlbyG.XXFqDj9t3Loz0poxQ4p7PISYMDqGT0T.W.k7DaJZ.fHmRH5yC.fPcCF_IkjUzo5G; BIGipServerpool_anquanfanghu=851583876.23835.0000; PURWW_SESSIONID=SwFc9fUcrv-EeAykn6gGnvWN39q9z6S9TX8ZJN0tBTBoXT28WUVX!1329624246; jqmEwVYRfTEJT=sOgnRajDFJjOrCviGUS_VRjX7sJnIL6c5xhwZXcIl2m5vi7T8BT3otijPq9Z3vyms35ph_uA2u6M3pRBiB9Y98XoUNHy_A4.0c7gLq3HsGT1iTiVv3q5bcHkIONs4ICkGK.e2mjsVjIZlpqgBnZ2JzNqJ7kcEy7CLuXsvz0sEIyi9.ZPJT3dsvTV4twXwpV8aa0OVD4CVSSFUkTUrpXtY4NNHHJfpXEc2hC2umM2YK2Z8WDRNkaln2QSqir0.MhAgESlL3e7IlrrDenU5qnfatrLPBnYXrdFvsHum8G8aVf2lodxngBvNTYXYK82RkLPDTMFQyNe.t2uCUkWgk2mMxoEP2haNxeu5ZbhMpHyW2h6RANRnjGDo4o3ubK8vp9fa5Gb4PKXy3CHoBZGFXUJTyjy59DuX.GKSu8FXmSf4zIg8__MjU3HYcT0t5Ojxsjr',
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
        }

    def parse(self):
        date = tool.date
        # date = '2020-01-06'
        page = 0
        while True:
            page += 1
            url=f'http://www.chinaunicombidding.cn/jsp/cnceb/web/info1/infoList.jsp?page={page}'
            print('*' * 20, page, '*' * 20)
            data={
            'type': '4',
            'notice': '',
            'province': '',
            'city': '',
            'time1': '',
            'time2': '',
            }
            text = tool.requests_post(url,data,self.headers).replace('&#x2f;', '/')
            html = HTML(text)
            print(11, text)
            time.sleep(6666)
            detail = html.xpath("//div[@class='pdbox']/ul/li")
            for li in detail:
                title = li.xpath('./a/text()')[0].replace('\xa0', '').replace('\n', ''). \
                    replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
                url = li.xpath('./a/@href')[0]
                date_Today = li.xpath("./span[@class='fr']/text()")[0].replace('\xa0', '').replace('\n', ''). \
                    replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '').replace('发布时间：','')
                if 'http' not in url:
                    url = self.domain_name + url
                    print(title, url, date_Today)
                # time.sleep(666)
                if tool.Transformation(date) <= tool.Transformation(date_Today):
                    if tool.removal(title, date):
                        self.parse_detile(title, url, date_Today)
                    else:
                        print('【existence】', url)
                        continue
                else:
                    print('日期不符, 正在切换类型', date_Today, self.url)
                    self.url = self.url_list.pop(0)
                    page = 0
                    break
            if page == 20:
                print('日期不符, 正在切换类型')
                self.url = self.url_list.pop(0)
                page = 0

    def parse_detile(self, title, url, date):
        print(url)
        # guid=re.findall('guid=([\d\w\-]+)&',url)[0]
        # newurl=f'https://node.dzzb.ciesco.com.cn/xunjia-mh/gonggaoxinxi/gongGao_view_3.html?guid={guid}&callBackUrl=https://dzzb.ciesco.com.cn/html/crossDomainForFeiZhaoBiao.html'
        url_text = requests.session().get(url=url, headers=self.headers).content.decode()
        url_html = etree.HTML(url_text)
        detail = url_html.xpath("//div[@class='bg-wz']")[0]
        detail_html = etree.tostring(detail, method='HTML')
        detail_html = html.unescape(detail_html.decode())
        detail_text = detail_html
            # .replace('\xa0', '').replace('\n','').replace('\r', '').replace('\t','').replace(' ', '').replace('\xa5', '')
        item = {}
        item['title'] = title.replace('\u2022', '')
        item['url'] = url
        item['date'] = date
        item['typeid'] = tool.get_typeid(item['title'])
        item['senddate'] = int(time.time())
        item['mid'] = 867
        item['address'] = tool.get_address(detail_text)
        item['nativeplace'] = float(tool.get_title_city(item['title']))
        item['infotype'] = tool.get_infotype(item['title'])
        item['body'] = tool.qudiao_width(detail_html)
        item['endtime'] = tool.get_endtime(detail_text)
        if item['endtime'] == '':
            item['endtime'] = int(time.mktime(time.strptime(date, "%Y-%m-%d")))
        else:
            try:
                item['endtime'] = int(time.mktime(time.strptime(item['endtime'], "%Y-%m-%d")))
            except:
                item['endtime'] = int(time.mktime(time.strptime(date, "%Y-%m-%d")))
        item['tel'] = tool.get_tel(detail_text)
        item['email'] = ''
        item['linkman'] = tool.get_linkman(detail_text)
        item['function'] = tool.get_function(detail_text)
        item['resource'] = '中国电信'
        item["shi"] = int(item["nativeplace"])
        if len(str(item["nativeplace"])) == 4:
            item['sheng'] = int(str(item["nativeplace"])[:2] + '00')
        elif len(str(item["nativeplace"])) == 5:
            item['sheng'] = int(str(item["nativeplace"])[:3] + '00')
        else:
            item['sheng'] = 0
        item['removal']= title
        process_item(item)
        # print(item["nativeplace"],item['address'],item['sheng'],item["shi"])
        print(item)



if __name__ == '__main__':
    import traceback, os
    try:
        jl = alashan_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
        if 'pop from empty list'!=str(e):
            print('报错')
            with open('../市级2/error_name.txt', 'a+', encoding='utf-8')as f:
                f.write(str(os.path.basename(__file__)))
                f.write('\n')
                f.write(str(traceback.format_exc()))
                f.write('\n')
        else:
            with open('success.txt','a+',encoding='utf-8')as f:
                f.write(str(os.path.basename(__file__)))
                f.write('\n')
                f.write(str('无连接抓取'))
                f.write('\n')

