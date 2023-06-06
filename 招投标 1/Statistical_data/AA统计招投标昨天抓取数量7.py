# -*- coding: utf-8 -*-
import base64, pytesseract
from PIL import Image
import time, json, re, requests
from lxml.etree import HTML
from tool import tool
from selenium import webdriver

class spider:
    def __init__(self):
        self.tool = tool()
        self.date = tool.date
        self.url_lss = [
            [self.sanming,'http://ggzyjyzx.shandong.gov.cn'],
            [self.linxi, 'http://www.ccgp-shandong.gov.cn'],
            [self.leshan, 'http://prec.sxzwfw.gov.cn'],
            [self.yunan, 'http://www.ccgp-shanxi.gov.cn'],
            [self.neijiang, 'http://www.czgcjy.com'],
            [self.beijing, 'http://www.gdzkgc.com'],
            [self.beijingzf, 'http://www.gdbidding.com'],
            [self.nanjing, 'http://zbtb.gd.gov.cn'],
            [self.nanchong, 'http://ggzy.xjbt.gov.cn'],
            [self.nanping, 'http://www.ccgp-xinjiang.gov.cn'],
            [self.nanchang, 'http://218.92.104.98:18080'],
            # [self.nantong, 'https://www.hzctc.cn'],  反应太慢
            [self.jian, 'http://czj.hangzhou.gov.cn'],
            [self.jilin, 'https://zbcg.jchc.cn'],
            # [self.jilinzf, 'http://www.jszb.com.cn'], 打不开
            [self.jiayuguan, 'http://218.90.220.218'],
            [self.sichuan, 'http://www.jnjianzhao.com'],
            [self.weihai, 'http://new.zmctc.com'],
            # [self.anhui, 'http://www.zjbid.cn'], 打不开
            [self.yichun, 'http://zfcgmanager.czt.zj.gov.cn'],
            [self.suqian, 'http://www.xsggzy.org.cn'],
            [self.bazhong, 'https://cgpt.sotcbb.com'],
            # # [self.changzhou, 'http://wsbs.gdqy.gov.cn'], 打不开
            [self.guangdong, 'http://ggzy.hunan.gov.cn'],
            [self.guangdongzf, 'http://www.ccgp-hunan.gov.cn'],
            [self.guangyuan, 'https://222.243.150.64:50680'],
            [self.guangan, 'http://www.ccgp-gansu.gov.cn'],
            [self.qingyang, 'http://ygjy.ggzyjy.gansu.gov.cn:3040'],
            [self.zhangye, 'http://ggzy.jlbc.gov.cn'],
            [self.dezhou, 'https://www.tcsggzyjyw.com'],
            [self.chengdu, 'http://dhggzy.dinghai.gov.cn'],
            [self.yangzhou, 'http://www.mudan.gov.cn'],
            [self.panzhihua, 'http://ggzy.hengyang.gov.cn'],
            [self.xinyu, 'https://www.chengezhao.com'],
            [self.wuxi, 'http://www.lnggzy.gov.cn'],
            [self.rizhao, 'http://ccgp-liaoning.gov.cn'],
            [self.zaozhuang, 'https://www.cqggzy.com'],
            [self.jiangsu, 'https://www.ccgp-chongqing.gov.cn'],
            [self.jiangxi, 'https://qjyzx.cqstl.gov.cn'],
            [self.taizhou, 'http://www.ycsggzy.cn'],
            [self.jining, 'http://www.ccgp-shaanxi.gov.cn'],
            [self.hubei, 'http://www.xaprtc.com'],
            [self.binzhou, 'http://www.qhggzyjy.gov.cn'],
            # [self.zhangzhou, 'http://hljggzyjyw.gov.cn'], 反应太慢
            [self.weifang, 'http://www.hljcg.gov.cn']
        ]

    # 山东省公共资源网
    def sanming(self):
        print('山东省公共资源网', 'http://ggzyjyzx.shandong.gov.cn')
        url_list = [
            'http://ggzyjyzx.shandong.gov.cn/col/col110306/index.html?uid=428723&pageNum={}',
            'http://ggzyjyzx.shandong.gov.cn/col/col110307/index.html?uid=428723&pageNum={}',
            'http://ggzyjyzx.shandong.gov.cn/col/col188376/index.html?uid=428723&pageNum={}',
            'http://ggzyjyzx.shandong.gov.cn/col/col110317/index.html?uid=314166&pageNum={}',
            'http://ggzyjyzx.shandong.gov.cn/col/col110318/index.html?uid=314166&pageNum={}'
        ]
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        }
        url = url_list.pop(0)
        page = 0
        ls = []
        while True:
            page += 1
            text = tool.requests_get(url.format(page), headers)
            detail = re.findall('<li class="ewb-list-node clearfix">.*?</li>', text, re.S)
            for li in detail:
                li_ = HTML(li)
                title = li_.xpath('//li/a/@title')[0].replace('\n', '').replace(' ', '')
                date_Today = li_.xpath('//li/span/text()')[0]
                url_ = li_.xpath('//li/a/@href')[0]
                if 'http' not in url_:
                    url_ = 'http://ggzyjyzx.shandong.gov.cn' +url_
                if '测试' in title:
                    continue
                if tool.Transformation(date_Today) > tool.Transformation(self.date):
                    continue
                elif tool.Transformation(date_Today) == tool.Transformation(self.date):
                    ls.append(url_)
                else:
                    if len(url_list) == 0:
                        return [len(ls), ls]
                    else:
                        url = url_list.pop(0)
                        page = 0
                        break

    # 山东省政府采购网
    def linxi(self):
        print('山东省政府采购网', 'http://www.ccgp-shandong.gov.cn')
        url_list = [
            ['0301', '2102', '0305', '0302', '0306'],
            ['0303', '2106', '0305', '0304', '0306']
        ]
        headers = {
            'Cookie': '_gscu_859717865=06285138rbcv4w59; AlteonP=AEcBbaXdHKxJXyA/5FhJEg$$; SsoCookierYzm=sjsv; wondersLog_zwdt_G_D_I=ee498f7112ef1975b078204349ec1b5b-2926; wondersLog_zwdt_sdk=%7B%22persistedTime%22%3A1614147940531%2C%22userId%22%3A%22%22%2C%22superProperties%22%3A%7B%22userType%22%3A2%7D%2C%22updatedTime%22%3A1614147941215%2C%22sessionStartTime%22%3A1614147941210%2C%22sessionReferrer%22%3A%22http%3A%2F%2Fgcls.sh.gov.cn%2F%22%2C%22deviceId%22%3A%22ee498f7112ef1975b078204349ec1b5b-2926%22%2C%22LASTEVENT%22%3A%7B%22eventId%22%3A%22wondersLog_pv%22%2C%22time%22%3A1614147941213%7D%2C%22sessionUuid%22%3A7948921178336179%2C%22costTime%22%3A%7B%7D%7D',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
        }
        grade = 'province'
        i = url_list.pop(0)
        url = i.pop(0)
        page = 0
        ls = []
        url_to = 'http://www.ccgp-shandong.gov.cn/sdgp2017/site/listnew.jsp'
        while True:
            page += 1
            data = '?subject=&pdate=&kindof=&areacode=&unitname=&projectname=&projectcode=&colcode={}&curpage={}&grade={}&firstpage=1'
            text = tool.requests_get(url_to+data.format(url, page, grade), headers)
            detail = HTML(text).xpath('//*[@id="preform"]/div[1]/div[3]/div[2]/div[1]/ul/li')
            for li in detail:
                title = li.xpath('./span/span[1]/a/@title')[0]
                try:
                    date_Today = li.xpath('./span[2]/text()')[0].replace('\xa0', '').replace('\n', '')
                except:
                    date_Today = li.xpath('./span/span[2]/text()')[0].replace('\xa0', '').replace('\n', '')
                url_ = li.xpath('./span/span[1]/a/@href')[0]
                if 'http' not in url_:
                    url_ = 'http://www.ccgp-shandong.gov.cn' + url_
                if '测试' in title:
                    continue
                if tool.Transformation(date_Today) > tool.Transformation(self.date):
                    continue
                elif tool.Transformation(date_Today) == tool.Transformation(self.date):
                    ls.append(url_)
                else:
                    if len(url_list) == 0 and len(i) == 0:
                        return [len(ls), ls]
                    else:
                        if len(i) == 0:
                            i = url_list.pop(0)
                            url = i.pop(0)
                            page = 0
                            grade = 'city'
                            break
                        url = i.pop(0)
                        page = 0
                        break

    # 山西公共资源
    def leshan(self):
        print('山西公共资源', 'http://prec.sxzwfw.gov.cn')
        url_list = ['http://prec.sxzwfw.gov.cn/jyxx/index_{}.jhtml',
                         'http://prec.sxzwfw.gov.cn/jyxxzc/index_{}.jhtml']
        headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Cookie': 'JSESSIONID=662863FD2199FBD1672A04A290868047; _CSRFCOOKIE=73F3D7A1BCDCA9001D7B1483A214C4E98DE2528B; EPTOKEN=73F3D7A1BCDCA9001D7B1483A214C4E98DE2528B; oauthClientId=demoClient; oauthPath=http://172.16.5.21:8080/EpointWebBuilder; oauthLoginUrl=http://172.16.5.21:8080/EpointWebBuilder/rest/oauth2/authorize?client_id=demoClient&state=a&response_type=code&scope=user&redirect_uri=; oauthLogoutUrl=http://172.16.5.21:8080/EpointWebBuilder/rest/oauth2/logout?redirect_uri=; noOauthRefreshToken=986d4fe7e5dd29b64c9e7b7a6d66e089; noOauthAccessToken=77c09e0bf98b6220b544961097eed84a; sub_domain_cokie=TiG5CMD9KQ41mmsARPTuAg%3D%3D; region_name=%E4%B9%8C%E9%B2%81%E6%9C%A8%E9%BD%90%E5%B8%82',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',

        }
        url = url_list.pop(0)
        ls = []
        page = 0
        while True:
            page += 1
            text = tool.requests_get(url.format(page), headers)
            detail = HTML(text).xpath('/html/body/div[2]/div/div[2]/div/div[4]/div[1]/a')
            for li in detail:
                url_ = li.xpath('./@href')[0]
                title = li.xpath('./p[1]/text()')[0].replace('\n', '').replace('\r', '').replace('\t', '').replace(' ',
                                                                                                                   '')
                date_Today = li.xpath('./p[2]/span[2]/text()')[0].replace('[',
                                                                          '').replace(
                    ']', '').replace('/', '-')
                if '测试' in title:
                    continue
                if tool.Transformation(date_Today) > tool.Transformation(self.date):
                    continue
                elif tool.Transformation(date_Today) == tool.Transformation(self.date):
                    ls.append(url_)
                else:
                    if len(url_list) == 0:
                        return [len(ls), ls]
                    else:
                        url = url_list.pop(0)
                        page = 0
                        break

    # 山西政府采购
    def yunan(self):
        print('山西政府采购', 'http://www.ccgp-shanxi.gov.cn')
        url_list = ['100', '104', '105', '116', '131', '153']
        headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Cookie': 'JSESSIONID=662863FD2199FBD1672A04A290868047; _CSRFCOOKIE=73F3D7A1BCDCA9001D7B1483A214C4E98DE2528B; EPTOKEN=73F3D7A1BCDCA9001D7B1483A214C4E98DE2528B; oauthClientId=demoClient; oauthPath=http://172.16.5.21:8080/EpointWebBuilder; oauthLoginUrl=http://172.16.5.21:8080/EpointWebBuilder/rest/oauth2/authorize?client_id=demoClient&state=a&response_type=code&scope=user&redirect_uri=; oauthLogoutUrl=http://172.16.5.21:8080/EpointWebBuilder/rest/oauth2/logout?redirect_uri=; noOauthRefreshToken=986d4fe7e5dd29b64c9e7b7a6d66e089; noOauthAccessToken=77c09e0bf98b6220b544961097eed84a; sub_domain_cokie=TiG5CMD9KQ41mmsARPTuAg%3D%3D; region_name=%E4%B9%8C%E9%B2%81%E6%9C%A8%E9%BD%90%E5%B8%82',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        }
        url = url_list.pop(0)
        page = 0
        ls = []
        url_to = 'http://www.ccgp-shanxi.gov.cn/view.php?app=&type=&nav={}&page={}'
        while True:
            page += 1
            text = tool.requests_get(url_to.format(url, page), headers)
            detail = HTML(text).xpath('//*[@id="node_list"]/tbody/tr')
            for li in detail:
                url_ = 'http://www.ccgp-shanxi.gov.cn/' + li.xpath('./td[1]/a/@href')[0]
                title = li.xpath('./td[1]/a/@title')[0]
                try:
                    date_Today = li.xpath('./td[4]/text()')[0].replace('[',
                                                                       '').replace(
                        ']', '')
                except:
                    date_Today = li.xpath('./td[3]/text()')[0].replace('[',
                                                                       '').replace(
                        ']', '')
                if '测试' in title:
                    continue
                if tool.Transformation(date_Today) > tool.Transformation(self.date):
                    continue
                elif tool.Transformation(date_Today) == tool.Transformation(self.date):
                    ls.append(url_)
                else:
                    if len(url_list) == 0:
                        return [len(ls), ls]
                    else:
                        url = url_list.pop(0)
                        page = 0
                        break

    # 常州市工程交易网
    def neijiang(self):
        print('常州市工程交易网', 'http://www.czgcjy.com')
        url_list = [
            'http://www.czgcjy.com/czztb/jyxx/010001/',
            'http://www.czgcjy.com/czztb/jyxx/010002/'
        ]
        headers = {
            'Cookie': 'homeid=1a444a31-e460-47ff-9931-1c075c0f3cd8',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        }
        url = url_list.pop(0)
        page = 0
        ls = []
        while True:
            page += 1
            text = tool.requests_get(url, headers)
            detail = HTML(text).xpath('/html/body/table/tr[2]/td/table/tr/td/table/tr/td[4]/table[2]/tr/td/table/tr')
            for li in detail:
                for tr in li.xpath('./td/table/tr[2]/td[2]/table/tr'):
                    title = tr.xpath('./td[2]/a/text()')[0]
                    url_ = 'http://www.czgcjy.com' + tr.xpath('./td[2]/a/@href')[0]
                    date_Today = tr.xpath('./td[3]/font/text()')[0].replace('(', '').replace(')', '')
                    if '测试' in title:
                        continue
                    if tool.Transformation(date_Today) > tool.Transformation(self.date):
                        continue
                    elif tool.Transformation(date_Today) == tool.Transformation(self.date):
                        ls.append(url_)
                    else:
                        if len(url_list) == 0:
                            return [len(ls), ls]
                        else:
                            url = url_list.pop(0)
                            page = 0
                            break

    # 广东中凯工程管理咨询有限公司
    def beijing(self):
        print('广东中凯工程管理咨询有限公司', 'http://www.gdzkgc.com')
        url_list = [
           'http://www.gdzkgc.com/plus/list.php?tid=4&TotalResult=1192&PageNo={}'
        ]
        headers = {
            'Cookie': 'homeid=1a444a31-e460-47ff-9931-1c075c0f3cd8',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        }
        url = url_list.pop(0)
        page = 0
        ls = []
        while True:
            page += 1
            text = tool.requests_get(url.format(page), headers)
            html = HTML(text)
            detail = html.xpath('//*[@id="content1"]/div[1]/ul/li')
            for li in detail:
                title = li.xpath('./a/text()')[0].replace('\xa0', '').replace(' ', '')
                url_ = 'http://www.gdzkgc.com' + \
                      li.xpath('./a/@href')[0]
                date_Today = li.xpath('./span/text()')[0].replace('\r', '').replace(' ', '').replace('\n', '').replace(
                    '\t', '').replace('发布时间：', '')
                if '测试' in title:
                    continue
                if tool.Transformation(date_Today) > tool.Transformation(self.date):
                    continue
                elif tool.Transformation(date_Today) == tool.Transformation(self.date):
                    ls.append(url_)
                else:
                    if len(url_list) == 0:
                        return [len(ls), ls]
                    else:
                        url = url_list.pop(0)
                        page = 0
                        break

    # 广东元正招标采购有限公司 需要线上修改
    def beijingzf(self):
        print('广东元正招标采购有限公司', 'http://www.gdbidding.com')
        url_list = [
            # 招标公告
            'http://120.78.91.121:3100/v1/public/findZbxxListById?limit=20&offset={}&id=1&beginDate={}&endDate={}&currentPage={}',
            # 中标公告
            'http://120.78.91.121:3100/v1/public/findZbxxListById?limit=20&offset={}&id=4&beginDate={}&endDate={}&currentPage={}',
            # 中标预告
            'http://120.78.91.121:3100/v1/public/findZbxxListById?limit=20&offset={}&id=2&beginDate={}&endDate={}&currentPage={}'
        ]
        headers = {
            'Accept': 'application/json, text/plain, */*',
            # 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Cookie': 'ASP.NET_SessionId=35z2fvq5lvv2beeme22crjin; __CSRFCOOKIE=b36f48c6-fa2d-4882-bd90-6012bef4acb3',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',

        }
        url = url_list.pop(0)
        page = 0
        ls = []
        date_to = tool.date
        while True:
            page += 1
            text = tool.requests_get(url.format((page - 1) * 20, self.date, date_to, page), headers)
            detail = json.loads(text)['data']['list']
            if len(detail) == 0:
                print('今日暂时没有招标...')
                if len(url_list) == 0:
                    return [len(ls), ls]
                url = url_list.pop(0)
                page = 0
                continue

            for li in detail:
                title = li['sys_title'].replace('\xa0', '').replace(' ', '')
                url_ = 'http://www.gdbidding.com/zbxxDetail?id=' + \
                      str(li['id'])
                try:
                    date_Today = tool.Time_stamp_to_date(tool.Transformation(li['cdate'][:10]) + 86400)
                except:
                    date_Today = tool.Time_stamp_to_date(tool.Transformation(li['sys_idate'][:10]) + 86400)
                if '测试' in title:
                    continue
                if tool.Transformation(date_Today) > tool.Transformation(self.date):
                    continue
                elif tool.Transformation(date_Today) == tool.Transformation(self.date):
                    ls.append(url_)
                else:
                    if len(url_list) == 0:
                        return [len(ls), ls]
                    else:
                        url = url_list.pop(0)
                        page = 0
                        break

    # 广东省招标投标监管网    需要线上修改
    def nanjing(self):
        print('广东省招标投标监管网', 'http://zbtb.gd.gov.cn')
        url_list = [
            'http://zbtb.gd.gov.cn/bid/listZbgcxx?createDate=1&draw=1&columns%5B0%5D%5Bdata%5D=id&columns%5B0%5D%5Bname%5D=&columns%5B0%5D%5Bsearchable%5D=true&columns%5B0%5D%5Borderable%5D=false&columns%5B0%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B0%5D%5Bsearch%5D%5Bregex%5D=false&start=0&length=20&search%5Bvalue%5D=&search%5Bregex%5D=false&page={}&type=&xmmc=&rows=20',
            'http://zbtb.gd.gov.cn/bid/listZbhxrgs?draw=1&columns%5B0%5D%5Bdata%5D=id&columns%5B0%5D%5Bname%5D=&columns%5B0%5D%5Bsearchable%5D=true&columns%5B0%5D%5Borderable%5D=false&columns%5B0%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B0%5D%5Bsearch%5D%5Bregex%5D=false&start=0&length=20&search%5Bvalue%5D=&search%5Bregex%5D=false&page={}&type=zbhxrgs&xmmc=&rows=20'
        ]
        headers = {
            'Cookie': 'Hm_lvt_ae3702a0997d560bba5902699c6cf1cc=1614046447; _d_id=7fea23cc84484839c41aab727f0371; Hm_lpvt_ae3702a0997d560bba5902699c6cf1cc=1614046525',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
        }
        url = url_list.pop(0)
        ls = []
        page = 0
        while True:
            page += 1
            text = tool.requests_get(url.format(page), headers)
            detail = json.loads(text)['data']
            for li in detail:
                title = li['title']
                url_ = 'http://zbtb.gd.gov.cn/platform/attach/getAttachList?parentId={}&parentType=GGNR&rows=999999&page=1'.format(
                    str(li['id']))
                date_Today = li['publishdate']
                if '测试' in title:
                    continue
                if tool.Transformation(date_Today) > tool.Transformation(self.date):
                    continue
                elif tool.Transformation(date_Today) == tool.Transformation(self.date):
                    ls.append(url_)
                    continue
                else:
                    if len(url_list) == 0:
                        return [len(ls), ls]
                    else:
                        url = url_list.pop(0)
                        page = 0
                        break

    # 新疆公共资源    浏览器 线上已修改
    def nanchong(self):
        print('新疆公共资源', 'http://ggzy.xjbt.gov.cn')
        url_list = ["004001/004001002/", "004001/004001003/", "004001/004001004/", "004001/004001005/", "004002/004002002/", "004002/004002003/",
                     "004002/004002004/", "004002/004002005/", "004002/004002007/"]
        headers = {
            'Cookie': 'homeid=1a444a31-e460-47ff-9931-1c075c0f3cd8',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        }
        url = url_list.pop(0)
        page = 0
        ls = []
        url_to = 'http://ggzy.xjbt.gov.cn/TPFront/jyxx/{}?Paging={}'
        while True:
            page += 1
            text = tool.selenium_get_to(url_to.format(url, page))
            detail = HTML(text).xpath('//*[@class="top10"]/tbody/tr[2]/td/div/table/tbody/tr')
            for li in detail:
                try:
                    title = li.xpath('./td[2]/a/@title')[0]
                    url_ = "http://ggzy.xjbt.gov.cn" + li.xpath('./td[2]/a/@href')[0]
                    date_Today = li.xpath('./td[3]/text()')[0].replace('[', '').replace(']', '')
                except:
                    continue
                if '测试' in title:
                    continue
                if tool.Transformation(date_Today) > tool.Transformation(self.date):
                    continue
                elif tool.Transformation(date_Today) == tool.Transformation(self.date):
                    ls.append(url_)
                else:
                    if len(url_list) == 0:
                        return [len(ls), ls]
                    else:
                        url = url_list.pop(0)
                        page = 0
                        break

    # 新疆政府采购
    def nanping(self):
        print('新疆政府采购', 'http://www.ccgp-xinjiang.gov.cn')
        url_list = ["ZcyAnnouncement1", "ZcyAnnouncement2", "ZcyAnnouncement4", "ZcyAnnouncement5", "ZcyAnnouncement3",
                               "ZcyAnnouncement10", "ZcyAnnouncement8"]
        headers = {
            'Cookie': 'zh_choose=n; _gscu_375154715=78462920k1peom21; _trs_uv=k54w2gs3_2380_dkza; pgv_pvi=7955464192; pgv_si=s3740718080; _gscbrs_375154715=1; _trs_ua_s_1=k56fo9sc_2380_2pvf; _gscs_375154715=78556317ftoe7i21|pv:10',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
        }
        url = url_list.pop(0)
        page = 0
        ls = []
        url_to = 'http://www.ccgp-xinjiang.gov.cn/front/search/category'
        while True:
            page += 1
            data = {"pageNo": page, "pageSize": 15, "categoryCode": "{}".format(url)}
            text = tool.requests_post_to(url_to, data, headers)
            detail = json.loads(text)["hits"]["hits"]
            for li in detail:
                url_ = 'http://www.ccgp-xinjiang.gov.cn' + li['_source']['url']
                date_Today = time.strftime("%Y-%m-%d", time.localtime(int(str(li["_source"]["publishDate"])[:-3])))
                title = li['_source']['title']
                if '测试' in title:
                    continue
                if tool.Transformation(date_Today) > tool.Transformation(self.date):
                    continue
                elif tool.Transformation(date_Today) == tool.Transformation(self.date):
                    ls.append(url_)
                else:
                    if len(url_list) == 0:
                        return [len(ls), ls]
                    else:
                        url = url_list.pop(0)
                        page = 0
                        break

    # 方洲集团电子采购平台
    def nanchang(self):
        print('方洲集团电子采购平台', 'http://218.92.104.98:18080')
        url_list = [
            'http://218.92.104.98:18080/jyxx/001001/{}.html',
            'http://218.92.104.98:18080/jyxx/001002/{}.html'
        ]
        headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Cookie': 'JSESSIONID=662863FD2199FBD1672A04A290868047; _CSRFCOOKIE=73F3D7A1BCDCA9001D7B1483A214C4E98DE2528B; EPTOKEN=73F3D7A1BCDCA9001D7B1483A214C4E98DE2528B; oauthClientId=demoClient; oauthPath=http://172.16.5.21:8080/EpointWebBuilder; oauthLoginUrl=http://172.16.5.21:8080/EpointWebBuilder/rest/oauth2/authorize?client_id=demoClient&state=a&response_type=code&scope=user&redirect_uri=; oauthLogoutUrl=http://172.16.5.21:8080/EpointWebBuilder/rest/oauth2/logout?redirect_uri=; noOauthRefreshToken=986d4fe7e5dd29b64c9e7b7a6d66e089; noOauthAccessToken=77c09e0bf98b6220b544961097eed84a; sub_domain_cokie=TiG5CMD9KQ41mmsARPTuAg%3D%3D; region_name=%E4%B9%8C%E9%B2%81%E6%9C%A8%E9%BD%90%E5%B8%82',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',

        }
        url = url_list.pop(0)
        page = 0
        ls = []
        while True:
            page += 1
            if page == 1:
                if '001002' in url:
                    text = tool.requests_get(url.format('list'), headers)
                else:
                    text = tool.requests_get(url.format('listcggg'), headers)
            else:
                text = tool.requests_get(url.format(page), headers)
            html = HTML(text)
            detail = html.xpath('//*[@id="list"]/li')
            for li in detail:
                title = li.xpath('./a/@title')[0].replace('\xa0', '').replace(' ', '')
                url_ = 'http://218.92.104.98:18080' + \
                      li.xpath('./a/@href')[0]
                date_Today = li.xpath('./span/text()')[0].replace('\r', '').replace(' ', '').replace('\n', '').replace(
                    '\t', '').replace('发布时间：', '')
                if '测试' in title:
                    continue
                if tool.Transformation(date_Today) > tool.Transformation(self.date):
                    continue
                elif tool.Transformation(date_Today) == tool.Transformation(self.date):
                    ls.append(url_)
                else:
                    if len(url_list) == 0:
                        return [len(ls), ls]
                    else:
                        url = url_list.pop(0)
                        page = 0
                        break

    # 杭州市公共资源网  反应太慢
    def nantong(self):
        print('杭州市公共资源网', 'https://www.hzctc.cn')
        url_list = ['22', '23', '465', '486', '25', '28', '27', '29', '32', '34', '499', '37']
        headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Cookie': 'JSESSIONID=662863FD2199FBD1672A04A290868047; _CSRFCOOKIE=73F3D7A1BCDCA9001D7B1483A214C4E98DE2528B; EPTOKEN=73F3D7A1BCDCA9001D7B1483A214C4E98DE2528B; oauthClientId=demoClient; oauthPath=http://172.16.5.21:8080/EpointWebBuilder; oauthLoginUrl=http://172.16.5.21:8080/EpointWebBuilder/rest/oauth2/authorize?client_id=demoClient&state=a&response_type=code&scope=user&redirect_uri=; oauthLogoutUrl=http://172.16.5.21:8080/EpointWebBuilder/rest/oauth2/logout?redirect_uri=; noOauthRefreshToken=986d4fe7e5dd29b64c9e7b7a6d66e089; noOauthAccessToken=77c09e0bf98b6220b544961097eed84a; sub_domain_cokie=TiG5CMD9KQ41mmsARPTuAg%3D%3D; region_name=%E4%B9%8C%E9%B2%81%E6%9C%A8%E9%BD%90%E5%B8%82',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        }
        url = url_list.pop(0)
        page = 0
        ls = []
        data = {
            'area': '',
            'afficheType': '',
            'IsToday': '',
            'title': '',
            'proID': '',
            'number': '',
            '_search': 'false',
            'nd': '1573459629871',
            'rows': '10',
            'page': '1',
            'sidx': 'PublishStartTime',
            'sord': 'desc'
        }
        url_to = 'https://www.hzctc.cn/SecondPage/GetNotice'
        while True:
            page += 1
            data['afficheType'] = url
            data['page'] = str(page)
            text = tool.requests_post(url_to, data, headers)
            detail = json.loads(text)['rows']
            for tr in detail:
                if url == '486':
                    url_ = "https://www.hzctc.cn/OpenBidRecord/Index?id={}&tenderID={}&ModuleID={}".format(tr['ID'], tr[
                        'TenderID'], url)
                    title = tr['TenderName']
                    date_Today = tr['PublishStartTime'][:10]
                elif url == '465':
                    url_ = "https://www.hzctc.cn/NewsShow/Home?id={}&ModuleID={}&AreadID=80".format(tr['id'], url)
                    title = tr['title']
                    date_Today = tr['news_entertime'][:10]
                else:
                    url_ = "https://www.hzctc.cn/AfficheShow/Home?AfficheID={}&IsInner=3&ModuleID={}".format(tr['ID'],
                                                                                                            url)
                    title = tr['TenderName']
                    date_Today = tr['PublishStartTime'][:10]
                if '测试' in title:
                    continue
                if tool.Transformation(date_Today) > tool.Transformation(self.date):
                    continue
                elif tool.Transformation(date_Today) == tool.Transformation(self.date):
                    ls.append(url_)
                else:
                    if len(url_list) == 0:
                        return [len(ls), ls]
                    else:
                        url = url_list.pop(0)
                        page = 0
                        break

    # 杭州市财政局
    def jian(self):
        print('杭州市财政局', 'http://zfcgmanager.czt.zj.gov.cn')
        url_list = ['http://czj.hangzhou.gov.cn/col/col1677825/index.html',
               'http://czj.hangzhou.gov.cn/col/col1677826/index.html',
               'http://czj.hangzhou.gov.cn/col/col1677827/index.html',#征询意见
               'http://czj.hangzhou.gov.cn/col/col1677829/index.html',
               'http://czj.hangzhou.gov.cn/col/col1677830/index.html',
               'http://czj.hangzhou.gov.cn/col/col1677833/index.html',
               'http://czj.hangzhou.gov.cn/col/col1677842/index.html',
               'http://czj.hangzhou.gov.cn/col/col1677843/index.html']
        headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Cookie': 'JSESSIONID=662863FD2199FBD1672A04A290868047; _CSRFCOOKIE=73F3D7A1BCDCA9001D7B1483A214C4E98DE2528B; EPTOKEN=73F3D7A1BCDCA9001D7B1483A214C4E98DE2528B; oauthClientId=demoClient; oauthPath=http://172.16.5.21:8080/EpointWebBuilder; oauthLoginUrl=http://172.16.5.21:8080/EpointWebBuilder/rest/oauth2/authorize?client_id=demoClient&state=a&response_type=code&scope=user&redirect_uri=; oauthLogoutUrl=http://172.16.5.21:8080/EpointWebBuilder/rest/oauth2/logout?redirect_uri=; noOauthRefreshToken=986d4fe7e5dd29b64c9e7b7a6d66e089; noOauthAccessToken=77c09e0bf98b6220b544961097eed84a; sub_domain_cokie=TiG5CMD9KQ41mmsARPTuAg%3D%3D; region_name=%E4%B9%8C%E9%B2%81%E6%9C%A8%E9%BD%90%E5%B8%82',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',

        }
        url = url_list.pop(0)
        page = 0
        ls = []
        while True:
            page += 1
            text = tool.requests_get(url, headers)
            detail = re.findall(
                '''<a href="(.*?)" title="(.*?)">.*?</a>		<span class="time">(.*?)</span>	</li>''', text)
            if len(detail) == 0:
                int('a')
            for tr in detail:
                title = tr[1]
                date_Today = tr[2]
                url_ = 'http://zfcgmanager.czt.zj.gov.cn/cms/api/cors/remote/results?noticeId={}&url=noticeDetail'.format(
                    tr[0].split('=')[1])
                if '测试' in title:
                    continue
                if tool.Transformation(date_Today) > tool.Transformation(self.date):
                    continue
                elif tool.Transformation(date_Today) == tool.Transformation(self.date):
                    ls.append(url_)
                else:
                    if len(url_list) == 0:
                        return [len(ls), ls]
                    else:
                        url = url_list.pop(0)
                        page = 0
                        break

    # 江苏交通控股有限公司招标与采购网
    def jilin(self):
        print('江苏交通控股有限公司招标与采购网', 'https://zbcg.jchc.cn')
        url_list = [
            'https://zbcg.jchc.cn/api/announce/notice/announcementUnionList?_t=1614651033&noticeType=1&pageSize=10&pageNo={}&noticeName=&companyCode=&projectType=&purchasingMethod=&type=',
            'https://zbcg.jchc.cn/api/announce/notice/announcementUnionList?_t=1614651089&noticeType=1&noticeName=&companyCode=&projectType=&purchasingMethod=&type=2',
            'https://zbcg.jchc.cn/api/announce/notice/announcementList?_t=1614651168&pageSize=10&pageNo={}&noticeType=2&noticeName=&companyCode=&projectType=&purchasingMethod=&type=',
            'https://zbcg.jchc.cn/api/announce/notice/announcementList?_t=1614651197&pageSize=10&pageNo={}&noticeType=3&noticeName=&companyCode=&projectType=&purchasingMethod=&type=',
            'https://zbcg.jchc.cn/api/announce/notice/announcementUnionList?_t=1614651221&pageSize=10&pageNo={}&noticeType=5&noticeName=&companyCode=&projectType=&purchasingMethod=&type='
        ]
        headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Cookie': 'JSESSIONID=662863FD2199FBD1672A04A290868047; _CSRFCOOKIE=73F3D7A1BCDCA9001D7B1483A214C4E98DE2528B; EPTOKEN=73F3D7A1BCDCA9001D7B1483A214C4E98DE2528B; oauthClientId=demoClient; oauthPath=http://172.16.5.21:8080/EpointWebBuilder; oauthLoginUrl=http://172.16.5.21:8080/EpointWebBuilder/rest/oauth2/authorize?client_id=demoClient&state=a&response_type=code&scope=user&redirect_uri=; oauthLogoutUrl=http://172.16.5.21:8080/EpointWebBuilder/rest/oauth2/logout?redirect_uri=; noOauthRefreshToken=986d4fe7e5dd29b64c9e7b7a6d66e089; noOauthAccessToken=77c09e0bf98b6220b544961097eed84a; sub_domain_cokie=TiG5CMD9KQ41mmsARPTuAg%3D%3D; region_name=%E4%B9%8C%E9%B2%81%E6%9C%A8%E9%BD%90%E5%B8%82',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',

        }
        url = url_list.pop(0)
        page = 0
        ls = []
        while True:
            page += 1
            if 'pageNo' in url:
                text = tool.requests_get(url.format(page), headers)
            else:
                text = tool.requests_get(url, headers)
            detail = json.loads(text)['result']['records']
            for li in detail:
                try:
                    title = li['projectName']
                    url_ = 'https://zbcg.jchc.cn/project_exceptioModel?projectId={}'.format(li['id'])
                    date_Today = li['publishTime'][:10].replace('\n', '').replace('\t', '').replace('\r',
                                                                                                    '').replace(
                        ' ', '')
                except:
                    title = li['noticeName']
                    url_ = 'https://zbcg.jchc.cn/notice_detailsModel?noticeId={}'.format(li['noticeId'])
                    date_Today = li['releaseDate'][:10].replace('\n', '').replace('\t', '').replace('\r',
                                                                                                    '').replace(
                        ' ', '')
                if '测试' in title:
                    continue
                if tool.Transformation(date_Today) > tool.Transformation(self.date):
                    continue
                elif tool.Transformation(date_Today) == tool.Transformation(self.date):
                    ls.append(url_)
                else:
                    if len(url_list) == 0:
                        return [len(ls), ls]
                    else:
                        url = url_list.pop(0)
                        page = 0
                        break

    # 江苏省建设工程招标网 
    def jilinzf(self):
        print('江苏省建设工程招标网', 'http://www.jszb.com.cn')
        url_list = [
            'http://www.jszb.com.cn/JSZB/YW_info/ZhaoBiaoGG/MoreInfo_ZBGG.aspx?categoryNum=012'
        ]
        headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Cookie': 'JSESSIONID=662863FD2199FBD1672A04A290868047; _CSRFCOOKIE=73F3D7A1BCDCA9001D7B1483A214C4E98DE2528B; EPTOKEN=73F3D7A1BCDCA9001D7B1483A214C4E98DE2528B; oauthClientId=demoClient; oauthPath=http://172.16.5.21:8080/EpointWebBuilder; oauthLoginUrl=http://172.16.5.21:8080/EpointWebBuilder/rest/oauth2/authorize?client_id=demoClient&state=a&response_type=code&scope=user&redirect_uri=; oauthLogoutUrl=http://172.16.5.21:8080/EpointWebBuilder/rest/oauth2/logout?redirect_uri=; noOauthRefreshToken=986d4fe7e5dd29b64c9e7b7a6d66e089; noOauthAccessToken=77c09e0bf98b6220b544961097eed84a; sub_domain_cokie=TiG5CMD9KQ41mmsARPTuAg%3D%3D; region_name=%E4%B9%8C%E9%B2%81%E6%9C%A8%E9%BD%90%E5%B8%82',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',

        }
        url = url_list.pop(0)
        page = 0
        ls = []
        data = {
            '__EVENTTARGET': 'MoreInfoList1$Pager',
            '__EVENTARGUMENT': '2',
            '__LASTFOCUS': '',
            '__VIEWSTATE': '',
            '__VIEWSTATEGENERATOR': '76D0A3AC',
            '__VIEWSTATEENCRYPTED': '',
            '__EVENTVALIDATION': '11',
            'MoreInfoList1$txtProjectName': '',
            'MoreInfoList1$txtBiaoDuanName': '',
            'MoreInfoList1$txtBiaoDuanNo': '',
            'MoreInfoList1$txtJSDW': '',
            'MoreInfoList1$StartDate': '',
            'MoreInfoList1$EndDate': '',
            'MoreInfoList1$jpdDi': '-1',
            'MoreInfoList1$jpdXian': '-1'
        }
        while True:
            page += 1
            if page == 1:
                text = tool.requests_get(url, headers)
            else:
                text = tool.requests_post(url, data, headers)
            html = HTML(text)
            data['__EVENTARGUMENT'] = str(page + 1)
            data['__VIEWSTATE'] = html.xpath('//*[@id = "__VIEWSTATE"]/@value')[0]
            data['__EVENTVALIDATION'] = html.xpath('//*[@id = "__EVENTVALIDATION"]/@value')[0]
            detail = html.xpath('//*[@id="MoreInfoList1_DataGrid1"]/tr')
            for li in detail:
                title = li.xpath('./td[2]/a/@title')[0]
                url_ = 'http://www.jszb.com.cn/JSZB/YW_info' + \
                      re.findall('"..(.*?)","",', li.xpath('./td[2]/a/@onclick')[0])[0]
                date_Today = li.xpath('./td[4]/text()')[0].replace('\n', '').replace('\t', '').replace('\r',
                                                                                                       '').replace(' ',
                                                                                                                   '')
                if '测试' in title:
                    continue
                if tool.Transformation(date_Today) > tool.Transformation(self.date):
                    continue
                elif tool.Transformation(date_Today) == tool.Transformation(self.date):
                    ls.append(url_)
                else:
                    if len(url_list) == 0:
                        return [len(ls), ls]
                    else:
                        url = url_list.pop(0)
                        page = 0
                        break

    # 泰州市公共资源交易平台-兴化站
    def jiayuguan(self):
        print('泰州市公共资源交易平台-兴化站', 'http://218.90.220.218')
        url_list = [
            'http://218.90.220.218/xhweb/jyxx/005001/005001001/MoreInfo.aspx?CategoryNum=005001001',
            'http://218.90.220.218/xhweb/jyxx/005001/005001004/MoreInfo.aspx?CategoryNum=005001004',
            'http://218.90.220.218/xhweb/jyxx/005001/005001008/MoreInfo.aspx?CategoryNum=005001008',
            'http://218.90.220.218/xhweb/jyxx/005002/005002001/MoreInfo.aspx?CategoryNum=005002001',
            'http://218.90.220.218/xhweb/jyxx/005002/005002002/MoreInfo.aspx?CategoryNum=005002002',
            'http://218.90.220.218/xhweb/jyxx/005002/005002003/MoreInfo.aspx?CategoryNum=005002003'
        ]
        headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Cookie': 'JSESSIONID=662863FD2199FBD1672A04A290868047; _CSRFCOOKIE=73F3D7A1BCDCA9001D7B1483A214C4E98DE2528B; EPTOKEN=73F3D7A1BCDCA9001D7B1483A214C4E98DE2528B; oauthClientId=demoClient; oauthPath=http://172.16.5.21:8080/EpointWebBuilder; oauthLoginUrl=http://172.16.5.21:8080/EpointWebBuilder/rest/oauth2/authorize?client_id=demoClient&state=a&response_type=code&scope=user&redirect_uri=; oauthLogoutUrl=http://172.16.5.21:8080/EpointWebBuilder/rest/oauth2/logout?redirect_uri=; noOauthRefreshToken=986d4fe7e5dd29b64c9e7b7a6d66e089; noOauthAccessToken=77c09e0bf98b6220b544961097eed84a; sub_domain_cokie=TiG5CMD9KQ41mmsARPTuAg%3D%3D; region_name=%E4%B9%8C%E9%B2%81%E6%9C%A8%E9%BD%90%E5%B8%82',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',

        }
        url = url_list.pop(0)
        ls = []
        data = {
            '__VIEWSTATE': '',
            '__VIEWSTATEGENERATOR': '4C01AA88',
            '__EVENTTARGET': 'MoreInfoList1$Pager',
            '__EVENTARGUMENT': '',
            '__VIEWSTATEENCRYPTED': ''
        }
        page = 0
        while True:
            page += 1
            if page == 1:
                text = tool.requests_get(url, headers)
            else:
                text = tool.requests_post(url, data, headers)
            html = HTML(text)
            data['__VIEWSTATE'] = html.xpath('//*[@id="__VIEWSTATE"]/@value')[0]
            data['__VIEWSTATEGENERATOR'] = html.xpath('//*[@id="__VIEWSTATEGENERATOR"]/@value')[0]
            data['__EVENTARGUMENT'] = page + 1
            detail = html.xpath('//*[@id="MoreInfoList1_DataGrid1"]/tr')
            for li in detail:
                title = li.xpath('./td[2]/a/@title')[0]
                url_ = 'http://218.90.220.218' + li.xpath('./td[2]/a/@href')[0]
                date_Today = li.xpath('./td[3]/text()')[0].replace('\r', '').replace('\n', '').replace('\t',
                                                                                                       '').replace(' ',
                                                                                                                   '')
                if '测试' in title:
                    continue
                if tool.Transformation(date_Today) > tool.Transformation(self.date):
                    continue
                elif tool.Transformation(date_Today) == tool.Transformation(self.date):
                    ls.append(url_)
                    continue
                else:
                    if len(url_list) == 0:
                        return [len(ls), ls]
                    else:
                        url = url_list.pop(0)
                        break

    # 济南建招工程咨询有限公司
    def sichuan(self):
        print('济南建招工程咨询有限公司', 'http://www.jnjianzhao.com')
        url_list = [
            # 招标公告
            '102',
            # 废标公告
            '119',
            # 中标公告
            '105'
        ]
        headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Cookie': 'JSESSIONID=662863FD2199FBD1672A04A290868047; _CSRFCOOKIE=73F3D7A1BCDCA9001D7B1483A214C4E98DE2528B; EPTOKEN=73F3D7A1BCDCA9001D7B1483A214C4E98DE2528B; oauthClientId=demoClient; oauthPath=http://172.16.5.21:8080/EpointWebBuilder; oauthLoginUrl=http://172.16.5.21:8080/EpointWebBuilder/rest/oauth2/authorize?client_id=demoClient&state=a&response_type=code&scope=user&redirect_uri=; oauthLogoutUrl=http://172.16.5.21:8080/EpointWebBuilder/rest/oauth2/logout?redirect_uri=; noOauthRefreshToken=986d4fe7e5dd29b64c9e7b7a6d66e089; noOauthAccessToken=77c09e0bf98b6220b544961097eed84a; sub_domain_cokie=TiG5CMD9KQ41mmsARPTuAg%3D%3D; region_name=%E4%B9%8C%E9%B2%81%E6%9C%A8%E9%BD%90%E5%B8%82',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',

        }
        url = url_list.pop(0)
        page = 0
        ls = []
        while True:
            page += 1
            if page == 1:
                text = tool.requests_get('http://www.jnjianzhao.com/channels/{}.html'.format(url), headers)
            else:
                text = tool.requests_get('http://www.jnjianzhao.com/channels/{}_{}.html'.format(url, page),
                                         headers)
            html = HTML(text)
            detail = html.xpath('//*[@id="main"]/div/div/div/div[2]/div[2]/ul/li')
            for li in detail:
                title = li.xpath('./a/text()')[0].replace('\xa0', '').replace(' ', '')
                url_ = 'http://www.jnjianzhao.com' + \
                      li.xpath('./a/@href')[0]
                date_Today = li.xpath('./span/text()')[0]
                if '测试' in title:
                    continue
                if tool.Transformation(date_Today) > tool.Transformation(self.date):
                    continue
                elif tool.Transformation(date_Today) == tool.Transformation(self.date):
                    ls.append(url_)
                else:
                    if len(url_list) == 0:
                        return [len(ls), ls]
                    else:
                        url = url_list.pop(0)
                        page = 0
                        break

    # 浙江公共资源网
    def weihai(self):
        print('浙江公共资源网', 'http://new.zmctc.com')
        url_list = ['004001', '004002', '004003', '004004', '004005', '004006']
        headers = {
            'Authorization': 'Bearer d084915340e388896b5724c69c43d5a3',
            'Cookie': 'homeid=1a444a31-e460-47ff-9931-1c075c0f3cd8',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        }
        url = url_list.pop(0)
        page = 0
        ls = []
        while True:
    num = 1
        while True:
            page += 1
            url_to = 'http://new.zmctc.com/zjgcjy/jyxx/{}/{}00{}/?Paging={}'.format(url, url, num, page)
            text = tool.requests_get(url_to, headers)
            detail = HTML(text).xpath('/html/body/div/table[1]/tr/td[2]/table/tr[2]/td/table[2]/tr/td[2]/div/table/tr')
            for li in detail:
                try:
                    title = li.xpath('./td[2]/a/@title')[0]
                    date_Today = str(li.xpath(
                        './td[3]/text()')[0]).strip().replace('[', '').replace(']', '')
                    url_ = 'http://new.zmctc.com' + li.xpath('./td[2]/a/@href')[0]
                except:
                    continue
                if '测试' in title:
                    continue
                if tool.Transformation(date_Today) > tool.Transformation(self.date):
                    continue
                elif tool.Transformation(date_Today) == tool.Transformation(self.date):
                    ls.append(url_)
                else:
                    if len(url_list) == 0:
                        return [len(ls), ls]
                    else:
                        url = url_list.pop(0)
                        page = 0
                        break

    # 浙江招标投标网   打不开
    def anhui(self):
        print('浙江招标投标网', 'http://www.zjbid.cn')
        url_list = ['001001001', '001001005', '001001009']
        headers = {
            'Cookie': 'homeid=1a444a31-e460-47ff-9931-1c075c0f3cd8',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        }
        url = url_list.pop(0)
        page = 0
        ls = []
        data = {
            '__VIEWSTATE': '',
            '__EVENTTARGET': 'MoreInfoListGG$Pager',
            '__EVENTARGUMENT': str(page)
        }
        while True:
            page += 1
            url_to = 'http://www.zjbid.cn/zjwz/template/default/GGInfo.aspx?CategoryNum={}'.format(url)
            if page == 1:
                text = tool.requests_get(url_to, headers)
            else:
                text = tool.requests_post(url_to, data, headers)
            data['__VIEWSTATE'] = HTML(text).xpath('//*[@id="__VIEWSTATE"]/@value')[0]
            data['__EVENTARGUMENT'] = str(page)
            detail = HTML(text).xpath('//*[@id="MoreInfoListGG_tdcontent"]/table/tr')
            for li in detail:
                title = li.xpath('./td[2]/a/@title')[0]
                date_Today = str(li.xpath('./td[3]/text()')[0]).strip().replace('[', '').replace(']', '')
                url_ = 'http://www.zjbid.cn' + li.xpath('./td[2]/a/@href')[0]
                if '测试' in title:
                    continue
                if tool.Transformation(date_Today) > tool.Transformation(self.date):
                    continue
                elif tool.Transformation(date_Today) == tool.Transformation(self.date):
                    ls.append(url_)
                else:
                    if len(url_list) == 0:
                        return [len(ls), ls]
                    else:
                        url = url_list.pop(0)
                        page = 0
                        break

    # 浙江政府采购网
    def yichun(self):
        print('浙江政府采购网', 'http://zfcgmanager.czt.zj.gov.cn')
        url_list = [
            'http://zfcgmanager.czt.zj.gov.cn/cms/api/cors/remote/results?pageSize=15&pageNo={}&sourceAnnouncementType=3001%2C3020&url=notice',
            'http://zfcgmanager.czt.zj.gov.cn/cms/api/cors/remote/results?pageSize=15&pageNo={}&sourceAnnouncementType=3012%2C1002%2C1003&url=notice',
            'http://zfcgmanager.czt.zj.gov.cn/cms/api/cors/remote/results?pageSize=15&pageNo={}&sourceAnnouncementType=3005%2C3017&url=notice',
            'http://zfcgmanager.czt.zj.gov.cn/cms/api/cors/remote/results?pageSize=15&pageNo={}&sourceAnnouncementType=3007&url=notice'
        ]
        headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Cookie': 'JSESSIONID=662863FD2199FBD1672A04A290868047; _CSRFCOOKIE=73F3D7A1BCDCA9001D7B1483A214C4E98DE2528B; EPTOKEN=73F3D7A1BCDCA9001D7B1483A214C4E98DE2528B; oauthClientId=demoClient; oauthPath=http://172.16.5.21:8080/EpointWebBuilder; oauthLoginUrl=http://172.16.5.21:8080/EpointWebBuilder/rest/oauth2/authorize?client_id=demoClient&state=a&response_type=code&scope=user&redirect_uri=; oauthLogoutUrl=http://172.16.5.21:8080/EpointWebBuilder/rest/oauth2/logout?redirect_uri=; noOauthRefreshToken=986d4fe7e5dd29b64c9e7b7a6d66e089; noOauthAccessToken=77c09e0bf98b6220b544961097eed84a; sub_domain_cokie=TiG5CMD9KQ41mmsARPTuAg%3D%3D; region_name=%E4%B9%8C%E9%B2%81%E6%9C%A8%E9%BD%90%E5%B8%82',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',

        }
        url = url_list.pop(0)
        page = 0
        ls = []
        while True:
            page += 1
            text = tool.requests_get(url.format(page), headers)
            detail = json.loads(text)['articles']
            for li in detail:
                title = li['title']
                city = li['districtName']
                url_ = 'http://zfcgmanager.czt.zj.gov.cn/cms/api/cors/remote/results?noticeId={}&url=noticeDetail'.format(
                    li['id'])
                time_now = int(li['pubDate'][:-3])
                date_Today = time.strftime('%Y-%m-%d', time.localtime(time_now))
                detail_text = li['keywords']
                if '测试' in title:
                    continue
                if tool.Transformation(date_Today) > tool.Transformation(self.date):
                    continue
                elif tool.Transformation(date_Today) == tool.Transformation(self.date):
                    ls.append(url_)
                else:
                    if len(url_list) == 0:
                        return [len(ls), ls]
                    else:
                        url = url_list.pop(0)
                        page = 0
                        break

    # 浠水县公共资源交易网
    def suqian(self):
        print('浠水县公共资源交易网', 'http://www.xsggzy.org.cn')
        url_list = [
            'http://www.xsggzy.org.cn/TPFront/jyxx/002002/002002001/MoreInfo.aspx?CategoryNum=002002001',
            'http://www.xsggzy.org.cn/TPFront/jyxx/002002/002002004/MoreInfo.aspx?CategoryNum=002002004'
        ]
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36',
        }
        url = url_list.pop(0)
        page = 0
        ls = []
        data = {
            '__CSRFTOKEN': '',
            '__VIEWSTATE': '',
            '__VIEWSTATEGENERATOR': '99CE51A5',
            '__EVENTTARGET': 'MoreInfoList1$Pager',
            '__EVENTARGUMENT': '2',
            '__VIEWSTATEENCRYPTED': '',
            'MoreInfoList1$Pager_input': '1'
        }
        while True:
            page += 1
            if page == 1:
                text = tool.requests_get(url, headers)
            else:
                text = tool.requests_post(url, data, headers)
            html = HTML(text)
            data['__CSRFTOKEN'] = html.xpath('//*[@id="__CSRFTOKEN"]/@value')[0]
            data['__VIEWSTATE'] = html.xpath('//*[@id="__VIEWSTATE"]/@value')[0]
            data['__VIEWSTATEGENERATOR'] = html.xpath('//*[@id="__VIEWSTATEGENERATOR"]/@value')[0]
            data['__EVENTARGUMENT'] = page + 1
            data['MoreInfoList1$Pager_input'] = page
            detail = html.xpath('//*[@id="MoreInfoList1_DataGrid1"]/tr')
            for li in detail:
                title = li.xpath('./td[2]/a/@title')[0]
                url_ = 'http://www.xsggzy.org.cn' + li.xpath('./td[2]/a/@href')[0]
                date_Today = li.xpath('./td[3]/text()')[0].replace('\n', '').replace('\r', '').replace('\t',
                                                                                                       '').replace(' ',
                                                                                                                   '')
                if '测试' in title:
                    continue
                if tool.Transformation(date_Today) > tool.Transformation(self.date):
                    continue
                elif tool.Transformation(date_Today) == tool.Transformation(self.date):
                    ls.append(url_)
                else:
                    if len(url_list) == 0:
                        return [len(ls), ls]
                    else:
                        url = url_list.pop(0)
                        page = 0
                        break

    # 深圳阳光采购平台
    def bazhong(self):
        print('深圳阳光采购平台', 'https://cgpt.sotcbb.com')
        url_list = [
            '采购公告',
            '变更公告',
            '废标公告',
            '单一来源采购公告'
        ]
        headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Cookie': 'JSESSIONID=662863FD2199FBD1672A04A290868047; _CSRFCOOKIE=73F3D7A1BCDCA9001D7B1483A214C4E98DE2528B; EPTOKEN=73F3D7A1BCDCA9001D7B1483A214C4E98DE2528B; oauthClientId=demoClient; oauthPath=http://172.16.5.21:8080/EpointWebBuilder; oauthLoginUrl=http://172.16.5.21:8080/EpointWebBuilder/rest/oauth2/authorize?client_id=demoClient&state=a&response_type=code&scope=user&redirect_uri=; oauthLogoutUrl=http://172.16.5.21:8080/EpointWebBuilder/rest/oauth2/logout?redirect_uri=; noOauthRefreshToken=986d4fe7e5dd29b64c9e7b7a6d66e089; noOauthAccessToken=77c09e0bf98b6220b544961097eed84a; sub_domain_cokie=TiG5CMD9KQ41mmsARPTuAg%3D%3D; region_name=%E4%B9%8C%E9%B2%81%E6%9C%A8%E9%BD%90%E5%B8%82',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',

        }
        url = url_list.pop(0)
        page = 0
        ls = []
        url_to = 'https://cgpt.sotcbb.com/trade/getSearchResultList'
        data = {
            'project_type': '',
            'pageNo': '0',
            'cate_id': '工程',
            'dateState': '',
            'moneyStr': '',
            'gonggaoStr': '',
            'gongshiStr': '',
            'company_name': '',
            'project_name': ''
        }
        while True:
            data['project_type'] = url
            data['pageNo'] = str(page * 10)
            text = tool.requests_post(url_to, data, headers)
            page += 1
            detail = json.loads(text)
            for li in detail:
                title = li['title']
                url_ = 'https://cgpt.sotcbb.com/trade/noticeDetail=' + str(li['id'])
                date_Today = li['publicity_start_date']
                if '测试' in title:
                    continue
                if tool.Transformation(date_Today) > tool.Transformation(self.date):
                    continue
                elif tool.Transformation(date_Today) == tool.Transformation(self.date):
                    ls.append(url_)
                else:
                    if len(url_list) == 0:
                        return [len(ls), ls]
                    else:
                        url = url_list.pop(0)
                        page = 0
                        break

    # 清远市网上中介服务超市   打不开
    def changzhou(self):
        print('清远市网上中介服务超市', 'http://wsbs.gdqy.gov.cn')
        url_list = [
            'http://wsbs.gdqy.gov.cn/gdqy-zjcs-pub/purchaseNotice'
        ]
        headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Cookie': 'JSESSIONID=662863FD2199FBD1672A04A290868047; _CSRFCOOKIE=73F3D7A1BCDCA9001D7B1483A214C4E98DE2528B; EPTOKEN=73F3D7A1BCDCA9001D7B1483A214C4E98DE2528B; oauthClientId=demoClient; oauthPath=http://172.16.5.21:8080/EpointWebBuilder; oauthLoginUrl=http://172.16.5.21:8080/EpointWebBuilder/rest/oauth2/authorize?client_id=demoClient&state=a&response_type=code&scope=user&redirect_uri=; oauthLogoutUrl=http://172.16.5.21:8080/EpointWebBuilder/rest/oauth2/logout?redirect_uri=; noOauthRefreshToken=986d4fe7e5dd29b64c9e7b7a6d66e089; noOauthAccessToken=77c09e0bf98b6220b544961097eed84a; sub_domain_cokie=TiG5CMD9KQ41mmsARPTuAg%3D%3D; region_name=%E4%B9%8C%E9%B2%81%E6%9C%A8%E9%BD%90%E5%B8%82',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',

        }
        url = url_list.pop(0)
        page = 0
        ls = []
        data = {
            'query_params_url': '/gdqy-zjcs-pub/purchaseNotice',
            'query_params_rest_url': 'purchaseNotice/listPost',
            'reloadQueryParamsReload': 'false',
            'listVo.projectName': '',
            'listVo.serviceType': '',
            'listVo.divisionCode': '441800',
            'purOrgCodePanel_selectname': '',
            'selectBox_purOrgCodePanel': '',
            'listVo.purOrgCode': '',
            'listVo.publishDateBegin': '',
            'listVo.publishDateEnd': '',
            'listVo.selectType': '',
            'listVo.projectType': '',
            'pageNumber': '1',
            'sourtType': ''
        }
        while True:
            page += 1
            if page == 1:
                text = tool.requests_get(url.format(page), headers)
            else:
                text = tool.requests_post(url.format(page), data, headers)
            data['pageNumber'] = page
            detail = HTML(text).xpath('//*[@id="resultPannel"]/table/tr')
            for li in detail:
                try:
                    title = li.xpath('./td[2]/a/text()')[0].replace('\n', '').replace('\r', '').replace('\t',
                                                                                                        '').replace(' ',
                                                                                                                    '')
                except:
                    continue
                url_ = 'http://wsbs.gdqy.gov.cn' + li.xpath('./td[2]/a/@href')[0]
                date_Today = li.xpath('./td[5]/text()')[0]
                if '测试' in title:
                    continue
                print(title)
                if tool.Transformation(date_Today) > tool.Transformation(self.date):
                    continue
                elif tool.Transformation(date_Today) == tool.Transformation(self.date):
                    ls.append(url_)
                else:
                    if len(url_list) == 0:
                        return [len(ls), ls]
                    else:
                        url = url_list.pop(0)
                        page = 0
                        break

    # 湖南公共资源交易网
    def guangdong(self):
        print('湖南公共资源交易网', 'https://ggzy.hunan.gov.cn')
        url_list_to = ['http://ggzy.hunan.gov.cn/jydt/002002/{}.html']
        headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Cookie': 'JSESSIONID=662863FD2199FBD1672A04A290868047; _CSRFCOOKIE=73F3D7A1BCDCA9001D7B1483A214C4E98DE2528B; EPTOKEN=73F3D7A1BCDCA9001D7B1483A214C4E98DE2528B; oauthClientId=demoClient; oauthPath=http://172.16.5.21:8080/EpointWebBuilder; oauthLoginUrl=http://172.16.5.21:8080/EpointWebBuilder/rest/oauth2/authorize?client_id=demoClient&state=a&response_type=code&scope=user&redirect_uri=; oauthLogoutUrl=http://172.16.5.21:8080/EpointWebBuilder/rest/oauth2/logout?redirect_uri=; noOauthRefreshToken=986d4fe7e5dd29b64c9e7b7a6d66e089; noOauthAccessToken=77c09e0bf98b6220b544961097eed84a; sub_domain_cokie=TiG5CMD9KQ41mmsARPTuAg%3D%3D; region_name=%E4%B9%8C%E9%B2%81%E6%9C%A8%E9%BD%90%E5%B8%82',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',

        }
        url = url_list_to.pop(0)
        page = 0
        ls = []
        while True:
            page += 1
            if page == 1:
                text = tool.requests_get(url.format('about'), headers)
            else:
                text = tool.requests_get(url.format(page), headers)
            detail = HTML(text).xpath('/html/body/div[2]/div[2]/div[2]/div/div[2]/ul/li')
            for tr in detail:
                title = tr.xpath('./div/a/@title')[0]
                date_Today = tr.xpath('./span/text()')[0]
                url_ = 'https://ggzy.hunan.gov.cn' + tr.xpath('./div/a/@href')[0]
                if '测试' in title:
                    continue
                if tool.Transformation(date_Today) > tool.Transformation(self.date):
                    continue
                elif tool.Transformation(date_Today) == tool.Transformation(self.date):
                    ls.append(url_)
                else:
                    if len(url_list_to) == 0:
                        return [len(ls), ls]
                    else:
                        url = url_list_to.pop(0)
                        page = 0
                        break

    # 湖南政府采购网
    def guangdongzf(self):
        print('湖南政府采购网', 'http://www.ccgp-hunan.gov.cn')
        url_list = ['http://www.ccgp-hunan.gov.cn/mvc/getNoticeList4Web.do']
        headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Cookie': 'JSESSIONID=662863FD2199FBD1672A04A290868047; _CSRFCOOKIE=73F3D7A1BCDCA9001D7B1483A214C4E98DE2528B; EPTOKEN=73F3D7A1BCDCA9001D7B1483A214C4E98DE2528B; oauthClientId=demoClient; oauthPath=http://172.16.5.21:8080/EpointWebBuilder; oauthLoginUrl=http://172.16.5.21:8080/EpointWebBuilder/rest/oauth2/authorize?client_id=demoClient&state=a&response_type=code&scope=user&redirect_uri=; oauthLogoutUrl=http://172.16.5.21:8080/EpointWebBuilder/rest/oauth2/logout?redirect_uri=; noOauthRefreshToken=986d4fe7e5dd29b64c9e7b7a6d66e089; noOauthAccessToken=77c09e0bf98b6220b544961097eed84a; sub_domain_cokie=TiG5CMD9KQ41mmsARPTuAg%3D%3D; region_name=%E4%B9%8C%E9%B2%81%E6%9C%A8%E9%BD%90%E5%B8%82',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',

        }
        url = url_list.pop(0)
        page = 0
        ls = []
        data = {
            'nType': '',
            'pType': '',
            'prcmPrjName': '',
            'prcmItemCode': '',
            'prcmOrgName': '',
            'startDate': '2021-01-01',
            'endDate': self.date,
            'prcmPlanNo': '',
            'page': '',
            'pageSize': '18'
        }
        while True:
            page += 1
            data['page'] = str(page)
            text = tool.requests_post(url, data, headers)
            detail = json.loads(text)['rows']
            for tr in detail:
                title = tr['NOTICE_TITLE']
                date_Today = tr['NEWWORK_DATE']
                url_ = 'http://www.ccgp-hunan.gov.cn/mvc/viewNoticeContent.do?noticeId={}&area_id='.format(
                    tr['NOTICE_ID'])
                if '测试' in title:
                    continue
                if tool.Transformation(date_Today) > tool.Transformation(self.date):
                    continue
                elif tool.Transformation(date_Today) == tool.Transformation(self.date):
                    ls.append(url_)
                else:
                    if len(url_list) == 0:
                        return [len(ls), ls]
                    else:
                        url = url_list.pop(0)
                        page = 0
                        break

    # 湘潭市公共资源交易平台
    def guangyuan(self):
        print('湘潭市公共资源交易平台', 'https://222.243.150.64:50680')
        url_list = [
            # 市本级
            #   工程建设
            #       招标公告
            'http://222.243.150.64:50680/zbgg/index_{}.jhtml',
            #       其他公告
            'http://222.243.150.64:50680/zsjggs/index_{}.jhtml',
            #       中标候选人公示
            'http://222.243.150.64:50680/zbhxrgs/index_{}.jhtml',
            #   政府采购
            #       采购公告
            'http://222.243.150.64:50680/cggg/index_{}.jhtml',
            #       其他公告
            'http://222.243.150.64:50680/ygg/index_{}.jhtml',
            #       更正公示
            'http://222.243.150.64:50680/gzgg/index_{}.jhtml',
            #       结果公示
            'http://222.243.150.64:50680/jggg/index_{}.jhtml'
        ]
        headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Cookie': 'JSESSIONID=662863FD2199FBD1672A04A290868047; _CSRFCOOKIE=73F3D7A1BCDCA9001D7B1483A214C4E98DE2528B; EPTOKEN=73F3D7A1BCDCA9001D7B1483A214C4E98DE2528B; oauthClientId=demoClient; oauthPath=http://172.16.5.21:8080/EpointWebBuilder; oauthLoginUrl=http://172.16.5.21:8080/EpointWebBuilder/rest/oauth2/authorize?client_id=demoClient&state=a&response_type=code&scope=user&redirect_uri=; oauthLogoutUrl=http://172.16.5.21:8080/EpointWebBuilder/rest/oauth2/logout?redirect_uri=; noOauthRefreshToken=986d4fe7e5dd29b64c9e7b7a6d66e089; noOauthAccessToken=77c09e0bf98b6220b544961097eed84a; sub_domain_cokie=TiG5CMD9KQ41mmsARPTuAg%3D%3D; region_name=%E4%B9%8C%E9%B2%81%E6%9C%A8%E9%BD%90%E5%B8%82',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',

        }
        url = url_list.pop(0)
        page = 0
        ls = []
        while True:
            page += 1
            text = tool.requests_get(url.format(page), headers)
            html = HTML(text)
            detail = html.xpath('//*[@class="text-list"]/ul/li')
            for li in detail:
                try:
                    title = li.xpath('./a/@title')[0]
                    url_ = 'http://222.243.150.64:50680' + li.xpath('./a/@href')[0]
                    date_Today = li.xpath('./a/em/text()')[0]
                except:
                    continue
                if '测试' in title:
                    continue
                if tool.Transformation(date_Today) > tool.Transformation(self.date):
                    continue
                elif tool.Transformation(date_Today) == tool.Transformation(self.date):
                    ls.append(url_)
                else:
                    if len(url_list) == 0:
                        return [len(ls), ls]
                    else:
                        url = url_list.pop(0)
                        page = 0
                        break

    # 甘肃政府采购网
    def guangan(self):
        print('甘肃政府采购网', 'http://www.ccgp-gansu.gov.cn')
        url_list = [
            'http://www.ccgp-gansu.gov.cn/web/doSearchmxarticlels.action?limit=20&start={}'
        ]
        headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Cookie': 'JSESSIONID=662863FD2199FBD1672A04A290868047; _CSRFCOOKIE=73F3D7A1BCDCA9001D7B1483A214C4E98DE2528B; EPTOKEN=73F3D7A1BCDCA9001D7B1483A214C4E98DE2528B; oauthClientId=demoClient; oauthPath=http://172.16.5.21:8080/EpointWebBuilder; oauthLoginUrl=http://172.16.5.21:8080/EpointWebBuilder/rest/oauth2/authorize?client_id=demoClient&state=a&response_type=code&scope=user&redirect_uri=; oauthLogoutUrl=http://172.16.5.21:8080/EpointWebBuilder/rest/oauth2/logout?redirect_uri=; noOauthRefreshToken=986d4fe7e5dd29b64c9e7b7a6d66e089; noOauthAccessToken=77c09e0bf98b6220b544961097eed84a; sub_domain_cokie=TiG5CMD9KQ41mmsARPTuAg%3D%3D; region_name=%E4%B9%8C%E9%B2%81%E6%9C%A8%E9%BD%90%E5%B8%82',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',

        }
        url = url_list.pop(0)
        page = 0
        ls = []
        url_to = 'http://www.ccgp-gansu.gov.cn/web/doSearchmxarticlels.action?articleSearchInfoVo.releasestarttime=&articleSearchInfoVo.releaseendtime=&articleSearchInfoVo.tflag=1&articleSearchInfoVo.classname=128&articleSearchInfoVo.dtype=&articleSearchInfoVo.days=&articleSearchInfoVo.releasestarttimeold=&articleSearchInfoVo.releaseendtimeold=&articleSearchInfoVo.title=&articleSearchInfoVo.agentname=&articleSearchInfoVo.bidcode=&articleSearchInfoVo.proj_name=&articleSearchInfoVo.buyername=&total=0&limit=20&current=1&sjm=7466'
        session = requests.session()
        while True:
            page += 1
            if page == 1:
                text = tool.session_get(url_to, session).replace('\xa9', '')
            else:
                text = tool.session_get(url.format((page - 1) * 20), session).replace('\xa9', '')
            html = HTML(text)
            detail = html.xpath('//*[@id="mainContent"]/div[2]/div[4]/ul/li')
            for li in detail:
                title = li.xpath('./a/text()')[0]
                url_ = 'http://www.ccgp-gansu.gov.cn' + li.xpath('./a/@href')[0]
                date_Today = li.xpath('./p[1]/span/text()')[0].replace('\r', '').replace('\n', '').replace('\t', '') \
                                 .replace(' ', '').split('|')[1].replace('发布时间：', '')[:10]
                if '测试' in title:
                    continue
                if tool.Transformation(date_Today) > tool.Transformation(self.date):
                    continue
                elif tool.Transformation(date_Today) == tool.Transformation(self.date):
                    ls.append(url_)
                else:
                    if len(url_list) == 0:
                        return [len(ls), ls]
                    else:
                        url = url_list.pop(0)
                        page = 0
                        break

    # 甘肃省阳光招标采购信息
    def qingyang(self):
        print('甘肃省阳光招标采购信息', 'http://ygjy.ggzyjy.gansu.gov.cn:3040')
        url_list = [
            '1',
            '3'
        ]
        headers = {
            # 'Accept': 'application/json, text/javascript, */*; q=0.01',
            # 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Cookie': 'ASP.NET_SessionId=35z2fvq5lvv2beeme22crjin; __CSRFCOOKIE=b36f48c6-fa2d-4882-bd90-6012bef4acb3',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',

        }
        url = url_list.pop(0)
        page = 0
        ls = []
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
            data['annoType'] = url
            data['pageNo'] = page
            text = '<div id="body">' + tool.requests_post(url_to, data, headers) + '</div>'
            html = HTML(text)
            detail = html.xpath('//*[@id="body"]/a')
            for li in detail:
                title = li.xpath('./div/@title')[0]
                url_ = 'http://ygjy.ggzyjy.gansu.gov.cn:3040' + li.xpath('./@href')[0]
                date_Today = li.xpath('./span/text()')[0].replace('\n', '').replace('\t', '').replace('\r',
                                                                                                      '').replace(
                    ' ', '')
                if '测试' in title:
                    continue
                if tool.Transformation(date_Today) > tool.Transformation(self.date):
                    continue
                elif tool.Transformation(date_Today) == tool.Transformation(self.date):
                    ls.append(url_)
                else:
                    if len(url_list) == 0:
                        return [len(ls), ls]
                    else:
                        url = url_list.pop(0)
                        page = 0
                        break

    # 白城市公共资源交易平台
    def zhangye(self):
        print('白城市公共资源交易平台', 'http://ggzy.jlbc.gov.cn')
        url_list = [
            # 工程建设
            'http://ggzy.jlbc.gov.cn/jyxx/003001/{}.html',
            # 政府采购
            'http://ggzy.jlbc.gov.cn/jyxx/003002/{}.html'
        ]
        headers = {
            # 'Accept': 'application/json, text/javascript, */*; q=0.01',
            # 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Cookie': 'JSESSIONID=662863FD2199FBD1672A04A290868047; _CSRFCOOKIE=73F3D7A1BCDCA9001D7B1483A214C4E98DE2528B; EPTOKEN=73F3D7A1BCDCA9001D7B1483A214C4E98DE2528B; oauthClientId=demoClient; oauthPath=http://172.16.5.21:8080/EpointWebBuilder; oauthLoginUrl=http://172.16.5.21:8080/EpointWebBuilder/rest/oauth2/authorize?client_id=demoClient&state=a&response_type=code&scope=user&redirect_uri=; oauthLogoutUrl=http://172.16.5.21:8080/EpointWebBuilder/rest/oauth2/logout?redirect_uri=; noOauthRefreshToken=986d4fe7e5dd29b64c9e7b7a6d66e089; noOauthAccessToken=77c09e0bf98b6220b544961097eed84a; sub_domain_cokie=TiG5CMD9KQ41mmsARPTuAg%3D%3D; region_name=%E4%B9%8C%E9%B2%81%E6%9C%A8%E9%BD%90%E5%B8%82',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',

        }
        url = url_list.pop(0)
        page = 0
        ls = []
        while True:
            page += 1
            if page == 1:
                text = tool.requests_get(url.format('secondPage'), headers)
            else:
                text = tool.requests_get(url.format(str(page)), headers)
            html = HTML(text)
            detail = html.xpath('//div[@class="ewb-info"]/ul/li')
            for li in detail:
                try:
                    title = li.xpath('./div/a/text()')[1].replace('\r', '').replace('\n', '').replace('\t', '').replace(
                        ' ', '')
                except:
                    title = li.xpath('./div/a/text()')[0].replace('\r', '').replace('\n', '').replace('\t', '').replace(
                        ' ', '')
                url_ = 'http://ggzy.jlbc.gov.cn' + li.xpath('./div/a/@href')[0]
                date_Today = li.xpath('./span/text()')[0].replace('\r', '').replace('\n', '').replace('\t', '').replace(
                    ' ', '')
                if tool.Transformation(date_Today) > tool.Transformation(self.date):
                    continue
                elif tool.Transformation(date_Today) == tool.Transformation(self.date):
                    ls.append(url_)
                else:
                    if len(url_list) == 0:
                        return [len(ls), ls]
                    else:
                        url = url_list.pop(0)
                        page = 0
                        break

    # 腾冲市公共资源
    def dezhou(self):
        print('腾冲市公共资源', 'https://www.tcsggzyjyw.com')
        url_list = [
            {
                "data": '["TrueLore.Web.WebUI.WebAjaxService","GetPageZBGGByCCGC",[{},15,"JSGC",1,"0",0,2,"BDMCGGBT","","ZBGG_Fbqssj DESC, PublishTime DESC"],null,null]',
                "url": 'http://www.tcsggzyjyw.com/Jyweb/ZBGGView.aspx?isbg=0&guid={}&type=%e4%ba%a4%e6%98%93%e4%bf%a1%e6%81%af&subType=1&subType2=1&zbtype=0&xxlb=%E4%BA%A4%E6%98%93%E4%BF%A1%E6%81%AF&IsShow=1'
            },
            {
                "data": '["TrueLore.Web.WebUI.WebAjaxService","GetPageJYXTXXFB_1",[{},15,"JSGC","0","24","0",2,"GCBDMC","","FBKSSJ DESC"],null,null]',
                "url": 'http://www.tcsggzyjyw.com/Jyweb/PBJGGSNewView.aspx?isBG=1&guid={}&subType2=24&subType=1&type=%E4%BA%A4%E6%98%93%E4%BF%A1%E6%81%AF&zbtype=0'
            },
            {
                "data": '["TrueLore.Web.WebUI.WebAjaxService","GetPageJYXTXXFB_1",[{},15,"ZFCG","28","0",4,1,"BDMCGGBT","","Fbkssj DESC"],null,null]',
                "url": 'http://www.tcsggzyjyw.com/Jyweb/ZFCGZBJGGSViewNew.aspx?isBG=0&guid={}&subType2=28&subType=2&type=%E4%BA%A4%E6%98%93%E4%BF%A1%E6%81%AF&xxlb=%E4%BA%A4%E6%98%93%E4%BF%A1%E6%81%AF'
            },
            {
                "data": '["TrueLore.Web.WebUI.WebAjaxService","GetPageJYXTXXFB_1",[{},15,"JSGC","0","5","0",2,"GCBDMC","","FBKSSJ DESC"],null,null]',
                "url": 'http://www.tcsggzyjyw.com/Jyweb/PBJGGSNewView.aspx?isBG=0&guid={}&subType2=5&subType=1&type=%E4%BA%A4%E6%98%93%E4%BF%A1%E6%81%AF&zbtype=0'
            },

            {
                "data": '["TrueLore.Web.WebUI.WebAjaxService","GetPageZBGGByCCGC",[{},15,"ZFCG","12","0",4,1,"BDMCGGBT","","ZBGG_Fbqssj DESC, PublishTime DESC"],null,null]',
                "url": 'http://www.tcsggzyjyw.com/Jyweb/ZFCGView.aspx?isBG=0&guid={}&subType2=12&subType=2&type=%E4%BA%A4%E6%98%93%E4%BF%A1%E6%81%AF&xxlb=%E4%BA%A4%E6%98%93%E4%BF%A1%E6%81%AF&IsShow=1'
            },
            {
                "data": '["TrueLore.Web.WebUI.WebAjaxService","GetPageZFCG",[{},15,"ZFCG","13","0",4,"BDMCGGBT","","Fbkssj DESC"],null,null]',
                "url": 'http://www.tcsggzyjyw.com/Jyweb/JYXTXXView.aspx?isBG=0&guid={}&subType2=13&subType=2&type=%E4%BA%A4%E6%98%93%E4%BF%A1%E6%81%AF&xxlb=%E4%BA%A4%E6%98%93%E4%BF%A1%E6%81%AF'
            },
            {
                "data": '["TrueLore.Web.WebUI.WebAjaxService","GetPageZFCG",[{},15,"ZFCG","14","0",4,"BDMCGGBT","","Fbkssj DESC"],null,null]',
                "url": 'http://www.tcsggzyjyw.com/Jyweb/ZFCGZBJGGSViewNew.aspx?isBG=0&guid={}&subType2=14&subType=2&type=%E4%BA%A4%E6%98%93%E4%BF%A1%E6%81%AF&xxlb=%E4%BA%A4%E6%98%93%E4%BF%A1%E6%81%AF'
            },
            {
                "data": '["TrueLore.Web.WebUI.WebAjaxService","GetPageJYXTXXFB_1",[{},15,"ZFCG","28","0",4,1,"BDMCGGBT","","Fbkssj DESC"],null,null]',
                "url": 'http://www.tcsggzyjyw.com/Jyweb/ZFCGZBJGGSViewNew.aspx?isBG=0&guid={}&subType2=28&subType=2&type=%E4%BA%A4%E6%98%93%E4%BF%A1%E6%81%AF&xxlb=%E4%BA%A4%E6%98%93%E4%BF%A1%E6%81%AF'
            },
            {
                'data': '["TrueLore.Web.WebUI.WebAjaxService","GetPageJYXTXXFB_1",[{},15,"JSGC","0","11","0",2,"GCBDMC","","FBKSSJ DESC"],null,null]',
                'url' : 'http://www.tcsggzyjyw.com/Jyweb/ZBJGGSNewView.aspx?isBG=0&guid={}&subType2=11&subType=1&type=%E4%BA%A4%E6%98%93%E4%BF%A1%E6%81%AF&zbtype=0'
            }
        ]
        headers = {
            "Ajax-method": "AjaxMethodFactory",
            "Content-Type": "text/plain; charset=UTF-8",
        }
        url = url_list.pop(0)
        ls = []
        url_to = 'https://www.tcsggzyjyw.com/TrueLoreAjax/TrueLore.Web.WebUI.AjaxHelper,TrueLore.Web.WebUI.ashx'
        page = 0
        while True:
            text = tool.requests_post(url_to, url['data'].format(page * 15), headers)
            page += 1
            detail = text[2:-1].split('},{')
            for li in detail:
                try:
                    id = re.findall('XXFBGuid:"(.*?)"', li)[0]
                except:
                    id = re.findall('Guid:"(.*?)"', li)[0]
                url_ = url['url'].format(id)
                try:
                    title = re.findall('BDMCGGBT:"(.*?)"', li)[0]
                except:
                    title = re.findall('FHJGGSTitle:"(.*?)"', li)[0]
                date_Today = re.findall('FBKSSJ:"(.*?)"', li)[0][:10]
                if '测试' in title:
                    continue
                if tool.Transformation(date_Today) > tool.Transformation(self.date):
                    continue
                elif tool.Transformation(date_Today) == tool.Transformation(self.date):
                    ls.append(url_)
                else:
                    if len(url_list) == 0:
                        return [len(ls), ls]
                    else:
                        url = url_list.pop(0)
                        page = 0
                        break

    # 舟山市定海区公共资源交易网
    def chengdu(self):
        print('舟山市定海区公共资源交易网', 'http://dhggzy.dinghai.gov.cn')
        url_list = [
            'http://dhggzy.dinghai.gov.cn/dhggzy/gcjs/010008/?Paging={}',
            'http://dhggzy.dinghai.gov.cn/dhggzy/gcjs/010009/?Paging={}',
            'http://dhggzy.dinghai.gov.cn/dhggzy/gcjs/010010/?Paging={}',
            'http://dhggzy.dinghai.gov.cn/dhggzy/zfcg/011001/?Paging={}',
            'http://dhggzy.dinghai.gov.cn/dhggzy/zfcg/011002/?Paging={}'
        ]
        headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Cookie': 'JSESSIONID=662863FD2199FBD1672A04A290868047; _CSRFCOOKIE=73F3D7A1BCDCA9001D7B1483A214C4E98DE2528B; EPTOKEN=73F3D7A1BCDCA9001D7B1483A214C4E98DE2528B; oauthClientId=demoClient; oauthPath=http://172.16.5.21:8080/EpointWebBuilder; oauthLoginUrl=http://172.16.5.21:8080/EpointWebBuilder/rest/oauth2/authorize?client_id=demoClient&state=a&response_type=code&scope=user&redirect_uri=; oauthLogoutUrl=http://172.16.5.21:8080/EpointWebBuilder/rest/oauth2/logout?redirect_uri=; noOauthRefreshToken=986d4fe7e5dd29b64c9e7b7a6d66e089; noOauthAccessToken=77c09e0bf98b6220b544961097eed84a; sub_domain_cokie=TiG5CMD9KQ41mmsARPTuAg%3D%3D; region_name=%E4%B9%8C%E9%B2%81%E6%9C%A8%E9%BD%90%E5%B8%82',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',

        }
        url = url_list.pop(0)
        page = 0
        ls = []
        while True:
            page += 1
            text = tool.requests_get(url.format(page), headers)
            detail = HTML(text).xpath('/html/body/div/div[2]/div/div[2]/div[2]/table/tr/td/table/tr')
            for li in detail:
                try:
                    title = li.xpath('./td[2]/a/@title')[0]
                    url_ = 'http://dhggzy.dinghai.gov.cn' + li.xpath('./td[2]/a/@href')[0]
                    date_Today = li.xpath('./td[3]/text()')[0].replace('[', '').replace(']', '')
                except:
                    continue
                if '测试' in title:
                    continue
                if tool.Transformation(date_Today) > tool.Transformation(self.date):
                    continue
                elif tool.Transformation(date_Today) == tool.Transformation(self.date):
                    ls.append(url_)
                else:
                    if len(url_list) == 0:
                        return [len(ls), ls]
                    else:
                        url = url_list.pop(0)
                        page = 0
                        break

    # 菏泽市牡丹区政府  需要线上修改
    def yangzhou(self):
        print('菏泽市牡丹区政府', 'http://www.mudan.gov.cn')
        url_list = [
            'http://www.mudan.gov.cn/module/xxgk/search.jsp?standardXxgk=1&infotypeId=A08&vc_title=&vc_number=&area=&infotypeId=0&jdid=122&divid=div23160&vc_title=&vc_number=&currpage=&vc_filenumber=&vc_all=&texttype=&fbtime=&standardXxgk=1&infotypeId=A08&vc_title=&vc_number=&area='
        ]
        headers = {
            # 'Accept': 'application/json, text/javascript, */*; q=0.01',
            # 'Content-Type': 'application/json;charset=UTF-8',
            # 'Cookie': 'suite-pmsuite=9d1e2f2a-1554-4331-87d3-7764a4418a5e',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',

        }
        url = url_list.pop(0)
        page = 0
        ls = []
        while True:
            text = tool.requests_get(url, headers)
            html = HTML(text)
            detail = html.xpath('//li')
            for li in detail:
                title = li.xpath('./a/@title')[0]
                url_ = li.xpath('./a/@href')[0]
                date_Today = \
                    li.xpath('./b/text()')[0].replace('\n', '').replace('\t', '').replace('/', '-').replace(
                        '\r',
                        '').replace(
                        ' ', '')
                if '测试' in title:
                    continue
                if tool.Transformation(date_Today) > tool.Transformation(self.date):
                    continue
                elif tool.Transformation(date_Today) == tool.Transformation(self.date):
                    ls.append(url_)
                else:
                    continue
            return [len(ls), ls]

    # 衡阳市公共资源交易平台
    def panzhihua(self):
        print('衡阳市公共资源交易平台', 'https://ggzy.hengyang.gov.cn')
        url_list = [
            # 市本级
            #   工程建设
            #       招标公告
            'http://ggzy.hengyang.gov.cn/jyxx/jsgcjy/zbgg/{}.html',
            #       其他公告
            'http://ggzy.hengyang.gov.cn/jyxx/jsgcjy/qtgg/{}.html',
            #       中标候选人公示
            'http://ggzy.hengyang.gov.cn/jyxx/jsgcjy/zbhxrgs/{}.html',
            #   政府采购
            #       采购公告
            'http://ggzy.hengyang.gov.cn/jyxx/zfcgjy/zbgg/{}.html',
            #       其他公告
            'http://ggzy.hengyang.gov.cn/jyxx/zfcgjy/qtgg/{}.html',
            #       结果公示
            'http://ggzy.hengyang.gov.cn/jyxx/zfcgjy/jggs/{}.html'
        ]
        headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Cookie': 'JSESSIONID=662863FD2199FBD1672A04A290868047; _CSRFCOOKIE=73F3D7A1BCDCA9001D7B1483A214C4E98DE2528B; EPTOKEN=73F3D7A1BCDCA9001D7B1483A214C4E98DE2528B; oauthClientId=demoClient; oauthPath=http://172.16.5.21:8080/EpointWebBuilder; oauthLoginUrl=http://172.16.5.21:8080/EpointWebBuilder/rest/oauth2/authorize?client_id=demoClient&state=a&response_type=code&scope=user&redirect_uri=; oauthLogoutUrl=http://172.16.5.21:8080/EpointWebBuilder/rest/oauth2/logout?redirect_uri=; noOauthRefreshToken=986d4fe7e5dd29b64c9e7b7a6d66e089; noOauthAccessToken=77c09e0bf98b6220b544961097eed84a; sub_domain_cokie=TiG5CMD9KQ41mmsARPTuAg%3D%3D; region_name=%E4%B9%8C%E9%B2%81%E6%9C%A8%E9%BD%90%E5%B8%82',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',

        }
        url = url_list.pop(0)
        page = 0
        ls = []
        while True:
            page += 1
            if page == 1:
                text = tool.requests_get(url.format('index'), headers)
            else:
                text = tool.requests_get(url.format('pages/' + str(page)), headers)
            html = HTML(text)
            detail = html.xpath('/html/body/div[2]/div/div/div[2]/div[3]/ul/li')
            for li in detail:
                title = li.xpath('./a/text()')[0]
                url_ = li.xpath('./a/@href')[0]
                date_Today = li.xpath('./span/text()')[0]
                if '测试' in title:
                    continue
                if tool.Transformation(date_Today) > tool.Transformation(self.date):
                    continue
                elif tool.Transformation(date_Today) == tool.Transformation(self.date):
                    ls.append(url_)
                else:
                    if len(url_list) == 0:
                        return [len(ls), ls]
                    else:
                        url = url_list.pop(0)
                        page = 0
                        break

    # 诚E招
    def xinyu(self):
        print('诚E招', 'https://www.chengezhao.com')
        url_list = [
           'https://www.chengezhao.com/cms/channel/ywgg/index.htm?pageNo={}'
        ]
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        }
        url = url_list.pop(0)
        page = 0
        ls = []
        while True:
            page += 1
            text = tool.requests_get(url.format(page), headers)
            html = HTML(text)
            detail = html.xpath('//*[@class="cez-business-main__news"]/div')
            for li in detail:
                try:
                    title = li.xpath('./div[2]/p/text()')[0].replace('\xa0', '').replace(' ', '')
                    url_ = 'https://www.chengezhao.com' + \
                          li.xpath('./a/@href')[0]
                    date_Today = li.xpath('./a/span[2]/text()')[0] + '-' + li.xpath('./a/span[1]/text()')[0]
                except:
                    continue
                if '测试' in title:
                    continue
                if tool.Transformation(date_Today) > tool.Transformation(self.date):
                    continue
                elif tool.Transformation(date_Today) == tool.Transformation(self.date):
                    ls.append(url_)
                else:
                    if len(url_list) == 0:
                        return [len(ls), ls]
                    else:
                        url = url_list.pop(0)
                        page = 0
                        break

    # 辽宁省公共资源交易平台
    def wuxi(self):
        print('辽宁省公共资源交易平台', 'http://www.lnggzy.gov.cn')
        url_list = [
            # 建设工程
            'http://www.lnggzy.gov.cn/lnggzy/showinfo/Morejyxx.aspx?timebegin=2021-02-01&timeend={}&timetype=04&num1=002&num2=002000&jyly=005&word=',
            # 政府采购
            'http://www.lnggzy.gov.cn/lnggzy/showinfo/Morejyxx.aspx?timebegin=2021-02-01&timeend={}&timetype=04&num1=001&num2=001000&jyly=005&word='
        ]
        headers = {
            'Cookie': 'ASP.NET_SessionId=ruvsda55gi0qkjntbtdsrm55',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        }
        url = url_list.pop(0)
        page = 0
        ls = []
        data = {
            '__VIEWSTATE': '',
            '__VIEWSTATEGENERATOR': '',
            '__EVENTTARGET': 'MoreInfoListjyxx1$Pager',
            '__EVENTARGUMENT': '',
            '__VIEWSTATEENCRYPTED': '',
            'MoreInfoListjyxx1$Pager_input': ''
        }
        while True:
            page += 1
            if page == 1:
                text = tool.requests_get(url.format(self.date), headers)
            else:
                text = tool.requests_post(url.format(self.date), data, headers)
            html = HTML(text)
            data['__VIEWSTATE'] = html.xpath('//*[@id="__VIEWSTATE"]/@value')[0]
            data['__VIEWSTATEGENERATOR'] = html.xpath('//*[@id="__VIEWSTATEGENERATOR"]/@value')[0]
            data['__EVENTARGUMENT'] = page + 1
            data['MoreInfoListjyxx1$Pager_input'] = page
            detail = html.xpath('//*[@id="MoreInfoListjyxx1_DataGrid1"]/tr')
            for li in detail:
                title = li.xpath('./td/div/div/h4/a/@title')[0]
                url_ = 'http://www.lnggzy.gov.cn' + li.xpath('./td/div/div/h4/a/@href')[0]
                date_Today = li.xpath('./td/div/div/h4/span/text()')[0].replace(' ', '')
                if tool.Transformation(date_Today) > tool.Transformation(self.date):
                    continue
                elif tool.Transformation(date_Today) == tool.Transformation(self.date):
                    ls.append(url_)
                else:
                    if len(url_list) == 0:
                        return [len(ls), ls]
                    else:
                        url = url_list.pop(0)
                        page = 0
                        break

    # 辽宁省政府采购网
    def rizhao(self):
        print('辽宁省政府采购网', 'http://ccgp-liaoning.gov.cn')
        url_list = [
            # 采购公告
            '1001',
            # 单一来源
            '1008',
            # 结果公告
            '1002',
            # 更正公告
            '1003'

        ]
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        }
        url = url_list.pop(0)
        page = 0
        ls = []
        url_to = 'http://ccgp-liaoning.gov.cn/portalindex.do?method=getPubInfoList&t_k=null'
        data = {
            'current': '',
            'rowCount': '10',
            'searchPhrase': '',
            'infoTypeCode': ''
        }
        while True:
            page += 1
            data['current'] = page
            data['infoTypeCode'] = url
            t = tool.requests_post(url_to, data, headers)
            detail = json.loads(t)['rows']
            for li in detail:
                title = li['title']
                url_ = 'http://ccgp-liaoning.gov.cn/portalindex.do?method=getPubInfoViewOpenNew&infoId=' + li['id']
                date_Today = li['releaseDate']
                if tool.Transformation(date_Today) > tool.Transformation(self.date):
                    continue
                elif tool.Transformation(date_Today) == tool.Transformation(self.date):
                    ls.append(url_)
                else:
                    if len(url_list) == 0:
                        return [len(ls), ls]
                    else:
                        url = url_list.pop(0)
                        page = 0
                        break

    # 重庆市公共资源交易网
    def zaozhuang(self):
        print('重庆市公共资源交易网', 'https://www.cqggzy.com')
        url_list = ["014001001",  "014001003", "014001004", "014001016"]
        headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Cookie': 'JSESSIONID=662863FD2199FBD1672A04A290868047; _CSRFCOOKIE=73F3D7A1BCDCA9001D7B1483A214C4E98DE2528B; EPTOKEN=73F3D7A1BCDCA9001D7B1483A214C4E98DE2528B; oauthClientId=demoClient; oauthPath=http://172.16.5.21:8080/EpointWebBuilder; oauthLoginUrl=http://172.16.5.21:8080/EpointWebBuilder/rest/oauth2/authorize?client_id=demoClient&state=a&response_type=code&scope=user&redirect_uri=; oauthLogoutUrl=http://172.16.5.21:8080/EpointWebBuilder/rest/oauth2/logout?redirect_uri=; noOauthRefreshToken=986d4fe7e5dd29b64c9e7b7a6d66e089; noOauthAccessToken=77c09e0bf98b6220b544961097eed84a; sub_domain_cokie=TiG5CMD9KQ41mmsARPTuAg%3D%3D; region_name=%E4%B9%8C%E9%B2%81%E6%9C%A8%E9%BD%90%E5%B8%82',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',

        }
        url = url_list.pop(0)
        page = 0
        ls = []
        url_to = 'https://www.cqggzy.com/EpointWebBuilderService/getInfoListAndCategoryList.action?cmd=getInfoList&pageIndex={}&pageSize=18&siteguid=d7878853-1c74-4913-ab15-1d72b70ff5e7&categorynum={}&title=&infoC=&_=1570670109425'
        while True:
            page += 1
            text = tool.requests_get(url_to.format(page, url), headers)
            detail = json.loads(json.loads(text)['custom'])
            for li in detail:
                date_Today = li["infodate"].replace('\n', '').replace('\t', '').replace('\r', '').replace(' ', '') \
                    .replace('[', '').replace(']', '')
                categorynum = li["categorynum"]
                time_to = str(tool.Time_stamp_to_date(tool.Transformation(date_Today) - 86400)).replace("-", "")
                id = li["infoid"]
                title = li["title"]
                if url == "014001001":
                    url_ = "https://www.cqggzy.com/xxhz/014001/{}/{}/{}/{}.html".format(url, categorynum, time_to,
                                                                                       id)
                else:
                    url_ = 'https://www.cqggzy.com/xxhz/014001/{}/{}/{}.html'.format(url, time_to, id)
                if '测试' in title:
                    continue
                if tool.Transformation(date_Today) > tool.Transformation(self.date):
                    continue
                elif tool.Transformation(date_Today) == tool.Transformation(self.date):
                    ls.append(url_)
                else:
                    if len(url_list) == 0:
                        return [len(ls), ls]
                    else:
                        url = url_list.pop(0)
                        page = 0
                        break

    # 重庆市政府采购网
    def jiangsu(self):
        print('重庆市政府采购网', 'https://www.ccgp-chongqing.gov.cn')
        url_list = [
            'https://www.ccgp-chongqing.gov.cn/gwebsite/api/v1/notices/stable/new?endDate={}&pi={}&ps=20&startDate=2020-06-05'
        ]

        headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Cookie': 'JSESSIONID=662863FD2199FBD1672A04A290868047; _CSRFCOOKIE=73F3D7A1BCDCA9001D7B1483A214C4E98DE2528B; EPTOKEN=73F3D7A1BCDCA9001D7B1483A214C4E98DE2528B; oauthClientId=demoClient; oauthPath=http://172.16.5.21:8080/EpointWebBuilder; oauthLoginUrl=http://172.16.5.21:8080/EpointWebBuilder/rest/oauth2/authorize?client_id=demoClient&state=a&response_type=code&scope=user&redirect_uri=; oauthLogoutUrl=http://172.16.5.21:8080/EpointWebBuilder/rest/oauth2/logout?redirect_uri=; noOauthRefreshToken=986d4fe7e5dd29b64c9e7b7a6d66e089; noOauthAccessToken=77c09e0bf98b6220b544961097eed84a; sub_domain_cokie=TiG5CMD9KQ41mmsARPTuAg%3D%3D; region_name=%E4%B9%8C%E9%B2%81%E6%9C%A8%E9%BD%90%E5%B8%82',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',

        }
        url = url_list.pop(0)
        page = 0
        ls = []
        while True:
            page += 1
            text = tool.requests_get(url.format(self.date, page), headers)
            detail = json.loads(text)['notices']
            for li in detail:
                id = li["id"]
                date_Today = li["issueTime"][:10]
                url_ = "https://www.ccgp-chongqing.gov.cn/gwebsite/api/v1/notices/stable/{}".format(id)
                title = li['title']
                if '测试' in title:
                    continue
                if tool.Transformation(date_Today) > tool.Transformation(self.date):
                    continue
                elif tool.Transformation(date_Today) == tool.Transformation(self.date):
                    ls.append(url_)
                else:
                    if len(url_list) == 0:
                        return [len(ls), ls]
                    else:
                        url = url_list.pop(0)
                        page = 0
                        break

    # 重庆市铜梁区公共资源综合交易中心  未完成
    def jiangxi(self):
        print('重庆市铜梁区公共资源综合交易中心', 'https://qjyzx.cqstl.gov.cn')
        url_list = [
            '863',
            '864'
        ]
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        }
        url = url_list.pop(0)
        page = 0
        ls = []
        url_to = 'https://qjyzx.cqstl.gov.cn/zfxx/data/datalist.asp'
        data = {
            'page': '1',
            'max': '10',
            'KeyWords': '',
            'OrganizationCode': '93',
            'SubjectCategoryCode': '863',
            'ThemeCategoryCode': '865',
            'CustomerCategoryCode': '',
            'SubjectKeywordCode': '',
            'IndexNO': '',
            'StartDate': '',
            'EndDate': '',
            'Level': '',
            'GWZ': '',
            'NH': '',
            'QH': ''
        }
        while True:
            page += 1
            data['SubjectCategoryCode'] = url
            data['page'] = page
            text = tool.requests_post(url_to, data, headers)
            print(11, text)
            time.sleep(666)
            detail = json.loads(text)['datalist']
            for li in detail:
                title = li['Title']
                url_ = 'https://qjyzx.cqstl.gov.cn' + li['Url']
                date_Today = li['Date']
                if '测试' in title:
                    continue
                if tool.Transformation(date_Today) > tool.Transformation(self.date):
                    continue
                elif tool.Transformation(date_Today) == tool.Transformation(self.date):
                    ls.append(url_)
                else:
                    if len(url_list) == 0:
                        return [len(ls), ls]
                    else:
                        url = url_list.pop(0)
                        page = 0
                        break

    # 银川市公共资源交易中心
    def taizhou(self):
        print('银川市公共资源交易中心', 'http://www.ycsggzy.cn')
        url_list = [
            '12|0|{}|20',
            '12|1|{}|20'
        ]
        headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Cookie': 'JSESSIONID=662863FD2199FBD1672A04A290868047; _CSRFCOOKIE=73F3D7A1BCDCA9001D7B1483A214C4E98DE2528B; EPTOKEN=73F3D7A1BCDCA9001D7B1483A214C4E98DE2528B; oauthClientId=demoClient; oauthPath=http://172.16.5.21:8080/EpointWebBuilder; oauthLoginUrl=http://172.16.5.21:8080/EpointWebBuilder/rest/oauth2/authorize?client_id=demoClient&state=a&response_type=code&scope=user&redirect_uri=; oauthLogoutUrl=http://172.16.5.21:8080/EpointWebBuilder/rest/oauth2/logout?redirect_uri=; noOauthRefreshToken=986d4fe7e5dd29b64c9e7b7a6d66e089; noOauthAccessToken=77c09e0bf98b6220b544961097eed84a; sub_domain_cokie=TiG5CMD9KQ41mmsARPTuAg%3D%3D; region_name=%E4%B9%8C%E9%B2%81%E6%9C%A8%E9%BD%90%E5%B8%82',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',

        }
        url = url_list.pop(0)
        page = 0
        ls = []
        url_to = 'http://www.ycsggzy.cn/Ajax/morelink.ashx'
        data = {
            'czlx': 'linetxt',
            'cxcs': '12|1|1|20'
        }
        while True:
            page += 1
            data['cxcs'] = url.format(page)
            text = tool.requests_post(url_to, data, headers)
            html = HTML(text)
            detail = html.xpath('//ul/li')
            for li in detail:
                title = li.xpath('./a/text()')[0]
                url_ = 'http://www.ycsggzy.cn/' + li.xpath('./a/@href')[0]
                date_Today = \
                li.xpath('./a/span/text()')[0].replace('\n', '').replace('\t', '').replace('/', '-').replace('\r',
                                                                                                             '').replace(
                    ' ', '').split('\xa0')[0]
                if '测试' in title:
                    continue
                if tool.Transformation(date_Today) > tool.Transformation(self.date):
                    continue
                elif tool.Transformation(date_Today) == tool.Transformation(self.date):
                    ls.append(url_)
                else:
                    if len(url_list) == 0:
                        return [len(ls), ls]
                    else:
                        url = url_list.pop(0)
                        page = 0
                        break


    # 陕西政府采购
    def jining(self):
        print('陕西政府采购', 'http://www.ccgp-shaanxi.gov.cn')
        url_list = ['3', '5', '4', '6', '99', '1']
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Host': 'www.jxsggzy.cn',
            'If-Modified-Since': 'Mon, 07 Dec 2020 08:56:39 GMT',
            'If-None-Match': 'W/"5fcdee47-6eab"',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36',
        }
        url = url_list.pop(0)
        page = 0
        ls = []
        url_to = 'http://www.ccgp-shaanxi.gov.cn/notice/noticeaframe.do?isgovertment=&noticetype={}'
        while True:
            page += 1
            data = {
                "parameters['purcatalogguid']": '',
                'page.pageNum': str(page),
                "parameters['title']": '',
                "parameters['startdate']": '',
                "parameters['enddate']": '',
                "parameters['regionguid']": '610001',
                "parameters['projectcode']": '',
                "province": '',
                "parameters['purmethod']": ''
            }
            text = tool.requests_post(url_to.format(url), data, headers)
            detail = HTML(text).xpath('/html/body/div/table/tbody/tr')
            for li in detail:
                title = li.xpath('./td[3]/@title')[0]
                date_Today = li.xpath('./td[4]/text()')[0]
                url_ = li.xpath('./td[3]/a/@href')[0]
                if '测试' in title:
                    continue
                if tool.Transformation(date_Today) > tool.Transformation(self.date):
                    continue
                elif tool.Transformation(date_Today) == tool.Transformation(self.date):
                    ls.append(url_)
                else:
                    if len(url_list) == 0:
                        return [len(ls), ls]
                    else:
                        url = url_list.pop(0)
                        page = 0
                        break

    # 雄安新区公共资源网
    def hubei(self):
        print('雄安新区公共资源网', 'http://www.xaprtc.com')
        url_list = [
            'http://www.xaprtc.com/jyxxzc/index_{}.jhtml?token=d89e753d90084c08a6b7ea95bd5c61c0',
            'http://www.xaprtc.com/jyxxgc/index_{}.jhtml?token=34311e73bf7a464c8b350e0ff4e01301'
        ]
        headers = {
            'ajax-method': 'AjaxMethodFactory',
            # 'Cookie': 'ASP.NET_SessionId=irwyyayh3dtwq5zxunzlnq3x',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        }
        url = url_list.pop(0)
        page = 0
        ls = []
        while True:
            page += 1
            text = tool.requests_get(url.format(page), headers)
            detail = HTML(text).xpath("//div[@class='er-container']/ul/li")
            for li in detail:
                url_ = li.xpath("./div/a/@href")[0]
                title = li.xpath("./div/a/@title")[0]
                date_Today = li.xpath("./div/p/text()")[0]
                if '测试' in title:
                    continue
                if tool.Transformation(date_Today) > tool.Transformation(self.date):
                    continue
                elif tool.Transformation(date_Today) == tool.Transformation(self.date):
                    ls.append(url_)
                else:
                    if len(url_list) == 0:
                        return [len(ls), ls]
                    else:
                        url = url_list.pop(0)
                        page = 0
                        break

    # 青海公共资源交易网
    def binzhou(self):
        print('青海公共资源交易网', 'http://www.qhggzyjy.gov.cn')
        url_list = ['001001', '001002', '001003', '001004', '001005']
        headers = {
            'Cookie': 'Hm_lvt_776eb6c6b51e3da5075c361337f94338=1584946762,1586936167; TS0161614b=01761419df1159ee5d0dc3cd6f5029798f9f5622ce83a1a6b58545a766632b4b2c2ba8a9c608459776a8aa67978b0cd44c6b44f253; Hm_lpvt_776eb6c6b51e3da5075c361337f94338=1586936490',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        }
        url = url_list.pop(0)
        page = 0
        ls = []
        url_to = 'http://www.qhggzyjy.gov.cn/inteligentsearch/rest/inteligentSearch/getFullTextData'
        while True:
            page += 1
            data = {"token": "", "pn": page * 10 - 10, "rn": 10, "sdt": "", "edt": "", "wd": "", "inc_wd": "",
                    "exc_wd": "",
                    "fields": "title", "cnum": "001;002;003;004;005;006;007;008;009;010",
                    "sort": "{\"showdate\":\"0\"}",
                    "ssort": "title", "cl": 200, "terminal": "",
                    "condition": [{"fieldName": "categorynum", "isLike": True, "likeType": 2, "equal": url}],
                    "time": None, "highlights": "title", "statistics": None, "unionCondition": None, "accuracy": "100",
                    "noParticiple": "0", "searchRange": None, "isBusiness": 1}
            text = tool.requests_post_to(url_to, data, headers)
            detail = json.loads(text)['result']['records']
            for tr in detail:
                title = tr['title']
                date_Today = tr['infodate'][:10]
                url_ = 'http://www.qhggzyjy.gov.cn' + tr['linkurl']
                if '测试' in title:
                    continue
                if tool.Transformation(date_Today) > tool.Transformation(self.date):
                    continue
                elif tool.Transformation(date_Today) == tool.Transformation(self.date):
                    ls.append(url_)
                else:
                    if len(url_list) == 0:
                        return [len(ls), ls]
                    else:
                        url = url_list.pop(0)
                        page = 0
                        break

    # 黑龙江公共资源交易网    反应太慢
    def zhangzhou(self):
        print('黑龙江公共资源交易网', 'http://hljggzyjyw.gov.cn')
        url_list = ["16","18","19","20"]
        headers = {
            # 'Accept': 'application/json, text/javascript, */*; q=0.01',
            # 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            # 'Cookie': 'JSESSIONID=662863FD2199FBD1672A04A290868047; _CSRFCOOKIE=73F3D7A1BCDCA9001D7B1483A214C4E98DE2528B; EPTOKEN=73F3D7A1BCDCA9001D7B1483A214C4E98DE2528B; oauthClientId=demoClient; oauthPath=http://172.16.5.21:8080/EpointWebBuilder; oauthLoginUrl=http://172.16.5.21:8080/EpointWebBuilder/rest/oauth2/authorize?client_id=demoClient&state=a&response_type=code&scope=user&redirect_uri=; oauthLogoutUrl=http://172.16.5.21:8080/EpointWebBuilder/rest/oauth2/logout?redirect_uri=; noOauthRefreshToken=986d4fe7e5dd29b64c9e7b7a6d66e089; noOauthAccessToken=77c09e0bf98b6220b544961097eed84a; sub_domain_cokie=TiG5CMD9KQ41mmsARPTuAg%3D%3D; region_name=%E4%B9%8C%E9%B2%81%E6%9C%A8%E9%BD%90%E5%B8%82',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        }
        url = url_list.pop(0)
        page = 0
        ls = []
        url_to = 'http://hljggzyjyw.gov.cn/trade/tradezfcg?cid={}&pageNo={}&type=0&notice_name='
        while True:
            page += 1
            text = tool.requests_get(url_to.format(url, page), headers)
            print(text)
            detail = HTML(text).xpath('/html/body/div/div[2]/div[2]/div[3]/div/ul/li')
            for tr in detail:
                title = tr.xpath('./a/@title')[0]
                date_Today = tr.xpath('./span[3]/text()')[0]
                url_ = 'http://hljggzyjyw.gov.cn' + tr.xpath('./a/@href')[0]
                print(title)
                if '测试' in title:
                    continue
                if tool.Transformation(date_Today) > tool.Transformation(self.date):
                    continue
                elif tool.Transformation(date_Today) == tool.Transformation(self.date):
                    ls.append(url_)
                else:
                    if len(url_list) == 0:
                        return [len(ls), ls]
                    else:
                        url = url_list.pop(0)
                        page = 0
                        break

    # 黑龙江政府采购网
    def weifang(self):
        print('黑龙江政府采购网', 'http://www.hljcg.gov.cn')
        url_list = ["4", "30", "98", "5"]
        url = url_list.pop(0)
        page = 0
        ls = []
        url_to = 'http://www.hljcg.gov.cn/xwzs!queryGd.action'
        data = {
            'lbbh': '',
            'xwzsPage.zlbh': '',
            'id': '110'
        }
        data_to = {
            'xwzsPage.pageNo': '',
            'xwzsPage.pageSize': '20',
            'xwzsPage.pageCount': '1955',
            'lbbh': '',
            'xwzsPage.zlbh': '',
            'id': '110',
            'xwzsPage.LBBH': '',
            'xwzsPage.GJZ': ''
        }
        session = requests.session()
        while True:
            page += 1
            if page == 1:
                n = 0
                while True:
                    data['lbbh'] = url
                    tool.session_get('http://www.hljcg.gov.cn/welcome.jsp?dq=23', session)
                    text = tool.session_post(url_to, data, session)
                    if '没有记录' in text:
                        if n == 10:
                            return
                        print('cookie失效')
                        time.sleep(5)
                        tool.session_get('http://www.hljcg.gov.cn/welcome.jsp?dq=23', session)
                        n += 1
                        continue
                    break
            else:
                num = 0
                while True:
                    data_to['lbbh'] = url
                    data_to['wzsPage.LBBH'] = url
                    data_to['xwzsPage.pageNo'] = str(page)
                    text = tool.session_get(url_to, session)
                    if '没有记录' in text:
                        if num == 10:
                            return
                        print('cookie失效')
                        num += 1
                        tool.session_get('http://www.hljcg.gov.cn/welcome.jsp?dq=23')
                        continue
                    break
            detail = HTML(text).xpath('//*[@id="rightej"]/div[2]/div')
            for tr in detail:
                title = tr.xpath('./span[1]/a/text()')[0]
                date_Today = tr.xpath('./span[2]/text()')[0]
                url_ = 'http://www.hljcg.gov.cn' + re.findall("href='(.*?)';return", tr.xpath(
                    './span[1]/a/@onclick')[0])[0]
                if '测试' in title:
                    continue
                if tool.Transformation(date_Today) > tool.Transformation(self.date):
                    continue
                elif tool.Transformation(date_Today) == tool.Transformation(self.date):
                    ls.append(url_)
                else:
                    if len(url_list) == 0:
                        return [len(ls), ls]
                    else:
                        url = url_list.pop(0)
                        page = 0
                        break

    def parse(self):
        with open('../log/'+self.date+'.txt', 'r', encoding='utf-8') as r:
            url_ls = r.readlines()
        # 去掉换行符
        url_ls = [j.replace('\n', '') for j in url_ls]
        # 循环市级url列表
        for i in self.url_lss:
            # 该市级网站url列表
            num = i[0]()
            # 该市级本地url列表
            ls = []
            # 该市级网站没有抓取的url列表
            lss = []
            # 循环该市级本地url列表
            for j in url_ls:
                # 挑选该市级url
                if i[1] in j:
                    ls.append(j)
            # 循环该市级网站url列表
            for k in num[1]:
                # 查找该市级没有抓取到的招投标
                if k not in ls:
                    lss.append(k)
            print(self.date, '------网站：', num[0], '本地：', len(ls))
            print('该市级网站没有抓取的url:')
            [print(k) for k in lss]
            print('-' * 150)


if __name__ == '__main__':
    sp = spider()
    sp.parse()


