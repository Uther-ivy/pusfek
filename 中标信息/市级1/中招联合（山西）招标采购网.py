# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 中招联合（山西）招标采购网
class shanxi_zbcg:
    def __init__(self):
        self.url_code = [
            # 招标公告
            # 'http://shanxi.365trade.com.cn/zbgg/index_{}.jhtml',
            # 变更
            # 'http://shanxi.365trade.com.cn/bggg/index_{}.jhtml',
            # 结果公告
            'http://shanxi.365trade.com.cn/jggs/index_{}.jhtml',
        ]
        self.url = self.url_code.pop(0)
        self.headers = {
            'Cookie': 'acw_tc=65c86a0915785495893707757e12b7478ad9e237eae61945b35ac2e233d62f; clientlanguage=zh_CN; Hm_lvt_3dc6b1861c3a72dd7fdba3c2c713fe0e=1578549592; Hm_lpvt_3dc6b1861c3a72dd7fdba3c2c713fe0e=1578549592',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
        }

    def parse(self):
        date = tool.date
        # date = '2020-01-06'
        page =184

        while True:
            page += 1
            print('*' * 20, page, '*' * 20)
            text = tool.requests_get(self.url.format(page), self.headers)
            # print(111, text)
            # time.sleep(666)
            html = HTML(text)
            detail = html.xpath('/html/body/div[2]/div/ul/li')
            for li in detail:
                try:
                    title = li.xpath('./a[1]/p/span/@title')[0]
                    url = 'http://shanxi.365trade.com.cn' + li.xpath('./a[2]/@href')[0]
                    date_Today = li.xpath('./a[1]/i/text()')[0][5:]
                    # print(title, url, date_Today)
                    # time.sleep(666)
                    if tool.Transformation(date) <= tool.Transformation(date_Today):
                        # if tool.removal(title, date):
                            self.parse_detile(title, url, date_Today)
                        # else:
                        #     print('【existence】', url)
                        #     continue
                    else:
                        print('日期不符, 正在切换类型...', date_Today)
                        return
                except Exception as e:
                    traceback.print_exc()
    def parse_detile(self, title, url, date):
        print(url)
        url_html = etree.HTML(tool.requests_get(url, self.headers))
        detail = url_html.xpath('//*[@id="content"]/div')[0]
        detail_html = etree.tostring(detail, method='HTML')
        detail_html = html.unescape(detail_html.decode())
        detail_text = url_html.xpath('string(//*[@id="content"]/div)').replace('\xa0', '').replace('\n', '').replace('\r', '').replace('\t',
                                                                                                                  '').replace(
            ' ', '').replace('\xa5', '')
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
        item['resource'] = '中招联合（山西）招标采购网'
        item['shi'] = int(str(item["nativeplace"]).split('.')[0])
        item['sheng'] = 2500
        item['removal']= title
        process_item(item)

    def get_nativeplace(self, addr):
        city = ''
        city_list = [['2501', '太原市'], ['2501.001', '小店区'], ['2501.01', '古交市'], ['2501.002', '迎泽区'], ['2501.003', '杏花岭区'], ['2501.004', '尖草坪区'], ['2501.005', '万柏林区'], ['2501.006', '晋源区'], ['2501.007', '清徐县'], ['2501.008', '阳曲县'], ['2501.009', '娄烦县'], ['2502', '大同市'], ['2502.001', '南郊区'], ['2502.01', '城区'], ['2502.011', '矿区'], ['2502.012', '南郊区'], ['2502.002', '新荣区'], ['2502.003', '阳高县'], ['2502.004', '天镇县'], ['2502.005', '广灵县'], ['2502.006', '灵丘县'], ['2502.007', '浑源县'], ['2502.008', '左云县'], ['2502.009', '大同县'], ['2503', '阳泉市'], ['2503.001', '城区'], ['2503.002', '矿区'], ['2503.003', '郊区'], ['2503.004', '平定县'], ['2503.005', '盂县'], ['2504', '长治市'], ['2504.001', '城区'], ['2504.01', '武乡县'], ['2504.011', '沁县'], ['2504.012', '沁源县'], ['2504.013', '潞城市'], ['2504.002', '郊区'], ['2504.003', '长治县'], ['2504.004', '襄垣县'], ['2504.005', '屯留县'], ['2504.006', '平顺县'], ['2504.007', '黎城县'], ['2504.008', '壶关县'], ['2504.009', '长子县'], ['2505', '晋城市'], ['2505.001', '城区'], ['2505.002', '沁水县'], ['2505.003', '阳城县'], ['2505.004', '陵川县'], ['2505.005', '泽州县'], ['2505.006', '高平市'], ['2506', '朔州市'], ['2506.001', '朔城区'], ['2506.002', '平鲁区'], ['2506.003', '山阴县'], ['2506.004', '应县'], ['2506.005', '右玉县'], ['2506.006', '怀仁县'], ['2507', '晋中市'], ['2507.001', '榆次区'], ['2507.01', '灵石县'], ['2507.011', '介休市'], ['2507.002', '榆社县'], ['2507.003', '左权县'], ['2507.004', '和顺县'], ['2507.005', '昔阳县'], ['2507.006', '寿阳县'], ['2507.007', '太谷县'], ['2507.008', '祁县'], ['2507.009', '平遥县'], ['2508', '运城市'], ['2508.001', '盐湖区'], ['2508.01', '平陆县'], ['2508.011', '芮城县'], ['2508.012', '永济市'], ['2508.013', '河津市'], ['2508.002', '临猗县'], ['2508.003', '万荣县'], ['2508.004', '闻喜县'], ['2508.005', '稷山县'], ['2508.006', '新绛县'], ['2508.007', '绛县'], ['2508.008', '垣曲县'], ['2508.009', '夏县'], ['2509', '忻州市'], ['2509.001', '忻府区'], ['2509.01', '岢岚县'], ['2509.011', '河曲县'], ['2509.012', '保德县'], ['2509.013', '偏关县'], ['2509.014', '原平市'], ['2509.002', '定襄县'], ['2509.003', '五台县'], ['2509.004', '代县'], ['2509.005', '繁峙县'], ['2509.006', '宁武县'], ['2509.007', '静乐县'], ['2509.008', '神池县'], ['2509.009', '五寨县'], ['2510', '临汾市'], ['2510.001', '尧都区'], ['2510.01', '乡宁县'], ['2510.011', '大宁县'], ['2510.012', '隰县'], ['2510.013', '永和县'], ['2510.014', '蒲县'], ['2510.015', '汾西县'], ['2510.016', '侯马市'], ['2510.017', '霍州市'], ['2510.002', '曲沃县'], ['2510.003', '翼城县'], ['2510.004', '襄汾县'], ['2510.005', '洪洞县'], ['2510.006', '古县'], ['2510.007', '安泽县'], ['2510.008', '浮山县'], ['2510.009', '吉县'], ['2511', '吕梁市'], ['2511.001', '离石区'], ['2511.01', '中阳县'], ['2511.011', '交口县'], ['2511.012', '孝义市'], ['2511.013', '汾阳市'], ['2511.002', '文水县'], ['2511.003', '交城县'], ['2511.004', '兴县'], ['2511.005', '临县'], ['2511.006', '柳林县'], ['2511.007', '石楼县'], ['2511.008', '岚县'], ['2511.009', '方山县']]

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
        jl = shanxi_zbcg()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
        tool.send_error('报错文件：'+str(os.path.basename(__file__))+'报错信息：'+str(e))


