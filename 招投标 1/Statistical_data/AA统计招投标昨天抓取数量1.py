# -*- coding: utf-8 -*-
import time, json, re, requests
from lxml.etree import HTML
from tool import tool

class spider:
    def __init__(self):
        self.tool = tool()
        self.date = tool.date
        self.url_lss = [
            [self.dongyuan,'http://ggzy.dg.gov.cn'],
            [self.wulanchabu, 'http://ggzy.wulanchabu.gov.cn'],
            [self.wulumuqi, 'http://zwfw.wlmq.gov.cn'],
            [self.yunfu, 'http://ggzy.yunfu.gov.cn'],
            [self.haozhou, 'http://ggzy.bozhou.gov.cn'],
            [self.yinchun, 'http://ggzy.yc.gov.cn'],
            [self.fuoshan, 'http://ggzy.foshan.gov.cn'],
            [self.hefei, 'http://ggzy.hefei.gov.cn'],
            [self.hulunbeier, 'http://www.hlbeggzyjy.org.cn'],
            [self.huhehaote, 'http://ggzy.huhhot.gov.cn'],
            [self.xianyang, 'http://xy.sxggzyjy.cn'],
            [self.tianshui, 'http://ggzyjy.tianshui.gov.cn'],
            [self.ankang, 'http://ak.sxggzyjy.cn'],
            [self.suzhou, 'http://ggzyjy.ahsz.gov.cn'],
            [self.bayanzhuoer, 'http://ggzyjy.bynr.gov.cn'],
            [self.guangzhou, 'http://www.gzebpubservice.cn'],
            [self.yanan, 'http://zyjy.yanan.gov.cn'],
            [self.huizhou, 'https://zyjy.huizhou.gov.cn'],
            [self.xinjiang, 'http://ztb.xjjs.gov.cn'],
            [self.benxi, 'http://ggzyjy.benxi.gov.cn'],
            [self.songyuan, 'http://syggzy.jlsy.gov.cn'],
            [self.yulin, 'http://yl.sxggzyjy.cn'],
            [self.hanzhong, 'http://www.hzzbb.com'],
            [self.shantou, 'https://www.shantou.gov.cn'],
            [self.shanwei, 'http://www.swggzy.cn'],
            [self.jiangmen, 'http://zyjy.jiangmen.cn'],
            [self.heyuan, 'http://61.143.150.176'],
            # [self.shenzhen, 'http://ggzy.sz.gov.cn'], 网站打不开
            [self.weinan, 'http://ggzy.weinan.gov.cn'],
            [self.chuzhou, 'http://ggzy.chuzhou.gov.cn'],
            [self.zhuhai, 'http://ggzy.zhuhai.gov.cn'],
            [self.gannan, 'http://ggzyjy.gnzrmzf.gov.cn'],
            [self.wuhu, 'http://whsggzy.wuhu.gov.cn'],
            # [self.zhaoqing, 'http://61.146.213.251'], 网站打不开
            [self.chifeng, 'http://ggzy.chifeng.gov.cn'],
            [self.liaoyuan, 'http://ggzy.liaoyuan.gov.cn'],
            [self.tonghua, 'http://thsggzyjy.tonghua.gov.cn'],
            [self.tongliao, 'http://ggzy.tongliao.gov.cn'],
            [self.eerduosi, 'http://www.ordosggzyjy.org.cn'],
            [self.tongling, 'http://ggzyjyzx.tl.gov.cn'],
            [self.hegang, 'http://www.hgggzyjyw.org.cn'],
            [self.huangshan, 'http://ggzy.huangshan.gov.cn'],
            [self.qiqihaer, 'http://ggzy.qqhr.gov.cn']
        ]

    # 东苑市公共资源交易中心
    def dongyuan(self):
        print('东苑市公共资源交易中心', 'http://ggzy.dg.gov.cn')
        url_list = [
            'http://ggzy.dg.gov.cn/ggzy/website/WebPagesManagement/findListByPage?fcInfotype=1&tenderkind=All&projecttendersite=SS&orderFiled=fcInfostartdate&orderValue=desc&fcInfotitle=&currentPage={}',
            'http://ggzy.dg.gov.cn/ggzy/website/WebPagesManagement/findListByPage?fcInfotype=4&tenderkind=All&projecttendersite=SS&fcInfotitle=&currentPage={}',
            # 结果
            'http://ggzy.dg.gov.cn/ggzy/website/WebPagesManagement/findListByPage?fcInfotype=7&tenderkind=All&projecttendersite=SS&orderFiled=fcInfostartdate&orderValue=desc&fcInfotitle=&extType=0&fcInfotype=7&currentPage={}',
            'http://ggzy.dg.gov.cn/ggzy/website/WebPagesManagement/TradeInfo/GovProcurement/findListByPage?fcInfotype=1&openbidbelong=All&fcInfotitle=&currentPage={}',
            'http://ggzy.dg.gov.cn/ggzy/website/WebPagesManagement/TradeInfo/GovProcurement/findListByPage?fcInfotype=4&openbidbelong=All&fcInfotitle=&currentPage={}',
            # 结果
            'http://ggzy.dg.gov.cn/ggzy/website/WebPagesManagement/TradeInfo/GovProcurement/findListByPage?fcInfotype=7&openbidbelong=All&fcInfotitle=&currentPage={}'
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
            detail = json.loads(text)['ls']
            for li in detail:
                if 'TradeInfo/GovProcurement' not in url:
                    if 'fcInfotype=1' in url:
                        url_to = 'http://ggzy.dg.gov.cn/ggzy/website/WebPagesManagement/jsdetail?publishId={}&fcInfotype=1'.format(
                            li['id'])
                    elif 'fcInfotype=4' in url:
                        url_to = 'http://ggzy.dg.gov.cn/ggzy/website/WebPagesManagement/jsdetail?publishId={}&fcInfotype=4'.format(
                            li['id'])
                    else:
                        url_to = 'http://ggzy.dg.gov.cn/ggzy/website/WebPagesManagement/jsdetail?publishId={}&fcInfotype=7'.format(
                            li['id'])
                else:
                    if 'fcInfotype=1' in url:
                        url_to = 'http://ggzy.dg.gov.cn/ggzy/website/WebPagesManagement/TradeInfo/GovProcurement/govdetail?publishinfoid={}&fcInfotype=1'.format(
                            li['publishinfoid'])
                    elif 'fcInfotype=4' in url:
                        url_to = 'http://ggzy.dg.gov.cn/ggzy/website/WebPagesManagement/TradeInfo/GovProcurement/govdetail?publishinfoid={}&fcInfotype=4'.format(
                            li['publishinfoid'])
                    else:
                        url_to = 'http://ggzy.dg.gov.cn/ggzy/website/WebPagesManagement/TradeInfo/GovProcurement/govdetail?publishinfoid={}&fcInfotype=7'.format(
                            li['publishinfoid'])
                date_Today = li['fcInfostartdate'][:10].replace('\xa0', '').replace('\n', ''). \
                    replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
                # print(title, url, date_Today)
                # time.sleep(666)
                if tool.Transformation(date_Today) > tool.Transformation(self.date):
                    continue
                elif tool.Transformation(date_Today) == tool.Transformation(self.date):
                    ls.append(url_to)
                else:
                    if len(url_list) == 0:
                        return [len(ls), ls]
                    else:
                        url = url_list.pop(0)
                        page = 0
                        break

    # 乌兰察布公共资源交易中心
    def wulanchabu(self):
        print('乌兰察布公共资源交易中心', 'http://ggzy.wulanchabu.gov.cn')
        url_list = [
             'http://ggzy.wulanchabu.gov.cn/jyxx/jsgcZbjggs',  #工程建设
             'http://ggzy.wulanchabu.gov.cn/jyxx/zfcg/zbjggs',
             'http://ggzy.wulanchabu.gov.cn/jyxx/jsgczbhxrgs',  # 工程建设
             'http://ggzy.wulanchabu.gov.cn/jyxx/jsgcZbgg',
             'http://ggzy.wulanchabu.gov.cn/jyxx/zfcg/cggg',  # 政府采购
             'http://ggzy.wulanchabu.gov.cn/jyxx/zfcg/gzsx'
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
                'currentPage': str(page),
                'area': '004',
                'secondArea': '000',
                'industriesTypeCode': '000',
                'bulletinName': ''
            }
            if page == 1:
                text = tool.requests_get(url, headers)
            else:
                text = tool.requests_post(url, data, headers)
            html = HTML(text)
            detail = html.xpath('//*[@id="p2"]/tr')
            for li in detail:
                try:
                    title = li.xpath('./td[2]/a/@title')[0]
                    url_to = 'http://ggzy.wulanchabu.gov.cn' + li.xpath('./td[2]/a/@href')[0]
                    date_Today = li.xpath('./td[3]/text()')[0]
                except:
                    try:
                        title = li.xpath('./td[3]/a/@title')[0]
                        url_to = 'http://ggzy.wulanchabu.gov.cn' + li.xpath('./td[3]/a/@href')[0]
                        date_Today = li.xpath('./td[4]/text()')[0]
                    except:
                        continue
                # print(title, url, date_Today)
                # time.sleep(666)
                if tool.Transformation(date_Today) > tool.Transformation(self.date):
                    continue
                elif tool.Transformation(date_Today) == tool.Transformation(self.date):
                    ls.append(url_to)
                else:
                    if len(url_list) == 0:
                        return [len(ls), ls]
                    else:
                        url = url_list.pop(0)
                        page = 0
                        break

    # 乌鲁木齐市公共资源交易中心
    def wulumuqi(self):
        print('乌鲁木齐市公共资源交易中心', 'http://zwfw.wlmq.gov.cn')
        url_list = [
            '001001',
            '001002'
        ]
        headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Cookie': 'JSESSIONID=662863FD2199FBD1672A04A290868047; _CSRFCOOKIE=73F3D7A1BCDCA9001D7B1483A214C4E98DE2528B; EPTOKEN=73F3D7A1BCDCA9001D7B1483A214C4E98DE2528B; oauthClientId=demoClient; oauthPath=http://172.16.5.21:8080/EpointWebBuilder; oauthLoginUrl=http://172.16.5.21:8080/EpointWebBuilder/rest/oauth2/authorize?client_id=demoClient&state=a&response_type=code&scope=user&redirect_uri=; oauthLogoutUrl=http://172.16.5.21:8080/EpointWebBuilder/rest/oauth2/logout?redirect_uri=; noOauthRefreshToken=986d4fe7e5dd29b64c9e7b7a6d66e089; noOauthAccessToken=77c09e0bf98b6220b544961097eed84a; sub_domain_cokie=TiG5CMD9KQ41mmsARPTuAg%3D%3D; region_name=%E4%B9%8C%E9%B2%81%E6%9C%A8%E9%BD%90%E5%B8%82',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',

        }
        url = url_list.pop(0)
        ls = []
        url_to = 'http://zwfw.wlmq.gov.cn/EWB-FRONT/rest/frontAppCustomAction/getPageInfoListNew'
        page = 0
        while True:
            data = {
                'params': '{"siteGuid":"7eb5f7f1-9041-43ad-8e13-8fcb82ea831a","categoryNum":"'+url+'","pageIndex":'+str(page)+',"pageSize":15,"jyStatus":"","kw":""}'
            }
            page += 1
            text = tool.requests_post(url_to, data, headers)
            detail = json.loads(text)['custom']['infodata']
            for li in detail:
                title = li['title']
                url_ = 'http://zwfw.wlmq.gov.cn' + li['infourl']
                date_Today = li['infodate'].replace('\xa0', '').replace('\n', ''). \
                    replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
                # print(title, url_to, date_Today)
                # time.sleep(666)
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

    # 云浮市公共资源交易中心
    def yunfu(self):
        print('云浮市公共资源交易中心', 'http://ggzy.yunfu.gov.cn')
        url_list = [
            'http://ggzy.yunfu.gov.cn/yfggzy/jsgc/002001/',
            'http://ggzy.yunfu.gov.cn/yfggzy/jsgc/002002/',
            'http://ggzy.yunfu.gov.cn/yfggzy/jsgc/002003/',
            'http://ggzy.yunfu.gov.cn/yfggzy/jsgc/002005/',#结果
            'http://ggzy.yunfu.gov.cn/yfggzy/zfcg/003001/',
            'http://ggzy.yunfu.gov.cn/yfggzy/zfcg/003002/',
            'http://ggzy.yunfu.gov.cn/yfggzy/zfcg/003003/',
            'http://ggzy.yunfu.gov.cn/yfggzy/zfcg/003005/',#结果
            'http://ggzy.yunfu.gov.cn/yfggzy/zfcg/003007/',
            'http://ggzy.yunfu.gov.cn/yfggzy/zfcg/003006/',
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
            detail = html.xpath('/html/body/div[4]/div/div[2]/div[2]/div[2]/ul/li')
            for li in detail:
                title = li.xpath('./div/a/@title')[0]
                url_to = 'http://ggzy.yunfu.gov.cn' + li.xpath('./div/a/@href')[0]
                date_Today = li.xpath('./span/text()')[0].replace('\xa0', '').replace('\n', ''). \
                    replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
                # print(title, url, date_Today)
                # time.sleep(666)
                if tool.Transformation(date_Today) > tool.Transformation(self.date):
                    continue
                elif tool.Transformation(date_Today) == tool.Transformation(self.date):
                    ls.append(url_to)
                else:
                    if len(url_list) == 0:
                        return [len(ls), ls]
                    else:
                        url = url_list.pop(0)
                        page = 0
                        break

    # 亳州市公共资源交易中心
    def haozhou(self):
        print('亳州市公共资源交易中心', 'http://ggzy.bozhou.gov.cn')
        url_list = [
            'http://ggzy.bozhou.gov.cn/BZWZ/jyxx/003001/003001001/003001001001/003001001001001/moreinfo.aspx?Paging={}',
            'http://ggzy.bozhou.gov.cn/BZWZ/jyxx/003002/003002001/003002001001/003002001001001/moreinfo.aspx?Paging={}',
            'http://ggzy.bozhou.gov.cn/BZWZ/jyxx/003001/003001002/003001002001/003001002001001/moreinfo.aspx?Paging={}',
            'http://ggzy.bozhou.gov.cn/BZWZ/jyxx/003002/003002002/003002002001/003002002001001/moreinfo.aspx?Paging={}',
            'http://ggzy.bozhou.gov.cn/BZWZ/jyxx/003001/003001003/003001003001/003001003001001/moreinfo.aspx?Paging={}',
            'http://ggzy.bozhou.gov.cn/BZWZ/jyxx/003002/003002003/003002003001/003002003001001/moreinfo.aspx?Paging={}',
            'http://ggzy.bozhou.gov.cn/BZWZ/jyxx/003001/003001004/003001004001/003001004001001/moreinfo.aspx?Paging={}'
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
            detail = html.xpath('//*[@id="MoreInfoList1_moreinfo"]/tr/td/table/tr')
            for li in detail:
                try:
                    title = li.xpath('./td/table/tr/td[3]/a/@title')[0]
                    url_to = 'http://ggzy.bozhou.gov.cn' + li.xpath('./td/table/tr/td[3]/a/@href')[0]
                    date_Today = li.xpath('./td/table/tr/td[4]/text()')[0]
                except:
                    try:
                        title = li.xpath('./td/table/tr/td[2]/a/@title')[0]
                        url_to = 'http://ggzy.bozhou.gov.cn' + li.xpath('./td/table/tr/td[2]/a/@href')[0]
                        date_Today = li.xpath('./td/table/tr/td[3]/text()')[0]
                    except:
                        continue
                # print(title, url, date_Today)
                # time.sleep(666)
                if tool.Transformation(date_Today) > tool.Transformation(self.date):
                    continue
                elif tool.Transformation(date_Today) == tool.Transformation(self.date):
                    ls.append(url_to)
                else:
                    if len(url_list) == 0:
                        return [len(ls), ls]
                    else:
                        url = url_list.pop(0)
                        page = 0
                        break

    # 伊春市公共资源交易网
    def yinchun(self):
        print('伊春市公共资源交易网', 'http://ggzy.yc.gov.cn')
        url_list = [
            'http://ggzy.yc.gov.cn/docweb/docList.action?channelId=2117&parentChannelId=-1&pageNo={}',
            'http://ggzy.yc.gov.cn/docweb/docList.action?channelId=2120&parentChannelId=-1&pageNo={}',
            'http://ggzy.yc.gov.cn/docweb/docList.action?channelId=2121&parentChannelId=2107',
            'http://ggzy.yc.gov.cn/docweb/docList.action?channelId=2123&parentChannelId=2107'
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
            if 'pageNo' in url:
                text = tool.requests_get(url.format(page), headers)
            else:
                text = tool.requests_get(url, headers)
            html = HTML(text)
            detail = html.xpath('/html/body/div/div[3]/div/div[2]/div[2]/div[1]/ul')
            for tr in detail:
                for li in tr.xpath('./li'):
                    title = li.xpath('./a/@title')[0]
                    url_to = 'http://ggzy.yc.gov.cn' + li.xpath('./a/@href')[0]
                    date_Today = li.xpath('./span/text()')[0]
                    if tool.Transformation(date_Today) > tool.Transformation(self.date):
                        continue
                    elif tool.Transformation(date_Today) == tool.Transformation(self.date):
                        ls.append(url_to)
                    else:
                        if len(url_list) == 0:
                            return [len(ls), ls]
                        else:
                            url = url_list.pop(0)
                            page = 0
                            break

    # 佛山市公共资源交易中心
    def fuoshan(self):
        print('佛山市公共资源交易中心', 'http://ggzy.foshan.gov.cn')
        url_list = [
            'http://ggzy.foshan.gov.cn/jyxx/fss/gcjy_1108550/zbgg/{}.html?1',
            'http://ggzy.foshan.gov.cn/jyxx/fss/gcjy_1108550/pbgs/{}.html?1',
            'http://ggzy.foshan.gov.cn/jyxx/fss/gcjy_1108550/zbjggk/{}.html?1',
            'http://ggzy.foshan.gov.cn/jyxx/fss/zfcg_1108551/cggg/{}.html?1',
            'http://ggzy.foshan.gov.cn/jyxx/fss/zfcg_1108551/gzgg/{}.html?1',
            'http://ggzy.foshan.gov.cn/jyxx/fss/zfcg_1108551/zbxx/{}.html?1'
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
            detail = html.xpath('//*[@id="articles2"]/ul/li')
            for li in detail:
                title = li.xpath('./div/a/text()')[0]
                url_to = li.xpath('./div/a/@href')[0]
                date_Today = li.xpath('./span/text()')[0].replace('\xa0', '').replace('\n', ''). \
                    replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
                # print(title, url, date_Today)
                # time.sleep(666)
                if tool.Transformation(date_Today) > tool.Transformation(self.date):
                    continue
                elif tool.Transformation(date_Today) == tool.Transformation(self.date):
                    ls.append(url_to)
                else:
                    if len(url_list) == 0:
                        return [len(ls), ls]
                    else:
                        url = url_list.pop(0)
                        page = 0
                        break

    # 合肥市公共资源交易中心
    def hefei(self):
        print('合肥市公共资源交易中心', 'http://ggzy.hefei.gov.cn')
        url_list = [
            'http://ggzy.hefei.gov.cn/jyxx/002001/002001001/{}.html',
            'http://ggzy.hefei.gov.cn/jyxx/002002/002002001/{}.html',
            'http://ggzy.hefei.gov.cn/jyxx/002001/002001002/{}.html',
            'http://ggzy.hefei.gov.cn/jyxx/002002/002002002/{}.html',
            'http://ggzy.hefei.gov.cn/jyxx/002001/002001003/{}.html',
            'http://ggzy.hefei.gov.cn/jyxx/002002/002002004/{}.html',
            'http://ggzy.hefei.gov.cn/jyxx/002001/002001004/{}.html'
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
                if '002002004' in url:
                    text = tool.requests_get(url.format('moreinfo_jyxxzfcggs'), headers)
                elif '002001004' in url:
                    text = tool.requests_get(url.format('moreinfo_jyxx4'), headers)
                elif '002001003' in url:
                    text = tool.requests_get(url.format('moreinfo_jyxxgs2'), headers)
                else:
                    text = tool.requests_get(url.format('moreinfo_jyxxgg2'), headers)
            else:
                text = tool.requests_get(url.format(page), headers)
            html = HTML(text)
            detail = html.xpath('/html/body/ul/li')
            for li in detail:
                title = li.xpath('./a/@title')[0]
                url_to = 'http://ggzy.hefei.gov.cn' + li.xpath('./a/@href')[0]
                date_Today = li.xpath('./span/text()')[0][:10]
                # print(title, url_to, date_Today)
                # time.sleep(666)
                if tool.Transformation(date_Today) > tool.Transformation(self.date):
                    continue
                elif tool.Transformation(date_Today) == tool.Transformation(self.date):
                    ls.append(url_to)
                    continue
                else:
                    if len(url_list) == 0:
                        return [len(ls), ls]
                    else:
                        url = url_list.pop(0)
                        page = 0
                        break

    # 呼伦贝尔市公共资源网
    def hulunbeier(self):
        print('呼伦贝尔市公共资源网', 'http://www.hlbeggzyjy.org.cn')
        url_list = [
            'http://www.hlbeggzyjy.org.cn/EpointWebBuilderService/jyxxlistaction.action?cmd=getInfolist&pageIndex={}&pageSize=16&siteGuid=7eb5f7f1-9041-43ad-8e13-8fcb82ea831a&xxlx=&fbsj=&dqfb=&jylx=&categoryzhu=021&_=1608537709440',
            'http://www.hlbeggzyjy.org.cn/EpointWebBuilderService/jyxxlistaction.action?cmd=getInfolist&pageIndex={}&pageSize=16&siteGuid=7eb5f7f1-9041-43ad-8e13-8fcb82ea831a&xxlx=&fbsj=&dqfb=&jylx=&categoryzhu=022&_=1608537709441',
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
            detail = json.loads(json.loads(text)['custom'])['Table']
            for li in detail:
                title = li['title']
                url_ = 'http://www.hlbeggzyjy.org.cn' + li['href']
                date_Today = li['date'].replace('[', '').replace(']', '').replace('\r',
                                                                                  '').replace(
                    '\n', '').replace('\t', '').replace(' ', '')
                if '招标文件' in title or '澄清补疑' in title:
                    continue
                # print(title, url, date_Today)
                # time.sleep(666)
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

    # 呼和浩特公共资源网
    def huhehaote(self):
        print('呼和浩特公共资源网', 'http://ggzy.huhhot.gov.cn')
        url_list = [
            'http://ggzy.huhhot.gov.cn/hsweb/004/004001/004001003/MoreInfo.aspx?CategoryNum=004001003',#建设工程
            'http://ggzy.huhhot.gov.cn/hsweb/004/004001/004001001/MoreInfo.aspx?CategoryNum=004001001',
            'http://ggzy.huhhot.gov.cn/hsweb/004/004001/004001004/MoreInfo.aspx?CategoryNum=004001004',
            'http://ggzy.huhhot.gov.cn/hsweb/004/004002/004002001/MoreInfo.aspx?CategoryNum=004002001',#政府采购
            'http://ggzy.huhhot.gov.cn/hsweb/004/004002/004002005/MoreInfo.aspx?CategoryNum=004002005',
            'http://ggzy.huhhot.gov.cn/hsweb/004/004002/004002003/MoreInfo.aspx?CategoryNum=004002003',
            'http://ggzy.huhhot.gov.cn/hsweb/004/004002/004002006/MoreInfo.aspx?CategoryNum=004002006',
            'http://ggzy.huhhot.gov.cn/hsweb/004/004002/004002004/MoreInfo.aspx?CategoryNum=004002004',
            'http://ggzy.huhhot.gov.cn/hsweb/004/004002/004002007/MoreInfo.aspx?CategoryNum=004002007',
            'http://ggzy.huhhot.gov.cn/hsweb/004/004010/004010001/MoreInfo.aspx?CategoryNum=004010001',#交通工程
            'http://ggzy.huhhot.gov.cn/hsweb/004/004010/004010003/MoreInfo.aspx?CategoryNum=004010003',
            'http://ggzy.huhhot.gov.cn/hsweb/004/004011/004011001/MoreInfo.aspx?CategoryNum=004011001',#水利工程
            'http://ggzy.huhhot.gov.cn/hsweb/004/004011/004011003/MoreInfo.aspx?CategoryNum=004011003',
            'http://ggzy.huhhot.gov.cn/hsweb/004/004012/004012001/MoreInfo.aspx?CategoryNum=004012001',#电力工程
            'http://ggzy.huhhot.gov.cn/hsweb/004/004012/004012003/MoreInfo.aspx?CategoryNum=004012003'
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
                '__EVENTTARGET': 'MoreInfoList1$Pager',
                '__EVENTARGUMENT': str(page)
            }
            detail = html.xpath('//*[@id="MoreInfoList1_DataGrid1"]/tr')
            for li in detail:
                title = li.xpath('./td[2]/a/text()')[0]
                url_ = 'http://ggzy.huhhot.gov.cn' + li.xpath('./td[2]/a/@href')[0]
                date_Today = li.xpath('./td[3]/text()')[0].replace('[', '').replace(']', '').replace('\r',
                                                                                                     '').replace(
                    '\n', '').replace('\t', '').replace(' ', '')
                # print(title, url, date_Today)
                # time.sleep(666)
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

    # 咸阳市公共资源交易中心
    def xianyang(self):
        print('咸阳市公共资源交易中心', 'http://xy.sxggzyjy.cn')
        url_list = [
            'http://xy.sxggzyjy.cn/jydt/001001/001001001/001001001001/{}.html',
            'http://xy.sxggzyjy.cn/jydt/001001/001001001/001001001002/{}.html',
            'http://xy.sxggzyjy.cn/jydt/001001/001001001/001001001005/{}.html',
            'http://xy.sxggzyjy.cn/jydt/001001/001001001/001001001003/{}.html',#结果
            'http://xy.sxggzyjy.cn/jydt/001001/001001004/001001004001/{}.html',
            'http://xy.sxggzyjy.cn/jydt/001001/001001004/001001004002/{}.html',
            'http://xy.sxggzyjy.cn/jydt/001001/001001004/001001004003/{}.html',#结果
            'http://xy.sxggzyjy.cn/jydt/001001/001001004/001001004004/{}.html'
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
                text = tool.requests_get(url.format('subPage'), headers)
            else:
                text = tool.requests_get(url.format(page), headers)
            html = HTML(text)
            detail = html.xpath('//*[@id="categorypagingcontent"]/ul/li')
            for li in detail:
                title = li.xpath('./a/@title')[0].replace('\n', ''). \
                    replace('\r', '').replace('\t', '').replace(' ', '')
                url_ = 'http://xy.sxggzyjy.cn' + li.xpath('./a/@href')[0]
                date_Today = self.date[:5] + li.xpath('./span/text()')[0].replace('\xa0', '').replace('\n', ''). \
                    replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
                if 'http' not in url_:
                    url_ = 'http://xy.sxggzyjy.cn' + url_
                # print(title, url, date_Today)
                # time.sleep(666)
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

    # 天水市公共资源交易中心
    def tianshui(self):
        print('天水市公共资源交易中心', 'http://ggzyjy.tianshui.gov.cn')
        url_list = ['A01','A99','A02','A03', 'D', 'C']
        headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Cookie': 'JSESSIONID=662863FD2199FBD1672A04A290868047; _CSRFCOOKIE=73F3D7A1BCDCA9001D7B1483A214C4E98DE2528B; EPTOKEN=73F3D7A1BCDCA9001D7B1483A214C4E98DE2528B; oauthClientId=demoClient; oauthPath=http://172.16.5.21:8080/EpointWebBuilder; oauthLoginUrl=http://172.16.5.21:8080/EpointWebBuilder/rest/oauth2/authorize?client_id=demoClient&state=a&response_type=code&scope=user&redirect_uri=; oauthLogoutUrl=http://172.16.5.21:8080/EpointWebBuilder/rest/oauth2/logout?redirect_uri=; noOauthRefreshToken=986d4fe7e5dd29b64c9e7b7a6d66e089; noOauthAccessToken=77c09e0bf98b6220b544961097eed84a; sub_domain_cokie=TiG5CMD9KQ41mmsARPTuAg%3D%3D; region_name=%E4%B9%8C%E9%B2%81%E6%9C%A8%E9%BD%90%E5%B8%82',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        }
        url = url_list.pop(0)
        page = 0
        ls = []
        url_to = 'http://ggzyjy.tianshui.gov.cn/f/trade/annogoods/getAnnoItem'
        while True:
            for i in range(2):
                data = {
                    'pageNo': str(page),
                    'pageSize': '20',
                    'prjpropertycode': url,
                    'annogoodstype': str(i + 1),
                    'type': '',
                    'tabType': '',
                    'isFrame': '',
                    'annogoodsname': ''
                }
                page += 1
                text = tool.requests_post(url_to, data, headers)
                html = HTML(text)
                detail = html.xpath('//*[@class="ejcotlist"]/ul/li')
                for li in detail:
                    title = li.xpath('./a/text()')[0].replace('\xa0', '').replace('\n', ''). \
                        replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
                    url_ = li.xpath('./a/@href')[0]
                    date_Today = li.xpath('./span/text()')[0].replace('\xa0', '').replace('\n', ''). \
                        replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '') \
                        .replace('[', '').replace(']', '').replace('/', '-')
                    if 'http' not in url_:
                        url_ = 'http://ggzyjy.tianshui.gov.cn' + url_
                    # print(title, url, date_Today)
                    # time.sleep(666)
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

    # 安康市公共资源交易中心
    def ankang(self):
        print('安康市公共资源交易中心', 'http://ak.sxggzyjy.cn')
        url_list = [
            'http://ak.sxggzyjy.cn/jydt/001001/001001001/001001001001/{}.html',
            'http://ak.sxggzyjy.cn/jydt/001001/001001001/001001001002/{}.html',
            'http://ak.sxggzyjy.cn/jydt/001001/001001001/001001001004/{}.html',
            'http://ak.sxggzyjy.cn/jydt/001001/001001001/001001001005/{}.html',
            'http://ak.sxggzyjy.cn/jydt/001001/001001001/001001001003/{}.html',#结果

            'http://ak.sxggzyjy.cn/jydt/001001/001001004/001001004001/{}.html',
            'http://ak.sxggzyjy.cn/jydt/001001/001001004/001001004002/{}.html',
            'http://ak.sxggzyjy.cn/jydt/001001/001001004/001001004003/{}.html',#结果
            'http://ak.sxggzyjy.cn/jydt/001001/001001004/001001004004/{}.html'
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
                text = tool.requests_get(url.format('subPage'), headers)
            else:
                text = tool.requests_get(url.format(page), headers)
            html = HTML(text)
            detail = html.xpath('//*[@id="categorypagingcontent"]/ul/li')
            for li in detail:
                title = li.xpath('./a/@title')[0]
                url_ = 'http://ak.sxggzyjy.cn' + li.xpath('./a/@href')[0]
                date_Today = self.date[:5] + li.xpath('./span/text()')[0].replace('\xa0', '').replace('\n', ''). \
                    replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
                # print(title, url, date_Today)
                # time.sleep(666)
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

    # 宿州市公共资源交易中心
    def suzhou(self):
        print('宿州市公共资源交易中心', 'http://ggzyjy.ahsz.gov.cn')
        url_list = [
            '001001',
            '001002'
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
        url_to = 'http://ggzyjy.ahsz.gov.cn/EpointWebBuilder/rest/informationsearchaction/getinfomationlist'
        while True:
            data = {
                'params': '{"title":"","typeId":"' + url + '","areaId":"","infotypeId":"","modeId":"","pageIndex":' + str(
                    page) + ',"pageSize":10}'}
            page += 1
            text = tool.requests_post(url_to, data, headers)
            detail = json.loads(text)['custom']['list']
            for li in detail:
                title = li['title']
                categorynum = li['categorynum']
                date_Today = li['infodate']
                date_today = str(date_Today).replace('-', '')
                url_ = f'http://ggzyjy.ahsz.gov.cn/jyxx/{categorynum[:6]}/{categorynum[:9]}/{categorynum}/{date_today}/{li["infoid"]}.html'

                # print(title, url, date_Today)
                # time.sleep(666)
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

    # 巴彦淖尔市公共资源中心
    def bayanzhuoer(self):
        print('巴彦淖尔市公共资源中心', 'http://ggzyjy.bynr.gov.cn')
        url_list = [
            'http://ggzyjy.bynr.gov.cn/EpointWebBuilder/tradeInfoSearchAction.action?cmd=getList'
             '&categorynums=018001&xiaqucode=&sdt=&edt=&jylx=&siteguid=7eb5f7f1-9041-43ad-8e13-8fcb82ea831a'
             '&pageSize=15&pageIndex={}',
             'http://ggzyjy.bynr.gov.cn/EpointWebBuilder/tradeInfoSearchAction.action?cmd=getList'
             '&categorynums=018002&xiaqucode=&sdt=&edt=&jylx=&siteguid=7eb5f7f1-9041-43ad-8e13-8fcb82ea831a'
             '&pageSize=15&pageIndex={}'
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
                title = li['titles']
                url_ = 'http://ggzyjy.bynr.gov.cn' + li['href']
                date_Today = li['infodate']
                # print(title, url, date_Today)
                # time.sleep(666)
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

    # 广州市公共资源交易中心
    def guangzhou(self):
        print('广州市公共资源交易中心', 'http://www.gzebpubservice.cn')
        url_list = [
            'http://www.gzebpubservice.cn/fjzbgg/index_{}.htm',
            'http://www.gzebpubservice.cn/fjzsjggs/index_{}.htm',#结果
            'http://www.gzebpubservice.cn/fjzbhxgs/index_{}.htm',
            'http://www.gzebpubservice.cn/fjzbxx/index_{}.htm',

            'http://www.gzebpubservice.cn/jtzbgg/index_{}.htm',
            'http://www.gzebpubservice.cn/jtysgg/index_{}.htm',
            'http://www.gzebpubservice.cn/jtzbhxgs/index_{}.htm',
            'http://www.gzebpubservice.cn/jtzbgs/index_{}.htm',  #交通 ==== ---->中标公告

            'http://www.gzebpubservice.cn/dlzbgg/index_{}.htm',
            'http://www.gzebpubservice.cn/dlzbhxgs/index_{}.htm',
            'http://www.gzebpubservice.cn/dlzbxx/index_{}.htm',

            'http://www.gzebpubservice.cn/tlzbgg/index_{}.htm',
            'http://www.gzebpubservice.cn/tlzbhxgs/index_{}.htm',
            'http://www.gzebpubservice.cn/tlzbxx/index_{}.htm',

            'http://www.gzebpubservice.cn/slzbgg/index_{}.htm',
            'http://www.gzebpubservice.cn/slzsjggs/index_{}.htm',
            'http://www.gzebpubservice.cn/slzbhxgs/index_{}.htm',
            'http://www.gzebpubservice.cn/slzbxx/index_{}.htm',

            'http://www.gzebpubservice.cn/ylzbgg/index_{}.htm',
            'http://www.gzebpubservice.cn/ylzsjggs/index_{}.htm',
            'http://www.gzebpubservice.cn/ylzbhxrgs/index_{}.htm',
            'http://www.gzebpubservice.cn/ylzbxx/index_{}.htm',

            'http://www.gzebpubservice.cn/mhzbgg/index_{}.htm',
            'http://www.gzebpubservice.cn/mhzbhxrgs/index_{}.htm',
            'http://www.gzebpubservice.cn/mhzbxx/index_{}.htm',
            'http://www.gzebpubservice.cn/qtzbgg/index_{}.htm',
            'http://www.gzebpubservice.cn/qtzsjggs/index_{}.htm',
            'http://www.gzebpubservice.cn/qtzbhxrgs/index_{}.htm',
            'http://www.gzebpubservice.cn/qtzbxx/index_{}.htm',
            'http://www.gzebpubservice.cn/xecbhxrgs/index_{}.htm',

            'http://www.gzebpubservice.cn/cggg/index_{}.htm',  #政府采购
            'http://www.gzebpubservice.cn/zfcgygg/index_{}.htm',
            'http://www.gzebpubservice.cn/gzgg/index_{}.htm',
            'http://www.gzebpubservice.cn/jggg/index_{}.htm',
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
            detail = html.xpath('/html/body/div[4]/ul[3]/li')
            for li in detail:
                title = li.xpath('./p[1]/a/@title')[0]
                url_ = li.xpath('./p[1]/a/@href')[0]
                date_Today = li.xpath('./p[2]/text()')[0].replace('\xa0', '').replace('\n', ''). \
                    replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
                # print(title, url, date_Today)
                # time.sleep(666)
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

    # 延安市公共资源交易平台
    def yanan(self):
        print('延安市公共资源交易平台', 'http://zyjy.yanan.gov.cn')
        url_list = [
            'http://zyjy.yanan.gov.cn/Front_YanAn/jyxx/004001/004001001/004001001001/?pageing={}',
            'http://zyjy.yanan.gov.cn/Front_YanAn/jyxx/004001/004001001/004001001002/?pageing={}',
            'http://zyjy.yanan.gov.cn/Front_YanAn/jyxx/004001/004001001/004001001003/?pageing={}',
            'http://zyjy.yanan.gov.cn/Front_YanAn/jyxx/004001/004001001/004001001004/?pageing={}',#结果

            'http://zyjy.yanan.gov.cn/Front_YanAn/jyxx/004001/004001002/004001002001/?pageing={}',
            'http://zyjy.yanan.gov.cn/Front_YanAn/jyxx/004001/004001002/004001002002/?pageing={}',
            'http://zyjy.yanan.gov.cn/Front_YanAn/jyxx/004001/004001002/004001002003/?pageing={}',
            'http://zyjy.yanan.gov.cn/Front_YanAn/jyxx/004001/004001002/004001002004/?pageing={}',#结果

            'http://zyjy.yanan.gov.cn/Front_YanAn/jyxx/004001/004001003/004001003001/?pageing={}',
            'http://zyjy.yanan.gov.cn/Front_YanAn/jyxx/004001/004001003/004001003002/?pageing={}',
            'http://zyjy.yanan.gov.cn/Front_YanAn/jyxx/004001/004001003/004001003004/?pageing={}',#结果

            'http://zyjy.yanan.gov.cn/Front_YanAn/jyxx/004001/004001007/004001007001/?pageing={}',
            'http://zyjy.yanan.gov.cn/Front_YanAn/jyxx/004001/004001007/004001007003/?pageing={}',
            'http://zyjy.yanan.gov.cn/Front_YanAn/jyxx/004001/004001007/004001007004/?pageing={}',#结果

            'http://zyjy.yanan.gov.cn/Front_YanAn/jyxx/004001/004001008/004001008001/?pageing={}',
            'http://zyjy.yanan.gov.cn/Front_YanAn/jyxx/004001/004001008/004001008002/?pageing={}',

            'http://zyjy.yanan.gov.cn/Front_YanAn/jyxx/004007/004007001/004007001001/?pageing={}',
            'http://zyjy.yanan.gov.cn/Front_YanAn/jyxx/004007/004007001/004007001003/?pageing={}',
            'http://zyjy.yanan.gov.cn/Front_YanAn/jyxx/004007/004007002/004007002001/?pageing={}',
            'http://zyjy.yanan.gov.cn/Front_YanAn/jyxx/004007/004007002/004007002003/?pageing={}',
            'http://zyjy.yanan.gov.cn/Front_YanAn/jyxx/004007/004007003/004007003001/?pageing={}',
            'http://zyjy.yanan.gov.cn/Front_YanAn/jyxx/004007/004007003/004007003003/?pageing={}'
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
            detail = html.xpath('/html/body/ul[1]/li')
            for li in detail:
                title = li.xpath('./div/a/text()')[0]
                url_ = li.xpath('./div/a/@href')[0]
                date_Today = li.xpath('./span/text()')[0].replace('\xa0', '').replace('\n', ''). \
                    replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
                if 'http' not in url_:
                    url_ = 'http://zyjy.yanan.gov.cn' + url_
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

    # 惠州市公共资源交易中心
    def huizhou(self):
        print('惠州市公共资源交易中心', 'https://zyjy.huizhou.gov.cn')
        url_list = [
            '20','22','26','23','14','15','10','11','12','19'
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
        url_to = 'https://zyjy.huizhou.gov.cn/PublicServer/commonAnnouncementAction/getCommonAnnouncementList.do'
        data = {
            'page': str(page),
            'rows': '15',
            'businessType': '2',
            'announcementType': url,
        }
        while True:
            page += 1
            data['page'] = str(page)
            data['announcementType'] = url
            if '14' in url:
                data['businessType'] = '1'
            text = tool.requests_post(url_to, data, headers)
            detail = json.loads(text)['data']['data']['list']
            for li in detail:
                title = li['title']
                url_ = 'https://zyjy.huizhou.gov.cn/PublicServer/commonAnnouncementAction/selectPublishAnnouncementById.do?id=' + \
                      li['id']
                date_Today = li['publishTime'][:10].replace('\xa0', '').replace('\n', ''). \
                    replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
                # print(title, url, date_Today)
                # time.sleep(666)
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

    # 新疆建设工程信息网
    def xinjiang(self):
        print('新疆建设工程信息网', 'http://ztb.xjjs.gov.cn')
        url_list = [
            'http://ztb.xjjs.gov.cn/xjweb/jyxx/004001/004001001/MoreInfo.aspx?CategoryNum=004001001&Paging={}',
            'http://ztb.xjjs.gov.cn/xjweb/jyxx/004001/004001002/MoreInfo.aspx?CategoryNum=004001002&Paging={}',
            'http://ztb.xjjs.gov.cn/xjweb/jyxx/004001/004001003/MoreInfo.aspx?CategoryNum=004001003&Paging={}',
            'http://ztb.xjjs.gov.cn/xjweb/jyxx/004001/004001006/004001006001/MoreInfo.aspx?CategoryNum=004001006001&Paging={}',
            'http://ztb.xjjs.gov.cn/xjweb/jyxx/004001/004001006/004001006002/MoreInfo.aspx?CategoryNum=004001006002&Paging={}',
            'http://ztb.xjjs.gov.cn/xjweb/jyxx/004001/004001006/004001006003/MoreInfo.aspx?CategoryNum=004001006003&Paging={}',
            'http://ztb.xjjs.gov.cn/xjweb/jyxx/004002/004002001/MoreInfo.aspx?CategoryNum=004002001&Paging={}',
            'http://ztb.xjjs.gov.cn/xjweb/jyxx/004002/004002002/MoreInfo.aspx?CategoryNum=004002002&Paging={}',
            'http://ztb.xjjs.gov.cn/xjweb/jyxx/004002/004002003/MoreInfo.aspx?CategoryNum=004002003&Paging={}',
            'http://ztb.xjjs.gov.cn/xjweb/jyxx/004002/004002006/004002006001/MoreInfo.aspx?CategoryNum=004002006001&Paging={}',
            'http://ztb.xjjs.gov.cn/xjweb/jyxx/004002/004002006/004002006002/MoreInfo.aspx?CategoryNum=004002006002&Paging={}',
            'http://ztb.xjjs.gov.cn/xjweb/jyxx/004002/004002006/004002006003/MoreInfo.aspx?CategoryNum=004002006003&Paging={}'
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
            # print(11, text)
            # time.sleep(6666)
            detail = html.xpath('//*[@id="MoreInfoList1_DataGrid1"]/tr')
            for li in detail:
                title = li.xpath('./td[2]/a/@title')[0]
                url_ = li.xpath('./td[2]/a/@href')[0]
                date_Today = li.xpath('./td[3]/text()')[0].replace('\xa0', '').replace('\n', ''). \
                    replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '') \
                    .replace('[', '').replace(']', '')
                if 'http' not in url_:
                    url_ = 'http://ztb.xjjs.gov.cn' + url_
                # print(title, url, date_Today)
                # time.sleep(666)
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

    # 本溪市公共资源
    def benxi(self):
        print('本溪市公共资源', 'http://ggzyjy.benxi.gov.cn')
        url_list = [
            'http://ggzyjy.benxi.gov.cn/jyxx/003001/003001001/{}.html',        #工程建设
            'http://ggzyjy.benxi.gov.cn/jyxx/003001/003001002/{}.html',
            'http://ggzyjy.benxi.gov.cn/jyxx/003002/003002001/{}.html',
            'http://ggzyjy.benxi.gov.cn/jyxx/003002/003002002/{}.html',
            'http://ggzyjy.benxi.gov.cn/jyxx/003002/003002003/{}.html'
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
                text = tool.requests_get(url.format('listjyxx'), headers)
            else:
                text = tool.requests_get(url.format(page), headers)
            html = HTML(text)
            detail = html.xpath('//*[@id="infoContent"]/li')
            for li in detail:
                title = li.xpath('./a/@title')[0]
                url_ = 'http://ggzyjy.benxi.gov.cn' + li.xpath('./a/@href')[0]
                date_Today = li.xpath('./span/text()')[0]
                # print(title, url, date_Today)
                # time.sleep(666)
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

    # 松原市公共资源交易中心
    def songyuan(self):
        print('松原市公共资源交易中心', 'http://syggzy.jlsy.gov.cn')
        url_list = [
            'http://syggzy.jlsy.gov.cn/EpointWebBuilder/webInfoAPI.action?cmd=getWebInfoList&categorynum=002&pageindex={}&pagesize=13&_=1614674559410'
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
            detail = json.loads(json.loads(text)['custom'])['data']
            for li in detail:
                title = li['title']
                url_ = 'http://syggzy.jlsy.gov.cn' + li['infourl']
                date_Today = li['infodate']
                # print(title, url_, date_Today)
                # time.sleep(666)
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

    # 榆林市公共资源交易中心
    def yulin(self):
        print('榆林市公共资源交易中心', 'http://yl.sxggzyjy.cn')
        url_list = [
            'http://yl.sxggzyjy.cn/jydt/001001/001001001/001001001001/{}.html',
            'http://yl.sxggzyjy.cn/jydt/001001/001001001/001001001002/{}.html',
            'http://yl.sxggzyjy.cn/jydt/001001/001001001/001001001004/{}.html',
            'http://yl.sxggzyjy.cn/jydt/001001/001001004/001001004001/{}.html',
            'http://yl.sxggzyjy.cn/jydt/001001/001001004/001001004002/{}.html',
            'http://yl.sxggzyjy.cn/jydt/001001/001001004/001001004003/{}.html',#结果
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
            if page == 10:
                if len(url_list) == 0:
                    return [len(ls), ls]
                else:
                    url = url_list.pop(0)
                    page = 0
                    continue
            if page == 1:
                text = tool.requests_get(url.format('subPage'), headers)
            else:
                text = tool.requests_get(url.format(page), headers)
            html = HTML(text)
            detail = html.xpath('//*[@id="categorypagingcontent"]/ul/li')
            for li in detail:
                title = li.xpath('./a/@title')[0]
                url_ = li.xpath('./a/@href')[0]
                date_Today = self.date[:5] + li.xpath('./span/text()')[0].replace('\xa0', '').replace('\n', ''). \
                    replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '') \
                    .replace('[', '').replace(']', '')
                if 'http' not in url_:
                    url_ = 'http://yl.sxggzyjy.cn' + url_
                # print(title, url, date_Today)
                # time.sleep(666)
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

    # 汉中市公共资源交易中心
    def hanzhong(self):
        print('汉中市公共资源交易中心', 'http://www.hzzbb.com')
        url_list_to = [
            'http://www.hzzbb.com/zhaobiao.asp?fd=&lb=&page={}',
            'http://www.hzzbb.com/zhongbiao.asp?fd=&zhob=1&page={}'
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
            if 'zhaobiao' in url:
                url_list = re.findall(
                    '''<div align="left"><SPAN class=a01><A target="_blank" HREF="(.*?)">(.*?)</A></SPAN></div></TD>''',
                    text)
                date_list = re.findall('''width=70>(.*?)</TD>''', text)
            else:
                url_list = re.findall(
                    '''<TD vAlign=bottom align=left width="500"><A target="_blank" HREF="(.*?)">(.*?)</A></TD>''',
                    text)
                date_list = re.findall('''<TD><div align="right">(.*?)</div></TD>''', text)
            for li in range(len(url_list)):
                title = url_list[li][1]
                url_ = url_list[li][0]
                date_Today = date_list[li].replace('\xa0', '').replace('\n', ''). \
                    replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '') \
                    .replace('[', '').replace(']', '')
                d = date_Today.replace(self.date[:5], '')
                if int(d[0]) < 10 and d[1] == '-':
                    date_Today = self.date[:5]+'0' + d
                if 'http' not in url_:
                    url_ = 'http://www.hzzbb.com/' + url_
                # print(title, url, date_Today)
                # time.sleep(666)
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

    # 汕头市人民政府门户网站
    def shantou(self):
        print('汕头市人民政府门户网站', 'https://www.shantou.gov.cn')
        url_list = [
            'https://www.shantou.gov.cn/cnst/zfcg/cggg/{}.html',
            'https://www.shantou.gov.cn/cnst/zfcg/gzgg/{}.html',
            'https://www.shantou.gov.cn/cnst/zfcg/yzbgg/{}.html',
            'https://www.shantou.gov.cn/cnst/zfcg/zbgg/{}.html',
            'https://www.shantou.gov.cn/cnst/zwgk/jcxxgk/gggs/{}.html'
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
            if 'jcxxgk' in url:
                detail = html.xpath('/html/body/div[4]/div/div[2]/div[1]/ul/li')
            else:
                detail = html.xpath('/html/body/div[4]/div/div[2]/div[2]/ul/li')
            for li in detail:
                title = li.xpath('./a/text()')[0]
                url_ = li.xpath('./a/@href')[0]
                date_Today = li.xpath('./span/text()')[0].replace('\xa0', '').replace('\n', ''). \
                    replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
                # print(title, url, date_Today)
                # time.sleep(666)
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

    # 汕尾市公共资源交易平台
    def shanwei(self):
        print('汕尾市公共资源交易平台', 'http://www.swggzy.cn')
        url_list = [
             '4793892710e942bdb8edb883822dbab4',
             'c0d135163be342c2b76a4957dc4b1999',
             '089ddf2ff80c4e259ac5b208e9154469',
             'd3174a1009b141bcb4a99666527f53ed',
             '4a6dafa78918407eb17400c5ef72dcfe',
             '02f4929cf37641a5b1dfbd746af46e7b'
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
            'area': 'all',
            'searchTitle': '',
            'columnId': '',
            'pageIndex': '0',
            'pageSize': '20',
        }
        url_to = 'http://www.swggzy.cn/intensive/noticesListIntensive/getNotices'
        while True:
            data['pageIndex'] = str(page)
            page += 1
            data['columnId'] = url
            if 'd3174a1009b141bcb4a99666527f53ed' in url:
                url_to = 'http://www.swggzy.cn/noticesList/getNotices'
            text = tool.requests_post(url_to, data, headers)
            detail = json.loads(text)['attributes']['notices']
            for li in detail:
                title = li['title']
                url_ = 'http://www.swggzy.cn' + li['href']
                date_Today = li['releaseTime'].replace('\xa0', '').replace('\n', ''). \
                    replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
                # print(title, url, date_Today)
                # time.sleep(666)
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

    # 江门市公共资源交易平台.
    def jiangmen(self):
        print('江门市公共资源交易平台', 'http://zyjy.jiangmen.cn')
        url_list = [
             'http://zyjy.jiangmen.cn/zbgg/{}.htm',
            'http://zyjy.jiangmen.cn/zbgzgg/{}.htm',
            'http://zyjy.jiangmen.cn/jggs/{}.htm',
            'http://zyjy.jiangmen.cn/zbgs/{}.htm',
            'http://zyjy.jiangmen.cn/cggg/{}.htm',
            'http://zyjy.jiangmen.cn/cjgg/{}.htm',
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
            detail = html.xpath('/html/body/div[2]/div/div[2]/div[3]/div/ul/li')
            for li in detail:
                title = li.xpath('./a/@title')[0]
                url_ = li.xpath('./a/@href')[0]
                date_Today = li.xpath('./a/span/text()')[0][:11].replace('\xa0', '').replace('\n', ''). \
                    replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
                # print(title, url, date_Today)
                # time.sleep(666)
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

    # 河源市公共资源交易平台
    def heyuan(self):
        print('河源市公共资源交易平台', 'http://61.143.150.176')
        url_list = [
             'http://61.143.150.176/jsgc/004001/{}.html',#结果
             'http://61.143.150.176/zfcg/{}.html'
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
                text = tool.requests_get(url.format('subpage'), headers)
            else:
                text = tool.requests_get(url.format(page), headers)
            html = HTML(text)
            detail = html.xpath('/html/body/div/div[2]/div[2]/div[2]/div/div[2]/ul[1]/li')
            for li in detail:
                title = li.xpath('./div/a/@title')[0]
                url_ = li.xpath('./div/a/@href')[0]
                date_Today = li.xpath('./span/text()')[0].replace('\xa0', '').replace('\n', ''). \
                    replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
                if 'http' not in url_:
                    url_ = 'http://61.143.150.176' + url_
                # print(title, url, date_Today)
                # time.sleep(666)
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

    # 深圳市公共资源交易平台   网站打不开
    def shenzhen(self):
        print('深圳市公共资源交易平台', 'http://ggzy.sz.gov.cn')
        url_list = [
             'http://ggzy.sz.gov.cn/cn/jyxx/jsgc/jsgz_zbgg/{}.html',
            'http://ggzy.sz.gov.cn/cn/jyxx/jsgc/zbgg/{}.html',#结果
            'http://ggzy.sz.gov.cn/cn/jyxx/jsgc/gzgg/{}.html',
            'http://ggzy.sz.gov.cn/cn/jyxx/szjy/jygg/{}.html',
            'http://ggzy.sz.gov.cn/cn/jyxx/szjy/jggg/{}.html',#三资交易 结果
            'http://ggzy.sz.gov.cn/cn/jyxx/zfcg/sbj/zbgg/{}.html',
            'http://ggzy.sz.gov.cn/cn/jyxx/zfcg/sbj/zhbgg/{}.html',
            'http://ggzy.sz.gov.cn/cn/jyxx/zfcg/sbj/gzgg/{}.html'
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
            if 'zfcg' in url:
                detail = html.xpath('//*[@id="tagContent"]/div/div/div[3]/ul/li')
            else:
                detail = html.xpath('//*[@id="tagContent"]/div/div/div[2]/ul/li')
            for li in detail:
                title = li.xpath('./a/@title')[0]
                url_ = li.xpath('./a/@href')[0]
                date_Today = li.xpath('./span[1]/text()')[0].replace('\xa0', '').replace('\n', ''). \
                    replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
                if 'http' not in url_:
                    url_ = 'http://ggzy.sz.gov.cn' + url_
                # print(title, url, date_Today)
                # time.sleep(666)
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

    # 渭南市公共资源交易中心
    def weinan(self):
        print('渭南市公共资源交易中心', 'http://ggzy.weinan.gov.cn')
        url_list = [
            'http://ggzy.weinan.gov.cn/wnggzyweb/jyxx/002001/002001006/002001006002/?Paging={}',
            'http://ggzy.weinan.gov.cn/wnggzyweb/jyxx/002001/002001006/002001006001/?Paging={}',
            'http://ggzy.weinan.gov.cn/wnggzyweb/jyxx/002001/002001006/002001006003/?Paging={}',#结果
            'http://ggzy.weinan.gov.cn/wnggzyweb/jyxx/002001/002001007/002001007001/?Paging={}',
            'http://ggzy.weinan.gov.cn/wnggzyweb/jyxx/002001/002001007/002001007002/?Paging={}',
            'http://ggzy.weinan.gov.cn/wnggzyweb/jyxx/002001/002001007/002001007003/?Paging={}',#结果

            'http://ggzy.weinan.gov.cn/wnggzyweb/jyxx/002001/002001008/002001008001/?Paging={}',
            'http://ggzy.weinan.gov.cn/wnggzyweb/jyxx/002001/002001008/002001008002/?Paging={}',
            'http://ggzy.weinan.gov.cn/wnggzyweb/jyxx/002001/002001008/002001008003/?Paging={}',

            'http://ggzy.weinan.gov.cn/wnggzyweb/jyxx/002002/002002001/?Paging={}',
            'http://ggzy.weinan.gov.cn/wnggzyweb/jyxx/002002/002002003/?Paging={}',
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
            detail = html.xpath('/html/body/div[2]/div/div[2]/div[2]/div[2]/div[1]/table/tr')
            for li in detail:
                title = li.xpath('./td[2]/a/@title')[0]
                url_ = li.xpath('./td[2]/a/@href')[0]
                date_Today = li.xpath('./td[3]/span/text()')[0].replace('\xa0', '').replace('\n', ''). \
                    replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '') \
                    .replace('[', '').replace(']', '')
                if 'http' not in url_:
                    url_ = 'http://ggzy.weinan.gov.cn' + url_
                # print(title, url, date_Today)
                # time.sleep(666)
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

    # 滁州市公共资源交易中心
    def chuzhou(self):
        print('滁州市公共资源交易中心', 'http://ggzy.chuzhou.gov.cn')
        url_list = [
            '005001',
            '005002'
        ]
        headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Host': 'ggzy.chuzhou.gov.cn',
            'Origin': 'http://ggzy.chuzhou.gov.cn',
            'Connection': 'keep-alive',
            'Content-Length': '306',
            'X-Requested-With': 'XMLHttpRequest',
            'Authorization': 'Bearer 31293ec99b7946c4d9dc3e286d97a0a0',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Referer': 'http://ggzy.chuzhou.gov.cn/jiaoyixinxi/005001/005001002/bussinessiBulid.html?cnum=005001002',
            'Cookie': 'userGuid=538255343; fontZoomState=0; oauthPath=http://127.0.0.1:8081/EpointWebBuilder; oauthClientId=demoClient; oauthLoginUrl=http://127.0.0.1:8081/EpointWebBuilder/rest/oauth2/authorize?client_id=demoClient&state=a&response_type=code&scope=user&redirect_uri=; oauthLogoutUrl=http://127.0.0.1:8081/EpointWebBuilder/rest/oauth2/logout?redirect_uri=; noOauthRefreshToken=6eba3a9624fb65c7182a9880cf755532; noOauthAccessToken=31293ec99b7946c4d9dc3e286d97a0a0; HttpOnly',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        }
        url = url_list.pop(0)
        page = 0
        ls = []
        url_to = 'http://ggzy.chuzhou.gov.cn/EpointWebBuilder/rest/GgSearchAction/getInfoMationList'
        while True:
            data = {'params': '{"siteGuid":"7eb5f7f1-9041-43ad-8e13-8fcb82ea831a","categoryNum":"'+url+'","keyword":"","startDate":"","endDate":"","publishDate":"","area":"","tradeType":"","pageIndex": %s,"pageSize":12}' %page}
            page += 1
            text = tool.requests_post(url_to, data, headers)
            detail = json.loads(text)['Table']
            for li in detail:
                title = li['title']
                url_ = 'http://ggzy.chuzhou.gov.cn/jiaoyixinxi/{}/{}/{}/{}.html'.format(li['categorynum'][:6],li['categorynum'],li['infodate'].replace('-', ''), li['infoId'])
                date_Today = li['infodate']
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

    # 珠海市公共资源交易中心
    def zhuhai(self):
        print('珠海市公共资源交易中心', 'http://ggzy.zhuhai.gov.cn')
        url_list = [
            'http://ggzy.zhuhai.gov.cn/exchangeinfo/govbuy/cggg/index_{}.jhtml',
            'http://ggzy.zhuhai.gov.cn/exchangeinfo/govbuy/zcjggs/index_{}.jhtml',
            'http://ggzy.zhuhai.gov.cn/exchangeinfo/govbuy/zcjggg/index_{}.jhtml',
            'http://ggzy.zhuhai.gov.cn/exchangeinfo/govbuy/gzgg/index_{}.jhtml',
            'http://ggzy.zhuhai.gov.cn/exchangeinfo/jsgc/zbgg/index_{}.jhtml',
            'http://ggzy.zhuhai.gov.cn/exchangeinfo/jsgc/zbwjdy/index_{}.jhtml',
            'http://ggzy.zhuhai.gov.cn/exchangeinfo/jsgc/kbjggg/index_{}.jhtml',
            'http://ggzy.zhuhai.gov.cn/exchangeinfo/jsgc/zgscjggs/index_{}.jhtml',
            'http://ggzy.zhuhai.gov.cn/exchangeinfo/jsgc/pbjggs/index_{}.jhtml',
            'http://ggzy.zhuhai.gov.cn/exchangeinfo/jsgc/zbgs/index_{}.jhtml',
            'http://ggzy.zhuhai.gov.cn/exchangeinfo/jsgc/zbjj/index_{}.jhtml',
            'http://ggzy.zhuhai.gov.cn/exchangeinfo/jsgc/xmyq/index_{}.jhtml',
            'http://ggzy.zhuhai.gov.cn/exchangeinfo/jsgc/JSGCZBSBGG/index_{}.jhtml',
            'http://ggzy.zhuhai.gov.cn/exchangeinfo/jsgc/xmtz/index_{}.jhtml',
            'http://ggzy.zhuhai.gov.cn/exchangeinfo/jsgc/zbzz/index_{}.jhtml',
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
            detail = html.xpath('/html/body/div[4]/div[2]/div[2]/div[2]/ul/li')
            for li in detail:
                title = li.xpath('./a/@title')[0]
                url_ = li.xpath('./a/@href')[0]
                try:
                    date_Today = li.xpath('./a/span/text()')[0]
                except:
                    date_Today = li.xpath('./span/text()')[0]
                # print(title, url_, date_Today)
                # time.sleep(666)
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

    # 甘南藏族自治州资源交易中心
    def gannan(self):
        print('甘南藏族自治州资源交易中心', 'http://ggzyjy.gnzrmzf.gov.cn')
        url_list = [
            'http://ggzyjy.gnzrmzf.gov.cn/f/newtrade/annogoods/getAnnoList?pageNo={}&pageSize=20&tradeStatus=0&prjpropertycode=1%2C2%2C3%2C4%2C5%2C6%2C7%2C8%2C9%2C10%2C11&prjpropertycode=21%2C22%2C23%2C24&prjpropertycode=31&prjpropertycode=13%2C14%2C15%2C16%2C18%2C19%2C20&prjpropertycode=600&tradeArea=14&projectname=&tabType=2&tradeType=',
            'http://ggzyjy.gnzrmzf.gov.cn/f/newtrade/annogoods/getAnnoList?pageNo={}&pageSize=20&tradeStatus=0&prjpropertycode=1%2C2%2C3%2C4%2C5%2C6%2C7%2C8%2C9%2C10%2C11&prjpropertycode=21%2C22%2C23%2C24&prjpropertycode=31&prjpropertycode=13%2C14%2C15%2C16%2C18%2C19%2C20&prjpropertycode=600&tradeArea=14&projectname=&tabType=1&tradeType=',
            'http://ggzyjy.gnzrmzf.gov.cn/f/newtrade/annogoods/getAnnoList?pageNo={}&pageSize=20&tradeStatus=0&prjpropertycode=1%2C2%2C3%2C4%2C5%2C6%2C7%2C8%2C9%2C10%2C11&prjpropertycode=21%2C22%2C23%2C24&prjpropertycode=31&prjpropertycode=13%2C14%2C15%2C16%2C18%2C19%2C20&prjpropertycode=600&tradeArea=14&projectname=&tabType=3&tradeType=']

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
            detail = html.xpath('//*[@class="byTradingDetail-Con byTradingDetail-ConActive"]/dl')
            for li in detail:
                title = li.xpath('string(./dd/a)').replace('\xa0', '').replace('\n', ''). \
                    replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
                url_ = li.xpath('./dd/a/@href')[0]
                url_ = 'http://ggzyjy.gnzrmzf.gov.cn/f/newtenderproject/flowBidpackage?tenderprojectid={}&projectType=H02' \
                    .format(url_.replace('/f/newtenderproject/', '').replace('/flowpage', ''))
                date_Today = li.xpath('./dd/span/text()')[0].replace('\xa0', '').replace('\n', ''). \
                    replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '') \
                    .replace('[', '').replace(']', '').replace('/', '-')
                if date_Today == '':
                    date_Today = li.xpath('./dd/span[2]/text()')[0].replace('\xa0', '').replace('\n', ''). \
                        replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '') \
                        .replace('[', '').replace(']', '').replace('/', '-')
                if 'http' not in url_:
                    url_ = 'http://ggzyjy.gnzrmzf.gov.cn' + url_
                # print(title, url_, date_Today)
                # time.sleep(666)
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

    # 羌胡市公共资源交易中心
    def wuhu(self):
        print('羌胡市公共资源交易中心', 'http://whsggzy.wuhu.gov.cn')
        url_list = [
            'http://whsggzy.wuhu.gov.cn/jyxx/005001/005001001/{}.html',
            'http://whsggzy.wuhu.gov.cn/jyxx/005001/005001002/{}.html',
            'http://whsggzy.wuhu.gov.cn/jyxx/005001/005001003/{}.html',
            'http://whsggzy.wuhu.gov.cn/jyxx/005001/005001004/{}.html',
            'http://whsggzy.wuhu.gov.cn/jyxx/005001/005001005/{}.html',
            'http://whsggzy.wuhu.gov.cn/jyxx/005002/005002001/{}.html',
            'http://whsggzy.wuhu.gov.cn/jyxx/005002/005002002/{}.html',
            'http://whsggzy.wuhu.gov.cn/jyxx/005002/005002003/{}.html',
            'http://whsggzy.wuhu.gov.cn/jyxx/005002/005002004/{}.html',
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
                text = tool.requests_get(url.format('moreinfo_listjy'), headers)
            else:
                text = tool.requests_get(url.format(page), headers)
            html = HTML(text)
            code = url.replace('http://whsggzy.wuhu.gov.cn/jyxx/', '').replace('005001/', '').replace('/{}.html',
                                                                                                           '').replace(
                '005002/', '')
            detail = html.xpath('//*[@id="list{}body"]/tr'.format(code))
            for li in detail:
                title = li.xpath('./td[2]/a/text()')[0]
                url_ = 'http://whsggzy.wuhu.gov.cn' + li.xpath('./td[2]/a/@href')[0]
                date_Today = li.xpath('./td[3]/text()')[0]
                # print(title, url, date_Today)
                # time.sleep(666)
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

    # 肇庆市公共资源交易平台
    def zhaoqing(self):
        print('肇庆市公共资源交易平台', 'http://61.146.213.251')
        url_list = [
            'http://61.146.213.251/zqfrontnew/showinfo/moreinfolist.aspx?categorynum=003001001&Paging={}',
            'http://61.146.213.251/zqfrontnew/jyxx/003001/003001002/?pageing={}',
            'http://61.146.213.251/zqfrontnew/jyxx/003001/003001003/?pageing={}',#结果
            'http://61.146.213.251/zqfrontnew/showinfo/moreinfolist.aspx?categorynum=003002001&Paging={}',
            'http://61.146.213.251/zqfrontnew/jyxx/003002/003002002/?pageing={}',
            'http://61.146.213.251/zqfrontnew/jyxx/003002/003002003/?pageing={}',
            'http://61.146.213.251/zqfrontnew/jyxx/003006/003006001/?pageing={}',
            'http://61.146.213.251/zqfrontnew/jyxx/003006/003006002/?pageing={}',
            'http://61.146.213.251/zqfrontnew/jyxx/003006/003006003/?pageing={}',
            'http://61.146.213.251/zqfrontnew/jyxx/003006/003006004/?pageing={}'
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
            # print(11, text)
            # time.sleep(6666)
            if 'moreinfolist' in url:
                detail = html.xpath('//*[@id="form1"]/div[3]/div[1]/ul/li')
            else:
                detail = html.xpath('/html/body/div[1]/ul/li')
            for li in detail:
                try:
                    title = li.xpath('./a/@title')[0]
                except:
                    title = li.xpath('./a/text()')[0]
                url_ = li.xpath('./a/@href')[0]
                date_Today = li.xpath('./span/text()')[0].replace('\xa0', '').replace('\n', ''). \
                    replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
                if 'http' not in url_:
                    url_ = 'http://61.146.213.251' + url_
                # print(title, url, date_Today)
                # time.sleep(666)
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

    # 赤峰市公共资源交易中心
    def chifeng(self):
        print('赤峰市公共资源交易中心', 'http://ggzy.chifeng.gov.cn')
        url_list = [
                    'http://ggzy.chifeng.gov.cn/EpointWeb_CF/jyxx_cf/003001/003001001/003001001001/?COLLCC=3495631849&',        #建设工程 招标公告
                    'http://ggzy.chifeng.gov.cn/EpointWeb_CF/jyxx_cf/003001/003001001/003001001002/?COLLCC=3495631849&',
                    'http://ggzy.chifeng.gov.cn/EpointWeb_CF/jyxx_cf/003001/003001001/003001001003/?COLLCC=3495631849&',
                    'http://ggzy.chifeng.gov.cn/EpointWeb_CF/jyxx_cf/003001/003001001/003001001004/?COLLCC=3495631849&',
                    'http://ggzy.chifeng.gov.cn/EpointWeb_CF/jyxx_cf/003001/003001001/003001001005/?COLLCC=3495631849&',
                    'http://ggzy.chifeng.gov.cn/EpointWeb_CF/jyxx_cf/003001/003001001/003001001006/?COLLCC=3495631849&',
                    'http://ggzy.chifeng.gov.cn/EpointWeb_CF/jyxx_cf/003001/003001003/003001003001/?COLLCC=3495631849&',        #中标公示
                    'http://ggzy.chifeng.gov.cn/EpointWeb_CF/jyxx_cf/003001/003001003/003001003002/?COLLCC=3495631849&',
                    'http://ggzy.chifeng.gov.cn/EpointWeb_CF/jyxx_cf/003001/003001003/003001003003/?COLLCC=3495631849&',
                    'http://ggzy.chifeng.gov.cn/EpointWeb_CF/jyxx_cf/003001/003001003/003001003004/?COLLCC=3495631849&',
                    'http://ggzy.chifeng.gov.cn/EpointWeb_CF/jyxx_cf/003001/003001003/003001003005/?COLLCC=3495631849&',
                    'http://ggzy.chifeng.gov.cn/EpointWeb_CF/jyxx_cf/003001/003001003/003001003006/?COLLCC=3495631849&',
                    'http://ggzy.chifeng.gov.cn/EpointWeb_CF/jyxx_cf/003001/003001005/003001005001/?COLLCC=3495631849&',        #结果公告
                    'http://ggzy.chifeng.gov.cn/EpointWeb_CF/jyxx_cf/003001/003001005/003001005002/?COLLCC=3495631849&',
                    'http://ggzy.chifeng.gov.cn/EpointWeb_CF/jyxx_cf/003001/003001005/003001005003/?COLLCC=3495631849&',
                    'http://ggzy.chifeng.gov.cn/EpointWeb_CF/jyxx_cf/003001/003001005/003001005004/?COLLCC=3495631849&',
                    'http://ggzy.chifeng.gov.cn/EpointWeb_CF/jyxx_cf/003001/003001005/003001005005/?COLLCC=3495631849&',
                    'http://ggzy.chifeng.gov.cn/EpointWeb_CF/jyxx_cf/003001/003001005/003001005006/?COLLCC=3495631849&',
                    'http://ggzy.chifeng.gov.cn/EpointWeb_CF/jyxx_cf/003001/003001006/003001006001/?COLLCC=3495631849&',         #开标结果
                    'http://ggzy.chifeng.gov.cn/EpointWeb_CF/jyxx_cf/003001/003001006/003001006002/?COLLCC=3495631849&',
                    'http://ggzy.chifeng.gov.cn/EpointWeb_CF/jyxx_cf/003001/003001006/003001006003/?COLLCC=3495631849&',
                    'http://ggzy.chifeng.gov.cn/EpointWeb_CF/jyxx_cf/003001/003001006/003001006004/?COLLCC=3495631849&',
                    'http://ggzy.chifeng.gov.cn/EpointWeb_CF/jyxx_cf/003001/003001006/003001006005/?COLLCC=3495631849&',
                    'http://ggzy.chifeng.gov.cn/EpointWeb_CF/jyxx_cf/003001/003001006/003001006006/?COLLCC=3495631849&'
                    ]
        headers = {
            'Cookie': 'ASP.NET_SessionId=njryktrsd23lij35rymqqo0o',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        }
        url = url_list.pop(0)
        page = 0
        ls = []
        while True:
            page += 1
            text = tool.requests_get(url, headers)
            detail = HTML(text).xpath('/html/body/div[2]/div/div[2]/div[2]/div/table/tr')
            for li in detail:
                try:
                    title = li.xpath('./td[2]/a/@title')[0]
                    url_ = 'http://ggzy.chifeng.gov.cn' + li.xpath('./td[2]/a/@href')[0]
                    date_Today = li.xpath('./td[3]/text()')[0].replace('[', '').replace(']', '')
                except:
                    continue
                # print(title, url, date_Today)
                # time.sleep(666)
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

    # 辽源市公共资源交易中心
    def liaoyuan(self):
        print('辽源市公共资源交易中心', 'http://ggzy.liaoyuan.gov.cn')
        url_list = [
            'http://ggzy.liaoyuan.gov.cn/jyxx/003001/003001001/{}.html', #招标公告
            'http://ggzy.liaoyuan.gov.cn/jyxx/003001/003001002/{}.html', #变更公告
            'http://ggzy.liaoyuan.gov.cn/jyxx/003001/003001003/{}.html',  # 建设 中标
            'http://ggzy.liaoyuan.gov.cn/jyxx/003002/003002003/{}.html',#采购 中标
            'http://ggzy.liaoyuan.gov.cn/jyxx/003002/003002001/{}.html',
            'http://ggzy.liaoyuan.gov.cn/jyxx/003002/003002002/{}.html',
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
            detail = html.xpath('/html/body/div/div[2]/div[2]/div[2]/ul/li')
            for li in detail:
                title = li.xpath('./a/text()')[1].replace('\n', ''). \
                    replace('\r', '').replace('\t', '').replace(' ', '')
                url_ = 'http://ggzy.liaoyuan.gov.cn' + li.xpath('./a/@href')[0]
                date_Today = li.xpath('./span/text()')[0].replace('\xa0', '').replace('\n', ''). \
                    replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
                # print(title, url, date_Today)
                # time.sleep(666)
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

    # 通化市公共资源交易中心
    def tonghua(self):
        print('通化市公共资源交易中心', 'http://thsggzyjy.tonghua.gov.cn')
        url_list = [
            'http://thsggzyjy.tonghua.gov.cn/jyxx/004001/{}.html', #招标公告
            'http://thsggzyjy.tonghua.gov.cn/jyxx/004002/{}.html',#采购 中标
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
                text = tool.requests_get(url.format('pageabout'), headers)
            else:
                text = tool.requests_get(url.format(page), headers)
            html = HTML(text)
            detail = html.xpath('/html/body/div[2]/div/div[2]/div[2]/div[2]/ul/li')
            for li in detail:
                title = li.xpath('./div/a/text()')[0].replace('\n', ''). \
                    replace('\r', '').replace('\t', '').replace(' ', '')
                url_ = 'http://thsggzyjy.tonghua.gov.cn' + li.xpath('./div/a/@href')[0]
                date_Today = li.xpath('./span/text()')[0].replace('\xa0', '').replace('\n', ''). \
                    replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
                # print(title, url, date_Today)
                # time.sleep(666)
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

    # 通辽市公共资源交易中心
    def tongliao(self):
        print('通辽市公共资源交易中心', 'http://ggzy.tongliao.gov.cn')
        url_list = [
            'http://ggzy.tongliao.gov.cn/EpointWebBuilder_tlsggzy/jyxxInfoAction.action?cmd=getInfolist&fbdate=10&jyfrom=&xxtype=010&jytype=&title=&pageSize=12&pageIndex={}',        #工程建设
            'http://ggzy.tongliao.gov.cn/EpointWebBuilder_tlsggzy/jyxxInfoAction.action?cmd=getInfolist&fbdate=10&jyfrom=&xxtype=011&jytype=&title=&pageSize=12&pageIndex={}'
        ]       #政府采购

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
                title = li['realtitle']
                url_ = 'http://ggzy.tongliao.gov.cn' + li['infourl']
                date_Today = li['infodate'].replace('[', '').replace(']', '').replace('\r',
                                                                                                     '').replace(
                    '\n', '').replace('\t', '').replace(' ', '')
                if '附件' in title:
                    continue
                # print(title, url, date_Today)
                # time.sleep(666)
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

    # 鄂尔多斯公共资源交易中心
    def eerduosi(self):
        print('鄂尔多斯公共资源交易中心', 'http://www.ordosggzyjy.org.cn')
        url_list = [
             'http://www.ordosggzyjy.org.cn/TPFront/showinfo/MoreListSqhb.aspx?CategoryNum=009001',
             'http://www.ordosggzyjy.org.cn/TPFront/showinfo/MoreListSqhb.aspx?CategoryNum=009002',
             'http://www.ordosggzyjy.org.cn/TPFront/showinfo/MoreListSqhb.aspx?CategoryNum=009003',
             'http://www.ordosggzyjy.org.cn/TPFront/showinfo/MoreListSqhb.aspx?CategoryNum=009004',
             'http://www.ordosggzyjy.org.cn/TPFront/showinfo/MoreListSqhb.aspx?CategoryNum=009005',
             'http://www.ordosggzyjy.org.cn/TPFront/showinfo/MoreListSqhb.aspx?CategoryNum=009006',
             'http://www.ordosggzyjy.org.cn/TPFront/showinfo/MoreListSqhb.aspx?CategoryNum=009007',
             'http://www.ordosggzyjy.org.cn/TPFront/showinfo/MoreListSqhb.aspx?CategoryNum=009008',
             'http://www.ordosggzyjy.org.cn/TPFront/zfcg/010001/?Paging=1',
             'http://www.ordosggzyjy.org.cn/TPFront/zfcg/010003/?categorynum=010003',
             'http://www.ordosggzyjy.org.cn/TPFront/zfcg/010005/?categorynum=010005',
             'http://www.ordosggzyjy.org.cn/TPFront/zfcg/010006/?categorynum=010006',
             'http://www.ordosggzyjy.org.cn/TPFront/zfcg/010010/?categorynum=010010',
             'http://www.ordosggzyjy.org.cn/TPFront/zfcg/010008/010008001/?categorynum=010008001',
             'http://www.ordosggzyjy.org.cn/TPFront/zfcg/010008/010008002/?categorynum=010008002',
             'http://www.ordosggzyjy.org.cn/TPFront/zfcg/010008/010008004/?categorynum=010008004',
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
            if 'zfcg' in url:
                detail = HTML(text).xpath(
                    '//*[@id="main"]/div[2]/table/tr/td[3]/table/tr[3]/td/div/table/tr/td/table/tr')
            else:
                detail = HTML(text).xpath('//*[@id="DataGrid1"]/tr')
            for li in detail:
                if 'zfcg' not in url:
                    title = li.xpath('./td[3]/a/@title')[0]
                    url_ = 'http://www.ordosggzyjy.org.cn' + li.xpath('./td[3]/a/@href')[0]
                    date_Today = li.xpath('./td[4]/text()')[0].replace('[', '').replace(']', '').replace('\r',
                                                                                                         '').replace(
                        '\n', '').replace('\t', '').replace(' ', '')
                else:
                    try:
                        title = li.xpath('./td[2]/a/@title')[0]
                        url_ = 'http://www.ordosggzyjy.org.cn' + li.xpath('./td[2]/a/@href')[0]
                        date_Today = li.xpath('./td[3]/text()')[0].replace('[', '').replace(']', '').replace('\r',
                                                                                                             '').replace(
                            '\n', '').replace('\t', '').replace(' ', '')
                    except:
                        continue
                # print(title, url, date_Today)
                # time.sleep(666)
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

    # 铜陵市公共资源交易中心
    def tongling(self):
        print('铜陵市公共资源交易中心', 'http://ggzyjyzx.tl.gov.cn')
        url_list = [
            'http://ggzyjyzx.tl.gov.cn/tlsggzy/ZtbInfo/zhaobiao.aspx?categorynum=006001001&Paging={}', #招标公告
            'http://ggzyjyzx.tl.gov.cn/tlsggzy/ZtbInfo/zhaobiao.aspx?categorynum=007001001&Paging={}',
            'http://ggzyjyzx.tl.gov.cn/tlsggzy/ZtbInfo/zhaobiao.aspx?categorynum=006001006&Paging={}',
            'http://ggzyjyzx.tl.gov.cn/tlsggzy/ZtbInfo/zhaobiao.aspx?categorynum=007001006&Paging={}',
            'http://ggzyjyzx.tl.gov.cn/tlsggzy/ZtbInfo/zhaobiao.aspx?categorynum=006001002&Paging={}',  # 招标公告
            'http://ggzyjyzx.tl.gov.cn/tlsggzy/ZtbInfo/zhaobiao.aspx?categorynum=007001002&Paging={}',
            'http://ggzyjyzx.tl.gov.cn/tlsggzy/ZtbInfo/zhaobiao.aspx?categorynum=006001003&Paging={}',  # 招标公告
            'http://ggzyjyzx.tl.gov.cn/tlsggzy/ZtbInfo/zhaobiao.aspx?categorynum=007001004&Paging={}',
            'http://ggzyjyzx.tl.gov.cn/tlsggzy/ZtbInfo/zhaobiao.aspx?categorynum=006001004&Paging={}',
            'http://ggzyjyzx.tl.gov.cn/tlsggzy/ZtbInfo/zhaobiao.aspx?categorynum=006001004&Paging={}'
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
            detail = html.xpath('//*[@id="DataGrid1"]/tr')
            for li in detail:
                title = li.xpath('./td[2]/a/text()')[0].replace('\n', ''). \
                    replace('\r', '').replace('\t', '').replace(' ', '')
                url_ = 'http://ggzyjyzx.tl.gov.cn' + li.xpath('./td[2]/a/@href')[0]
                date_Today = '20' + li.xpath('./td[3]/span/text()')[0].replace('\xa0', '').replace('\n', ''). \
                    replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
                # print(title, url, date_Today)
                # time.sleep(666)
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

    # 鹤岗市公共资源交易中心
    def hegang(self):
        print('鹤岗市公共资源交易中心', 'http://www.hgggzyjyw.org.cn')
        url_list = [
            'http://www.hgggzyjyw.org.cn/gcjs/{}.html', #变更公告
            'http://www.hgggzyjyw.org.cn/zfcg/{}.html'
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
            detail = html.xpath('/html/body/div[2]/div/div/div[2]/div[2]/div[2]/ul/li')
            for li in detail:
                title = li.xpath('./a/@title')[0].replace('\n', ''). \
                    replace('\r', '').replace('\t', '').replace(' ', '')
                url_ = 'http://www.hgggzyjyw.org.cn' + li.xpath('./a/@href')[0]
                date_Today = li.xpath('./span/text()')[0].replace('\xa0', '').replace('\n', ''). \
                    replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
                # print(title, url, date_Today)
                # time.sleep(666)
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

    # 黄山市公共资源交易中心
    def huangshan(self):
        print('黄山市公共资源交易中心', 'http://ggzy.huangshan.gov.cn')
        url_list = [
            'http://ggzy.huangshan.gov.cn/EpointWebBuilder/rest/webbuilderserverforHeFZTB/getinfolistnew'
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
            data = {'params': '{"categorynum":"004","xiaqucode":"","title":"","startdate":"","enddate":"","siteguid":"7eb5f7f1-9041-43ad-8e13-8fcb82ea831a","pageSize":10,"pageIndex":'+str(page)+'}'}
            text = tool.requests_post(url, data, headers)
            detail = json.loads(text)['infoList']
            for li in detail:
                title = li['title']
                url_ = 'http://ggzy.huangshan.gov.cn/004/{}/{}/{}/{}.html'.format(li['categorynum'][:6], li['categorynum']
                                                                                  , li['infodate'].replace('-', ''), li['infoid'])
                date_Today = li['infodate']
                # print(title, url, date_Today)
                # time.sleep(666)
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

    # 齐齐哈尔市公共资源交易中心
    def qiqihaer(self):
        print('齐齐哈尔市公共资源交易中心', 'http://ggzy.qqhr.gov.cn')
        url_list = [
            'http://ggzy.qqhr.gov.cn/jyxx/003001/{}.html',#采购 中标
            'http://ggzy.qqhr.gov.cn/jyxx/003002/{}.html'
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
                title = li.xpath('./div/a/text()')[0].replace('\n', ''). \
                    replace('\r', '').replace('\t', '').replace(' ', '')
                url_ = 'http://ggzy.qqhr.gov.cn' + li.xpath('./div/a/@href')[0]
                date_Today = li.xpath('./span/text()')[0].replace('\xa0', '').replace('\n', ''). \
                    replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
                # print(title, url, date_Today)
                # time.sleep(666)
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


