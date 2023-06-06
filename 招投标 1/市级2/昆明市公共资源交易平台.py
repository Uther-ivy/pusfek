# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 昆明市公共资源交易平台
class kunming_ggzy:
    def __init__(self):
        self.code_list = [
            # 市本级
            #   工程建设
            #       招标公告
            ['["TrueLore.Web.WebUI.WebAjaxService","GetPageZBGGByCCGC",[{},15,"\xe6\x98\x86\xe6\x98\x8e\xe5\xb8\x82","11,12,13,14,15,16,17,18,19,20",'
             '"1","0","JSGC",1,"","","zhaoBiao_XiangMu_Name",""],null,null]1624007755841',
             'https://www.kmggzy.com/Jyweb/ZBGGViewNew.aspx?isbg=0&guid={}&type=%e4%ba%a4%e6%98%93%e4%bf%a1%e6%81%a'
             'f&subType=1&subType2=1&area=1&zbtype=0&xxlb=%E4%BA%A4%E6%98%93%E4%BF%A1%E6%81%AF&IsShow=1'],
            #       补遗公告
            ['["TrueLore.Web.WebUI.WebAjaxService","GetPageJYXTXXFB_JSGC",[{},15,"\xe6\x98\x86\xe6\x98\x8e\xe5\xb8\x82","11,12,13,14,15,16,17,18,19,20"'
             ',"1","JSGC","2","","","zhaoBiao_XiangMu_Name",""],null,null]1608607091140',
             'https://www.kmggzy.com/Jyweb/JYXTXXView.aspx?isBG=0&guid={}&subType2=2&subType=1&type=%e4%ba%a4%e6%98'
             '%93%e4%bf%a1%e6%81%af&area=1&xxlb=%E4%BA%A4%E6%98%93%E4%BF%A1%E6%81%AF'],
            #       评标结果公示
            ['["TrueLore.Web.WebUI.WebAjaxService","GetPageJYXTXXFB_PBJGGS",[{},15,"\xe6\x98\x86\xe6\x98\x8e\xe5\xb8\x82",'
            '"11,12,13,14,15,16,17,18,19,20","1","0","JSGC",24,"","","BDMCGGBT",""],null,null]1585878116379',
             'https://www.kmggzy.com/Jyweb/PBJGGSNewView2.aspx?isBG=0&guid={}&subType2=24&subType=1&type=%e4%ba%a4%e6%9'
             '8%93%e4%bf%a1%e6%81%af&area=1&zbtype=0'],
            #       中标结果
            ['["TrueLore.Web.WebUI.WebAjaxService","GetPageJYXTXXFB_PBJGGS",[{},15,"\xe6\x98\x86\xe6\x98\x8e\xe5\xb8\x82",'
            '"11,12,13,14,15,16,17,18,19,20","1","0","JSGC",11,"","","BDMCGGBT",""],null,null]1585878116379',
             'https://www.kmggzy.com/Jyweb/ZBJGGSNewView2.aspx?isBG=0&guid={}&subType2=11&subType=1&type=%e4%ba%a4%e6%9'
             '8%93%e4%bf%a1%e6%81%af&area=1&zbtype=0'],
            #       流标公示
            ['["TrueLore.Web.WebUI.WebAjaxService","GetPageJYXTXXFB_PBJGGS",[{},15,"\xe6\x98\x86\xe6\x98\x8e\xe5\xb8\x82",'
            '"11,12,13,14,15,16,17,18,19,20","1","0","JSGC",5,"","","BDMCGGBT",""],null,null]1585878116379',
             'https://www.kmggzy.com/Jyweb/PBJGGSNewView2.aspx?isBG=0&guid={}&subType2=5&subType=1&type=%e4%ba%a4%e6%98'
             '%93%e4%bf%a1%e6%81%af&area=1&zbtype=0'],
            #   政府采购
            #       采购公告
            ['["TrueLore.Web.WebUI.WebAjaxService","GetPageZBGGByCCGC",[{},15,"\xe6\x98\x86\xe6\x98\x8e\xe5\xb8\x82",'
            '"11,12,13,14,15,16,17,18,19,20","1","0","ZFCG","12","","","BDMCGGBT",""],null,null]1585878116379',
             'https://www.kmggzy.com/Jyweb/ZFCGView.aspx?isBG=1&guid={}&bgZBGGGuid={}&subType2=12&subType=2&'
             'type=%e4%ba%a4%e6%98%93%e4%bf%a1%e6%81%af&area=1&xxlb=%E4%BA%A4%E6%98%93%E4%BF%A1%E6%81%AF&IsShow=0'],

            #       补遗通知
            ['["TrueLore.Web.WebUI.WebAjaxService","GetPageZFCG",[{},15,"\xe6\x98\x86\xe6\x98\x8e\xe5\xb8\x82",'
            '"11,12,13,14,15,16,17,18,19,20","1","0","ZFCG","13","","","BDMCGGBT",""],null,null]1585878116379',
             'https://www.kmggzy.com/Jyweb/JYXTXXView.aspx?isBG=0&guid={}&subType2=13&subType=2&type=%e4%ba%a4%e6%98%9'
             '3%e4%bf%a1%e6%81%af&area=1&xxlb=%E4%BA%A4%E6%98%93%E4%BF%A1%E6%81%AF'],
            #       结果公示
            ['["TrueLore.Web.WebUI.WebAjaxService","GetPageZFCG",[{},15,"\xe6\x98\x86\xe6\x98\x8e\xe5\xb8\x82",'
            '"11,12,13,14,15,16,17,18,19,20","1","0","ZFCG","14","","","BDMCGGBT",""],null,null]1585878116379',
             'https://www.kmggzy.com/Jyweb/ZFCGZBJGGSViewNew.aspx?isBG=0&guid={}&subType2=14&subType=2&type=%e4%ba%a4%'
             'e6%98%93%e4%bf%a1%e6%81%af&area=1&xxlb=%E4%BA%A4%E6%98%93%E4%BF%A1%E6%81%AF'],
            #       流标公示
           [ '["TrueLore.Web.WebUI.WebAjaxService","GetPageJYXTXXFB_ZFCG",[{},15,"\xe6\x98\x86\xe6\x98\x8e\xe5\xb8\x82",'
            '"11,12,13,14,15,16,17,18,19,20","1","0","ZFCG","28","","","BDMCGGBT",""],null,null]1585878116379',
             'https://www.kmggzy.com/Jyweb/ZFCGZBJGGSViewNew.aspx?isBG=0&guid={}&subType2=28&subType=2&type=%e4%ba%a4%e'
             '6%98%93%e4%bf%a1%e6%81%af&area=1&xxlb=%E4%BA%A4%E6%98%93%E4%BF%A1%E6%81%AF']
        ]
        self.url = 'https://www.kmggzy.com/TrueLoreAjax/TrueLore.Web.WebUI.AjaxHelper,TrueLore.Web.WebUI.ashx'
        self.code = self.code_list.pop(0)
        self.headers = {
            'ajax-method': 'AjaxMethodFactory',
            # 'Cookie': 'ASP.NET_SessionId=irwyyayh3dtwq5zxunzlnq3x',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        }

    def parse(self):
        date = tool.date
        # date = '2021-07-30'
        page = 0
        while True:
            num = page * 15
            page += 1
            res = str(requests.post(self.url, data=self.code[0].format(num), headers=self.headers).text).replace("'", '"')
            res = res[1:-1].replace('\\r', '').replace('\\n', '').replace('\t', '').replace(' ', '').replace('\\', '')
            print('*' * 20, page, '*' * 20)
            # time.sleep(6666)
            detail = json.loads(res)['data']
            for i in detail:
                try:
                    title = i['title']
                except:
                    title = i['zhaoBiao_XiangMu_Name']
                if 'ZFCGView.aspx' in self.code[1]:
                    try:
                        url = self.code[1].format(i['yuanGongGao_Guid'], i['guid'])
                    except:
                        url = 'https://www.kmggzy.com/Jyweb/ZFCGView.aspx?isBG=&guid={}&subType2=12&subType=2&type=%e4%ba%a4%e6%98%93%e4%bf%a1%e6%81%af&area=1&xxlb=%E4%BA%A4%E6%98%93%E4%BF%A1%E6%81%AF&IsShow=1'.format(i['guid'])
                else:
                    url = self.code[1].format(i['guid'])
                date_Today = i['publish_StartTime'][:10]
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
                    self.code = self.code_list.pop(0)
                    page = 0
                    break
            if page == 20:
                self.code = self.code_list.pop(0)
                page = 0

    def parse_detile(self, title, url, date):
        print(url)
        url_html = etree.HTML(tool.requests_get(url, self.headers))
        try:
            detail = url_html.xpath('//*[@id="form1"]/div[5]/div[4]')[0]
            detail_html = etree.tostring(detail, method='HTML')
            detail_html = html.unescape(detail_html.decode())
            detail_text = url_html.xpath('string(//*[@id="form1"]/div[5]/div[4])').replace('\xa0', '').replace('\n',
                                                                                                               ''). \
                replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
            if len(detail_text) < 10:
                int('a')
        except:
            try:
                detail = url_html.xpath('//*[@id="form1"]/div[6]/div[4]/table[1]')[0]
                detail_html = etree.tostring(detail, method='HTML')
                detail_html = html.unescape(detail_html.decode())
                detail_text = url_html.xpath('string(//*[@id="form1"]/div[6]/div[4]/table[1])').replace('\xa0', '').replace('\n',
                                                                                                                   ''). \
                    replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
                if len(detail_text) < 10:
                    int('a')
            except:
                try:
                    detail = url_html.xpath('//*[@id="ctl00_Content_GridView1"]')[0]
                    detail_html = etree.tostring(detail, method='HTML')
                    detail_html = html.unescape(detail_html.decode())
                    detail_text = url_html.xpath('string(//*[@id="ctl00_Content_GridView1"])').replace('\xa0',
                                                                                                            '').replace(
                        '\n',
                        ''). \
                        replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
                    if len(detail_text) < 10:
                        int('a')
                except:
                    detail = url_html.xpath('//*[@class="xx_content2"]')[0]
                    detail_html = etree.tostring(detail, method='HTML')
                    detail_html = html.unescape(detail_html.decode())
                    detail_text = url_html.xpath('string(//*[@class="xx_content2"])').replace('\xa0',
                                                                                                       '').replace(
                        '\n',
                        ''). \
                        replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
        # print(detail_html.replace('\xa0','').replace('\xa5',''))
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
        item['resource'] = '昆明市公共资源交易平台'
        item['shi'] = 13001
        item['sheng'] = 13000
        item['removal']= title
        process_item(item)
    def get_nativeplace(self, addr):
        city = ''
        city_list = [['13001.001', '五华区'], ['13001.01', '石林彝族自治县'], ['13001.011', '嵩明县'], ['13001.012', '禄劝彝族苗族自治县'], ['13001.013', '寻甸回族彝族自治县'], ['13001.014', '安宁'], ['13001.002', '盘龙区'], ['13001.003', '官渡区'], ['13001.004', '西山区'], ['13001.005', '东川区'], ['13001.006', '呈贡县'], ['13001.007', '晋宁县'], ['13001.008', '富民县'], ['13001.009', '宜良县']]

        for i in city_list:
            if i[1] in addr:
                city = float(i[0])
                break
        if city == '':
            city = 13001
        return city

if __name__ == '__main__':

    import traceback, os
    try:
        jl = kunming_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
        # traceback.print_exc()
        tool.send_error('报错文件：'+str(os.path.basename(__file__))+'报错信息：'+str(e))


