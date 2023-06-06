# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 四川建设网
class xinyang_ggzy:
    def __init__(self):
        self.url_list = [
           'http://www.sccin.com.cn/InvestmentInfo/ZhaoBiao/InvitNotice.aspx?typeid=0&&type=ZBGG',
            'http://www.sccin.com.cn/InvestmentInfo/ZhaoBiao/houxuanren.aspx?type=ZBHXR'
        ]
        self.url = self.url_list.pop(0)
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        }

    def parse(self):
        date = tool.date
        # date = '2020-07-01'
        page = 0
        data = {
            '__EVENTTARGET': 'ctl00$ContentPlaceHolder1$myPager',
            '__EVENTARGUMENT': '2',
            '__LASTFOCUS': '',
            '__VIEWSTATE':'',
            '__EVENTVALIDATION':'',
            'ctl00$Control_Ads1$hdfClickedAdKeys': '',
            'ctl00$Search1$txtQuery': '',
            'ctl00$ContentPlaceHolder1$tb_Name': '',
            'ctl00$ContentPlaceHolder1$ucCodeModule_IPBtype$ddlCodeList': '0',
            'ctl00$ContentPlaceHolder1$ucAreaCode1$ddlProvince': '0',
            'ctl00$ContentPlaceHolder1$myPager_input': '1',
            'ctl00$Control_Ads2$hdfClickedAdKeys': ''
        }
        while True:
            page += 1
            if page == 1:
                text = tool.requests_get(self.url, self.headers)
            else:
                text = tool.requests_post(self.url, data, self.headers)
            # print(text)
            # time.sleep(666)
            html = HTML(text)
            data['__EVENTARGUMENT'] = page
            data['ctl00$ContentPlaceHolder1$myPager_input'] = page-1
            data['__VIEWSTATE'] = html.xpath('//*[@id="__VIEWSTATE"]/@value')[0]
            data['__EVENTVALIDATION'] = html.xpath('//*[@id="__EVENTVALIDATION"]/@value')[0]
            print('*' * 20, page, '*' * 20)
            if 'ZBGG' in self.url:
                detail = html.xpath('//*[@id="ContentPlaceHolder1_GVList"]/tr')
            else:
                detail = html.xpath('//*[@class="lie"]/tbody/tr[2]/td[1]/table/tr')
            for li in detail:
                if 'ZBGG' in self.url:
                   try:
                       title = li.xpath('./td[1]/a/span/@title')[0].replace('\xa0', '').replace(' ', '')
                       url = 'http://www.sccin.com.cn/InvestmentInfo/ZhaoBiao/' + \
                             li.xpath('./td[1]/a/@href')[0]
                       date_Today = li.xpath('./td[3]/text()')[0].replace('/', '-')
                   except:
                       continue
                else:
                    title = li.xpath('./td[1]/a/@title')[0].replace('\xa0', '').replace(' ', '')
                    url = 'http://www.sccin.com.cn/InvestmentInfo/ZhaoBiao/' + \
                          li.xpath('./td[1]/a/@href')[0]
                    date_Today = li.xpath('./td[3]/text()')[0].replace('\r', '').replace(' ', '').replace('\n', '').replace('\t', '').replace('/', '-')
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
        t = tool.requests_get(url, self.headers)
        t = t.replace("""<DIV class='.wmain12"'>""", "<DIV class='.wmain12'>")
        url_html = etree.HTML(t)
        try:
            detail = url_html.xpath('//*[@class="sanji_con"]')[0]
            detail_html = etree.tostring(detail, method='HTML')
            detail_html = html.unescape(detail_html.decode()).replace('\xa0', '').replace('\ufeff', '')
            detail_text = url_html.xpath('string(//*[@class="sanji_con"])') \
                .replace('\xa0', '').replace('\n', '').replace('\r', '').replace('\t', '') \
                .replace(' ', '').replace('\xa5', '').replace('\ufeff', '')
        except:
            try:
                detail = url_html.xpath('//*[@class=".wmain12"]')[0]
                detail_html = etree.tostring(detail, method='HTML')
                detail_html = html.unescape(detail_html.decode()).replace('\xa0', '').replace('\ufeff', '')
                detail_text = url_html.xpath('string(//*[@class=".wmain12"])') \
                    .replace('\xa0', '').replace('\n', '').replace('\r', '').replace('\t', '') \
                    .replace(' ', '').replace('\xa5', '').replace('\ufeff', '')
            except:
                try:
                    detail = url_html.xpath('//*[@class="wmain"]')[0]
                    detail_html = etree.tostring(detail, method='HTML')
                    detail_html = html.unescape(detail_html.decode()).replace('\xa0', '').replace('\ufeff', '')
                    detail_text = url_html.xpath('string(//*[@class="wmain"])') \
                        .replace('\xa0', '').replace('\n', '').replace('\r', '').replace('\t', '') \
                        .replace(' ', '').replace('\xa5', '').replace('\ufeff', '')
                except:
                    detail = url_html.xpath('//div[@class="kuang"]')[0]
                    detail_html = etree.tostring(detail, method='HTML')
                    detail_html = html.unescape(detail_html.decode()).replace('\xa0', '').replace('\ufeff', '')
                    detail_text = url_html.xpath('string(//div[@class="kuang"])') \
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
        item['winner'] = tool.get_winner(detail_text)
        item['address'] = tool.get_address(detail_text)
        item['nativeplace'] = self.get_nativeplace_to(item['title'])
        item['linkman'] = tool.get_linkman(detail_text)
        item['function'] = tool.get_function(detail_text)
        item['resource'] = '四川建设网'
        item["shi"] = int(str(item["nativeplace"]).split('.')[0])
        item['sheng'] = 12000
        item['removal']= title
        process_item(item)
        # print(item['body'])

    def get_nativeplace_to(self, city):
        a = ''
        ls = [['12001', '成都'], ['12001.001', '锦江区'], ['12001.01', '金堂县'], ['12001.011', '双流县'], ['12001.012', '郫县'], ['12001.013', '大邑县'], ['12001.014', '蒲江县'], ['12001.015', '新津县'], ['12001.016', '都江堰'], ['12001.017', '彭州'], ['12001.018', '邛崃'], ['12001.019', '崇州'], ['12001.002', '青羊区'], ['12001.003', '金牛区'], ['12001.004', '武侯区'], ['12001.005', '成华区'], ['12001.006', '龙泉驿区'], ['12001.007', '青白江区'], ['12001.008', '新都区'], ['12001.009', '温江区'], ['12002', '自贡'], ['12002.001', '自流井区'], ['12002.002', '贡井区'], ['12002.003', '大安区'], ['12002.004', '沿滩区'], ['12002.005', '荣县'], ['12002.006', '富顺县'], ['12003', '攀枝花'], ['12003.001', '东区'], ['12003.002', '西区'], ['12003.003', '仁和区'], ['12003.004', '米易县'], ['12003.005', '盐边县'], ['12004', '泸州'], ['12004.001', '江阳区'], ['12004.002', '纳溪区'], ['12004.003', '龙马潭区'], ['12004.004', '泸县'], ['12004.005', '合江县'], ['12004.006', '叙永县'], ['12004.007', '古蔺县'], ['12005', '德阳'], ['12005.001', '旌阳区'], ['12005.002', '中江县'], ['12005.003', '罗江县'], ['12005.004', '广汉'], ['12005.005', '什邡'], ['12005.006', '绵竹'], ['12006', '绵阳'], ['12006.001', '涪城区'], ['12006.002', '游仙区'], ['12006.003', '三台县'], ['12006.004', '盐亭县'], ['12006.005', '安县'], ['12006.006', '梓潼县'], ['12006.007', '北川羌族自治县'], ['12006.008', '平武县'], ['12006.009', '江油'], ['12007', '广元'], ['12007.001', '中区'], ['12007.002', '元坝区'], ['12007.003', '朝天区'], ['12007.004', '旺苍县'], ['12007.005', '青川县'], ['12007.006', '剑阁县'], ['12007.007', '苍溪县'], ['12008', '遂宁'], ['12008.001', '船山区'], ['12008.002', '安居区'], ['12008.003', '蓬溪县'], ['12008.004', '射洪县'], ['12008.005', '大英县'], ['12009', '内江'], ['12009.001', '中区'], ['12009.002', '东兴区'], ['12009.003', '威远县'], ['12009.004', '资中县'], ['12009.005', '隆昌县'], ['12010', '乐山'], ['12010.001', '中区'], ['12010.01', '马边彝族自治县'], ['12010.011', '峨眉山'], ['12010.002', '沙湾区'], ['12010.003', '五通桥区'], ['12010.004', '金口河区'], ['12010.005', '犍为县'], ['12010.006', '井研县'], ['12010.007', '夹江县'], ['12010.008', '沐川县'], ['12010.009', '峨边彝族自治县'], ['12011', '南充'], ['12011.001', '顺庆区'], ['12011.002', '高坪区'], ['12011.003', '嘉陵区'], ['12011.004', '南部县'], ['12011.005', '营山县'], ['12011.006', '蓬安县'], ['12011.007', '仪陇县'], ['12011.008', '西充县'], ['12011.009', '阆中'], ['12012', '眉山'], ['12012.001', '东坡区'], ['12012.002', '仁寿县'], ['12012.003', '彭山县'], ['12012.004', '洪雅县'], ['12012.005', '丹棱县'], ['12012.006', '青神县'], ['12013', '宜宾'], ['12013.001', '翠屏区'], ['12013.01', '屏山县'], ['12013.002', '宜宾县'], ['12013.003', '南溪县'], ['12013.004', '江安县'], ['12013.005', '长宁县'], ['12013.006', '高县'], ['12013.007', '珙县'], ['12013.008', '筠连县'], ['12013.009', '兴文县'], ['12014', '广安'], ['12014.001', '广安区'], ['12014.002', '岳池县'], ['12014.003', '武胜县'], ['12014.004', '邻水县'], ['12014.005', '华莹'], ['12015', '达州'], ['12015.001', '通川区'], ['12015.002', '达县'], ['12015.003', '宣汉县'], ['12015.004', '开江县'], ['12015.005', '大竹县'], ['12015.006', '渠县'], ['12015.007', '万源'], ['12016', '雅安'], ['12016.001', '雨城区'], ['12016.002', '名山县'], ['12016.003', '荥经县'], ['12016.004', '汉源县'], ['12016.005', '石棉县'], ['12016.006', '天全县'], ['12016.007', '芦山县'], ['12016.008', '宝兴县'], ['12017', '巴中'], ['12017.001', '巴州区'], ['12017.002', '通江县'], ['12017.003', '南江县'], ['12017.004', '平昌县'], ['12018', '资阳'], ['12018.001', '雁江区'], ['12018.002', '安岳县'], ['12018.003', '乐至县'], ['12018.004', '简阳'], ['12019', '阿坝藏族羌族自治州'], ['12019.001', '汶川县'], ['12019.01', '壤塘县'], ['12019.011', '阿坝县'], ['12019.012', '若尔盖县'], ['12019.013', '红原县'], ['12019.002', '理县'], ['12019.003', '茂县'], ['12019.004', '松潘县'], ['12019.005', '九寨沟县'], ['12019.006', '金川县'], ['12019.007', '小金县'], ['12019.008', '黑水县'], ['12019.009', '马尔康县'], ['12020', '甘孜藏族自治州'], ['12020.001', '康定县'], ['12020.01', '德格县'], ['12020.011', '白玉县'], ['12020.012', '石渠县'], ['12020.013', '色达县'], ['12020.014', '理塘县'], ['12020.015', '巴塘县'], ['12020.016', '乡城县'], ['12020.017', '稻城县'], ['12020.018', '得荣县'], ['12020.002', '泸定县'], ['12020.003', '丹巴县'], ['12020.004', '九龙县'], ['12020.005', '雅江县'], ['12020.006', '道孚县'], ['12020.007', '炉霍县'], ['12020.008', '甘孜县'], ['12020.009', '新龙县'], ['12021', '凉山彝族自治州'], ['12021.001', '西昌'], ['12021.01', '金阳县'], ['12021.011', '昭觉县'], ['12021.012', '喜德县'], ['12021.013', '冕宁县'], ['12021.014', '越西县'], ['12021.015', '甘洛县'], ['12021.016', '美姑县'], ['12021.017', '雷波县'], ['12021.002', '木里藏族自治县'], ['12021.003', '盐源县'], ['12021.004', '德昌县'], ['12021.005', '会理县'], ['12021.006', '会东县'], ['12021.007', '宁南县'], ['12021.008', '普格县'], ['12021.009', '布拖县']]
        for i in ls:
            if i[1] in city:
                a = i[0]
                break
        if a == '':
            return 12000
        else:
            return a

if __name__ == '__main__':
    jl = xinyang_ggzy()
    jl.parse()
    try:
        jl = anshun_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
        tool.send_error('报错文件：'+str(os.path.basename(__file__))+'报错信息：'+str(e))


