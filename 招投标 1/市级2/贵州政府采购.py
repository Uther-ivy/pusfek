# -*- coding: utf-8 -*-
import json
import re
import time, html
from lxml import etree
import tool
from save_database import process_item

# 贵州政府采购
class alashan_ggzy:
    def __init__(self):
        self.url_code = [
            {"categoryCode":"ZcyAnnouncement2","pageSize":15,"pageNo":1},
            {"categoryCode":"ZcyAnnouncement3","pageSize":15,"pageNo":1},
        ]
        self.url = self.url_code.pop(0)
        self.headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Cookie': 'isInitAreaCode=null; _gscu_653689772=78282348u2bs1g18; _gscbrs_653689772=1; UM_distinctid=16f78f570621fa-0e76a94f9f3d2d-e343166-1fa400-16f78f570631fc; _gscs_653689772=t782895054fvlkv12|pv:14; CNZZDATA1260595804=985342442-1578282342-%7C1578291895',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
        }

    def parse(self):
        date = tool.date
        # date = '2020-01-06'
        page = 0
        index_url = 'http://zfcg.guizhou.gov.cn/front/search/category'
        while True:
            page += 1
            self.url['pageNo'] = page
            print('*' * 20, page, '*' * 20)
            text = tool.requests_post_to(index_url, self.url, self.headers)
            # print(111, text)
            # time.sleep(666)
            detail = json.loads(text)['hits']['hits']
            for li in detail:
                title = li['_source']['title']
                url = 'http://zfcg.guizhou.gov.cn' +li['_source']['url']
                date_Today = tool.Time_stamp_to_date(li['_source']['publishDate']/1000)
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
                page = 0

    def parse_detile(self, title, url, date):
        print(url)
        url_text = tool.requests_get(url, self.headers)
        url_html = etree.HTML(url_text)
        deta = url_html.xpath('//*[@name="articleDetail"]/@value')[0]
        detail_html = json.loads(deta)['content']
        detail_text = ''.join(re.findall('>(.*?)<', detail_html, re.S)).replace('\xa0', '').replace('\n', '').replace('\r', '').replace('\t',
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
        item['address'] = tool.get_address(detail_text)
        item['linkman'] = tool.get_linkman(detail_text)
        item['function'] = tool.get_function(detail_text)
        item['resource'] = '贵州政府采购网'
        item['shi'] = int(str(item['nativeplace']).split('.')[0])
        item['sheng'] = 12500
        item['removal']= title
        process_item(item)
        # print(item['nativeplace'], item['title'])

    def get_nativeplace(self, addr):
        city_list = [['12501', '贵阳市'], ['12501.001', '南明区'], ['12501.01', '清镇市'], ['12501.002', '云岩区'], ['12501.003', '花溪区'], ['12501.004', '乌当区'], ['12501.005', '白云区'], ['12501.006', '小河区'], ['12501.007', '开阳县'], ['12501.008', '息烽县'], ['12501.009', '修文县'], ['12502', '六盘水市'], ['12502.001', '钟山区'], ['12502.002', '六枝特区'], ['12502.003', '水城县'], ['12502.004', '盘县'], ['12503', '遵义市'], ['12503.001', '红花岗区'], ['12503.01', '湄潭县'], ['12503.011', '余庆县'], ['12503.012', '习水县'], ['12503.013', '赤水市'], ['12503.014', '仁怀市'], ['12503.002', '汇川区'], ['12503.003', '遵义县'], ['12503.004', '桐梓县'], ['12503.005', '绥阳县'], ['12503.006', '正安县'], ['12503.007', '道真仡佬族苗族自治县'], ['12503.008', '务川仡佬族苗族自治县'], ['12503.009', '凤冈县'], ['12504', '安顺市'], ['12504.001', '西秀区'], ['12504.002', '平坝县'], ['12504.003', '普定县'], ['12504.004', '镇宁布依族苗族自治县'], ['12504.005', '关岭布依族苗族自治县'], ['12504.006', '紫云苗族布依族自治县'], ['12505', '铜仁地区'], ['12505.001', '铜仁市'], ['12505.01', '万山特区'], ['12505.002', '江口县'], ['12505.003', '玉屏侗族自治县'], ['12505.004', '石阡县'], ['12505.005', '思南县'], ['12505.006', '印江土家族苗族自治县'], ['12505.007', '德江县'], ['12505.008', '沿河土家族自治县'], ['12505.009', '松桃苗族自治县'], ['12506', '黔西南布依族苗族自治州'], ['12506.001', '兴义市'], ['12506.002', '兴仁县'], ['12506.003', '普安县'], ['12506.004', '晴隆县'], ['12506.005', '贞丰县'], ['12506.006', '望谟县'], ['12506.007', '册亨县'], ['12506.008', '安龙县'], ['12507', '毕节地区'], ['12507.001', '毕节市'], ['12507.002', '大方县'], ['12507.003', '黔西县'], ['12507.004', '金沙县'], ['12507.005', '织金县'], ['12507.006', '纳雍县'], ['12507.007', '威宁彝族回族苗族自治县'], ['12507.008', '赫章县'], ['12508', '黔东南苗族侗族自治州'], ['12508.001', '凯里市'], ['12508.01', '台江县'], ['12508.011', '黎平县'], ['12508.012', '榕江县'], ['12508.013', '从江县'], ['12508.014', '雷山县'], ['12508.015', '麻江县'], ['12508.002', '黄平县'], ['12508.003', '施秉县'], ['12508.004', '三穗县'], ['12508.005', '镇远县'], ['12508.006', '岑巩县'], ['12508.007', '天柱县'], ['12508.008', '锦屏县'], ['12508.009', '剑河县'], ['12509', '黔南布依族苗族自治州'], ['12509.001', '都匀市'], ['12509.01', '龙里县'], ['12509.011', '惠水县'], ['12509.012', '三都水族自治县'], ['12509.002', '福泉市'], ['12509.003', '荔波县'], ['12509.004', '贵定县'], ['12509.005', '瓮安县'], ['12509.006', '独山县'], ['12509.007', '平塘县'], ['12509.008', '罗甸县'], ['12509.009', '长顺县']]
        for i in city_list:
            if i[1] in addr:
                return float(i[0])
        return 12500

if __name__ == '__main__':
    import traceback, os
    try:
        jl = alashan_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
        if 'pop from empty list'!=str(e):
            print('报错')
            with open('error_name.txt','a+',encoding='utf-8')as f:
                f.write(str(os.path.basename(__file__)))
                f.write('\n')
                f.write(str(traceback.format_exc()))
                f.write('\n')
        else:
            with open('success.txt','a+',encoding='utf-8')as f:
                f.write(str(os.path.basename(__file__)))
                f.write('\n')
                f.write(str('无连接抓取'))
                f.write('\n')

