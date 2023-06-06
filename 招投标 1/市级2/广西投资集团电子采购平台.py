# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 广西投资集团电子采购平台
class wenshan_ggzy:
    def __init__(self):
        self.domain_name = 'http://www.gigeps.com'
        self.url_list = [
            'http://www.gigeps.com/cms/channel/xmgg1hw/index.htm?pageNo={}',
            'http://www.gigeps.com/cms/channel/xmgg1gc/index.htm?pageNo={}',

            'http://www.gigeps.com/cms/channel/xmgg4hw/index.htm?pageNo={}',
            'http://www.gigeps.com/cms/channel/xmgg4gc/index.htm?pageNo={}',

            'http://www.gigeps.com/cms/channel/xmgg3hw/index.htm?pageNo={}',
            'http://www.gigeps.com/cms/channel/xmgg3gc/index.htm?pageNo={}'
        ]
        self.url = self.url_list.pop(0)
        self.headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Cookie': 'JSESSIONID=662863FD2199FBD1672A04A290868047; _CSRFCOOKIE=73F3D7A1BCDCA9001D7B1483A214C4E98DE2528B; EPTOKEN=73F3D7A1BCDCA9001D7B1483A214C4E98DE2528B; oauthClientId=demoClient; oauthPath=http://172.16.5.21:8080/EpointWebBuilder; oauthLoginUrl=http://172.16.5.21:8080/EpointWebBuilder/rest/oauth2/authorize?client_id=demoClient&state=a&response_type=code&scope=user&redirect_uri=; oauthLogoutUrl=http://172.16.5.21:8080/EpointWebBuilder/rest/oauth2/logout?redirect_uri=; noOauthRefreshToken=986d4fe7e5dd29b64c9e7b7a6d66e089; noOauthAccessToken=77c09e0bf98b6220b544961097eed84a; sub_domain_cokie=TiG5CMD9KQ41mmsARPTuAg%3D%3D; region_name=%E4%B9%8C%E9%B2%81%E6%9C%A8%E9%BD%90%E5%B8%82',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',

        }


    def parse(self):
        date = tool.date
        # date = '2021-07-27'
        page = 0
        while True:
            page += 1
            text = tool.requests_get(self.url.format(page), self.headers)
            html = HTML(text)
            print('*' * 20, page, '*' * 20)
            # print(11, text)
            # time.sleep(6666)
            detail = html.xpath('//*[@id="list1"]/li')
            for li in detail:
                title = li.xpath('./a/@title')[0]
                url = li.xpath('./a/@href')[0]
                date_Today = li.xpath('./a/span[3]/text()')[0].replace('\xa0', '').replace('\n', ''). \
                    replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '') \
                    .replace('[', '').replace(']', '').replace('/', '-')
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
        try:
            detail = url_html.xpath('//*[@id="main"]/div[2]/div/div[1]/div/div/div[2]')[0]
            detail_html = etree.tostring(detail, method='HTML')
            detail_html = html.unescape(detail_html.decode()).replace("display: none", '').replace("\u2022", '').replace('\xa0', '')
            detail_text = url_html.xpath('string(//*[@id="main"]/div[2]/div/div[1]/div/div/div[2])').replace('\xa0', '').replace('\n',
                                                                                                                 ''). \
                replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
            if len(detail_html) < 200:
                int('a')
        except:
            detail = url_html.xpath('//*[@class="ninfo-con"]')[0]
            detail_html = etree.tostring(detail, method='HTML')
            detail_html = html.unescape(detail_html.decode()).replace("display: none", '').replace("\u2022",
                                                                                                   '').replace('\xa0',
                                                                                                               '')
            detail_text = url_html.xpath('string(//*[@class="ninfo-con"])').replace('\xa0',
                                                                                                             '').replace(
                '\n',
                ''). \
                replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
            if len(detail_html) < 200:
                return
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
        item['resource'] = '广西投资集团电子采购平台'
        item['shi'] = int(item['nativeplace'])
        item['sheng'] = 10500
        item['removal']= title
        process_item(item)

    def get_nativeplace(self, addr):
        city = ''
        city_list = [['10501', '南宁'], ['10501.001', '兴宁区'], ['10501.01', '上林县'], ['10501.011', '宾阳县'], ['10501.012', '横县'], ['10501.002', '青秀区'], ['10501.003', '江南区'], ['10501.004', '西乡塘区'], ['10501.005', '良庆区'], ['10501.006', '邕宁区'], ['10501.007', '武鸣县'], ['10501.008', '隆安县'], ['10501.009', '马山县'], ['10502', '柳州'], ['10502.001', '城中区'], ['10502.01', '三江侗族自治县'], ['10502.002', '鱼峰区'], ['10502.003', '柳南区'], ['10502.004', '柳北区'], ['10502.005', '柳江县'], ['10502.006', '柳城县'], ['10502.007', '鹿寨县'], ['10502.008', '融安县'], ['10502.009', '融水苗族自治县'], ['10503', '桂林'], ['10503.001', '秀峰区'], ['10503.01', '兴安县'], ['10503.011', '永福县'], ['10503.012', '灌阳县'], ['10503.013', '龙胜各族自治县'], ['10503.014', '资源县'], ['10503.015', '平乐县'], ['10503.016', '荔蒲县'], ['10503.017', '恭城瑶族自治县'], ['10503.002', '叠彩区'], ['10503.003', '象山区'], ['10503.004', '七星区'], ['10503.005', '雁山区'], ['10503.006', '阳朔县'], ['10503.007', '临桂县'], ['10503.008', '灵川县'], ['10503.009', '全州县'], ['10504', '梧州'], ['10504.001', '万秀区'], ['10504.002', '蝶山区'], ['10504.003', '长洲区'], ['10504.004', '苍梧县'], ['10504.005', '藤县'], ['10504.006', '蒙山县'], ['10504.007', '岑溪'], ['10505', '北海'], ['10505.001', '海城区'], ['10505.002', '银海区'], ['10505.003', '铁山港区'], ['10505.004', '合浦县'], ['10506', '防城港'], ['10506.001', '港口区'], ['10506.002', '防城区'], ['10506.003', '上思县'], ['10506.004', '东兴'], ['10507', '钦州'], ['10507.001', '钦南区'], ['10507.002', '钦北区'], ['10507.003', '灵山县'], ['10507.004', '浦北县'], ['10508', '贵港'], ['10508.001', '港北区'], ['10508.002', '港南区'], ['10508.003', '覃塘区'], ['10508.004', '平南县'], ['10508.005', '桂平'], ['10509', '玉林'], ['10509.001', '玉州区'], ['10509.002', '容县'], ['10509.003', '陆川县'], ['10509.004', '博白县'], ['10509.005', '兴业县'], ['10509.006', '北流'], ['10510', '百色'], ['10510.001', '右江区'], ['10510.01', '田林县'], ['10510.011', '西林县'], ['10510.012', '隆林各族自治县'], ['10510.002', '田阳县'], ['10510.003', '田东县'], ['10510.004', '平果县'], ['10510.005', '德保县'], ['10510.006', '靖西县'], ['10510.007', '那坡县'], ['10510.008', '凌云县'], ['10510.009', '乐业县'], ['10511', '贺州'], ['10511.001', '八步区'], ['10511.002', '昭平县'], ['10511.003', '钟山县'], ['10511.004', '富川瑶族自治县'], ['10512', '河池'], ['10512.001', '金城江区'], ['10512.01', '大化瑶族自治县'], ['10512.011', '宜州'], ['10512.002', '南丹县'], ['10512.003', '天峨县'], ['10512.004', '凤山县'], ['10512.005', '东兰县'], ['10512.006', '罗城仫佬族自治县'], ['10512.007', '环江毛南族自治县'], ['10512.008', '巴马瑶族自治县'], ['10512.009', '都安瑶族自治县'], ['10513', '来宾'], ['10513.001', '兴宾区'], ['10513.002', '忻城县'], ['10513.003', '象州县'], ['10513.004', '武宣县'], ['10513.005', '金秀瑶族自治县'], ['10513.006', '合山'], ['10514', '崇左'], ['10514.001', '江洲区'], ['10514.002', '扶绥县'], ['10514.003', '宁明县'], ['10514.004', '龙州县'], ['10514.005', '大新县'], ['10514.006', '天等县'], ['10514.007', '凭祥']]

        for i in city_list:
            if i[1] in addr:
                city = float(i[0])
                break
        if city == '':
            city = 10500
        return city

if __name__ == '__main__':
    import traceback,os
    try:
        jl = wenshan_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
        tool.send_error('报错文件：'+str(os.path.basename(__file__))+'报错信息：'+str(e))


