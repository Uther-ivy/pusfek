# -*- coding: utf-8 -*-
import time, html, re
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 山西公共资源
class xinyang_ggzy:
    def __init__(self):
        self.url_list = ['http://prec.sxzwfw.gov.cn/queryContent_{}-jyxx.jspx',]
        self.url = self.url_list.pop(0)
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
            # 'Cookie': 'JSESSIONID=Jhs7fR6dYN1sfp2nr6qwFFyJzQGyyxJY4DbWnkT0FvTx1DR6hH3y!-1581166878'
            # 'Cookie': 'JSESSIONID=6cf5cad7-9e11-4d3d-9efd-70e2f5bc0d11'
        }
        self.data = {'title':"", 'channelId': 12, 'origin': "", 'inDates': 4000, 'beginTime': "", 'endTime': "",'ext':""}

    def parse(self):
        date = tool.date
        # date = '2020-07-10'
        page = 0
        while True:
            page += 1
            if page==1:
                text = tool.requests_post(url=self.url.replace('_{}',''), data=self.data, headers=self.headers)

            else:
                text = tool.requests_post(url=self.url.format(page),data=self.data,headers= self.headers)

            # time.sleep(666)
            detail = HTML(text).xpath('/html/body/div[3]/div/div[2]/div/div[4]/div[1]/a')
            print('*' * 20, page, '*' * 20)
            for li in detail:
                url = li.xpath('./@href')[0]
                print(url)
                title = li.xpath('./p[1]/text()')[0].replace('\n','').replace('\r', '').replace('\t', '').replace(' ', '')
                date_Today = li.xpath('./p[2]/span[2]/text()')[0].replace('[',
                                                                                                            '').replace(
                    ']', '').replace('/', '-')
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
                break


    def parse_detile(self, title, url, date):
        print(url)
        t = tool.requests_get(url, self.headers)
        # print(t)
        # time.sleep(6666)
        url_html = etree.HTML(t)
        if 'iframe' in t:
            pdf=url_html.xpath("//iframe/@src")[0].replace('\\','/')
            print(pdf)
            detail_html = f'<embed src="{pdf.replace("http://prec.sxzwfw.gov.cn/", "")}" />'
            detail_text = ''.join(re.findall('>(.*?)<', detail_html, re.S)) \
                .replace('\xa0', '').replace('\n', '').replace('\r', '').replace('\t', '') \
                .replace(' ', '').replace('\xa5', '').replace('\ufeff', '')
        else:
            detail = url_html.xpath('//table[@class="gycq-table"]')[0]
            detail_html = etree.tostring(detail, method='HTML')
            detail_html = html.unescape(detail_html.decode()).replace('\xa0', '').replace('\ufeff', '')
            detail_text = url_html.xpath('string(/html/body/div[2]/div/div/div/div[2]/table)') \
                .replace('\xa0', '').replace('\n', '').replace('\r', '').replace('\t', '') \
                .replace(' ', '').replace('\xa5', '').replace('\ufeff', '')
        item = {}
        item['title'] = title.replace('\u2022', '')
        item['url'] = url
        item['date'] = date
        item['typeid'] = tool.get_typeid(item['title'])
        item['senddate'] = int(time.time())
        item['mid'] = 867
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
        item['nativeplace'] = self.get_nativeplace(item['title'])
        item['linkman'] = tool.get_linkman(detail_text)
        item['function'] = tool.get_function(detail_text)
        item['resource'] = '山西公共资源'
        item["shi"] = int(str(item["nativeplace"]).split('.')[0])
        item['sheng'] = 2500
        item['removal']= title
        # process_item(item)
        print(item)

    def get_nativeplace(self, addr):
        city = ''
        city_list = [['2501', '太原'], ['2501.001', '小店'], ['2501.01', '古交'], ['2501.002', '迎泽'], ['2501.003', '杏花岭'], ['2501.004', '尖草坪'], ['2501.005', '万柏林'], ['2501.006', '晋源'], ['2501.007', '清徐'], ['2501.008', '阳曲'], ['2501.009', '娄烦'], ['2502', '大同'], ['2502.001', '南郊'], ['2502.01', '城'], ['2502.011', '矿'], ['2502.012', '南郊'], ['2502.002', '新荣'], ['2502.003', '阳高'], ['2502.004', '天镇'], ['2502.005', '广灵'], ['2502.006', '灵丘'], ['2502.007', '浑源'], ['2502.008', '左云'], ['2502.009', '大同'], ['2503', '阳泉'], ['2503.001', '城'], ['2503.002', '矿'], ['2503.003', '郊'], ['2503.004', '平定'], ['2503.005', '盂'], ['2504', '长治'], ['2504.001', '城'], ['2504.01', '武乡'], ['2504.011', '沁'], ['2504.012', '沁源'], ['2504.013', '潞城'], ['2504.002', '郊'], ['2504.003', '长治'], ['2504.004', '襄垣'], ['2504.005', '屯留'], ['2504.006', '平顺'], ['2504.007', '黎城'], ['2504.008', '壶关'], ['2504.009', '长子'], ['2505', '晋城'], ['2505.001', '城'], ['2505.002', '沁水'], ['2505.003', '阳城'], ['2505.004', '陵川'], ['2505.005', '泽州'], ['2505.006', '高平'], ['2506', '朔州'], ['2506.001', '朔城'], ['2506.002', '平鲁'], ['2506.003', '山阴'], ['2506.004', '应'], ['2506.005', '右玉'], ['2506.006', '怀仁'], ['2507', '晋中'], ['2507.001', '榆次'], ['2507.01', '灵石'], ['2507.011', '介休'], ['2507.002', '榆社'], ['2507.003', '左权'], ['2507.004', '和顺'], ['2507.005', '昔阳'], ['2507.006', '寿阳'], ['2507.007', '太谷'], ['2507.008', '祁'], ['2507.009', '平遥'], ['2508', '运城'], ['2508.001', '盐湖'], ['2508.01', '平陆'], ['2508.011', '芮城'], ['2508.012', '永济'], ['2508.013', '河津'], ['2508.002', '临猗'], ['2508.003', '万荣'], ['2508.004', '闻喜'], ['2508.005', '稷山'], ['2508.006', '新绛'], ['2508.007', '绛'], ['2508.008', '垣曲'], ['2508.009', '夏'], ['2509', '忻州'], ['2509.001', '忻府'], ['2509.01', '岢岚'], ['2509.011', '河曲'], ['2509.012', '保德'], ['2509.013', '偏关'], ['2509.014', '原平'], ['2509.002', '定襄'], ['2509.003', '五台'], ['2509.004', '代'], ['2509.005', '繁峙'], ['2509.006', '宁武'], ['2509.007', '静乐'], ['2509.008', '神池'], ['2509.009', '五寨'], ['2510', '临汾'], ['2510.001', '尧都'], ['2510.01', '乡宁'], ['2510.011', '大宁'], ['2510.012', '隰'], ['2510.013', '永和'], ['2510.014', '蒲'], ['2510.015', '汾西'], ['2510.016', '侯马'], ['2510.017', '霍州'], ['2510.002', '曲沃'], ['2510.003', '翼城'], ['2510.004', '襄汾'], ['2510.005', '洪洞'], ['2510.006', '古'], ['2510.007', '安泽'], ['2510.008', '浮山'], ['2510.009', '吉'], ['2511', '吕梁'], ['2511.001', '离石'], ['2511.01', '中阳'], ['2511.011', '交口'], ['2511.012', '孝义'], ['2511.013', '汾阳'], ['2511.002', '文水'], ['2511.003', '交城'], ['2511.004', '兴'], ['2511.005', '临'], ['2511.006', '柳林'], ['2511.007', '石楼'], ['2511.008', '岚']]

        for i in city_list:
            if i[1] in addr:
                city = float(i[0])
                break
        if city == '':
            city = 2500
        return city

if __name__ == '__main__':
    import traceback, os
    try:
        jl = xinyang_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
        tool.send_error('报错文件：'+str(os.path.basename(__file__))+'报错信息：'+str(e))



