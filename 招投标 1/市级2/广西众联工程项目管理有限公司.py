# -*- coding: utf-8 -*-
import json
import re
import time, html
from lxml import etree
import tool
from save_database import process_item

# 广西众联工程项目管理有限公司
class alashan_ggzy:
    def __init__(self):
        self.url_code = [
            'http://gxzhonglian.cn/NewsList.aspx?NewsTypeKeyID=3',
            'http://gxzhonglian.cn/NewsList.aspx?NewsTypeKeyID=4',
            'http://gxzhonglian.cn/NewsList.aspx?NewsTypeKeyID=5'
        ]
        self.url = self.url_code.pop(0)
        self.headers = {
            'Accept': '*/*',
            'Content-Type': 'text/plain',
            'Cookie': 'JSESSIONID=D980623A7832F8A6ACC7BFF452E89D55; DWRSESSIONID=xzGTYIJ1XtAQg0rWY8ouhMDXwOoI~OVfkzn; JSESSIONID=D980623A7832F8A6ACC7BFF452E89D55; JSESSIONID=D980623A7832F8A6ACC7BFF452E89D55; DWRSESSIONID=xzGTYIJ1XtAQg0rWY8ouhMDXwOoI~OVfkzn',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
        }

    def parse(self):
        date = tool.date
        # date = '2021-07-27'
        page = 0
        while True:
            page += 1
            print('*' * 20, page, '*' * 20)
            data = {
                '__EVENTTARGET':'grdNews$ctl23$LinkButton3',
                '__EVENTARGUMENT':'',
                '__VIEWSTATE':'2',
                '__VIEWSTATEGENERATOR':'3',
                '__VIEWSTATEENCRYPTED':'',
                '__EVENTVALIDATION':'4',
                'Top1$incontent':''
            }
            if page == 1:
                text = tool.requests_get_bm(self.url, self.headers)
            else:
                text = tool.requests_post_bm(self.url, data, self.headers)
            if 'http://host4455326.xincache1.cn/xinnety.html' in text:
                print('当前链接地址或网站因含有违规内容，暂时无法访问')
                self.url = self.url_code.pop(0)

                continue
            url_ht = etree.HTML(text)
            data['__VIEWSTATE'] = url_ht.xpath('//*[@id="__VIEWSTATE"]/@value')[0]
            data['__VIEWSTATEGENERATOR'] = url_ht.xpath('//*[@id="__VIEWSTATEGENERATOR"]/@value')[0]
            data['__EVENTVALIDATION'] = url_ht.xpath('//*[@id="__EVENTVALIDATION"]/@value')[0]
            detail = url_ht.xpath('//*[@id="grdNews"]/tr')
            # print(111, detail)
            # time.sleep(666)
            for li in detail:
                title = li.xpath('./td[1]/a/text()')[0].replace('\r', '').replace('\t', '').replace(' ', '').replace('\n', '')
                url = 'http://gxzhonglian.cn/'+li.xpath('./td[1]/a/@href')[0]
                date_Today = li.xpath('./td[2]/text()')[0].replace('\r', '').replace('\t', '').replace(' ', '').replace('[', '').replace(']', '')
                # print(title, url, date_Today)
                # time.sleep(666)
                if tool.Transformation(date) <= tool.Transformation(date_Today):
                    if tool.removal(title, date):
                        self.parse_detile(title, url, date_Today)
                    else:
                        print('【existence】', url)
                        continue
                else:
                    print('日期不符, 正在切换类型...', date_Today, self.url)
                    self.url = self.url_code.pop(0)
                    page=0
                    break
            if page == 20:
                self.url = self.url_code.pop(0)
                break

    def parse_detile(self, title, url, date):
        print(url)
        url_text = tool.requests_get_bm(url, self.headers)
        url_html = etree.HTML(url_text)
        detail = url_html.xpath('//*[@id="form1"]/div[4]/div[3]')[0]
        detail_html = etree.tostring(detail, method='HTML')
        detail_html = html.unescape(detail_html.decode()).replace('\xa0', '')
        detail_text = url_html.xpath('string(//*[@id="form1"]/div[4]/div[3])').replace('\xa0', '').replace('\n', '').replace('\r', '').replace('\t',
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
        item['resource'] = '广西众联工程项目管理有限公司'
        item['shi'] = int(item["nativeplace"])
        item['sheng'] = 10500
        item['removal']= title
        process_item(item)
        # print(item['nativeplace'], item['title'])

    def get_nativeplace(self, addr):
        city_list = [['10501', '南宁市'], ['10501.001', '兴宁区'], ['10501.01', '上林县'], ['10501.011', '宾阳县'], ['10501.012', '横县'], ['10501.002', '青秀区'], ['10501.003', '江南区'], ['10501.004', '西乡塘区'], ['10501.005', '良庆区'], ['10501.006', '邕宁区'], ['10501.007', '武鸣县'], ['10501.008', '隆安县'], ['10501.009', '马山县'], ['10502', '柳州市'], ['10502.001', '城中区'], ['10502.01', '三江侗族自治县'], ['10502.002', '鱼峰区'], ['10502.003', '柳南区'], ['10502.004', '柳北区'], ['10502.005', '柳江县'], ['10502.006', '柳城县'], ['10502.007', '鹿寨县'], ['10502.008', '融安县'], ['10502.009', '融水苗族自治县'], ['10503', '桂林市'], ['10503.001', '秀峰区'], ['10503.01', '兴安县'], ['10503.011', '永福县'], ['10503.012', '灌阳县'], ['10503.013', '龙胜各族自治县'], ['10503.014', '资源县'], ['10503.015', '平乐县'], ['10503.016', '荔蒲县'], ['10503.017', '恭城瑶族自治县'], ['10503.002', '叠彩区'], ['10503.003', '象山区'], ['10503.004', '七星区'], ['10503.005', '雁山区'], ['10503.006', '阳朔县'], ['10503.007', '临桂县'], ['10503.008', '灵川县'], ['10503.009', '全州县'], ['10504', '梧州市'], ['10504.001', '万秀区'], ['10504.002', '蝶山区'], ['10504.003', '长洲区'], ['10504.004', '苍梧县'], ['10504.005', '藤县'], ['10504.006', '蒙山县'], ['10504.007', '岑溪市'], ['10505', '北海市'], ['10505.001', '海城区'], ['10505.002', '银海区'], ['10505.003', '铁山港区'], ['10505.004', '合浦县'], ['10506', '防城港市'], ['10506.001', '港口区'], ['10506.002', '防城区'], ['10506.003', '上思县'], ['10506.004', '东兴市'], ['10507', '钦州市'], ['10507.001', '钦南区'], ['10507.002', '钦北区'], ['10507.003', '灵山县'], ['10507.004', '浦北县'], ['10508', '贵港市'], ['10508.001', '港北区'], ['10508.002', '港南区'], ['10508.003', '覃塘区'], ['10508.004', '平南县'], ['10508.005', '桂平市'], ['10509', '玉林市'], ['10509.001', '玉州区'], ['10509.002', '容县'], ['10509.003', '陆川县'], ['10509.004', '博白县'], ['10509.005', '兴业县'], ['10509.006', '北流市'], ['10510', '百色市'], ['10510.001', '右江区'], ['10510.01', '田林县'], ['10510.011', '西林县'], ['10510.012', '隆林各族自治县'], ['10510.002', '田阳县'], ['10510.003', '田东县'], ['10510.004', '平果县'], ['10510.005', '德保县'], ['10510.006', '靖西县'], ['10510.007', '那坡县'], ['10510.008', '凌云县'], ['10510.009', '乐业县'], ['10511', '贺州市'], ['10511.001', '八步区'], ['10511.002', '昭平县'], ['10511.003', '钟山县'], ['10511.004', '富川瑶族自治县'], ['10512', '河池市'], ['10512.001', '金城江区'], ['10512.01', '大化瑶族自治县'], ['10512.011', '宜州市'], ['10512.002', '南丹县'], ['10512.003', '天峨县'], ['10512.004', '凤山县'], ['10512.005', '东兰县'], ['10512.006', '罗城仫佬族自治县'], ['10512.007', '环江毛南族自治县'], ['10512.008', '巴马瑶族自治县'], ['10512.009', '都安瑶族自治县'], ['10513', '来宾市'], ['10513.001', '兴宾区'], ['10513.002', '忻城县'], ['10513.003', '象州县'], ['10513.004', '武宣县'], ['10513.005', '金秀瑶族自治县'], ['10513.006', '合山市'], ['10514', '崇左市'], ['10514.001', '江洲区'], ['10514.002', '扶绥县'], ['10514.003', '宁明县'], ['10514.004', '龙州县'], ['10514.005', '大新县'], ['10514.006', '天等县'], ['10514.007', '凭祥市']]

        for i in city_list:
            if i[1] in addr:
                return float(i[0])
        return 10500

if __name__ == '__main__':
    import traceback, os
    try:
        jl = alashan_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
        if 'pop from empty list'!=str(e):
            print('报错')
            traceback.print_exc()
            with open('../error_name.txt', 'a+', encoding='utf-8')as f:
                f.write(str(os.path.basename(__file__)))
                f.write('\n')
                f.write(str(traceback.format_exc()))
                f.write('\n')
        else:
            with open('../success.txt', 'a+', encoding='utf-8')as f:
                f.write(str(os.path.basename(__file__)))
                f.write('\n')
                f.write(str('无连接抓取'))
                f.write('\n')

