# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 上海市建设工程交易服务中心
class shanghai_jsgc:
    def __init__(self):
        self.url_list = [
            # 'https://ciac.zjw.sh.gov.cn/NetInterBidweb/GKTB/SgfbZbxx.aspx',
        #                  'https://ciac.zjw.sh.gov.cn/XmZtbbaWeb/Gsqk/GsFbList.aspx',
                         'https://ciac.zjw.sh.gov.cn/XmZtbbaWeb/gsqk/ZbjgGkList.aspx'
                         ]
        self.url = self.url_list.pop(0)
        self.headers = {
            'Cookie': 'AlteonP=AUVcXqXdHKwyLHhgcsiQOA$$; SsoCookierYzm=2wal',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
        }

    def parse(self):
        date = tool.date
        # date = '2020-01-14'
        page = 0
        data = {
            '_EVENTTARGET': '',
            '__EVENTARGUMENT': '',
            '__VIEWSTATE': '1',
            '__VIEWSTATEGENERATOR': '2',
            '__EVENTVALIDATION': '3',
            'dr_gglb': '0',
            'txt_beginTime': '',
            'txt_endTime': '',
            'nextPages': '下一页',
            'DropDownList_page': page-1,
            'hdInputNum': '1',
            'hdPageCount': '5',
            'hdState': ''
        }
        data_to = {
            '__EVENTTARGET': 'gvList',
            '__EVENTARGUMENT': 'Page$',
            '__VIEWSTATE': '1',
            '__VIEWSTATEGENERATOR': '2',
            '__EVENTVALIDATION': '3',
            'ddlZblx': '',
            'txtgsrq': '',
            'txtTogsrq': '',
            'txttbr': '',
            'txtzbhxr': '',
            'txtxmmc': '',
        }
        data_san = {
            '__EVENTTARGET': 'gvZbjgGkList',
            '__EVENTARGUMENT': 'Page$3',
            '__VIEWSTATE': '1',
            '__VIEWSTATEGENERATOR': '2',
            '__EVENTVALIDATION': '3',
            'ddlZblx': '',
            'txtZbrqBegin': '',
            'txtZbrqEnd': '',
            'txtZbr': '',
        }
        while True:
            page += 1
            print('*' * 20, page, '*' * 20)
            if page == 1:
                text = tool.requests_get(self.url, self.headers)
                html = HTML(text)
            else:
                if 'SgfbZbxx' in self.url:
                    text = tool.requests_post(self.url, data, self.headers)
                    html = HTML(text)
                elif 'GsFbList' in self.url:
                    text = tool.requests_post(self.url, data_to, self.headers)
                    html = HTML(text)
                else:
                    text = tool.requests_post(self.url, data_san, self.headers)
                    html = HTML(text)
                print(data_to, text)
                time.sleep(6666)
            if 'SgfbZbxx' in self.url:
                data['__VIEWSTATE'] = html.xpath('//*[@id="__VIEWSTATE"]/@value')[0]
                data['__VIEWSTATEGENERATOR'] = html.xpath('//*[@id="__VIEWSTATEGENERATOR"]/@value')[0]
                data['__EVENTVALIDATION'] = html.xpath('//*[@id="__EVENTVALIDATION"]/@value')[0]
                data['DropDownList_page'] = page
                detail = html.xpath('//*[@id="form1"]/div[3]/table/tbody/tr/td/table[3]/tbody/tr')
            elif 'GsFbList' in self.url:
                data_to['__VIEWSTATE'] = html.xpath('//*[@id="__VIEWSTATE"]/@value')[0]
                data_to['__EVENTARGUMENT'] = 'Page$' + str(page+1)
                data_to['__VIEWSTATEGENERATOR'] = html.xpath('//*[@id="__VIEWSTATEGENERATOR"]/@value')[0]
                data_to['__EVENTVALIDATION'] = html.xpath('//*[@id="__EVENTVALIDATION"]/@value')[0]
                detail = html.xpath('//*[@id="gvList"]/tr')
            else:
                data_san['__VIEWSTATE'] = html.xpath('//*[@id="__VIEWSTATE"]/@value')[0]
                data_san['__EVENTARGUMENT'] = 'Page$' + str(page+1)
                data_san['__VIEWSTATEGENERATOR'] = html.xpath('//*[@id="__VIEWSTATEGENERATOR"]/@value')[0]
                data_san['__EVENTVALIDATION'] = html.xpath('//*[@id="__EVENTVALIDATION"]/@value')[0]
                detail = html.xpath('//*[@id="gvZbjgGkList"]/tr')
                # print(111, text)
                # time.sleep(666)
            for i in range(1, len(detail)):
                if 'SgfbZbxx' in self.url:
                    title = html.xpath('//*[@id="form1"]/div[3]/table/tbody/tr/td/table[3]/tbody/tr[{}]/td[2]/a/span/text()'
                               .format(i+1))[0].replace('\n', '').replace('\r', '').replace('\t', '').replace(' ', '')
                    url = 'https://ciac.zjw.sh.gov.cn/NetInterBidweb/GKTB/DefaultV2019.aspx?gkzbXh={}'.format(
                        html.xpath('//*[@id="form1"]/div[3]/table/tbody/tr/td/table[3]/tbody/tr[{}]/td[2]/a/@onclick'
                               .format(i+1))[0].replace('openWindow(', '').replace(')', '').replace("'", '').split(',')[0])

                    date_Today = html.xpath('//*[@id="form1"]/div[3]/table/tbody/tr/td/table[3]/tbody/tr[{}]/td[3]/a/text()'
                    .format(i+1))[0].replace('\n', '').replace('\r', '').replace('\t', '').replace(' ', '').replace('/', '-')
                    print(title, url, date_Today)
                    # time.sleep(666)
                elif 'GsFbList' in self.url:
                    try:
                        title = html.xpath('//*[@id="gvList"]/tr[{}]/td[1]/a/text()'.format(i + 1))[0]
                        url = 'https://ciac.zjw.sh.gov.cn/XmZtbbaWeb/Gsqk/GsFb2015.aspx?zbdjid=&zbid={}&gsid=&gsmn=' \
                            .format(html.xpath('//*[@id="gvList"]/tr[{}]/td[1]/a/@onclick'.format(i + 1))[0]
                                    .replace('ShowGs(', '').replace(');', '').replace('"', '').split(',')[0])
                        date_Today = html.xpath('//*[@id="gvList"]/tr[{}]/td[2]/span/text()'.format(i + 1))[0] \
                            .replace('年', '-').replace('月', '-').replace('日', '')
                        # print(title, url, date_Today)
                    except:
                        continue
                else:
                    try:
                        title = html.xpath('//*[@id="gvZbjgGkList"]/tr[{}]/td[2]/a/text()'.format(i+1))[0]
                        url = 'https://ciac.zjw.sh.gov.cn/XmZtbbaWeb/gsqk/ZbjgGkList.aspx'
                        code = html.xpath('//*[@id="gvZbjgGkList"]/tr[{}]/td[2]/a/@href'.format(i+1))[0]\
                            .replace("javascript:__doPostBack('", '').replace("','')", '')
                        data_si = {
                            '__EVENTTARGET': code,
                            '__EVENTARGUMENT': '',
                            '__VIEWSTATE': html.xpath('//*[@id="__VIEWSTATE"]/@value')[0],
                            '__VIEWSTATEGENERATOR': html.xpath('//*[@id="__VIEWSTATEGENERATOR"]/@value')[0],
                            '__EVENTVALIDATION': html.xpath('//*[@id="__EVENTVALIDATION"]/@value')[0]
                        }
                        text = tool.requests_post(url, data_si, self.headers)
                        html_to = HTML(text)
                        url = 'https://ciac.zjw.sh.gov.cn/XmZtbbaWeb/gsqk' + html_to.xpath('//*[@id="form1"]/@action')[0][1:]
                        date_Today = html.xpath('//*[@id="gvZbjgGkList"]/tr[{}]/td[3]/text()'.format(i + 1))[0]\
                            .replace('年', '-').replace('月', '-').replace('日', '').replace('\n', '').replace('\r', '')\
                            .replace('\t', '').replace(' ', '')
                        # print(title, url, code, date_Today)
                        # time.sleep(666)
                    except:
                        continue
                if tool.Transformation(date) <= tool.Transformation(date_Today):
                    if tool.removal(title, date):
                        if self.parse_detile(title, url, date_Today) == '1':
                            continue
                    else:
                        print('【existence】', url)
                        continue
                else:
                    print('日期不符, 正在切换类型...', date_Today)
                    return

    def parse_detile(self, title, url, date):
        print(url)
        text = tool.requests_get(url, self.headers)
        if '访问的页面不存在' in text:
            return '1'
        url_html = etree.HTML(text)
        try:
            detail = url_html.xpath('//*[@id="aspnetForm"]/div[2]/table/tr[2]/td/table')[0]
            detail_html = etree.tostring(detail, method='HTML')
            detail_html = html.unescape(detail_html.decode())
            detail_text = url_html.xpath('string(//*[@id="aspnetForm"]/div[2]/table/tr[2]/td/table)')\
                .replace('\xa0', '').replace('\n', '').replace('\r', '').replace('\t', '').replace(' ', '')\
                .replace('\xa5', '')
        except:
            try:
                detail = url_html.xpath('//*[@id="form1"]/div[3]/div/table')[0]
                detail_html = etree.tostring(detail, method='HTML')
                detail_html = html.unescape(detail_html.decode())
                detail_text = url_html.xpath('string(//*[@id="form1"]/div[3]/div/table)') \
                    .replace('\xa0', '').replace('\n', '').replace('\r', '').replace('\t', '').replace(' ', '') \
                    .replace('\xa5', '')
            except:
                detail = url_html.xpath('//*[@id="ggTbxx"]')[0]
                detail_html = etree.tostring(detail, method='HTML')
                detail_html = html.unescape(detail_html.decode())
                detail_text = url_html.xpath('string(//*[@id="ggTbxx"])') \
                    .replace('\xa0', '').replace('\n', '').replace('\r', '').replace('\t', '').replace(' ', '') \
                    .replace('\xa5', '')

        print(detail_text.replace('\xa0','').replace('\xa5',''))
        # time.sleep(6666)
        item = {}
        item['title'] = title.replace('\u2022', '')
        item['url'] = url
        item['date'] = date
        item['typeid'] = tool.get_typeid(item['title'])
        item['senddate'] = int(time.time())
        item['mid'] = 867
        item['nativeplace'] = self.get_nativeplace(item['title'])
        item['infotype'] = tool.get_infotype(item['title'])
        item['body'] = detail_html
        width_list = re.findall('width="(.*?)"', item["body"])
        for i in width_list:
            item["body"] = item["body"].replace('width="{}"'.format(i), '')
        width_list = re.findall('WIDTH: (.*?)pt;', item["body"])
        for i in width_list:
            item["body"] = item["body"].replace('WIDTH: {}pt;'.format(i), '')
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
        item['winner'] = tool.get_winner(detail_text)
        item['address'] = tool.get_address(detail_text)
        item['linkman'] = tool.get_linkman(detail_text)
        item['function'] = tool.get_function(detail_text)
        item['resource'] = '上海市建设工程交易服务中心'
        item['shi'] = int(str(item["nativeplace"]).split('.')[0])
        item['sheng'] = 5000
        item['removal']= title
        process_item(item)

    def get_nativeplace(self, addr):
        city = ''
        city_list = [['5001', '黄浦区'], ['5002', '卢湾区'], ['5003', '徐汇区'], ['5004', '长宁区'], ['5005', '静安区'], ['5006', '普陀区'], ['5007', '闸北区'], ['5008', '虹口区'], ['5009', '杨浦区'], ['5010', '闵行区'], ['5011', '宝山区'], ['5012', '嘉定区'], ['5013', '浦东新区'], ['5014', '金山区'], ['5015', '松江区'], ['5016', '青浦区'], ['5017', '南汇区'], ['5018', '奉贤区'], ['5019', '崇明县']]

        for i in city_list:
            if i[1] in addr:
                city = float(i[0])
                break
        if city == '':
            city = 5000
        return city
if __name__ == '__main__':

    import traceback, os
    try:
        jl = shanghai_jsgc()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
        tool.send_error('报错文件：'+str(os.path.basename(__file__))+'报错信息：'+str(e))



