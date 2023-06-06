# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 广西招标采购网
class baoshan_ggzy:
    def __init__(self):
        self.url_list = [
            'http://www.gxbidding.com/Home/AnnouncementList?typecode=ZBGG',
            'http://www.gxbidding.com/Home/AnnouncementList?typecode=KZJGG',
            'http://www.gxbidding.com/Home/AnnouncementList?typecode=BGGG',
            'http://www.gxbidding.com/Home/AnnouncementList?typecode=JGGS',
            'http://www.gxbidding.com/Home/AnnouncementList?typecode=JGGG'

        ]
        self.url = self.url_list.pop(0)
        self.headers = {
            # 'Cookie': 'homeid=1a444a31-e460-47ff-9931-1c075c0f3cd8',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        }
    def Transformation(self,date):
        """日期转时间戳"""
        timeArray = time.strptime(date, "%b %d %Y")
        timeStamp = int(time.mktime(timeArray))
        return timeStamp

    def parse(self):
        while True:
            date = tool.date
            # date='2021-07-27'
            text = tool.requests_get(self.url,self.headers)
            # print(text)
            html = HTML(text)
            detail = html.xpath('//div[@class="list-group"]//a')

            # print(de)
            for li in range(len(detail)):
                # print(html.xpath('(//table[@id="dataTable"]//tr//@id)[1]'))
                url= 'http://www.gxbidding.com'+html.xpath(f'(//div[@class="list-group"]//a//@href)[{li+1}]')[0]
                # urls_=re.findall("view\('(.*?)','(.*?)'\);",urls)
                # print(urls_)
                title = ''.join(html.xpath(f'((//div[@class="list-group"]//a)[{li+1}]//text())[3]')).replace(' ','').strip()
                #
                date_Today = html.xpath(f'(//div[@class="list-group"]//a//label//text())[{li+1}]')[0]
                # print(li+1,url,title,date_Today)
                if '发布' in date_Today:
                    continue
                # month=re.findall('(\d*)-\d*-\d*',date_Today)
                # day=re.findall('\d*-(\d*)-\d*',date_Today)
                # print(month,day)
                if '测试' in title:
                    continue
                # urls=re.findall("(.*?)\(\'(.*?)\'\)",url)[0]
                # url='http://ggzy.qqhr.gov.cn'+url
                # print(title, url, date_Today)
                # # time.sleep(666)
                if tool.Transformation(date) <= tool.Transformation(date_Today):
                    if tool.removal(title, date):
                        self.parse_detile(title, url, date_Today)
                    else:
                        print('【existence】', url)
                        continue
                else:
                    # print(tool.Transformation(date),self.Transformation(date_Today))
                    print('日期不符, 正在切换类型', date_Today, self.url)
                    self.url = self.url_list.pop(0)
                    page = 0
                    continue
            self.url = self.url_list.pop(0)

    def parse_detile(self, title, url, date):
        print(url)
        t = tool.requests_get(url, self.headers)
        url_html = etree.HTML(t)
        detail = url_html.xpath('//div[@class="panel-body"]')[0]
        # print(detail)
        detail_html = etree.tostring(detail, method='HTML')
        detail_html = html.unescape(detail_html.decode())
        detail_text = url_html.xpath('string(//div[@class="panel-body"])').replace('\xa0', '').replace('\n', ''). \
            replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
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
        item['nativeplace'] = self.get_nativeplace(title)
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
        item['resource'] = '广西招标采购网'
        item["shi"] = int(float(item["nativeplace"]))
        item['sheng'] = 10500
        # print(item)
        item['removal']= title
        process_item(item)

    def get_nativeplace(self, addr):
        city = ''
        city_list = [['10501', '南宁'], ['10501.001', '兴宁'], ['10501.01', '上林'], ['10501.011', '宾阳'], ['10501.012', '横'], ['10501.002', '青秀'], ['10501.003', '江南'], ['10501.004', '西乡塘'], ['10501.005', '良庆'], ['10501.006', '邕宁'], ['10501.007', '武鸣'], ['10501.008', '隆安'], ['10501.009', '马山'], ['10502', '柳州'], ['10502.001', '城中'], ['10502.01', '三江侗族自治'], ['10502.002', '鱼峰'], ['10502.003', '柳南'], ['10502.004', '柳北'], ['10502.005', '柳江'], ['10502.006', '柳城'], ['10502.007', '鹿寨'], ['10502.008', '融安'], ['10502.009', '融水苗族自治'], ['10503', '桂林'], ['10503.001', '秀峰'], ['10503.01', '兴安'], ['10503.011', '永福'], ['10503.012', '灌阳'], ['10503.013', '龙胜各族自治'], ['10503.014', '资源'], ['10503.015', '平乐'], ['10503.016', '荔蒲'], ['10503.017', '恭城瑶族自治'], ['10503.002', '叠彩'], ['10503.003', '象山'], ['10503.004', '七星'], ['10503.005', '雁山'], ['10503.006', '阳朔'], ['10503.007', '临桂'], ['10503.008', '灵川'], ['10503.009', '全州'], ['10504', '梧州'], ['10504.001', '万秀'], ['10504.002', '蝶山'], ['10504.003', '长洲'], ['10504.004', '苍梧'], ['10504.005', '藤'], ['10504.006', '蒙山'], ['10504.007', '岑溪'], ['10505', '北海'], ['10505.001', '海城'], ['10505.002', '银海'], ['10505.003', '铁山港'], ['10505.004', '合浦'], ['10506', '防城港'], ['10506.001', '港口'], ['10506.002', '防城'], ['10506.003', '上思'], ['10506.004', '东兴'], ['10507', '钦州'], ['10507.001', '钦南'], ['10507.002', '钦北'], ['10507.003', '灵山'], ['10507.004', '浦北'], ['10508', '贵港'], ['10508.001', '港北'], ['10508.002', '港南'], ['10508.003', '覃塘'], ['10508.004', '平南'], ['10508.005', '桂平'], ['10509', '玉林'], ['10509.001', '玉州'], ['10509.002', '容'], ['10509.003', '陆川'], ['10509.004', '博白'], ['10509.005', '兴业'], ['10509.006', '北流'], ['10510', '百色'], ['10510.001', '右江'], ['10510.01', '田林'], ['10510.011', '西林'], ['10510.012', '隆林各族自治'], ['10510.002', '田阳'], ['10510.003', '田东'], ['10510.004', '平果'], ['10510.005', '德保'], ['10510.006', '靖西'], ['10510.007', '那坡'], ['10510.008', '凌云'], ['10510.009', '乐业'], ['10511', '贺州'], ['10511.001', '八步'], ['10511.002', '昭平'], ['10511.003', '钟山'], ['10511.004', '富川瑶族自治'], ['10512', '河池'], ['10512.001', '金城江'], ['10512.01', '大化瑶族自治'], ['10512.011', '宜州'], ['10512.002', '南丹'], ['10512.003', '天峨'], ['10512.004', '凤山'], ['10512.005', '东兰'], ['10512.006', '罗城仫佬族自治'], ['10512.007', '环江毛南族自治'], ['10512.008', '巴马瑶族自治'], ['10512.009', '都安瑶族自治'], ['10513', '来宾'], ['10513.001', '兴宾'], ['10513.002', '忻城'], ['10513.003', '象州'], ['10513.004', '武宣'], ['10513.005', '金秀瑶族自治'], ['10513.006', '合山'], ['10514', '崇左'], ['10514.001', '江洲'], ['10514.002', '扶绥'], ['10514.003', '宁明'], ['10514.004', '龙州'], ['10514.005', '大新'], ['10514.006', '天等']]

        for i in city_list:
            if i[1] in addr:
                city = float(i[0])
                break
        if city == '':
            city = 10500
        return city

if __name__ == '__main__':

    import traceback, os
    try:
        jl = baoshan_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
