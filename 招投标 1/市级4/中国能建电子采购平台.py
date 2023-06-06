# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 辽宁阳光采购平台
class wenshan_ggzy:
    def __init__(self):
        self.url_list = [
            'https://ec.ceec.net.cn/ajaxpro/CeecBidWeb.HomeInfo.ProjectList,CeecBidWeb.ashx', #招标公告
                    ]
        self.url = self.url_list.pop(0)
        self.headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
         'X-AjaxPro-Method': 'getdata',
         'Sec-Fetch-Site': 'same-origin',
         'Sec-Fetch-Mode': 'cors',
         'Sec-Fetch-Dest': 'empty',
         'Origin': 'https://ec.ceec.net.cn',
         'Host': 'ec.ceec.net.cn',
         'Content-Type': 'text/plain; charset=UTF-8',
         'Connection': 'keep-alive',
         'Accept-Language': 'zh-CN,zh;q=0.9',
         'Accept-Encoding': 'gzip, deflate, br',
         'Accept': '*/*',
         'Cookie': '54668b83ab8146a1a3cad0c2ab0d9a77=WyIyOTc0NzgyMTQ3Il0; HWWAFSESID=799c5886cb19b19913; HWWAFSESTIME=1679445755948',
         'Referer': 'https://ec.ceec.net.cn/HomeInfo/ProjectList.aspx',
         'Content-Length': '95'
}
    def parse(self):
        date = tool.date
        # date = '2020-09-21'
        page = 0
        while True:
            page += 1
            data={"_bigtype_base64":"WgBCAEcARwA=","_smalltype_base64":"aAB3AA==","_pageIndex":page,"_pageSize":20}
            ProjectCode_headers = {
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
                'Connection': 'keep-alive',
                'Content-Length': '37',
                'Content-Type': 'text/plain; charset=UTF-8',
                'Cookie': 'HWWAFSESID=920a079794c244ff2e; HWWAFSESTIME=1679388474037; 54668b83ab8146a1a3cad0c2ab0d9a77=WyI4OTc0Mzg0MDkiXQ; ASP.NET_SessionId=5z2arcxgwcn0ttms1vcfl2cl; CheckCode=6TPD8',
                'Host': 'ec.ceec.net.cn',
                'Origin': 'https://ec.ceec.net.cn',
                'Referer': 'https://ec.ceec.net.cn/HomeInfo/ProjectList.aspx?InfoLevel=MgA=&bigType=WgBCAEcAUwA=',
                'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'same-origin',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
                'X-AjaxPro-Method': 'encode',
            }
            text = tool.requests_post_to(url=self.url,data=data, headers=self.headers)
            page_text = "".join(list(text)[1:]).replace('";/*', '').replace('\\', '').replace('********************','')
            print('*' * 20, page, '*' * 20)
            html = json.loads(page_text)
            # print(11, text)
            # time.sleep(6666)
            detail=html["maindata"][0]
            for li in detail:
                title = li["ZhaoBiaoXMMC"]
                date_Today = li["BaoMingJZSJ"].split(' ')[0].replace('/', '-')
                ZhaoBiaoXMBH = li["ZhaoBiaoXMBH"]
                ProjectCode_data = '{"s":"'+ZhaoBiaoXMBH+'"}'
                ProjectCode_resp = requests.post(url=self.url, headers=ProjectCode_headers, data=ProjectCode_data)
                ProjectCode = "".join(list(ProjectCode_resp.text)[1:]).replace('";/*', '').replace('\\', '')
                url = 'https://ec.ceec.net.cn/ajaxpro/CeecBidWeb.HomeInfo.ZhaoBiaoGG_Details,CeecBidWeb.ashx'
                # print(title, url, date_Today)
                # time.sleep(666)
                # self.parse_detile(title, url, date_Today)
                if tool.Transformation(date) <= tool.Transformation(date_Today):
                    if tool.removal(title, date):
                        self.parse_detile(title, url, date_Today,ProjectCode)
                    else:
                        print('【existence】', url)
                        continue
                else:
                    print('日期不符, 正在切换类型', date_Today)
                    self.url = self.url_list.pop(0)
                    page = 0
                    break
            if page == 20:
                print('日期不符, 正在切换类型')
                self.url = self.url_list.pop(0)
                break

    def parse_detile(self, title, url,date,ProjectCode):
        print(url)
        data2 = {"_vProjectCode_EN": ProjectCode}
        headers2 = {'X-AjaxPro-Method': 'GetZhaoBiaoGG',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
                    'Sec-Fetch-Site': 'same-origin',
                    'Sec-Fetch-Mode': 'cors',
                    'Sec-Fetch-Dest': 'empty',
                    'Referer': f'https://ec.ceec.net.cn/HomeInfo/ZhaoBiaoGG_Details.aspx?zbxmbh={ProjectCode}',
                    'Origin': 'https://ec.ceec.net.cn',
                    'Host': 'ec.ceec.net.cn',
                    'Cookie': '54668b83ab8146a1a3cad0c2ab0d9a77=WyIyOTc0NzgyMTQ3Il0; HWWAFSESID=799c5886cb19b19913; HWWAFSESTIME=1679445755948; ASP.NET_SessionId=ruidbqevwkveaeu1ckss44xu; CheckCode=NDBXP',
                    'Content-Type': 'text/plain; charset=UTF-8',
                    'Content-Length': '87',
                    'Connection': 'keep-alive',
                    'Accept-Language': 'zh-CN,zh;q=0.9',
                    'Accept-Encoding': 'gzip, deflate, br',
                    'Accept': '*/*'
                    }
        t = tool.requests_post_to(url=url,data=data2,headers=headers2)
        page2 = "".join(list(t)[1:]).replace('";/*', '').replace('\\', '')
        # print(page2)
        # print(t)
        # time.sleep(2222)
        url_html = json.loads(page2)
        detail_text =url_html["ZhaoBiaoGG"][0]["GongGaoZW"]
        index_url=f'https://ec.ceec.net.cn/HomeInfo/ZhaoBiaoGG_Details.aspx?zbxmbh={ProjectCode}'
        # print(index_url)
        # detail_html = etree.tostring(detail, method='HTML')
        # detail_html = html.unescape(detail_html.decode()).replace("display: none", '')
        # detail_text = url_html.xpath('string(//div[@class="box"])').replace('\xa0', '').replace('\n', '').\
        #     replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
        if len(detail_text) < 200:
            int('a')
        item = {}
        item['title'] = title.replace('\u2022', '')
        item['url'] = index_url
        item['date'] = date
        item['typeid'] = tool.get_typeid(item['title'])
        item['senddate'] = int(time.time())
        item['mid'] = 867
        item['nativeplace'] = self.get_nativeplace(item['title'])
        item['infotype'] = tool.get_infotype(item['title'])
        item['body'] = detail_text
        # item['body'] = item['body'].replace('''<a href="http://www.hfztb.cn" target="_blank"><img src="../Template/Default/images/wybm.png"></a>''', '')
        # print(item['body'].replace('\xa0', '').replace('\xa5', '').replace('\xb3', ''))
        # time.sleep(6666)
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
        item['resource'] = '辽宁阳光采购平台'
        item['shi'] = 6507
        item['sheng'] = 6500
        item['removal']= title
        # print(item["body"])
        process_item(item)
    def get_nativeplace(self, addr):
        city = ''
        city_list = [['6507.001', '铜官山区'], ['6507.002', '狮子山区'], ['6507.003', '郊区'], ['6507.004', '铜陵县']]

        for i in city_list:
            if i[1] in addr:
                city = float(i[0])
                break
        if city == '':
            city = 6507
        return city

if __name__ == '__main__':
    import os,traceback
    try:
        jl = wenshan_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
        tool.send_error('报错文件：'+str(os.path.basename(__file__))+'报错信息：'+str(e))



