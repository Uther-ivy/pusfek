# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 西藏公共资源交易信息网
class baoshan_ggzy:
    def __init__(self):
        self.url_list = [
            'http://www.xzggzy.gov.cn:9090/gcjs/index_{}.jhtml',
            'http://www.xzggzy.gov.cn:9090/jyjggg/index_{}.jhtml',
            'http://www.xzggzy.gov.cn:9090/zbwjcq/index_{}.jhtml',
            'http://www.xzggzy.gov.cn:9090/zfcg/index_{}.jhtml',
            'http://www.xzggzy.gov.cn:9090/zbgg/index_{}.jhtml',
            'http://www.xzggzy.gov.cn:9090/gzsx/index_{}.jhtml'
        ]
        self.url = self.url_list.pop(0)
        self.headers = {
            'Cookie': 'homeid=1a444a31-e460-47ff-9931-1c075c0f3cd8',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        }

    def parse(self):
        date = tool.date
        # date = '2020-12-17'
        page = 0
        while True:
            page += 1
            text = tool.requests_get(self.url.format(page), self.headers)
            print('*' * 20, page, '*' * 20)
            html = HTML(text)
            # print(11, text)
            # time.sleep(6666)
            detail = html.xpath('//*[@class="article-list-old"]/li')
            for li in detail:
                title = li.xpath('./a/@title')[0].replace('\n', '').replace('\r', '')\
                    .replace('\t', '').replace(' ', '')
                url = li.xpath('./a/@href')[0]
                if 'http' not in url:
                    if '../../' in url:
                        url = 'http://www.xzggzy.gov.cn:9090' + url[5:]
                    elif '../' in url:
                        url = 'http://www.xzggzy.gov.cn:9090' + url[2:]
                    elif './' in url:
                        url = 'http://www.xzggzy.gov.cn:9090' + url[1:]
                    else:
                        url = 'http://www.xzggzy.gov.cn:9090' + url
                date_Today = li.xpath('./div/text()')[0][:10].replace('\n', '').replace('\r', '')\
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
        detail = url_html.xpath('/html/body/div[3]/div[2]/div[3]')[0]
        detail_html = etree.tostring(detail, method='HTML')
        detail_html = html.unescape(detail_html.decode()).replace('浏览次数：', '').replace('原文链接', '')
        detail_text = url_html.xpath('string(/html/body/div[3]/div[2]/div[3])').replace('\xa0', '').replace('\n', ''). \
            replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
        if len(detail_html) < 300:
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
        item['winner'] = tool.get_winner(detail_text)
        item['address'] = tool.get_address(detail_text)
        item['linkman'] = tool.get_linkman(detail_text)
        item['function'] = tool.get_function(detail_text)
        item['resource'] = '西藏公共资源交易信息网'
        item['shi'] = int(item['nativeplace'])
        item['sheng'] = 13500
        item['removal']= title
        process_item(item)

    def get_nativeplace(self, addr):
        city = ''
        city_list = [['13501', '拉萨市'], ['13501.001', '城关区'], ['13501.002', '林周县'], ['13501.003', '当雄县'], ['13501.004', '尼木县'], ['13501.005', '曲水县'], ['13501.006', '堆龙德庆县'], ['13501.007', '达孜县'], ['13501.008', '墨竹工卡县'], ['13502', '昌都地区'], ['13502.001', '昌都县'], ['13502.01', '洛隆县'], ['13502.011', '边坝县'], ['13502.002', '江达县'], ['13502.003', '贡觉县'], ['13502.004', '类乌齐县'], ['13502.005', '丁青县'], ['13502.006', '察雅县'], ['13502.007', '八宿县'], ['13502.008', '左贡县'], ['13502.009', '芒康县'], ['13503', '山南地区'], ['13503.001', '乃东县'], ['13503.01', '隆子县'], ['13503.011', '错那县'], ['13503.012', '浪卡子县'], ['13503.002', '扎囊县'], ['13503.003', '贡嘎县'], ['13503.004', '桑日县'], ['13503.005', '琼结县'], ['13503.006', '曲松县'], ['13503.007', '措美县'], ['13503.008', '洛扎县'], ['13503.009', '加查县'], ['13504', '日喀则地区'], ['13504.001', '日喀则市'], ['13504.01', '仁布县'], ['13504.011', '康马县'], ['13504.012', '定结县'], ['13504.013', '仲巴县'], ['13504.014', '亚东县'], ['13504.015', '吉隆县'], ['13504.016', '聂拉木县'], ['13504.017', '萨嘎县'], ['13504.018', '岗巴县'], ['13504.002', '南木林县'], ['13504.003', '江孜县'], ['13504.004', '定日县'], ['13504.005', '萨迦县'], ['13504.006', '拉孜县'], ['13504.007', '昂仁县'], ['13504.008', '谢通门县'], ['13504.009', '白朗县'], ['13505', '那曲地区'], ['13505.001', '那曲县'], ['13505.01', '尼玛县'], ['13505.002', '嘉黎县'], ['13505.003', '比如县'], ['13505.004', '聂荣县'], ['13505.005', '安多县'], ['13505.006', '申扎县'], ['13505.007', '索县'], ['13505.008', '班戈县'], ['13505.009', '巴青县'], ['13506', '阿里地区'], ['13506.001', '普兰县'], ['13506.002', '札达县'], ['13506.003', '噶尔县'], ['13506.004', '日土县'], ['13506.005', '革吉县'], ['13506.006', '改则县'], ['13506.007', '措勤县'], ['13507', '林芝地区'], ['13507.001', '林芝县'], ['13507.002', '工布江达县'], ['13507.003', '米林县'], ['13507.004', '墨脱县'], ['13507.005', '波密县'], ['13507.006', '察隅县'], ['13507.007', '朗县']]

        for i in city_list:
            if i[1] in addr:
                city = float(i[0])
                break
        if city == '':
            city = 13500
        return city

if __name__ == '__main__':
    import traceback, os
    try:
        jl = baoshan_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
        tool.send_error('报错文件：'+str(os.path.basename(__file__))+'报错信息：'+str(e))


