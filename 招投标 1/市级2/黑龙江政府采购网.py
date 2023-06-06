# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 黑龙江政府采购网
class xinyang_ggzy:
    def __init__(self):
        self.url_list = [
            "https://hljcg.hlj.gov.cn/freecms/rest/v1/notice/selectInfoMoreChannel.do?&siteId=94c965cc-c55d-4f92-8469-d5875c68bd04&channel=c5bff13f-21ca-4dac-b158-cb40accd3035&currPage={}&pageSize=8&noticeType=00101&regionCode=230001&purchaseManner=&title=&openTenderCode=&purchaser=&agency=&purchaseNature=&operationStartTime=&operationEndTime=&selectTimeName=noticeTime"
        ]
        self.url = self.url_list.pop(0)
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
            'Cookie': 'JSESSIONID=Jhs7fR6dYN1sfp2nr6qwFFyJzQGyyxJY4DbWnkT0FvTx1DR6hH3y!-1581166878'
        }

    def parse(self):
        date = tool.date
        # date = '2020-07-10'
        page = 0
        while True:
            page += 1
            text = tool.requests_get(self.url.format(page), self.headers)
            # print(text)
            # time.sleep(6666)
            detail = json.loads(text)['data']
            print('*' * 20, page, '*' * 20)
            for tr in detail:
                title = tr['title']
                date_Today = tr['noticeTime'][:10]
                url = 'https://hljcg.hlj.gov.cn' + tr['pageurl'] + '?noticeType=' + tr['noticeType']
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
            if page == 30:
                self.url = self.url_list.pop(0)
                page = 0

    def parse_detile(self, title, url, date):
        print(url)
        url_html = etree.HTML(tool.requests_get(url, self.headers))
        detail = url_html.xpath('//*[@id="noticeArea"]')[0]
        detail_html = etree.tostring(detail, method='HTML')
        detail_html = html.unescape(detail_html.decode()).replace('\xa0', '').replace('\ufeff', '')
        detail_text = url_html.xpath('string(//*[@id="noticeArea"])') \
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
        # print(item['body'])
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
        item['nativeplace'] = self.get_nativeplace(item['title'])
        item['linkman'] = tool.get_linkman(detail_text)
        item['function'] = tool.get_function(detail_text)
        item['resource'] = '黑龙江政府采购网'
        item["shi"] = int(str(item["nativeplace"]).split('.')[0])
        item['sheng'] = 4500
        item['removal']= title
        process_item(item)
        # print(item['body'])

    def get_nativeplace(self, addr):
        city = ''
        city_list = [['4501', '哈尔滨'], ['4501.001', '道里'], ['4501.01', '方正'], ['4501.011', '宾'], ['4501.012', '巴彦'], ['4501.013', '木兰'], ['4501.014', '通河'], ['4501.015', '延寿'], ['4501.016', '阿城'], ['4501.017', '双城'], ['4501.018', '尚志'], ['4501.019', '五常'], ['4501.02', '利民开发'], ['4501.002', '南岗'], ['4501.003', '道外'], ['4501.004', '香坊'], ['4501.005', '动力'], ['4501.006', '平房'], ['4501.007', '松北'], ['4501.008', '呼兰'], ['4501.009', '依兰'], ['4502', '齐齐哈尔'], ['4502.001', '龙沙'], ['4502.01', '甘南'], ['4502.011', '富裕'], ['4502.012', '克山'], ['4502.013', '克东'], ['4502.014', '拜泉'], ['4502.015', '讷河'], ['4502.002', '建华'], ['4502.003', '铁锋'], ['4502.004', '昂昂溪'], ['4502.005', '富拉尔基'], ['4502.006', '碾子山'], ['4502.007', '梅里斯达斡尔族'], ['4502.008', '龙江 依安'], ['4502.009', '泰来'], ['4503', '鸡西'], ['4503.001', '鸡冠'], ['4503.002', '恒山'], ['4503.003', '滴道'], ['4503.004', '梨树'], ['4503.005', '城子河'], ['4503.006', '麻山'], ['4503.007', '鸡东'], ['4503.008', '虎林'], ['4503.009', '密山'], ['4504', '鹤岗'], ['4504.001', '向阳'], ['4504.002', '工农'], ['4504.003', '南山'], ['4504.004', '兴安'], ['4504.005', '东山'], ['4504.006', '兴山'], ['4504.007', '萝北'], ['4504.008', '绥滨'], ['4505', '双鸭山'], ['4505.001', '尖山'], ['4505.002', '岭东'], ['4505.003', '四方台'], ['4505.004', '宝山'], ['4505.005', '集贤'], ['4505.006', '友谊'], ['4505.007', '宝清'], ['4505.008', '饶河'], ['4506', '大庆'], ['4506.001', '萨尔图'], ['4506.002', '龙凤'], ['4506.003', '让胡路'], ['4506.004', '红岗'], ['4506.005', '大同'], ['4506.006', '肇州'], ['4506.007', '肇源'], ['4506.008', '林甸'], ['4506.009', '杜尔伯特蒙古族自治'], ['4507', '伊春'], ['4507.001', '伊春'], ['4507.01', '乌马河'], ['4507.011', '汤旺河'], ['4507.012', '带岭'], ['4507.013', '乌伊岭'], ['4507.014', '红星'], ['4507.015', '上甘岭'], ['4507.016', '嘉荫'], ['4507.017', '铁力'], ['4507.002', '南岔'], ['4507.003', '友好'], ['4507.004', '西林'], ['4507.005', '翠峦'], ['4507.006', '新青'], ['4507.007', '美溪'], ['4507.008', '金山屯'], ['4507.009', '五营'], ['4508', '佳木斯'], ['4508.001', '永红'], ['4508.01', '同江'], ['4508.011', '富锦'], ['4508.002', '向阳'], ['4508.003', '前进'], ['4508.004', '东风'], ['4508.005', '郊'], ['4508.006', '桦南'], ['4508.007', '桦川'], ['4508.008', '汤原'], ['4508.009', '抚远'], ['4509', '七台河'], ['4509.001', '新兴'], ['4509.002', '桃山'], ['4509.003', '茄子河'], ['4509.004', '勃利'], ['4510', '牡丹江'], ['4510.001', '东安'], ['4510.01', '穆棱'], ['4510.002', '阳明'], ['4510.003', '爱民'], ['4510.004', '西安'], ['4510.005', '东宁'], ['4510.006', '林口'], ['4510.007', '绥芬河'], ['4510.008', '海林'], ['4510.009', '宁安'], ['4511', '黑河'], ['4511.001', '爱辉'], ['4511.002', '嫩江'], ['4511.003', '逊克'], ['4511.004', '孙吴'], ['4511.005', '北安'], ['4511.006', '五大连池'], ['4512', '绥化'], ['4512.001', '北林'], ['4512.01', '海伦'], ['4512.002', '望奎'], ['4512.003', '兰西'], ['4512.004', '青冈'], ['4512.005', '庆安'], ['4512.006', '明水'], ['4512.007', '绥棱'], ['4512.008', '安达'], ['4512.009', '肇东'], ['4513', '大兴安岭地'], ['4513.001', '呼玛'], ['4513.002', '塔河']]

        for i in city_list:
            if i[1] in addr:
                city = float(i[0])
                break
        if city == '':
            city = 4500
        return city

if __name__ == '__main__':
    import traceback, os
    try:
        jl = xinyang_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
        tool.send_error('报错文件：'+str(os.path.basename(__file__))+'报错信息：'+str(e))



