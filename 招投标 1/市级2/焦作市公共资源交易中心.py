# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 焦作市公共资源交易中心
class wenshan_ggzy:
    def __init__(self):
        self.domain_name = 'http://www.jzggzy.cn'
        self.url_list = [
            '006001',
            '006002',
            '006005'
        ]
        self.url = self.url_list.pop(0)
        self.headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate',
            'X-Requested-With': 'XMLHttpRequest',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Host': 'www.jzggzy.cn',
            'Origin': 'http://www.jzggzy.cn',
            'Referer': 'http://www.jzggzy.cn/jyxx/006005/project.html',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',

        }

    def parse(self):
        date = tool.date
        # date = '2021-08-02'
        page = 0
        url_to = 'http://www.jzggzy.cn/inteligentsearch/rest/esinteligentsearch/getFullTextDataNew'
        while True:
            page += 1
            data = {"token":"","pn":page,"rn":15,"sdt":"","edt":"","wd":"%20","inc_wd":"","exc_wd":"","fields":"titles","cnum":"001","sort":"{\"webdate\":\"0\"}","ssort":"title","cl":200,"terminal":"","condition":[{"fieldName":"categorynum","equal":self.url,"notEqual":None,"equalList":None,"notEqualList":None,"isLike":True,"likeType":2}],"time":[{"fieldName":"webdate","startTime":"1970-01-01 00:00:00","endTime":"2999-12-31 23:59:59"}],"highlights":"","statistics":None,"unionCondition":None,"accuracy":"","noParticiple":"0","searchRange":None,"isBusiness":"1"}
            text = tool.requests_post_to(url_to, data, self.headers)
            print('*' * 20, page, '*' * 20)
            detail = json.loads(text)['result']['records']
            for li in detail:
                title = li['title'].replace('\xa0', '').replace('\n', ''). \
                    replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
                url = 'http://www.jzggzy.cn/jyxx/{}/{}/{}/{}.html'.format(li['categorynum'][:6],li['categorynum'], li['infodate'][:10].replace('-', ''),li['linkurl'])
                date_Today = li['webdate'][:10].replace('\xa0', '').replace('\n', ''). \
                    replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '') \
                    .replace('[', '').replace(']', '').replace('/', '-')
                if 'http' not in url:
                    url = self.domain_name + url
                # print(title, url, date_Today)
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
                self.url = self.url_list.pop(0)
                break

    def parse_detile(self, title, url, date):
        print(url)
        t = tool.requests_get(url, self.headers).replace('\xa9', '').replace('<br>&nbsp;&nbsp;', '')
        # print(t)
        # time.sleep(2222)
        url_html = etree.HTML(t)
        try:
            detail = url_html.xpath('//*[@id="infodetail"]')[0]
            detail_html = etree.tostring(detail, method='HTML')
            detail_html = html.unescape(detail_html.decode()).replace("display: none", '')
            detail_text = url_html.xpath('string(//*[@id="infodetail"])').replace('\xa0', '').replace('\n',
                                                                                                                 ''). \
                replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
        except:
            try:
                detail = url_html.xpath('//*[@class="tabview"]')[0]
                detail_html = etree.tostring(detail, method='HTML')
                detail_html = html.unescape(detail_html.decode()).replace("display: none", '')
                detail_text = url_html.xpath('string(//*[@class="tabview"])').replace('\xa0', '').replace('\n',
                                                                                                          ''). \
                    replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
            except:
                return
        item = {}
        item['title'] = title.replace('\u2022', '')
        item['url'] = url
        item['date'] = date
        item['typeid'] = tool.get_typeid(item['title'])
        item['senddate'] = int(time.time())
        item['mid'] = 867
        item['nativeplace'] = self.get_nativeplace(item['title'])
        item['infotype'] = tool.get_infotype(item['title'])
        item['body'] = tool.qudiao_width(detail_html)
        item['body'] = item['body'].replace('<a href="http://222.143.135.34:8085/tpbidder" target="_blank"><img src="../Template/Default/images/hybm.jpg"></a>', '').replace('\xa0', '')
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
        item['address'] = tool.get_address(detail_text)
        item['linkman'] = tool.get_linkman(detail_text)
        item['function'] = tool.get_function(detail_text)
        item['resource'] = '焦作市公共资源交易中心'
        item['shi'] = 8508
        item['sheng'] = 8500
        item['removal']= title
        process_item(item)

    def get_nativeplace(self, addr):
        city = ''
        city_list = [['8508.001', '解放区'], ['8508.01', '沁阳'], ['8508.011', '孟州'], ['8508.002', '中站区'], ['8508.003', '马村区'], ['8508.004', '山阳区'], ['8508.005', '修武县'], ['8508.006', '博爱县'], ['8508.007', '武陟县'], ['8508.008', '温县'], ['8508.009', '济源']]

        for i in city_list:
            if i[1] in addr:
                city = float(i[0])
                break
        if city == '':
            city = 8508
        return city

if __name__ == '__main__':
    import os,traceback
    try:
        jl = wenshan_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
        tool.send_error('报错文件：'+str(os.path.basename(__file__))+'报错信息：'+str(e))



