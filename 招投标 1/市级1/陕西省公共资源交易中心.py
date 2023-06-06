# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 陕西省公共资源交易中心
class baoshan_ggzy:
    def __init__(self):
        self.url_list = [
            'http://www.sxggzyjy.cn/jydt/001001/001001001/{}.html',
            'http://www.sxggzyjy.cn/jydt/001001/001001004/{}.html',
        ]
        self.url = self.url_list.pop(0)
        self.headers = {
            'Cookie': 'homeid=1a444a31-e460-47ff-9931-1c075c0f3cd8',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        }

    def parse(self):
        date = tool.date
        # date = '2020-12-11'
        page = 0
        while True:
            page += 1
            if page == 1:
                text = tool.requests_get(self.url.format('subPage_jyxx'), self.headers)
            else:
                text = tool.requests_get(self.url.format(page), self.headers)
            print('*' * 20, page, '*' * 20)
            html = HTML(text)
            # print(11, text)
            # time.sleep(6666)
            detail = html.xpath('//*[@class="ewb-list"]/li')
            for li in detail:
                title = li.xpath('./a/@title')[0].replace('\n', '').replace('\r', '')\
                    .replace('\t', '').replace(' ', '')
                url = li.xpath('./a/@href')[0]
                if 'http' not in url:
                    if '../../' in url:
                        url = 'http://www.sxggzyjy.cn' + url[5:]
                    elif '../' in url:
                        url = 'http://www.sxggzyjy.cn' + url[2:]
                    elif './' in url:
                        url = 'http://www.sxggzyjy.cn' + url[1:]
                    else:
                        url = 'http://www.sxggzyjy.cn' + url
                date_Today = li.xpath('./span/text()')[0].replace('\n', '').replace('\r', '')\
                    .replace('\t', '').replace(' ', '').replace('.', '-')
                if '测试' in title:
                    continue
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
                    return


    def parse_detile(self, title, url, date):
        print(url)
        t = tool.requests_get(url, self.headers)
        url_html = etree.HTML(t)
        try:
            detail = url_html.xpath('//*[@id="mainContent"]')[0]
            detail_html = etree.tostring(detail, method='HTML')
            detail_html = html.unescape(detail_html.decode()).replace('浏览次数：', '').replace('原文链接', '')
            detail_text = url_html.xpath('string(//*[@id="mainContent"])').replace('\xa0', '').replace('\n', ''). \
                replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
        except:
            try:
                detail = url_html.xpath('//*[@id="c"]/div[2]')[0]
                detail_html = etree.tostring(detail, method='HTML')
                detail_html = html.unescape(detail_html.decode()).replace('浏览次数：', '').replace('原文链接', '')
                detail_text = url_html.xpath('string(//*[@id="c"]/div[2])').replace('\xa0', '').replace('\n', ''). \
                    replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
            except:
                try:
                    detail = url_html.xpath('//*[@id="mainContent"]')[0]
                    detail_html = etree.tostring(detail, method='HTML')
                    detail_html = html.unescape(detail_html.decode()).replace('浏览次数：', '').replace('原文链接', '')
                    detail_text = url_html.xpath('string(//*[@id="mainContent"])').replace('\xa0', '').replace('\n', ''). \
                        replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
                except:
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
        item['resource'] = '陕西省公共资源交易中心'
        item['shi'] = int(item['nativeplace'])
        item['sheng'] = 14000
        item['removal']= title
        process_item(item)

    def get_nativeplace(self, addr):
        city = ''
        city_list = [['14001', '西安市'], ['14001.001', '新城区'], ['14001.01', '蓝田县'], ['14001.011', '周至县'], ['14001.012', '户县'], ['14001.013', '高陵县'], ['14001.002', '碑林区'], ['14001.003', '莲湖区'], ['14001.004', '灞桥区'], ['14001.005', '未央区'], ['14001.006', '雁塔区'], ['14001.007', '阎良区'], ['14001.008', '临潼区'], ['14001.009', '长安区'], ['14002', '铜川市'], ['14002.001', '王益区'], ['14002.002', '印台区'], ['14002.003', '耀州区'], ['14002.004', '宜君县'], ['14003', '宝鸡市'], ['14003.001', '滨区'], ['14003.01', '麟游县'], ['14003.011', '凤县'], ['14003.012', '太白县'], ['14003.002', '金台区'], ['14003.003', '陈仓区'], ['14003.004', '凤翔县'], ['14003.005', '岐山县'], ['14003.006', '扶风县'], ['14003.007', '眉县'], ['14003.008', '陇县'], ['14003.009', '千阳县'], ['14004', '咸阳市'], ['14004.001', '秦都区'], ['14004.01', '长武县'], ['14004.011', '旬邑县'], ['14004.012', '淳化县'], ['14004.013', '武功县'], ['14004.014', '兴平市'], ['14004.002', '杨凌区'], ['14004.003', '渭城区'], ['14004.004', '三原县'], ['14004.005', '泾阳县'], ['14004.006', '乾县'], ['14004.007', '礼泉县'], ['14004.008', '永寿县'], ['14004.009', '彬县'], ['14005', '渭南市'], ['14005.001', '临渭区'], ['14005.01', '韩城市'], ['14005.011', '华阴市'], ['14005.002', '华县'], ['14005.003', '潼关县'], ['14005.004', '大荔县'], ['14005.005', '合阳县'], ['14005.006', '澄城县'], ['14005.007', '蒲城县'], ['14005.008', '白水县'], ['14005.009', '富平县'], ['14006', '延安市'], ['14006.001', '宝塔区'], ['14006.01', '洛川县'], ['14006.011', '宜川县'], ['14006.012', '黄龙县'], ['14006.013', '黄陵县'], ['14006.002', '延长县'], ['14006.003', '延川县'], ['14006.004', '子长县'], ['14006.005', '安塞县'], ['14006.006', '志丹县'], ['14006.007', '吴旗县'], ['14006.008', '甘泉县'], ['14006.009', '富县'], ['14007', '汉中市'], ['14007.001', '汉台区'], ['14007.01', '留坝县'], ['14007.011', '佛坪县'], ['14007.002', '南郑县'], ['14007.003', '城固县'], ['14007.004', '洋县'], ['14007.005', '西乡县'], ['14007.006', '勉县'], ['14007.007', '宁强县'], ['14007.008', '略阳县'], ['14007.009', '镇巴县'], ['14008', '榆林市'], ['14008.001', '榆阳区'], ['14008.01', '吴堡县'], ['14008.011', '清涧县'], ['14008.012', '子洲县'], ['14008.002', '神木县'], ['14008.003', '府谷县'], ['14008.004', '横山县'], ['14008.005', '靖边县'], ['14008.006', '定边县'], ['14008.007', '绥德县'], ['14008.008', '米脂县'], ['14008.009', '佳县'], ['14009', '安康市'], ['14009.001', '汉滨区'], ['14009.01', '白河县'], ['14009.002', '汉阴县'], ['14009.003', '石泉县'], ['14009.004', '宁陕县'], ['14009.005', '紫阳县'], ['14009.006', '岚皋县'], ['14009.007', '平利县'], ['14009.008', '镇坪县'], ['14009.009', '旬阳县'], ['14010', '商洛市'], ['14010.001', '商州区'], ['14010.002', '洛南县'], ['14010.003', '丹凤县'], ['14010.004', '商南县'], ['14010.005', '山阳县'], ['14010.006', '镇安县'], ['14010.007', '柞水县']]

        for i in city_list:
            if i[1] in addr:
                city = float(i[0])
                break
        if city == '':
            city = 14000
        return city

if __name__ == '__main__':
    import traceback,os
    try:
        jl = baoshan_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
        tool.send_error('报错文件：'+str(os.path.basename(__file__))+'报错信息：'+str(e))


