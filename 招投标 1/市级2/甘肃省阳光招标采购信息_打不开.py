# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 甘肃省阳光招标采购信息
class xinyang_ggzy:
    def __init__(self):
        self.url_list = [
            '1',
            '3'
        ]
        self.url = self.url_list.pop(0)
        self.headers = {
    # 'Accept': 'text/html, */*; q=0.01',
    # 'Accept-Encoding': 'gzip, deflate',
    # 'Accept-Language': 'zh-CN,zh;q=0.9',
    # 'Connection': 'keep-alive',
    # 'Content-Length': '28',
    # 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    # 'Cookie': 'jeeplus.session.id=d87ec3cf168948369f97c8a381100454; JSESSIONID=9F7A954DF3CD0CA2AD624F2F11178DCF; SERVERID=a54ced1935cc37de956819248ff32884|1614587934|1614587072',
    # 'Host': 'ygjy.ggzyjy.gansu.gov.cn:3040',
    # 'Origin': 'http://ygjy.ggzyjy.gansu.gov.cn:3040',
    # 'Referer': 'http://ygjy.ggzyjy.gansu.gov.cn:3040/f/engineer/36114/engineerAnno.html',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
    # 'X-Requested-With': 'XMLHttpRequest'

}

    def parse(self):
        date = tool.date
        # date = '2020-09-27'
        page = 0
        url_to = 'http://ygjy.ggzyjy.gansu.gov.cn:3040/f/getAnnoList'
        data = {
            'annoType': '1',
            'annoTitle': '',
            'platformCode': '',
            'pageNo': '',
            'pageSize': '15'
        }
        while True:
            page += 1
            data['annoType'] = self.url
            data['pageNo'] = page
            text = '<div id="body">' + tool.requests_post(url_to, data, self.headers) + '</div>'
            # print(text)
            html = HTML(text)
            # print(11, text)
            # time.sleep(666)
            detail = html.xpath('//*[@id="body"]/a')
            print('*' * 20, page, '*' * 20)
            for li in detail:
                title = li.xpath('./div/@title')[0]
                url = 'http://ygjy.ggzyjy.gansu.gov.cn:3040' + li.xpath('./@href')[0]
                date_Today = li.xpath('./span/text()')[0].replace('\n', '').replace('\t', '').replace('\r',
                                                                                                       '').replace(
                    ' ', '')
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
        # resp=requests.get(url=url,headers=self.headers).text
        resp=tool.requests_get(url=url,headers=self.headers)
        projectId=re.findall("data:{projectId:'(.*?)'},",resp)[0]
        annoId=re.findall("annoId:'(.*?)',projectId",resp)[0]
        data={
            'annoId':annoId ,
            'projectId': projectId
        }
        # print(data)
        url='http://ygjy.ggzyjy.gansu.gov.cn:3040/f/engineer/getAnnoDetail'
        t = requests.post(url=url,data=data,headers=self.headers).text
        # print(t)
        # detail_html = requests.post(url_to, data, self.headers).text
        # print(data, detail_html)
        # time.sleep(6666)
        url_html = etree.HTML(t)
        detail = url_html.xpath('//ul[@class="CaiGouPrinciple"]')[0]
        detail_html = etree.tostring(detail, method='HTML')
        detail_html = html.unescape(detail_html.decode()).replace('\xa0', '').replace('\ufeff', '')
        detail_text = url_html.xpath('string(//ul[@class="CaiGouPrinciple"])') \
            .replace('\xa0', '').replace('\n', '').replace('\r', '').replace('\t', '') \
            .replace(' ', '').replace('\xa5', '').replace('\ufeff', '')
        if len(detail_html) < 200 or '系统内部错误' in detail_html:
            return 
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
        try:
            b = re.findall('<div class="CaiGouPrompt">.*?</div>', item['body'], re.S)[0]
            item['body'] = item['body'].replace(b, '')
        except:
            pass
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
        item['nativeplace'] = self.get_nativeplace_to(item['title'])
        item['linkman'] = tool.get_linkman(detail_text)
        item['function'] = tool.get_function(detail_text)
        item['resource'] = '甘肃省阳光招标采购信息'
        item["shi"] = int(str(item["nativeplace"]).split('.')[0])
        item['sheng'] = 14500
        item['removal']= title
        process_item(item)
        # print(item['body'])

    def get_nativeplace_to(self, city):
        a = ''
        ls = [['14500', '甘肃'], ['14501', '兰州'], ['14501.001', '城关区'], ['14501.002', '七里河区'], ['14501.003', '西固区'], ['14501.004', '安宁区'], ['14501.005', '红古区'], ['14501.006', '永登县'], ['14501.007', '皋兰县'], ['14501.008', '榆中县'], ['14502', '嘉峪关'], ['14503', '金昌'], ['14503.001', '金川区'], ['14503.002', '永昌县'], ['14504', '白银'], ['14504.001', '白银区'], ['14504.002', '平川区'], ['14504.003', '靖远县'], ['14504.004', '会宁县'], ['14504.005', '景泰县'], ['14505', '天水'], ['14505.001', '秦城区'], ['14505.002', '北道区'], ['14505.003', '清水县'], ['14505.004', '秦安县'], ['14505.005', '甘谷县'], ['14505.006', '武山县'], ['14505.007', '张家川回族自治县'], ['14506', '武威'], ['14506.001', '凉州区'], ['14506.002', '民勤县'], ['14506.003', '古浪县'], ['14506.004', '天祝藏族自治县'], ['14507', '张掖'], ['14507.001', '甘州区'], ['14507.002', '肃南裕固族自治县'], ['14507.003', '民乐县'], ['14507.004', '临泽县'], ['14507.005', '高台县'], ['14507.006', '山丹县'], ['14508', '平凉'], ['14508.001', '崆峒区'], ['14508.002', '泾川县'], ['14508.003', '灵台县'], ['14508.004', '崇信县'], ['14508.005', '华亭县'], ['14508.006', '庄浪县'], ['14508.007', '静宁县'], ['14509', '酒泉'], ['14509.001', '肃州区'], ['14509.002', '金塔县'], ['14509.003', '安西县'], ['14509.004', '肃北蒙古族自治县'], ['14509.005', '阿克塞哈萨克族自治县'], ['14509.006', '玉门'], ['14509.007', '敦煌'], ['14510', '庆阳'], ['14510.001', '西峰区'], ['14510.002', '庆城县'], ['14510.003', '环县'], ['14510.004', '华池县'], ['14510.005', '合水县'], ['14510.006', '正宁县'], ['14510.007', '宁县'], ['14510.008', '镇原县'], ['14511', '定西'], ['14511.001', '安定区'], ['14511.002', '通渭县'], ['14511.003', '陇西县'], ['14511.004', '渭源县'], ['14511.005', '临洮县'], ['14511.006', '漳县'], ['14511.007', '岷县'], ['14512', '陇南'], ['14512.001', '武都区'], ['14512.002', '成县'], ['14512.003', '文县'], ['14512.004', '宕昌县'], ['14512.005', '康县'], ['14512.006', '西和县'], ['14512.007', '礼县'], ['14512.008', '徽县'], ['14512.009', '两当县'], ['14513', '临夏回族自治州'], ['14513.001', '临夏'], ['14513.002', '临夏县'], ['14513.003', '康乐县'], ['14513.004', '永靖县'], ['14513.005', '广河县'], ['14513.006', '和政县'], ['14513.007', '东乡族自治县'], ['14513.008', '积石山保安族东乡族撒拉族自治县'], ['14514', '甘南藏族自治州'], ['14514.001', '合作'], ['14514.002', '临潭县'], ['14514.003', '卓尼县'], ['14514.004', '舟曲县'], ['14514.005', '迭部县'], ['14514.006', '玛曲县'], ['14514.007', '碌曲县'], ['14514.008', '夏河县']]
        for i in ls:
            if i[1] in city:
                a = i[0]
                break
        if a == '':
            return 14500
        else:
            return a

if __name__ == '__main__':
    jl = xinyang_ggzy()
    jl.parse()


