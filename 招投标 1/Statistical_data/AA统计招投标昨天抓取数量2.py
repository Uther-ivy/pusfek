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
            [self.linxia,'http://ggzyjy.linxia.gov.cn'],
            [self.yunyang, 'http://www.yunyang.gov.cn'],
            [self.wufeng, 'http://ggzyjy.hbwf.gov.cn'],
            [self.liuan, 'http://ggjfwpt.luan.gov.cn'],
            [self.beilun, 'http://www.bl91.com'],
            [self.beihai, 'http://www.bhsggzy.cn'],
            [self.nanning, 'https://nnggzy.org.cn'],
            [self.xiamen, 'http://www.xmzyjy.cn'],
            [self.haerbin, 'http://hrbggzy.org.cn'],
            # [self.tangshan, 'http://eps.jidd-jdsb.com'], 打不开
            [self.guyaun, 'http://www.gysggzyjy.cn'],
            [self.daqing, 'http://ggzyjyzx.daqing.gov.cn'],
            [self.ningde, 'http://ggzyjy.xzfw.ningde.gov.cn'],
            [self.ningbo, 'http://zjcs.nbxzfw.gov.cn'],
            [self.anqing, 'http://aqggzy.anqing.gov.cn'],
            [self.baoan, 'http://www.baoan.gov.cn'],
            [self.shandong, 'https://www.sdbidding.org.cn'],
            [self.chongzuo, 'http://www.czjyzx.gov.cn'],
            [self.pingli, 'http://www.pingli.gov.cn'],
            [self.guangzhou, 'http://gzg2b.gzfinance.gov.cn'],
            [self.guangxi, 'http://www.gigeps.com'],
            [self.guangxizhaobiao, 'http://www.guangxibid.com.cn'],
            [self.deqing, 'http://ggzy.deqing.gov.cn'],
            [self.chengdu, 'https://ep.cdmetro.cn:1443'],
            [self.chaoxian, 'http://ybggzy.com'],
            [self.liuzhou, 'http://login.ggzy.liuzhou.gov.cn'],
            [self.guilin, 'http://glggzy.org.cn'],
            [self.wuzhou, 'http://www.wzggzy.cn'],
            [self.yuyang, 'http://www.yuyang.gov.cn'],
            [self.wuwei, 'http://gzjy.gswuwei.gov.cn'],
            [self.chizhou, 'http://ggj.chizhou.gov.cn'],
            [self.hechi, 'http://218.65.221.79'],
            [self.quanzhou, 'http://ggzyjy.quanzhou.gov.cn'],
            [self.zibo, 'http://ggzyjy.zibo.gov.cn'],
            [self.huanbei, 'http://ggzy.huaibei.gov.cn'],
            [self.jiaozuo, 'http://www.jzggzy.cn'],
            [self.yulin, 'http://202.103.240.162'],
            [self.baise, 'http://www.bsggzy.org.cn'],
            [self.suzhou, 'http://www.szzyjy.com.cn'],
            [self.suzhouzf, 'http://czju.suzhou.gov.cn'],
            # [self.xiaoshan, 'http://www.xszbjyw.com'], 打不开
            [self.bengbu, 'http://ggzy.bengbu.gov.cn'],
            [self.guigang, 'http://ggggjy.gxgg.gov.cn:9005'],
            [self.hezhou, 'http://www.hzggzy.org.cn'],
            [self.qinzhou, 'http://ggzyjy.qinzhou.gov.cn'],
            [self.fuyang, 'http://jyzx.fy.gov.cn'],
            [self.fangchenggang, 'http://www.fcgggzy.cn'],
            [self.qinghai, 'http://www.qhei.net.cn'],
            [self.maanshan, 'http://zbcg.mas.gov.cn']
        ]

    # 临夏州市公共资源交易中心
    def linxia(self):
        print('临夏州市公共资源交易中心', 'http://ggzyjy.linxia.gov.cn')
        url_list = [
            'http://ggzyjy.linxia.gov.cn/f/tenderannquainqueryanns/tenderannquainqueryanns/annquainList?tradeType=1&projectName=&pageNo={}&pageSize=20&isAll=&dataType=0&projectType=2&listType=1&projectname=&prjpropertyid=1,2,3,4,5,6,7,8,10,11,12,13,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,32,31,33&tradeArea=1,18,9,10,11,12,13,14,16&tabType=1',
            'http://ggzyjy.linxia.gov.cn/f/tenderannquainqueryanns/tenderannquainqueryanns/annquainList?tradeType=2&projectName=&pageNo={}&pageSize=20&isAll=&dataType=0&projectType=2&listType=1&projectname=&prjpropertyid=1,2,3,4,5,6,7,8,10,11,12,13,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,32,31,33&tradeArea=1,18,9,10,11,12,13,14,16&tabType=1',
            'http://ggzyjy.linxia.gov.cn/f/tenderannquainqueryanns/tenderannquainqueryanns/annquainList?tradeType=3&projectName=&pageNo={}&pageSize=20&isAll=&dataType=0&projectType=2&listType=1&projectname=&prjpropertyid=1,2,3,4,5,6,7,8,10,11,12,13,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,32,31,33&tradeArea=1,18,9,10,11,12,13,14,16&tabType=1',
            'http://ggzyjy.linxia.gov.cn/f/tenderannquainqueryanns/tenderannquainqueryanns/annquainList?tradeType=4&projectName=&pageNo={}&pageSize=20&isAll=&dataType=0&projectType=2&listType=1&projectname=&prjpropertyid=1,2,3,4,5,6,7,8,10,11,12,13,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,32,31,33&tradeArea=1,18,9,10,11,12,13,14,16&tabType=1'
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
            detail = html.xpath('//*[@class="wq_lx_ggzypzxxItemList hw_list"]/li')
            for li in detail:
                title = li.xpath('./a/div[1]/p/text()')[0].replace('\xa0', '').replace('\n', ''). \
                    replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '').replace(
                    "<fontstyle='color:red'>(网)</font>", '')
                url_ = li.xpath('./a/@href')[0]
                date_Today = li.xpath('./a/span/text()')[0].replace('\xa0', '').replace('\n', ''). \
                    replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '') \
                    .replace('[', '').replace(']', '').replace('/', '-')
                if 'http' not in url_:
                    url_ = 'http://ggzyjy.linxia.gov.cn' + url_
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

    # 云阳县公共资源交易中心
    def yunyang(self):
        print('云阳县公共资源交易中心', 'http://www.yunyang.gov.cn')
        url_list = [
            'http://www.yunyang.gov.cn/zwgk_257/zfxxgkml/{}.html'
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
                text = tool.requests_get(url.format('list'), headers)
            else:
                text = tool.requests_get(url.format('list_' + str(page - 1)), headers)
            html = HTML(text)
            detail = html.xpath('/html/body/div/table/tr')
            for li in detail:
                try:
                    title = li.xpath('./td[1]/a/text()')[0].replace('\xa0', '').replace('\n', ''). \
                        replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '').replace(
                        "<fontstyle='color:red'>(网)</font>", '')
                    url_ = li.xpath('./td[1]/a/@href')[0]
                    date_Today = li.xpath('./td[2]/text()')[0].replace('\xa0', '').replace('\n', ''). \
                        replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '') \
                        .replace('[', '').replace(']', '').replace('/', '-')
                except:
                    continue
                if 'http' not in url_:
                    url_ = 'http://www.yunyang.gov.cn/zwgk_257/zfxxgkml' + url_[1:]
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

    # 五峰土家族公共资源交易中心
    def wufeng(self):
        print('五峰土家族公共资源交易中心', 'http://ggzyjy.hbwf.gov.cn')
        url_list = [
            'http://ggzyjy.hbwf.gov.cn/wfSite/jyxx/003002/003002001/003002001003/?pageing={}',
            'http://ggzyjy.hbwf.gov.cn/wfSite/jyxx/003001/003001001/003001001001/?pageing={}',
            'http://ggzyjy.hbwf.gov.cn/wfSite/jyxx/003001/003001001/003001001002/?pageing={}',
            'http://ggzyjy.hbwf.gov.cn/wfSite/jyxx/003001/003001001/003001001003/?pageing={}',
            'http://ggzyjy.hbwf.gov.cn/wfSite/jyxx/003001/003001002/003001002001/?pageing={}',
            'http://ggzyjy.hbwf.gov.cn/wfSite/jyxx/003001/003001002/003001002002/?pageing={}',
            'http://ggzyjy.hbwf.gov.cn/wfSite/jyxx/003001/003001002/003001002003/?pageing={}',

            'http://ggzyjy.hbwf.gov.cn/wfSite/jyxx/003002/003002001/003002001001/?pageing={}',
            'http://ggzyjy.hbwf.gov.cn/wfSite/jyxx/003002/003002002/003002002001/?pageing={}',
            'http://ggzyjy.hbwf.gov.cn/wfSite/jyxx/003002/003002004/003002004001/?pageing={}',
            'http://ggzyjy.hbwf.gov.cn/wfSite/jyxx/003002/003002004/003002004003/?pageing={}'
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
            text = tool.requests_get(url.format(page), headers)
            html = HTML(text)
            detail = html.xpath('//*[@class="list"]/li')
            for li in detail:
                title = li.xpath('./a/@title')[0].replace('\xa0', '').replace('\n', ''). \
                    replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
                url_ = li.xpath('./a/@href')[0]
                date_Today = li.xpath('./span/text()')[0].replace('\xa0', '').replace('\n', ''). \
                    replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '') \
                    .replace('[', '').replace(']', '').replace('/', '-')
                if 'http' not in url_:
                    url_ = 'http://ggzyjy.hbwf.gov.cn' + url_
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

    # 六安市公共资源交易中心
    def liuan(self):
        print('六安市公共资源交易中心', 'http://ggjfwpt.luan.gov.cn')
        url_list = [
            'http://ggjfwpt.luan.gov.cn/EpointWebBuilder/rest/GgSearchAction/getJyInfoList'
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
            data = {
                'params': '{"siteGuid":"7eb5f7f1-9041-43ad-8e13-8fcb82ea831a","keywords":"","fbdate":"","jyly":"","categoryNum":"001","jyfs":"","pageIndex":' + str(
                    page) + ',"pageSize":10}'
            }
            page += 1
            text = tool.requests_post(url, data, headers)
            detail = json.loads(text)['Table']
            for li in detail:
                title = li['title1'].replace('\xa0', '').replace('\n', ''). \
                    replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
                url_ = li['infourl']
                date_Today = li['infodate'].replace('\xa0', '').replace('\n', ''). \
                    replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '') \
                    .replace('[', '').replace(']', '').replace('/', '-')
                if 'http' not in url_:
                    url_ = 'http://ggjfwpt.luan.gov.cn' + url_
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

    # 北仑区人民医院
    def beilun(self):
        print('北仑区人民医院', 'http://www.bl91.com')
        url_list = [
            'http://www.bl91.com/col/col7395/{}.html'
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
                text = tool.requests_get(url.format(page), headers)
            detail = re.findall('''<record><!(.*?)</recordset>''', text, re.S)[0].replace('[CDATA[', '').replace('\n',
                                                                                                                 '') \
                .replace('\r', '').replace('\t', '').replace(' ', '').split('</record>')
            for li in detail:
                l = re.findall(
                    '<li><span></span><spanclass="sj">(.*?)</span><ahref="(.*?)"target="_blank"title="(.*?)</a></li>]]>',
                    li)[0]
                # print(11, l)
                # time.sleep(6666)
                title = l[2]
                url_ = l[1]
                date_Today = l[0].replace('\xa0', '').replace('\n', ''). \
                    replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '') \
                    .replace('[', '').replace(']', '').replace('/', '-')
                if 'http' not in url_:
                    url_ = 'http://www.bl91.com' + url_
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

    # 北海市公共资源交易中心
    def beihai(self):
        print('北海市公共资源交易中心', 'http://www.bhsggzy.cn')
        url_list = [
            'http://www.bhsggzy.cn/gxbhzbw/jyxx/001001/001001001/MoreInfo.aspx?CategoryNum=001001001',
            'http://www.bhsggzy.cn/gxbhzbw/jyxx/001001/001001002/MoreInfo.aspx?CategoryNum=001001002',
            'http://www.bhsggzy.cn/gxbhzbw/jyxx/001001/001001004/MoreInfo.aspx?CategoryNum=001001004',
            'http://www.bhsggzy.cn/gxbhzbw/jyxx/001001/001001005/MoreInfo.aspx?CategoryNum=001001005',
            'http://www.bhsggzy.cn/gxbhzbw/jyxx/001001/001001006/MoreInfo.aspx?CategoryNum=001001006',#结果

            'http://www.bhsggzy.cn/gxbhzbw/jyxx/001004/001004001/MoreInfo.aspx?CategoryNum=001004001',
            'http://www.bhsggzy.cn/gxbhzbw/jyxx/001004/001004002/MoreInfo.aspx?CategoryNum=001004002',
            'http://www.bhsggzy.cn/gxbhzbw/jyxx/001004/001004004/MoreInfo.aspx?CategoryNum=001004004',

            'http://www.bhsggzy.cn/gxbhzbw/jyxx/001010/001010001/MoreInfo.aspx?CategoryNum=001010001',
            'http://www.bhsggzy.cn/gxbhzbw/jyxx/001010/001010002/MoreInfo.aspx?CategoryNum=001010002',
            'http://www.bhsggzy.cn/gxbhzbw/jyxx/001010/001010003/MoreInfo.aspx?CategoryNum=001010003',
            'http://www.bhsggzy.cn/gxbhzbw/jyxx/001010/001010004/MoreInfo.aspx?CategoryNum=001010004',
            'http://www.bhsggzy.cn/gxbhzbw/jyxx/001011/001011001/MoreInfo.aspx?CategoryNum=001011001',
            'http://www.bhsggzy.cn/gxbhzbw/jyxx/001011/001011002/MoreInfo.aspx?CategoryNum=001011002',
            'http://www.bhsggzy.cn/gxbhzbw/jyxx/001011/001011004/MoreInfo.aspx?CategoryNum=001011004',
        ]
        headers = {
            'Cookie': 'homeid=1a444a31-e460-47ff-9931-1c075c0f3cd8',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        }
        url = url_list.pop(0)
        page = 0
        ls = []
        data = {
            '__VIEWSTATE': str(page),
            '__VIEWSTATEGENERATOR': 'D4683C32',
            '__EVENTTARGET': 'MoreInfoList1$Pager',
            '__EVENTARGUMENT': page,
            '__VIEWSTATEENCRYPTED': ''
        }
        while True:
            page += 1
            if page == 1:
                text = tool.requests_get(url, headers)
            else:
                text = tool.requests_post(url, data, headers)
            html = HTML(text)
            data['__VIEWSTATE'] = html.xpath('//*[@id="__VIEWSTATE"]/@value')[0]
            data['__EVENTARGUMENT'] = str(page)
            detail = html.xpath('//*[@id="MoreInfoList1_DataGrid1"]/tr')
            for li in detail:
                title = li.xpath('./td[2]/a/@title')[0].replace('\xa0', '').replace('\n', ''). \
                    replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
                url_ = li.xpath('./td[2]/a/@href')[0]
                date_Today = li.xpath('./td[3]/text()')[0].replace('\xa0', '').replace('\n', ''). \
                    replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '') \
                    .replace('[', '').replace(']', '').replace('/', '-')
                if 'http' not in url_:
                    url_ = 'http://www.bhsggzy.cn' + url_
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

    # 南宁市公共资源交易中心
    def nanning(self):
        print('南宁市公共资源交易中心', 'https://nnggzy.org.cn')
        url_list = [
            'https://nnggzy.org.cn/nnzbwmanger/ShowInfo/more.aspx?categoryNum=001001001',
            'https://nnggzy.org.cn/nnzbwmanger/ShowInfo/more.aspx?categoryNum=001001002',
            'https://nnggzy.org.cn/nnzbwmanger/ShowInfo/more.aspx?categoryNum=001001004', #控制价
            'https://nnggzy.org.cn/nnzbwmanger/ShowInfo/more.aspx?categoryNum=001001005', #结果
            'https://nnggzy.org.cn/nnzbwmanger/ShowInfo/more.aspx?categoryNum=001001006',

            'https://nnggzy.org.cn/nnzbwmanger/ShowInfo/more.aspx?categoryNum=001004001',
            'https://nnggzy.org.cn/nnzbwmanger/ShowInfo/more.aspx?categoryNum=001004002',
            'https://nnggzy.org.cn/nnzbwmanger/ShowInfo/more.aspx?categoryNum=001004008',
            'https://nnggzy.org.cn/nnzbwmanger/ShowInfo/more.aspx?categoryNum=001004004',#结果

            'https://nnggzy.org.cn/nnzbwmanger/ShowInfo/more.aspx?categoryNum=001010001',
            'https://nnggzy.org.cn/nnzbwmanger/ShowInfo/more.aspx?categoryNum=001010002',
            'https://nnggzy.org.cn/nnzbwmanger/ShowInfo/more.aspx?categoryNum=001010004',
            'https://nnggzy.org.cn/nnzbwmanger/ShowInfo/more.aspx?categoryNum=001010005',#结果

            'https://nnggzy.org.cn/nnzbwmanger/ShowInfo/more.aspx?categoryNum=001011001',
            'https://nnggzy.org.cn/nnzbwmanger/ShowInfo/more.aspx?categoryNum=001011002',
            'https://nnggzy.org.cn/nnzbwmanger/ShowInfo/more.aspx?categoryNum=001011004',
            'https://nnggzy.org.cn/nnzbwmanger/ShowInfo/more.aspx?categoryNum=001011005',#结果
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
        data = {
            '__CSRFTOKEN': '/wEFJGIzNmY0OGM2LWZhMmQtNDg4Mi1iZDkwLTYwMTJiZWY0YWNiMw==',
            '__VIEWSTATE': str(page),
            '__EVENTTARGET': 'MoreInfoList1$Pager',
            '__EVENTARGUMENT': page,
            '__VIEWSTATEENCRYPTED': ''
        }
        while True:
            page += 1
            if page == 1:
                text = tool.requests_get(url, headers)
            else:
                text = tool.requests_post(url, data, headers)
            html = HTML(text)
            data['__VIEWSTATE'] = html.xpath('//*[@id="__VIEWSTATE"]/@value')[0]
            data['__EVENTARGUMENT'] = str(page)
            detail = html.xpath('//*[@id="MoreInfoList1_DataGrid1"]/tr')
            for li in detail:
                title = li.xpath('./td[2]/a/@title')[0].replace('\xa0', '').replace('\n', ''). \
                    replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
                url_ = li.xpath('./td[2]/a/@href')[0]
                date_Today = li.xpath('./td[3]/text()')[0].replace('\xa0', '').replace('\n', ''). \
                    replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '') \
                    .replace('[', '').replace(']', '').replace('/', '-')
                if 'http' not in url_:
                    url_ = 'https://nnggzy.org.cn' + url_
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

    # 厦门市公共资源交易中心
    def xiamen(self):
        print('厦门市公共资源交易中心', 'http://www.xmzyjy.cn')
        url_list = [
            'http://www.xmzyjy.cn/XmUiForWeb2.0/project/getBltPage.do',
            'http://www.xmzyjy.cn/XmUiForWeb2.0/project/getAnQuestionPage_project.do',#结果
            'http://www.xmzyjy.cn/XmUiForWeb2.0/project/getEvaBulletinPage.do',
            'http://www.xmzyjy.cn/XmUiForWeb2.0/project/getwinBulletinPage_project.do'
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
            data = {"pageIndex": str(page), "pageSize": "10", "projName": "", "centerId": 0, "showRange": "",
                    "tenderProjType": "", "searchBeginTime": "", "searchEndTime": ""}
            text = tool.requests_post_to(url, data, headers)
            detail = json.loads(text)['data']['dataList']
            for li in detail:
                title = li['projName']
                try:
                    url_ = 'http://www.xmzyjy.cn/XmUiForWeb2.0/xmebid/agentBid.do?leftIndex=F00{}&uniqueId={}&objId={}'.format(
                        num, li['uniqueId'], li['bid'])
                except:
                    url_ = 'http://www.xmzyjy.cn/XmUiForWeb2.0/xmebid/agentBid.do?leftIndex=F00{}&uniqueId={}&objId={}'.format(
                        num, li['uniqueId'], li['id'])
                try:
                    date_Today = li['pubDate'].replace('\xa0', '').replace('\n', ''). \
                        replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
                except:
                    try:
                        date_Today = li['sendTime'].replace('\xa0', '').replace('\n', ''). \
                            replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
                    except:
                        date_Today = li['SEND_TIM'].replace('\xa0', '').replace('\n', ''). \
                            replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
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

    # 哈尔滨市公共资源交易中心
    def haerbin(self):
        print('哈尔滨市公共资源交易中心', 'http://hrbggzy.org.cn')
        url_list = [
            'http://hrbggzy.org.cn/zbgg/{}.html',
            'http://hrbggzy.org.cn/zbgs/{}.html',
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
                text = tool.requests_get(url.format('secondpage'), headers)
            else:
                text = tool.requests_get(url.format(page), headers)
            html = HTML(text)
            detail = html.xpath('//*[@id="showList"]/li')
            for li in detail:
                title = li.xpath('./a/@title')[0].replace('\xa0', '').replace('\n', ''). \
                    replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
                url_ = li.xpath('./a/@href')[0]
                date_Today = li.xpath('./span/text()')[0].replace('\xa0', '').replace('\n', ''). \
                    replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '') \
                    .replace('[', '').replace(']', '').replace('/', '-')
                if 'http' not in url_:
                    url_ = 'http://hrbggzy.org.cn' + url_
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

    # 唐山冀东机电设备有限公司电子采购平台
    def tangshan(self):
        print('唐山冀东机电设备有限公司电子采购平台', 'http://eps.jidd-jdsb.com')
        url_list = [
            'http://eps.jidd-jdsb.com/ForePage/Skin/NewList1.aspx?page={}&pagesize=20&title=%E9%87%87%E8%B4%AD%E5%85%AC%E5%91%8A&keyword=&ClassId=140&GroupId=&ParentId=1',
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
            detail = html.xpath('//*[@id="page"]/div[2]/div[2]/div[2]/ul/li')
            for li in detail:
                title = li.xpath('./a/@title')[0].replace('\xa0', '').replace('\n', ''). \
                    replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '').replace(
                    "<fontstyle='color:red'>(网)</font>", '')
                url_ = li.xpath('./a/@href')[0]
                date_Today = li.xpath('./span/text()')[0].split(' ')[0].replace('\xa0', '').replace('\n', ''). \
                    replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '') \
                    .replace('[', '').replace(']', '').replace('/', '-')
                if 'http' not in url_:
                    url_ = 'http://eps.jidd-jdsb.com' + url_
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

    # 固原市公共资源交易中心
    def guyaun(self):
        print('固原市公共资源交易中心', 'http://www.gysggzyjy.cn')
        url_list = [
            'http://www.gysggzyjy.cn/gysggzyjy/002/002002/{}.html',
            'http://www.gysggzyjy.cn/gysggzyjy/002/002001/{}.html'
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
            detail = html.xpath('//*[@id="GV1"] /tr')
            for li in detail:
                try:
                    title = li.xpath('./td[1]/a/text()')[0].replace('\xa0', '').replace('\n', ''). \
                        replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '').replace(
                        "<fontstyle='color:red'>(网)</font>", '')
                    url_ = li.xpath('./td[1]/a/@href')[0]
                    date_Today = li.xpath('./td[2]/text()')[0][:10].replace('\xa0', '').replace('\n', ''). \
                        replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '') \
                        .replace('[', '').replace(']', '').replace('/', '-')
                except:
                    continue
                if 'http' not in url_:
                    url_ = 'http://www.gysggzyjy.cn' + url_
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

    # 大庆市公共资源交易中心
    def daqing(self):
        print('大庆市公共资源交易中心', 'http://ggzyjyzx.daqing.gov.cn')
        url_list = [
            'http://ggzyjyzx.daqing.gov.cn/jyxxZfcgCggg/{}.htm',
            'http://ggzyjyzx.daqing.gov.cn/jyxxZfcgFbgg/{}.htm',
            'http://ggzyjyzx.daqing.gov.cn/jyxxJsgcZbgg/{}.htm',
            'http://ggzyjyzx.daqing.gov.cn/jyxxJsgcBgcggg/{}.htm'
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
            detail = html.xpath('/html/body/div/div[2]/div[2]/div[2]/div[1]/ul/li')
            for li in detail:
                title = li.xpath('./a/@title')[0].replace('\xa0', '').replace('\n', ''). \
                    replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '').replace(
                    "<fontstyle='color:red'>(网)</font>", '')
                url_ = li.xpath('./a/@href')[0]
                date_Today = li.xpath('./span/text()')[0].replace('\xa0', '').replace('\n', ''). \
                    replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '') \
                    .replace('[', '').replace(']', '').replace('/', '-')
                if 'http' not in url_:
                    url_ = 'http://ggzyjyzx.daqing.gov.cn' + url_
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

    # 宁德市公共资源交易中心
    def ningde(self):
        print('宁德市公共资源交易中心', 'http://ggzyjy.xzfw.ningde.gov.cn')
        url_list = [
            'http://ggzyjy.xzfw.ningde.gov.cn/EpointWebBuilder/rest/frontAppCustomAction/getPageInfoListNew',
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
            data = {
                "params": '{"siteGuid":"7eb5f7f1-9041-43ad-8e13-8fcb82ea831a","categoryNum":"002","startDate":"","endDate":"","kw":"","order":"","diqu":"","xmlx":"","zblx":"","pageIndex":'+str(page)+',"pageSize":8}'}
            page += 1
            text = tool.requests_post(url, data, headers)
            detail = json.loads(text)['custom']['infodata']
            for li in detail:
                title = li['title'].replace("<font color='#0066FF'>", '').replace("</font>", '')
                url_ = 'http://ggzyjy.xzfw.ningde.gov.cn/gcjs/{}/{}/{}.html'.format(li['categorynum'],
                                                                                   li['infodate'].replace('-', ''),
                                                                                   li['infoid'])
                date_Today = li['infodate'].replace('\xa0', '').replace('\n', ''). \
                    replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
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

    # 宁波中介超市网
    def ningbo(self):
        print('宁波中介超市网', 'http://zjcs.nbxzfw.gov.cn')
        url_list = [
            'http://zjcs.nbxzfw.gov.cn/News/Infogg?ClassId=0902&Type=1&page={}&pageSize=15'
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
            detail = html.xpath('/html/body/div[5]/table/tbody/tr')
            for li in detail:
                title = li.xpath('./td[3]/a/text()')[0].replace('\xa0', '').replace('\n', ''). \
                    replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '').replace(
                    "<fontstyle='color:red'>(网)</font>", '')
                url_ = li.xpath('./td[3]/a/@href')[0]
                date_Today = li.xpath('./td[5]/text()')[0].split(' ')[0].replace('\xa0', '').replace('\n', ''). \
                    replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '') \
                    .replace('[', '').replace(']', '').replace('/', '-')
                m = date_Today[5:]
                if int(m[0]) < 10 and m[1] == '-':
                    date_Today = date_Today[:5] + '0' + m
                if 'http' not in url_:
                    url_ = 'http://zjcs.nbxzfw.gov.cn' + url_[2:]
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

    # 安庆市公共资源交易中心
    def anqing(self):
        print('安庆市公共资源交易中心', 'http://aqggzy.anqing.gov.cn')
        url_list = [
            'http://aqggzy.anqing.gov.cn/jyxx/012001/012001001/{}.html',
            'http://aqggzy.anqing.gov.cn/jyxx/012001/012001002/{}.html',
            'http://aqggzy.anqing.gov.cn/jyxx/012001/012001003/{}.html',
            'http://aqggzy.anqing.gov.cn/jyxx/012001/012001004/{}.html',
            'http://aqggzy.anqing.gov.cn/jyxx/012002/012002001/{}.html',
            'http://aqggzy.anqing.gov.cn/jyxx/012002/012002002/{}.html',
            'http://aqggzy.anqing.gov.cn/jyxx/012002/012002003/{}.html',
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
                text = tool.requests_get(url.format('project'), headers)
            else:
                text = tool.requests_get(url.format(page), headers)
            html = HTML(text)
            detail = html.xpath('//*[@id="jt"]/ul/li')
            for li in detail:
                title = li.xpath('./div/a/@title')[0].replace('\xa0', '').replace('\n', ''). \
                    replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
                url_ = li.xpath('./div/a/@href')[0]
                date_Today = li.xpath('./span/text()')[0].replace('\xa0', '').replace('\n', ''). \
                    replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '') \
                    .replace('[', '').replace(']', '').replace('/', '-')
                if 'http' not in url_:
                    url_ = 'http://aqggzy.anqing.gov.cn' + url_
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

    # 宝安区人民政府
    def baoan(self):
        print('宝安区人民政府', 'http://www.baoan.gov.cn')
        url_list = [
            'http://www.baoan.gov.cn/xxgk/zbcg/zfcg/cg/{}.html',
            'http://www.baoan.gov.cn/xxgk/zbcg/gc/zb/{}.html',
            'http://www.baoan.gov.cn/xxgk/zbcg/gyqy/cggg/{}.html',
            'http://www.baoan.gov.cn/xxgk/zbcg/gyqy/bggg/{}.html'
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
            detail = html.xpath('//*[@class="contab_con"]/div')
            for li in detail:
                try:
                    title = li.xpath('./div[2]/p/a/text()')[0].replace('\xa0', '').replace('\n', ''). \
                        replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '').replace(
                        "<fontstyle='color:red'>(网)</font>", '')
                    url_ = li.xpath('./div[2]/p/a/@href')[0]
                    date_Today = li.xpath('./div[3]/span/text()')[0].replace('\xa0', '').replace('\n', ''). \
                        replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '') \
                        .replace('[', '').replace(']', '').replace('/', '-').replace('年', '').replace('月', '').replace(
                        '日', '')
                except:
                    continue
                if 'http' not in url_:
                    url_ = 'http://www.baoan.gov.cn' + url_
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

    # 山东省采购与招标网
    def shandong(self):
        print('山东省采购与招标网', 'https://www.sdbidding.org.cn')
        url_list = [
            'https://www.sdbidding.org.cn/bulletins;jsessionid=4D4235AAE29ABF6302007184DF9AA064?titleLike=&pageNo={}&pageSize=10&infoType=11',
            'https://www.sdbidding.org.cn/bulletins?titleLike=&pageNo={}&pageSize=10&infoType=12',
            'https://www.sdbidding.org.cn/bulletins?titleLike=&pageNo={}&pageSize=10&infoType=13',
            'https://www.sdbidding.org.cn/bulletins?titleLike=&pageNo={}&pageSize=10&infoType=14'
        ]
        headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Cookie': 'Hm_lvt_3bc19bf638a10bf839128052d35265ec=1613793244; JSESSIONID=4C96874F732463A1FA6D3FD7854B3C7A; x-token=eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJVc2VyIiwiZXhwIjoxNjEzOTc4NTkxLCJ1c2VySWQiOjI3ODk5NiwiaWF0IjoxNjEzOTU2OTkxLCJqdGkiOiJqd3QifQ.lNBD3Gnvkx1KpAHj1A6Il9o4TGtTsu00cSVxQeettK4; Hm_lpvt_3bc19bf638a10bf839128052d35265ec=1613956996',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',

        }
        url = url_list.pop(0)
        page = 0
        ls = []
        while True:
            page += 1
            text = tool.requests_get(url.format(page), headers)
            html = HTML(text)
            detail = html.xpath('/html/body/div[2]/div[2]/div[2]/div[1]/table/tr')
            for li in detail:
                try:
                    title = li.xpath('./td[2]/a/@title')[0].replace('\xa0', '').replace('\n', ''). \
                        replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '').replace(
                        "<fontstyle='color:red'>(网)</font>", '')
                    url_ = li.xpath('./td[2]/a/@href')[0]
                    date_Today = li.xpath('./td[5]/text()')[0].replace('\xa0', '').replace('\n', ''). \
                        replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '') \
                        .replace('[', '').replace(']', '').replace('/', '-')
                except:
                    continue
                if 'http' not in url_:
                    url_ = 'https://www.sdbidding.org.cn' + url_
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

    # 崇左市公共资源交易中心
    def chongzuo(self):
        print('崇左市公共资源交易中心', 'http://www.czjyzx.gov.cn')
        url_list = [
            'http://www.czjyzx.gov.cn/gxczzbw/jyxx/001010/001010001/MoreInfo.aspx?CategoryNum=001010001',
            'http://www.czjyzx.gov.cn/gxczzbw/jyxx/001010/001010002/MoreInfo.aspx?CategoryNum=001010002',
            'http://www.czjyzx.gov.cn/gxczzbw/jyxx/001010/001010004/MoreInfo.aspx?CategoryNum=001010004', #结果

            'http://www.czjyzx.gov.cn/gxczzbw/jyxx/001001/001001001/MoreInfo.aspx?CategoryNum=001001001',
            'http://www.czjyzx.gov.cn/gxczzbw/jyxx/001001/001001002/MoreInfo.aspx?CategoryNum=001001002',
            'http://www.czjyzx.gov.cn/gxczzbw/jyxx/001001/001001005/MoreInfo.aspx?CategoryNum=001001005',#结果

            'http://www.czjyzx.gov.cn/gxczzbw/jyxx/001004/001004001/MoreInfo.aspx?CategoryNum=001004001',
            'http://www.czjyzx.gov.cn/gxczzbw/jyxx/001004/001004002/MoreInfo.aspx?CategoryNum=001004002',
            'http://www.czjyzx.gov.cn/gxczzbw/jyxx/001004/001004004/MoreInfo.aspx?CategoryNum=001004004',#结果

            'http://www.czjyzx.gov.cn/gxczzbw/jyxx/001011/001011001/MoreInfo.aspx?CategoryNum=001011001',
            'http://www.czjyzx.gov.cn/gxczzbw/jyxx/001011/001011004/MoreInfo.aspx?CategoryNum=001011004',
            'http://www.czjyzx.gov.cn/gxczzbw/jyxx/001011/001011002/MoreInfo.aspx?CategoryNum=001011002'#结果
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
            '__VIEWSTATE': str(page),
            '__VIEWSTATEGENERATOR': 'C06A8508',
            '__EVENTTARGET': 'MoreInfoList1$Pager',
            '__EVENTARGUMENT': page,
            '__VIEWSTATEENCRYPTED': ''
        }
        while True:
            page += 1
            if page == 1:
                text = tool.requests_get(url, headers)
            else:
                text = tool.requests_post(url, data, headers)
            html = HTML(text)
            data['__VIEWSTATE'] = html.xpath('//*[@id="__VIEWSTATE"]/@value')[0]
            data['__EVENTARGUMENT'] = str(page)
            detail = html.xpath('//*[@id="MoreInfoList1_DataGrid1"]/tr')
            for li in detail:
                title = li.xpath('./td[2]/a/@title')[0].replace('\xa0', '').replace('\n', ''). \
                    replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
                url_ = li.xpath('./td[2]/a/@href')[0]
                date_Today = li.xpath('./td[3]/text()')[0].replace('\xa0', '').replace('\n', ''). \
                    replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '') \
                    .replace('[', '').replace(']', '').replace('/', '-')
                if 'http' not in url_:
                    url_ = 'http://www.czjyzx.gov.cn' + url_
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

    # 平利县人民政府
    def pingli(self):
        print('平利县人民政府', 'http://www.pingli.gov.cn')
        url_list = [
            '2090', '2088'
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
        url_to = 'http://www.pingli.gov.cn/special/{}.html'
        while True:
            page += 1
            if page == 1:
                text = tool.requests_get(url_to.format(url), headers)
            else:
                text = tool.requests_get(url_to.format(url + '_' + page), headers)
            html = HTML(text)
            detail = html.xpath('//*[@id="container"]/div[2]/div[2]/div[2]/div[2]/ul/ul/li')
            for li in detail:
                title = li.xpath('./a/text()')[0]
                url_ = li.xpath('./a/@href')[0]
                date_Today = li.xpath('./span/text()')[0].replace('\xa0', '').replace('\n', ''). \
                    replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '') \
                    .replace('[', '').replace(']', '').replace('/', '-')
                if 'http' not in url_:
                    url_ = 'http://www.pingli.gov.cn' + url_
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

    # 广州市政府采购
    def guangzhou(self):
        print('广州市政府采购', 'http://gzg2b.gzfinance.gov.cn')
        url_list = [
            'http://gzg2b.gzfinance.gov.cn/gzgpimp/portalsys/portal.do?method=queryHomepageList&t_k=null&current={}&rowCount=10&searchPhrase=&title_name=&porid=zbcggg&kwd='
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
            detail = json.loads(text)['rows']
            for li in detail:
                title = li['title'].replace('\xa0', '').replace('\n', ''). \
                    replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '').replace(
                    "<fontstyle='color:red'>(网)</font>", '')
                url_ = 'http://gzg2b.gzfinance.gov.cn/gzgpimp/portalsys/portal.do?method=pubinfoView&&info_id={}&&porid=zbcggg&t_k=null'.format(
                    li['info_id'])
                date_Today = li['finish_day'].replace('\xa0', '').replace('\n', ''). \
                    replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '') \
                    .replace('[', '').replace(']', '').replace('/', '-')
                if 'http' not in url_:
                    url_ = 'http://gzg2b.gzfinance.gov.cn' + url_
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

    # 广西投资集团电子采购平台
    def guangxi(self):
        print('广西投资集团电子采购平台', 'http://www.gigeps.com')
        url_list = [
            'http://www.gigeps.com/cms/channel/xmgg1hw/index.htm?pageNo={}',
            'http://www.gigeps.com/cms/channel/xmgg1gc/index.htm?pageNo={}',

            'http://www.gigeps.com/cms/channel/xmgg4hw/index.htm?pageNo={}',
            'http://www.gigeps.com/cms/channel/xmgg4gc/index.htm?pageNo={}',

            'http://www.gigeps.com/cms/channel/xmgg3hw/index.htm?pageNo={}',
            'http://www.gigeps.com/cms/channel/xmgg3gc/index.htm?pageNo={}'
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
            detail = html.xpath('//*[@id="list1"]/li')
            for li in detail:
                title = li.xpath('./a/@title')[0]
                url_ = li.xpath('./a/@href')[0]
                date_Today = li.xpath('./a/span[3]/text()')[0].replace('\xa0', '').replace('\n', ''). \
                    replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '') \
                    .replace('[', '').replace(']', '').replace('/', '-')
                if 'http' not in url_:
                    url_ = 'http://www.gigeps.com' + url_
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

    # 广西招标网
    def guangxizhaobiao(self):
        print('广西招标网', 'http://www.guangxibid.com.cn')
        url_list_to = [
            'http://www.guangxibid.com.cn/zbcg/002002/{}.html',
            'http://www.guangxibid.com.cn/zbcg/002001/{}.html',
            'http://www.guangxibid.com.cn/zbcg/002003/{}.html'
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
            if page == 1:
                text = tool.requests_get(url.format('list'), headers)
            else:
                text = tool.requests_get(url.format(page), headers)
            html = HTML(text)
            detail = html.xpath('//*[@id="main"]/div/div[2]/ul/li')
            for li in detail:
                title = li.xpath('./div[1]/a/@title')[0]
                url_ = li.xpath('./div[1]/a/@href')[0]
                date_Today = li.xpath('./div[2]/text()')[0].replace('\xa0', '').replace('\n', ''). \
                    replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '') \
                    .replace('[', '').replace(']', '').replace('/', '-')
                if 'http' not in url_:
                    url_ = 'http://www.guangxibid.com.cn' + url_
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

    # 德清县公共资源交易中心
    def deqing(self):
        print('德清县公共资源交易中心', 'http://ggzy.deqing.gov.cn')
        url_list = [
            'http://ggzy.deqing.gov.cn/cms/jyxxgcjs/{}.htm',
            'http://ggzy.deqing.gov.cn/cms/jyxxcgxm/{}.htm',
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
            detail = html.xpath('/html/body/div[4]/div[2]/div[3]/div/ul/li')
            for li in detail:
                title = li.xpath('./p[1]/a/text()')[0].replace('\xa0', '').replace('\n', ''). \
                    replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '').replace(
                    "<fontstyle='color:red'>(网)</font>", '')
                url_ = li.xpath('./p[1]/a/@href')[0]
                date_Today = li.xpath('./p[2]/text()')[0].replace('\xa0', '').replace('\n', ''). \
                    replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '') \
                    .replace('[', '').replace(']', '').replace('/', '-')
                if 'http' not in url_:
                    url_ = 'http://ggzy.deqing.gov.cn' + url_
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

    # 成都轨道集团电子采购
    def chengdu(self):
        print('成都轨道集团电子采购', 'https://ep.cdmetro.cn:1443')
        url_list = [
            '0000000000000201',
            '0000000000000202'
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
        url_to = 'https://ep.cdmetro.cn:1443/suneps/EiService'
        while True:
            page += 1
            data = {
                'service': 'NE9001',
                'method': 'query',
                'eiinfo': '{attr:{"efFormEname":"NE9001","efFormCname":"概览列表","efFormPopup":"","efFormTime":"","efCurFormEname":"NE9001","efCurButtonEname":"","packageName":"","serviceName":"NE9001","methodName":"initLoad","efFormInfoTag":"","efFormLoadPath":"/NE/NE9001.jsp","efFormButtonDesc":"{\\"msg\\":\\"\\",\\"msgKey\\":\\"\\",\\"detailMsg\\":\\"\\",\\"status\\":0,\\"blocks\\":{}}","code":"' + url + '","query":"  查 询  ","":"跳转","ef_grid_result_jumpto":"2","perPageRecord":"10","limit":10,"offset":10,"currentPage":' + str(
                    page) + '},blocks:{inqu_status:{attr:{},meta:{attr:{},columns:[{name:"title",descName:"",type:"C"},{name:"startRecCreateTime",descName:"",type:"C"},{name:"endRecCreateTime",descName:"",type:"C"}]},rows:[["","",""]]}}}'
            }
            if page == 1:
                text = tool.requests_get(
                    'https://ep.cdmetro.cn:1443/suneps/DispatchAction.do?efFormEname=NE9001&code=' + url,
                    headers)
                text = re.findall('var __ei=(.*?);', text, re.S)[0]
            else:
                text = tool.requests_post(url_to, data, headers)
            detail = json.loads(text)['blocks']['edit']['rows']
            for li in detail:
                title = li[2].replace('\xa0', '').replace('\n', ''). \
                    replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '').replace(
                    "<fontstyle='color:red'>(网)</font>", '')
                url_ = 'https://ep.cdmetro.cn:1443/suneps/DispatchAction.do?efFormEname=NE9003&code=0000000000000201&articleId={}&columnId={}'.format(
                    li[0], li[1])
                date_Today = li[5].replace('\xa0', '').replace('\n', ''). \
                    replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '') \
                    .replace('[', '').replace(']', '').replace('/', '-')
                date_Today = date_Today[:4] + '-' + date_Today[4:6] + '-' + date_Today[6:]
                if 'http' not in url_:
                    url_ = 'https://ep.cdmetro.cn:1443' + url_
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

    # 朝鲜自治州公共资源交易中心
    def chaoxian(self):
        print('朝鲜自治州公共资源交易中心', 'http://ybggzy.com')
        url_list = [
            'http://ybggzy.com/jyxx/005001/005001001/{}.html',
            'http://ybggzy.com/jyxx/005001/005001002/{}.html',
            'http://ybggzy.com/jyxx/005002/005002001/{}.html',
            'http://ybggzy.com/jyxx/005002/005002002/{}.html'
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
                if '005001' in url:
                    text = tool.requests_get(url.format('aboutsub'), headers)
                else:
                    text = tool.requests_get(url.format('aboutsubgc'), headers)
            else:
                text = tool.requests_get(url.format(page), headers)
            html = HTML(text)
            detail = html.xpath('//*[@id="showList"]/li')
            for li in detail:
                title = li.xpath('./div/a/text()')[0].replace('\xa0', '').replace('\n', ''). \
                    replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '').replace(
                    "<fontstyle='color:red'>(网)</font>", '')
                url_ = li.xpath('./div/a/@href')[0]
                date_Today = li.xpath('./span/text()')[0].replace('\xa0', '').replace('\n', ''). \
                    replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '') \
                    .replace('[', '').replace(']', '').replace('/', '-')
                if 'http' not in url_:
                    url_ = 'http://ybggzy.com' + url_
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

    # 柳州市公共资源交易中心
    def liuzhou(self):
        print('柳州市公共资源交易中心', 'http://login.ggzy.liuzhou.gov.cn')
        url_list = [
            'http://login.ggzy.liuzhou.gov.cn/gxlzzbw/ShowInfo/Jyxxsearch.aspx?ywtype=001001&infotype=&Eptr3=&Paging={}',
            'http://login.ggzy.liuzhou.gov.cn/gxlzzbw/ShowInfo/Jyxxsearch.aspx?ywtype=001004&infotype=&Eptr3=&Paging={}',
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
            detail = html.xpath('//*[@id="result"]/div[2]/ul/li')
            for li in detail:
                title = li.xpath('./div/a/@title')[0].replace('\xa0', '').replace('\n', ''). \
                    replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
                url_ = li.xpath('./div/a/@href')[0]
                date_Today = li.xpath('./span/text()')[0].replace('\xa0', '').replace('\n', ''). \
                    replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '') \
                    .replace('[', '').replace(']', '').replace('/', '-')
                if 'http' not in url_:
                    url_ = 'http://login.ggzy.liuzhou.gov.cn' + url_
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

    # 桂林市公共资源交易中心
    def guilin(self):
        print('桂林市公共资源交易中心', 'http://glggzy.org.cn')
        url_list = [
            'http://glggzy.org.cn/gxglzbw/jyxx/001001/001001001/?Paging={}',
            'http://glggzy.org.cn/gxglzbw/jyxx/001001/001001002/?Paging={}',
            'http://glggzy.org.cn/gxglzbw/jyxx/001001/001001004/?Paging={}',
            'http://glggzy.org.cn/gxglzbw/jyxx/001001/001001006/?Paging={}',#中标公告
            'http://glggzy.org.cn/gxglzbw/jyxx/001001/001001007/?Paging={}',#候选人
            'http://glggzy.org.cn/gxglzbw/jyxx/001001/001001008/?Paging={}',#结果

            'http://glggzy.org.cn/gxglzbw/jyxx/001004/001004001/?Paging={}',
            'http://glggzy.org.cn/gxglzbw/jyxx/001004/001004002/?Paging={}',#中标公告
            'http://glggzy.org.cn/gxglzbw/jyxx/001004/001004005/?Paging={}',#结果
            'http://glggzy.org.cn/gxglzbw/jyxx/001004/001004006/?Paging={}'
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
                title = li.xpath('./div/a/@title')[0].replace('\xa0', '').replace('\n', ''). \
                    replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
                url_ = li.xpath('./div/a/@href')[0]
                date_Today = li.xpath('./span/text()')[0].replace('\xa0', '').replace('\n', ''). \
                    replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '') \
                    .replace('[', '').replace(']', '').replace('/', '-')
                if 'http' not in url_:
                    url_ = 'http://glggzy.org.cn' + url_
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

    # 梧州市公共资源交易中心
    def wuzhou(self):
        print('梧州市公共资源交易中心', 'http://www.wzggzy.cn')
        url_list = [
            'http://www.wzggzy.cn/gxwzzbw/jyxx/001001/001001001/MoreInfo.aspx?CategoryNum=001001001',
            'http://www.wzggzy.cn/gxwzzbw/jyxx/001001/001001002/MoreInfo.aspx?CategoryNum=001001002',
            'http://www.wzggzy.cn/gxwzzbw/jyxx/001001/001001004/MoreInfo.aspx?CategoryNum=001001004', #上限价
            'http://www.wzggzy.cn/gxwzzbw/jyxx/001001/001001005/MoreInfo.aspx?CategoryNum=001001005',
            'http://www.wzggzy.cn/gxwzzbw/jyxx/001001/001001006/MoreInfo.aspx?CategoryNum=001001006',#结果

            'http://www.wzggzy.cn/gxwzzbw/jyxx/001004/001004001/MoreInfo.aspx?CategoryNum=001004001',
            'http://www.wzggzy.cn/gxwzzbw/jyxx/001004/001004002/MoreInfo.aspx?CategoryNum=001004002',
            'http://www.wzggzy.cn/gxwzzbw/jyxx/001004/001004004/MoreInfo.aspx?CategoryNum=001004004',#结果
            'http://www.wzggzy.cn/gxwzzbw/jyxx/001004/001004005/MoreInfo.aspx?CategoryNum=001004005',
            'http://www.wzggzy.cn/gxwzzbw/jyxx/001004/001004006/MoreInfo.aspx?CategoryNum=001004006'
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
            '__VIEWSTATE': str(page),
            '__VIEWSTATEGENERATOR': 'F6C8A21A',
            '__EVENTTARGET': 'MoreInfoList1$Pager',
            '__EVENTARGUMENT': page,
            '__VIEWSTATEENCRYPTED': ''
        }
        while True:
            page += 1
            if page == 1:
                text = tool.requests_get(url, headers)
            else:
                text = tool.requests_post(url, data, headers)
            html = HTML(text)
            data['__VIEWSTATE'] = html.xpath('//*[@id="__VIEWSTATE"]/@value')[0]
            data['__EVENTARGUMENT'] = str(page)
            detail = html.xpath('//*[@id="MoreInfoList1_DataGrid1"]/tr')
            for li in detail:
                title = li.xpath('./td[2]/a/@title')[0].replace('\xa0', '').replace('\n', ''). \
                    replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
                url_ = li.xpath('./td[2]/a/@href')[0]
                date_Today = li.xpath('./td[3]/text()')[0].replace('\xa0', '').replace('\n', ''). \
                    replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '') \
                    .replace('[', '').replace(']', '').replace('/', '-')
                if 'http' not in url_:
                    url_ = 'http://www.wzggzy.cn' + url_
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

    # 榆林市榆阳区人民政府
    def yuyang(self):
        print('榆林市榆阳区人民政府', 'http://www.yuyang.gov.cn')
        url_list = [
            'http://www.yuyang.gov.cn/zwgk/fdzdgkml/ggzypz/zfcg/{}.html'
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
            detail = html.xpath('//*[@class="m-lst48"]/ul/li')
            for li in detail:
                title = li.xpath('./a/text()')[0].replace('\xa0', '').replace('\n', ''). \
                    replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '').replace(
                    "<fontstyle='color:red'>(网)</font>", '')
                url_ = li.xpath('./a/@href')[0]
                date_Today = li.xpath('./span/text()')[0].replace('\xa0', '').replace('\n', ''). \
                    replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '') \
                    .replace('[', '').replace(']', '').replace('/', '-').replace('年', '').replace('月', '').replace(
                    '日', '')
                if 'http' not in url_:
                    url_ = 'http://www.yuyang.gov.cn' + url_
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

    # 武威市公共资源交易中心
    def wuwei(self):
        print('武威市公共资源交易中心', 'http://gzjy.gswuwei.gov.cn')
        url_list = [
            'http://gzjy.gswuwei.gov.cn/f/newtrade/annogoods/getAnnoList?pageNo={}&pageSize=20&tradeStatus=0&prjpropertycode=A01,A02,A99,A04,A03,A07,D01,D02,D03,C01,C02,C03,B,B02,B03,B04,A99,B01,801,802&projectname=&tabType=1',
            'http://gzjy.gswuwei.gov.cn/f/newtrade/annogoods/getAnnoList?pageNo={}&pageSize=20&tradeStatus=0&prjpropertycode=A01,A02,A99,A04,A03,A07,D01,D02,D03,C01,C02,C03,B,B02,B03,B04,A99,B01,801,802&projectname=&tabType=2'
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
            detail = html.xpath('//*[@class="byTradingDetail-Con byTradingDetail-ConActive"]/dl')
            for li in detail:
                title = li.xpath('./dd/a/text()')[1].replace('\xa0', '').replace('\n', ''). \
                    replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '').replace("]", '')
                url_ = li.xpath('./dd/a/@href')[0]
                try:
                    date_Today = li.xpath('./dd/span[2]/text()')[0].replace('\xa0', '').replace('\n', ''). \
                        replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '') \
                        .replace('[', '').replace(']', '').replace('/', '-')
                except:
                    date_Today = li.xpath('./dd/span/text()')[0].replace('\xa0', '').replace('\n', ''). \
                        replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '') \
                        .replace('[', '').replace(']', '').replace('/', '-')
                if 'http' not in url_:
                    url_ = 'http://gzjy.gswuwei.gov.cn' + url_
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

    # 池州市公共资源交易中心
    def chizhou(self):
        print('池州市公共资源交易中心', 'http://ggj.chizhou.gov.cn')
        url_list = [
            'http://ggj.chizhou.gov.cn/front/bidcontent/9005001002',
            'http://ggj.chizhou.gov.cn/front/bidcontent/9005001005',
            'http://ggj.chizhou.gov.cn/front/bidcontent/9005001003',
            'http://ggj.chizhou.gov.cn/front/bidcontent/9005001004',
            'http://ggj.chizhou.gov.cn/front/bidcontent/9005001007',
            'http://ggj.chizhou.gov.cn/front/bidcontent/9005002002',
            'http://ggj.chizhou.gov.cn/front/bidcontent/9005002004',
            'http://ggj.chizhou.gov.cn/front/bidcontent/9005002003',
            'http://ggj.chizhou.gov.cn/front/bidcontent/9005002006',
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
        while True:
            page += 1
            data = {"filter": {"date": "", "regionCode": "", "tenderProjectType": "", "tenderMode": ""}, "page": page,
                    "rows": 15, "searchKey": ""}
            text = tool.requests_post_to(url, data, headers)
            detail = json.loads(text)['rows']
            for li in detail:
                title = li['title'].replace('\xa0', '').replace('\n', ''). \
                    replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
                url_ = 'http://ggj.chizhou.gov.cn/front/bidcontent/detailByTenderProjectCode?categoryCode={}&tenderProjectCode={}'.format(url.split('/')[-1], base64.b64encode(li['tenderProjectCode'].encode('utf-8')).decode('ascii')[:-2])
                date_Today = li['publishTime'][:10].replace('\xa0', '').replace('\n', ''). \
                    replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '') \
                    .replace('[', '').replace(']', '').replace('/', '-')
                if 'http' not in url_:
                    url_ = 'http://ggj.chizhou.gov.cn' + url_
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

    # 河池市公共资源交易中心
    def hechi(self):
        print('河池市公共资源交易中心', 'http://218.65.221.79')
        url_list = [
            'http://218.65.221.79/gxhczbw/jyxx/001001/001001001/MoreInfo.aspx?CategoryNum=001001001',
            'http://218.65.221.79/gxhczbw/jyxx/001001/001001002/MoreInfo.aspx?CategoryNum=001001002',
            'http://218.65.221.79/gxhczbw/jyxx/001001/001001005/MoreInfo.aspx?CategoryNum=001001005',
            'http://218.65.221.79/gxhczbw/jyxx/001004/001004001/MoreInfo.aspx?CategoryNum=001004001',
            'http://218.65.221.79/gxhczbw/jyxx/001004/001004002/MoreInfo.aspx?CategoryNum=001004002',
            'http://218.65.221.79/gxhczbw/jyxx/001004/001004004/MoreInfo.aspx?CategoryNum=001004004'
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
            '__VIEWSTATE': str(page),
            '__VIEWSTATEGENERATOR': 'A5A96421',
            '__EVENTTARGET': 'MoreInfoList1$Pager',
            '__EVENTARGUMENT': page,
            '__VIEWSTATEENCRYPTED': ''
        }
        while True:
            page += 1
            if page == 1:
                text = tool.requests_get(url, headers)
            else:
                text = tool.requests_post(url, data, headers)
            html = HTML(text)
            data['__VIEWSTATE'] = html.xpath('//*[@id="__VIEWSTATE"]/@value')[0]
            data['__EVENTARGUMENT'] = str(page)
            detail = html.xpath('//*[@id="MoreInfoList1_DataGrid1"]/tr')
            for li in detail:
                title = li.xpath('./td[2]/a/@title')[0].replace('\xa0', '').replace('\n', ''). \
                    replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
                url_ = li.xpath('./td[2]/a/@href')[0]
                date_Today = li.xpath('./td[3]/text()')[0].replace('\xa0', '').replace('\n', ''). \
                    replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '') \
                    .replace('[', '').replace(']', '').replace('/', '-')
                if 'http' not in url_:
                    url_ = 'http://218.65.221.79' + url_
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

    # 泉州市公共资源交易网
    def quanzhou(self):
        print('泉州市公共资源交易网', 'http://ggzyjy.quanzhou.gov.cn')
        url_list = [
            'http://ggzyjy.quanzhou.gov.cn/project/getProjPage_project.do',
            'http://ggzyjy.quanzhou.gov.cn/project/getwinBulletinPage_project.do'#结果
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
        while True:
            page += 1
            if 'getProjPage_project' in url:
                data = {"pageIndex": page, "pageSize": 10, "classId": 0, "centerId": 0, "projNo": "", "projName": "",
                        "ownerDeptName": ""}
            else:
                data = {"pageIndex": page, "pageSize": 10, "keyword": "", "centerId": 0}
            text = tool.requests_post_to(url, data, headers)
            detail = json.loads(text)['data']['dataList']
            for li in detail:
                if 'getProjPage_project' in url:
                    title = li['projName']
                    url_ = 'http://ggzyjy.quanzhou.gov.cn/project/projectInfo.do?projId={}'.format(li['projId'])
                    date_Today = li['auditDate'].replace('\xa0', '').replace('\n', ''). \
                        replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
                else:
                    title = li['bltTitle']
                    url_ = li['linkStr']
                    date_Today = li['pubDate'].replace('\xa0', '').replace('\n', ''). \
                        replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
                if 'http' not in url_:
                    url_ = 'http://ggzyjy.quanzhou.gov.cn' + url_
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

    # 淄博市公共资源交易中心
    def zibo(self):
        print('淄博市公共资源交易中心', 'http://ggzyjy.zibo.gov.cn')
        url_list = [
            'http://ggzyjy.zibo.gov.cn/TPFront/jyxx/002001/002001001/002001001001/MoreInfo.aspx?CategoryNum=268698113',
            'http://ggzyjy.zibo.gov.cn/TPFront/jyxx/002001/002001001/002001001002/MoreInfo.aspx?CategoryNum=268698114',
            'http://ggzyjy.zibo.gov.cn/TPFront/jyxx/002001/002001001/002001001013/MoreInfo.aspx?CategoryNum=268698123',
            'http://ggzyjy.zibo.gov.cn/TPFront/jyxx/002001/002001001/002001001009/MoreInfo.aspx?CategoryNum=2001001009',
            'http://ggzyjy.zibo.gov.cn/TPFront/jyxx/002001/002001001/002001001010/MoreInfo.aspx?CategoryNum=268698120',
            'http://ggzyjy.zibo.gov.cn/TPFront/jyxx/002001/002001001/002001001007/MoreInfo.aspx?CategoryNum=268698119',
            'http://ggzyjy.zibo.gov.cn/TPFront/jyxx/002001/002001001/002001001008/MoreInfo.aspx?CategoryNum=2001001008',

            'http://ggzyjy.zibo.gov.cn/TPFront/jyxx/002001/002001002/002001002001/MoreInfo.aspx?CategoryNum=268698625',
            'http://ggzyjy.zibo.gov.cn/TPFront/jyxx/002001/002001002/002001002002/MoreInfo.aspx?CategoryNum=268698626',
            'http://ggzyjy.zibo.gov.cn/TPFront/jyxx/002001/002001002/002001002009/MoreInfo.aspx?CategoryNum=2001002009',
            'http://ggzyjy.zibo.gov.cn/TPFront/jyxx/002001/002001002/002001002010/MoreInfo.aspx?CategoryNum=268698632',
            'http://ggzyjy.zibo.gov.cn/TPFront/jyxx/002001/002001002/002001002007/MoreInfo.aspx?CategoryNum=268698631',

            'http://ggzyjy.zibo.gov.cn/TPFront/jyxx/002002/002002001/002002001001/MoreInfo.aspx?CategoryNum=268960257',
            'http://ggzyjy.zibo.gov.cn/TPFront/jyxx/002002/002002001/002002001002/MoreInfo.aspx?CategoryNum=268960258',
            'http://ggzyjy.zibo.gov.cn/TPFront/jyxx/002002/002002001/002002001011/MoreInfo.aspx?CategoryNum=268960265',
            'http://ggzyjy.zibo.gov.cn/TPFront/jyxx/002002/002002001/002002001007/MoreInfo.aspx?CategoryNum=268960263',
            'http://ggzyjy.zibo.gov.cn/TPFront/jyxx/002002/002002001/002002001012/MoreInfo.aspx?CategoryNum=268960266',
            'http://ggzyjy.zibo.gov.cn/TPFront/jyxx/002002/002002001/002002001009/MoreInfo.aspx?CategoryNum=2002001009',

            'http://ggzyjy.zibo.gov.cn/TPFront/jyxx/002002/002002002/002002002001/MoreInfo.aspx?CategoryNum=268960769',
            'http://ggzyjy.zibo.gov.cn/TPFront/jyxx/002002/002002002/002002002002/MoreInfo.aspx?CategoryNum=268960770',
            'http://ggzyjy.zibo.gov.cn/TPFront/jyxx/002002/002002002/002002002011/MoreInfo.aspx?CategoryNum=268960777',

            'http://ggzyjy.zibo.gov.cn/TPFront/jyxx/002002/002002005/002002005001/MoreInfo.aspx?CategoryNum=268962305'
        ]
        headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Cookie': 'JSESSIONID=662863FD2199FBD1672A04A290868047; _CSRFCOOKIE=73F3D7A1BCDCA9001D7B1483A214C4E98DE2528B; EPTOKEN=73F3D7A1BCDCA9001D7B1483A214C4E98DE2528B; oauthClientId=demoClient; oauthPath=http://172.16.5.21:8080/EpointWebBuilder; oauthLoginUrl=http://172.16.5.21:8080/EpointWebBuilder/rest/oauth2/authorize?client_id=demoClient&state=a&response_type=code&scope=user&redirect_uri=; oauthLogoutUrl=http://172.16.5.21:8080/EpointWebBuilder/rest/oauth2/logout?redirect_uri=; noOauthRefreshToken=986d4fe7e5dd29b64c9e7b7a6d66e089; noOauthAccessToken=77c09e0bf98b6220b544961097eed84a; sub_domain_cokie=TiG5CMD9KQ41mmsARPTuAg%3D%3D; region_name=%E4%B9%8C%E9%B2%81%E6%9C%A8%E9%BD%90%E5%B8%82',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',

        }
        url = url_list.pop(0)
        page = 0
        data = {
            # '__CSRFTOKEN': '',
            '__VIEWSTATE': '',
            '__VIEWSTATEGENERATOR': '86E82E3C',
            '__EVENTTARGET': 'MoreInfoList1$Pager',
            '__EVENTARGUMENT': page,
            '__VIEWSTATEENCRYPTED': '',
            'MoreInfoList1$Pager_input': '1'
        }
        ls = []
        while True:
            page += 1
            if page == 1:
                text = tool.requests_get(url, headers)
            else:
                text = tool.requests_post(url, data, headers)
            html = HTML(text)
            data['__VIEWSTATE'] = html.xpath('//*[@id="__VIEWSTATE"]/@value')[0]
            # data['__CSRFTOKEN'] = html.xpath('//*[@id="__CSRFTOKEN"]/@value')[0]
            data['__EVENTARGUMENT'] = str(page)
            detail = html.xpath('//*[@id="MoreInfoList1_DataGrid1"]/tr')
            for li in detail:
                title = li.xpath('./td[2]/a/@title')[0].replace('\xa0', '').replace('\n', ''). \
                    replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '').replace(
                    "<fontstyle='color:red'>(网)</font>", '')
                url_ = li.xpath('./td[2]/a/@href')[0]
                date_Today = li.xpath('./td[3]/text()')[0].replace('\xa0', '').replace('\n', ''). \
                    replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '') \
                    .replace('[', '').replace(']', '').replace('/', '-')
                if 'http' not in url_:
                    url_ = 'http://ggzyjy.zibo.gov.cn' + url_
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

    # 淮北市公共资源交易中心
    def huanbei(self):
        print('淮北市公共资源交易中心', 'http://ggzy.huaibei.gov.cn')
        url_list = [
            '002001',
            '002002'
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
        url_to = 'http://ggzy.huaibei.gov.cn/EpointWebBuilder/rest/GgSearchAction/getInfoMationList'
        while True:
            data = {
                'params': '{"siteGuid":"7eb5f7f1-9041-43ad-8e13-8fcb82ea831a","categoryNum":"' + url + '","keyword":"","startDate":"","endDate":"","publishDate":"","area":"","tradeType":"","pageIndex":' + str(
                    page) + ',"pageSize":12}'}
            page += 1
            text = tool.requests_post(url_to, data, headers)
            detail = json.loads(text)['Table']
            for li in detail:
                title = li['title'].replace('\xa0', '').replace('\n', ''). \
                    replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '').replace(
                    "<fontstyle='color:red'>(网)</font>", '')
                url_ = li['infourl']
                date_Today = li['infodate'].replace('\xa0', '').replace('\n', ''). \
                    replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '') \
                    .replace('[', '').replace(']', '').replace('/', '-')
                if 'http' not in url_:
                    url_ = 'http://ggzy.huaibei.gov.cn' + url_
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

    # 焦作市公共资源交易中心
    def jiaozuo(self):
        print('焦作市公共资源交易中心', 'http://www.jzggzy.cn')
        url_list = [
            'http://www.jzggzy.cn/TPFront/ztbzx/069002/069002001/069002001001/MoreInfo.aspx?CategoryNum=69002001001',
            'http://www.jzggzy.cn/TPFront/ztbzx/069002/069002001/069002001002/MoreInfo.aspx?CategoryNum=69002001002',
            'http://www.jzggzy.cn/TPFront/ztbzx/069002/069002002/069002002001/MoreInfo.aspx?CategoryNum=69002002001',
            'http://www.jzggzy.cn/TPFront/ztbzx/069002/069002002/069002002002/MoreInfo.aspx?CategoryNum=69002002002'
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
            '__VIEWSTATEGENERATOR': '41F3473A',
            '__EVENTTARGET': 'MoreInfoList1$Pager',
            '__EVENTARGUMENT': page,
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
            data['__VIEWSTATE'] = html.xpath('//*[@id="__VIEWSTATE"]/@value')[0]
            data['__EVENTARGUMENT'] = str(page)
            detail = html.xpath('//*[@id="MoreInfoList1_DataGrid1"]/tr')
            for li in detail:
                title = li.xpath('./td[2]/a/@title')[0].replace('\xa0', '').replace('\n', ''). \
                    replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
                url_ = li.xpath('./td[2]/a/@href')[0]
                date_Today = li.xpath('./td[3]/text()')[0].replace('\xa0', '').replace('\n', ''). \
                    replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '') \
                    .replace('[', '').replace(']', '').replace('/', '-')
                if 'http' not in url_:
                    url_ = 'http://www.jzggzy.cn' + url_
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

    # 玉林市公共资源交易中心
    def yulin(self):
        print('玉林市公共资源交易中心', 'http://202.103.240.162')
        url_list = [
            'http://202.103.240.162/EWB-FRONT/rest/frontAppCustomAction/getPageInfoListNew'
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
            data = {
                'params': '{"siteGuid":"ed8a7a3d-b04b-40dd-a1ff-06d78da1d1b4","categoryNum":"001","kw":"","pageIndex":' + str(
                    page) + ',"pageSize":15}'}
            page += 1
            text = tool.requests_post(url, data, headers)
            detail = json.loads(text)['custom']['infodata']
            for li in detail:
                title = li['title']
                url_ = li['infourl']
                date_Today = li['infodate']
                if 'http' not in url_:
                    url_ = 'http://202.103.240.162' + url_
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

    # 百色市公共资源交易中心
    def baise(self):
        print('百色市公共资源交易中心', 'http://www.bsggzy.org.cn')
        url_list = [
            'http://www.bsggzy.org.cn/gxbszbw/jyxx/001001/001001001/MoreInfo.aspx?CategoryNum=001001001',
            'http://www.bsggzy.org.cn/gxbszbw/jyxx/001001/001001002/MoreInfo.aspx?CategoryNum=001001002',
            'http://www.bsggzy.org.cn/gxbszbw/jyxx/001001/001001005/MoreInfo.aspx?CategoryNum=001001005',
            'http://www.bsggzy.org.cn/gxbszbw/jyxx/001004/001004001/MoreInfo.aspx?CategoryNum=001004001',
            'http://www.bsggzy.org.cn/gxbszbw/jyxx/001004/001004002/MoreInfo.aspx?CategoryNum=001004002',
            'http://www.bsggzy.org.cn/gxbszbw/jyxx/001004/001004004/MoreInfo.aspx?CategoryNum=001004004'
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
            '__CSRFTOKEN': '',
            '__VIEWSTATE': '',
            '__VIEWSTATEGENERATOR': 'CE49891B',
            '__EVENTTARGET': 'MoreInfoList1$Pager',
            '__EVENTARGUMENT': page,
            '__VIEWSTATEENCRYPTED': ''
        }
        while True:
            page += 1
            if page == 1:
                text = tool.requests_get(url, headers)
            else:
                text = tool.requests_post(url, data, headers)
            html = HTML(text)
            data['__VIEWSTATE'] = html.xpath('//*[@id="__VIEWSTATE"]/@value')[0]
            data['__CSRFTOKEN'] = html.xpath('//*[@id="__CSRFTOKEN"]/@value')[0]
            data['__EVENTARGUMENT'] = str(page)
            detail = html.xpath('//*[@id="MoreInfoList1_DataGrid1"]/tr')
            for li in detail:
                title = li.xpath('./td[2]/a/@title')[0].replace('\xa0', '').replace('\n', ''). \
                    replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '').replace(
                    "<fontstyle='color:red'>(网)</font>", '')
                url_ = li.xpath('./td[2]/a/@href')[0]
                date_Today = li.xpath('./td[3]/text()')[0].replace('\xa0', '').replace('\n', ''). \
                    replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '') \
                    .replace('[', '').replace(']', '').replace('/', '-')
                if 'http' not in url_:
                    url_ = 'http://www.bsggzy.org.cn' + url_
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

    # 苏州市公共资源交易中心
    def suzhou(self):
        print('苏州市公共资源交易中心', 'http://www.szzyjy.com.cn')
        url_list = [
            'http://www.szzyjy.com.cn/jyxx/003001/003001001/{}.html',
            'http://www.szzyjy.com.cn/jyxx/003001/003001003/{}.html',
            'http://www.szzyjy.com.cn/jyxx/003001/003001007/{}.html',
            'http://www.szzyjy.com.cn/jyxx/003001/003001006/{}.html',
            'http://www.szzyjy.com.cn/jyxx/003003/003003001/{}.html',
            'http://www.szzyjy.com.cn/jyxx/003003/003003003/{}.html',
            'http://www.szzyjy.com.cn/jyxx/003003/003003013/{}.html'
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
                text = tool.requests_get(url.format('tradeInfo'), headers)
            else:
                text = tool.requests_get(url.format(page), headers)
            html = HTML(text)
            detail = html.xpath('//*[@id="jt"]/table/tbody/tr')
            for li in detail:
                title = li.xpath('./td[3]/a/@title')[0]
                url_ = li.xpath('./td[3]/a/@href')[0]
                date_Today = li.xpath('./td[5]/text()')[0].replace('\xa0', '').replace('\n', ''). \
                    replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '') \
                    .replace('[', '').replace(']', '').replace('/', '-')
                if 'http' not in url_:
                    url_ = 'http://www.szzyjy.com.cn' + url_
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

    # 苏州市政府采购
    def suzhouzf(self):
        print('苏州市政府采购', 'http://czju.suzhou.gov.cn')
        url_list = [
            'http://czju.suzhou.gov.cn/zfcg/content/cpContents.action'
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
            'type': '',
            'title': '',
            'choose': '',
            'projectType': '',
            'zbCode': '',
            'appcode': '',
            'page': '1',
            'rows': '30',
        }
        while True:
            page += 1
            data['page'] = str(page)
            text = tool.requests_post(url, data, headers)
            detail = json.loads(text)['rows']
            for li in detail:
                title = li['TITLE']
                url_ = 'http://czju.suzhou.gov.cn/zfcg/html/project/{}.shtml'.format(li['ID'])
                date_Today = li['RELEASETIME'][:10].replace('\xa0', '').replace('\n', ''). \
                    replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '') \
                    .replace('[', '').replace(']', '').replace('/', '-')
                if 'http' not in url_:
                    url_ = 'http://czju.suzhou.gov.cn' + url_
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

    # 萧山区公共资源交易中心
    # def xiaoshan(self):
    #     print('萧山区公共资源交易中心', 'http://www.xszbjyw.com')
    #     url_list = [
    #         'http://www.xszbjyw.com/Bulletin/BulletinList.aspx?ProType=11&AfficheType=584&ViewID=24',
    #         'http://www.xszbjyw.com/Bulletin/BulletinList.aspx?ProType=11&AfficheType=992&ViewID=26',
    #         'http://www.xszbjyw.com/Bulletin/BulletinList.aspx?ProType=11&AfficheType=591&ViewID=27',
    #         'http://www.xszbjyw.com/Bulletin/BulletinList.aspx?ProType=11&AfficheType=593&ViewID=29',
    #         'http://www.xszbjyw.com/Bulletin/BulletinList.aspx?ProType=12&AfficheType=601&ViewID=36',
    #         'http://www.xszbjyw.com/Bulletin/BulletinList.aspx?ProType=12&AfficheType=602&ViewID=38',
    #         'http://www.xszbjyw.com/Bulletin/BulletinList.aspx?ProType=12&AfficheType=603&ViewID=40'
    #     ]
    #     headers = {
    #         'Accept': 'application/json, text/javascript, */*; q=0.01',
    #         'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    #         'Cookie': 'JSESSIONID=662863FD2199FBD1672A04A290868047; _CSRFCOOKIE=73F3D7A1BCDCA9001D7B1483A214C4E98DE2528B; EPTOKEN=73F3D7A1BCDCA9001D7B1483A214C4E98DE2528B; oauthClientId=demoClient; oauthPath=http://172.16.5.21:8080/EpointWebBuilder; oauthLoginUrl=http://172.16.5.21:8080/EpointWebBuilder/rest/oauth2/authorize?client_id=demoClient&state=a&response_type=code&scope=user&redirect_uri=; oauthLogoutUrl=http://172.16.5.21:8080/EpointWebBuilder/rest/oauth2/logout?redirect_uri=; noOauthRefreshToken=986d4fe7e5dd29b64c9e7b7a6d66e089; noOauthAccessToken=77c09e0bf98b6220b544961097eed84a; sub_domain_cokie=TiG5CMD9KQ41mmsARPTuAg%3D%3D; region_name=%E4%B9%8C%E9%B2%81%E6%9C%A8%E9%BD%90%E5%B8%82',
    #         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
    #
    #     }
    #     url = url_list.pop(0)
    #     page = 0
    #     ls = []
    #     data = {
    #         # '__CSRFTOKEN': '',
    #         '__VIEWSTATE': '',
    #         '__EVENTVALIDATION': '',
    #         'txtProjectNo': '',
    #         'txtProjectName': '',
    #         'ddlState': '0',
    #         'grdBulletin$ctl18$BtnNext': '下页',
    #         'grdBulletin$ctl18$NumGoto': '1'
    #     }
    #     while True:
    #         page += 1
    #         if page == 1:
    #             text = tool.requests_get(url, headers)
    #         else:
    #             text = tool.requests_get(url, headers)
    #         html = HTML(text)
    #         data['__VIEWSTATE'] = html.xpath('//*[@id="__VIEWSTATE"]/@value')[0]
    #         data['__EVENTVALIDATION'] = html.xpath('//*[@id="__EVENTVALIDATION"]/@value')[0]
    #         data['grdBulletin$ctl18$NumGoto'] = str(page)
    #         detail = html.xpath('//*[@id="grdBulletin"]/tr')
    #         for li in detail:
    #             title = li.xpath('./td[3]/div/a/@title')[0].replace('\xa0', '').replace('\n', ''). \
    #                 replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '').replace(
    #                 "<fontstyle='color:red'>(网)</font>", '')
    #             url_ = li.xpath('./td[3]/div/a/@href')[0]
    #             date_Today = li.xpath('./td[5]/text()')[0].replace('\xa0', '').replace('\n', ''). \
    #                 replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '') \
    #                 .replace('[', '').replace(']', '').replace('/', '-')
    #             if 'http' not in url_:
    #                 url_ = 'http://www.xszbjyw.com/Bulletin/' + url_
    #             if tool.Transformation(date_Today) > tool.Transformation(self.date):
    #                 continue
    #             elif tool.Transformation(date_Today) == tool.Transformation(self.date):
    #                 ls.append(url_)
    #             else:
    #                 if len(url_list) == 0:
    #                     return [len(ls), ls]
    #                 else:
    #                     url = url_list.pop(0)
    #                     page = 0
    #                     break



    # 蚌埠市公共资源交易中心
    def bengbu(self):
        print('蚌埠市公共资源交易中心', 'http://ggzy.bengbu.gov.cn')
        url_list = [
            'http://ggzy.bengbu.gov.cn/bbfwweb/jyxx/003001/003001001/MoreInfo.aspx?CategoryNum=003001001',
            'http://ggzy.bengbu.gov.cn/bbfwweb/jyxx/003001/003001004/MoreInfo.aspx?CategoryNum=003001004',
            'http://ggzy.bengbu.gov.cn/bbfwweb/jyxx/003001/003001005/MoreInfo.aspx?CategoryNum=003001005',
            'http://ggzy.bengbu.gov.cn/bbfwweb/jyxx/003001/003001006/MoreInfo.aspx?CategoryNum=003001006',
            'http://ggzy.bengbu.gov.cn/bbfwweb/jyxx/003002/003002001/MoreInfo.aspx?CategoryNum=003002001',
            'http://ggzy.bengbu.gov.cn/bbfwweb/jyxx/003002/003002004/MoreInfo.aspx?CategoryNum=003002004',
            'http://ggzy.bengbu.gov.cn/bbfwweb/jyxx/003002/003002005/MoreInfo.aspx?CategoryNum=003002005',
            'http://ggzy.bengbu.gov.cn/bbfwweb/jyxx/003002/003002006/MoreInfo.aspx?CategoryNum=003002006',

            'http://ggzy.bengbu.gov.cn/bbfwweb/dyxx/026001/026001001/026001001001/MoreInfo.aspx?CategoryNum=026001001001',
            'http://ggzy.bengbu.gov.cn/bbfwweb/dyxx/026001/026001001/026001001002/MoreInfo.aspx?CategoryNum=026001001002',
            'http://ggzy.bengbu.gov.cn/bbfwweb/dyxx/026001/026001001/026001001003/MoreInfo.aspx?CategoryNum=026001001003',
            'http://ggzy.bengbu.gov.cn/bbfwweb/dyxx/026001/026001001/026001001004/MoreInfo.aspx?CategoryNum=026001001004',
            'http://ggzy.bengbu.gov.cn/bbfwweb/dyxx/026002/026002001/026002001001/MoreInfo.aspx?CategoryNum=026002001001',
            'http://ggzy.bengbu.gov.cn/bbfwweb/dyxx/026002/026002001/026002001002/MoreInfo.aspx?CategoryNum=026002001002',
            'http://ggzy.bengbu.gov.cn/bbfwweb/dyxx/026002/026002001/026002001003/MoreInfo.aspx?CategoryNum=026002001003',
            'http://ggzy.bengbu.gov.cn/bbfwweb/dyxx/026002/026002001/026002001004/MoreInfo.aspx?CategoryNum=026002001004',

            'http://ggzy.bengbu.gov.cn/bbfwweb/zbgs/004001/004001001/MoreInfo.aspx?CategoryNum=004001001',
            'http://ggzy.bengbu.gov.cn/bbfwweb/zbgs/004001/004001002/MoreInfo.aspx?CategoryNum=004001002',
            'http://ggzy.bengbu.gov.cn/bbfwweb/zbgs/004001/004001003/MoreInfo.aspx?CategoryNum=004001003',
            'http://ggzy.bengbu.gov.cn/bbfwweb/zbgs/004001/004001004/MoreInfo.aspx?CategoryNum=004001004', #中标候选人

            'http://ggzy.bengbu.gov.cn/bbfwweb/zbgs/004002/004002001/MoreInfo.aspx?CategoryNum=004002001',
            'http://ggzy.bengbu.gov.cn/bbfwweb/zbgs/004002/004002002/MoreInfo.aspx?CategoryNum=004002002',
            'http://ggzy.bengbu.gov.cn/bbfwweb/zbgs/004002/004002003/MoreInfo.aspx?CategoryNum=004002003',
            'http://ggzy.bengbu.gov.cn/bbfwweb/zbgs/004002/004002004/MoreInfo.aspx?CategoryNum=004002004',  #采购  中标结果

            'http://ggzy.bengbu.gov.cn/bbfwweb/jggs/044004/MoreInfo.aspx?CategoryNum=044004',
            'http://ggzy.bengbu.gov.cn/bbfwweb/jggs/044001/MoreInfo.aspx?CategoryNum=044001',
            'http://ggzy.bengbu.gov.cn/bbfwweb/jggs/044002/MoreInfo.aspx?CategoryNum=044002',
            'http://ggzy.bengbu.gov.cn/bbfwweb/jggs/044003/MoreInfo.aspx?CategoryNum=044003'
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
            # '__CSRFTOKEN': '',
            '__VIEWSTATE': '',
            '__VIEWSTATEGENERATOR': '7378C9FF',
            '__EVENTTARGET': 'MoreInfoList1$Pager',
            '__EVENTARGUMENT': page,
            '__VIEWSTATEENCRYPTED': ''
        }
        while True:
            page += 1
            if page == 1:
                text = tool.requests_get(url, headers)
            else:
                text = tool.requests_post(url, data, headers)
            html = HTML(text)
            data['__VIEWSTATE'] = html.xpath('//*[@id="__VIEWSTATE"]/@value')[0]
            # data['__CSRFTOKEN'] = html.xpath('//*[@id="__CSRFTOKEN"]/@value')[0]
            data['__EVENTARGUMENT'] = str(page)
            detail = html.xpath('//*[@id="MoreInfoList1_DataGrid1"]/tr')
            for li in detail:
                title = li.xpath('./td[2]/a/text()')[0].replace('\xa0', '').replace('\n', ''). \
                    replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '').replace(
                    "<fontstyle='color:red'>(网)</font>", '')
                url_ = li.xpath('./td[2]/a/@href')[0]
                date_Today = li.xpath('./td[3]/text()')[0].replace('\xa0', '').replace('\n', ''). \
                    replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '') \
                    .replace('[', '').replace(']', '').replace('/', '-')
                if 'http' not in url_:
                    url_ = 'http://ggzy.bengbu.gov.cn' + url_
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

    # 贵港市公共资源交易中心
    def guigang(self):
        print('贵港市公共资源交易中心', 'http://ggggjy.gxgg.gov.cn:9005')
        url_list = [
            'http://ggggjy.gxgg.gov.cn:9005/zbxx/002001/002001001/002001001001/{}.html',
            'http://ggggjy.gxgg.gov.cn:9005/zbxx/002001/002001001/002001001002/{}.html',
            'http://ggggjy.gxgg.gov.cn:9005/zbxx/002001/002001001/002001001004/{}.html',
            'http://ggggjy.gxgg.gov.cn:9005/zbxx/002001/002001002/002001002001/{}.html',
            'http://ggggjy.gxgg.gov.cn:9005/zbxx/002001/002001002/002001002002/{}.html',
            'http://ggggjy.gxgg.gov.cn:9005/zbxx/002001/002001002/002001002004/{}.html',
            'http://ggggjy.gxgg.gov.cn:9005/zbxx/002001/002001003/002001003001/{}.html',
            'http://ggggjy.gxgg.gov.cn:9005/zbxx/002001/002001003/002001003002/{}.html',
            'http://ggggjy.gxgg.gov.cn:9005/zbxx/002001/002001003/002001003004/{}.html'
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
            detail = html.xpath('//*[@id="main"]/div/div[2]/ul/li')
            for li in detail:
                title = li.xpath('./div/a/text()')[0].replace('\xa0', '').replace('\n', ''). \
                    replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '').replace(
                    "<fontstyle='color:red'>(网)</font>", '')
                url_ = li.xpath('./div/a/@href')[0]
                date_Today = li.xpath('./span/text()')[0].replace('\xa0', '').replace('\n', ''). \
                    replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '') \
                    .replace('[', '').replace(']', '').replace('/', '-')
                if 'http' not in url_:
                    url_ = 'http://ggggjy.gxgg.gov.cn:9005' + url_
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

    # 贺州市公共资源交易中心
    def hezhou(self):
        print('贺州市公共资源交易中心', 'http://www.hzggzy.org.cn')
        url_list = [
            'http://www.hzggzy.org.cn/gxhzzbw/jyxx/001001/001001001/MoreInfo.aspx?CategoryNum=001001001',
            'http://www.hzggzy.org.cn/gxhzzbw/jyxx/001001/001001005/MoreInfo.aspx?CategoryNum=001001005',
            'http://www.hzggzy.org.cn/gxhzzbw/jyxx/001001/001001002/MoreInfo.aspx?CategoryNum=001001002',#结果
            'http://www.hzggzy.org.cn/gxhzzbw/jyxx/001001/001001004/MoreInfo.aspx?CategoryNum=001001004',
            'http://www.hzggzy.org.cn/gxhzzbw/jyxx/001013/001013001/MoreInfo.aspx?CategoryNum=001013001',
            'http://www.hzggzy.org.cn/gxhzzbw/jyxx/001014/001014001/MoreInfo.aspx?CategoryNum=001014001'
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
            '__VIEWSTATE': str(page),
            '__VIEWSTATEGENERATOR': 'E8623272',
            '__EVENTTARGET': 'MoreInfoList1$Pager',
            '__EVENTARGUMENT': page,
            '__VIEWSTATEENCRYPTED': ''
        }
        while True:
            page += 1
            if page == 1:
                text = tool.requests_get(url, headers)
            else:
                text = tool.requests_post(url, data, headers)
            html = HTML(text)
            data['__VIEWSTATE'] = html.xpath('//*[@id="__VIEWSTATE"]/@value')[0]
            data['__EVENTARGUMENT'] = str(page)
            detail = html.xpath('//*[@id="MoreInfoList1_DataGrid1"]/tr')
            for li in detail:
                title = li.xpath('./td[2]/a/@title')[0].replace('\xa0', '').replace('\n', ''). \
                    replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
                url_ = li.xpath('./td[2]/a/@href')[0]
                date_Today = li.xpath('./td[3]/text()')[0].replace('\xa0', '').replace('\n', ''). \
                    replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '') \
                    .replace('[', '').replace(']', '').replace('/', '-')
                if 'http' not in url_:
                    url_ = 'http://www.hzggzy.org.cn' + url_
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

    # 钦州市公共资源交易中心
    def qinzhou(self):
        print('钦州市公共资源交易中心', 'http://ggzyjy.qinzhou.gov.cn')
        url_list = [
            'http://ggzyjy.qinzhou.gov.cn/gxqzzbw/jyxx/001001/001001001/MoreInfo.aspx?CategoryNum=001001001',
            'http://ggzyjy.qinzhou.gov.cn/gxqzzbw/jyxx/001001/001001002/MoreInfo.aspx?CategoryNum=001001002',
            'http://ggzyjy.qinzhou.gov.cn/gxqzzbw/jyxx/001001/001001004/MoreInfo.aspx?CategoryNum=001001004', #控制价
            'http://ggzyjy.qinzhou.gov.cn/gxqzzbw/jyxx/001001/001001005/MoreInfo.aspx?CategoryNum=001001005', #结果
            'http://ggzyjy.qinzhou.gov.cn/gxqzzbw/jyxx/001001/001001006/MoreInfo.aspx?CategoryNum=001001006', #结果

            'http://ggzyjy.qinzhou.gov.cn/gxqzzbw/jyxx/001004/001004001/MoreInfo.aspx?CategoryNum=001004001',
            'http://ggzyjy.qinzhou.gov.cn/gxqzzbw/jyxx/001004/001004002/MoreInfo.aspx?CategoryNum=001004002',
            'http://ggzyjy.qinzhou.gov.cn/gxqzzbw/jyxx/001004/001004004/MoreInfo.aspx?CategoryNum=001004004'#结果
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
            '__CSRFTOKEN': '',
            '__VIEWSTATE': '',
            # '__VIEWSTATEGENERATOR': 'CE49891B',
            '__EVENTTARGET': 'MoreInfoList1$Pager',
            '__EVENTARGUMENT': page,
            '__VIEWSTATEENCRYPTED': ''
        }
        while True:
            page += 1
            if page == 1:
                text = tool.requests_get(url, headers)
            else:
                text = tool.requests_post(url, data, headers)
            html = HTML(text)
            data['__VIEWSTATE'] = html.xpath('//*[@id="__VIEWSTATE"]/@value')[0]
            data['__CSRFTOKEN'] = html.xpath('//*[@id="__CSRFTOKEN"]/@value')[0]
            data['__EVENTARGUMENT'] = str(page)
            detail = html.xpath('//*[@id="MoreInfoList1_DataGrid1"]/tr')
            for li in detail:
                title = li.xpath('./td[2]/a/@title')[0].replace('\xa0', '').replace('\n', ''). \
                    replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '').replace(
                    "<fontstyle='color:red'>(网)</font>", '')
                url_ = li.xpath('./td[2]/a/@href')[0]
                date_Today = li.xpath('./td[3]/text()')[0].replace('\xa0', '').replace('\n', ''). \
                    replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '') \
                    .replace('[', '').replace(']', '').replace('/', '-')
                if 'http' not in url_:
                    url_ = 'http://ggzyjy.qinzhou.gov.cn' + url_
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

    # 阜阳市公共资源交易中心
    def fuyang(self):
        print('阜阳市公共资源交易中心', 'http://jyzx.fy.gov.cn')
        url_list = [
            'http://jyzx.fy.gov.cn/FuYang/ShowInfo/ShowSearchInfo.aspx?CategoryNum=012001&Eptr3=&xiaqu=&Paging={}',
            'http://jyzx.fy.gov.cn/FuYang/ShowInfo/ShowSearchInfo.aspx?CategoryNum=012002&Eptr3=&xiaqu=&Paging={}',
            'http://jyzx.fy.gov.cn/FuYang/ShowInfo/ShowSearchInfo.aspx?CategoryNum=012003&Eptr3=&xiaqu=&Paging={}',
            'http://jyzx.fy.gov.cn/FuYang/ShowInfo/ShowSearchInfo.aspx?CategoryNum=012004&Eptr3=&xiaqu=&Paging={}',
            'http://jyzx.fy.gov.cn/FuYang/ShowInfo/ShowSearchInfo.aspx?CategoryNum=012006&Eptr3=&xiaqu=&Paging={}',
            'http://jyzx.fy.gov.cn/FuYang/ShowInfo/ShowSearchInfo.aspx?CategoryNum=011001&Eptr3=&xiaqu=&Paging={}',
            'http://jyzx.fy.gov.cn/FuYang/ShowInfo/ShowSearchInfo.aspx?CategoryNum=011002&Eptr3=&xiaqu=&Paging={}',
            'http://jyzx.fy.gov.cn/FuYang/ShowInfo/ShowSearchInfo.aspx?CategoryNum=011004&Eptr3=&xiaqu=&Paging={}',
            'http://jyzx.fy.gov.cn/FuYang/ShowInfo/ShowSearchInfo.aspx?CategoryNum=011005&Eptr3=&xiaqu=&Paging={}'
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
            detail = html.xpath('//*[@id="infolist"]/div[1]/div/ul/li')
            for li in detail:
                title = li.xpath('./div/a/@title')[0].replace('\xa0', '').replace('\n', ''). \
                    replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '').replace(
                    "<fontstyle='color:red'>(网)</font>", '')
                url_ = li.xpath('./div/a/@href')[0]
                date_Today = li.xpath('./span/text()')[0].replace('\xa0', '').replace('\n', ''). \
                    replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '') \
                    .replace('[', '').replace(']', '').replace('/', '-')
                if 'http' not in url_:
                    url_ = 'http://jyzx.fy.gov.cn' + url_
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

    # 防城港市公共资源交易中心
    def fangchenggang(self):
        print('防城港市公共资源交易中心', 'http://www.fcgggzy.cn')
        url_list = [
            'http://www.fcgggzy.cn/gxfcgzbw/jyxx/001004/001004001/MoreInfo.aspx?CategoryNum=001004001',
            'http://www.fcgggzy.cn/gxfcgzbw/jyxx/001004/001004002/MoreInfo.aspx?CategoryNum=001004002',
            'http://www.fcgggzy.cn/gxfcgzbw/jyxx/001004/001004007/MoreInfo.aspx?CategoryNum=001004007',
            'http://www.fcgggzy.cn/gxfcgzbw/jyxx/001004/001004004/MoreInfo.aspx?CategoryNum=001004004',#结果
            'http://www.fcgggzy.cn/gxfcgzbw/jyxx/001004/001004008/MoreInfo.aspx?CategoryNum=001004008',
            'http://www.fcgggzy.cn/gxfcgzbw/jyxx/001004/001004009/MoreInfo.aspx?CategoryNum=001004009',

            'http://www.fcgggzy.cn/gxfcgzbw/jyxx/001001/001001001/MoreInfo.aspx?CategoryNum=001001001',
            'http://www.fcgggzy.cn/gxfcgzbw/jyxx/001001/001001002/MoreInfo.aspx?CategoryNum=001001002',
            'http://www.fcgggzy.cn/gxfcgzbw/jyxx/001001/001001004/MoreInfo.aspx?CategoryNum=001001004',
            'http://www.fcgggzy.cn/gxfcgzbw/jyxx/001001/001001005/MoreInfo.aspx?CategoryNum=001001005',
            'http://www.fcgggzy.cn/gxfcgzbw/jyxx/001001/001001006/MoreInfo.aspx?CategoryNum=001001006',
            'http://www.fcgggzy.cn/gxfcgzbw/jyxx/001001/001001008/MoreInfo.aspx?CategoryNum=001001008',

            'http://www.fcgggzy.cn/gxfcgzbw/jyxx/001011/001011001/MoreInfo.aspx?CategoryNum=001011001',
            'http://www.fcgggzy.cn/gxfcgzbw/jyxx/001011/001011002/MoreInfo.aspx?CategoryNum=001011002',
            'http://www.fcgggzy.cn/gxfcgzbw/jyxx/001011/001011008/MoreInfo.aspx?CategoryNum=001011008',
            'http://www.fcgggzy.cn/gxfcgzbw/jyxx/001011/001011004/MoreInfo.aspx?CategoryNum=001011004',

            'http://www.fcgggzy.cn/gxfcgzbw/jyxx/001010/001010001/MoreInfo.aspx?CategoryNum=001010001',
            'http://www.fcgggzy.cn/gxfcgzbw/jyxx/001010/001010002/MoreInfo.aspx?CategoryNum=001010002',
            'http://www.fcgggzy.cn/gxfcgzbw/jyxx/001010/001010008/MoreInfo.aspx?CategoryNum=001010008',
            'http://www.fcgggzy.cn/gxfcgzbw/jyxx/001010/001010004/MoreInfo.aspx?CategoryNum=001010004'
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
            # '__CSRFTOKEN': '',
            '__VIEWSTATE': '',
            '__VIEWSTATEGENERATOR': '42628481',
            '__EVENTTARGET': 'MoreInfoList1$Pager',
            '__EVENTARGUMENT': page,
            '__VIEWSTATEENCRYPTED': ''
        }
        while True:
            page += 1
            if page == 1:
                text = tool.requests_get(url, headers)
            else:
                text = tool.requests_post(url, data, headers)
            html = HTML(text)
            data['__VIEWSTATE'] = html.xpath('//*[@id="__VIEWSTATE"]/@value')[0]
            # data['__CSRFTOKEN'] = html.xpath('//*[@id="__CSRFTOKEN"]/@value')[0]
            data['__EVENTARGUMENT'] = str(page)
            detail = html.xpath('//*[@id="MoreInfoList1_DataGrid1"]/tr')
            for li in detail:
                title = li.xpath('./td[2]/a/@title')[0].replace('\xa0', '').replace('\n', ''). \
                    replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '').replace(
                    "<fontstyle='color:red'>(网)</font>", '')
                url_ = li.xpath('./td[2]/a/@href')[0]
                date_Today = li.xpath('./td[3]/text()')[0].replace('\xa0', '').replace('\n', ''). \
                    replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '') \
                    .replace('[', '').replace(']', '').replace('/', '-')
                if 'http' not in url_:
                    url_ = 'http://www.fcgggzy.cn' + url_
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

    # 青海项目信息网
    def qinghai(self):
        print('青海项目信息网', 'http://www.qhei.net.cn')
        url_list = [
            'http://www.qhei.net.cn/html/zbcg/list_1698.html',
            'http://www.qhei.net.cn/html/zbcg/list_1696.html',
            'http://www.qhei.net.cn/html/zbcg/list_1695.html',
            'http://www.qhei.net.cn/html/zbcg/list_1694.html',
            'http://www.qhei.net.cn/html/zbcg/list_1692.html',
            'http://www.qhei.net.cn/html/zbcg/list_1691.html'
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
            detail = html.xpath('/html/body/div[6]/div[2]/ul/li')
            for li in detail:
                title = li.xpath('./a/@title')[0].replace('\xa0', '').replace('\n', ''). \
                    replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '').replace(
                    "<fontstyle='color:red'>(网)</font>", '')
                url_ = li.xpath('./a/@href')[0]
                try:
                    date_Today = li.xpath('./font/text()')[0].replace('\xa0', '').replace('\n', ''). \
                        replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '') \
                        .replace('[', '').replace(']', '').replace('/', '-')
                except:
                    date_Today = li.xpath('./text()')[0].replace('\xa0', '').replace('\n', ''). \
                        replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '') \
                        .replace('[', '').replace(']', '').replace('/', '-')
                if 'http' not in url_:
                    url_ = 'http://www.qhei.net.cn' + url_
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

    # 马鞍山市公共资源交易中心
    def maanshan(self):
        print('马鞍山市公共资源交易中心', 'http://zbcg.mas.gov.cn')
        url_list = [
            'http://zbcg.mas.gov.cn/fwdt/002005/002005001/{}.html',
            'http://zbcg.mas.gov.cn/fwdt/002005/002005002/{}.html'
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
                text = tool.requests_get(url.format('tradelist'), headers)
            else:
                text = tool.requests_get(url.format(page), headers)
            html = HTML(text)
            detail = html.xpath('/html/body/div[2]/div[2]/div[2]/div[3]/ul/li')
            for li in detail:
                title = li.xpath('./div/a/text()')[0].replace('\xa0', '').replace('\n', ''). \
                    replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '').replace(
                    "<fontstyle='color:red'>(网)</font>", '')
                url_ = li.xpath('./div/a/@href')[0]
                date_Today = li.xpath('./span/text()')[0].replace('\xa0', '').replace('\n', ''). \
                    replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '') \
                    .replace('[', '').replace(']', '').replace('/', '-')
                if 'http' not in url_:
                    url_ = 'http://zbcg.mas.gov.cn' + url_
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

    def parse(self): # 全国公共资源交易平台
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


