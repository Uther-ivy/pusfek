# -*- coding: utf-8 -*-
import re
import time, html, json
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 广西公共资源网
class xinyang_ggzy:
    def __init__(self):
        self.url_list = [
            'http://gxggzy.gxzf.gov.cn/igs/front/search/list.html?&filter%5BDOCTITLE%5D=&pageNumber={}&pageSize=10&index=gxggzy_jyfw&type=jyfw&filter%5Bparentparentid%5D=&filter%5Bparentchnldesc%5D=&filter%5Bchnldesc%5D=&filter%5BSITEID%5D=234&orderProperty=PUBDATE&orderDirection=desc&filter%5BAVAILABLE%5D=true'
        ]
        self.url = self.url_list.pop(0)
        self.headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Connection': 'keep-alive',
            'Cookie': '_trs_uv=kqaj8euy_3928_10a7; token=8aee98b4-5a1c-4c64-b725-487be4021cd4; uuid=8aee98b4-5a1c-4c64-b725-487be4021cd4; _trs_ua_s_1=kqakh51x_3928_dtix',
            'Host': 'gxggzy.gxzf.gov.cn',
            'Referer': 'http://gxggzy.gxzf.gov.cn/jyfw/jyfw_gcjs/tlgc/zbgg/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
        }

    def parse(self):
        date = tool.date
        # date = '2021-07-29'
        page = 0
        while True:
            page += 1
            tool.session_get('http://ta.trs.cn/c/1.gif?event=mousedown&sr=1920*1080&br=1903*1558&dpr=1.0000&clicktype=2&mpId=3928&cs=kqakh51x_3928_dtix&cu=kqaj8euy_3928_10a7&pv=3928_kqakk0af_g19x&url=http%3A%2F%2Fgxggzy.gxzf.gov.cn%2Fjyfw%2Fjyfw_gcjs%2Ftlgc%2Fzbgg%2F&e_tu=javascript%3A%3B&e_tp=javascript&e_tx=%E5%85%A8%E9%83%A8&e_tn=a&e_iac=1&e_et=mouseup&e_nd=Ly8qW0BpZD0nYnVzaW5lc3NUeXBlSXRlbXNBbGwnXS9h&e_etd=2&x=506&y=492&x2=-454')
            tool.session_get('http://ta.trs.cn/c/1.gif?event=mousedown&sr=1920*1080&br=1903*1558&dpr=1.0000&clicktype=3&url=http%3A%2F%2Fgxggzy.gxzf.gov.cn%2Fjyfw%2Fjyfw_gcjs%2Ftlgc%2Fzbgg%2F&br=1903*1558&pa=[{x:506,y:492}]&pb=[{z:-454,y:492}]')
            text = tool.session_get(self.url.format(page))
            print('*' * 20, page, '*' * 20)
            try:
                detail = json.loads(text)['page']['content']
            except Exception as e:
                print(text)
                page -= 1
                time.sleep(5)
                continue
            for li in detail:
                try:
                    title = li['DOCTITLE']
                except:
                    continue
                url = li['DOCPUBURL']
                date_Today = li['PUBDATE'][:10].replace('\n', '').replace('\t', '').replace('\r', '') \
                    .replace(' ', '').replace('/', '-')
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
                    page=0
                    break
            if page == 30:
                self.url = self.url_list.pop(0)
                page = 0

    def parse_detile(self, title, url, date):
        print(url)
        url_html = etree.HTML(tool.requests_get(url, self.headers))
        try:
            detail = url_html.xpath('/html/body/div[11]/div[2]/div/div[3]')[0]
            detail_html = etree.tostring(detail, method='HTML')
            detail_html = html.unescape(detail_html.decode()).replace('\xa0', '').replace('\ufeff', '')
            detail_text = url_html.xpath('string(/html/body/div[11]/div[2]/div/div[3])') \
                .replace('\xa0', '').replace('\n', '').replace('\r', '').replace('\t', '') \
                .replace(' ', '').replace('\xa5', '').replace('\ufeff', '')
        except:
            try:
                detail = url_html.xpath('//*[@class="view TRS_UEDITOR trs_paper_default trs_word"]')[0]
                detail_html = etree.tostring(detail, method='HTML')
                detail_html = html.unescape(detail_html.decode()).replace('\xa0', '').replace('\ufeff', '')
                detail_text = url_html.xpath('string(//*[@class="view TRS_UEDITOR trs_paper_default trs_word"])') \
                    .replace('\xa0', '').replace('\n', '').replace('\r', '').replace('\t', '') \
                    .replace(' ', '').replace('\xa5', '').replace('\ufeff', '')
            except:
                detail = url_html.xpath('//*[@class="ewb-details-info"]')[0]
                detail_html = etree.tostring(detail, method='HTML')
                detail_html = html.unescape(detail_html.decode()).replace('\xa0', '').replace('\ufeff', '')
                detail_text = url_html.xpath('string(//*[@class="ewb-details-info"])') \
                    .replace('\xa0', '').replace('\n', '').replace('\r', '').replace('\t', '') \
                    .replace(' ', '').replace('\xa5', '').replace('\ufeff', '')
        # print(111, detail_text.replace('\xa0','').replace('\xa5',''))
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
        item['body'] = detail_html
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
        item['resource'] = '广西公共资源网'
        item['shi'] = int(str(item["nativeplace"]).split('.')[0])
        item['sheng'] = 10500
        item['removal']= title
        process_item(item)
        # print(item['body'])

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
        jl = xinyang_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
        # tool.send_error('报错文件：'+str(os.path.basename(__file__))+'报错信息：'+str(e))


