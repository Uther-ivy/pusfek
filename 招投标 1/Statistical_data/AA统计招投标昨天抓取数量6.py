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
            [self.sanming,'http://gzjy.smx.gov.cn'],
            [self.linxi, 'https://ciac.zjw.sh.gov.cn'],
            [self.leshan, 'http://www.shjzxh.org'],
            [self.yunan, 'http://www.sqggzy.com'],
            [self.neijiang, 'http://shanxi.365trade.com.cn'],
            [self.beijing, 'http://ztggzyjy.zt.gov.cn'],
            [self.nanjing, 'http://ggzy.shenyang.gov.cn'],
            [self.nanchong, 'https://www.szjsjy.com.cn:8001'],
            [self.nanping, 'http://www.szzfcg.cn'],
            [self.nanchang, 'http://szggzy.shuozhou.gov.cn'],
            [self.nantong, 'http://ggzy.siping.gov.cn'],
            [self.jian, 'http://www.taggzyjy.com.cn:8081'],
            [self.jilin, 'http://www.tzztb.com'],
            [self.jilinzf, 'http://www.tsjj.com.cn'],
            [self.jiayuguan, 'http://jyzx.trs.gov.cn'],
            [self.sichuan, 'https://wsggzy.cn'],
            [self.weihai, 'http://ggzy.wzzbtb.com:6081'],
            [self.anhui, 'http://www.whggzy.com'],
            # [self.yichun, 'http://xmzwggzy.xlgl.gov.cn'], 打不开
            [self.suqian, 'http://www.xxggzy.cn'],
            [self.bazhong, 'http://www.xyggzyjy.cn'],
            [self.changzhou, 'http://www.xsbnggzyjyxx.com'],
            [self.guangdong, 'http://ggzy.xuchang.gov.cn'],
            [self.guangdongzf, 'http://ggzy.yq.gov.cn'],
            [self.guangyuan, 'http://ccgp.yingkou.gov.cn'],
            [self.guangan, 'http://jyzx.yiyang.gov.cn'],
            [self.qingyang, 'http://ggzy.yzcity.gov.cn'],
            [self.zhangye, 'http://ggzy.yueyang.gov.cn'],
            [self.xuzhou, 'http://60.222.222.42'],
            [self.dezhou, 'http://www.yngp.com'],
            [self.chengdu, 'http://60.160.190.130:8001'],
            # [self.yangzhou, 'https://www.cnpcbidding.com'],
            # [self.panzhihua, 'http://ggzy.huaihua.gov.cn'], 打不开
            [self.xinyu, 'http://jyzx.zhoukou.gov.cn'],
            [self.wuxi, 'http://zsztb.zhoushan.gov.cn'],
            [self.rizhao, 'http://www.zmdggzy.gov.cn'],
            [self.zaozhuang, 'http://www.zzzyjy.cn'],
            [self.jiangsu, 'http://ggzyjy.zunyi.gov.cn'],
            # [self.jiangxi, 'http://ggzy.sheic.org.cn'],
            [self.taizhou, 'http://czj.dg.gov.cn'],
            [self.luzhou, 'http://ec.ccccltd.cn'],
            [self.hubei, 'http://www.ccgp.gov.cn'],
            [self.binzhou, 'https://buy.cnooc.com.cn'],
            [self.zhangzhou, 'https://ec.powerchina.cn'],
            [self.weifang, 'https://bidding.sinopec.com'],
            [self.yantai, 'http://www.365trade.com.cn'],
            [self.gansu, 'https://zjcs.yn.gov.cn'],
            # [self.baiyin, 'http://www.yilongjyzx.com'],  网站打不开
            [self.yancheng, 'http://www.ggzy.gov.cn/'],
            [self.meishan, 'http://ggzyjy.nmg.gov.cn'],
            [self.fuzhou, 'http://www.jlsjsxxw.com:20001'],
            # [self.liaocheng, 'http://www.sccin.com.cn'],
            [self.putian, 'http://www.ccgp-sichuan.gov.cn'],
            [self.xian, 'http://eps.sdic.com.cn'],
            [self.xizang, 'http://www.ccgp-tianjin.gov.cn'],
            [self.xizangzf, 'http://www.tjgdjt.com'],
            [self.dazhou, 'http://www.nxggzyjy.org'],
            [self.jinchang, 'http://ggzyjyzx.qdn.gov.cn'],
            [self.longnan, 'http://www.nbzfcg.cn'],
            [self.shanxi, 'http://www.ahggzyjt.com'],
            [self.yaan, 'http://ggzy.ah.gov.cn'],
            #　[self.longyan, 'http://www.ccgp-anhui.gov.cn']　网站打不开反应太慢
        ]

    # 三门峡市公共资源交易平台
    def sanming(self):
        print('三门峡市公共资源交易平台', 'http://gzjy.smx.gov.cn')
        url_list = [
            # 建设工程
            # 招标公告
            'http://gzjy.smx.gov.cn/spweb/SMX/TradeCenter/ColTableInfo.do?date=1month&begin_time=&end_time=&begin_time2='
            '&end_time2=&dealType=Deal_Type1&noticType=1+&huanJie=NOTICE&pageIndex={}',
            # 资格预审
            'http://gzjy.smx.gov.cn/spweb/SMX/TradeCenter/ColTableInfo.do?date=1month&begin_time=&end_time=&begin_time2='
            '&end_time2=&dealType=Deal_Type1&noticType=2+&huanJie=NOTICE&pageIndex={}',
            # 变更公告
            'http://gzjy.smx.gov.cn/spweb/SMX/TradeCenter/ColTableInfo.do?date=1month&begin_time=&end_time=&begin_time2='
            '&end_time2=&dealType=Deal_Type1&noticType=9-2&huanJie=NOTICE&pageIndex={}',
            # 结果公告
            'http://gzjy.smx.gov.cn/spweb/SMX/TradeCenter/ColTableInfo.do?date=1month&begin_time=&end_time=&begin_time2='
            '&end_time2=&dealType=Deal_Type1&noticType=RESULT_NOTICE&huanJie=NOTICE&pageIndex={}',
            # 政府采购
            # 采购公告
            'http://gzjy.smx.gov.cn/spweb/SMX/TradeCenter/ColTableInfo.do?date=1month&begin_time=&end_time=&begin_time2='
            '&end_time2=&dealType=Deal_Type4&noticType=NOTICE&huanJie=NOTICE&pageIndex={}',
            # 变更公告
            'http://gzjy.smx.gov.cn/spweb/SMX/TradeCenter/ColTableInfo.do?date=1month&begin_time=&end_time=&begin_time2='
            '&end_time2=&dealType=Deal_Type4&noticType=PUBLICITY-6&huanJie=NOTICE&pageIndex={}',
            # 结果公告
            'http://gzjy.smx.gov.cn/spweb/SMX/TradeCenter/ColTableInfo.do?date=1month&begin_time=&end_time=&begin_time2='
            '&end_time2=&dealType=Deal_Type4&noticType=RESULT_NOTICE&huanJie=NOTICE&pageIndex={}'
        ]
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        }
        url = url_list.pop(0)
        page = 0
        ls = []
        while True:
            page += 1
            text = '<table class="cui-table">' + tool.requests_get(url.format(page), headers) + '</table>'
            html = HTML(text)
            detail = html.xpath('//*[@class="cui-table"]/tr')
            for li in detail:
                try:
                    title = li.xpath('./td[2]/a/@title')[0]
                    url_ = 'http://gzjy.smx.gov.cn' + li.xpath('./td[2]/a/@href')[0]
                    date_Today = li.xpath('./td[3]/span/text()')[0].replace('\r', '').replace('\t', '').replace(' ',
                                                                                                                '').replace(
                        '\n', '')
                except:
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

    # 上海市建设工程交易服务中心
    def linxi(self):
        print('上海市建设工程交易服务中心', 'https://ciac.zjw.sh.gov.cn')
        url_list = [
             'https://ciac.zjw.sh.gov.cn/NetInterBidweb/GKTB/SgfbZbxx.aspx',
             'https://ciac.zjw.sh.gov.cn/XmZtbbaWeb/Gsqk/GsFbList.aspx',
        ]
        headers = {
            'Cookie': '_gscu_859717865=06285138rbcv4w59; AlteonP=AEcBbaXdHKxJXyA/5FhJEg$$; SsoCookierYzm=sjsv; wondersLog_zwdt_G_D_I=ee498f7112ef1975b078204349ec1b5b-2926; wondersLog_zwdt_sdk=%7B%22persistedTime%22%3A1614147940531%2C%22userId%22%3A%22%22%2C%22superProperties%22%3A%7B%22userType%22%3A2%7D%2C%22updatedTime%22%3A1614147941215%2C%22sessionStartTime%22%3A1614147941210%2C%22sessionReferrer%22%3A%22http%3A%2F%2Fgcls.sh.gov.cn%2F%22%2C%22deviceId%22%3A%22ee498f7112ef1975b078204349ec1b5b-2926%22%2C%22LASTEVENT%22%3A%7B%22eventId%22%3A%22wondersLog_pv%22%2C%22time%22%3A1614147941213%7D%2C%22sessionUuid%22%3A7948921178336179%2C%22costTime%22%3A%7B%7D%7D',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
        }
        url = url_list.pop(0)
        page = 0
        ls = []
        data = {
            '__EVENTTARGET': 'gvList',
            '__EVENTARGUMENT': 'Page$',
            '__VIEWSTATE': '1',
            '__VIEWSTATEGENERATOR': '17E6FEBA',
            '__EVENTVALIDATION': '3',
            'ddlZblx': '',
            'txtgsrq': '',
            'txtTogsrq': '',
            'txttbr': '',
            'txtzbhxr': '',
            'txtxmmc': '',
        }
        VIEWSTATE = ''
        EVENTVALIDATION = ''
        while True:
            print(url)
            page += 1
            if page == 1:
                text = tool.requests_get(url, headers)
                html = HTML(text)
            else:
                if 'SgfbZbxx' in url:
                    url_to = url + '?__EVENTTARGET=&__EVENTARGUMENT=&__VIEWSTATE={}&__VIEWSTATEGENERATOR=B423BA48&__EVENTVALIDATION={}&dr_gglb=0&dr_szqx=&txt_beginTime=&txt_endTime=&nextPages=%E4%B8%8B%E4%B8%80%E9%A1%B5&DropDownList_page={}&hdInputNum={}&hdPageCount=3&hdState='
                    text = tool.requests_get(url_to.format(requests.utils.quote(VIEWSTATE), requests.utils.quote(EVENTVALIDATION), str(page-1), str(page-1)), headers)
                    html = HTML(text)
                else:
                    text = tool.requests_post(url, data, headers)
                    html = HTML(text)
            if 'SgfbZbxx' in url:
                VIEWSTATE = html.xpath('//*[@id="__VIEWSTATE"]/@value')[0]
                EVENTVALIDATION = html.xpath('//*[@id="__EVENTVALIDATION"]/@value')[0]
                detail = html.xpath('//*[@id="form1"]/div[3]/table/tbody/tr/td/table[3]/tbody/tr')
            else:
                data['__EVENTARGUMENT'] = 'Page$' + str(page+1)
                data['__VIEWSTATE'] = html.xpath('//*[@id="__VIEWSTATE"]/@value')[0]
                data['__EVENTVALIDATION'] = html.xpath('//*[@id="__EVENTVALIDATION"]/@value')[0]
                detail = html.xpath('//*[@id="gvList"]/tr')
            for i in range(1, len(detail)):
                if 'SgfbZbxx' in url:
                    title = \
                    html.xpath('//*[@id="form1"]/div[3]/table/tbody/tr/td/table[3]/tbody/tr[{}]/td[2]/a/span/text()'
                               .format(i + 1))[0].replace('\n', '').replace('\r', '').replace('\t', '').replace(' ', '')
                    url_ = 'https://ciac.zjw.sh.gov.cn/NetInterBidweb/GKTB/DefaultV2019.aspx?gkzbXh={}'.format(
                        html.xpath('//*[@id="form1"]/div[3]/table/tbody/tr/td/table[3]/tbody/tr[{}]/td[2]/a/@onclick'
                                   .format(i + 1))[0].replace('openWindow(', '').replace(')', '').replace("'",
                                                                                                          '').split(
                            ',')[0])

                    date_Today = \
                    html.xpath('//*[@id="form1"]/div[3]/table/tbody/tr/td/table[3]/tbody/tr[{}]/td[3]/a/text()'
                               .format(i + 1))[0].replace('\n', '').replace('\r', '').replace('\t', '').replace(' ',
                                                                                                                '').replace(
                        '/', '-')
                else:
                    try:
                        title = html.xpath('//*[@id="gvList"]/tr[{}]/td[1]/a/text()'.format(i + 1))[0]
                        url_ = 'https://ciac.zjw.sh.gov.cn/XmZtbbaWeb/Gsqk/GsFb2015.aspx?zbdjid=&zbid={}&gsid=&gsmn=' \
                            .format(html.xpath('//*[@id="gvList"]/tr[{}]/td[1]/a/@onclick'.format(i + 1))[0]
                                    .replace('ShowGs(', '').replace(');', '').replace('"', '').split(',')[0])
                        date_Today = html.xpath('//*[@id="gvList"]/tr[{}]/td[2]/span/text()'.format(i + 1))[0] \
                            .replace('年', '-').replace('月', '-').replace('日', '')
                    except:
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

    # 上海市机电设备招标投标协会
    def leshan(self):
        print('上海市机电设备招标投标协会', 'http://www.shjzxh.org')
        url_list = [
            'http://www.shjzxh.org/list_2_265_{}.html'
        ]
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
            if page == 1:
                url = 'http://www.shjzxh.org/list_2_265.html'
            else:
                url = 'http://www.shjzxh.org/list_2_265_{}.html'.format(page)
            text = tool.requests_get(url, headers)
            html = HTML(text)
            detail = html.xpath('//*[@id="neirong"]/ul/li')
            for li in detail:
                title = li.xpath('./a/@title')[0]
                url_ = 'http://www.shjzxh.org/' + li.xpath('./a/@href')[0]
                date_Today = li.xpath('./a/span/text()')[0]
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

    # 商丘市公共资源交易平台
    def yunan(self):
        print('商丘市公共资源交易平台', 'https://ggzyjy.shangqiu.gov.cn')
        url_list = [
            'https://ggzyjy.shangqiu.gov.cn/spweb/HNSQ/TradeCenter/ColTableInfo.do?projectName=&date=1month&begin_time=&end_time=&begin_time2=&end_time2=&dealType=Deal_Type1&noticType=1+&area=&huanJie=NOTICE&pageIndex={}',
            'https://ggzyjy.shangqiu.gov.cn/spweb/HNSQ/TradeCenter/ColTableInfo.do?projectName=&date=1month&begin_time=&end_time=&begin_time2=&end_time2=&dealType=Deal_Type1&noticType=PUBLICITY&area=&huanJie=NOTICE&pageIndex={}',
            'https://ggzyjy.shangqiu.gov.cn/spweb/HNSQ/TradeCenter/ColTableInfo.do?projectName=&date=1month&begin_time=&end_time=&begin_time2=&end_time2=&dealType=Deal_Type1&noticType=RESULT_NOTICE&area=&huanJie=NOTICE&pageIndex={}',
            'https://ggzyjy.shangqiu.gov.cn/spweb/HNSQ/TradeCenter/ColTableInfo.do?projectName=&date=1month&begin_time=&end_time=&begin_time2=&end_time2=&dealType=Deal_Type1&noticType=WEB_JY_NOTICE&area=&huanJie=NOTICE&pageIndex={}',
            'https://ggzyjy.shangqiu.gov.cn/spweb/HNSQ/TradeCenter/ColTableInfo.do?projectName=&date=1month&begin_time=&end_time=&begin_time2=&end_time2=&dealType=Deal_Type4&noticType=NOTICE&area=&huanJie=NOTICE&pageIndex={}',
            'https://ggzyjy.shangqiu.gov.cn/spweb/HNSQ/TradeCenter/ColTableInfo.do?projectName=&date=1month&begin_time=&end_time=&begin_time2=&end_time2=&dealType=Deal_Type4&noticType=RESULT_NOTICE&area=&huanJie=NOTICE&pageIndex={}',
            'https://ggzyjy.shangqiu.gov.cn/spweb/HNSQ/TradeCenter/ColTableInfo.do?projectName=&date=1month&begin_time=&end_time=&begin_time2=&end_time2=&dealType=Deal_Type4&noticType=WEB_JY_NOTICE&area=&huanJie=NOTICE&pageIndex={}',
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
            detail = html.xpath('//tr')
            for li in detail[1:]:
                title = li.xpath('./td[2]/a/@title')[0]
                url_ = 'https://ggzyjy.shangqiu.gov.cn/' + li.xpath('./td[2]/a/@href')[0]
                date_Today = li.xpath('./td[3]/span[1]/text()')[0].replace('\n', '').replace(
                    '\t', '') \
                    .replace('\r', '').replace(' ', '').replace('发布时间:', '')
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

    # 中招联合（山西）招标采购网
    def neijiang(self):
        print('中招联合（山西）招标采购网', 'http://shanxi.365trade.com.cn')
        url_list = [
            # 招标公告
            'http://shanxi.365trade.com.cn/zbgg/index_{}.jhtml',
            # 变更
            'http://shanxi.365trade.com.cn/bggg/index_{}.jhtml',
            # 结果公告
            'http://shanxi.365trade.com.cn/jggs/index_{}.jhtml',
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
            detail = html.xpath('/html/body/div[2]/div/ul/li')
            for li in detail:
                title = li.xpath('./a[1]/p/span/@title')[0]
                url_ = 'http://shanxi.365trade.com.cn' + li.xpath('./a[2]/@href')[0]
                date_Today = li.xpath('./a[1]/i/text()')[0][5:]
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

    # 邵通市公共资源交易平台
    def beijing(self):
        print('邵通市公共资源交易平台', 'http://ztggzyjy.zt.gov.cn')
        url_list = [
            # 市本级
            #   工程建设
            #       招标公告
            ['http://ztggzyjy.zt.gov.cn/jyxx/jsgcZbgg?currentPage={}','//*[@id="zbggForm"]/div[3]/table/tr'],
            #       变更公告
            ['http://ztggzyjy.zt.gov.cn/jyxx/jsgcBgtz?currentPage={}','//*[@id="bgtzForm"]/div[2]/table/tr'],
            #       评标结果公示
            ['http://ztggzyjy.zt.gov.cn/jyxx/jsgcpbjggs?currentPage={}','//*[@id="zbggForm"]/div[2]/table/tr'],
            #       中标结果
            ['http://ztggzyjy.zt.gov.cn/jyxx/jsgcZbjggs?currentPage={}','//*[@id="zbggForm"]/div[3]/table/tr'],
            #       异常公告
            ['http://ztggzyjy.zt.gov.cn/jyxx/jsgcZbyc?currentPage={}','//*[@id="ycggForm"]/div[2]/table/tr'],
            #   政府采购
            #       采购公告
            ['http://ztggzyjy.zt.gov.cn/jyxx/zfcg/cggg?currentPage={}','//*[@id="zbggForm"]/div[2]/table/tr'],
            #       变更通知
            ['http://ztggzyjy.zt.gov.cn/jyxx/zfcg/gzsx?currentPage={}','//*[@id="zbggForm"]/div[2]/table/tr'],
            #       结果公示
            ['http://ztggzyjy.zt.gov.cn/jyxx/zfcg/zbjggs?currentPage={}','//*[@id="zbggForm"]/div[2]/table/tr'],
            #       异常公示
            ['http://ztggzyjy.zt.gov.cn/jyxx/zfcg/zfcgYcgg?currentPage={}','//*[@id="ycggForm"]/div[2]/table/tr']
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
            text = tool.requests_get(url[0].format(page), headers)
            html = HTML(text)
            detail = html.xpath(url[1])
            for i in range(1, len(detail)):
                try:
                    title = html.xpath(url[1] + '[{}]/td[3]/a/@title'.format(i + 1))[0]
                    url_ = 'http://ztggzyjy.zt.gov.cn' + html.xpath(url[1] + '[{}]/td[3]/a/@href'.format(i + 1))[0]
                    date_Today = html.xpath(url[1] + '[{}]/td[4]/text()'.format(i + 1))[0]
                    if '招标' in date_Today or '采购' in date_Today:
                        date_Today = html.xpath(url[1] + '[{}]/td[5]/text()'.format(i + 1))[0]
                    if title == '':
                        title = html.xpath(url[1] + '[{}]/td[3]/@title'.format(i + 1))[0]
                except:
                    title = html.xpath(url[1] + '[{}]/td[4]/a/@title'.format(i + 1))[0]
                    url_ = 'http://ztggzyjy.zt.gov.cn' + html.xpath(url[1] + '[{}]/td[4]/a/@href'.format(i + 1))[0]
                    date_Today = html.xpath(url[1] + '[{}]/td[5]/text()'.format(i + 1))[0]
                    if title == '':
                        title = html.xpath(url[1] + '[{}]/td[4]/@title'.format(i + 1))[0]
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

    # 沈阳市公共资源交易平台
    def nanjing(self):
        print('沈阳市公共资源交易平台', 'http://ggzy.shenyang.gov.cn')
        url_list = [
            'http://ggzy.shenyang.gov.cn/jyxxgcjs/index_{}.jhtml',
            'http://ggzy.shenyang.gov.cn/jyxxzfcg/index_{}.jhtml'
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
            html = HTML(text)
            detail = html.xpath('/html/body/div/div[2]/div[3]/div/ul/li')
            for li in detail:
                title = li.xpath('./div/a/text()')[0]
                url_ = li.xpath('./div/a/@href')[0]
                date_Today = li.xpath('./div/div/text()')[0]
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

    # 深圳市住房和建设局
    def nanchong(self):
        print('深圳市住房和建设局', 'https://www.szjsjy.com.cn:8001')
        url_list = [
            # 招标公告
            'https://www.szjsjy.com.cn:8001/jyw/queryGongGaoList.do?rows=10&page={}',
            # 定标结果
            'https://www.szjsjy.com.cn:8001/jyw/queryDBJieGuoList.do?rows=10&page={}',
            # 中标公告
            'https://www.szjsjy.com.cn:8001/jyw/queryZBJieGuoList.do?rows=10&page={}',
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
            text = tool.requests_get(url.format(page), headers).replace('var gongGaoList=', '').replace(
                'var dbList=', '').replace('var zbList=', '')[:-1]
            detail = json.loads(text)['rows']
            for i in detail:
                if 'GongGao' in url:
                    title = i['gcName']
                    url_ = 'https://www.szjsjy.com.cn:8001/jyw/showGongGao.do?ggGuid={}&gcbh=&bdbhs='.format(i['ggGuid'])
                    date_Today = i['ggStartTime2'].replace('"', '')[:10]
                elif 'DBJieGuo' in url:
                    url_ = 'https://www.szjsjy.com.cn:8001/jyw/queryDbJieGuoByGuid.do?guid={}'.format(i['dbJieGuoGuid'])
                    title = i['bdName']
                    date_Today = i['createTime2'].replace('"', '')[:10]
                elif 'ZBJieGuo' in url:
                    url_ = 'https://www.szjsjy.com.cn:8001/jyw/queryZbgs.do?guid={}&ggGuid=&bdGuid='.format(
                        i['dbZhongBiaoJieGuoGuid'])
                    title = i['bdName']
                    date_Today = i['fabuTime2'].replace('"', '')[:10]
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

    # 深圳市政府采购中心
    def nanping(self):
        print('深圳市政府采购中心', 'http://www.szzfcg.cn')
        url_list = [
            'http://www.szzfcg.cn/portal/topicView.do?method=view&id=1660',
            'http://www.szzfcg.cn/portal/topicView.do?method=view&id=201901',
            'http://www.szzfcg.cn/portal/topicView.do?method=view&id=2014',
            'http://www.szzfcg.cn/portal/topicView.do?method=view&id=201911']
        headers = {
            'Cookie': 'zh_choose=n; _gscu_375154715=78462920k1peom21; _trs_uv=k54w2gs3_2380_dkza; pgv_pvi=7955464192; pgv_si=s3740718080; _gscbrs_375154715=1; _trs_ua_s_1=k56fo9sc_2380_2pvf; _gscs_375154715=78556317ftoe7i21|pv:10',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
        }
        url = url_list.pop(0)
        page = 0
        ls = []
        while True:
            page += 1
            data = {
                'ec_i': 'topicChrList_20070702',
                'topicChrList_20070702_crd': '20',
                'topicChrList_20070702_f_a': '',
                'topicChrList_20070702_p': str(page),
                'topicChrList_20070702_s_siteId': '',
                'topicChrList_20070702_s_name': '',
                'topicChrList_20070702_s_speciesCategory': '',
                'id': '1660',
                'method': 'view',
                '__ec_pages': '1',
                'topicChrList_20070702_rd': '20',
                'topicChrList_20070702_f_name': '',
                'topicChrList_20070702_f_speciesCategory': '',
                'topicChrList_20070702_f_ldate': ''
            }
            text = tool.requests_post(url, data, headers)
            html = HTML(text)
            detail = html.xpath('//*[@id="topicChrList_20070702_table"]/tbody/tr')
            for tr in detail:
                url_ = 'http://www.szzfcg.cn/portal/documentView.do?method=view&id=' + tr.xpath('./td[3]/a/@href')[0] \
                    .replace('/viewer.do?id=', '')
                title = tr.xpath('./td[3]/a/text()')[0]
                date_Today = tr.xpath('./td[5]/text()')[0][:10]
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

    # 朔州市公共资源交易信息网
    def nanchang(self):
        print('朔州市公共资源交易信息网', 'http://szggzy.shuozhou.gov.cn')
        url_list = [
            'http://szggzy.shuozhou.gov.cn/moreInfoController.do?getMoreNoticeInfo&page={}&rows=10&dateFlag=&tableName=&projectRegion=&projectName=&beginReceivetime=&endReceivetime=',
            'http://szggzy.shuozhou.gov.cn/moreInfoController.do?getMoreResultNoticeInfo&page={}&rows=10&dateFlag=&tableName=&projectRegion=&projectName=&beginReceivetime=&endReceivetime='
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
            detail = json.loads(text)['obj']
            for li in detail:
                try:
                    title = li['PROJECTNAME']
                except:
                    title = li['PROJECT_NAME']
                try:
                    if 'noticeDetail' in li['HTTP_URL']:
                        code = 'getNoticeDetail'
                    else:
                        code = 'getResultNoticeDetail'
                except:
                    if 'noticeDetail' in li['HTTPURL']:
                        code = 'getNoticeDetail'
                    else:
                        code = 'getResultNoticeDetail'
                url_ = 'http://szggzy.shuozhou.gov.cn/moreInfoController.do?{}&url={}&id={}'.format(code, li['URL'],
                                                                                                   li['ID'])
                try:
                    date_Today = li['RECEIVETIME']
                except:
                    date_Today = tool.Time_stamp_to_date(int(str(li['RECEIVE_TIME'])[:-3]))
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

    # 四平市公共资源交易中心
    def nantong(self):
        print('四平市公共资源交易中心', 'http://ggzy.siping.gov.cn')
        url_list = [
            # 建设工程
            'http://ggzy.siping.gov.cn/jyxx/004001/{}.html',
            # 政府采购
            'http://ggzy.siping.gov.cn/jyxx/004002/{}.html'
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
                text = tool.requests_get(url.format('about'), headers)
            else:
                text = tool.requests_get(url.format(page), headers)
            html = HTML(text)
            detail = html.xpath('/html/body/div[2]/div/div[2]/div[2]/div/div[2]/ul/li')
            for li in detail:
                title = li.xpath('./div/a/text()')[0]
                url_ = 'http://ggzy.siping.gov.cn' + li.xpath('./div/a/@href')[0]
                date_Today = li.xpath('./span/text()')[0]
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

    # 泰安市公共资源交易平台
    def jian(self):
        print('泰安市公共资源交易平台', 'http://www.taggzyjy.com.cn:8081')
        url_list = [
           'http://www.taggzyjy.com.cn:8081/jydt/{}.html'
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
                text = tool.requests_get(url.format('moreinfojy'), headers)
            else:
                text = tool.requests_get(url.format(page), headers)
            html = HTML(text)
            detail = html.xpath('//*[@id="infoContent"]/li')
            for li in detail:
                title = li.xpath('./a/@title')[0]
                url_ = 'http://www.taggzyjy.com.cn:8081' + \
                      li.xpath('./a/@href')[0]
                date_Today = li.xpath('./span/text()')[0].replace(
                    '[', '').replace(']', '')
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

    # 台州市公共资源交易平台
    def jilin(self):
        print('台州市公共资源交易平台', 'http://www.tzztb.com')
        url_list = [
            # 市本级
            #   建设工程
            #       招标公告
            'http://www.tzztb.com/tzcms/gcjyzhaobgg/index_{}.htm',
            #       中标候选人
            'http://www.tzztb.com/tzcms/gcjyzbgg/index_{}.htm?loca=1&xiaoe=1&type=4',
            #       中标结果
            'http://www.tzztb.com/tzcms/gcjyzbjg/index_{}.htm?loca=1&xiaoe=1&type=5',
            #   政府采购
            #       采购公告
            'http://www.tzztb.com/tzcms/zfcg/index_{}.htm',
            #       中标公示
            'http://www.tzztb.com/tzcms/zfcgzbhxgs/index_{}.htm?loca=1&xiaoe=1&type=3',
            # 临海市
            #   建设工程
            #       招标公告
            'http://www.tzztb.com/tzcms/lhxjsgc/index_{}.htm?loca=2&xiaoe=1&type=1',
            #       中标结果
            'http://www.tzztb.com/tzcms/zbgglhxjsgc/index_{}.htm?loca=2&xiaoe=1&type=5',
            #   政府采购
            #       采购公告
            'http://www.tzztb.com/tzcms/lhxzfcg/index_{}.htm?loca=2&xiaoe=1&type=1',
            #       中标公示
            'http://www.tzztb.com/tzcms/zbgglhxzfcg/index_{}.htm?loca=2&xiaoe=1&type=3',
            # 温岭市
            'http://www.tzztb.com/tzcms/wlxjsgc/index_{}.htm?loca=3&xiaoe=1&type=1',
            'http://www.tzztb.com/tzcms/pbgswlxjsgc/index_{}.htm?loca=3&xiaoe=1&type=4',
            'http://www.tzztb.com/tzcms/zbggwlxjsgc/index_{}.htm?loca=3&xiaoe=1&type=5',
            'http://www.tzztb.com/tzcms/wlxzfcg/index_{}.htm?loca=3&xiaoe=1&type=1',
            'http://www.tzztb.com/tzcms/zbggwlxzfcg/index_{}.htm?loca=3&xiaoe=1&type=3',
            # 玉环市
            'http://www.tzztb.com/tzcms/zbggyhxjsgc/index_{}.htm?loca=4&xiaoe=1&type=5',
            'http://www.tzztb.com/tzcms/yhxzfcg/index_{}.htm?loca=4&xiaoe=1&type=1',
            'http://www.tzztb.com/tzcms/zbggyhxzfcg/index_{}.htm?loca=4&xiaoe=1&type=3',
            # 天台县
            'http://www.tzztb.com/tzcms/ttxjsgc/index_{}.htm?loca=5&xiaoe=1&type=1',
            'http://www.tzztb.com/tzcms/pbgsttxjsgc/index_{}.htm?loca=5&xiaoe=1&type=4',
            'http://www.tzztb.com/tzcms/zbggttxjsgc/index_{}.htm?loca=5&xiaoe=1&type=5',
            'http://www.tzztb.com/tzcms/ttxzfcg/index_{}.htm?loca=5&xiaoe=1&type=1',
            'http://www.tzztb.com/tzcms/zbggttxzfcg/index_{}.htm?loca=5&xiaoe=1&type=3',
            # 仙居县
            'http://www.tzztb.com/tzcms/xjxjsgc/index_{}.htm?loca=6&xiaoe=1&type=1',
            'http://www.tzztb.com/tzcms/zbggxjxjsgc/index_{}.htm?loca=6&xiaoe=1&type=5',
            'http://www.tzztb.com/tzcms/xjxzfcg/index_{}.htm?loca=6&xiaoe=1&type=1',
            'http://www.tzztb.com/tzcms/zbggxjxzfcg/index_{}.htm?loca=6&xiaoe=1&type=3',
            # 三门县
            'http://www.tzztb.com/tzcms/smxjsgc/index_{}.htm?loca=7&xiaoe=1&type=1',
            'http://www.tzztb.com/tzcms/pbgssmxjsgc/index_{}.htm?loca=7&xiaoe=1&type=4',
            'http://www.tzztb.com/tzcms/zbggsmxjsgc/index_{}.htm?loca=7&xiaoe=1&type=5',
            'http://www.tzztb.com/tzcms/smxzfcg/index_{}.htm?loca=7&xiaoe=1&type=1',
            'http://www.tzztb.com/tzcms/zbggsmxzfcg/index_{}.htm?loca=7&xiaoe=1&type=3'
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
            detail = html.xpath('/html/body/div[2]/div[1]/ul/li/table/tr')
            for li in detail[1:]:
                title = li.xpath('./td[2]/a/span/text()')[0]
                url_ = 'http://www.tzztb.com' + li.xpath('./td[2]/a/@href')[0]
                date_Today = li.xpath('./td[4]/text()')[0]
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

    # 天津水务有形市场 
    def jilinzf(self):
        print('天津水务有形市场', 'http://www.tsjj.com.cn')
        url_list = [
            # 招标公告
            'http://www.tsjj.com.cn/Portals/TSJJ/PageTwoColumn?qbJcVsCVAUztN3aGgCAlMQ%3d%3d',
            # 公示
            'http://www.tsjj.com.cn/Portals/TSJJ/PageTwoColumn?9lOQzqgtkKLUWohla1MzjA%3d%3d'
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
            '__EVENTTARGET': 'ctl00$ctl00$ctl00$CPH_PeakPane$CPH_MainPane$CPH_ContentPane$ctl00$PaginationBar1$T5',
            '__EVENTARGUMENT': '',
            '__LASTFOCUS': '',
            '__VIEWSTATE': "",
            '__VIEWSTATEGENERATOR': '2',
            '__EVENTVALIDATION': '3',
            'ctl00$ctl00$ctl00$CPH_PeakPane$hdSearchRange': '',
            'ctl00$ctl00$ctl00$CPH_PeakPane$txtKeywords': '',
            'ctl00$ctl00$ctl00$CPH_PeakPane$CPH_MainPane$CPH_ContentPane$ctl00$returl': '',
            'ctl00$ctl00$ctl00$CPH_PeakPane$CPH_MainPane$CPH_ContentPane$ctl00$PaginationBar1$ctl01': str(page - 1),
            'ctl00$ctl00$ctl00$CPH_PeakPane$CPH_MainPane$CPH_ContentPane$ctl00$PaginationBar1$_PageSize': '20'
        }
        while True:
            page += 1
            if page == 1:
                rst = tool.requests_get(url, headers)
                html = HTML(rst)
            else:
                rst = tool.requests_post(url, data, headers)
                html = HTML(rst)
            data['__VIEWSTATEGENERATOR'] = html.xpath('//*[@id="__VIEWSTATEGENERATOR"]/@value')[0]
            data['__EVENTVALIDATION'] = html.xpath('//*[@id="__EVENTVALIDATION"]/@value')[0]
            data['__VIEWSTATE'] = html.xpath('//*[@id="__VIEWSTATE"]/@value')[0]
            detail = html.xpath('//*[@id="form1"]/div[3]/div[2]/div/div[2]/table/tr/td/div[1]/ul/li')
            for li in detail:
                title = li.xpath('./a/@title')[0]
                url_ = 'http://www.tsjj.com.cn' + li.xpath('./a/@href')[0]
                date_Today = li.xpath('./a/span/text()')[0]
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

    # 铜仁市公共资源交易平台
    def jiayuguan(self):
        print('铜仁市公共资源交易平台', 'http://jyzx.trs.gov.cn')
        url_list = [
            # 市本级
            #   工程建设
            #       招标公告
            'http://jyzx.trs.gov.cn/gcjs/zbgg/index.html',
            #       中标公示
            'http://jyzx.trs.gov.cn/gcjs/zbjggg/index.html',
            #       中标候选人
            'http://jyzx.trs.gov.cn/gcjs/zbgs/index.html',
            #       更正公告
            'http://jyzx.trs.gov.cn/gcjs/bggg/index.html',
            #       流标公告
            'http://jyzx.trs.gov.cn/gcjs/lbgs/index.html',
            #   政府采购
            #       采购公告
            'http://jyzx.trs.gov.cn/zfcg/cgxqgs/index.html',
            #       中标公告
            'http://jyzx.trs.gov.cn/zfcg/jggszgysjggs/index.html',
            #       更正公告
            'http://jyzx.trs.gov.cn/zfcg/bggg_5230297/index.html',
            #       流标公告
            'http://jyzx.trs.gov.cn/zfcg/fbgg/index.html'
        ]
        headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Cookie': 'JSESSIONID=662863FD2199FBD1672A04A290868047; _CSRFCOOKIE=73F3D7A1BCDCA9001D7B1483A214C4E98DE2528B; EPTOKEN=73F3D7A1BCDCA9001D7B1483A214C4E98DE2528B; oauthClientId=demoClient; oauthPath=http://172.16.5.21:8080/EpointWebBuilder; oauthLoginUrl=http://172.16.5.21:8080/EpointWebBuilder/rest/oauth2/authorize?client_id=demoClient&state=a&response_type=code&scope=user&redirect_uri=; oauthLogoutUrl=http://172.16.5.21:8080/EpointWebBuilder/rest/oauth2/logout?redirect_uri=; noOauthRefreshToken=986d4fe7e5dd29b64c9e7b7a6d66e089; noOauthAccessToken=77c09e0bf98b6220b544961097eed84a; sub_domain_cokie=TiG5CMD9KQ41mmsARPTuAg%3D%3D; region_name=%E4%B9%8C%E9%B2%81%E6%9C%A8%E9%BD%90%E5%B8%82',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',

        }
        url = url_list.pop(0)
        ls = []
        while True:
            text = tool.requests_get(url, headers)
            trsItemCount = int(re.findall('var trsItemCount = (.*?); // 总条数', text, re.S)[0])
            while True:
                url_to = url.replace('index.html', '') + '{}/{}.json?v={}'.format(int(trsItemCount/100), trsItemCount, str(time.time()).replace('.', '')[:13])
                detail = json.loads(tool.requests_get(url_to, headers))
                title = detail['DOCTITLE']
                url_ = detail['SOURCELINK']
                date_Today = detail['DOCRELTIME']
                if '测试' in title:
                    continue
                if tool.Transformation(date_Today) > tool.Transformation(self.date):
                    trsItemCount -= 1
                    continue
                elif tool.Transformation(date_Today) == tool.Transformation(self.date):
                    ls.append(url_)
                    trsItemCount -= 1
                    continue
                else:
                    if len(url_list) == 0:
                        return [len(ls), ls]
                    else:
                        url = url_list.pop(0)
                        break

    # 文山州公共资源交易平台
    def sichuan(self):
        print('文山州公共资源交易平台', 'https://wsggzy.cn')
        url_list = [
            # 市本级
            #   工程建设
            #       招标公告
            ['https://wsggzy.cn/jyxx/jsgcZbgg?currentPage={}','//*[@id="zbggForm"]/div[3]/table/tr'],
            #       变更公告
            ['https://wsggzy.cn/jyxx/jsgcBgtz?currentPage={}','//*[@id="bgtzForm"]/div[2]/table/tr'],
            #       评标结果公示
            ['https://wsggzy.cn/jyxx/jsgcpbjggs?currentPage={}','//*[@id="zbggForm"]/div[2]/table/tr'],
            #       中标结果
            ['https://wsggzy.cn/jyxx/jsgcZbjggs?currentPage={}','//*[@id="zbggForm"]/div[3]/table/tr'],
            #       异常公告
            ['https://wsggzy.cn/jyxx/jsgcZbyc?currentPage={}','//*[@id="ycggForm"]/div[2]/table/tr'],
            #   政府采购
            #       采购公告
            ['https://wsggzy.cn/jyxx/zfcg/cggg?currentPage={}','//*[@id="zbggForm"]/div[2]/table/tr'],
            #       变更通知
            ['https://wsggzy.cn/jyxx/zfcg/gzsx?currentPage={}','//*[@id="zbggForm"]/div[2]/table/tr'],
            #       结果公示
            ['https://wsggzy.cn/jyxx/zfcg/zbjggs?currentPage={}','//*[@id="zbggForm"]/div[2]/table/tr'],
            #       异常公示
            ['https://wsggzy.cn/jyxx/zfcg/zfcgYcgg?currentPage={}','//*[@id="ycggForm"]/div[2]/table/tr']
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
            text = tool.requests_get(url[0].format(page), headers)
            html = HTML(text)
            detail = html.xpath(url[1])
            for i in range(1, len(detail)):
                try:
                    title = html.xpath(url[1] + '[{}]/td[3]/a/@title'.format(i + 1))[0]
                    url_ = 'https://wsggzy.cn' + html.xpath(url[1] + '[{}]/td[3]/a/@href'.format(i + 1))[0]
                    date_Today = html.xpath(url[1] + '[{}]/td[4]/text()'.format(i + 1))[0]
                    if '招标' in date_Today or '采购' in date_Today:
                        date_Today = html.xpath(url[1] + '[{}]/td[5]/text()'.format(i + 1))[0]
                    if title == '':
                        title = html.xpath(url[1] + '[{}]/td[3]/@title'.format(i + 1))[0]
                except:
                    title = html.xpath(url[1] + '[{}]/td[4]/a/@title'.format(i + 1))[0]
                    url_ = 'https://wsggzy.cn' + html.xpath(url[1] + '[{}]/td[4]/a/@href'.format(i + 1))[0]
                    date_Today = html.xpath(url[1] + '[{}]/td[5]/text()'.format(i + 1))[0]
                    if title == '':
                        title = html.xpath(url[1] + '[{}]/td[4]/@title'.format(i + 1))[0]
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

    # 温州市公共资源交易平台
    def weihai(self):
        print('温州市公共资源交易平台', 'http://ggzy.wzzbtb.com:6081')
        url_list = [
            # 政府采购
            # 采购公告
            'http://ggzy.wzzbtb.com:6081/wzcms/zfcgcggg/index_{}.htm',
            # 中标公告
            'http://ggzy.wzzbtb.com:6081/wzcms/zfcgzbgg/index_{}.htm'
        ]
        headers = {
            'Authorization': 'Bearer d084915340e388896b5724c69c43d5a3',
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
            detail = html.xpath('/html/body/div[2]/div[3]/div/div[2]/ul/li')
            for li in detail:
                title = li.xpath('./a/@title')[0]
                url_ = 'http://ggzy.wzzbtb.com:6081' + li.xpath('./a/@href')[0]
                date_Today = li.xpath('./span/text()')[0]
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

    # 乌海市公告资源交易中心
    def anhui(self):
        print('乌海市公告资源交易中心', 'http://www.whggzy.com')
        url_list = [
            # 招标公告
            'ZcyAnnouncement11',
            # 招标变更
            'ZcyAnnouncement12',
            # 单一来源
            'ZcyAnnouncement13',
            # 中标公告
            'ZcyAnnouncement14',
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
            data = {
                'categoryCode': url,
                'pageNo': str(page),
                'pageSize': '15',
                'utm': "sites_group_front.2ef5001f.0.0.df31198031b511ea82280161e58e2c92"
            }
            url_to = 'http://www.whggzy.com/front/search/category'
            text = tool.requests_post_to(url_to, data, headers)
            detail = json.loads(text)['hits']['hits']
            for i in detail:
                title = i['_source']['title']
                url_ = 'http://www.whggzy.com' + i['_source']['url']
                date_Today = tool.Time_stamp_to_date(int(str(i['_source']['publishDate'])[:-3]))
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

    # 锡林郭勒盟公共资源  打不开
    def yichun(self):
        print('锡林郭勒盟公共资源', 'http://xmzwggzy.xlgl.gov.cn')
        url_list = [
            # 建设工程
                # 招标公告
            'http://xmzwggzy.xlgl.gov.cn/xmweb/ggzyjy/009001/009001005/009001005001/MoreInfo.aspx?CategoryNum=009001005001',
                # 招标变更
            'http://xmzwggzy.xlgl.gov.cn/xmweb/ggzyjy/009001/009001005/009001005005/MoreInfo.aspx?CategoryNum=009001005005',
                # 中标公告
            'http://xmzwggzy.xlgl.gov.cn/xmweb/ggzyjy/009001/009001005/009001005004/MoreInfo.aspx?CategoryNum=009001005004',
            # 政府采购
                # 招标公告
            'http://xmzwggzy.xlgl.gov.cn/xmweb/ggzyjy/009002/009002006/009002006001/MoreInfo.aspx?CategoryNum=009002006001',
                # 招标变更
            'http://xmzwggzy.xlgl.gov.cn/xmweb/ggzyjy/009002/009002006/009002006004/MoreInfo.aspx?CategoryNum=009002006004',
                # 废标公示
            'http://xmzwggzy.xlgl.gov.cn/xmweb/ggzyjy/009002/009002006/009002006003/MoreInfo.aspx?CategoryNum=009002006003',
                # 中标公告
            'http://xmzwggzy.xlgl.gov.cn/xmweb/ggzyjy/009002/009002006/009002006002/MoreInfo.aspx?CategoryNum=009002006002'
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
            '__VIEWSTATE': '',
            '__VIEWSTATEGENERATOR': '',
            '__EVENTTARGET': 'MoreInfoList1$Pager',
            '__EVENTARGUMENT': '',
            '__VIEWSTATEENCRYPTED': ''
        }
        while True:
            page += 1
            if page == 1:
                text = tool.requests_get(url, headers)
            else:
                print(111,data)
                time.sleep(666)
                text = tool.requests_post(url, data, headers)
            html = HTML(text)
            data['__VIEWSTATE'] = html.xpath('//*[@id="__VIEWSTATE"]/@value')[0]
            data['__VIEWSTATEGENERATOR'] = html.xpath('//*[@id="__VIEWSTATEGENERATOR"]/@value')[0]
            data['__EVENTARGUMENT'] = page + 1
            detail = html.xpath('//*[@id="MoreInfoList1_DataGrid1"]/tr')
            for i in range(0, len(detail), 2):
                title = html.xpath('//*[@id="MoreInfoList1_DataGrid1"]/tr[{}]/td[2]/a/@title'.format(i + 1))[0]
                url_ = 'http://xmzwggzy.xlgl.gov.cn' + \
                      html.xpath('//*[@id="MoreInfoList1_DataGrid1"]/tr[{}]/td[2]/a/@href'.format(i + 1))[0]
                date_Today = html.xpath('//*[@id="MoreInfoList1_DataGrid1"]/tr[{}]/td[3]/text()'.format(i + 1))[0] \
                    .replace('\r', '').replace('\t', '').replace('\n', '').replace(' ', '')
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

    # 新乡市公共资源交易平台
    def suqian(self):
        print('新乡市公共资源交易平台', 'http://www.xxggzy.cn')
        url_list = [
            # 政府采购
            # 公告信息
            'http://www.xxggzy.cn/jyxx/089004/089004001/{}.html',
            # 变更公告
            'http://www.xxggzy.cn/jyxx/089004/089004002/{}.html',
            # 结果公示
            'http://www.xxggzy.cn/jyxx/089004/089004003/{}.html',
            # 建设工程
            # 公告信息
            'http://www.xxggzy.cn/jyxx/089003/089003001/{}.html',
            # 变更公告
            'http://www.xxggzy.cn/jyxx/089003/089003002/{}.html',
            # 中标候选人
            'http://www.xxggzy.cn/jyxx/089003/089003011/{}.html',
            # 结果公示
            'http://www.xxggzy.cn/jyxx/089003/089003003/{}.html'
        ]
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36',
        }
        url = url_list.pop(0)
        page = 0
        ls = []
        while True:
            page += 1
            text = tool.requests_get(url.format(page), headers)
            if page == 1:
                text = tool.requests_get(url.format('moreinfo_len6'), headers)
            html = HTML(text)
            detail = html.xpath('//*[@class="ewb-info-items"]/li')
            for li in detail:
                title = li.xpath('./a/@title')[0]
                url_ = 'http://www.xxggzy.cn' + li.xpath('./a/@href')[0]
                date_Today = li.xpath('./span/text()')[0].replace('\r', '').replace('\t', '').replace(' ', '').replace(
                    '\n', '')
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

    # 信阳市公共资源交易平台
    def bazhong(self):
        print('信阳市公共资源交易平台', 'http://www.xyggzyjy.cn')
        url_list = [
            # 建设工程
            # 招标公告
            'http://www.xyggzyjy.cn/jyxx/002001/002001001/{}.html',
            # 变更公告
            'http://www.xyggzyjy.cn/jyxx/002001/002001002/{}.html',
            # 中标结果
            'http://www.xyggzyjy.cn/jyxx/002001/002001003/{}.html',
            # 政府采购
            # 采购公告
            'http://www.xyggzyjy.cn/jyxx/002002/002002001/{}.html',
            # 变更公告
            'http://www.xyggzyjy.cn/jyxx/002002/002002002/{}.html',
            # 中标结果
            'http://www.xyggzyjy.cn/jyxx/002002/002002003/{}.html'
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
                text = tool.requests_get(url.format('moreinfo'), headers)
            else:
                text = tool.requests_get(url.format(page), headers)
            html = HTML(text)
            detail = html.xpath('//*[@id="showList"]/li')
            for li in detail:
                title = li.xpath('./span[2]/a/text()')[0]
                url_ = 'http://www.xyggzyjy.cn' + li.xpath('./span[2]/a/@href')[0]
                date_Today = li.xpath('./span[1]/text()')[0].replace('\n', '').replace('\t', '').replace('\r', '') \
                    .replace(' ', '').replace('[', '').replace(']', '')
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

    # 西双版纳州公共资源交易平台
    def changzhou(self):
        print('西双版纳州公共资源交易平台', 'http://www.xsbnggzyjyxx.com')
        url_list = [
            # 市本级
            #   工程建设
            #       招标公告
            ['http://www.xsbnggzyjyxx.com/jyxx/jsgcZbgg?currentPage={}','//*[@id="zbggForm"]/div[3]/table/tr'],
            #       变更公告
            ['http://www.xsbnggzyjyxx.com/jyxx/jsgcBgtz?currentPage={}','//*[@id="bgtzForm"]/div[2]/table/tr'],
            #       评标结果公示
            ['http://www.xsbnggzyjyxx.com/jyxx/jsgcpbjggs?currentPage={}','//*[@id="zbggForm"]/div[2]/table/tr'],
            #       中标结果
            ['http://www.xsbnggzyjyxx.com/jyxx/jsgcZbjggs?currentPage={}','//*[@id="zbggForm"]/div[3]/table/tr'],
            #       异常公告
            ['http://www.xsbnggzyjyxx.com/jyxx/jsgcZbyc?currentPage={}','//*[@id="ycggForm"]/div[2]/table/tr'],
            #   政府采购
            #       采购公告
            ['http://www.xsbnggzyjyxx.com/jyxx/zfcg/cggg?currentPage={}','//*[@id="zbggForm"]/div[2]/table/tr'],
            #       变更通知
            ['http://www.xsbnggzyjyxx.com/jyxx/zfcg/gzsx?currentPage={}','//*[@id="zbggForm"]/div[2]/table/tr'],
            #       结果公示
            ['http://www.xsbnggzyjyxx.com/jyxx/zfcg/zbjggs?currentPage={}','//*[@id="zbggForm"]/div[2]/table/tr'],
            #       异常公示
            ['http://www.xsbnggzyjyxx.com/jyxx/zfcg/zfcgYcgg?currentPage={}','//*[@id="ycggForm"]/div[2]/table/tr']
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
            text = tool.requests_get(url[0].format(page), headers)
            html = HTML(text)
            detail = html.xpath(url[1])
            for i in range(1, len(detail)):
                try:
                    title = html.xpath(url[1] + '[{}]/td[3]/a/@title'.format(i + 1))[0]
                    url_ = 'http://www.xsbnggzyjyxx.com' + html.xpath(url[1] + '[{}]/td[3]/a/@href'.format(i + 1))[
                        0]
                    date_Today = html.xpath(url[1] + '[{}]/td[4]/text()'.format(i + 1))[0]
                    if '招标' in date_Today or '采购' in date_Today:
                        date_Today = html.xpath(url[1] + '[{}]/td[5]/text()'.format(i + 1))[0]
                    if title == '':
                        title = html.xpath(url[1] + '[{}]/td[3]/@title'.format(i + 1))[0]
                except:
                    title = html.xpath(url[1] + '[{}]/td[4]/a/@title'.format(i + 1))[0]
                    url_ = 'http://www.xsbnggzyjyxx.com' + html.xpath(url[1] + '[{}]/td[4]/a/@href'.format(i + 1))[
                        0]
                    date_Today = html.xpath(url[1] + '[{}]/td[5]/text()'.format(i + 1))[0]
                    if title == '':
                        title = html.xpath(url[1] + '[{}]/td[4]/@title'.format(i + 1))[0]
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

    # 许昌市公共资源交易平台
    def guangdong(self):
        print('许昌市公共资源交易平台', 'http://ggzy.xuchang.gov.cn')
        url_list_to = [
            # 建设工程
            # 公告信息
            'http://ggzy.xuchang.gov.cn/fbzzgg/index_{}.jhtml',
            # 变更公告
            'http://ggzy.xuchang.gov.cn/gbggg/index_{}.jhtml',
            # 中标候选人
            'http://ggzy.xuchang.gov.cn/gpbgs/index_{}.jhtml',
            # 结果公示
            'http://ggzy.xuchang.gov.cn/gzbgs/index_{}.jhtml',
            # 政府采购
            # 公告信息
            'http://ggzy.xuchang.gov.cn/zzbgg/index_{}.jhtml',
            # 变更公告
            'http://ggzy.xuchang.gov.cn/zbggg/index_{}.jhtml',
            # 征求意见
            'http://ggzy.xuchang.gov.cn/zbqgs/index_{}.jhtml',
            # 结果公示
            'http://ggzy.xuchang.gov.cn/zzbgs/index_{}.jhtml'
        ]
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
            text = tool.requests_get(url.format(page), headers)
            html = HTML(text)
            detail = html.xpath('/html/body/div[10]/div[2]/div/div[2]/ul/li')
            for li in detail:
                title = li.xpath('./a/@title')[0]
                url_ = 'http://ggzy.xuchang.gov.cn' + li.xpath('./a/@href')[0]
                date_Today = li.xpath('./em/text()')[0].replace('\r', '').replace('\t', '').replace(' ', '').replace(
                    '\n', '')
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

    # 阳泉市公共资源交易中心
    def guangdongzf(self):
        print('阳泉市公共资源交易中心', 'http://ggzy.yq.gov.cn')
        url_list = [
            # 工程建设
            'http://ggzy.yq.gov.cn/gcjs/index_{}.htm',
            # 政府采购
            'http://ggzy.yq.gov.cn/zfcg/index_{}.htm',
            # 交通运输
            'http://ggzy.yq.gov.cn/jyfwjtys/index_{}.htm'
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
                text = tool.requests_get(url.format(page), headers)
            html = HTML(text)
            detail = html.xpath('/html/body/div/section/div/div[2]/div[2]/div/div[2]/ul/li')
            for li in detail:
                title = li.xpath('./a/@title')[0]
                url_ = 'http://ggzy.yq.gov.cn' + li.xpath('./a/@href')[0]
                date_Today = li.xpath('./span/text()')[0]
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

    # 营口市公共资源交易网
    def guangyuan(self):
        print('营口市公共资源交易网', 'http://ccgp.yingkou.gov.cn')
        url_list = [
            'http://ccgp.yingkou.gov.cn/Html/NewsList.asp?SortID=98&SortPath=0,98,&Page={}'
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
            text = tool.requests_get(url.format(page), headers).replace("<td width='680'", "<tr><td width='680'")
            html = HTML(text)
            detail = html.xpath('//*[@class="page_r_mid_v"]/table/tr[2]/td[2]/table/tr')
            for li in detail[:-1]:
                title = li.xpath('./td[1]/a/@title')[0]
                url_ = 'http://ccgp.yingkou.gov.cn/Html/' + li.xpath('./td[1]/a/@href')[0]
                date_Today = li.xpath('./td[2]/text()')[0]
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

    # 益阳市公共资源交易平台
    def guangan(self):
        print('益阳市公共资源交易平台', 'http://jyzx.yiyang.gov.cn')
        url_list = [
            # 市本级
            #   工程建设
            'http://jyzx.yiyang.gov.cn/ggzyjy/31065/31081/{}',
            #   政府采购
            'http://jyzx.yiyang.gov.cn/ggzyjy/31065/31082/31113/{}'
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
                text = tool.requests_get(url.format('index.htm'), headers)
            else:
                text = tool.requests_get(url.format('index_' + str(page - 1) + '.htm'), headers)
            html = HTML(text)
            detail = html.xpath('//*[@class="tllb_rg_con"]/ul')
            for i in detail:
                for li in i.xpath('./li'):
                    title = li.xpath('./a/@title')[0]
                    url_ = url.format(li.xpath('./a/@href')[0])
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

    # 永州市公共资源交易平台
    def qingyang(self):
        print('永州市公共资源交易平台', 'http://ggzy.yzcity.gov.cn')
        url_list = [
            # 市本级
            #   工程建设
            'http://ggzy.yzcity.gov.cn/jyxx/003001/{}.html',
            #   政府采购
            'http://ggzy.yzcity.gov.cn/jyxx/003002/{}.html'
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
        while True:
            page += 1
            if page == 1:
                text = tool.requests_get(url.format('about-trade'), headers)
            else:
                text = tool.requests_get(url.format(page), headers)
            html = HTML(text)
            detail = html.xpath('/html/body/div[2]/div[2]/div[2]/div/div[2]/ul/li')
            for li in detail:
                title = li.xpath('./a/@title')[0]
                url_ = 'http://ggzy.yzcity.gov.cn' + li.xpath('./a/@href')[0]
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

    # 岳阳市公共资源交易平台
    def zhangye(self):
        print('岳阳市公共资源交易平台', 'http://ggzy.yueyang.gov.cn')
        url_list = [
            # 市本级
            #   工程建设
            'http://ggzy.yueyang.gov.cn/56114/56125/{}',
            #   政府采购
            'http://ggzy.yueyang.gov.cn/56114/56131/{}',
            # 医疗采购
            'http://ggzy.yueyang.gov.cn/56114/56143/{}'
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
                text = tool.requests_get(url.format('index.htm'), headers)
            else:
                text = tool.requests_get(url.format('index_' + str(page - 1) + '.htm'), headers)
            html = HTML(text)
            detail = html.xpath('//*[@class="list-right"]/ul/li')
            for li in detail:
                title = li.xpath('./a/@title')[0]
                url_ = url.format(li.xpath('./a/@href')[0])
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

    # 运城市公共资源交易平台
    def xuzhou(self):
        print('运城市公共资源交易平台', 'http://60.222.222.42')
        url_list = [
            # 政府采购
                # 采购公告
            'http://60.222.222.42/TPFront/jyxx/005002/005002001/?Paging={}',
                # 变更公告
            'http://60.222.222.42/TPFront/jyxx/005002/005002002/?Paging={}',
                # 结果公告
            'http://60.222.222.42/TPFront/jyxx/005002/005002003/?Paging={}',
            # 工程建设
                # 招标公告
            'http://60.222.222.42/TPFront/jyxx/005001/005001001/?Paging={}',
                # 变更公告
            'http://60.222.222.42/TPFront/jyxx/005001/005001002/?Paging={}',
                # 候选人公示
            'http://60.222.222.42/TPFront/jyxx/005001/005001003/?Paging={}',
                # 结果公告
            'http://60.222.222.42/TPFront/jyxx/005001/005001004/?Paging={}'
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
            detail = html.xpath('//*[@id="categorypagingcontent"]/ul/li')
            for li in detail:
                title = li.xpath('./div/a/@title')[0]
                url_ = 'http://60.222.222.42' + li.xpath('./div/a/@href')[0]
                date_Today = li.xpath('./span/text()')[0]
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

    # 云南省政府采购网
    def dezhou(self):
        print('云南省政府采购网', 'http://www.yngp.com')
        url_list = [
            'http://www.yngp.com/bulletin.do?method=moreListQuery&current={}&rowCount=10&searchPhrase=&query_sign=1',
            'http://www.yngp.com/bulletin.do?method=moreListQuery&current={}&rowCount=10&searchPhrase=&query_bulletintitle=&query_startTime=&query_endTime=&query_sign=3',
            'http://www.yngp.com/bulletin.do?method=moreListQuery&current={}&rowCount=10&searchPhrase=&query_bulletintitle=&query_startTime=&query_endTime=&query_sign=2',
            'http://www.yngp.com/bulletin.do?method=moreListQuery&current={}&rowCount=10&searchPhrase=&query_bulletintitle=&query_startTime=&query_endTime=&query_sign=7'
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
            detail = json.loads(text)
            for li in detail['rows']:
                title = li['bulletintitle']
                if 'query_sign=3' in url:
                    url_ = 'http://www.yngp.com/newbulletin_zz.do?method=toaddmodify&operator_state=1&lxflag=dy&flag=view&bulletin_id=' + \
                          li['bulletin_id']
                elif 'query_sign=1' in url:
                    url_ = 'http://www.yngp.com/newbulletin_zz.do?method=preinsertgomodify&operator_state=1&flag=view&bulletin_id=' + \
                          li['bulletin_id']
                elif 'query_sign=2' in url:
                    url_ = 'http://www.yngp.com/newbulletin_zz.do?method=preinsertgomodify&operator_state=1&flag=view&bulletin_id=' + \
                          li['bulletin_id']
                elif 'query_sign=7' in url:
                    url_ = 'http://www.yngp.com/newbulletin_zz.do?method=preinsertgomodify&operator_state=1&flag=view&bulletin_id=' + \
                          li['bulletin_id']
                date_Today = li['finishday']
                if date_Today == '':
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

    # 玉溪市公共资源交易平台
    def chengdu(self):
        print('玉溪市公共资源交易平台', 'http://60.160.190.130:8001')
        url_list = [
            # 市本级
            #   工程建设
            #       招标公告
            ['http://60.160.190.130:8001/jyxx/jsgcZbgg?currentPage={}','//*[@id="zbggForm"]/div[3]/table/tr'],
            #       变更公告
            ['http://60.160.190.130:8001/jyxx/jsgcBgtz?currentPage={}','//*[@id="bgtzForm"]/div[2]/table/tr'],
            #       评标结果公示
            ['http://60.160.190.130:8001/jyxx/jsgcpbjggs?currentPage={}','//*[@id="zbggForm"]/div[2]/table/tr'],
            #       中标结果
            ['http://60.160.190.130:8001/jyxx/jsgcZbjggs?currentPage={}','//*[@id="zbggForm"]/div[3]/table/tr'],
            #       异常公告
            ['http://60.160.190.130:8001/jyxx/jsgcZbyc?currentPage={}','//*[@id="ycggForm"]/div[2]/table/tr'],
            #   政府采购
            #       采购公告
            ['http://60.160.190.130:8001/jyxx/zfcg/cggg?currentPage={}','//*[@id="zbggForm"]/div[2]/table/tr'],
            #       变更通知
            ['http://60.160.190.130:8001/jyxx/zfcg/gzsx?currentPage={}','//*[@id="zbggForm"]/div[2]/table/tr'],
            #       结果公示
            ['http://60.160.190.130:8001/jyxx/zfcg/zbjggs?currentPage={}','//*[@id="zbggForm"]/div[2]/table/tr'],
            #       异常公示
            ['http://60.160.190.130:8001/jyxx/zfcg/zfcgYcgg?currentPage={}','//*[@id="ycggForm"]/div[2]/table/tr']
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
            text = tool.requests_get(url[0].format(page), headers)
            html = HTML(text)
            detail = html.xpath(url[1])
            for i in range(1, len(detail)):
                try:
                    title = html.xpath(url[1] + '[{}]/td[3]/a/@title'.format(i + 1))[0]
                    url_ = 'http://60.160.190.130:8001' + html.xpath(url[1] + '[{}]/td[3]/a/@href'.format(i + 1))[0]
                    date_Today = html.xpath(url[1] + '[{}]/td[4]/text()'.format(i + 1))[0]
                    if '招标' in date_Today or '采购' in date_Today:
                        date_Today = html.xpath(url[1] + '[{}]/td[5]/text()'.format(i + 1))[0]
                    if title == '':
                        title = html.xpath(url[1] + '[{}]/td[3]/@title'.format(i + 1))[0]
                except:
                    title = html.xpath(url[1] + '[{}]/td[4]/a/@title'.format(i + 1))[0]
                    url_ = 'http://60.160.190.130:8001' + html.xpath(url[1] + '[{}]/td[4]/a/@href'.format(i + 1))[0]
                    date_Today = html.xpath(url[1] + '[{}]/td[5]/text()'.format(i + 1))[0]
                    if title == '':
                        title = html.xpath(url[1] + '[{}]/td[4]/@title'.format(i + 1))[0]
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

    # 中国石油招标投标网     加密
    def yangzhou(self):
        print('中国石油招标投标网', 'https://www.cnpcbidding.com')
        url_list = [
           ['198','199'],['198','201']
        ]
        headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Content-Type': 'application/json;charset=UTF-8',
            'Cookie': 'suite-pmsuite=9d1e2f2a-1554-4331-87d3-7764a4418a5e',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',

        }
        url = url_list.pop(0)
        page = 0
        ls = []
        data = {"url": "./list.html", "pid": "198", "pageSize": 15, "categoryId": "199", "title": "", "projectType": "",
                "pageNo": 1}
        url_to = 'https://www.cnpcbidding.com/cms/pmsbidInfo/listPageOut'
        while True:
            page += 1
            data['pid'] = url[0]
            data['categoryId'] = url[1]
            data['pageNo'] = page
            text = tool.requests_post_to(url_to, data, headers)
            detail = json.loads(text)['list']
            for li in detail:
                title = li['projectname']
                url_ = 'https://www.cnpcbidding.com/' + li['id']
                date_Today = li['dateTime'].replace('\n', '').replace('\t', '').replace('\r', '') \
                    .replace(' ', '').replace('/', '-')
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

    # 张家界市公共资源交易平台  打不开
    def panzhihua(self):
        print('张家界市公共资源交易平台', 'http://www.zjjsggzy.gov.cn')
        url_list = [
            # 市本级
            #   工程建设
            #       招标公告
            'http://www.zjjsggzy.gov.cn/TenderProject/GetTpList?page={}&records=15&name=&category=%E6%88%BF%E5%BB%BA%'
            'E5%B8%82%E6%94%BF%2C%E6%B0%B4%E5%88%A9%2C%E4%BA%A4%E9%80%9A%E8%BF%90%E8%BE%93%2C%E5%9C%9F%E5%9C%B0%E5%BC%'
            '80%E5%8F%91%E6%95%B4%E7%90%86%2C%E5%85%B6%E4%BB%96%2C%E9%9D%9E%E6%94%BF%E5%BA%9C%E9%87%87%E8%B4%AD%2C%E5%8'
            'C%BB%E8%8D%AF%E9%87%87%E8%B4%AD&method=&publishbegintime=&publishendtime=&bpType=&IsShowOld=true',
            #       补充通知
            'http://www.zjjsggzy.gov.cn/tenderproject/GetClarificationNotice?page={}&records=15&name=&category=%E6%88%BF'
            '%E5%BB%BA%E5%B8%82%E6%94%BF%2C%E6%B0%B4%E5%88%A9%2C%E4%BA%A4%E9%80%9A%E8%BF%90%E8%BE%93%2C%E5%9C%9F%E5%9C%'
            'B0%E5%BC%80%E5%8F%91%E6%95%B4%E7%90%86%2C%E5%85%B6%E4%BB%96%2C%E9%9D%9E%E6%94%BF%E5%BA%9C%E9%87%87%E8%B4%'
            'AD%2C%E5%8C%BB%E8%8D%AF%E9%87%87%E8%B4%AD&method=&publishbegintime=&publishendtime=&bpType=&IsShowOld=true',
            #       中标候选人公示
            'http://www.zjjsggzy.gov.cn/TenderProject/GetBidderList?page={}&records=15&name=&category=%E6%88%BF%E5%BB%BA'
            '%E5%B8%82%E6%94%BF%2C%E6%B0%B4%E5%88%A9%2C%E4%BA%A4%E9%80%9A%E8%BF%90%E8%BE%93%2C%E5%9C%9F%E5%9C%B0%E5%BC'
            '%80%E5%8F%91%E6%95%B4%E7%90%86%2C%E5%85%B6%E4%BB%96%2C%E9%9D%9E%E6%94%BF%E5%BA%9C%E9%87%87%E8%B4%AD%2C%E5'
            '%8C%BB%E8%8D%AF%E9%87%87%E8%B4%AD&method=&publishbegintime=&publishendtime=&bpType=%E4%B8%AD%E6%A0%87%E5%'
            '85%AC%E7%A4%BA%2C%E4%B8%AD%E6%A0%87%E5%80%99%E9%80%89%E4%BA%BA%E5%85%AC%E7%A4%BA&IsShowOld=true',
            # 结果公示
            'http://www.zjjsggzy.gov.cn/TenderProject/GetBidderList?page={}&records=15&name=&category=%E6%88%BF%E5%BB'
            '%BA%E5%B8%82%E6%94%BF%2C%E6%B0%B4%E5%88%A9%2C%E4%BA%A4%E9%80%9A%E8%BF%90%E8%BE%93%2C%E5%9C%9F%E5%9C%B0%E5'
            '%BC%80%E5%8F%91%E6%95%B4%E7%90%86%2C%E5%85%B6%E4%BB%96%2C%E9%9D%9E%E6%94%BF%E5%BA%9C%E9%87%87%E8%B4%AD%2'
            'C%E5%8C%BB%E8%8D%AF%E9%87%87%E8%B4%AD&method=&publishbegintime=&publishendtime=&bpType=%E6%B5%81%E6%A0%'
            '87%E5%85%AC%E7%A4%BA%2C%E5%BA%9F%E6%A0%87%E5%85%AC%E7%A4%BA%2C%E4%B8%AD%E6%A0%87%E7%BB%93%E6%9E%9C%E5%85'
            '%AC%E7%A4%BA&IsShowOld=true',
            #   政府采购
            #       采购公告
            'http://www.zjjsggzy.gov.cn/TenderProject/GetTpList?page={}&records=15&name=&category=%E6%94%BF%E5%BA%9C%E9'
            '%87%87%E8%B4%AD&method=%E5%85%AC%E5%BC%80%E6%8B%9B%E6%A0%87&publishbegintime=&publishendtime=&bpType=&'
            'IsShowOld=true',
            # 补充公告
            'http://www.zjjsggzy.gov.cn/tenderproject/GetClarificationNotice?page={}&records=15&name=&category=%E6%94%B'
            'F%E5%BA%9C%E9%87%87%E8%B4%AD&method=%E5%85%AC%E5%BC%80%E6%8B%9B%E6%A0%87&publishbegintime=&publishendtim'
            'e=&bpType=&IsShowOld=true',
            #       结果公示
            'http://www.zjjsggzy.gov.cn/TenderProject/GetBidderList?page=1&records=15&name=&category=%E6%94%BF%E5%BA%9'
            'C%E9%87%87%E8%B4%AD&method=%E5%85%AC%E5%BC%80%E6%8B%9B%E6%A0%87&publishbegintime=&publishendtime=&bpType='
            '&IsShowOld=true'
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
            detail = json.loads(text)['json']
            if 'tenderproject' in url:
                detail = json.loads(text)['json']['list']
            for i in detail:
                title = i['Title']
                if 'TpId' in i:
                    code = i['TpId']
                else:
                    code = i['id']
                try:
                    date_Today = str(i['time'])[:10]
                except:
                    date_Today = str(i['PublishTime'])[:10]
                url_ = ''
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

    # 周口市公共资源交易平台
    def xinyu(self):
        print('周口市公共资源交易平台', 'http://jyzx.zhoukou.gov.cn')
        url_list = [
            # 建设工程
            # 招标公告
            'http://jyzx.zhoukou.gov.cn/TPFront/jyxx/002001/002001001/',
            # 变更公告
            'http://jyzx.zhoukou.gov.cn/TPFront/jyxx/002001/002001002/',
            # 中标公告
            'http://jyzx.zhoukou.gov.cn/TPFront/jyxx/002001/002001003/',
            # 政府采购
            # 采购公告
            'http://jyzx.zhoukou.gov.cn/TPFront/jyxx/002002/002002001/',
            # 变更公告
            'http://jyzx.zhoukou.gov.cn/TPFront/jyxx/002002/002002002/',
            # 中标结果
            'http://jyzx.zhoukou.gov.cn/TPFront/jyxx/002002/002002003/',
        ]
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        }
        url = url_list.pop(0)
        page = 0
        ls = []
        while True:
            page += 1
            text = tool.requests_get(url, headers)
            html = HTML(text)
            detail = html.xpath('/html/body/div/div[2]/table[2]/tr/td/table/tr/td[3]/table[3]/tr[2]/td/table/tr')
            for tr in detail[1:]:
                for li in tr.xpath('./td/table/tr[2]/td[2]/table/tr'):
                    title = li.xpath('./td[2]/a/@title')[0]
                    url_ = 'http://jyzx.zhoukou.gov.cn' + li.xpath('./td[2]/a/@href')[0]
                    date_Today = li.xpath('./td[3]/font/text()')[0]
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

    # 舟山市公共资源交易平台
    def wuxi(self):
        print('舟山市公共资源交易平台', 'http://zsztb.zhoushan.gov.cn')
        url_list = [
            # 政府采购
            # 采购公告
            'http://zsztb.zhoushan.gov.cn/zsztbweb/gcjs/010008/?Paging={}',
            # 变更公告
            'http://zsztb.zhoushan.gov.cn/zsztbweb/gcjs/010009/?Paging={}',
            # 中标候选人
            'http://zsztb.zhoushan.gov.cn/zsztbweb/gcjs/010010/?Paging={}',
            # 中标结果
            'http://zsztb.zhoushan.gov.cn/zsztbweb/gcjs/010015/?Paging={}',
            # 政府采购
            # 采购公告
            'http://zsztb.zhoushan.gov.cn/zsztbweb/zfcg/011001/?Paging={}',
            # 更正公告
            'http://zsztb.zhoushan.gov.cn/zsztbweb/zfcg/011002/?Paging={}',
            # 结果公告
            'http://zsztb.zhoushan.gov.cn/zsztbweb/zfcg/011004/?Paging={}'
        ]
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36',
        }
        url = url_list.pop(0)
        page = 0
        ls = []
        while True:
            page += 1
            text = tool.requests_get(url.format(page), headers)
            html = HTML(text)
            detail = html.xpath('/html/body/div/div[2]/div/div[2]/div[2]/table/tr/td/table/tr')
            for li in range(0, len(detail), 2):
                title = html.xpath(
                    '/html/body/div/div[2]/div/div[2]/div[2]/table/tr/td/table/tr[{}]/td[2]/a/@title'.format(li + 1))[0]
                url_ = 'http://zsztb.zhoushan.gov.cn' + html.xpath(
                    '/html/body/div/div[2]/div/div[2]/div[2]/table/tr/td/table/tr[{}]/td[2]/a/@href'.format(li + 1))[0]
                date_Today = html.xpath(
                    '/html/body/div/div[2]/div/div[2]/div[2]/table/tr/td/table/tr[{}]/td[3]/text()'.format(li + 1))[
                    0].replace('[', '').replace(']', '')
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

    # 驻马店市公共资源交易平台
    def rizhao(self):
        print('驻马店市公共资源交易平台', 'http://www.zmdggzy.gov.cn')
        url_list = [
            # 建设工程
            # 招标公告
            'http://www.zmdggzy.gov.cn/TPFront/jyxx/003001/003001001/',
            # 变更公告
            'http://www.zmdggzy.gov.cn/TPFront/jyxx/003001/003001003/',
            # 结果异常
            'http://www.zmdggzy.gov.cn/TPFront/jyxx/003001/003001004/',
            # 中标候选人
            'http://www.zmdggzy.gov.cn/TPFront/jyxx/003001/003001005/',
            # 政府采购
            # 采购公告
            'http://www.zmdggzy.gov.cn/TPFront/jyxx/003002/003002001/',
            # 变更公告
            'http://www.zmdggzy.gov.cn/TPFront/jyxx/003002/003002003/',
            # 结果公告
            'http://www.zmdggzy.gov.cn/TPFront/jyxx/003002/003002004/',
            # 异常公告
            'http://www.zmdggzy.gov.cn/TPFront/jyxx/003002/003002005/'
        ]
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        }
        url = url_list.pop(0)
        page = 0
        ls = []
        while True:
            page += 1
            text = tool.requests_get(url, headers)
            html = HTML(text)
            detail = html.xpath('//*[@id="categorypagingcontent"]/div/div')
            for i in detail:
                for j in i.xpath('./ul/li'):
                    title = j.xpath('./div/a/text()')[0].replace('\n', '').replace('\r', '').replace('\t', '').replace(
                        ' ', '')
                    url_ = 'http://www.zmdggzy.gov.cn' + j.xpath('./div/a/@href')[0]
                    date_Today = j.xpath('./span/text()')[0].replace('\n', '').replace('\r', '').replace('\t',
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

    # 株洲市公共资源交易平台
    def zaozhuang(self):
        print('株洲市公共资源交易平台', 'http://www.zzzyjy.cn')
        url_list = [
            # 房屋市政
            'http://www.zzzyjy.cn/016/016001/{}.html',
            # 市政工程
            'http://www.zzzyjy.cn/016/016002/{}.html',
            # 交通
            'http://www.zzzyjy.cn/016/016003/{}.html',
            # 水利水电
            'http://www.zzzyjy.cn/016/016004/{}.html',
            # 其他
            'http://www.zzzyjy.cn/016/016005/{}.html'
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
            detail = html.xpath('/html/body/div[2]/div[1]/div/div[2]/div/ul/li')
            for li in detail:
                title = li.xpath('./a/@title')[0]
                url_ = 'http://www.zzzyjy.cn' + li.xpath('./a/@href')[0]
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

    # 遵义市公共资源交易平台
    def jiangsu(self):
        print('遵义市公共资源交易平台', 'http://ggzyjy.zunyi.gov.cn')
        url_list = [
            # 市本级
            #   工程建设
            #       招标公告
            'http://ggzyjy.zunyi.gov.cn/jyxx/gcjs/zbgg/{}.html',
            #       中标公示
            'http://ggzyjy.zunyi.gov.cn/jyxx/gcjs/zbqrgg/{}.html',
            #       中标候选人
            'http://ggzyjy.zunyi.gov.cn/jyxx/gcjs/zbhxrgs/{}.html',
            #       更正公告
            'http://ggzyjy.zunyi.gov.cn/jyxx/gcjs/bggg/{}.html',
            #       流标公告
            'http://ggzyjy.zunyi.gov.cn/jyxx/gcjs/xmycgs/{}.html',
            #   政府采购
            #       采购公告
            'http://ggzyjy.zunyi.gov.cn/jyxx/zfcg/cggg/{}.html',
            #       中标公告
            'http://ggzyjy.zunyi.gov.cn/jyxx/zfcg/zbcjgg/{}.html',
            #       更正公告
            'http://ggzyjy.zunyi.gov.cn/jyxx/zfcg/gzgg/{}.html',
            #       流标公告
            'http://ggzyjy.zunyi.gov.cn/jyxx/zfcg/fbgg/{}.html'
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
                text = tool.requests_get(url.format('index_' + str(page)), headers)
            html = HTML(text)
            detail = html.xpath('/html/body/div[3]/div/div[2]/ul/li')
            for li in detail:
                title = li.xpath('./a/@title')[0]
                url_ = li.xpath('./a/@href')[0]
                date_Today = li.xpath('./span/text()')[0].replace('\n', '').replace('\r', '') \
                    .replace('\t', '').replace(' ', '')
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

    # 上海公共资源交易平台  网站打不开
    def jiangxi(self):
        print('上海公共资源交易平台', 'http://ggzy.sheic.org.cn')
        url_list = [
            'http://ggzy.sheic.org.cn/publicity/transaction/page?page={}&pageSize=10'
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
            print(text)
            detail = json.loads(text)['result']['list']
            for li in detail:
                title = li['projectName']
                code = li["projectCode"]
                stage = li["stage"]
                module = li["module"]
                try:
                    if module == '3' and stage == '1':  # 招标公告
                        url_ = "http://ggzy.sheic.org.cn/publicity/constructionBulletin/findBulletinList/{}".format(code)
                        url_ = json.loads(tool.requests_get(url, headers))['result']['source']
                        start_to = '1'
                    elif module == '1' and stage == '1':  # 采购公告
                        url_ = "http://ggzy.sheic.org.cn/publicity/gp/bulletin/{}".format(code)
                        start_to = '5'
                    elif module == '1' and stage == '2':  # 采购结果
                        url_ = 'http://ggzy.sheic.org.cn/publicity/gp/winnerBulletin/{}'.format(code)
                        start_to = '6'
                    elif module == '3' and stage == '5':  # 中标结果
                        url_ = "http://ggzy.sheic.org.cn/publicity/constructionWinner/{}".format(code)
                        url_ = json.loads(tool.requests_get(url, headers))['result']['source']
                        start_to = '8'
                    else:
                        print('内容不符')
                        continue
                except:
                    continue
                date_Today = li['time']
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

    # 东苑市政府采购网
    def taizhou(self):
        print('东苑市政府采购网', 'http://czj.dg.gov.cn')
        url_list = [
           'http://czj.dg.gov.cn/dggp/portal/topicView.do?method=view&id=1660',
           'http://czj.dg.gov.cn/dggp/portal/topicView.do?method=view&id=1663'
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
            'ec_i': 'topicChrList',
            'topicChrList_crd': '30',
            'topicChrList_f_a': '',
            'topicChrList_p': '2',
            'topicChrList_s_stockProjectCode': '',
            'topicChrList_s_name': '',
            'topicChrList_s_ldate': '',
            'id': '1663',
            'method': 'view',
            '__ec_pages': '1',
            'topicChrList_rd': '30',
            'topicChrList_f_stockProjectCode': '',
            'topicChrList_f_name': '',
            'topicChrList_f_ldate': ''
        }
        while True:
            page += 1
            if page == 1:
                text = tool.requests_get(url, headers)
            else:
                text = tool.requests_post(url, data, headers)
            data['topicChrList_p'] = page
            data['id'] = url[-4:]
            html = HTML(text.replace('<?xml version="1.0" encoding="UTF-8" ?>', ''))
            detail = html.xpath('//*[@id="topicChrList_table"]/tbody/tr')
            for li in detail:
                title = li.xpath('./td[2]/a/text()')[0].replace('\xa0', '').replace(' ', '')
                url_ = 'http://czj.dg.gov.cn' + \
                      li.xpath('./td[2]/a/@href')[0]
                date_Today = li.xpath('./td[3]/text()')[0].replace('月', '-').replace('日', '').replace('\n', '').replace(
                    '\t', '').replace('年', '-')
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

    # 中国交建物资采购管理信息系统
    def luzhou(self):
        print('中国交建物资采购管理信息系统', 'http://ec.ccccltd.cn')
        url_list = [
            ['http://ec.ccccltd.cn/PMS/gysmore.shtml?id=sjN7r9ttBwLI2dpg4DQpQb68XreXjaqknBMygP8dAEQ57TILyRtTnCZX1hIiXHcc1Ra16D6TzZdblRFD/JXcCd5FP7Ek60ksxl9KkyODirY=', '2639'],
            ['http://ec.ccccltd.cn/PMS/gysmore.shtml?id=sjN7r9ttBwLI2dpg4DQpQb68XreXjaqknBMygP8dAEQ57TILyRtTnPr0y7nbc5lW1Ra16D6TzZdblRFD/JXcCd5FP7Ek60ksxl9KkyODirY=', '1015']
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
            data = {
                'pid': '',
                'announcetstrtime_from': '',
                'announcetstrtime_to': '',
                'announcetitle': '',
                'VENUS_PAGE_NO_KEY_INPUT': str(page - 1),
                'VENUS_PAGE_NO_KEY': str(page),
                'VENUS_PAGE_COUNT_KEY': url[1],
                'VENUS_PAGE_SIZE_KEY': '15'
            }
            text = tool.requests_post(url[0], data, headers)
            html = HTML(text)
            data['VENUS_PAGE_COUNT_KEY'] = html.xpath(
                '//*[@id="pageTable"]/tr/td[2]/table/tr/td[5]/input[2]/@value')[0]
            data['VENUS_PAGE_SIZE_KEY'] = html.xpath(
                '//*[@id="pageTable"]/tr/td[2]/table/tr/td[5]/input[3]/@value')[0]
            detail = html.xpath('//*[@id="ccChild1"]/table/tr/td/div/table/tr/td/table/tr')
            for li in detail:
                try:
                    title = li.xpath('./td[2]/a/text()')[0].replace(
                        '<font color=red></font>', '')
                    date_Today = str(li.xpath('./td[3]/text()')[0]).strip().replace('[', '').replace(']', '')
                    url_ = 'http://ec.ccccltd.cn/PMS/moredetail.shtml?id=' + li.xpath(
                        './td[2]/a/@href')[0].replace('javaScript:goAdjustBidResultDetail(', '').replace(
                        'javaScript:goLostBidDetail(', '').replace('javaScript:goByDetail(', '').replace(
                        'javaScript:goAnnounceDetail(', '').replace(');', '').replace("'", '').replace(r"\r\n", '')
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

    # 中国政府采购网
    def hubei(self):
        print('中国政府采购网', 'http://www.ccgp.gov.cn')
        url_list = ['cggg/zygg', 'cggg/dfgg', 'http://search.ccgp.gov.cn/eanotice?ptit=&pnm=&ptime=&ptime_end=&ptime_start=&page_index={}']
        headers = {
            'ajax-method': 'AjaxMethodFactory',
            # 'Cookie': 'ASP.NET_SessionId=irwyyayh3dtwq5zxunzlnq3x',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        }
        url = url_list.pop(0)
        page = 0
        ls = []
        url_to = 'http://www.ccgp.gov.cn/{}/{}.htm'
        while True:
            page += 1
            if 'eanotice' in url:
                text = tool.requests_get(url.format(page), headers)
                text = re.findall(" var a='(.*?)'.replace", text, re.S)[0].replace('},]','}]')
            else:
                if page == 1:
                    text = tool.requests_get(url_to.format(url, 'index'), headers)
                else:
                    text = tool.requests_get(url_to.format(url, 'index_' + str(page - 1)), headers)
                html = HTML(text)
            if 'eanotice' in url:
                detail = json.loads(text)
            elif url == 'cggg/dfgg':
                detail = html.xpath('//*[@class="c_list_bid"]/li')
            else:
                detail = html.xpath('//*[@id="bid_lst"]/div[2]/div/div[1]/div/div[2]/div[1]/ul/li')
            for li in detail:
                if 'eanotice' in url:
                    title = li['title']
                    date_Today = li['date']
                    url_ = li['lnk']
                elif url == 'cggg/dfgg':
                    try:
                        title = li.xpath('./a/@title')[0]
                        date_Today = str(li.xpath('./em[2]/text()')[0]).strip()[:10]
                        url_ = 'http://www.ccgp.gov.cn/' + url + li.xpath('./a/@href')[0][1:]
                    except:
                        continue
                else:
                    title = li.xpath('./a/@title')[0]
                    date_Today = str(li.xpath('./em[2]/text()')[0])[:10]
                    url_ = 'http://www.ccgp.gov.cn/' + url + li.xpath('./a/@href')[0][1:]
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

    # 中国海洋石油集团有限公司
    def binzhou(self):
        print('中国海洋石油集团有限公司', 'https://buy.cnooc.com.cn')
        url_list = [
            'https://buy.cnooc.com.cn/cbjyweb/001/001001/{}.html',
            'https://buy.cnooc.com.cn/cbjyweb/001/001002/{}.html',
            'https://buy.cnooc.com.cn/cbjyweb/001/001003/{}.html'
        ]
        headers = {
            'Cookie': 'Hm_lvt_776eb6c6b51e3da5075c361337f94338=1584946762,1586936167; TS0161614b=01761419df1159ee5d0dc3cd6f5029798f9f5622ce83a1a6b58545a766632b4b2c2ba8a9c608459776a8aa67978b0cd44c6b44f253; Hm_lpvt_776eb6c6b51e3da5075c361337f94338=1586936490',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        }
        url = url_list.pop(0)
        page = 0
        ls = []
        while True:
            page += 1
            text = tool.requests_get(url.format(page), headers)
            html = HTML(text)
            detail = html.xpath('//*[@id="categorypagingcontent"]/ul/li')
            for li in detail:
                title = li.xpath('./a/@title')[0].replace('\xa0', '').replace(' ', '')
                url_ = 'https://buy.cnooc.com.cn' + \
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

    # 中国电建设备物资集中采购平台
    def zhangzhou(self):
        print('中国电建设备物资集中采购平台', 'https://ec.powerchina.cn')
        url_list = [
            'https://ec.powerchina.cn/zgdjcms/category/bulletinList.html?searchDate=1995-07-21&dates=300&word=&categoryId=2&tabName=&startPublishDate=&endPublishDate=&page={}',
            'https://ec.powerchina.cn/zgdjcms/category/bulletinList.html?searchDate=1995-07-21&dates=300&word=&categoryId=3&tabName=&startPublishDate=&endPublishDate=&page={}',
            'https://ec.powerchina.cn/zgdjcms/category/bulletinList.html?searchDate=1995-07-21&dates=300&word=&categoryId=5&tabName=&startPublishDate=&endPublishDate=&page={}'
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
            detail = html.xpath('//*[@id="bulletinList"]/li')
            for li in detail:
                try:
                    title = li.xpath('./a/@title')[0].replace('\xa0', '').replace(' ', '')
                    url_ = 'https:' + \
                          li.xpath('./a/@href')[0]
                    date_Today = li.xpath('./a/div/div/text()')[0].replace('月', '-').replace('日', '').replace('\n',
                                                                                                              '').replace(
                        '\t', '').replace('年', '-')
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

    # 中国石化物资招标投标网
    def weifang(self):
        print('中国石化物资招标投标网', 'https://bidding.sinopec.com')
        url_list = [
            'https://bidding.sinopec.com/tpfront/CommonPages/searchmore.aspx?CategoryNum=004001',
            'https://bidding.sinopec.com/tpfront/CommonPages/searchmore.aspx?CategoryNum=004004',
            'https://bidding.sinopec.com/tpfront/CommonPages/searchmore.aspx?CategoryNum=004005'
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
        data = ''
        while True:
            page += 1
            if page == 1:
                text = tool.requests_get(url, headers)
            else:
                text = tool.requests_post(url, data, headers)
            html = HTML(text)
            data = {
                '__VIEWSTATE': html.xpath('//*[@id="__VIEWSTATE"]/@value')[0],
                '__VIEWSTATEGENERATOR': html.xpath('//*[@id="__VIEWSTATEGENERATOR"]/@value')[0],
                '__EVENTTARGET': 'MoreinfoListsearch1$Pager',
                '__EVENTARGUMENT': str(page+1),
                '__VIEWSTATEENCRYPTED': '',
                '__EVENTVALIDATION': html.xpath('//*[@id="__EVENTVALIDATION"]/@value')[0],
                'MoreinfoListsearch1$txtTitle': '',
                'MoreinfoListsearch1$slrq': '',
                'MoreinfoListsearch1$slrq2':'',
                'MoreinfoListsearch1$Pager_input': str(page)
            }
            detail = html.xpath('//*[@id="MoreinfoListsearch1_DataGrid1"]/tr')
            for tr in detail[1:]:
                title = tr.xpath('./td[2]/div/a/@title')[0]
                url_ = 'https://bidding.sinopec.com' + tr.xpath('./td[2]/div/a/@href')[0]
                date_Today = self.date[:5] + tr.xpath('./td[3]/text()')[0].replace('\n', '').replace('\r', '').replace('\t', '')\
                    .replace(' ', '')
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

    # 中招联合招标采购网
    def yantai(self):
        print('中招联合招标采购网', 'http://www.365trade.com.cn')
        url_list = [
            'http://www.365trade.com.cn/zbgg/index_{}.jhtml',
            'http://www.365trade.com.cn/bggg/index_{}.jhtml'
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
            detail = HTML(text).xpath('/html/body/div[2]/div/ul/li')
            for li in detail:
                title = li.xpath('./a[1]/p/span/@title')[0]
                url_ = 'http://www.365trade.com.cn' + li.xpath('./a[1]/@href')[0]
                date_Today = li.xpath('./a[1]/i/text()')[0].replace('发布日期：', '')
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

    # 云南省投资审批中介超市
    def gansu(self):
        print('云南省投资审批中介超市', 'http://220.163.118.100')
        url_list = [
            'http://220.163.118.100/yns/purchaseNotice'
        ]
        headers = {
            'Cookie': 'JSESSIONID=D9F5E5809737BA00C2E040B1DA3BEB3E',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        }
        url = url_list.pop(0)
        page = 0
        ls = []
        data = {
            'listVo.projectName': '',
            'listVo.serviceType': '',
            'listVo.divisionCode': '530000',
            'purOrgCodePanel_selectname': '',
            'selectBox_purOrgCodePanel': '',
            'listVo.purOrgCode': '',
            'listVo.publishDateBegin': '',
            'listVo.publishDateEnd': '',
            'listVo.selectType': '',
            'pageNumber': '1',
            'sourtType': ''
        }
        while True:
            page += 1
            if page == 1:
                text = tool.requests_get(url, headers)
            else:
                text = tool.requests_post('http://220.163.118.100/yns/purchaseNotice/listPost', data, headers)
            data['pageNumber'] = page
            html = HTML(text)
            detail = html.xpath('//*[@id="resultPannel"]/table/tr')
            for li in detail:
                try:
                    title = li.xpath('./td[2]/a/text()')[1].replace('\n', '').replace('\t', '').replace(
                        ' ', '')
                    url_ = 'http://220.163.118.100' + li.xpath('./td[2]/a/@href')[0]
                    date_Today = li.xpath('./td[5]/text()')[0].replace('\n', '').replace('\t', '').replace('\r',
                                                                                                           '').replace(
                        ' ', '')
                    city = li.xpath('./td[1]/text()')[0].replace('\n', '').replace('\t', '').replace('\r',
                                                                                                     '').replace(
                        ' ', '')
                except:
                    continue
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

    # 仪陇县公共资源交易网  网站打不开
    def baiyin(self):
        print('仪陇县公共资源交易网', 'http://www.yilongjyzx.com')
        url_list = [
            'http://www.yilongjyzx.com/Front/zfcg/002001/?Paging={}',
            'http://www.yilongjyzx.com/Front/zfcg/002002/?Paging={}',
            'http://www.yilongjyzx.com/Front/gcjs/003001/?Paging={}',
            'http://www.yilongjyzx.com/Front/gcjs/003003/?Paging={}'
        ]
        headers = {
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
            detail = html.xpath('/html/body/div[4]/div/div[2]/div/div[2]/ul/table/tr')
            for li in detail:
                try:
                    title = li.xpath('./td[2]/a/@title')[0]
                    url_ = 'http://www.yilongjyzx.com' + li.xpath('./td[2]/a/@href')[0]
                    date_Today = li.xpath('./td[3]/text()')[0].replace('\n', '').replace('\t', '').replace('\r',
                                                                                                           '').replace(
                        ' ', '')
                except:
                    continue
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

    # 全国公共资源交易平台
    def yancheng(self):
        print('全国公共资源交易平台', 'http://www.ggzy.gov.cn/')
        url_list = [
            'http://deal.ggzy.gov.cn/ds/deal/dealList_find.jsp?TIMEBEGIN_SHOW={}&TIMEEND_SHOW={}&TIMEBEGIN={}&TIMEEND={}&SOURCE_TYPE=1&DEAL_TIME=02&DEAL_CLASSIFY=00&DEAL_STAGE=0000&DEAL_PROVINCE=0&DEAL_CITY=0&DEAL_PLATFORM=0&BID_PLATFORM=0&DEAL_TRADE=0&isShowAll=1&PAGENUMBER={}&FINDTXT=',
            'http://deal.ggzy.gov.cn/ds/deal/dealList_find.jsp?TIMEBEGIN_SHOW={}&TIMEEND_SHOW={}&TIMEBEGIN={}&TIMEEND={}&SOURCE_TYPE=2&DEAL_TIME=02&DEAL_CLASSIFY=01&DEAL_STAGE=0100&DEAL_PROVINCE=0&DEAL_CITY=0&DEAL_PLATFORM=0&BID_PLATFORM=0&DEAL_TRADE=0&isShowAll=1&PAGENUMBER={}&FINDTXT='
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
        date_to = time.strftime('%Y-%m-%d', time.localtime(time.time()-86400-86400-86400))
        while True:
            page += 1
            text = tool.requests_get(url.format(date_to, self.date, date_to, self.date, page), headers).replace('\n', '').replace('\r',
                                                                                                                '') \
                .replace(' ', '').replace('\t', '')
            detail = json.loads(text)['data']
            for li in detail:
                title = li['title'].replace('\xa0', '').replace('\n', ''). \
                    replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '').replace(
                    "<fontstyle='color:red'>(网)</font>", '')
                url_ = li['url'].replace('http://www.ggzy.gov.cn/information/html/a',
                                        'http://www.ggzy.gov.cn/information/html/b')
                date_Today = li['timeShow'].replace('\xa0', '').replace('\n', ''). \
                    replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '') \
                    .replace('[', '').replace(']', '').replace('/', '-')
                if 'http' not in url_:
                    url_ = 'http://deal.ggzy.gov.cn' + url_
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

    # 内蒙古公共资源网
    def meishan(self):
        print('内蒙古公共资源网', 'http://ggzyjy.nmg.gov.cn')
        url_list = [
            'http://ggzyjy.nmg.gov.cn/jyxx/jsgcZbgg', 'http://ggzyjy.nmg.gov.cn/jyxx/jsgcGzsx', 'http://ggzyjy.nmg.gov.cn/jyxx/jsgcZbhxrgs', 'http://ggzyjy.nmg.gov.cn/jyxx/jsgcZbjggs',
                     # 政府采购
            'http://ggzyjy.nmg.gov.cn/jyxx/zfcg/cggg', 'http://ggzyjy.nmg.gov.cn/jyxx/zfcg/gzsx', 'http://ggzyjy.nmg.gov.cn/jyxx/zfcg/zbjggs',
                    # 其他交易
            'http://ggzyjy.nmg.gov.cn/jyxx/qtjy/jygg', 'http://ggzyjy.nmg.gov.cn/jyxx/qtjy/jyqr'
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
            'currentPage': '',
            'industriesTypeCode': '000',
            'time': '',
            'scrollValue': '1200',
            'bulletinName': '',
            'area': '001',
            'startTime': '',
            'endTime': ''
        }
        while True:
            page += 1
            if page == 1:
                text = tool.requests_get(url, headers)
            else:
                text = tool.requests_post(url, data, headers)
            data['currentPage'] = str(page)
            detail = HTML(text).xpath('/html/body/div[2]/div[2]/div/div[4]/table/tr')
            for tr in detail:
                if 'jsgcZbjggs' in url or 'jsgcZbhxrgs' in url:
                    try:
                        title = tr.xpath('./td[2]/a/@title')[0]
                        date_Today = tr.xpath('./td[3]/text()')[0].replace('\n', '').replace('\r',
                                                                                             '') \
                            .replace('\t', '').replace(' ', '')
                        url_ = 'http://ggzyjy.nmg.gov.cn' + tr.xpath('./td[2]/a/@href')[0].replace('\n', '').replace(
                            '\r',
                            '') \
                            .replace('\t', '').replace(' ', '')
                    except:
                        continue
                else:
                    try:
                        title = tr.xpath('./td[3]/a/@title')[0]
                        date_Today = tr.xpath('./td[4]/text()')[0].replace('\n', '').replace('\r',
                                                                                             '') \
                            .replace('\t', '').replace(' ', '')
                        url_ = 'http://ggzyjy.nmg.gov.cn' + tr.xpath('./td[3]/a/@href')[0].replace('\n', '').replace(
                            '\r', '') \
                            .replace('\t', '').replace(' ', '')
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

    # 吉林省建设信息网
    def fuzhou(self):
        print('吉林省建设信息网', 'http://www.jlsjsxxw.com')
        url_list = [
            'http://www.jlsjsxxw.com:20001/web/bblistdata?sortOrder=desc&pageSize=14&pageNumber={}&_=1594114796684',
            'http://www.jlsjsxxw.com:20001/web/alterationShow/list?sortOrder=desc&pageSize=14&pageNumber={}&_=1594114936887',
            'http://www.jlsjsxxw.com:20001/web/candidateShow/list?sortOrder=desc&pageSize=14&pageNumber={}&_=1594114960508'
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
            detail = json.loads(text)['rows']
            for li in detail:
                title = li['projectName']
                if 'bblistdata' in url:
                    url_ = 'http://www.jlsjsxxw.com/bblistdata/' + \
                          str(li['id'])
                    t = li['contents']
                elif 'candidateShow' in url:
                    url_ = 'http://www.jlsjsxxw.com:20001/web/candidateShow/detail/' + \
                          str(li['id'])
                    t = ''
                else:
                    url_ = 'http://www.jlsjsxxw.com:20001/web/alterationShow/detail/' + \
                          str(li['id'])
                    t = ''
                date_Today = li['releaseDate'].split(' ')[0].replace('/', '-')
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

    # 四川建设网
    def liaocheng(self):
        print('四川建设网', 'http://www.sccin.com.cn')
        url_list = [
            'http://www.sccin.com.cn/InvestmentInfo/ZhaoBiao/InvitNotice.aspx?typeid=0&&type=ZBGG',
            'http://www.sccin.com.cn/InvestmentInfo/ZhaoBiao/houxuanren.aspx?type=ZBHXR'
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
            '__EVENTTARGET': 'ctl00$ContentPlaceHolder1$myPager',
            '__EVENTARGUMENT': '2',
            '__LASTFOCUS': '',
            '__VIEWSTATE': '',
            '__EVENTVALIDATION': '',
            'ctl00$Control_Ads1$hdfClickedAdKeys': '',
            'ctl00$Search1$txtQuery': '',
            'ctl00$ContentPlaceHolder1$tb_Name': '',
            'ctl00$ContentPlaceHolder1$ucCodeModule_IPBtype$ddlCodeList': '0',
            'ctl00$ContentPlaceHolder1$ucAreaCode1$ddlProvince': '0',
            'ctl00$ContentPlaceHolder1$myPager_input': '1',
            'ctl00$Control_Ads2$hdfClickedAdKeys': ''
        }
        while True:
            page += 1
            if page == 1:
                text = tool.requests_get(url, headers)
            else:
                text = tool.requests_post(url, data, headers)
            html = HTML(text)
            data['__EVENTARGUMENT'] = page
            data['ctl00$ContentPlaceHolder1$myPager_input'] = page - 1
            data['__VIEWSTATE'] = html.xpath('//*[@id="__VIEWSTATE"]/@value')[0]
            data['__EVENTVALIDATION'] = html.xpath('//*[@id="__EVENTVALIDATION"]/@value')[0]
            if 'ZBGG' in url:
                detail = html.xpath('//*[@id="ContentPlaceHolder1_GVList"]/tr')
            else:
                detail = html.xpath('//*[@class="lie"]/tbody/tr[2]/td[1]/table/tr')
            for li in detail:
                if 'ZBGG' in url:
                    try:
                        title = li.xpath('./td[1]/a/span/@title')[0].replace('\xa0', '').replace(' ', '')
                        url_ = 'http://www.sccin.com.cn/InvestmentInfo/ZhaoBiao/' + \
                              li.xpath('./td[1]/a/@href')[0]
                        date_Today = li.xpath('./td[3]/text()')[0].replace('/', '-')
                    except:
                        continue
                else:
                    title = li.xpath('./td[1]/a/@title')[0].replace('\xa0', '').replace(' ', '')
                    url_ = 'http://www.sccin.com.cn/InvestmentInfo/ZhaoBiao/' + \
                          li.xpath('./td[1]/a/@href')[0]
                    date_Today = li.xpath('./td[3]/text()')[0].replace('\r', '').replace(' ', '').replace('\n',
                                                                                                          '').replace(
                        '\t', '').replace('/', '-')
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

    # 四川政府采购
    def putian(self):
        print('四川政府采购', 'http://www.ccgp-sichuan.gov.cn')
        url_list = [
            'http://www.ccgp-sichuan.gov.cn/CmsNewsController.do?method=recommendBulletinList&moreType=provincebuyBulletinMore&channelCode=sjcg2&rp=25&page={}',
            'http://www.ccgp-sichuan.gov.cn/CmsNewsController.do?method=recommendBulletinList&rp=25&page={}&moreType=provincebuyBulletinMore&channelCode=sjcg1'
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
            detail = HTML(text).xpath("//div[@class='info']/ul/li")
            for li in detail:
                title = li.xpath('./a/@title')[0]
                url_ = li.xpath("./a/@href")[0].replace("http//202.61.88.152:8006", '')
                if 'http' not in url_:
                    url_ = "http://www.ccgp-sichuan.gov.cn" + url_
                ri = li.xpath("./div[1]/span/text()")[0]
                try:
                    date_Today = li.xpath("./div[1]/text()[2]")[0].replace('\n',
                                                                           '').replace(
                        '\t', '').replace('\r', '').replace(' ', '') + '-' + ri
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

    # 国家开发投资公司电子采购平台
    def xian(self):
        print('国家开发投资公司电子采购平台', 'http://eps.sdic.com.cn')
        url_list = [
            'http://eps.sdic.com.cn/gggc/index_{}.jhtml',
            'http://eps.sdic.com.cn/bggc/index_{}.jhtml',
            'http://eps.sdic.com.cn/cggc/index_{}.jhtml'
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
            detail = html.xpath('//*[@id="main"]/div[2]/div/div[1]/div/div[2]/div/div/ul/li')
            for li in detail:
                title = li.xpath('./a/@title')[0]
                url_ = li.xpath('./a/@href')[0]
                date_Today = li.xpath('./a/span[3]/text()')[0].replace('\n', '').replace('\r', '').replace('\t',
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

    def time_date(self, date):
        date_ls = date.split(' ')
        month = ''
        month_ls = ['Jan', 'Feb','Mar', 'Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
        for i in month_ls:
            if date_ls[1] == i:
                month = str(month_ls.index(i)+1)
                if len(month) == 1:
                    month = '0' + month
                break
        return date_ls[-1] + '-' + month + '-' + date_ls[2]

    # 天津政府采购
    def xizang(self):
        print('天津政府采购', 'http://www.ccgp-tianjin.gov.cn')
        url_list = [1665, 1664, 1663, 1666, 2014, 2013]
        headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Cookie': 'JSESSIONID=662863FD2199FBD1672A04A290868047; _CSRFCOOKIE=73F3D7A1BCDCA9001D7B1483A214C4E98DE2528B; EPTOKEN=73F3D7A1BCDCA9001D7B1483A214C4E98DE2528B; oauthClientId=demoClient; oauthPath=http://172.16.5.21:8080/EpointWebBuilder; oauthLoginUrl=http://172.16.5.21:8080/EpointWebBuilder/rest/oauth2/authorize?client_id=demoClient&state=a&response_type=code&scope=user&redirect_uri=; oauthLogoutUrl=http://172.16.5.21:8080/EpointWebBuilder/rest/oauth2/logout?redirect_uri=; noOauthRefreshToken=986d4fe7e5dd29b64c9e7b7a6d66e089; noOauthAccessToken=77c09e0bf98b6220b544961097eed84a; sub_domain_cokie=TiG5CMD9KQ41mmsARPTuAg%3D%3D; region_name=%E4%B9%8C%E9%B2%81%E6%9C%A8%E9%BD%90%E5%B8%82',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',

        }
        url = url_list.pop(0)
        page = 0
        ls = []
        url_to = 'http://www.ccgp-tianjin.gov.cn/portal/topicView.do'
        while True:
            page += 1
            data = {"method": "view",
                    "page": "{}".format(page),
                    "id": "{}".format(url),
                    "step": "1",
                    "view": "Infor",
                    "st": "1",
                    'ldateQGE': '',
                    'ldateQLE': ''}
            text = tool.requests_post(url_to, data, headers)
            detail = HTML(text).xpath("//div[@id='reflshPage']/ul/li")
            for li in detail:
                url_ = "http://www.ccgp-tianjin.gov.cn/portal/documentView.do?method=view&id={}&ver=2".format(
                    re.findall('id=(.*?)&', li.xpath("./a/@href")[0])[0])
                date_Today = self.time_date(li.xpath("./span/text()")[0])
                title = li.xpath("./a/text()")[0]
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

    # 天津轨道交通
    def xizangzf(self):
        print('天津轨道交通', 'http://www.tjgdjt.com')
        url_list = [
            'http://www.tjgdjt.com/xinwen/{}.htm'
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
                text = tool.requests_get(url.format('node_163'), headers)
            else:
                text = tool.requests_get(url.format('node_163_' + str(page)), headers)
            detail = HTML(text).xpath('/html/body/div/div[3]/div[2]/div[2]/ul/li')
            for li in detail:
                title = li.xpath('./a/text()')[0]
                url_ = 'http://www.tjgdjt.com/xinwen/' + li.xpath('./a/@href')[0]
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

    # 宁夏公共资源交易网
    def dazhou(self):
        print('宁夏公共资源交易网', 'http://www.nxggzyjy.org')
        url_list = [
            'http://www.nxggzyjy.org/ningxiaweb/002/{}.html'
        ]
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        }
        url = url_list.pop(0)
        ls = []
        page = 0
        while True:
            page += 1
            text = tool.requests_get(url.format(page), headers)
            html = HTML(text)
            detail = html.xpath('//*[@id="showList"]/ul/li')
            for li in detail:
                title = li.xpath('./div/a/text()')[0]
                date_Today = li.xpath('./span/text()')[0]
                url_ = 'http://www.nxggzyjy.org' + li.xpath('./div/a/@href')[0]
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

    # 宁夏政府采购网
    def jinchang(self):
        print('宁夏政府采购网', 'http://www.ccgp-ningxia.gov.cn')
        url_list = [
            'http://www.ccgp-ningxia.gov.cn//site/InteractionQuestion_findVNotice.do?type=&date=&page={}&regionId=640000&tab=Q&dateq1=&dateq2=&keyword=&buyerName=&agentName=&projectNumber=&planNumber=&authCode='
        ]
        url = url_list.pop(0)
        page = 0
        ls = []
        session = requests.session()
        while True:
            page += 1
            while True:
                text = session.get(url.format(page)).text
                if 'reload' in text:
                    print('reload')
                    time.sleep(2)
                    continue
                break
            detail = re.findall("noticeId.*?}", text, re.S)
            for li in detail:
                li = json.loads('{"' + li.replace('\\', ''))
                title = li['name']
                url_ = 'http://www.ccgp-ningxia.gov.cn/public/NXGPPNEW/dynamic/{}&type={}'.format(li['url'], li['type'])
                date_Today = li['date'].replace('\n', '').replace('\r', '') \
                    .replace('\t', '').replace(' ', '')
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

    # 宁波政府采购网
    def longnan(self):
        print('宁波政府采购网', 'http://www.nbzfcg.cn')
        url_list = [
            'http://www.nbzfcg.cn/project/zcyNotice.aspx?noticetype=2',
            'http://www.nbzfcg.cn/project/zcyNotice.aspx?noticetype=4',
            'http://www.nbzfcg.cn/project/zcyNotice.aspx?noticetype=53'
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
            '__VIEWSTATE': '',
            '__EVENTTARGET': 'gdvNotice3$ctl18$AspNetPager1',
            '__EVENTARGUMENT': '',
            'ddlRegion': '',
            'txtNoticeTitle': '',
            'txtNoticeDate1': '',
            'txtNoticeDate2': '',
            'gdvNotice3$ctl18$AspNetPager1_input': ''
        }
        while True:
            page += 1
            if page == 1:
                text = tool.requests_get(url, headers)
            else:
                text = tool.requests_post(url, data, headers)
            html = HTML(text)
            data['__VIEWSTATE'] = html.xpath('//*[@id="__VIEWSTATE"]/@value')[0]
            data['__EVENTARGUMENT'] = page + 1
            data['gdvNotice3$ctl18$AspNetPager1_input'] = page
            detail = html.xpath('//*[@id="gdvNotice3"]/tr')
            for li in detail:
                try:
                    title = li.xpath('./td[3]/a/text()')[0]
                    url_ = 'http://www.nbzfcg.cn/project/' + li.xpath('./td[3]/a/@href')[0]
                    date_Today = li.xpath('./td[4]/text()')[0].replace('\n', '').replace('\t', '').replace('\r',
                                                                                                           '').replace(
                        ' ', '')
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

    # 安徽公共资源交易集团
    def shanxi(self):
        print('安徽公共资源交易集团', 'http://www.ahggzyjt.com')
        url_list = [
            'http://www.ahggzyjt.com/jyxx/002001/002001001/{}.html',
            'http://www.ahggzyjt.com/jyxx/002002/002002001/{}.html',
            'http://www.ahggzyjt.com/jyxx/002003/002003001/{}.html'
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
                text = tool.requests_get(url.format('secondPage'), headers)
            else:
                text = tool.requests_get(url.format(page), headers)
            html = HTML(text)
            detail = html.xpath('//*[@id="right"]/ul/li')
            for li in detail:
                title = li.xpath('./a/text()')[0]
                url_ = 'http://www.ahggzyjt.com' + li.xpath('./a/@href')[0]
                date_Today = li.xpath('./span/text()')[0].replace('\n', '').replace('\t', '').replace('\r', '').replace(
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

    # 安徽省公共资源交易监管网
    def yaan(self):
        print('安徽省公共资源交易监管网', 'http://ggzy.ah.gov.cn')
        url_list = [
            'http://ggzy.ah.gov.cn/jsgc/list',
            'http://ggzy.ah.gov.cn/jsgc/list?tenderProjectType=A07',
            'http://ggzy.ah.gov.cn/jsgc/list?tenderProjectType=AAA',
            'http://ggzy.ah.gov.cn/jsgc/list?tenderProjectType=A99',
            'http://ggzy.ah.gov.cn/zfcg/list'
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
            text = tool.requests_get(url, headers)
            dateil = HTML(text).xpath('//*[@class="list clear"]/ul[2]/li')
            for li in dateil:
                title = li.xpath('./a/span[2]/@title')[0]
                url_ = 'http://ggzy.ah.gov.cn' + \
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
                        break
            url = url_list.pop(0)
            page = 0

    # 安徽省政府采购网  未完成 网站打不开反应太慢
    def longyan(self):
        print('安徽省政府采购网', 'http://www.ccgp-anhui.gov.cn')
        url_list = [
            'http://www.ccgp-anhui.gov.cn/cmsNewsController/getCgggNewsList.do?pageNum={}&numPerPage=20&title=&buyer_name='
            '&agent_name=&proj_code=&bid_type=&type=&dist_code=&pubDateStart=&pubDateEnd=&pProviceCode=&areacode_city=&areacode_dist=&channelCode=cggg&three='
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
            detail = HTML(text).xpath('//*[@id="bodyMain"]/div/div[3]/table/tr')
            for li in detail:
                url_ = 'http://www.ccgp-anhui.gov.cn' + li.xpath('./td[1]/a/@href')[0]
                title = li.xpath('./td[1]/a/@title')[0]
                date_Today = li.xpath('./td[2]/a/text()')[0].replace('\n', '').replace('\t', '').replace('\r',
                                                                                                         '').replace(
                    ' ', '') \
                    .replace('[', '').replace(']', '')
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


