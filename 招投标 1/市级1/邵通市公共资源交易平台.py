# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 邵通市公共资源交易平台
class baoshan_ggzy:
    def __init__(self):
        self.url_list = [
            # 市本级
            #   工程建设
            #       招标公告
            ['http://ztggzyjy.zt.gov.cn/jyxx/jsgcZbgg?currentPage={}','//*[@id="zbggForm"]/div[3]/table/tr'],
            #       变更公告
            ['http://ztggzyjy.zt.gov.cn/jyxx/jsgcBgtz?currentPage={}','//*[@id="bgtzForm"]/div[2]/table/tr'],
            #       评标结果公示
            ['http://ztggzyjy.zt.gov.cn/jyxx/jsgcpbjggs?currentPage={}','//*[@id="zbggForm"]/div[2]/table/tr'],
            #       中标结果
            ['http://ztggzyjy.zt.gov.cn/jyxx/jsgcZbjggs?currentPage={}','//*[@id="zbggForm"]/div[3]/table/tr'],
            #       异常公告
            ['http://ztggzyjy.zt.gov.cn/jyxx/jsgcZbyc?currentPage={}','//*[@id="ycggForm"]/div[2]/table/tr'],
            #   政府采购
            #       采购公告
            ['http://ztggzyjy.zt.gov.cn/jyxx/zfcg/cggg?currentPage={}','//*[@id="zbggForm"]/div[2]/table/tr'],
            #       变更通知
            ['http://ztggzyjy.zt.gov.cn/jyxx/zfcg/gzsx?currentPage={}','//*[@id="zbggForm"]/div[2]/table/tr'],
            #       结果公示
            ['http://ztggzyjy.zt.gov.cn/jyxx/zfcg/zbjggs?currentPage={}','//*[@id="zbggForm"]/div[2]/table/tr'],
            #       异常公示
            ['http://ztggzyjy.zt.gov.cn/jyxx/zfcg/zfcgYcgg?currentPage={}','//*[@id="ycggForm"]/div[2]/table/tr']
        ]
        self.url = self.url_list.pop(0)
        self.headers = {
            'Cookie': 'homeid=1a444a31-e460-47ff-9931-1c075c0f3cd8',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        }

    def parse(self):
        date = tool.date
        # date = '2020-04-07'
        page = 0
        while True:
            page += 1
            text = tool.requests_get(self.url[0].format(page), self.headers)
            print('*' * 20, page, '*' * 20)
            html = HTML(text)
            # print(11, res)
            # time.sleep(6666)
            detail = html.xpath(self.url[1])
            for i in range(1, len(detail)):
                try:
                    title = html.xpath(self.url[1] + '[{}]/td[3]/a/@title'.format(i+1))[0]
                    url = 'http://ztggzyjy.zt.gov.cn' + html.xpath(self.url[1] + '[{}]/td[3]/a/@href'.format(i + 1))[0]
                    date_Today = html.xpath(self.url[1] + '[{}]/td[4]/text()'.format(i + 1))[0]
                    if '招标' in date_Today or '采购' in date_Today:
                        date_Today = html.xpath(self.url[1] + '[{}]/td[5]/text()'.format(i + 1))[0]
                    if title == '':
                        title = html.xpath(self.url[1] + '[{}]/td[3]/@title'.format(i+1))[0]
                except:
                    title = html.xpath(self.url[1] + '[{}]/td[4]/a/@title'.format(i + 1))[0]
                    url = 'http://ztggzyjy.zt.gov.cn' + html.xpath(self.url[1] + '[{}]/td[4]/a/@href'.format(i + 1))[0]
                    date_Today = html.xpath(self.url[1] + '[{}]/td[5]/text()'.format(i + 1))[0]
                    if title == '':
                        title = html.xpath(self.url[1] + '[{}]/td[4]/@title'.format(i+1))[0]
                if '测试' in title:
                    continue
                # print(title, url, date_Today)
                # time.sleep(666)
                if tool.Transformation(date) <= tool.Transformation(date_Today):
                    if tool.removal(title, date):
                        self.parse_detile(title, url, date_Today)
                    else:
                        print('【existence】', url)
                        continue
                else:
                    print('日期不符, 正在切换类型', date_Today)
                    self.url = self.url_list.pop(0)
                    page = 0
                    break
            if page == 20:
                self.url = self.url_list.pop(0)
                break
    def parse_detile(self, title, url, date):
        print(url)
        url_html = etree.HTML(tool.requests_get(url, self.headers))
        try:
            detail = url_html.xpath('/html/body/div[2]/div[1]/div/div[2]/div[3]')[0]
            detail_html = etree.tostring(detail, method='HTML')
            detail_html = html.unescape(detail_html.decode())
            detail_text = url_html.xpath('string(/html/body/div[2]/div[1]/div/div[2]/div[3])').replace('\xa0', '').replace('\n', '').\
                replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
        except:
            try:
                detail = url_html.xpath('/html/body/div[2]/div/div/div[2]/table')[0]
                detail_html = etree.tostring(detail, method='HTML')
                detail_html = html.unescape(detail_html.decode())
                detail_text = url_html.xpath('string(/html/body/div[2]/div/div/div[2]/table)').replace('\xa0',
                                                                                                           '').replace('\n',
                                                                                                                       ''). \
                    replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
                if len(detail) < 1000:
                    int('a')
            except:
                detail = url_html.xpath('/html/body/div[2]/div/div/div[2]')[0]
                detail_html = etree.tostring(detail, method='HTML')
                detail_html = html.unescape(detail_html.decode())
                detail_text = url_html.xpath('string(/html/body/div[2]/div/div/div[2])').replace('\xa0',
                                                                                                       '').replace('\n',
                                                                                                                   ''). \
                    replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
        # print(detail_text.replace('\xa0','').replace('\xa5',''))
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
        item['winner'] = tool.get_winner(detail_text)
        item['address'] = tool.get_address(detail_text)
        item['linkman'] = tool.get_linkman(detail_text)
        item['function'] = tool.get_function(detail_text)
        item['resource'] = '邵通市公共资源交易平台'
        item['shi'] = 13005
        item['sheng'] = 13000
        item['removal']= title
        process_item(item)

    def get_nativeplace(self, addr):
        city = ''
        city_list = [['13005.001', '昭阳区'], ['13005.01', '威信县'], ['13005.011', '水富县'], ['13005.002', '鲁甸县'], ['13005.003', '巧家县'], ['13005.004', '盐津县'], ['13005.005', '大关县'], ['13005.006', '永善县'], ['13005.007', '绥江县'], ['13005.008', '镇雄县'], ['13005.009', '彝良县']]
        for i in city_list:
            if i[1] in addr:
                city = float(i[0])
                break
        if city == '':
            city = 13005
        return city

if __name__ == '__main__':
    import traceback, os
    try:
        jl = baoshan_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
        tool.send_error('报错文件：'+str(os.path.basename(__file__))+'报错信息：'+str(e))


