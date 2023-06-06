# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
import tool
from save_database import process_item

# 内蒙古自治区工程项目招投标中心
class neimenggu_ztb:
    def __init__(self):
        self.url_code = [
            # 房建市政
                # 中标信息
            'http://www.nmggcztb.cn/e/index/zbgglb.php?t=w&page={}&cont=fjsz',
                # 招标变更
            'http://www.nmggcztb.cn/e/index/zbgglb.php?t=z&page={}&cont=fjsz',
                # 中标候选人公示
            'http://www.nmggcztb.cn/e/index/zbgglb.php?t=a&page={}&cont=fjsz',
                # 招标公告
            'http://www.nmggcztb.cn/e/index/zbgglb.php?t=n&page={}&cont=fjsz',
            # 水利
                # 中标信息
            'http://www.nmggcztb.cn/e/index/zbgglb.php?t=w&page={}&cont=sl',
                # 招标变更
            'http://www.nmggcztb.cn/e/index/zbgglb.php?t=z&page={}&cont=sl',
                # 中标候选人公示
            'http://www.nmggcztb.cn/e/index/zbgglb.php?t=a&page={}&cont=sl',
                # 招标公告
            'http://www.nmggcztb.cn/e/index/zbgglb.php?t=n&page={}&cont=sl',
            # 铁路
                # 中标信息
            'http://www.nmggcztb.cn/e/index/zbgglb.php?t=w&page={}&cont=tl',
                # 招标变更
            'http://www.nmggcztb.cn/e/index/zbgglb.php?t=z&page={}&cont=tl',
                # 中标候选人公示
            'http://www.nmggcztb.cn/e/index/zbgglb.php?t=a&page={}&cont=tl',
                # 招标公告
            'http://www.nmggcztb.cn/e/index/zbgglb.php?t=n&page={}&cont=tl',
            # 公路
                # 中标信息
            'http://www.nmggcztb.cn/e/index/zbgglb.php?t=w&page={}&cont=gl',
                # 招标变更
            'http://www.nmggcztb.cn/e/index/zbgglb.php?t=z&page={}&cont=gl',
                # 中标候选人公示
            'http://www.nmggcztb.cn/e/index/zbgglb.php?t=a&page={}&cont=gl',
                # 招标公告
            'http://www.nmggcztb.cn/e/index/zbgglb.php?t=n&page={}&cont=gl',
            # 其他
                # 中标信息
            'http://www.nmggcztb.cn/e/index/zbgglb.php?t=w&page={}&cont=qt',
                # 招标变更
            'http://www.nmggcztb.cn/e/index/zbgglb.php?t=z&page={}&cont=qt',
                # 中标候选人公示
            'http://www.nmggcztb.cn/e/index/zbgglb.php?t=a&page={}&cont=qt',
                # 招标公告
            'http://www.nmggcztb.cn/e/index/zbgglb.php?t=n&page={}&cont=qt',
            ]
        self.url = self.url_code.pop(0)
        self.headers = {
            'Cookie': 'UM_distinctid=16f78ae47421d5-017b963a320ae1-e343166-1fa400-16f78ae474324c; CNZZDATA1031917=cnzz_eid%3D1126657079-1578272571-%26ntime%3D1578277982',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
        }

    def parse(self):
        date = tool.date
        # date = '2021-07-26'
        page = 1
        while 1:
            print('*' * 20, page, '*' * 20)
            text = tool.requests_get(self.url.format(page), self.headers)
            print(self.url.format(page))
            detail = json.loads(text)['L']
            for i in detail:
                title = i['2']
                type = re.findall('t=(.*?)&page', self.url)[0]
                if type == 'w':
                    url = 'http://www.nmggcztb.cn/gcxx/detail.php?n=3&id=' + i['0']
                elif type == 'z':
                    url = 'http://www.nmggcztb.cn/gcxx/detail.php?n=4&id=' + i['0']
                elif type == 'a':
                    url = 'http://www.nmggcztb.cn/gcxx/detail.php?n=2&id=' + i['0']
                elif type == 'n':
                    url = 'http://www.nmggcztb.cn/gcxx/detail.php?n=1&id=' + i['0']
                date_Today = i['Time']
                # print(title, url, date_Today)
                # time.sleep(666)
                if tool.Transformation(date) <= tool.Transformation(date_Today):
                    if tool.removal(title, date):
                        self.parse_detile(title, url, date_Today)
                    else:
                        print('【existence】', url)
                        continue
                else:
                    print('日期不符, 正在切换类型...', date_Today)
                    self.url = self.url_code.pop(0)
                    page = 0

                    break
            if page == 20:
                self.url = self.url_code.pop(0)
                break
    def parse_detile(self, title, url, date):
        url_html = etree.HTML(tool.requests_get(url, self.headers))
        detail = url_html.xpath('//*[@id="con"]')[0]
        detail_html = etree.tostring(detail, method='HTML')
        detail_html = html.unescape(detail_html.decode())
        detail_text = url_html.xpath('string(//*[@id="con"])').replace('\xa0','').replace('\n','').replace('\r','').replace('\t','').replace(' ','')
        # print(detail_text.replace('\xa0',''))
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
        item['address'] = tool.get_address(detail_text)
        item['linkman'] = tool.get_linkman(detail_text)
        item['function'] = tool.get_function(detail_text)
        item['resource'] = '内蒙古自治区工程项目招投标中心'
        item['shi'] = int(str(item["nativeplace"]).split('.')[0])
        item['sheng'] = 3000
        item['removal']= title
        process_item(item)

    def get_nativeplace(self, addr):
        city = ''
        city_list = [['3001', '呼和浩特市'], ['3001.001', '新城区'], ['3001.002', '回民区'], ['3001.003', '玉泉区'], ['3001.004', '赛罕区'], ['3001.005', '土默特左旗'], ['3001.006', '托克托县'], ['3001.007', '和林格尔县'], ['3001.008', '清水河县'], ['3001.009', '武川县'], ['3002', '包头市'], ['3002.001', '东河区'], ['3002.002', '昆都仑区'], ['3002.003', '青山区'], ['3002.004', '石拐区'], ['3002.005', '白云矿区'], ['3002.006', '九原区'], ['3002.007', '土默特右旗'], ['3002.008', '固阳县'], ['3002.009', '达尔罕茂明安联合旗'], ['3003', '乌海市'], ['3003.001', '海勃湾区'], ['3003.002', '海南区'], ['3003.003', '乌达区'], ['3004', '赤峰市'], ['3004.001', '红山区'], ['3004.01', '喀喇沁旗'], ['3004.011', '宁城县'], ['3004.012', '敖汉旗'], ['3004.002', '元宝山区'], ['3004.003', '松山区'], ['3004.004', '阿鲁科尔沁旗'], ['3004.005', '巴林左旗'], ['3004.006', '巴林右旗'], ['3004.007', '林西县'], ['3004.008', '克什克腾旗'], ['3004.009', '翁牛特旗'], ['3005', '通辽市'], ['3005.001', '科尔沁区'], ['3005.002', '科尔沁左翼中旗'], ['3005.003', '科尔沁左翼后旗'], ['3005.004', '开鲁县'], ['3005.005', '库伦旗'], ['3005.006', '奈曼旗'], ['3005.007', '扎鲁特旗'], ['3005.008', '霍林郭勒市'], ['3006', '鄂尔多斯市'], ['3006.001', '东胜区'], ['3006.002', '达拉特旗'], ['3006.003', '准格尔旗'], ['3006.004', '鄂托克前旗'], ['3006.005', '鄂托克旗'], ['3006.006', '杭锦旗'], ['3006.007', '乌审旗'], ['3006.008', '伊金霍洛旗'], ['3007', '呼伦贝尔市'], ['3007.001', '海拉尔区'], ['3007.01', '牙克石市'], ['3007.011', '扎兰屯市'], ['3007.012', '额尔古纳市'], ['3007.013', '根河市'], ['3007.002', '阿荣旗'], ['3007.003', '莫力达瓦达斡尔族自治旗'], ['3007.004', '鄂伦春自治旗'], ['3007.005', '鄂温克族自治旗'], ['3007.006', '陈巴尔虎旗'], ['3007.007', '新巴尔虎左旗'], ['3007.008', '新巴尔虎右旗'], ['3007.009', '满洲里市'], ['3008', '巴彦淖尔市'], ['3008.001', '临河区'], ['3008.002', '五原县'], ['3008.003', '磴口县'], ['3008.004', '乌拉特前旗'], ['3008.005', '乌拉特中旗'], ['3008.006', '乌拉特后旗'], ['3008.007', '杭锦后旗'], ['3009', '乌兰察布市'], ['3009.001', '集宁区'], ['3009.01', '四子王旗'], ['3009.011', '丰镇市'], ['3009.002', '卓资县'], ['3009.003', '化德县'], ['3009.004', '商都县'], ['3009.005', '兴和县'], ['3009.006', '凉城县'], ['3009.007', '察哈尔右翼前旗'], ['3009.008', '察哈尔右翼中旗'], ['3009.009', '察哈尔右翼后旗'], ['3010', '兴安盟'], ['3010.001', '乌兰浩特市'], ['3010.002', '阿尔山市'], ['3010.003', '科尔沁右翼前旗'], ['3010.004', '科尔沁右翼中旗'], ['3010.005', '扎赉特旗'], ['3010.006', '突泉县'], ['3011', '锡林郭勒盟'], ['3011.001', '二连浩特市'], ['3011.01', '正镶白旗'], ['3011.011', '正蓝旗'], ['3011.012', '多伦县'], ['3011.002', '锡林浩特市'], ['3011.003', '阿巴嘎旗'], ['3011.004', '苏尼特左旗'], ['3011.005', '苏尼特右旗'], ['3011.006', '东乌珠穆沁旗'], ['3011.007', '西乌珠穆沁旗'], ['3011.008', '太仆寺旗'], ['3011.009', '镶黄旗'], ['3012', '阿拉善盟'], ['3012.001', '阿拉善左旗'], ['3012.002', '阿拉善右旗'], ['3012.003', '额济纳旗']]

        for i in city_list:
            if i[1] in addr:
                city = float(i[0])
                break
        if city == '':
            city = 3000
        return city

if __name__ == '__main__':

    import traceback, os
    try:
        jl = neimenggu_ztb()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
        tool.send_error('报错文件：'+str(os.path.basename(__file__))+'报错信息：'+str(e))


