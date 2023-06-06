# -*- coding: utf-8 -*-
import json
import re
import time, html
from lxml import etree
import tool
from save_database import process_item

# 全国公共资源交易平台(承德市)
class alashan_ggzy:
    def __init__(self):
        self.url_code = [
            # 'http://xzspj.chengde.gov.cn/ggzy/jyxx/jsgcZbgg?currentPage={}&area=004&secondArea=000&industriesTypeCode=000&tenderProjectCode=&bulletinName=&startTime=&endTime=',
            # 'http://xzspj.chengde.gov.cn/ggzy/jyxx/jsgcBgtz?currentPage={}&area=004&secondArea=000&industriesTypeCode=000&tenderProjectCode=&bulletinName=&startTime=&endTime=',
            # 'http://xzspj.chengde.gov.cn/ggzy/jyxx/jsgczbhxrgs?currentPage={}&area=004&secondArea=000&industriesTypeCode=000&tenderProjectCode=&bulletinName=&startTime=&endTime=',
            'http://xzspj.chengde.gov.cn/ggzy/jyxx/jsgcZbjggs?currentPage={}&area=004&secondArea=000&industriesTypeCode=000&tenderProjectCode=&bulletinName=&startTime=&endTime=',
            # 'http://xzspj.chengde.gov.cn/ggzy/jyxx/zfcg/cggg?currentPage={}&area=004&secondArea=000&industriesTypeCode=&purchaseProjectCode=&bulletinTitle=&startTime=&endTime=',
            # 'http://xzspj.chengde.gov.cn/ggzy/jyxx/zfcg/gzsx?currentPage={}&area=004&secondArea=000&industriesTypeCode=&purchaseProjectCode=&bulletinTitle=&startTime=&endTime=',
            # 'http://xzspj.chengde.gov.cn/ggzy/jyxx/zfcg/zbjggs?currentPage={}&area=004&secondArea=000&industriesTypeCode=&purchaseProjectCode=&bulletinTitle=&startTime=&endTime=',
            # 'http://xzspj.chengde.gov.cn/ggzy/jyxx/fbzzgs?currentPage={}&area=004&secondArea=000&bulletinType=1&bulletinTitle=&startTime=&endTime=',
        ]
        self.url = self.url_code.pop(0)
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Cookie': 'homeid=3d38fa73-5381-4cb3-bdf4-4a6060d74256',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
        }

    def parse(self):
        date = tool.date
        # date = '2020-01-06'
        page = 50
        while True:
            page += 1
            print('*' * 20, page, '*' * 20)
            text = tool.requests_get(self.url.format(page), self.headers)
            detail = etree.HTML(text).xpath('//*[@id="p2"]/tr')
            for li in detail[1:]:
                try:
                    try:
                        title = li.xpath('./td[3]/a/@title')[0].replace('\r', '').replace('\t', '').replace(' ', '').replace('\n', '').replace('\xa0', '')
                        url = 'http://xzspj.chengde.gov.cn' + li.xpath('./td[3]/a/@href')[0]
                    except:
                        continue
                    date_Today = li.xpath('./td[4]/text()')[0].replace('\r', '').replace('\t', '').replace(' ', '').replace('\n', '').replace('发布于', '')
                    # print(title, url, date_Today)
                    # time.sleep(666)
                    if tool.Transformation(date) <= tool.Transformation(date_Today):
                        # if tool.removal(title, date):
                            self.parse_detile(title, url, date_Today)
                        # else:
                        #     print('【existence】', url)
                        #     continue
                    else:
                        print('日期不符, 正在切换类型...', date_Today, self.url)
                        return
                except Exception as e:
                    traceback.print_exc()
    def parse_detile(self, title, url, date):
        print(url)
        url_text = tool.requests_get(url, self.headers)
        url_html = etree.HTML(url_text)
        try:
            detail = url_html.xpath('//div[@class="detailDetail"]')[0]
            detail_html = etree.tostring(detail, method='HTML')
            detail_html = html.unescape(detail_html.decode())
            detail_text = url_html.xpath('string(//div[@class="detailDetail"])').replace('\xa0', '').replace('\n', '').replace('\r', '').replace('\t',
                                                                                                                      '').replace(
                ' ', '').replace('\xa5', '')
        except:
            detail = url_html.xpath('//*[@class="infro_table"]')[0]
            detail_html = etree.tostring(detail, method='HTML')
            detail_html = html.unescape(detail_html.decode())
            detail_text = url_html.xpath('string(//*[@class="infro_table"])').replace('\xa0',
                                                                                                            '').replace(
                '\n', '').replace('\r', '').replace('\t',
                                                    '').replace(
                ' ', '').replace('\xa5', '')
        item = {}
        item['title'] = title.replace('\u2022', '')
        item['url'] = url
        item['date'] = date
        item['typeid'] = tool.get_typeid(item['title'])
        item['senddate'] = int(time.time())
        item['mid'] = 867
        item['nativeplace'] = self.get_nativeplace(item['title']+detail_text)
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
        item['resource'] = '全国公共资源交易平台(承德市)'
        item['shi'] = 2008
        item['sheng'] = 2000
        item['removal']= title
        process_item(item)
        # print(item['nativeplace'], item['title'])

    def get_nativeplace(self, addr):
        city_list = [['2008', '承德市'], ['2008.001', '双桥区'], ['2008.01', '宽城满族自治'], ['2008.011', ' 围场满族蒙古族自治县'], ['2008.002', '双滦区'], ['2008.003', '鹰手营子矿区'], ['2008.004', '承德县'], ['2008.005', '兴隆县'], ['2008.006', '平泉县'], ['2008.007', '滦平县'], ['2008.008', '隆化县'], ['2008.009', '丰宁满族自治县']]

        for i in city_list:
            if i[1] in addr:
                return float(i[0])
        return 2008

if __name__ == '__main__':
    import traceback, os
    try:
        jl = alashan_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
        tool.send_error('报错文件：'+str(os.path.basename(__file__))+'报错信息：'+str(e))

