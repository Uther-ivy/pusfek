# -*- coding: utf-8 -*-
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 驻马店市公共资源交易平台
class zhumadian_ggzy:
    def __init__(self):
        self.url_list = [
            # 建设工程
            # 招标公告
            # 'http://www.zmdggzy.gov.cn/TPFront/jyxx/003001/003001001/',
            # 变更公告
            # 'http://www.zmdggzy.gov.cn/TPFront/jyxx/003001/003001003/',
            # 结果异常
            # 'http://www.zmdggzy.gov.cn/TPFront/jyxx/003001/003001004/',
            # 中标候选人
            # 'http://www.zmdggzy.gov.cn/TPFront/jyxx/003001/003001005/',
            # 政府采购
            # 采购公告
            # 'http://www.zmdggzy.gov.cn/TPFront/jyxx/003002/003002001/',
            # 变更公告
            # 'http://www.zmdggzy.gov.cn/TPFront/jyxx/003002/003002003/',
            # 结果公告
            # 'http://www.zmdggzy.gov.cn/TPFront/jyxx/003002/003002004/',
            # 异常公告
            # 'http://www.zmdggzy.gov.cn/TPFront/jyxx/003002/003002005/'
           '/TPFront/jyxx/003001/003001006/003001006001',
            '/TPFront/jyxx/003001/003001006/003001006002',
            '/TPFront/jyxx/003001/003001006/003001006003',
            '/TPFront/jyxx/003001/003001006/003001006004',
            '/TPFront/jyxx/003001/003001006/003001006005',
            '/TPFront/jyxx/003001/003001006/003001006006',
            '/TPFront/jyxx/003001/003001006/003001006007',
            '/TPFront/jyxx/003001/003001006/003001006008',
            '/TPFront/jyxx/003001/003001006/003001006009',
            '/TPFront/jyxx/003001/003001006/003001006010'
        ]

        self.headers = {
            'Cookie': 'ASP.NET_SessionId=nda2ju5nkvbrcknjl3d45izz',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        }

    def parse(self):

        date = tool.date
        # date = '2020-03-20'
        page=0
        while True:
            href= self.url_list.pop()
            while True:
                page+=1
                print('*'*20,page,'*'*20)

                url='https://ggzy.zhumadian.gov.cn'+href+f'?pageing={page}'
                print(url)
                text = tool.requests_get_GBK(url, self.headers)
                html = HTML(text)

                detail = html.xpath("//ul[@class='ewb-data-item']/li")
                # time.sleep(666)
                if detail:
                    for j in detail:
                        try:
                            title = j.xpath('./div/a/text()')[0].replace('\n', '').replace('\r', '').replace('\t', '').replace(' ', '')
                            url = 'https://ggzy.zhumadian.gov.cn/' + j.xpath('./div/a/@href')[0]
                            date_Today = j.xpath('./span/text()')[0].replace('\n', '').replace('\r', '').replace('\t', '').replace(' ', '')
                            print(title, url, date_Today)
                            # time.sleep(666)
                            if '测试' in title:
                                continue
                            if tool.Transformation(date) <= tool.Transformation(date_Today):
                                # if tool.removal(title, date):
                                self.parse_detile(title, url, date_Today)
                            # else:
                            # print('【existence】', url)
                            # continue
                            else:
                                print('日期不符', date_Today)
                                break

                        except Exception as e:
                            traceback.print_exc()
                else:
                    page=0
                    break
    def parse_detile(self, title, url, date):
        print(url)
        url_html = etree.HTML(tool.requests_get_GBK(url, self.headers))
        detail = url_html.xpath('//*[@id="mainContent"]')[0]
        detail_html = etree.tostring(detail, method='HTML')
        detail_html = html.unescape(detail_html.decode()).replace('\xa0', '').replace('\ufeff', '')
        detail_text = url_html.xpath('string(//*[@id="mainContent"])') \
            .replace('\xa0', '').replace('\n', '').replace('\r', '').replace('\t', '') \
            .replace(' ', '').replace('\xa5', '').replace('\ufeff', '')
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
        item['resource'] = '驻马店市公共资源交易平台'
        item['shi'] = 8517
        item['sheng'] = 8500
        item['removal']= title
        process_item(item)
        # print(item['body'])
    def get_nativeplace(self, addr):
        city = ''
        city_list = [['8517.001', '驿城区'], ['8517.01', '新蔡县'], ['8517.002', '西平县'], ['8517.003', '上蔡县'], ['8517.004', '平舆县'], ['8517.005', '正阳县'], ['8517.006', '确山县'], ['8517.007', '泌阳县'], ['8517.008', '汝南县'], ['8517.009', '遂平县']]

        for i in city_list:
            if i[1] in addr:
                city = float(i[0])
                break
        if city == '':
            city = 8517
        return city
if __name__ == '__main__':
    import traceback,os
    jl = zhumadian_ggzy()
    jl.parse()
    try:
        jl = zhumadian_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
        tool.send_error('报错文件：'+str(os.path.basename(__file__))+'报错信息：'+str(e))


