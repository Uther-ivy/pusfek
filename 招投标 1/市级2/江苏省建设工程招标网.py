# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 江苏省建设工程招标网
class xinyang_ggzy:
    def __init__(self):
        self.url_list = [
            'http://www.jszb.com.cn/JSZB/YW_info/ZhaoBiaoGG/MoreInfo_ZBGG.aspx?categoryNum=012'
        ]
        self.url = self.url_list.pop(0)
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        }

    def parse(self):
        date = tool.date
        # date = '2020-07-10'
        page = 0
        data = {
            '__EVENTTARGET': 'MoreInfoList1$Pager',
            '__EVENTARGUMENT': '2',
            '__LASTFOCUS': '',
            '__VIEWSTATE': '',
            '__VIEWSTATEGENERATOR': '76D0A3AC',
            '__VIEWSTATEENCRYPTED': '',
            '__EVENTVALIDATION': '11',
            'MoreInfoList1$txtProjectName': '',
            'MoreInfoList1$txtBiaoDuanName': '',
            'MoreInfoList1$txtBiaoDuanNo': '',
            'MoreInfoList1$txtJSDW': '',
            'MoreInfoList1$StartDate': '',
            'MoreInfoList1$EndDate': '',
            'MoreInfoList1$jpdDi': '-1',
            'MoreInfoList1$jpdXian': '-1'
        }
        while True:
            page += 1
            if page == 1:
                text = tool.requests_get_bm(self.url, self.headers)
            else:
                text = tool.requests_post_bm(self.url, data, self.headers)
            html = HTML(text)
            data['__EVENTARGUMENT'] = str(page+1)
            data['__VIEWSTATE'] = html.xpath('//*[@id = "__VIEWSTATE"]/@value')[0]
            data['__EVENTVALIDATION'] = html.xpath('//*[@id = "__EVENTVALIDATION"]/@value')[0]
            # print(11, text)
            # time.sleep(666)
            detail = html.xpath('//*[@id="MoreInfoList1_DataGrid1"]/tr')
            print('*' * 20, page, '*' * 20)
            for li in detail:
                title = li.xpath('./td[2]/a/@title')[0]
                url = 'http://www.jszb.com.cn/JSZB/YW_info' + re.findall('"..(.*?)","",', li.xpath('./td[2]/a/@onclick')[0])[0]
                # url = li.xpath('./td[2]/a/@onclick')[0]
                date_Today = li.xpath('./td[4]/text()')[0].replace('\n', '').replace('\t', '').replace('\r', '').replace(' ', '')
                # print(title, url, date_Today)
                # time.sleep(666)
                if '测试' in title:
                    continue
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
        url_html = HTML(tool.requests_get_GBK(url,self.headers))
        try:
            detail = url_html.xpath('//*[@id="Table1"]')[0]
            detail_html = etree.tostring(detail, method='HTML')
            detail_html = html.unescape(detail_html.decode()).replace('\xa0', '').replace('\ufeff', '')
            detail_text = url_html.xpath('string(//*[@id="Table1"])') \
                .replace('\xa0', '').replace('\n', '').replace('\r', '').replace('\t', '') \
                .replace(' ', '').replace('\xa5', '').replace('\ufeff', '')
        except:
            detail = url_html.xpath('//*[@id="zygg_kkk"]/table')[0]
            detail_html = etree.tostring(detail, method='HTML')
            detail_html = html.unescape(detail_html.decode()).replace('\xa0', '').replace('\ufeff', '')
            detail_text = url_html.xpath('string(//*[@id="zygg_kkk"]/table)') \
                .replace('\xa0', '').replace('\n', '').replace('\r', '').replace('\t', '') \
                .replace(' ', '').replace('\xa5', '').replace('\ufeff', '')
        # print(detail_text)
        # time.sleep(6666)
        item = {}
        item['title'] = title.replace('\u2022', '')
        item['url'] = url
        item['date'] = date
        item['typeid'] = tool.get_typeid(item['title'])
        item['senddate'] = int(time.time())
        item['mid'] = 867
        item['infotype'] = tool.get_infotype(item['title'])
        item['body'] = tool.qudiao_width(detail_html)
        # print(detail_html)
        # time.sleep(666)
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
        item['nativeplace'] = self.get_nativeplace_to(item['title'])
        item['linkman'] = tool.get_linkman(detail_text)
        item['function'] = tool.get_function(detail_text)
        item['resource'] = '江苏省建设工程招标网'
        item["shi"] = int(str(item["nativeplace"]).split('.')[0])
        item['sheng'] = 5500
        # print(item)
        item['removal']= title
        process_item(item)
        # print(item['body'])

    def get_nativeplace_to(self, city):
        a = ''
        ls = [['5501', '南京'], ['5501.001', '武区'], ['5501.01', '江宁区'], ['5501.011', '六合区'], ['5501.012', '溧水县'], ['5501.013', '高淳县'], ['5501.002', '白下区'], ['5501.003', '秦淮区'], ['5501.004', '建邺区'], ['5501.005', '鼓楼区'], ['5501.006', '下关区'], ['5501.007', '浦口区'], ['5501.008', '栖霞区'], ['5501.009', '雨花台区'], ['5502', '无锡'], ['5502.001', '崇安区'], ['5502.002', '南长区'], ['5502.003', '北塘区'], ['5502.004', '锡山区'], ['5502.005', '惠山区'], ['5502.006', '滨湖区'], ['5502.007', '江阴'], ['5502.008', '宜兴'], ['5503', '徐州'], ['5503.001', '鼓楼区'], ['5503.01', '新沂'], ['5503.011', '邳州'], ['5503.002', '云龙区'], ['5503.003', '九里区'], ['5503.004', '贾汪区'], ['5503.005', '泉山区'], ['5503.006', '丰县'], ['5503.007', '沛县'], ['5503.008', '铜山县'], ['5503.009', '睢宁县'], ['5504', '常州'], ['5504.001', '天宁区'], ['5504.002', '钟楼区'], ['5504.003', '戚墅堰区'], ['5504.004', '新北区'], ['5504.005', '武进区'], ['5504.006', '溧阳'], ['5504.007', '金坛'], ['5505', '苏州'], ['5505.001', '沧浪区'], ['5505.01', '吴江'], ['5505.011', '太仓'], ['5505.002', '平江区'], ['5505.003', '金阊区'], ['5505.004', '虎丘区'], ['5505.005', '吴中区'], ['5505.006', '相城区'], ['5505.007', '常熟'], ['5505.008', '张家港'], ['5505.009', '昆山'], ['5506', '南通'], ['5506.001', '崇川区'], ['5506.002', '港闸区'], ['5506.003', '海安县'], ['5506.004', '如东县'], ['5506.005', '启东'], ['5506.006', '如皋'], ['5506.007', '通州'], ['5506.008', '海门'], ['5507', '连云港'], ['5507.001', '连云区'], ['5507.002', '新浦区'], ['5507.003', '海州区'], ['5507.004', '赣榆县'], ['5507.005', '东海县'], ['5507.006', '灌云县'], ['5507.007', '灌南县'], ['5508', '淮安'], ['5508.001', '清河区'], ['5508.002', '楚州区'], ['5508.003', '淮阴区'], ['5508.004', '清浦区'], ['5508.005', '涟水县'], ['5508.006', '洪泽县'], ['5508.007', '盱眙县'], ['5508.008', '金湖县'], ['5509', '盐城'], ['5509.001', '亭湖区'], ['5509.002', '盐都区'], ['5509.003', '响水县'], ['5509.004', '滨海县'], ['5509.005', '阜宁县'], ['5509.006', '射阳县'], ['5509.007', '建湖县'], ['5509.008', '东台'], ['5509.009', '大丰'], ['5510', '扬州'], ['5510.001', '广陵区'], ['5510.002', '邗江区'], ['5510.003', '郊区'], ['5510.004', '宝应县'], ['5510.005', '仪征'], ['5510.006', '高邮'], ['5510.007', '江都'], ['5511', '镇江'], ['5511.001', '京口区'], ['5511.002', '润州区'], ['5511.003', '丹徒区'], ['5511.004', '丹阳'], ['5511.005', '扬中'], ['5511.006', '句容'], ['5512', '泰州'], ['5512.001', '海陵区'], ['5512.002', '高港区'], ['5512.003', '兴化'], ['5512.004', '靖江'], ['5512.005', '泰兴'], ['5512.006', '姜堰'], ['5513', '宿迁'], ['5513.001', '宿城区'], ['5513.002', '宿豫区'], ['5513.003', '沭阳县'], ['5513.004', '泗阳县'], ['5513.005', '泗洪县']]
        for i in ls:
            if i[1] in city:
                a = i[0]
                break
        if a == '':
            return 5500
        else:
            return a

if __name__ == '__main__':
    jl = xinyang_ggzy()
    jl.parse()


