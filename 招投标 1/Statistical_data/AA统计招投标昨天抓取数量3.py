# -*- coding: utf-8 -*-
import base64
import time, json, re, requests
from lxml.etree import HTML
from tool import tool

class spider:
    def __init__(self):
        self.tool = tool()
        self.date = tool.date
        self.url_lss = [
            [self.sanming,'http://smggzy.sm.gov.cn'],
            [self.linxi, 'http://ggzyjy.linyi.gov.cn'],
            [self.leshan, 'http://ggzyjy.hbwf.gov.cn'],
            [self.yunan, 'https://www.ynggzy.com'],
            [self.neijiang, 'http://ggzy.neijiang.gov.cn'],
            [self.beijing, 'https://ggzyfw.beijing.gov.cn'],
            [self.beijingzf, 'http://www.ccgp-beijing.gov.cn'],
            [self.nanjing, 'http://njggzy.nanjing.gov.cn'],
            [self.nanchong, 'http://www.scncggzy.com.cn'],
            [self.nanping, 'http://ggzy.np.gov.cn'],
            [self.nanchang, 'http://www.jxsncggzy.cn'],
            [self.nantong, 'http://zfcg.nantong.gov.cn'],
            [self.jian, 'http://ggzy.jian.gov.cn'],
            [self.jilin, 'http://was.jl.gov.cn'],
            [self.jilinzf, 'http://www.ggzyzx.jl.gov.cn'],
            [self.jiayuguan, 'http://www.jygzyjy.gov.cn'],
            [self.sichuan, 'http://ggzyjy.sc.gov.cn'],
            [self.weihai, 'http://ggzyjy.weihai.cn'],
            [self.anhui, 'http://www.ahtba.org.cn'],
            [self.yichun, 'http://xzspj.yichun.gov.cn'],
            [self.suqian, 'http://ggzy.sqzwfw.gov.cn'],
            [self.bazhong, 'http://117.172.156.43:82'],
            [self.changzhou, 'http://58.216.50.99:8089'],
            [self.guangdong, 'http://bs.gdggzy.org.cn'],
            [self.guangdongzf, 'http://www.ccgp-guangdong.gov.cn'],
            [self.guangyuan, 'http://www.gyggzyjy.cn'],
            [self.guangan, 'http://125.66.2.245'],
            [self.qingyang, 'http://www.qysggzyjy.cn'],
            [self.zhangye, 'http://60.165.196.18:8090'],
            [self.xuzhou, 'http://www.xzcet.com'],
            [self.dezhou, 'http://ggzyjy.dezhou.gov.cn:8086'],
            [self.chengdu, 'https://www.cdggzy.com'],
            [self.yangzhou, 'http://ggzyjyzx.yangzhou.gov.cn'],
            [self.panzhihua, 'http://ggzy.panzhihua.gov.cn'],
            [self.xinyu, 'http://www.xyggzy.cn'],
            [self.wuxi, 'http://xzfw.wuxi.gov.cn'],
            [self.rizhao, 'http://ggzyjy.rizhao.gov.cn'],
            [self.zaozhuang, 'http://www.zzggzy.com'],
            [self.jiangsu, 'http://www.ccgp-jiangsu.gov.cn'],
            [self.jiangxi, 'https://www.jxsggzy.cn'],
            [self.taizhou, 'http://58.222.225.18:8138'],
            [self.luzhou, 'https://www.lzsggzy.com'],
            [self.jining, 'http://ggzy.jining.gov.cn'],
            [self.hubei, 'https://www.hbggzyfwpt.cn'],
            [self.binzhou, 'http://ggzyjy.binzhou.gov.cn'],
            [self.zhangzhou, 'http://www.zzgcjyzx.com'],
            [self.weifang, 'http://ggzy.weifang.gov.cn'],
            [self.yantai, 'http://ggzyjy.yantai.gov.cn'],
            #   [self.gansu, 'https://ggzyjy.gansu.gov.cn'],  网站改版
            [self.baiyin, 'http://ggzyjy.baiyin.gov.cn'],
            [self.yancheng, 'http://112.24.96.37:9890'],
            [self.meishan, 'http://www.msggzy.org.cn'],
            [self.fuzhou, 'http://fzsggzyjyfwzx.cn'],
            [self.liaocheng, 'http://www.lcsggzyjy.cn'],
            [self.putian, 'http://ggzyjy.xzfwzx.putian.gov.cn'],
            [self.xian, 'http://www.xacin.com.cn'],
            [self.xizang, 'http://www.xzggzy.gov.cn:9090'],
            #[self.xizangzf, 'http://www.ccgp-xizang.gov.cn'], 打不开
            [self.dazhou, 'http://www.dzggzy.cn'],
            [self.longnan, 'http://www.lnsggzyjy.cn'],
            [self.shanxi, 'http://www.sxggzyjy.cn'],
            [self.yaan, 'http://www.yaggzy.org.cn'],
            [self.longyan, 'https://www.lyggzy.com.cn']
        ]

    # 三明市公共资源交易网
    def sanming(self):
        print('三明市公共资源交易网', 'http://smggzy.sm.gov.cn')
        url_list = [
            'http://smggzy.sm.gov.cn/smwz/jyxx/022001/022001001/?pageing={}',
            'http://smggzy.sm.gov.cn/smwz/jyxx/022001/022001002/?pageing={}',
            'http://smggzy.sm.gov.cn/smwz/jyxx/022001/022001004/?pageing={}',
            'http://smggzy.sm.gov.cn/smwz/jyxx/022001/022001005/?pageing={}',
            'http://smggzy.sm.gov.cn/smwz/jyxx/022002/022002001/?pageing={}',
            'http://smggzy.sm.gov.cn/smwz/jyxx/022002/022002002/?pageing={}',
            'http://smggzy.sm.gov.cn/smwz/jyxx/022002/022002005/?pageing={}'
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
            detail = html.xpath('//div[1]/ul/li')
            for li in detail:
                title = li.xpath('./a/text()')[0].replace('\n', '').replace('\t', '').replace(' ', '').replace('\r', '')
                url_ = li.xpath('./a/@href')[0]
                url_domain = 'http://smggzy.sm.gov.cn'
                if 'http' not in url_:
                    if '../../' in url_:
                        url_ = url_domain + url_[5:]
                    elif '../' in url_:
                        url_ = url_domain + url_[2:]
                    elif './' in url_:
                        url_ = url_domain + url_[1:]
                    else:
                        url_ = url_domain + url_
                date_Today = li.xpath('./span/text()')[0].replace('\n', '').replace('\t', '').replace(' ', '').replace(
                    '\r', '')
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

    # 临沂市公共资源交易网
    def linxi(self):
        print('临沂市公共资源交易网', 'http://ggzyjy.linyi.gov.cn')
        url_list = [
            'http://ggzyjy.linyi.gov.cn/linyi/jyxx/{}.html'
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
            if page == 1:
                text = tool.requests_get(url.format('jylist'), headers)
            else:
                text = tool.requests_get(url.format(page), headers)
            html = HTML(text)
            detail = html.xpath('//*[@id="list"]/li')
            for li in detail:
                title = li.xpath('./a/@title')[0].replace('\n', '').replace('\r', '') \
                    .replace('\t', '').replace(' ', '')
                url_ = li.xpath('./a/@href')[0]
                if 'http' not in url_:
                    url_ = 'http://ggzyjy.linyi.gov.cn' + url_
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

    # 乐山市公共资源交易网
    def leshan(self):
        print('乐山市公共资源交易网', 'http://www.lsggzy.com.cn')
        url_list = [
            ['JYGCJS', 'ZBGG'],
            ['JYGCJS', 'PBJG'],
            ['JYZFCG', 'CGGG'],
            ['JYZFCG', 'GZGG'],
            ['JYZFCG', 'JGGG'],
            ['JYZFCG', 'ZZGG']
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
            data = {
                'rootCode': 'jyxx',
                'menuCode': url[0],
                'typeCode': url[1],
                'page': page,
                'areaCode': '',
                'title': '',
                'pubStime': '',
                'pubEtime': '',
                '_csrf': 'f8e504f8-cc39-4347-b398-d50ee9e709a1'
            }
            page += 1
            text = tool.requests_post('http://www.lsggzy.com.cn/pub/infoSearch', data, headers)
            html = HTML(text)
            detail = html.xpath('//*[@class="MainUl"]/ul/li')
            for li in detail:
                title = li.xpath('./a/@title')[0].replace('\n', '').replace('\r', '') \
                    .replace('\t', '').replace(' ', '')
                url_ = li.xpath('./a/@href')[0]
                if 'http' not in url_:
                    url_ = 'http://www.lsggzy.com.cn' + url_
                date_Today = li.xpath('./a/span[1]/text()')[0].replace('\n', '').replace('\r', '') \
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

    # 云南省公共资源交易中心
    def yunan(self):
        print('云南省公共资源交易中心', 'https://www.ynggzy.com')
        url_list = [
            'https://www.ynggzy.com/jyxx/jsgcZbgg?currentPage={}&area=000&industriesTypeCode=0&scrollValue=900&tenderProjectCode=&bulletinName=',
            'https://www.ynggzy.com/jyxx/jsgcBgtz?currentPage={}&area=&industriesTypeCode=&scrollValue=1500&bidSectionCode=&bidSectionName=',
            'https://www.ynggzy.com/jyxx/jsgcpbjggs?currentPage={}&area=000&industriesTypeCode=0&scrollValue=1277&tenderProjectCode=&tenderProjectName=',
            'https://www.ynggzy.com/jyxx/jsgcZbjggs?currentPage={}&area=000&industriesTypeCode=0&scrollValue=1000&bulletinName=',
            'https://www.ynggzy.com/jyxx/jsgcZbyc?currentPage={}&area=000&industriesTypeCode=&scrollValue=1100&bidSectionCode=&exceptionName=',
            'https://www.ynggzy.com/jyxx/zfcg/cggg?currentPage={}&area=000&industriesTypeCode=&scrollValue=900&purchaseProjectCode=&bulletinTitle=',
            'https://www.ynggzy.com/jyxx/zfcg/gzsx?currentPage={}&area=000&industriesTypeCode=&scrollValue=900&purchaseSectionCode=&terminationBulletinTitle=',
            'https://www.ynggzy.com/jyxx/zfcg/zbjggs?currentPage={}&area=000&industriesTypeCode=&scrollValue=900&winBidBulletinTitle=',
            'https://www.ynggzy.com/jyxx/zfcg/zfcgYcgg?currentPage={}&industriesTypeCode=&scrollValue=1000&purchaseSectionCode=&exceptionName=',
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
            detail = html.xpath('//*[@id="data_tab"]/tbody/tr')
            for li in detail:
                try:
                    if 'jsgcBgtz' in url:
                        title = li.xpath('./td[3]/text()')[0].replace('\n', '').replace('\r', '') \
                            .replace('\t', '').replace(' ', '')
                        url_ = li.xpath('./td[4]/a/@href')[0]
                        date_Today = li.xpath('./td[5]/text()')[0][:10].replace('\n', '').replace('\r', '') \
                            .replace('\t', '').replace(' ', '').replace('.', '-')
                    elif 'jsgcZbjggs' in url or 'zfcg/zbjggs' in url:
                        title = li.xpath('./td[2]/a/text()')[0].replace('\n', '').replace('\r', '') \
                            .replace('\t', '').replace(' ', '')
                        url_ = li.xpath('./td[2]/a/@href')[0]
                        date_Today = li.xpath('./td[3]/text()')[0][:10].replace('\n', '').replace('\r', '') \
                            .replace('\t', '').replace(' ', '').replace('.', '-')
                    elif 'jsgcZbyc' in url or 'zfcg/zfcgYcgg' in url:
                        title = li.xpath('./td[3]/a/text()')[0].replace('\n', '').replace('\r', '') \
                            .replace('\t', '').replace(' ', '')
                        url_ = li.xpath('./td[3]/a/@href')[0]
                        date_Today = li.xpath('./td[5]/text()')[0][:10].replace('\n', '').replace('\r', '') \
                            .replace('\t', '').replace(' ', '').replace('.', '-')
                    else:
                        title = li.xpath('./td[3]/a/text()')[0].replace('\n', '').replace('\r', '') \
                            .replace('\t', '').replace(' ', '')
                        url_ = li.xpath('./td[3]/a/@href')[0]
                        date_Today = li.xpath('./td[4]/text()')[0][:10].replace('\n', '').replace('\r', '') \
                            .replace('\t', '').replace(' ', '').replace('.', '-')
                except:
                    continue
                if 'http' not in url_:
                    if '../../' in url_:
                        url_ = 'https://www.ynggzy.com' + url_[5:]
                    elif '../' in url_:
                        url_ = 'https://www.ynggzy.com' + url_[2:]
                    elif './' in url_:
                        url_ = 'https://www.ynggzy.com' + url_[1:]
                    else:
                        url_ = 'https://www.ynggzy.com' + url_
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

    # 内江市公共资源交易网
    def neijiang(self):
        print('内江市公共资源交易网', 'http://ggzy.neijiang.gov.cn')
        url_list = [
            'http://ggzy.neijiang.gov.cn/EpointWebBuilder/tradeInfoSearchAction.action?cmd=getList&categorynum=006&xiaqucode=&wd=&edt=&sdt=&pageSize=15&siteguid=7eb5f7f1-9041-43ad-8e13-8fcb82ea831a&pageIndex={}'
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
            detail = json.loads(json.loads(text)['custom'])['records']
            for li in detail:
                title = li['title'].replace('\n', '').replace('\r', '') \
                    .replace('\t', '').replace(' ', '')
                url_ = li['href']
                if 'http' not in url_:
                    url_ = 'http://ggzy.neijiang.gov.cn' + url_
                date_Today = li['infodate'].replace('\n', '').replace('\r', '') \
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

    # 北京市公共资源交易平台
    def beijing(self):
        print('北京市公共资源交易平台', 'https://ggzyfw.beijing.gov.cn')
        url_list = [
            'https://ggzyfw.beijing.gov.cn/jylcgcjs/{}.html',
            'https://ggzyfw.beijing.gov.cn/jylczfcg/{}.html'
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
            if page == 1:
                text = tool.requests_get(url.format('index'), headers)
            else:
                text = tool.requests_get(url.format('index_' + str(page)), headers)
            html = HTML(text)
            detail = html.xpath('//*[@class="article-list2"]/li')
            for li in detail:
                title = li.xpath('./a/@title')[0].replace('\n', '').replace('\r', '') \
                    .replace('\t', '').replace(' ', '')
                url_ = li.xpath('./a/@href')[0]
                if 'http' not in url_:
                    url_ = 'https://ggzyfw.beijing.gov.cn' + url_
                date_Today = li.xpath('./div[2]/text()')[0].replace('\n', '').replace('\r', '') \
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

    # 北京市政府采购网
    def beijingzf(self):
        print('北京市政府采购网', 'http://www.ccgp-beijing.gov.cn')
        url_list = [
            'http://www.ccgp-beijing.gov.cn/xxgg/sjzfcggg/{}.html',
            'http://www.ccgp-beijing.gov.cn/xxgg/qjzfcggg/{}.html'
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
                text = tool.requests_get(url.format('index'), headers)
            else:
                text = tool.requests_get(url.format('index_' + str(page)), headers)
            html = HTML(text)
            detail = html.xpath('//*[@class="xinxi_ul"]/li')
            for li in detail:
                title = li.xpath('./a/text()')[0].replace('\n', '').replace('\r', '') \
                    .replace('\t', '').replace(' ', '')
                url_ = li.xpath('./a/@href')[0]
                if 'http' not in url_:
                    if 'sjzfcggg' in url:
                        url_ = 'http://www.ccgp-beijing.gov.cn/xxgg/sjzfcggg' + url_[1:]
                    else:
                        url_ = 'http://www.ccgp-beijing.gov.cn/xxgg/qjzfcggg' + url_[1:]
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

    # 南京市公共资源交易网
    def nanjing(self):
        print('南京市公共资源交易网', 'http://njggzy.nanjing.gov.cn')
        url_list = [
            'http://njggzy.nanjing.gov.cn/njweb/gchw/070001/{}.html?_=23843',
            'http://njggzy.nanjing.gov.cn/njweb/gchw/070003/{}.html?_=52346',
            'http://njggzy.nanjing.gov.cn/njweb/gchw/070004/{}.html?_=71959',
            'http://njggzy.nanjing.gov.cn/njweb/zfcg/067001/067001001/{}.html?_=61648',
            'http://njggzy.nanjing.gov.cn/njweb/zfcg/067002/067002001/{}.html?_=56940'
        ]
        headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Content-Type': 'application/json;charset=UTF-8',
            'Referer': 'http://www.xmzyjy.cn/XmUiForWeb2.0/xmebid/default.do',
            # 'Cookie': 'JSESSIONID=662863FD2199FBD1672A04A290868047; _CSRFCOOKIE=73F3D7A1BCDCA9001D7B1483A214C4E98DE2528B; EPTOKEN=73F3D7A1BCDCA9001D7B1483A214C4E98DE2528B; oauthClientId=demoClient; oauthPath=http://172.16.5.21:8080/EpointWebBuilder; oauthLoginUrl=http://172.16.5.21:8080/EpointWebBuilder/rest/oauth2/authorize?client_id=demoClient&state=a&response_type=code&scope=user&redirect_uri=; oauthLogoutUrl=http://172.16.5.21:8080/EpointWebBuilder/rest/oauth2/logout?redirect_uri=; noOauthRefreshToken=986d4fe7e5dd29b64c9e7b7a6d66e089; noOauthAccessToken=77c09e0bf98b6220b544961097eed84a; sub_domain_cokie=TiG5CMD9KQ41mmsARPTuAg%3D%3D; region_name=%E4%B9%8C%E9%B2%81%E6%9C%A8%E9%BD%90%E5%B8%82',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',

        }
        url = url_list.pop(0)
        page = 0
        ls = []
        while True:
    num = 1
        while True:
            page += 1
            if page == 1:
                if 'zfcg' in url:
                    text = tool.requests_get(url.format('moreinfozfcg'), headers)
                else:
                    text = tool.requests_get(url.format('moreinfogchw'), headers)
            else:
                text = tool.requests_get(url.format(page), headers)
            html = HTML(text)
            detail = html.xpath('//*[@id="iframe{}"]/ul/li'.format(url.split('/')[-2]))
            for li in detail:
                title = li.xpath('./div[2]/p/text()')[0].replace('\n', '').replace('\r', '') \
                    .replace('\t', '').replace(' ', '')
                url_ = li.xpath('./@onclick')[0].replace("window.open('", '').replace("');", '')
                if 'http' not in url_:
                    url_ = 'http://njggzy.nanjing.gov.cn' + url_
                date_Today = li.xpath('./div[4]/p/text()')[0].replace('\n', '').replace('\r', '') \
                    .replace('\t', '').replace(' ', '')
                if '067001' in url:
                    date_Today = li.xpath('./div[5]/p/text()')[0].replace('\n', '').replace('\r', '') \
                        .replace('\t', '').replace(' ', '')
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
                        if 'getAnQuestionPage_project' in url:
                            num += 2
                        else:
                            num += 1
                        url = url_list.pop(0)
                        page = 0
                        break

    # 南充市公共资源交易网
    def nanchong(self):
        print('南充市公共资源交易网', 'http://www.scncggzy.com.cn')
        url_list = [
            'http://www.scncggzy.com.cn/TPFront/ShowInfo/Jyxxsearch.aspx?area=&category=071002&categoryno=&Eptr3=&Paging={}',
            'http://www.scncggzy.com.cn/TPFront/ShowInfo/Jyxxsearch.aspx?area=&category=071003&categoryno=&Eptr3=&Paging={}',
            'http://www.scncggzy.com.cn/TPFront/ShowInfo/Jyxxsearch.aspx?area=&category=071005&categoryno=&Eptr3=&Paging={}',
            'http://www.scncggzy.com.cn/TPFront/ShowInfo/Jyxxsearch.aspx?area=&category=072001&categoryno=&Eptr3=&Paging={}',
            'http://www.scncggzy.com.cn/TPFront/ShowInfo/Jyxxsearch.aspx?area=&category=072002&categoryno=&Eptr3=&Paging={}',
            'http://www.scncggzy.com.cn/TPFront/ShowInfo/Jyxxsearch.aspx?area=&category=072003&categoryno=&Eptr3=&Paging={}',
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
            detail = html.xpath('//*[@id="result"]/div/ul/li')
            for li in detail:
                title = li.xpath('./div/a/text()')[0].replace('\n', '').replace('\r', '') \
                    .replace('\t', '').replace(' ', '')
                url_ = li.xpath('./div/a/@href')[0].replace("window.open('", '').replace("');", '')
                if 'http' not in url_:
                    url_ = 'http://www.scncggzy.com.cn' + url_
                date_Today = li.xpath('./span/text()')[0].replace('\n', '').replace('\r', '') \
                    .replace('\t', '').replace(' ', '')
                if '067001' in url:
                    date_Today = li.xpath('./div[5]/p/text()')[0].replace('\n', '').replace('\r', '') \
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

    # 南平市公共资源交易网
    def nanping(self):
        print('南平市公共资源交易网', 'http://ggzy.np.gov.cn')
        url_list = [
            'http://ggzy.np.gov.cn/npztb/jsgc/010001/?Paging={}',
            'http://ggzy.np.gov.cn/npztb/jsgc/010002/?Paging={}',
            'http://ggzy.np.gov.cn/npztb/jsgc/010003/?Paging={}',
            'http://ggzy.np.gov.cn/npztb/jsgc/010004/?Paging={}',
            'http://ggzy.np.gov.cn/npztb/jsgc/010005/?Paging={}'
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
            detail = html.xpath('/html/body/div[2]/div[2]/div/div[1]/table/tr')
            for li in detail:
                title = li.xpath('./td[2]/a/@title')[0].replace('\n', '').replace('\t', '').replace(' ', '').replace(
                    '\r', '')
                url_ = li.xpath('./td[2]/a/@href')[0]
                url_domain = 'http://ggzy.np.gov.cn'
                if 'http' not in url_:
                    if '../../' in url_:
                        url_ = url_domain + url_[5:]
                    elif '../' in url:
                        url_ = url_domain + url_[2:]
                    elif './' in url:
                        url_ = url_domain + url_[1:]
                    else:
                        url_ = url_domain + url_
                date_Today = li.xpath('./td[3]/text()')[0].replace('\n', '').replace('\t', '').replace(' ', '').replace(
                    '\r', '').replace('[', '').replace(']', '')
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

    # 南昌市公共资源交易网
    def nanchang(self):
        print('南昌市公共资源交易网', 'http://www.jxsncggzy.cn')
        url_list = ['http://www.jxsncggzy.cn/nczbw/jyxx/002001/',
                    'http://www.jxsncggzy.cn/nczbw/jyxx/002002/',
                    'http://www.jxsncggzy.cn/nczbw/jyxx/002003/',
                    'http://www.jxsncggzy.cn/nczbw/jyxx/002009/',
                    'http://www.jxsncggzy.cn/nczbw/jyxx/002004/',
                    'http://www.jxsncggzy.cn/nczbw/jyxx/002010/']
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
            html = HTML(text)
            detail = html.xpath('/html/body/table[2]/tr/td/table/tr/td/table/tr/td[2]/table[2]/tr[2]/td/table/tr')
            for ul in detail:
                for li in ul.xpath('./td/table/tr[2]/td[2]/table/tr'):
                    title = li.xpath('./td[2]/a/@title')[0].replace('\n', '').replace('\r', '') \
                        .replace('\t', '').replace(' ', '')
                    url_ = li.xpath('./td[2]/a/@href')[0]
                    if 'http' not in url_:
                        url_ = 'http://www.jxsncggzy.cn' + url_
                    date_Today = li.xpath('./td[3]/font/text()')[0].replace('\n', '').replace('\r', '') \
                        .replace('\t', '').replace(' ', '').replace('(', '').replace(')', '')
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

    # 南通市公共资源交易网
    def nantong(self):
        print('南通市公共资源交易网', 'http://zfcg.nantong.gov.cn')
        url_list = [
            'http://zfcg.nantong.gov.cn/services/XzsJsggWebservice/getList?response=application/json&pageIndex={}&pageSize=15&&categorynum=&bianhao=&xmmc='
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
            detail = json.loads(json.loads(text)['return'])['Table']
            for li in detail:
                title = li['title'].replace('\n', '').replace('\r', '') \
                    .replace('\t', '').replace(' ', '').replace('<spanstyle="color:red">', '').replace('</span>', '')
                url_ = li['href']
                if 'http' not in url_:
                    url_ = 'http://zfcg.nantong.gov.cn' + url_
                date_Today = li['postdate'].replace('\n', '').replace('\r', '') \
                    .replace('\t', '').replace(' ', '').replace('(', '').replace(')', '')
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

    # 吉安市公共资源交易网
    def jian(self):
        print('吉安市公共资源交易网', 'http://zbtb.jian.gov.cn')
        url_list = [
            'http://ggzy.jian.gov.cn/jyxx/jsgc/zbgg/{}.htm',
            'http://ggzy.jian.gov.cn/jyxx/jsgc/zbgs/{}.htm',
            'http://ggzy.jian.gov.cn/jyxx/zfcg/zbgg/{}.htm',
            'http://ggzy.jian.gov.cn/jyxx/zfcg/zbgs/{}.htm'
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
                text = tool.requests_get(url.format('index' + str(page - 1)), headers)
            html = HTML(text)
            detail = html.xpath('/html/body/div[3]/div/div[2]/div[2]/ul/li')
            for li in detail:
                title = li.xpath('./a/@title')[0].replace('\n', '').replace('\r', '') \
                    .replace('\t', '').replace(' ', '').replace('<spanstyle="color:red">', '').replace('</span>', '')
                url_ = li.xpath('./a/@href')[0]
                if 'http' not in url_:
                    url_ = 'http://zbtb.jian.gov.cn' + url_
                date_Today = li.xpath('./span/text()')[0].replace('\n', '').replace('\r', '') \
                    .replace('\t', '').replace(' ', '').replace('(', '').replace(')', '')
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

    # 吉林省公共资源交易平台
    def jilin(self):
        print('吉林省公共资源交易平台', 'http://www.jl.gov.cn')
        url_list = [
            'http://was.jl.gov.cn/was5/web/search?channelid=237687&page={}&prepage=100'
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
            text = tool.requests_get(url.format(page), headers).replace('result(', '').replace(');', '')
            detail = json.loads(text)['datas']
            for li in detail:
                title = li['title'].replace('\n', '').replace('\r', '') \
                    .replace('\t', '').replace(' ', '')
                url_ = li['docpuburl']
                if 'http' not in url_:
                    url_ = 'http://www.jl.gov.cn' + url_[1:]
                date_Today = li['timestamp'][:10].replace('\n', '').replace('\r', '') \
                    .replace('\t', '').replace(' ', '').replace('.', '-')
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

    # 吉林省政府采购中心
    def jilinzf(self):
        print('吉林省政府采购中心', 'http://www.ggzyzx.jl.gov.cn')
        url_list = [
            'http://www.ggzyzx.jl.gov.cn/jygg/zcjz/zbgg/{}.html',
            'http://www.ggzyzx.jl.gov.cn/jygg/zcjz/bggg/{}.html',
            'http://www.ggzyzx.jl.gov.cn/jygg/zcjz/zbjggg/{}.html',
            'http://www.ggzyzx.jl.gov.cn/jygg/zcjz/fbgg/{}.html',
            'http://www.ggzyzx.jl.gov.cn/jygg/zcfjz/cgzxzbgg/{}.html',
            'http://www.ggzyzx.jl.gov.cn/jygg/zcfjz/cgzxbggg/{}.html',
            'http://www.ggzyzx.jl.gov.cn/jygg/zcfjz/cgzxzbjggg/{}.html',
            'http://www.ggzyzx.jl.gov.cn/jygg/zcfjz/cgzxfbgg/{}.html',
            'http://www.ggzyzx.jl.gov.cn/jygg/cgzxgcjs/cgzxzbgg/{}.html',
            'http://www.ggzyzx.jl.gov.cn/jygg/cgzxgcjs/cgzxbggg/{}.html',
            'http://www.ggzyzx.jl.gov.cn/jygg/cgzxgcjs/zbgg/{}.html',
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
                text = tool.requests_get(url.format('index'), headers).replace('result(', '').replace(');',
                                                                                                                '')
            else:
                text = tool.requests_get(url.format('index_' + str(page)), headers).replace('result(',
                                                                                                      '').replace(');',
                                                                                                                  '')
            html = HTML(text)
            detail = html.xpath('//*[@class="content_r_main"]/ul')
            for ul in detail:
                for li in ul.xpath('./li'):
                    title = li.xpath('./a/text()')[0].replace('\n', '').replace('\r', '') \
                        .replace('\t', '').replace(' ', '')
                    url_ = li.xpath('./a/@href')[0]
                    if 'http' not in url_:
                        url_ = '/'.join(url.split('/')[:-1]) + url_[1:]
                    date_Today = li.xpath('./div/text()')[0].replace('\n', '').replace('\r', '') \
                        .replace('\t', '').replace(' ', '').replace('.', '-')
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

    # 嘉峪关市公共资源交易网
    def jiayuguan(self):
        print('嘉峪关市公共资源交易网', 'http://www.jygzyjy.gov.cn')
        url_list = [
            'http://www.jygzyjy.gov.cn/f/newtrade/tenderannquainqueryanns/getListByProjectType?projectType=A',
            'http://www.jygzyjy.gov.cn/f/newtrade/tenderannquainqueryanns/getListByProjectType?projectType=D'
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
            html = HTML(text)
            detail = html.xpath('//a')
            for li in detail:
                title = li.xpath('./div/p/text()')[0].replace('\n', '').replace('\r', '') \
                    .replace('\t', '').replace(' ', '').replace('<spanstyle="color:red">', '').replace('</span>', '')
                url_ = li.xpath('./@onclick')[0].replace('loadTender(', '').replace(')', '').replace("'", '').split(',')
                if 'http' not in url_:
                    # 提取出来的code 先经过base64加密 在转成utf-8
                    url_ = 'http://www.jygzyjy.gov.cn/f/newtrade/tenderprojects/{}/flowpage?annogoodsId={}&pageIndex=MQ==' \
                        .format(str(base64.b64encode(url[0].encode('utf-8')), 'utf8'),
                                str(base64.b64encode(url[1].encode('utf-8')), 'utf8'))
                date_Today = li.xpath('./div/span/text()')[0].replace('\n', '').replace('\r', '') \
                    .replace('\t', '').replace(' ', '').replace('(', '').replace(')', '')
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

    # 四川省公共资源交易信息网
    def sichuan(self):
        print('四川省公共资源交易信息网', 'http://ggzyjy.sc.gov.cn')
        url_list = [
            'http://ggzyjy.sc.gov.cn/jyxx/{}.html',
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
                text = tool.requests_get(url.format('transactionInfo'), headers).replace('result(',
                                                                                                   '').replace(');', '')
            else:
                text = tool.requests_get(url.format(page), headers).replace('result(', '').replace(');', '')
            html = HTML(text)
            detail = html.xpath('//*[@id="transactionInfo"]/li')
            for li in detail:
                title = li.xpath('./p/a/text()')[0].replace('\n', '').replace('\r', '') \
                    .replace('\t', '').replace(' ', '')
                url_ = li.xpath('./p/a/@href')[0]
                if 'http' not in url_:
                    url_ = 'http://ggzyjy.sc.gov.cn' + url_
                date_Today = li.xpath('./p/span/text()')[0].replace('\n', '').replace('\r', '') \
                    .replace('\t', '').replace(' ', '').replace('.', '-')
                if '测试' in title or '补遗' in title:
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

    # 威海市公共资源交易网
    def weihai(self):
        print('威海市公共资源交易网', 'http://ggzyjy.weihai.cn')
        url_list = [
            'http://ggzyjy.weihai.cn/EpointWebBuilder/rest/frontAppCustomAction/getPageInfoListNew'
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
            data = {
                'params': '{"siteGuid":"7eb5f7f1-9041-43ad-8e13-8fcb82ea831a","categoryNum":"003","kw":"","startDate":"","endDate":"","pageIndex":' + str(
                    page) + ',"pageSize":12,"area":""}'}
            text = tool.requests_post(url, data, headers)
            detail = json.loads(text)['custom']['infodata']
            for li in detail:
                title = li['title'].replace('\n', '').replace('\r', '') \
                    .replace('\t', '').replace(' ', '').replace('<spanstyle="color:red">', '').replace('</span>', '')
                url_ = li['infourl']
                if 'http' not in url_:
                    url_ = 'http://ggzyjy.weihai.cn' + url_
                date_Today = li['infodate'].replace('\n', '').replace('\r', '') \
                    .replace('\t', '').replace(' ', '').replace('(', '').replace(')', '')
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

    # 安徽省招标投标信息网
    def anhui(self):
        print('安徽省招标投标信息网', 'http://www.ahtba.org.cn')
        url_list = [
            'http://www.ahtba.org.cn/site/trade/affiche/pageList'
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
            data = {"pubTime": "", "tradeType": "", "regionCode": "", "afficheSourceType": "", "afficheTitle": "",
                    "pageNum": page, "pageSize": 10}
            text = tool.requests_post_to(url, data, headers)
            html = HTML(text)
            detail = html.xpath('//*[@class="rightBoxList"]/ul/li')
            for li in detail:
                title = li.xpath('./div[1]/div[1]/a/text()')[0].replace('\n', '').replace('\r', '') \
                    .replace('\t', '').replace(' ', '').replace('<spanstyle="color:red">', '').replace('</span>', '')
                url_ = li.xpath('./div[1]/div[1]/a/@href')[0]
                if 'http' not in url_:
                    url_ = 'http://www.ahtba.org.cn/htmlUrl/trade_/{}/{}.html'.format(self.date, url_.split('/')[-1])
                date_Today = li.xpath('./div[1]/div[2]/text()')[0].replace('\n', '').replace('\r', '') \
                    .replace('\t', '').replace(' ', '').replace('(', '').replace(')', '')
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

    # 宜春市行政审批局
    def yichun(self):
        print('宜春市行政审批局', 'http://xzspj.yichun.gov.cn')
        url_list = [
            'http://xzspj.yichun.gov.cn/api-ajax_list-1.html'
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
            data = 'ajax_type%5B%5D=35_news&ajax_type%5B%5D=45&ajax_type%5B%5D=35&ajax_type%5B%5D=news&ajax_type%5B%5D=Y-m-d&ajax_type%5B%5D=40&ajax_type%5B%5D=20&ajax_type%5B%5D=0&ajax_type%5B8%5D=&is_ds=1'
            text = tool.requests_post(url, data, headers)
            detail = json.loads(text)['data']
            for li in detail:
                title = li['title'].replace('\n', '').replace('\r', '') \
                    .replace('\t', '').replace(' ', '').replace('<spanstyle="color:red">', '').replace('</span>', '')
                url_ = li['url']
                if 'http' not in url_:
                    url_ = 'http://ggzyjy.weihai.cn' + url_
                date_Today = li['inputtime'].replace('\n', '').replace('\r', '') \
                    .replace('\t', '').replace(' ', '').replace('(', '').replace(')', '')
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

    # 宿迁市公共资源交易网
    def suqian(self):
        print('宿迁市公共资源交易网', 'http://ggzy.sqzwfw.gov.cn')
        url_list = [
            'http://ggzy.sqzwfw.gov.cn/WebBuilderDS/jyxxAction.action?cmd=getList&categorynum=001&city=&xmmc=&pageIndex={}&pageSize=15'
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
            detail = json.loads(json.loads(text)['custom'])['Table']
            for li in detail:
                title = li['title'].replace('\n', '').replace('\r', '') \
                    .replace('\t', '').replace(' ', '').replace('<spanstyle="color:red">', '').replace('</span>', '')
                url_ = li['href']
                if 'http' not in url_:
                    url_ = 'http://ggzy.sqzwfw.gov.cn' + url_
                date_Today = li['postdate'].replace('\n', '').replace('\r', '') \
                    .replace('\t', '').replace(' ', '').replace('(', '').replace(')', '')
                if '测试' in title or '合同登记' in title:
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

    # 巴中市公共资源交易网
    def bazhong(self):
        print('巴中市公共资源交易网', 'http://117.172.156.43:82')
        url_list = [
            'http://117.172.156.43:82/pub/showMcontent?mcode=JYGCJS&clicktype=0',
            'http://117.172.156.43:82/pub/showMcontent?mcode=JYZFCG&clicktype=0'
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
            detail = json.loads(text)['data']
            for i in detail:
                for li in i['content']:
                    title = li['mctype'].replace('\n', '').replace('\r', '') \
                        .replace('\t', '').replace(' ', '').replace('<spanstyle="color:red">', '').replace('</span>',
                                                                                                           '')
                    url_ = 'http://117.172.156.43:82/pub/BZ_indexContent_{}.html'.format(li['id'])
                    if 'http' not in url_:
                        url_ = 'http://117.172.156.43:82' + url_
                    date_Today = li['mckeys'].replace('\n', '').replace('\r', '') \
                        .replace('\t', '').replace(' ', '').replace('(', '').replace(')', '')
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

    # 常州市公共资源交易网
    def changzhou(self):
        print('常州市公共资源交易网', 'http://58.216.50.99:8089')
        url_list = [
            'http://58.216.50.99:8089/czggzyweb/jyxxAction.action?cmd=initPageList&pageIndex={}&pageSize=15&siteGuid=7eb5f7f1-9041-43ad-8e13-8fcb82ea831a&cityCode=&type=001&categorynum=&title=&chanquanleibie='
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
            detail = json.loads(json.loads(text)['custom'])['Table']
            for li in detail:
                title = li['title'].replace('\n', '').replace('\r', '') \
                    .replace('\t', '').replace(' ', '').replace('<spanstyle="color:red">', '').replace('</span>', '')
                url_ = li['categorynum'][:-3] + '/' + li['categorynum'] + '/' + li['infodate'].replace('-', '') + '/' + \
                      li['infoid'] + '.html'
                if 'http' not in url_:
                    url_ = 'http://58.216.50.99:8089/jyzx/' + url_
                date_Today = li['infodate'].replace('\n', '').replace('\r', '') \
                    .replace('\t', '').replace(' ', '').replace('(', '').replace(')', '')
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

    # 广东省公共资源交易平台
    def guangdong(self):
        print('广东省公共资源交易平台', 'http://bs.gdggzy.org.cn')
        url_list_to = [
            'http://bs.gdggzy.org.cn/osh-web/project/projectbulletin/bulletinList?orgCode=&tradeTypeId=Construction&queryType=1&tradeItemId=gc_res_bulletin&bulletinName=&startTime=&endTime=&pageNum={}',
            'http://bs.gdggzy.org.cn/osh-web/project/projectbulletin/bulletinList?orgCode=&tradeTypeId=Construction&queryType=3&tradeItemId=gc_res_result&bulletinName=&startTime=&endTime=&pageNum={}',
            'http://bs.gdggzy.org.cn/osh-web/project/projectbulletin/bulletinList?orgCode=&tradeTypeId=GovernmentProcurement&queryType=1&tradeItemId=zf_res_bulletin&bulletinName=&startTime=&endTime=&pageNum={}',
            'http://bs.gdggzy.org.cn/osh-web/project/projectbulletin/bulletinList?orgCode=&tradeTypeId=GovernmentProcurement&queryType=3&tradeItemId=zf_res_result&bulletinName=&startTime=&endTime=&pageNum={}'
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
            text = tool.requests_get(url.format(page), headers).replace('result(', '').replace(');', '')
            html = HTML(text)
            detail = html.xpath('//*[@id="queryForm"]/table/tbody/tr')
            for li in detail:
                title = li.xpath('./td[2]/@title')[0].replace('\n', '').replace('\r', '') \
                    .replace('\t', '').replace(' ', '')
                url_ = li.xpath('./td[2]/a/@href')[0]
                if 'http' not in url_:
                    url_ = 'http://bs.gdggzy.org.cn' + url_
                date_Today = li.xpath('./td[4]/span/text()')[0].replace('\n', '').replace('\r', '') \
                    .replace('\t', '').replace(' ', '').replace('.', '-')
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

    # 广东省政府采购网
    def guangdongzf(self):
        print('广东省政府采购网', 'http://www.ccgp-guangdong.gov.cn')
        url_list = [
            'http://www.ccgp-guangdong.gov.cn/queryMoreInfoList.do?channelCode=-1&issueOrgan=&operateDateFrom=2020-11-15&operateDateTo=2020-12-15&performOrgName=&poor=&purchaserOrgName=&regionIds=&sitewebId=4028889705bebb510105bec068b00003&sitewebName=%E7%9C%81%E7%9B%B4&stockIndexName=&stockNum=&stockTypes=&title=&pageIndex={}&pageSize=15&pointPageIndexId=1',
            'http://www.ccgp-guangdong.gov.cn/queryMoreCityCountyInfoList2.do?channelCode=00051&pageIndex={}&pageSize=15&pointPageIndexId=1',
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
            detail = html.xpath('//*[@class="m_m_c_list"]/li')
            for li in detail:
                title = li.xpath('./a/@title')[0].replace('\n', '').replace('\r', '') \
                    .replace('\t', '').replace(' ', '')
                url_ = li.xpath('./a/@href')[0]
                if 'http' not in url_:
                    url_ = 'http://www.ccgp-guangdong.gov.cn' + url_
                date_Today = li.xpath('./em/text()')[0][:10].replace('\n', '').replace('\r', '') \
                    .replace('\t', '').replace(' ', '').replace('.', '-')
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

    # 广元市公共资源交易网
    def guangyuan(self):
        print('广元市公共资源交易网', 'http://www.gyggzyjy.cn')
        url_list = [
            'http://www.gyggzyjy.cn/ggfwpt/012001/012001001/{}.html',
            'http://www.gyggzyjy.cn/ggfwpt/012001/012001002/{}.html'
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
            detail = html.xpath('/html/body/div[2]/div/div[2]/div[2]/ul/li')
            for li in detail:
                title = li.xpath('./div/a/@title')[0].replace('\n', '').replace('\r', '') \
                    .replace('\t', '').replace(' ', '').replace('<spanstyle="color:red">', '').replace('</span>', '')
                url_ = li.xpath('./div/a/@href')[0]
                if 'http' not in url_:
                    url_ = 'http://www.gyggzyjy.cn' + url_
                date_Today = li.xpath('./span/text()')[0].replace('\n', '').replace('\r', '') \
                    .replace('\t', '').replace(' ', '').replace('(', '').replace(')', '')
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

    # 广安市公共资源交易网
    def guangan(self):
        print('广安市公共资源交易网', 'http://125.66.2.245')
        url_list = [
            'http://125.66.2.245/gasggzy/gcjs/009001/009001001/',
            'http://125.66.2.245/gasggzy/gcjs/009001/009001002/',
            'http://125.66.2.245/gasggzy/gcjs/009001/009001004/',
            'http://125.66.2.245/gasggzy/gcjs/009001/009001005/',
            'http://125.66.2.245/gasggzy/zfcg/010001/010001002/',
            'http://125.66.2.245/gasggzy/zfcg/010001/010001003/',
            'http://125.66.2.245/gasggzy/zfcg/010001/010001004/'
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
            html = HTML(text)
            detail = html.xpath('/html/body/div[4]/div/div/div[2]/div[2]/div/table/tr')
            for li in detail:
                title = li.xpath('./td[2]/a/@title')[0].replace('\n', '').replace('\r', '') \
                    .replace('\t', '').replace(' ', '').replace('<spanstyle="color:red">', '').replace('</span>', '')
                url_ = li.xpath('./td[2]/a/@href')[0]
                if 'http' not in url_:
                    url_ = 'http://125.66.2.245' + url_
                date_Today = li.xpath('./td[3]/text()')[0].replace('\n', '').replace('\r', '') \
                    .replace('\t', '').replace(' ', '').replace('(', '').replace(')', '')
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

    # 庆阳市公共资源交易网
    def qingyang(self):
        print('庆阳市公共资源交易网', 'http://www.qysggzyjy.cn')
        url_list = [
            'http://www.qysggzyjy.cn/f/newtrade/tenderannquainqueryanns/getListByProjectTypePage?projectType=all&purchaseCode=&gsPlatformNavActive=1&projectName=&tradePlatformId=1&tenderMode=1&pageNo={}',
            'http://www.qysggzyjy.cn/f/newtrade/tenderannquainqueryanns/getListByProjectTypePage?projectType=all&purchaseCode=&gsPlatformNavActive=2&projectName=&tradePlatformId=1&tenderMode=1&pageNo={}',
            'http://www.qysggzyjy.cn/f/newtrade/tenderannquainqueryanns/getListByProjectTypePage?projectType=all&purchaseCode=&gsPlatformNavActive=5&projectName=&tradePlatformId=1&tenderMode=1&pageNo={}',
            'http://www.qysggzyjy.cn/f/newtrade/tenderannquainqueryanns/getListByProjectTypePage?projectType=all&purchaseCode=&gsPlatformNavActive=6&projectName=&tradePlatformId=1&tenderMode=1&pageNo={}',
            'http://www.qysggzyjy.cn/f/newtrade/tenderannquainqueryanns/getListByProjectTypePage?projectType=D&purchaseCode=&gsPlatformNavActive=1&projectName=&tradePlatformId=1&tenderMode=1&pageNo={}',
            'http://www.qysggzyjy.cn/f/newtrade/tenderannquainqueryanns/getListByProjectTypePage?projectType=D&purchaseCode=&gsPlatformNavActive=6&projectName=&tradePlatformId=1&tenderMode=1&pageNo={}',
            'http://www.qysggzyjy.cn/f/newtrade/tenderannquainqueryanns/getListByProjectTypePage?projectType=D&purchaseCode=&gsPlatformNavActive=7&projectName=&tradePlatformId=1&tenderMode=1&pageNo={}',
            'http://www.qysggzyjy.cn/f/newtrade/tenderannquainqueryanns/getListByProjectTypePage?projectType=D&purchaseCode=&gsPlatformNavActive=2&projectName=&tradePlatformId=1&tenderMode=1&pageNo={}'
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
            text = tool.requests_get(url.format(page), headers)
            html = HTML(text)
            detail = html.xpath('//a')
            for li in detail:
                title = li.xpath('./li/p/@title')[0].replace('\n', '').replace('\r', '') \
                    .replace('\t', '').replace(' ', '').replace('<spanstyle="color:red">', '').replace('</span>', '')
                url_ = li.xpath('./@href')[0]
                if 'http' not in url_:
                    url_ = 'http://www.qysggzyjy.cn' + url_
                date_Today = li.xpath('./li/span/text()')[0].replace('\n', '').replace('\r', '') \
                    .replace('\t', '').replace(' ', '').replace('(', '').replace(')', '')
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

    # 张掖市公共资源交易网
    def zhangye(self):
        print('张掖市公共资源交易网', 'http://60.165.196.18:8090')
        url_list = [
            'http://60.165.196.18:8090/EpointWebBuilder/jyxxInfoListAction.action?cmd=getInfolist&siteguid=7eb5f7f1-9041-43ad-8e13-8fcb82ea831a&daytime=&jyfrom=&xxtype=001001&jytype=&jyfs=&title=&pageSize=16&pageIndex={}',

            'http://60.165.196.18:8090/EpointWebBuilder/jyxxInfoListAction.action?cmd=getInfolist&siteguid=7eb5f7f1-9041-43ad-8e13-8fcb82ea831a&daytime=&jyfrom=&xxtype=001002&jytype=&jyfs=&title=&pageSize=16&pageIndex={}'

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
            text = tool.requests_get(url.format(page), headers)
            page += 1
            detail = json.loads(json.loads(text)['custom'])['Table']
            for li in detail:
                title = li['realtitle'].replace('\n', '').replace('\r', '') \
                    .replace('\t', '').replace(' ', '').replace('<spanstyle="color:red">', '').replace('</span>', '')
                url_ = li['href']
                if 'http' not in url_:
                    url_ = 'http://60.165.196.18:8090' + url_
                date_Today = li['date'].replace('\n', '').replace('\r', '') \
                    .replace('\t', '').replace(' ', '').replace('(', '').replace(')', '')
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

    # 徐州市公共资源交易网
    def xuzhou(self):
        print('徐州市公共资源交易网', 'http://www.xzcet.com')
        url_list = [
            'http://www.xzcet.com/xzwebnew/ztbpages/MoreinfoZbgg.aspx?categoryNum=046001',
            'http://www.xzcet.com/xzwebnew/ztbpages/MoreinfoZbrgg.aspx?categoryNum=046002'
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
            text = tool.requests_get(url, headers)
            page += 1
            html = HTML(text)
            detail = html.xpath('//*[@id="MoreinfoListJyxx1_DataGrid1"]/tr')
            if '046002' in url:
                detail = html.xpath('//*[@id="moreinfoListZB1_DataGrid1"]/tr')
            for li in detail:
                title = li.xpath('./td[2]/a/@title')[0].replace('\n', '').replace('\r', '') \
                    .replace('\t', '').replace(' ', '').replace('<spanstyle="color:red">', '').replace('</span>', '')
                url_ = li.xpath('./td[2]/a/@href')[0]
                if 'http' not in url_:
                    url_ = 'http://www.xzcet.com' + url_
                date_Today = self.date[:5] + li.xpath('./td[3]/text()')[0].replace('\n', '').replace('\r', '') \
                    .replace('\t', '').replace(' ', '').replace('(', '').replace(')', '')
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

    # 德州市公共资源交易网
    def dezhou(self):
        print('德州市公共资源交易网', 'http://ggzyjy.dezhou.gov.cn:8086')
        url_list = [
            'http://ggzyjy.dezhou.gov.cn:8086/dzggzy/xmxx/004001/moreinfo3.html',
            'http://ggzyjy.dezhou.gov.cn:8086/dzggzy/xmxx/004002/moreinfo4.html'
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
            page += 1
            html = HTML(text)
            detail = html.xpath('//*[@id="categorypagingcontent"]/div/div')
            for ul in detail:
                for li in ul.xpath('./ul/li'):
                    title = li.xpath('./a/@title')[0].replace('\n', '').replace('\r', '') \
                        .replace('\t', '').replace(' ', '').replace('<spanstyle="color:red">', '').replace('</span>',
                                                                                                           '')
                    url_ = li.xpath('./a/@href')[0]
                    if 'http' not in url_:
                        url_ = 'http://ggzyjy.dezhou.gov.cn:8086' + url_
                    date_Today = self.date[:5] + li.xpath('./span/text()')[0].replace('\n', '').replace('\r', '') \
                        .replace('\t', '').replace(' ', '').replace('(', '').replace(')', '')
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

    # 成都市公共资源交易网
    def chengdu(self):
        print('成都市公共资源交易网', 'https://www.cdggzy.com')
        url_list = [
            'https://www.cdggzy.com/site/JSGC/List.aspx',
            'https://www.cdggzy.com/site/Notice/ZFCG/NoticeVersionOneList.aspx'
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
        data = {}
        while True:
            page += 1
            if page == 1:
                text = tool.requests_get(url, headers)
            else:
                text = tool.requests_post(url, data, headers)
            html = HTML(text)
            data['ctl00$ScriptManager1'] = 'ctl00$ContentPlaceHolder1$UpdatePanel1|ctl00$ContentPlaceHolder1$Pager'
            data['__EVENTTARGET'] = 'ctl00$ContentPlaceHolder1$Pager'
            data['__EVENTARGUMENT'] = page + 1
            try:
                data['__VIEWSTATE'] = html.xpath('//*[@id="__VIEWSTATE"]/@value')[0]
            except:
                data['__VIEWSTATE'] = '/' + re.findall('wEPDw.*?__EVENTTARGET', text, re.S)[0] \
                    .replace('|0|hiddenField|__EVENTTARGET', '').replace('|8|hiddenField|__VIEWSTATEGENERATOR|9F052A18',
                                                                         '')
            data['__VIEWSTATEGENERATOR'] = '9F052A18'
            try:
                data['__EVENTVALIDATION'] = html.xpath('//*[@id="__EVENTVALIDATION"]/@value')[0]
            except:
                data['__EVENTVALIDATION'] = re.findall('__EVENTVALIDATION.*?asyncPostBackControlIDs', text, re.S)[0] \
                    .replace('__EVENTVALIDATION|', '').replace('|0|asyncPostBackControlIDs', '')
            data['ctl00$ContentPlaceHolder1$displaytypeval'] = '0'
            data['ctl00$ContentPlaceHolder1$displaystateval'] = '0'
            data['ctl00$ContentPlaceHolder1$dealaddressval'] = '0'
            data['ctl00$ContentPlaceHolder1$keyword'] = ''
            data['__ASYNCPOST'] = 'true'
            detail = html.xpath('//*[@id="contentlist"]/div')
            for li in detail:
                title = li.xpath('./div[2]/a/text()')[0].replace('\n', '').replace('\r', '') \
                    .replace('\t', '').replace(' ', '').replace('<spanstyle="color:red">', '').replace('</span>', '')
                url_ = li.xpath('./div[2]/a/@href')[0]
                if 'http' not in url_:
                    if 'ZFCG' not in url:
                        url_ = 'https://www.cdggzy.com' + url_
                    else:
                        url_ = 'https://www.cdggzy.com/site/Notice/ZFCG/' + url_
                date_Today = li.xpath('./div[3]/div[1]/text()')[0].replace('\n', '').replace('\r', '') \
                    .replace('\t', '').replace(' ', '').replace('(', '').replace(')', '')
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

    # 扬州市公共资源交易网
    def yangzhou(self):
        print('扬州市公共资源交易网', 'http://ggzyjyzx.yangzhou.gov.cn')
        url_list = [
            'http://ggzyjyzx.yangzhou.gov.cn/qtyy/ggzyjyzx/right_list/right_list_jsgc.jsp?t=1607071644393',
            'http://ggzyjyzx.yangzhou.gov.cn/qtyy/ggzyjyzx/right_list/right_list_zfcg.jsp?categorynum=00200&t=1607071671085'
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
        data = {}
        while True:
            page += 1
            text = tool.requests_post(url, data, headers)
            html = HTML(text)
            detail = html.xpath('/html/body/div/form/div/ul/li')
            for li in detail:
                title = li.xpath('./a/text()')[0].replace('\n', '').replace('\r', '') \
                    .replace('\t', '').replace(' ', '').replace('<spanstyle="color:red">', '').replace('</span>', '')
                url_ = li.xpath('./a/@href')[0]
                if 'http' not in url_:
                    url_ = 'http://ggzyjyzx.yangzhou.gov.cn' + url_
                date_Today = li.xpath('./span/text()')[0].replace('\n', '').replace('\r', '') \
                    .replace('\t', '').replace(' ', '').replace('(', '').replace(')', '')
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

    # 攀枝花市公共资源交易网
    def panzhihua(self):
        print('攀枝花市公共资源交易网', 'http://ggzy.panzhihua.gov.cn')
        url_list = [
            'http://ggzy.panzhihua.gov.cn/searchJyxx/list?sousuo_title=&ywlx=&xxlx=&jyptid=&timeid=&startData=&endData=&currentPage={}',
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
        }
        while True:
            page += 1
            text = tool.requests_post(url.format(page), data, headers)
            html = HTML(text)
            detail = html.xpath('//*[@class="jyxx_table"]/ul/li')
            for li in detail:
                try:
                    title = li.xpath('./div[1]/div[1]/a/text()')[0].replace('\n', '').replace('\r', '') \
                        .replace('\t', '').replace(' ', '').replace('<spanstyle="color:red">', '').replace('</span>',
                                                                                                           '')
                    url_ = li.xpath('./div[1]/div[1]/a/@href')[0]
                except:
                    continue
                if 'http' not in url_:
                    url_ = 'http://ggzy.panzhihua.gov.cn' + url_
                date_Today = li.xpath('./div[1]/div[2]/text()')[0].replace('\n', '').replace('\r', '') \
                    .replace('\t', '').replace(' ', '').replace('(', '').replace(')', '')
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

    # 新余市公共资源交易网
    def xinyu(self):
        print('新余市公共资源交易网', 'http://www.xyggzy.cn')
        url_list = [
            'http://www.xyggzy.cn/ggzy/jsgc/010001/MoreInfo.aspx?CategoryNum=010001',
            'http://www.xyggzy.cn/ggzy/jsgc/010002/MoreInfo.aspx?CategoryNum=010002',
            'http://www.xyggzy.cn/ggzy/zfcg/009001/MoreInfo.aspx?CategoryNum=009001',
            'http://www.xyggzy.cn/ggzy/zfcg/009002/MoreInfo.aspx?CategoryNum=009002'
                         ]
        headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Content-Type': 'application/json;charset=UTF-8',
            # 'Cookie': 'JSESSIONID=662863FD2199FBD1672A04A290868047; _CSRFCOOKIE=73F3D7A1BCDCA9001D7B1483A214C4E98DE2528B; EPTOKEN=73F3D7A1BCDCA9001D7B1483A214C4E98DE2528B; oauthClientId=demoClient; oauthPath=http://172.16.5.21:8080/EpointWebBuilder; oauthLoginUrl=http://172.16.5.21:8080/EpointWebBuilder/rest/oauth2/authorize?client_id=demoClient&state=a&response_type=code&scope=user&redirect_uri=; oauthLogoutUrl=http://172.16.5.21:8080/EpointWebBuilder/rest/oauth2/logout?redirect_uri=; noOauthRefreshToken=986d4fe7e5dd29b64c9e7b7a6d66e089; noOauthAccessToken=77c09e0bf98b6220b544961097eed84a; sub_domain_cokie=TiG5CMD9KQ41mmsARPTuAg%3D%3D; region_name=%E4%B9%8C%E9%B2%81%E6%9C%A8%E9%BD%90%E5%B8%82',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',

        }
        url = url_list.pop(0)
        page = 0
        ls = []
        data = {}
        while True:
            page += 1
            text = tool.requests_post(url, data, headers)
            html = HTML(text)
            detail = html.xpath('//*[@id="MoreInfoList1_DataGrid1"]/tr')
            for li in detail:
                try:
                    title = li.xpath('./td[2]/a/@title')[0].replace('\n', '').replace('\r', '') \
                        .replace('\t', '').replace(' ', '').replace('<spanstyle="color:red">', '').replace('</span>',
                                                                                                           '')
                    url_ = li.xpath('./td[2]/a/@href')[0]
                except:
                    continue
                if 'http' not in url_:
                    url_ = 'http://www.xyggzy.cn' + url_
                date_Today = li.xpath('./td[3]/span/text()')[0].replace('\n', '').replace('\r', '') \
                    .replace('\t', '').replace(' ', '').replace('(', '').replace(')', '')
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

    # 无锡市公共资源交易网
    def wuxi(self):
        print('无锡市公共资源交易网', 'http://xzfw.wuxi.gov.cn')
        url_list = [
            'http://xzfw.wuxi.gov.cn/intertidwebapp/xzsp/XzspZyjyzx?chanId=53047&jyly=&pageIndex={}&pageSize=20',
            'http://xzfw.wuxi.gov.cn/intertidwebapp/xzsp/XzspZyjyzx?chanId=53051&jyly=&pageIndex={}&pageSize=20',
            'http://xzfw.wuxi.gov.cn/intertidwebapp/xzsp/XzspZyjyzx?chanId=53054&jyly=&pageIndex={}&pageSize=20',
            'http://xzfw.wuxi.gov.cn/intertidwebapp/xzsp/XzspZyjyzx?chanId=53056&jyly=&pageIndex={}&pageSize=20',
            'http://xzfw.wuxi.gov.cn/intertidwebapp/xzsp/XzspZyjyzx?chanId=53061%2C36908%2C36910%2C36911%2C36912%2C36913%2C36914%2C36918&cgpm=A&jyly=&pageIndex={}&pageSize=20',
            'http://xzfw.wuxi.gov.cn/intertidwebapp/xzsp/XzspZyjyzx?chanId=53062%2C36917%2C36919&cgpm=A&jyly=&pageIndex={}&pageSize=20',
            'http://xzfw.wuxi.gov.cn/intertidwebapp/xzsp/XzspZyjyzx?chanId=53063%2C36915%2C36916&cgpm=A&jyly=&pageIndex={}&pageSize=20',
                         ]
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36',
        }
        url = url_list.pop(0)
        page = 0
        data = {}
        ls = []
        while True:
            page += 1
            text = tool.requests_post(url.format(page), data, headers)
            detail = json.loads(text)['list']
            for li in detail:
                title = li['title'].replace('\n', '').replace('\r', '') \
                    .replace('\t', '').replace(' ', '').replace('<spanstyle="color:red">', '').replace('</span>', '')
                url_ = li['url']
                if 'http' not in url_:
                    url_ = 'http://xzfw.wuxi.gov.cn' + url_
                date_Today = li['writeTime'].replace('\n', '').replace('\r', '') \
                    .replace('\t', '').replace(' ', '').replace('(', '').replace(')', '')
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

    # 日照市公共资源交易网
    def rizhao(self):
        print('日照市公共资源交易网', 'http://ggzyjy.rizhao.gov.cn')
        url_list = [
            'http://ggzyjy.rizhao.gov.cn/rzwz/ShowInfo/MoreJyxxList.aspx?categoryNum=071001001&Paging={}',
            'http://ggzyjy.rizhao.gov.cn/rzwz/ShowInfo/MoreJyxxList.aspx?categoryNum=071001002&Paging={}',
            'http://ggzyjy.rizhao.gov.cn/rzwz/ShowInfo/MoreJyxxList.aspx?categoryNum=071001003&Paging={}',
            'http://ggzyjy.rizhao.gov.cn/rzwz/ShowInfo/MoreJyxxList.aspx?categoryNum=071001004&Paging={}',
            'http://ggzyjy.rizhao.gov.cn/rzwz/ShowInfo/MoreJyxxList.aspx?categoryNum=071002002&Paging={}',
            'http://ggzyjy.rizhao.gov.cn/rzwz/ShowInfo/MoreJyxxList.aspx?categoryNum=071002003&Paging={}',
            'http://ggzyjy.rizhao.gov.cn/rzwz/ShowInfo/MoreJyxxList.aspx?categoryNum=071002004&Paging={}'
        ]
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        }
        url = url_list.pop(0)
        page = 0
        ls = []
        data = {}
        while True:
            page += 1
            text = tool.requests_post(url.format(page), data, headers)
            html = HTML(text)
            detail = html.xpath('//*[@id="DataList1"]/tr')
            for li in detail:
                title = li.xpath('./td/li/a/div[1]/text()')[0].replace('\n', '').replace('\r', '') \
                    .replace('\t', '').replace(' ', '').replace('<spanstyle="color:red">', '').replace('</span>', '')
                url_ = li.xpath('./td/li/a/@href')[0]
                if 'http' not in url_:
                    url_ = 'http://ggzyjy.rizhao.gov.cn/rzwz' + url_[2:]
                date_Today = li.xpath('./td/li/a/div[2]/text()')[0].replace('\n', '').replace('\r', '') \
                    .replace('\t', '').replace(' ', '').replace('(', '').replace(')', '').replace('.', '-')
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

    # 枣庄市公共资源交易网
    def zaozhuang(self):
        print('枣庄市公共资源交易网', 'http://www.zzggzy.com')
        url_list = [
            'http://www.zzggzy.com/TPFront/jyxx/070001/070001001/?Paging={}',
            'http://www.zzggzy.com/TPFront/jyxx/070001/070001004/?Paging={}',
            'http://www.zzggzy.com/TPFront/jyxx/070001/070001005/?Paging={}',
            'http://www.zzggzy.com/TPFront/jyxx/070002/070002001/?Paging={}',
            'http://www.zzggzy.com/TPFront/jyxx/070002/070002002/?Paging={}',
            'http://www.zzggzy.com/TPFront/jyxx/070002/070002003/?Paging={}',
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
        data = {}
        while True:
            page += 1
            text = tool.requests_post(url.format(page), data, headers)
            html = HTML(text)
            detail = html.xpath('/html/body/div[2]/table/tr/td[3]/table/tr[2]/td/table/tr')
            for li in detail:
                try:
                    title = li.xpath('./td[3]/a/text()')[0].replace('\n', '').replace('\r', '') \
                        .replace('\t', '').replace(' ', '').replace('<spanstyle="color:red">', '').replace('</span>',
                                                                                                           '')
                    url_ = li.xpath('./td[3]/a/@href')[0]
                except:
                    continue
                if 'http' not in url_:
                    url_ = 'http://www.zzggzy.com' + url_
                date_Today = li.xpath('./td[4]/text()')[0].replace('\n', '').replace('\r', '') \
                    .replace('\t', '').replace(' ', '').replace('(', '').replace(')', '').replace('.', '-') \
                    .replace('[', '').replace(']', '')
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

    # 江苏省政府采购网
    def jiangsu(self):
        print('江苏省政府采购网', 'http://www.ccgp-jiangsu.gov.cn')
        url_list = [
            'http://www.ccgp-jiangsu.gov.cn/ggxx/gkzbgg/{}.html',
            'http://www.ccgp-jiangsu.gov.cn/ggxx/dylygg/{}.html',
            'http://www.ccgp-jiangsu.gov.cn/ggxx/zbgg/{}.html',
            'http://www.ccgp-jiangsu.gov.cn/ggxx/cgcjgg/{}.html',
            'http://www.ccgp-jiangsu.gov.cn/ggxx/zzgg/{}.html',
            'http://www.ccgp-jiangsu.gov.cn/ggxx/cggzgg/{}.html',
            'http://www.ccgp-jiangsu.gov.cn/ggxx/qtgg/{}.html'
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
            detail = html.xpath('//*[@id="newsList"]/ul/li')
            for li in detail:
                title = li.xpath('./a/text()')[0].replace('\n', '').replace('\r', '') \
                    .replace('\t', '').replace(' ', '')
                url_ = li.xpath('./a/@href')[0]
                if 'http' not in url_:
                    if '../../' in url_:
                        url_ = 'http://www.ccgp-jiangsu.gov.cn' + url_[5:]
                    elif '../' in url_:
                        url_ = '/'.join(url.split('/')[:-1]) + url_[2:]
                    elif './' in url_:
                        url_ = '/'.join(url.split('/')[:-1]) + url_[1:]
                    else:
                        url_ = 'http://www.ccgp-jiangsu.gov.cn' + url_
                date_Today = li.xpath('./text()')[1].replace('\n', '').replace('\r', '') \
                    .replace('\t', '').replace(' ', '').replace('.', '-')
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

    # 江西省公共资源交易网
    def jiangxi(self):
        print('江西省公共资源交易网', 'https://www.jxsggzy.cn')
        url_list = [
            'https://www.jxsggzy.cn/web/jyxx/002001/002001001/{}.html',
            'https://www.jxsggzy.cn/web/jyxx/002001/002001004/{}.html',
            'https://www.jxsggzy.cn/web/jyxx/002002/002002002/{}.html',
            'https://www.jxsggzy.cn/web/jyxx/002002/002002005/{}.html',
            'https://www.jxsggzy.cn/web/jyxx/002006/002006001/{}.html',
            'https://www.jxsggzy.cn/web/jyxx/002006/002006002/{}.html',
            'https://www.jxsggzy.cn/web/jyxx/002006/002006004/{}.html',
            'https://www.jxsggzy.cn/web/jyxx/002006/002006005/{}.html'
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
            detail = html.xpath('//*[@id="gengerlist"]/div[1]/ul/li')
            for li in detail:
                title = li.xpath('./a/text()')[0].replace('\n', '').replace('\r', '') \
                    .replace('\t', '').replace(' ', '').replace('<spanstyle="color:red">', '').replace('</span>', '')
                url_ = li.xpath('./a/@href')[0]
                if 'http' not in url_:
                    url_ = 'https://www.jxsggzy.cn' + url_
                date_Today = li.xpath('./span/text()')[0].replace('\n', '').replace('\r', '') \
                    .replace('\t', '').replace(' ', '').replace('(', '').replace(')', '').replace('.', '-') \
                    .replace('[', '').replace(']', '')
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

    # 泰州市公共资源交易平台
    def taizhou(self):
        print('泰州市公共资源交易平台', 'http://58.222.225.18:8138')
        url_list = [
            'http://58.222.225.18:8138/jyxx/{}.html',
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
            detail = html.xpath('//*[@id="showList"]/tr')
            for li in detail:
                title = li.xpath('./td[2]/a/text()')[0].replace('\n', '').replace('\r', '') \
                    .replace('\t', '').replace(' ', '').replace('<spanstyle="color:red">', '').replace('</span>', '')
                url_ = li.xpath('./td[2]/a/@href')[0]
                if 'http' not in url_:
                    url_ = 'http://58.222.225.18:8138' + url_
                date_Today = li.xpath('./td[3]/text()')[0].replace('\n', '').replace('\r', '') \
                    .replace('\t', '').replace(' ', '').replace('(', '').replace(')', '').replace('.', '-') \
                    .replace('[', '').replace(']', '')
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

    # 泸州市公共资源交易平台
    def luzhou(self):
        print('泸州市公共资源交易平台', 'https://www.lzsggzy.com')
        url_list = [
            'https://www.lzsggzy.com/gcjs/004001/{}.html',
            'https://www.lzsggzy.com/zfcg/005001/{}.html'
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
                if '004001' in url:
                    text = tool.requests_get(url.format('projectBuild'), headers)
                else:
                    text = tool.requests_get(url.format('projectBuild_zfcg'), headers)
            else:
                text = tool.requests_get(url.format(page), headers)
            html = HTML(text)
            detail = html.xpath('//*[@id="jingtai"]/li')
            for li in detail:
                try:
                    title = li.xpath('./a/text()')[1].replace('\n', '').replace('\r', '') \
                        .replace('\t', '').replace(' ', '')
                except:
                    title = li.xpath('./a/text()')[0].replace('\n', '').replace('\r', '') \
                        .replace('\t', '').replace(' ', '')
                url_ = li.xpath('./a/@href')[0]
                if 'http' not in url_:
                    url_ = 'https://www.lzsggzy.com' + url_
                date_Today = li.xpath('./span/text()')[0].replace('\n', '').replace('\r', '') \
                    .replace('\t', '').replace(' ', '').replace('(', '').replace(')', '').replace('.', '-') \
                    .replace('[', '').replace(']', '')
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

    # 济宁市公共资源交易平台
    def jining(self):
        print('济宁市公共资源交易平台', 'http://jnggzy.jnzbtb.cn')
        url_list = [
            '503000',
            '503002',
            '511001',
            '513001',
            '517001',
            '551001',
            '552001',
            '553001'
                         ]
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
        url_to = 'http://jnggzy.jnzbtb.cn/api/services/app/stPrtBulletin/GetBulletinList'
        while True:
            data = {"skipCount": page * 20, "maxResultCount": 20, "tenantId": "3", "categoryCode": url,
                    "FilterText": ""}
            page += 1
            text = tool.requests_post_to(url_to, data, headers)
            detail = json.loads(text)['result']['items']
            for li in detail:
                title = li['title'].replace('\n', '').replace('\r', '') \
                    .replace('\t', '').replace(' ', '')
                url_ = li['id']
                if 'http' not in url_:
                    url_ = 'http://jnggzy.jnzbtb.cn/JiNing/Bulletins/Detail/{}/?CategoryCode={}'.format(url_, url)
                date_Today = li['releaseDate'][:10].replace('\n', '').replace('\r', '') \
                    .replace('\t', '').replace(' ', '').replace('(', '').replace(')', '').replace('.', '-') \
                    .replace('[', '').replace(']', '')
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

    # 湖北省公共资源交易平台
    def hubei(self):
        print('湖北省公共资源交易平台', 'https://www.hbggzyfwpt.cn')
        url_list = [
            'https://www.hbggzyfwpt.cn/jyxx/jsgcXmxx?currentPage={}&area=000&industriesTypeCode=0&scrollValue=1085&projectName=&publishTimeType=1&publishTimeStart=&publishTimeEnd=',
            'https://www.hbggzyfwpt.cn/jyxx/jsgcZbgg?currentPage={}&area=000&industriesTypeCode=0&scrollValue=0&bulletinName=&publishTimeType=1&publishTimeStart=&publishTimeEnd=',
            'https://www.hbggzyfwpt.cn/jyxx/jsgcpbjggs?currentPage={}&area=000&indusTriesTypeCode=0&scrollValue=0&publiCityName=&publishTimeType=1&publishTimeStart=&publishTimeEnd=',
            'https://www.hbggzyfwpt.cn/jyxx/jsgcZbjggs?currentPage={}&area=000&industriesTypeCode=0&scrollValue=0&bulletinName=&publishTimeType=1&publishTimeStart=&publishTimeEnd=',
            'https://www.hbggzyfwpt.cn/jyxx/zfcg/cggg?currentPage={}&area=000&industriesTypeCode=&scrollValue=0&bulletinTitle=&purchaserMode=99&purchaserModeType=0&publishTimeType=1&publishTimeStart=&publishTimeEnd=',
            'https://www.hbggzyfwpt.cn/jyxx/zfcg/gzsxs?currentPage={}&area=000&scrollValue=0&title=&publishTimeType=1&publishTimeStart=&publishTimeEnd='
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
            detail = html.xpath('/html/body/div[3]/div[4]/table/tr')
            for li in detail:
                title = li.xpath('./td[1]/a/text()')[0].replace('\n', '').replace('\r', '') \
                    .replace('\t', '').replace(' ', '')
                url_ = li.xpath('./td[1]/a/@href')[0]
                if 'http' not in url_:
                    if '../../' in url_:
                        url_ = 'https://www.hbggzyfwpt.cn' + url_[5:]
                    elif '../' in url_:
                        url_ = 'https://www.hbggzyfwpt.cn' + url_[2:]
                    elif './' in url_:
                        url_ = 'https://www.hbggzyfwpt.cn' + url_[1:]
                    else:
                        url_ = 'https://www.hbggzyfwpt.cn' + url_
                date_Today = li.xpath('./td[2]/text()')[0].replace('\n', '').replace('\r', '') \
                    .replace('\t', '').replace(' ', '').replace('.', '-')
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

    # 滨州市公共资源交易平台
    def binzhou(self):
        print('滨州市公共资源交易平台', 'http://www.bzggzyjy.cn')
        url_list = [
            'http://www.bzggzyjy.cn/bzweb/002/002004/',
            'http://www.bzggzyjy.cn/bzweb/002/002005/',
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
            html_ = HTML(text)
            detail = html_.xpath('//*[@id="right"]/table/tr')
            for ul in detail:
                for li in ul.xpath('./td/table/tr[2]/td[2]/table/tr'):
                    title = li.xpath('./td[2]/a/@title')[0].replace('\n', '').replace('\r', '') \
                        .replace('\t', '').replace(' ', '')
                    url_ = li.xpath('./td[2]/a/@href')[0]
                    if 'http' not in url_:
                        url_ = 'http://www.bzggzyjy.cn' + url_
                    date_Today = li.xpath('./td[3]/font/text()')[0].replace('\n', '').replace('\r', '') \
                        .replace('\t', '').replace(' ', '').replace('(', '').replace(')', '').replace('.', '-') \
                        .replace('[', '').replace(']', '')
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

    # 漳州市公共资源交易网
    def zhangzhou(self):
        print('漳州市公共资源交易网', 'http://www.zzgcjyzx.com')
        url_list = [
            'http://www.zzgcjyzx.com/Front/gcxx/002001/002001001/?Paging={}',
            'http://www.zzgcjyzx.com/Front/gcxx/002001/002001002/?pageing={}',
            'http://www.zzgcjyzx.com/Front/gcxx/002001/002001003/?pageing={}',
            'http://www.zzgcjyzx.com/Front/gcxx/002001/002001005/?pageing={}',
            'http://www.zzgcjyzx.com/Front/gcxx/002002/002002001/?pageing={}',
            'http://www.zzgcjyzx.com/Front/gcxx/002002/002002006/?pageing={}',
            'http://www.zzgcjyzx.com/Front/gcxx/002002/002002002/?pageing={}'
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
            detail = html.xpath('/html/body/table/tr/td[2]/table/tr/td[4]/table/tr[2]/td/table/tr')
            for li in detail:
                title = li.xpath('./td[2]/a/@title')[0].replace('\n', '').replace('\t', '').replace(' ', '').replace(
                    '\r', '')
                url_ = li.xpath('./td[2]/a/@href')[0]
                url_domain = 'http://www.zzgcjyzx.com'
                if 'http' not in url_:
                    if '../../' in url_:
                        url_ = url_domain + url_[5:]
                    elif '../' in url_:
                        url_ = url_domain + url_[2:]
                    elif './' in url_:
                        url_ = url_domain + url_[1:]
                    else:
                        url_ = url_domain + url_
                date_Today = li.xpath('./td[3]/text()')[0].replace('\n', '').replace('\t', '').replace(' ', '').replace(
                    '\r', '')
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

    # 潍坊市公共资源交易平台
    def weifang(self):
        print('潍坊市公共资源交易平台', 'http://ggzy.weifang.gov.cn')
        url_list = [
            'http://ggzy.weifang.gov.cn/wfggzy/showinfo/moreinfo_gg.aspx?address=&type=&categorynum=004012001&Paging={}',
            'http://ggzy.weifang.gov.cn/wfggzy/showinfo/moreinfo_gg.aspx?address=&type=&categorynum=004012002&Paging={}',
            'http://ggzy.weifang.gov.cn/wfggzy/showinfo/moreinfo_gg.aspx?address=&type=&categorynum=004012006&Paging={}',
            'http://ggzy.weifang.gov.cn/wfggzy/showinfo/moreinfo_gg.aspx?address=&type=&categorynum=004012007&Paging={}',
            'http://ggzy.weifang.gov.cn/wfggzy/showinfo/moreinfo_gg_zfcgtwo.aspx?address=&type=&categorynum=004002001&Paging={}',
            'http://ggzy.weifang.gov.cn/wfggzy/showinfo/moreinfo_gg_zfcg.aspx?address=&type=&categorynum=004002011&Paging={}',
            'http://ggzy.weifang.gov.cn/wfggzy/showinfo/moreinfo_gg_zfcg.aspx?address=&type=&categorynum=004002012&Paging={}',
            'http://ggzy.weifang.gov.cn/wfggzy/showinfo/moreinfo_gg_zfcg.aspx?address=&type=&categorynum=004002016&Paging={}'
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
            html_ = HTML(text)
            detail = html_.xpath('//*[@id="form1"]/div[3]/div[2]/table/tbody/tr')
            for li in detail:
                title = li.xpath('./td[3]/span/a/text()')[0].replace('\n', '').replace('\r', '') \
                    .replace('\t', '').replace(' ', '')
                url_ = li.xpath('./td[3]/span/a/@href')[0]
                if 'http' not in url_:
                    url_ = 'http://ggzy.weifang.gov.cn' + url_
                date_Today = li.xpath('./td[4]/span/text()')[0].replace('\n', '').replace('\r', '') \
                    .replace('\t', '').replace(' ', '').replace('(', '').replace(')', '').replace('.', '-') \
                    .replace('[', '').replace(']', '')
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

    # 烟台市公共资源交易平台
    def yantai(self):
        print('烟台市公共资源交易平台', 'http://ggzyjy.yantai.gov.cn')
        url_list = [
            'http://ggzyjy.yantai.gov.cn/jyxxgc/index_{}.jhtml',
            'http://ggzyjy.yantai.gov.cn/jyxxzc/index_{}.jhtml',
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
            html_ = HTML(text)
            detail = html_.xpath('//*[@class="article-list2"]/li')
            for li in detail:
                title = li.xpath('./div[1]/a/@title')[0].replace('\n', '').replace('\r', '') \
                    .replace('\t', '').replace(' ', '')
                url_ = li.xpath('./div[1]/a/@href')[0]
                if 'http' not in url_:
                    url_ = 'http://ggzyjy.yantai.gov.cn' + url_
                try:
                    date_Today = li.xpath('./div[1]/div/text()')[0].replace('\n', '').replace('\r', '') \
                        .replace('\t', '').replace(' ', '').replace('(', '').replace(')', '').replace('.', '-') \
                        .replace('[', '').replace(']', '').replace('.', '-')
                except:
                    date_Today = li.xpath('./div[1]/span/text()')[0][:10].replace('\n', '').replace('\r', '') \
                        .replace('\t', '').replace(' ', '').replace('(', '').replace(')', '').replace('.', '-') \
                        .replace('[', '').replace(']', '').replace('.', '-')
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

    # 甘肃省公共资源交易局
    def gansu(self):
        print('甘肃省公共资源交易局', 'https://ggzyjy.gansu.gov.cn')
        url_list = [
            'https://ggzyjy.gansu.gov.cn/f/newprovince/annogoods/getAnnoList?pageNo={}&pageSize=&area=620000&projecttype=I&prjpropertynewI=I&prjpropertynewA=A&prjpropertynewD=D&prjpropertynewC=C&prjpropertynewB=B&prjpropertynewE=E&projectname=',
            'https://ggzyjy.gansu.gov.cn/f/newprovince/annogoods/getAnnoList?pageNo={}&pageSize=&area=620000&projecttype=A&prjpropertynewI=I&prjpropertynewA=A&prjpropertynewD=D&prjpropertynewC=C&prjpropertynewB=B&prjpropertynewE=E&projectname=',
            'https://ggzyjy.gansu.gov.cn/f/newprovince/annogoods/getAnnoList?pageNo={}&pageSize=&area=620000&projecttype=D&prjpropertynewI=I&prjpropertynewA=A&prjpropertynewD=D&prjpropertynewC=C&prjpropertynewB=B&prjpropertynewE=E&projectname=',
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
            text = tool.requests_get(url.format(page), headers)
            page += 1
            html = HTML(text)
            detail = html.xpath('//*[@class="sTradingInformationSelectedBtoList"]/dl')
            for li in detail:
                title = li.xpath('./dd/p/a/text()')[0].replace('\n', '').replace('\r', '') \
                    .replace('\t', '').replace(' ', '')
                url_ = li.xpath('./dd/p/a/@href')[0]
                if 'http' not in url_:
                    if '../../' in url_:
                        url_ = 'https://ggzyjy.gansu.gov.cn' + url_[5:]
                    elif '../' in url_:
                        url_ = 'https://ggzyjy.gansu.gov.cn' + url_[2:]
                    elif './' in url_:
                        url_ = 'https://ggzyjy.gansu.gov.cn' + url_[1:]
                    else:
                        url_ = 'https://ggzyjy.gansu.gov.cn' + url_
                date_Today = li.xpath('./dd/i/text()')[0].replace('\n', '').replace('\r', '') \
                    .replace('\t', '').replace(' ', '').replace('.', '-')
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

    # 白银市公共资源交易平台
    def baiyin(self):
        print('白银市公共资源交易平台', 'http://ggzyjy.baiyin.gov.cn')
        url_list = [
            'http://ggzyjy.baiyin.gov.cn/ajax/InfoPage_TradeInfomation,App_Web_5301wvhd.ashx?_method=getTradeDataList&_session=no'
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
            data = 'infoType=0\ncurr=' + str(
                page) + '\nkeywords=\nqueryStr=and  a.PrjPropertyNew in (1,2,3,21,22,23,24,5,6,12,13,14,15,16,17,18,19,20,4,7,8,9,11,41,31,44,43,551,552,553,0,441,442,443,0,331,332,333,0,2000) and a.Field1 in(3259,2955,2956,2957,2958,2959,2960)'
            text = tool.requests_post(url, data, headers)
            html_ = HTML(text)
            detail = html_.xpath('//li')
            for li in detail:
                title = li.xpath('./a/@title')[0].replace('\n', '').replace('\r', '') \
                    .replace('\t', '').replace(' ', '')
                url_ = li.xpath('./a/@href')[0]
                if 'http' not in url_:
                    url_ = 'http://ggzyjy.baiyin.gov.cn' + url_[2:]
                date_Today = li.xpath('./span/text()')[0].replace('\n', '').replace('\r', '') \
                    .replace('\t', '').replace(' ', '').replace('(', '').replace(')', '').replace('.', '-') \
                    .replace('[', '').replace(']', '').replace('.', '-')
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

    # 盐城市公共资源交易平台
    def yancheng(self):
        print('盐城市公共资源交易平台', 'http://112.24.96.37:9890')
        url_list = [
            'http://112.24.96.37:9890/EpointWebBuilder/xyxxInfoListAction.action?cmd=getInfolist&categorynum=003&city=&title=&pageSize=20&pageIndex={}',
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
            text = tool.requests_get(url.format(page), headers)
            page += 1
            detail = json.loads(json.loads(text)['custom'])['Table']
            for li in detail:
                title = li['title'].replace('\n', '').replace('\r', '') \
                    .replace('\t', '').replace(' ', '')
                url_ = li['href']
                if 'http' not in url_:
                    url_ = 'http://112.24.96.37:9890' + url_
                date_Today = li['infodate'].replace('\n', '').replace('\r', '') \
                    .replace('\t', '').replace(' ', '').replace('(', '').replace(')', '').replace('.', '-') \
                    .replace('[', '').replace(']', '').replace('.', '-')
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

    # 眉山市公共资源交易平台
    def meishan(self):
        print('眉山市公共资源交易平台', 'http://www.msggzy.org.cn')
        url_list = [
            'http://www.msggzy.org.cn/front/jsgc/001002/?Paging={}',
            'http://www.msggzy.org.cn/front/jsgc/001013/?Paging={}',
            'http://www.msggzy.org.cn/front/zfcg/002001/?Paging={}',
            'http://www.msggzy.org.cn/front/zfcg/002003/?Paging={}'
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
            text = tool.requests_get(url.format(page), headers)
            page += 1
            html_ = HTML(text)
            detail = html_.xpath('/html/body/div[2]/div[2]/div/div/div/div[1]/table/tr')
            for li in detail:
                title = li.xpath('./td[1]/a/@title')[0].replace('\n', '').replace('\r', '') \
                    .replace('\t', '').replace(' ', '')
                url_ = li.xpath('./td[1]/a/@href')[0]
                if 'http' not in url_:
                    url_ = 'http://www.msggzy.org.cn' + url_
                date_Today = li.xpath('./td[2]/text()')[0].replace('\n', '').replace('\r', '') \
                    .replace('\t', '').replace(' ', '').replace('(', '').replace(')', '').replace('.', '-') \
                    .replace('[', '').replace(']', '').replace('.', '-')
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

    # 福州市公共资源交易网
    def fuzhou(self):
        print('福州市公共资源交易网', 'http://fzsggzyjyfwzx.cn')
        url_list = [
            'http://fzsggzyjyfwzx.cn/jyxxzbgg/index_{}.jhtml', 'http://fzsggzyjyfwzx.cn/jyxxgcbc/index_{}.jhtml',
            'http://fzsggzyjyfwzx.cn/jyxxkbjl/index_{}.jhtml', 'http://fzsggzyjyfwzx.cn/jyxxzsjg/index_{}.jhtml',
            'http://fzsggzyjyfwzx.cn/jyxxzbgs/index_{}.jhtml', 'http://fzsggzyjyfwzx.cn/jyxxcggg/index_{}.jhtml',
            'http://fzsggzyjyfwzx.cn/jyxxgzsx/index_{}.jhtml', 'http://fzsggzyjyfwzx.cn/jyxxcjgg/index_{}.jhtml'
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
                text = tool.requests_get(url.format('about-trade'), headers)
            else:
                text = tool.requests_get(url.format(page), headers)
            html = HTML(text)
            detail = html.xpath('/html/body/div[1]/div[4]/div[3]/div/ul/li')
            for li in detail:
                title = li.xpath('string(./div/a)').replace('\n', '').replace('\t', '').replace(' ', '')
                url_ = li.xpath('./div/a/@href')[0]
                date_Today = li.xpath('./div/div/text()')[0].replace('\n', '').replace('\t', '').replace(' ', '')
                if '测试' in title:
                    continue
                url_domain = 'http://fzsggzyjyfwzx.cn'
                if 'http' not in url_:
                    if '../../' in url_:
                        url_ = url_domain + url_[5:]
                    elif '../' in url_:
                        url_ = url_domain + url_[2:]
                    elif './' in url_:
                        url_ = url_domain + url_[1:]
                    else:
                        url_ = url_domain + url_
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

    # 聊城市公共资源交易平台
    def liaocheng(self):
        print('聊城市公共资源交易平台', 'http://www.lcsggzyjy.cn')
        url_list = [
            'http://www.lcsggzyjy.cn/lcweb/jyxx/079001/079001001/',
            'http://www.lcsggzyjy.cn/lcweb/jyxx/079001/079001002/',
            'http://www.lcsggzyjy.cn/lcweb/jyxx/079001/079001003/',
            'http://www.lcsggzyjy.cn/lcweb/jyxx/079001/079001005/',
            'http://www.lcsggzyjy.cn/lcweb/jyxx/079001/079001006/',
            'http://www.lcsggzyjy.cn/lcweb/jyxx/079002/079002001/',
            'http://www.lcsggzyjy.cn/lcweb/jyxx/079002/079002002/',
            'http://www.lcsggzyjy.cn/lcweb/jyxx/079002/079002003/',
            'http://www.lcsggzyjy.cn/lcweb/jyxx/079002/079002004/'
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
            text = tool.requests_get(url, headers)
            page += 1
            html_ = HTML(text)
            detail = html_.xpath('//*[@class="content"]/table/tr')
            for ul in detail:
                for li in ul.xpath('./td/table/tr[2]/td[2]/table/tr'):
                    title = li.xpath('./td[2]/a/@title')[0].replace('\n', '').replace('\r', '') \
                        .replace('\t', '').replace(' ', '')
                    url_ = li.xpath('./td[2]/a/@href')[0]
                    if 'http' not in url_:
                        url_ = 'http://www.lcsggzyjy.cn' + url_
                    date_Today = li.xpath('./td[3]/font/text()')[0].replace('\n', '').replace('\r', '') \
                        .replace('\t', '').replace(' ', '').replace('(', '').replace(')', '').replace('.', '-') \
                        .replace('[', '').replace(']', '').replace('.', '-')
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

    # 莆田市公共资源交易网
    def putian(self):
        print('莆田市公共资源交易网', 'http://ggzyjy.xzfwzx.putian.gov.cn')
        url_list = [
            'http://ggzyjy.xzfwzx.putian.gov.cn/fwzx/wjzyzx/004003/004003002/?Paging={}',
            'http://ggzyjy.xzfwzx.putian.gov.cn/fwzx/wjzyzx/004003/004003004/?Paging={}',
            'http://ggzyjy.xzfwzx.putian.gov.cn/fwzx/wjzyzx/004003/004003006/?Paging={}',
            'http://ggzyjy.xzfwzx.putian.gov.cn/fwzx/wjzyzx/004002/004002005/004002005002/?Paging={}',
            'http://ggzyjy.xzfwzx.putian.gov.cn/fwzx/wjzyzx/004002/004002005/004002005003/?Paging={}',
            'http://ggzyjy.xzfwzx.putian.gov.cn/fwzx/wjzyzx/004002/004002005/004002005004/?Paging={}',
            'http://ggzyjy.xzfwzx.putian.gov.cn/fwzx/wjzyzx/004002/004002005/004002005005/?Paging={}',
            'http://ggzyjy.xzfwzx.putian.gov.cn/fwzx/wjzyzx/004002/004002005/004002005006/?Paging={}',
            'http://ggzyjy.xzfwzx.putian.gov.cn/fwzx/wjzyzx/004002/004002005/004002005007/?Paging={}',
            'http://ggzyjy.xzfwzx.putian.gov.cn/fwzx/wjzyzx/004002/004002005/004002005008/?Paging={}',
            'http://ggzyjy.xzfwzx.putian.gov.cn/fwzx/wjzyzx/004002/004002005/004002005009/?Paging={}',
            'http://ggzyjy.xzfwzx.putian.gov.cn/fwzx/wjzyzx/004002/004002007/?Paging={}',
            'http://ggzyjy.xzfwzx.putian.gov.cn/fwzx/wjzyzx/004002/004002010/004002010002/?Paging={}',
            'http://ggzyjy.xzfwzx.putian.gov.cn/fwzx/wjzyzx/004002/004002010/004002010003/?Paging={}',
            'http://ggzyjy.xzfwzx.putian.gov.cn/fwzx/wjzyzx/004002/004002010/004002010004/?Paging={}',
            'http://ggzyjy.xzfwzx.putian.gov.cn/fwzx/wjzyzx/004002/004002010/004002010005/?Paging={}',
            'http://ggzyjy.xzfwzx.putian.gov.cn/fwzx/wjzyzx/004002/004002010/004002010006/?Paging={}',
            'http://ggzyjy.xzfwzx.putian.gov.cn/fwzx/wjzyzx/004002/004002010/004002010007/?Paging={}',
            'http://ggzyjy.xzfwzx.putian.gov.cn/fwzx/wjzyzx/004002/004002010/004002010008/?Paging={}',
            'http://ggzyjy.xzfwzx.putian.gov.cn/fwzx/wjzyzx/004002/004002010/004002010009/?Paging={}',
            'http://ggzyjy.xzfwzx.putian.gov.cn/fwzx/wjzyzx/004002/004002022/?Paging={}',
            'http://ggzyjy.xzfwzx.putian.gov.cn/fwzx/wjzyzx/004002/004002008/?Paging={}'
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
            detail = html.xpath('//*[@id="right"]/ul/li')
            for li in detail:
                title = li.xpath('./a/@title')[0].replace('\n', '').replace('\t', '').replace(' ', '').replace('\r', '')
                url_ = li.xpath('./a/@href')[0]
                date_Today = li.xpath('./span/text()')[0].replace('\n', '').replace('\t', '').replace(' ', '').replace(
                    '\r', '')
                if '测试' in title:
                    continue
                url_domain = 'http://ggzyjy.xzfwzx.putian.gov.cn'
                if 'http' not in url_:
                    if '../../' in url_:
                        url_ = url_domain + url_[5:]
                    elif '../' in url_:
                        url_ = url_domain + url_[2:]
                    elif './' in url_:
                        url_ = url_domain + url_[1:]
                    else:
                        url_ = url_domain + url_
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

    # 西安市公共资源交易中心
    def xian(self):
        print('西安市公共资源交易中心', 'http://www.xacin.com.cn')
        url_list = [
            'http://www.xacin.com.cn/XianGcjy/web/tender/shed_gc.jsp?gc_type=5&page={}',
            'http://www.xacin.com.cn/XianGcjy/web/tender/shed_gc.jsp?gc_type=3&page={}',
            'http://www.xacin.com.cn/XianGcjy/web/tender/shed_gc.jsp?gc_type=6&page={}'
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
            detail = html.xpath('/html/body/table[7]/tr[1]/td[2]/table[2]/tr')
            for li in detail:
                try:
                    title = li.xpath('./td[1]/a/@title')[0].replace('\n', '').replace('\r', '') \
                        .replace('\t', '').replace(' ', '')
                    url_ = li.xpath('./td[1]/a/@href')[0]
                except:
                    continue
                if 'http' not in url_:
                    if '../../' in url_:
                        url_ = 'http://www.xacin.com.cn/XianGcjy/web/tender/' + url_[5:]
                    elif '../' in url_:
                        url_ = 'http://www.xacin.com.cn/XianGcjy/web/tender/' + url_[2:]
                    elif './' in url_:
                        url_ = 'http://www.xacin.com.cn/XianGcjy/web/tender/' + url_[1:]
                    else:
                        url_ = 'http://www.xacin.com.cn/XianGcjy/web/tender/' + url_
                date_Today = li.xpath('./td[2]/text()')[0].replace('\n', '').replace('\r', '') \
                    .replace('\t', '').replace(' ', '').replace('.', '-')
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

    # 西藏公共资源交易信息网
    def xizang(self):
        print('西藏公共资源交易信息网', 'http://www.xzggzy.gov.cn:9090')
        url_list = [
            'http://www.xzggzy.gov.cn:9090/gcjs/index_{}.jhtml',
            'http://www.xzggzy.gov.cn:9090/jyjggg/index_{}.jhtml',
            'http://www.xzggzy.gov.cn:9090/zbwjcq/index_{}.jhtml',
            'http://www.xzggzy.gov.cn:9090/zfcg/index_{}.jhtml',
            'http://www.xzggzy.gov.cn:9090/zbgg/index_{}.jhtml',
            'http://www.xzggzy.gov.cn:9090/gzsx/index_{}.jhtml'
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
            detail = html.xpath('//*[@class="article-list-old"]/li')
            for li in detail:
                title = li.xpath('./a/@title')[0].replace('\n', '').replace('\r', '') \
                    .replace('\t', '').replace(' ', '')
                url_ = li.xpath('./a/@href')[0]
                if 'http' not in url_:
                    if '../../' in url_:
                        url_ = 'http://www.xzggzy.gov.cn:9090' + url_[5:]
                    elif '../' in url_:
                        url_ = 'http://www.xzggzy.gov.cn:9090' + url_[2:]
                    elif './' in url_:
                        url_ = 'http://www.xzggzy.gov.cn:9090' + url_[1:]
                    else:
                        url_ = 'http://www.xzggzy.gov.cn:9090' + url_
                date_Today = li.xpath('./div/text()')[0][:10].replace('\n', '').replace('\r', '') \
                    .replace('\t', '').replace(' ', '').replace('.', '-')
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

    # 西藏自治区政府采购网
    def xizangzf(self):
        print('西藏自治区政府采购网', 'http://www.ccgp-xizang.gov.cn')
        url_list = [
            'http://www.ccgp-xizang.gov.cn/shopHome/morePolicyNews.action?categoryId=124,125&currentPage={}',
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
            detail = html.xpath('//*[@id="news_div"]/ul/li')
            for li in detail:
                title = li.xpath('./div[1]/a/text()')[0].replace('\n', '').replace('\r', '') \
                    .replace('\t', '').replace(' ', '')
                url_ = li.xpath('./div[1]/a/@href')[0]
                if 'http' not in url_:
                    if '../../' in url_:
                        url_ = 'http://www.ccgp-xizang.gov.cn' + url_[5:]
                    elif '../' in url_:
                        url_ = 'http://www.ccgp-xizang.gov.cn' + url_[2:]
                    elif './' in url_:
                        url_ = 'http://www.ccgp-xizang.gov.cn' + url_[1:]
                    else:
                        url_ = 'http://www.ccgp-xizang.gov.cn' + url_
                date_Today = li.xpath('./span/text()')[0][:10].replace('\n', '').replace('\r', '') \
                    .replace('\t', '').replace(' ', '').replace('.', '-')
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

    # 达州市公共资源交易平台
    def dazhou(self):
        print('达州市公共资源交易平台', 'http://www.dzggzy.cn')
        url_list = [
            'http://www.dzggzy.cn/dzsggzy/jyxx/025001/025001001/?Paging={}',
            'http://www.dzggzy.cn/dzsggzy/jyxx/025001/025001015/?Paging={}',
            'http://www.dzggzy.cn/dzsggzy/jyxx/025001/025001004/?Paging={}',
            'http://www.dzggzy.cn/dzsggzy/jyxx/025002/025002001/?Paging={}',
            'http://www.dzggzy.cn/dzsggzy/jyxx/025002/025002003/?Paging={}',
            'http://www.dzggzy.cn/dzsggzy/jyxx/025002/025002005/?Paging={}',
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
            text = tool.requests_get(url.format(page), headers)
            page += 1
            html_ = HTML(text)
            detail = html_.xpath('/html/body/div[3]/div/div[2]/div[2]/div/div[1]/table/tr')
            for li in detail:
                title = li.xpath('./td[2]/a/@title')[0].replace('\n', '').replace('\r', '') \
                    .replace('\t', '').replace(' ', '')
                url_ = li.xpath('./td[2]/a/@href')[0]
                if 'http' not in url_:
                    url_ = 'http://www.dzggzy.cn' + url_
                date_Today = li.xpath('./td[3]/text()')[0].replace('\n', '').replace('\r', '') \
                    .replace('\t', '').replace(' ', '').replace('(', '').replace(')', '').replace('.', '-') \
                    .replace('[', '').replace(']', '').replace('.', '-')
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

    # 陇南市公共资源交易平台
    def longnan(self):
        print('陇南市公共资源交易平台', 'http://www.lnsggzyjy.cn')
        url_list = [
            'http://www.lnsggzyjy.cn/jyxx/{}.html',
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
            html_ = HTML(text)
            detail = html_.xpath('//*[@class="ewb-info-items"]/li')
            for li in detail:
                title = li.xpath('./div/a/@title')[0].replace('\n', '').replace('\r', '') \
                    .replace('\t', '').replace(' ', '')
                url_ = li.xpath('./div/a/@href')[0]
                if 'http' not in url_:
                    url_ = 'http://www.lnsggzyjy.cn' + url_
                date_Today = li.xpath('./span/text()')[0].replace('\n', '').replace('\r', '') \
                    .replace('\t', '').replace(' ', '').replace('(', '').replace(')', '').replace('.', '-') \
                    .replace('[', '').replace(']', '').replace('.', '-')
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

    # 陕西省公共资源交易中心
    def shanxi(self):
        print('陕西省公共资源交易中心', 'http://www.sxggzyjy.cn')
        url_list = [
            'http://www.sxggzyjy.cn/jydt/001001/001001001/{}.html',
            'http://www.sxggzyjy.cn/jydt/001001/001001004/{}.html',
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
                text = tool.requests_get(url.format('subPage_jyxx'), headers)
            else:
                text = tool.requests_get(url.format(page), headers)
            html = HTML(text)
            detail = html.xpath('//*[@class="ewb-list"]/li')
            for li in detail:
                title = li.xpath('./a/@title')[0].replace('\n', '').replace('\r', '') \
                    .replace('\t', '').replace(' ', '')
                url_ = li.xpath('./a/@href')[0]
                if 'http' not in url_:
                    if '../../' in url_:
                        url_ = 'http://www.sxggzyjy.cn' + url_[5:]
                    elif '../' in url_:
                        url_ = 'http://www.sxggzyjy.cn' + url_[2:]
                    elif './' in url_:
                        url_ = 'http://www.sxggzyjy.cn' + url_[1:]
                    else:
                        url_ = 'http://www.sxggzyjy.cn' + url_
                date_Today = li.xpath('./span/text()')[0].replace('\n', '').replace('\r', '') \
                    .replace('\t', '').replace(' ', '').replace('.', '-')
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

    # 雅安市公共资源交易平台
    def yaan(self):
        print('雅安市公共资源交易平台', 'http://www.yaggzy.org.cn')
        url_list = [
            'http://www.yaggzy.org.cn/jyxx/jsgcBgtz',
            'http://www.yaggzy.org.cn/jyxx/jsgcpbjggs',
            'http://www.yaggzy.org.cn/jyxx/jsgcZbjggs',
            'http://www.yaggzy.org.cn/jyxx/zfcg/zbjggs'
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
            html_ = HTML(text)
            if 'jsgcZbjggs' in url:
                detail = html_.xpath('/html/body/div[6]/div[2]/ul/li[3]/table/tr')
            else:
                detail = html_.xpath('//*[@id="p2"]/tr')
            for li in detail:
                try:
                    title = li.xpath('./td[3]/a/@title')[0].replace('\n', '').replace('\r', '') \
                        .replace('\t', '').replace(' ', '')
                    url_ = li.xpath('./td[3]/a/@href')[0]
                except:
                    continue
                if 'http' not in url_:
                    url_ = 'http://www.yaggzy.org.cn' + url_
                date_Today = li.xpath('./td[4]/text()')[0].replace('\n', '').replace('\r', '') \
                    .replace('\t', '').replace(' ', '').replace('(', '').replace(')', '').replace('.', '-') \
                    .replace('[', '').replace(']', '').replace('.', '-')
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

    # 龙岩市公共资源交易网
    def longyan(self):
        print('龙岩市公共资源交易网', 'https://www.lyggzy.com.cn')
        url_list = [
            'https://www.lyggzy.com.cn/lyztb/gcjs/081001/081001003/081001003001/?pageing={}',
            'https://www.lyggzy.com.cn/lyztb/gcjs/081001/081001003/081001003002/?pageing={}',
            'https://www.lyggzy.com.cn/lyztb/gcjs/081001/081001010/?pageing={}',
            'https://www.lyggzy.com.cn/lyztb/gcjs/081001/081001005/?pageing={}',
            'https://www.lyggzy.com.cn/lyztb/gcjs/081008/081008001/081008001001/?pageing={}',
            'https://www.lyggzy.com.cn/lyztb/gcjs/081008/081008001/081008001003/?pageing={}',
            'https://www.lyggzy.com.cn/lyztb/gcjs/081008/081008001/081008001004/?pageing={}',
            'https://www.lyggzy.com.cn/lyztb/gcjs/081008/081008002/081008002001/?pageing={}',
            'https://www.lyggzy.com.cn/lyztb/gcjs/081008/081008002/081008002003/?pageing={}',
            'https://www.lyggzy.com.cn/lyztb/gcjs/081008/081008002/081008002004/?pageing={}',
            'https://www.lyggzy.com.cn/lyztb/gcjs/081008/081008003/081008003001/?pageing={}',
            'https://www.lyggzy.com.cn/lyztb/gcjs/081008/081008003/081008003003/?pageing={}',
            'https://www.lyggzy.com.cn/lyztb/gcjs/081008/081008003/081008003004/?pageing={}',
            'https://www.lyggzy.com.cn/lyztb/gcjs/081008/081008004/081008004001/?pageing={}',
            'https://www.lyggzy.com.cn/lyztb/gcjs/081008/081008004/081008004003/?pageing={}',
            'https://www.lyggzy.com.cn/lyztb/gcjs/081008/081008004/081008004004/?pageing={}',
            'https://www.lyggzy.com.cn/lyztb/gcjs/081008/081008005/081008005001/?pageing={}',
            'https://www.lyggzy.com.cn/lyztb/gcjs/081008/081008005/081008005003/?pageing={}',
            'https://www.lyggzy.com.cn/lyztb/gcjs/081008/081008005/081008005004/?pageing={}',
            'https://www.lyggzy.com.cn/lyztb/gcjs/081008/081008006/081008006001/?pageing={}',
            'https://www.lyggzy.com.cn/lyztb/gcjs/081008/081008006/081008006003/?pageing={}',
            'https://www.lyggzy.com.cn/lyztb/gcjs/081008/081008006/081008006004/?pageing={}',
            'https://www.lyggzy.com.cn/lyztb/gcjs/081008/081008007/081008007001/?pageing={}',
            'https://www.lyggzy.com.cn/lyztb/gcjs/081008/081008007/081008007003/?pageing={}',
            'https://www.lyggzy.com.cn/lyztb/gcjs/081008/081008007/081008007004/?pageing={}',
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
            detail = html.xpath('/html/body/div/div[2]/ul[1]/li')
            for li in detail:
                title = li.xpath('./a/text()')[0].replace('\n', '').replace('\t', '').replace(' ', '').replace('\r', '')
                url_ = li.xpath('./a/@href')[0]
                date_Today = li.xpath('./span/text()')[0].replace('\n', '').replace('\t', '').replace(' ', '').replace(
                    '\r', '')
                if '测试' in title:
                    continue
                url_domain = 'https://www.lyggzy.com.cn'
                if 'http' not in url_:
                    if '../../' in url_:
                        url_ = url_domain + url_[5:]
                    elif '../' in url_:
                        url_ = url_domain + url_[2:]
                    elif './' in url_:
                        url_ = url_domain + url_[1:]
                    else:
                        url_ = url_domain + url_
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


