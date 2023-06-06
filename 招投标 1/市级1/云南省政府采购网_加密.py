# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 云南省政府采购网
class lijiang_ggzy:
    def __init__(self):
        self.url_list = [
            'http://www.yngp.com/bulletin.do?method=moreListQuery&current={}&rowCount=10&searchPhrase=&query_sign=1',
            'http://www.yngp.com/bulletin.do?method=moreListQuery&current={}&rowCount=10&searchPhrase=&query_bulletintitle=&query_startTime=&query_endTime=&query_sign=3',
            'http://www.yngp.com/bulletin.do?method=moreListQuery&current={}&rowCount=10&searchPhrase=&query_bulletintitle=&query_startTime=&query_endTime=&query_sign=2',
            'http://www.yngp.com/bulletin.do?method=moreListQuery&current={}&rowCount=10&searchPhrase=&query_bulletintitle=&query_startTime=&query_endTime=&query_sign=7'
        ]
        self.url = self.url_list.pop(0)
        self.headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Connection': 'keep-alive',
            # 'Content-Length': '48',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Cookie': 'elvasid=af48ebdfbe58684c362ed45c9c305cae; xincaigou=49737.2918.1072.0000; JSESSIONID=fGQ7r8UtP7uEOl9PFxs0_1TM5U8AZJisuEqQP6SH29ledkDK4i9O!1575934459; __jsluid_h=975864996922cb06f9221ec9536958e0; CoreSessionId=86cc884b8580f67a4ecfaad3d925f94a7a83fd7d813f6a3e; _g_sign=4daa67b74742a033e5a9561db4679ded',
            'Host': 'www.yngp.com',
            'Origin': 'http://www.yngp.com',
            'Referer': 'http://www.yngp.com/bulletin.do?method=moreList&menuSelect=nav2',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
        
        
        }

    def parse(self):
        date = tool.date
        # date = '2020-04-07'
        page = 0
        while True:
            page += 1
            text = tool.requests_get(self.url.format(page), self.headers).replace('�', '').replace('\\', '')
            print('*' * 20, page, '*' * 20)
            try:
                detail = json.loads(text)
            except Exception as e:
                print(e)
                time.sleep(5)
                page -= 1
                continue
            for li in detail['rows']:
                title = li['bulletintitle']
                if 'query_sign=3' in self.url:
                    url = 'http://www.yngp.com/newbulletin_zz.do?method=toaddmodify&operator_state=1&lxflag=dy&flag=view&bulletin_id=' + li['bulletin_id']
                elif 'query_sign=1' in self.url:
                    url = 'http://www.yngp.com/newbulletin_zz.do?method=preinsertgomodify&operator_state=1&flag=view&bulletin_id=' + \
                          li['bulletin_id']
                elif 'query_sign=2' in self.url:
                    url = 'http://www.yngp.com/newbulletin_zz.do?method=preinsertgomodify&operator_state=1&flag=view&bulletin_id=' + \
                          li['bulletin_id']
                elif 'query_sign=7' in self.url:
                    url = 'http://www.yngp.com/newbulletin_zz.do?method=preinsertgomodify&operator_state=1&flag=view&bulletin_id=' + \
                          li['bulletin_id']
                date_Today = li['finishday']
                if date_Today == '':
                    continue
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
                    print('日期不符, 正在切换类型', date_Today)
                    self.url = self.url_list.pop(0)
                    page = 0
                    break
            if page == 20:
                self.url = self.url_list.pop(0)
                break


    def parse_detile(self, title, url, date):
        print(url)
        text = tool.requests_get(url, self.headers)
        url_html = etree.HTML(text)
        try:
            detail = url_html.xpath('//*[@class="vF_detail_content_container"]')[0]
            detail_html = etree.tostring(detail, method='HTML')
            detail_html = html.unescape(detail_html.decode()).replace('\xa0', '').replace('\xa5', '')
            detail_text = url_html.xpath('string(//*[@class="vF_detail_content_container"])').replace('\xa0', '').replace('\n', '').\
                replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
        except:
            try:
                detail = url_html.xpath('//*[@id="UserDetails"]/div[1]')[0]
                detail_html = etree.tostring(detail, method='HTML')
                detail_html = html.unescape(detail_html.decode())
                detail_text = url_html.xpath('string(//*[@id="UserDetails"]/div[1])').replace('\xa0',
                                                                                                          '').replace(
                    '\n', ''). \
                    replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
            except:
                detail = url_html.xpath('/html/body/div[2]/div/div/div[2]')[0]
                detail_html = etree.tostring(detail, method='HTML')
                detail_html = html.unescape(detail_html.decode())
                detail_text = url_html.xpath('string(/html/body/div[2]/div/div/div[2])').replace('\xa0',
                                                                                                       '').replace('\n',
                                                                                                                   ''). \
                    replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
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
        item['body'] = tool.qudiao_width(detail_html).replace('display: none;', '')
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
        item['resource'] = '云南省政府采购网'
        item['shi'] = int(str(item["nativeplace"]).split('.')[0])
        item['sheng'] = 13000
        item['removal']= title
        process_item(item)

    def get_nativeplace(self, addr):
        city = ''
        city_list = [['13001', '昆明'], ['13001.001', '五华区'], ['13001.01', '石林彝族自治县'], ['13001.011', '嵩明县'], ['13001.012', '禄劝彝族苗族自治县'], ['13001.013', '寻甸回族彝族自治县'], ['13001.014', '安宁'], ['13001.002', '盘龙区'], ['13001.003', '官渡区'], ['13001.004', '西山区'], ['13001.005', '东川区'], ['13001.006', '呈贡县'], ['13001.007', '晋宁县'], ['13001.008', '富民县'], ['13001.009', '宜良县'], ['13002', '曲靖'], ['13002.001', '麒麟区'], ['13002.002', '马龙县'], ['13002.003', '陆良县'], ['13002.004', '师宗县'], ['13002.005', '罗平县'], ['13002.006', '富源县'], ['13002.007', '会泽县'], ['13002.008', '沾益县'], ['13002.009', '宣威'], ['13003', '玉溪'], ['13003.001', '红塔区'], ['13003.002', '江川县'], ['13003.003', '澄江县'], ['13003.004', '通海县'], ['13003.005', '华宁县'], ['13003.006', '易门县'], ['13003.007', '峨山彝族自治县'], ['13003.008', '新平彝族傣族自治县'], ['13003.009', '元江哈尼族彝族傣族自治县'], ['13004', '保山'], ['13004.001', '隆阳区'], ['13004.002', '施甸县'], ['13004.003', '腾冲县'], ['13004.004', '龙陵县'], ['13004.005', '昌宁县'], ['13005', '昭通'], ['13005.001', '昭阳区'], ['13005.01', '威信县'], ['13005.011', '水富县'], ['13005.002', '鲁甸县'], ['13005.003', '巧家县'], ['13005.004', '盐津县'], ['13005.005', '大关县'], ['13005.006', '永善县'], ['13005.007', '绥江县'], ['13005.008', '镇雄县'], ['13005.009', '彝良县'], ['13006', '丽江'], ['13006.001', '古城区'], ['13006.002', '玉龙纳西族自治县'], ['13006.003', '永胜县'], ['13006.004', '华坪县'], ['13006.005', '宁蒗彝族自治县'], ['13007', '思茅'], ['13007.001', '翠云区'], ['13007.01', '西盟佤族自治县'], ['13007.002', '普洱哈尼族彝族自治县'], ['13007.003', '墨江哈尼族自治县'], ['13007.004', '景东彝族自治县'], ['13007.005', '景谷傣族彝族自治县'], ['13007.006', '镇沅彝族哈尼族拉祜族自治县'], ['13007.007', '江城哈尼族彝族自治县'], ['13007.008', '孟连傣族拉祜族佤族自治县'], ['13007.009', '澜沧拉祜族自治县'], ['13008', '临沧'], ['13008.001', '临翔区'], ['13008.002', '凤庆县'], ['13008.003', '云县'], ['13008.004', '永德县'], ['13008.005', '镇康县'], ['13008.006', '双江拉祜族佤族布朗族傣族自治县'], ['13008.007', '耿马傣族佤族自治县'], ['13008.008', '沧源佤族自治县'], ['13009', '楚雄彝族自治州'], ['13009.001', '楚雄'], ['13009.01', '禄丰县'], ['13009.002', '双柏县'], ['13009.003', '牟定县'], ['13009.004', '南华县'], ['13009.005', '姚安县'], ['13009.006', '大姚县'], ['13009.007', '永仁县'], ['13009.008', '元谋县'], ['13009.009', '武定县'], ['13010', '红河哈尼族彝族自治州'], ['13010.001', '个旧'], ['13010.01', '金平苗族瑶族傣族自治县'], ['13010.011', '绿春县'], ['13010.012', '河口瑶族自治县'], ['13010.002', '开远'], ['13010.003', '蒙自县'], ['13010.004', '屏边苗族自治县'], ['13010.005', '建水县'], ['13010.006', '石屏县'], ['13010.007', '弥勒县'], ['13010.008', '泸西县'], ['13010.009', '元阳县'], ['13011', '文山壮族苗族自治州'], ['13011.001', '文山县'], ['13011.002', '砚山县'], ['13011.003', '西畴县'], ['13011.004', '麻栗坡县'], ['13011.005', '马关县'], ['13011.006', '丘北县'], ['13011.007', '广南县'], ['13011.008', '富宁县'], ['13012', '西双版纳傣族自治州'], ['13012.001', '景洪'], ['13012.002', '勐海县'], ['13012.003', '勐腊县'], ['13013', '大理白族自治州'], ['13013.001', '大理'], ['13013.01', '洱源县'], ['13013.011', '剑川县'], ['13013.012', '鹤庆县'], ['13013.002', '漾濞彝族自治县'], ['13013.003', '祥云县'], ['13013.004', '宾川县'], ['13013.005', '弥渡县'], ['13013.006', '南涧彝族自治县'], ['13013.007', '巍山彝族回族自治县'], ['13013.008', '永平县'], ['13013.009', '云龙县'], ['13014', '德宏傣族景颇族自治州'], ['13014.001', '瑞丽'], ['13014.002', '潞西'], ['13014.003', '梁河县'], ['13014.004', '盈江县'], ['13014.005', '陇川县'], ['13015', '怒江傈僳族自治州'], ['13015.001', '泸水县'], ['13015.002', '福贡县'], ['13015.003', '贡山独龙族怒族自治县'], ['13015.004', '兰坪白族普米族自治县'], ['13016', '迪庆藏族自治州'], ['13016.001', '香格里拉县'], ['13016.002', '德钦县'], ['13016.003', '维西傈僳族自治县']]

        for i in city_list:
            if i[1] in addr:
                city = float(i[0])
                break
        if city == '':
            city = 13000
        return city

if __name__ == '__main__':
    import traceback,os
    try:
        jl = lijiang_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
        # tool.send_error('报错文件：'+str(os.path.basename(__file__))+'报错信息：'+str(e))


