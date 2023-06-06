# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 成都轨道集团电子采购
class wenshan_ggzy:
    def __init__(self):
        self.domain_name = 'https://ep.cdmetro.cn:1443'
        self.url_list = [
            '0000000000000201',
            '0000000000000202'
        ]
        self.url = self.url_list.pop(0)
        self.headers = {
            'Accept': 'application/json, text/javascript, */*',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Cookie': 'JSESSIONID=wFkLfsChTa700RX-Dsu1rA5KsEIECUcZ8YGuU52QQnOe8yMm1G8K!-1296881825',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',

        }

    def parse(self):
        date = tool.date
        # date = '2020-09-27'
        page = 0
        url_to = 'https://ep.cdmetro.cn:1443/suneps/EiService'

        while True:
            page += 1
            data = {
                'service': 'NE9001',
                'method': 'query',
                'eiinfo': '{attr:{"efFormEname":"NE9001","efFormCname":"概览列表","efFormPopup":"","efFormTime":"","efCurFormEname":"NE9001","efCurButtonEname":"","packageName":"","serviceName":"NE9001","methodName":"initLoad","efFormInfoTag":"","efFormLoadPath":"/NE/NE9001.jsp","efFormButtonDesc":"{\\"msg\\":\\"\\",\\"msgKey\\":\\"\\",\\"detailMsg\\":\\"\\",\\"status\\":0,\\"blocks\\":{}}","code":"'+self.url+'","query":"  查 询  ","":"跳转","ef_grid_result_jumpto":"2","perPageRecord":"10","limit":10,"offset":10,"currentPage":'+str(page)+'},blocks:{inqu_status:{attr:{},meta:{attr:{},columns:[{name:"title",descName:"",type:"C"},{name:"startRecCreateTime",descName:"",type:"C"},{name:"endRecCreateTime",descName:"",type:"C"}]},rows:[["","",""]]}}}'
            }
            if page == 1:
                text = tool.requests_get('https://ep.cdmetro.cn:1443/suneps/DispatchAction.do?efFormEname=NE9001&code='+self.url, self.headers)
                text = re.findall('var __ei=(.*?);', text, re.S)[0]
            else:
                text = tool.requests_post(url_to, data, self.headers)
            detail = json.loads(text)['blocks']['edit']['rows']
            print('*' * 20, page, '*' * 20)
            # print(11, text.replace('\ufffd', ' ').replace('\u30fb', ' '))
            # time.sleep(6666)
            for li in detail:
                title = li[2].replace('\xa0', '').replace('\n', ''). \
                    replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '').replace("<fontstyle='color:red'>(网)</font>", '')
                url = 'https://ep.cdmetro.cn:1443/suneps/DispatchAction.do?efFormEname=NE9003&code=0000000000000201&articleId={}&columnId={}'.format(li[0], li[1])
                date_Today = li[5].replace('\xa0', '').replace('\n', ''). \
                    replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '') \
                    .replace('[', '').replace(']', '').replace('/', '-')
                date_Today = date_Today[:4] + '-' + date_Today[4:6] + '-' + date_Today[6:]
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
        detail = url_html.xpath('//*[@id="wrapper1"]/div[4]/div[1]/dl/div')[0]
        detail_html = etree.tostring(detail, method='HTML')
        detail_html = html.unescape(detail_html.decode()).replace("display: none", '').replace("\u2022", '').replace('\xa0', '')
        detail_text = url_html.xpath('string(//*[@id="wrapper1"]/div[4]/div[1]/dl/div)').replace('\xa0', '').replace('\n',
                                                                                                             ''). \
            replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
        if len(detail_html) < 200:
            int('a')
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
        item['resource'] = '成都轨道集团电子采购'
        item['shi'] = int(item['nativeplace'])
        item['sheng'] = 12000
        item['removal']= title
        process_item(item)

    def get_nativeplace(self, addr):
        city = ''
        city_list = [['12001.001', '锦江区'], ['12001.01', '金堂县'], ['12001.011', '双流县'], ['12001.012', '郫县'], ['12001.013', '大邑县'], ['12001.014', '蒲江县'], ['12001.015', '新津县'], ['12001.016', '都江堰'], ['12001.017', '彭州'], ['12001.018', '邛崃'], ['12001.019', '崇州'], ['12001.002', '青羊区'], ['12001.003', '金牛区'], ['12001.004', '武侯区'], ['12001.005', '成华区'], ['12001.006', '龙泉驿区'], ['12001.007', '青白江区'], ['12001.008', '新都区'], ['12001.009', '温江区']]

        for i in city_list:
            if i[1] in addr:
                city = float(i[0])
                break
        if city == '':
            city = 12000
        return city

if __name__ == '__main__':
    import os,traceback
    try:
        jl = wenshan_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
        tool.send_error('报错文件：'+str(os.path.basename(__file__))+'报错信息：'+str(e))



