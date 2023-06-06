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
            [self.sanming,'http://www.alsggzyjy.cn'],
            [self.linxi, 'http://www.asggzyjy.cn'],
            [self.leshan, 'http://www.ggzy.anshun.gov.cn'],
            [self.yunan, 'http://ggzy.jlbc.gov.cn'],
            [self.neijiang, 'http://bsggzyjy.cbs.gov.cn'],
            [self.beijing, 'http://www.bszwzx.gov.cn'],
            # [self.beijingzf, 'http://zfcg.baotou.gov.cn'], 打不开
            [self.nanjing, 'http://www.bcactc.com'],
            [self.nanchong, 'https://www.bjggzyzhjy.cn'],
            [self.nanping, 'http://www.bijie.gov.cn'],
            [self.nanchang, 'http://www.ccggzy.com.cn'],
            [self.nantong, 'http://111.8.133.22:8000'],
            [self.jian, 'http://fwpt.csggzy.cn'],
            [self.jilin, 'http://ggzy.changzhi.gov.cn'],
            [self.jilinzf, 'http://218.60.2.98'],
            [self.jiayuguan, 'http://czggzy.czs.gov.cn'],
            [self.sichuan, 'http://www.cxggzy.cn'],
            [self.weihai, 'https://www.dlggzy.cn'],
            [self.anhui, 'http://ggzyjy.dl.gov.cn'],
            [self.yichun, 'http://218.61.232.162'],
            [self.suqian, 'http://ggzyjy.dt.gov.cn'],
            [self.bazhong, 'https://jyzx.dh.gov.cn'],
            [self.changzhou, 'http://183.224.249.60:8001'],
            [self.guangdong, 'http://www.ezggzy.cn'],
            [self.guangdongzf, 'http://ggzy.fuxin.gov.cn'],
            [self.guangyuan, 'http://www.gyggzyjy.cn'],
            [self.guangan, 'http://ztb.guizhou.gov.cn'],
            [self.qingyang, 'http://ggzy.hebi.gov.cn'],
            [self.zhangye, 'http://www.hebeieb.com'],
            # [self.xuzhou, 'http://ztbzx.hbsjtt.gov.cn'], 打不开
            [self.dezhou, 'http://hndzzbtb.hndrc.gov.cn'],
            #　[self.chengdu, 'http://www.qzggzy.com'],　打不开
            [self.yangzhou, 'https://www.hhzy.net'],
            [self.panzhihua, 'http://ggzy.huaihua.gov.cn'],
            [self.xinyu, 'http://www.hldggzyjyzx.com.cn'],
            [self.wuxi, 'http://www.jxzbtb.cn'],
            [self.rizhao, 'http://www.jlsggzyjy.gov.cn'],
            [self.zaozhuang, 'http://jnggzy.jinan.gov.cn'],
            [self.jiangsu, 'http://www.jcggzyfw.cn'],
            # #[self.jiangxi, 'http://zyjy.jingmen.gov.cn'], 网站改版 需要登陆
            [self.taizhou, 'http://ggzy.sxjz.gov.cn'],
            [self.luzhou, 'http://ggzy.jz.gov.cn'],
            [self.jining, 'http://www.kfsggzyjyw.cn'],
            [self.hubei, 'https://www.kmggzy.com'],
            [self.binzhou, 'http://ggzy.lasa.gov.cn'],
            [self.zhangzhou, 'https://www.ljggzyxx.cn'],
            [self.weifang, 'http://lssggzy.lishui.gov.cn'],
            [self.yantai, 'http://ggzy.gzlps.gov.cn'],
            [self.gansu, 'http://ldggzy.hnloudi.gov.cn'],
            [self.baiyin, 'https://www.lhjs.cn'],
            [self.yancheng, 'http://www.lyggzyjy.cn'],
            [self.meishan, 'http://www.mzlggzy.org.cn'],
            [self.fuzhou, 'http://www.nyggzyjy.cn'],
            [self.liaocheng, 'http://www.nmggcztb.cn'],
            [self.putian, 'http://bidding.ningbo.gov.cn'],
            [self.xian, 'http://182.246.203.127:8001'],
            [self.xizang, 'http://202.97.171.175'],
            [self.xizangzf, 'http://www.pdsggzy.com'],
            [self.dazhou, 'http://www.pesggzyjyxxw.com'],
            [self.jinchang, 'http://ggzyjyzx.qdn.gov.cn'],
            [self.longnan, 'http://ggzy.qiannan.gov.cn'],
            [self.shanxi, 'http://ggzyjy.qxn.gov.cn'],
            [self.yaan, 'https://ggzy.qingdao.gov.cn'],
            [self.longyan, 'http://jyxt.qjggzyxx.gov.cn']
        ]

    # 阿拉善公共资源交易网
    def sanming(self):
        print('阿拉善公共资源交易网', 'http://www.alsggzyjy.cn')
        url_list = [
            # 建设工程
            # 招标公告
            ['000', '2'],
            # 招标变更
            ['001', '2'],
            # 中标候选人公示
            ['002', '2'],
            # 中标、流标公告
            ['003', '2'],
            # 政府采购
            # 采购公告
            ['006', '1'],
            # 变更公告
            ['001', '1'],
            # 中标
            ['003', '1'],
            # 废标
            ['007', '1'],
        ]
        headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Cookie': 'JSESSIONID=662863FD2199FBD1672A04A290868047; _CSRFCOOKIE=73F3D7A1BCDCA9001D7B1483A214C4E98DE2528B; EPTOKEN=73F3D7A1BCDCA9001D7B1483A214C4E98DE2528B; oauthClientId=demoClient; oauthPath=http://172.16.5.21:8080/EpointWebBuilder; oauthLoginUrl=http://172.16.5.21:8080/EpointWebBuilder/rest/oauth2/authorize?client_id=demoClient&state=a&response_type=code&scope=user&redirect_uri=; oauthLogoutUrl=http://172.16.5.21:8080/EpointWebBuilder/rest/oauth2/logout?redirect_uri=; noOauthRefreshToken=986d4fe7e5dd29b64c9e7b7a6d66e089; noOauthAccessToken=77c09e0bf98b6220b544961097eed84a; sub_domain_cokie=TiG5CMD9KQ41mmsARPTuAg%3D%3D; region_name=%E4%B9%8C%E9%B2%81%E6%9C%A8%E9%BD%90%E5%B8%82',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',

        }
        code = url_list.pop(0)
        page = 0
        ls = []
        while True:
            page += 1
            url = 'http://www.alsggzyjy.cn/PublicServer/commonAnnouncementAction/getCommonAnnouncementList.do?businessType={}&announcementType={}&page={}&rows=15&areaCode=152900'
            if code[0] == '003' and code[1] == '2':
                url = 'http://www.alsggzyjy.cn/PublicServer/commonAnnouncementAction/getAnnsByBulletinList.do?businessType={}&announcementType={}&page={}&rows=15&areaCode=152900'
            text = tool.requests_get(url.format(code[1], code[0], page), headers)
            detail = json.loads(text)['data']['list']
            for i in detail:
                title = i['title']
                url_ = 'http://www.alsggzyjy.cn/PublicServer/public/commonAnnouncement/showDetail.html?businessType=2&sidebarIndex={}&id='.format(
                    int(code[0][2]) + 1) + i['id']
                date_Today = i['publishTime'][:10]
                if tool.Transformation(date_Today) > tool.Transformation(self.date):
                    continue
                elif tool.Transformation(date_Today) == tool.Transformation(self.date):
                    ls.append(url_)
                else:
                    if len(url_list) == 0:
                        return [len(ls), ls]
                    else:
                        code = url_list.pop(0)
                        page = 0
                        break

    # 鞍山市公共资源交易平台
    def linxi(self):
        print('鞍山市公共资源交易平台', 'http://www.asggzyjy.cn')
        url_list = [
            # 建设工程
                # 招标公告
            'http://www.asggzyjy.cn/gcjs/014001/{}.html',
                # 中标公示
            'http://www.asggzyjy.cn/gcjs/014002/{}.html',
                # 中标结果
            'http://www.asggzyjy.cn/gcjs/014003/{}.html',
            # 政府采购
                # 采购公告
            'http://www.asggzyjy.cn/zfcg/015001/{}.html',
                # 中标通知
            'http://www.asggzyjy.cn/zfcg/015002/{}.html'
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
            if page == 1:
                text = tool.requests_get(url.format('about'), headers)
            html = HTML(text)
            detail = html.xpath('/html/body/div[2]/div/div/div[2]/div[2]/div[2]/ul/li')
            for li in detail:
                title = li.xpath('./a/@title')[0]
                url_ = 'http://www.asggzyjy.cn' + li.xpath('./a/@href')[0]
                date_Today = li.xpath('./span/text()')[0].replace('\r', '').replace('\t', '').replace('\n', '') \
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

    # 安顺市公共资源交易平台
    def leshan(self):
        print('安顺市公共资源交易平台', 'http://www.ggzy.anshun.gov.cn')
        url_list = [
            # 市本级
            #   工程建设
            #       招标公告
            'http://www.ggzy.anshun.gov.cn/jyxx/jsgc/zbgg_5377271/{}.html',
            #       中标公示
            'http://www.ggzy.anshun.gov.cn/jyxx/jsgc/jyjggs/{}.html',
            #       更正公告
            'http://www.ggzy.anshun.gov.cn/jyxx/jsgc/fbgg/{}.html',
            #       流标公告
            'http://www.ggzy.anshun.gov.cn/jyxx/jsgc/dycg/{}.html',
            #   政府采购
            #       采购公告
            'http://www.ggzy.anshun.gov.cn/jyxx/zfcg/zbgg_5377276/{}.html',
            #       中标公告
            'http://www.ggzy.anshun.gov.cn/jyxx/zfcg/jyjggs_5377277/{}.html',
            #       更正公告
            'http://www.ggzy.anshun.gov.cn/jyxx/zfcg/dycg_5377280/{}.html',
            #       流标公告
            'http://www.ggzy.anshun.gov.cn/jyxx/zfcg/fbgg_5377278/{}.html'
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
                text = tool.requests_get(url.format('index'), headers)
            else:
                text = tool.requests_get(url.format('index_' + str(page)), headers)
            html = HTML(text)
            detail = html.xpath('/html/body/div[2]/div[2]/div[2]/ul/li')
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

    # 白城市公共资源交易平台
    def yunan(self):
        print('白城市公共资源交易平台', 'http://ggzy.jlbc.gov.cn')
        url_list = [
            # 工程建设
            'http://ggzy.jlbc.gov.cn/jyxx/003001/{}.html',
            # 政府采购
            'http://ggzy.jlbc.gov.cn/jyxx/003002/{}.html'
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

    # 白山公共资源交易中心
    def neijiang(self):
        print('白山公共资源交易中心', 'http://bsggzyjy.cbs.gov.cn')
        url_list = [
            # 工程建设
            'http://bsggzyjy.cbs.gov.cn/jyxx/003001/{}.html',
            # 政府采购
            'http://bsggzyjy.cbs.gov.cn/jyxx/003002/{}.html'
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
            detail = html.xpath('/html/body/div[2]/div/div/div[2]/div/div[2]/ul/li')
            for li in detail:
                title = li.xpath('./div/a/@title')[0]
                url_ = 'http://bsggzyjy.cbs.gov.cn' + li.xpath('./div/a/@href')[0]
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

    # 保山市公共资源交易平台
    def beijing(self):
        print('保山市公共资源交易平台', 'http://www.bszwzx.gov.cn')
        url_list = [
            # 市本级
            #   工程建设
            #       招标公告
            ['http://www.bszwzx.gov.cn/jyxx/jsgcZbgg?currentPage={}','//*[@id="zbggForm"]/div[3]/table/tr'],
            #       变更公告
            ['http://www.bszwzx.gov.cn/jyxx/jsgcBgtz?currentPage={}','//*[@id="bgtzForm"]/div[2]/table/tr'],
            #       评标结果公示
            ['http://www.bszwzx.gov.cn/jyxx/jsgcpbjggs?currentPage={}','//*[@id="zbggForm"]/div[2]/table/tr'],
            #       中标结果
            ['http://www.bszwzx.gov.cn/jyxx/jsgcZbjggs?currentPage={}','//*[@id="zbggForm"]/div[3]/table/tr'],
            #       异常公告
            ['http://www.bszwzx.gov.cn/jyxx/jsgcZbyc?currentPage={}','//*[@id="ycggForm"]/div[2]/table/tr'],
            #   政府采购
            #       采购公告
            ['http://www.bszwzx.gov.cn/jyxx/zfcg/cggg?currentPage={}','//*[@id="zbggForm"]/div[2]/table/tr'],
            #       变更通知
            ['http://www.bszwzx.gov.cn/jyxx/zfcg/gzsx?currentPage={}','//*[@id="zbggForm"]/div[2]/table/tr'],
            #       结果公示
            ['http://www.bszwzx.gov.cn/jyxx/zfcg/zbjggs?currentPage={}','//*[@id="zbggForm"]/div[2]/table/tr'],
            #       异常公示
            ['http://www.bszwzx.gov.cn/jyxx/zfcg/zfcgYcgg?currentPage={}','//*[@id="ycggForm"]/div[2]/table/tr']
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
                    url_ = 'http://www.bszwzx.gov.cn' + html.xpath(url[1] + '[{}]/td[3]/a/@href'.format(i + 1))[0]
                    date_Today = html.xpath(url[1] + '[{}]/td[4]/text()'.format(i + 1))[0]
                    if '招标' in date_Today or '采购' in date_Today:
                        date_Today = html.xpath(url[1] + '[{}]/td[5]/text()'.format(i + 1))[0]
                    if title == '':
                        title = html.xpath(url[1] + '[{}]/td[3]/@title'.format(i + 1))[0]
                except:
                    title = html.xpath(url[1] + '[{}]/td[4]/a/@title'.format(i + 1))[0]
                    url_ = 'http://www.bszwzx.gov.cn' + html.xpath(url[1] + '[{}]/td[4]/a/@href'.format(i + 1))[0]
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

    def processing_image(self):
        img = Image.open('yzm.png').convert("L")
        pixdata = img.load()
        w, h = img.size
        threshold = 160
        # 遍历所有像素，大于阈值的为黑色
        for y in range(h):
            for x in range(w):
                if pixdata[x, y] < threshold:
                    pixdata[x, y] = 0
                else:
                    pixdata[x, y] = 255
        data = img.getdata()
        w, h = img.size
        black_point = 0
        for x in range(1, w - 1):
            for y in range(1, h - 1):
                mid_pixel = data[w * y + x]  # 中央像素点像素值
                if mid_pixel < 50:  # 找出上下左右四个方向像素点像素值
                    top_pixel = data[w * (y - 1) + x]
                    left_pixel = data[w * y + (x - 1)]
                    down_pixel = data[w * (y + 1) + x]
                    right_pixel = data[w * y + (x + 1)]
                    # 判断上下左右的黑色像素点总个数
                    if top_pixel < 10:
                        black_point += 1
                    if left_pixel < 10:
                        black_point += 1
                    if down_pixel < 10:
                        black_point += 1
                    if right_pixel < 10:
                        black_point += 1
                    if black_point < 1:
                        img.putpixel((x, y), 255)
                    black_point = 0
        pytesseract.pytesseract.tesseract_cmd = r"D:\Tesseract-OCR\tesseract.exe"  # 设置pyteseract路径
        result = pytesseract.image_to_string(img)  # 图片转文字
        resultj = re.sub(u"([^\u4e00-\u9fa5\u0030-\u0039\u0041-\u005a\u0061-\u007a])", "", result)  # 去除识别出来的特殊字符
        result_four = resultj[0:4]  # 只获取前4个字符
        # print(result_four)  # 打印识别的验证码
        # time.sleep(6666)
        return result_four

    # 包头市政府采购网  网站打不开
    def beijingzf(self):
        print('包头市政府采购网', 'http://zfcg.baotou.gov.cn')
        url_list = [
            # 招标公告
            'http://zfcg.baotou.gov.cn/portal/topicView.do?method=view&view=stockBulletin&id=1660&stockModeIdType=666&ver=2',
            # 单一来源
            'http://zfcg.baotou.gov.cn/portal/topicView.do?method=view&view=stockBulletin&id=1660&stockModeIdType=60&ver=2',
            # 中标公告
            'http://zfcg.baotou.gov.cn/portal/topicView.do?method=view&view=stockBulletin&id=2014&ver=2',
            # 更正公告
            'http://zfcg.baotou.gov.cn/portal/topicView.do?method=view&view=stockBulletin&id=1663&ver=2',
            # 合同公告
            'http://zfcg.baotou.gov.cn/portal/topicView.do?method=view&view=stockBulletin&id=2015&ver=2',
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
        print('打开浏览器...')
        options = webdriver.ChromeOptions()
        # 不加载图片,加快访问速度
        # options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
        print('设置无界面模式...')
        options.add_argument('--headless')
        # 此步骤很重要，设置为开发者模式，防止被各大网站识别出来使用了Selenium
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        driver = webdriver.Chrome(options=options)
        driver.maximize_window()
        print('请求首页...')
        driver.get(url)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
            'Cookie': 'UM_distinctid=16f7d9a380334c-09e791f4fa51bd-e343166-1fa400-16f7d9a380437f; JSESSIONID=' +
                      driver.get_cookies()[0]['value'] + '; CNZZDATA1278039014=1257312036-1578357560-%7C1578373994'
        }
        while True:
            page += 1
            text = driver.page_source
            if '请输入验证码查看公告列表' in text:
                yzm_url = 'http://zfcg.baotou.gov.cn/commons/imageTopic.jsp'
                img = requests.get(yzm_url, headers=headers)
                with open('yzm.png', 'wb') as f:
                    f.write(img.content)
                time.sleep(1)
                driver.find_element_by_id('verify').send_keys(self.processing_image())
                driver.find_element_by_xpath('/html/body/form/div/div[2]/input').click()
                text = driver.page_source
            html = HTML(text)
            detail = html.xpath('//*[@id="topicChrList_20070702_table"]/tbody/tr')
            for tr in detail:
                title = tr.xpath('./td[2]/a/text()')[0]
                url_ = 'http://zfcg.baotou.gov.cn/portal/documentView.do?method=view&id={}&ver=null'.format(
                    tr.xpath('./td[2]/a/@href')[0].replace('/viewer.do?id=', ''))
                date_Today = tr.xpath('./td[3]/text()')[0][:10]
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

    # 北京市建设工程信息网
    def nanjing(self):
        print('北京市建设工程信息网', 'http://www.bcactc.com')
        url_list = [
            # 勘察设计
                # 中标候选人
            'http://www.bcactc.com/home/gcxx/now_kcsjzbgs.aspx',
            # 施工
            'http://www.bcactc.com/home/gcxx/now_sgzbgg.aspx',
            'http://www.bcactc.com/home/gcxx/now_sgzbgs.aspx',
                # 中标结果
            'http://www.bcactc.com/home/gcxx/now_zbjggs.aspx?type=sg',
            # 监理
            'http://www.bcactc.com/home/gcxx/now_jlzbgg.aspx',
            'http://www.bcactc.com/home/gcxx/now_jlzbgs.aspx',
            'http://www.bcactc.com/home/gcxx/now_zbjggs.aspx?type=jl',
            # 专业
            'http://www.bcactc.com/home/gcxx/now_zyzbgg.aspx',
            'http://www.bcactc.com/home/gcxx/now_zyzbgs.aspx',
            'http://www.bcactc.com/home/gcxx/now_zbjggs.aspx?type=zy',
            # 材料设备
            'http://www.bcactc.com/home/gcxx/now_clsbzbgg.aspx',
            'http://www.bcactc.com/home/gcxx/now_clsbzbgs.aspx',
            'http://www.bcactc.com/home/gcxx/now_zbjggs.aspx?type=clsb',
            # 铁路
            'http://www.bcactc.com/home/gcxx/now_tdzbgg.aspx',
            'http://www.bcactc.com/home/gcxx/now_tdzbgs.aspx',
            'http://www.bcactc.com/home/gcxx/now_zbjggs.aspx?type=tl',
            # 园林
            'http://www.bcactc.com/home/gcxx/now_ylzbgg.aspx',
            'http://www.bcactc.com/home/gcxx/now_ylzbgs.aspx',
            'http://www.bcactc.com/home/gcxx/now_zbjggs.aspx?type=yl',
            # 其他
            'http://www.bcactc.com/home/gcxx/now_qtzbgg.aspx'
        ]
        headers = {
            'Cookie': 'Hm_lvt_ae3702a0997d560bba5902699c6cf1cc=1614046447; _d_id=7fea23cc84484839c41aab727f0371; Hm_lpvt_ae3702a0997d560bba5902699c6cf1cc=1614046525',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
        }
        url = url_list.pop(0)
        ls = []
        while True:
            text = tool.requests_get(url, headers)
            html = HTML(text)
            detail = html.xpath('//*[@id="MyGridView1"]/tr')
            for i in range(1, len(detail)):
                try:
                    title = html.xpath('//*[@id="MyGridView1"]/tr[{}]/td[2]/a/text()'.format(i + 1))[0]
                except:
                    title = html.xpath('//*[@id="MyGridView1"]/tr[{}]/td[1]/a/text()'.format(i + 1))[0]
                try:
                    url_ = 'http://www.bcactc.com/home/gcxx/' + \
                          html.xpath('//*[@id="MyGridView1"]/tr[{}]/td[2]/a/@href'.format(i + 1))[0]
                except:
                    url_ = 'http://www.bcactc.com/home/gcxx/' + \
                          html.xpath('//*[@id="MyGridView1"]/tr[{}]/td[1]/a/@href'.format(i + 1))[0]
                try:
                    date_Today = html.xpath('//*[@id="MyGridView1"]/tr[{}]/td[5]/text()'.format(i + 1))[0][:10]
                    if '-' not in date_Today:
                        int('a')
                except:
                    try:
                        date_Today = html.xpath('//*[@id="MyGridView1"]/tr[{}]/td[3]/text()'.format(i + 1))[0][:10]
                        if '-' not in date_Today:
                            int('a')
                    except:
                        try:
                            date_Today = html.xpath('//*[@id="MyGridView1"]/tr[{}]/td[2]/text()'.format(i + 1))[0][:10]
                            if '-' not in date_Today:
                                int('a')
                        except:
                            date_Today = html.xpath('//*[@id="MyGridView1"]/tr[{}]/td[4]/text()'.format(i + 1))[0][:10]
                title = title.replace('\u30fb', '')
                date_Today = date_Today.replace(' ', '').replace('\r', '').replace('\t', '')
                if tool.Transformation(date_Today) > tool.Transformation(self.date):
                    continue
                elif tool.Transformation(date_Today) == tool.Transformation(self.date):
                    ls.append(url_)
                    continue
                else:
                    if len(url_list) == 0:
                        return [len(ls), ls]
                    else:
                        break
            url = url_list.pop(0)
            page = 0
            
    # 北京市公共资源综合交易系统
    def nanchong(self):
        print('北京市公共资源综合交易系统', 'https://www.bjggzyzhjy.cn')
        url_list = [
            # 招标公告
            'https://www.bjggzyzhjy.cn/G2/public-notice!noticeList.do?',
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
                'data': '',
                'defined_operations_': '',
                'nocheck_operations_': '',
                'gridSearch': 'false',
                'nd': str(time.time()).replace(".", "")[:13],
                'PAGESIZE': '10',
                'PAGE': page,
                'sortField': '',
                'sortDirection': 'asc'
            }
            if 'noticeList' in url:
                data[
                    'filter_params_'] = 'bidNoticeId,packageId,projectId,enrollId,reviewWay,noticePublishWay,tenderNoticeNo,tenderCategory,enrollEntId,bidSectionNameAndCode,packageName,rowNum,uniformProjectCode,systemType,projectName,projectType,applyTimeStart,applyTimeEnd'
            elif 'noticePubList' in url:
                data[
                    'filter_params_'] = 'resultPubGatherId,projectId,packageId,resultPubId,publicityType,packageName,rowNum,systemType,bidSectionNameAndCode,uniformProjectCode,projectName,projectType,tenderCategory'
            text = tool.requests_post(url, data, headers)
            detail = json.loads(text)['data']
            for i in detail:
                title = i['packageName']
                code = i['systemType']['desc']
                if '水利工程' in code:
                    url_ = 'https://www.bjggzyzhjy.cn/G2/pubnotice/sw-tender-notice!previewNoticeSingle.do?flag=toLogin&view' \
                          'Flag=false&projectId='
                elif '交通工程' in code:
                    url_ = 'https://www.bjggzyzhjy.cn/G2/pubnotice/jt-tender-notice!previewNotice.do?flag=toLogin&viewFlag=' \
                          'false&projectId='
                elif '勘察设计' in code:
                    url_ = 'https://www.bjggzyzhjy.cn/G2/pubnotice/kb-enroll!previewNotice.do?flag=toLogin&viewFlag=false&' \
                          'projectId=ff8080816f6b494e016f784c5dc10b84&bidNoticeId='
                else:
                    url_ = 'https://www.bjggzyzhjy.cn/G2/pubnotice/ty-tender-notice!previewNotice.do?flag=toLogin&viewFlag=' \
                          'false&projectId='
                url_ += i['projectId']
                date_Today = i['applyTimeStart'][:10]
                date_Today_end = i['applyTimeEnd'][:10]
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

    # 毕节市公共资源交易平台
    def nanping(self):
        print('毕节市公共资源交易平台', 'http://www.bijie.gov.cn')
        url_list = [
            # 市本级
            #   工程建设
            #       招标公告
            'http://www.bijie.gov.cn/bm/bjsggzyjyzx/jy/jsgc/zbgg_5127738/{}.html',
            #       中标公示
            'http://www.bijie.gov.cn/bm/bjsggzyjyzx/jy/jsgc/zbgs/{}.html',
            #       更正公告
            'http://www.bijie.gov.cn/bm/bjsggzyjyzx/jy/jsgc/bggg_5127740/{}.html',
            #       流标公告
            'http://www.bijie.gov.cn/bm/bjsggzyjyzx/jy/jsgc/lbgg_5127742/{}.html',
            #   政府采购
            #       采购公告
            'http://www.bijie.gov.cn/bm/bjsggzyjyzx/jy/zfcg_5127744/cggg_5127745/{}.html',
            #       中标公告
            'http://www.bijie.gov.cn/bm/bjsggzyjyzx/jy/zfcg_5127744/jggg_5127748/{}.html',
            #       更正公告
            'http://www.bijie.gov.cn/bm/bjsggzyjyzx/jy/zfcg_5127744/bggg_5127747/{}.html',
            #       流标公告
            'http://www.bijie.gov.cn/bm/bjsggzyjyzx/jy/zfcg_5127744/lbgg_5127749/{}.html'
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
            detail = html.xpath('/html/body/div[3]/div[3]/div[2]/div[1]/ul/li')
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

    # 长春市公共资源交易网
    def nanchang(self):
        print('长春市公共资源交易网', 'http://www.ccggzy.com.cn')
        url_list = [
            # 政府采购
                # 采购公告
            'http://www.ccggzy.com.cn/ccggzy/getxxgkAction.action?cmd=getCityZfcgInfo&pageIndex={}&pageSize=16&siteGuid=7eb5f7f1-9041-43ad-8e13-8fcb82ea831a&categorynum=002001&xiaqucode=220101&jyfl=%E5%85%A8%E9%83%A8',
                # 更正公告
            'http://www.ccggzy.com.cn/ccggzy/getxxgkAction.action?cmd=getCityZfcgInfo&pageIndex={}&pageSize=16&siteGuid=7eb5f7f1-9041-43ad-8e13-8fcb82ea831a&categorynum=002001003&xiaqucode=220101&jyfl=%E5%85%A8%E9%83%A8',
                # 中标公告
            'http://www.ccggzy.com.cn/ccggzy/getxxgkAction.action?cmd=getCityZfcgInfo&pageIndex={}&pageSize=16&siteGuid='
            '7eb5f7f1-9041-43ad-8e13-8fcb82ea831a&categorynum=002001004&xiaqucode=220101&jyfl=%E5%85%A8%E9%83%A8',
            # 工程建设
                # 招标公告
            'http://www.ccggzy.com.cn/ccggzy/getxxgkAction.action?cmd=getCityTradeInfo&categorynum=002002001&xiaqucode=220101&pageSize=18&pageIndex={}&siteguid=7eb5f7f1-9041-43ad-8e13-8fcb82ea831a',
                # 中标候选人
            'http://www.ccggzy.com.cn/ccggzy/getxxgkAction.action?cmd=getCityTradeInfo&categorynum=002002002&xiaqucode=220101&pageSize=18&pageIndex={}&siteguid=7eb5f7f1-9041-43ad-8e13-8fcb82ea831a',
            'http://www.ccggzy.com.cn/ccggzy/getxxgkAction.action?cmd=getCityTradeInfo&categorynum=002002003&xiaqucode=220101&pageSize=18&pageIndex={}&siteguid=7eb5f7f1-9041-43ad-8e13-8fcb82ea831a',
                # 中标结果
            'http://www.ccggzy.com.cn/ccggzy/getxxgkAction.action?cmd=getCityTradeInfo&categorynum=002002004&xiaqucode=220101&pageSize=18&pageIndex={}&siteguid=7eb5f7f1-9041-43ad-8e13-8fcb82ea831a'
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
                title = li['title']
                url_ = 'http://www.ccggzy.com.cn' + li['href']
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

    # 常德市公共资源交易平台
    def nantong(self):
        print('常德市公共资源交易平台', 'http://111.8.133.22:8000')
        url_list = [
            # 市本级
            #   工程建设
            #       招标公告
            'http://111.8.133.22:8000/jyxx/014001/014001001/{}.html',
            #       更正公告
            'http://111.8.133.22:8000/jyxx/014001/014001004/{}.html',
            #       中标候选人
            'http://111.8.133.22:8000/jyxx/014001/014001002/{}.html',
            #       中标结果
            'http://111.8.133.22:8000/jyxx/014001/014001003/{}.html',
            #   政府采购
            #       采购公告
            'http://111.8.133.22:8000/jyxx/014002/014002001/{}.html',
            #       更正公告
            'http://111.8.133.22:8000/jyxx/014002/014002003/{}.html',
            #       中标成交公告
            'http://111.8.133.22:8000/jyxx/014002/014002002/{}.html',
            #       废标公告
            'http://111.8.133.22:8000/jyxx/014002/014002004/{}.html'
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
                text = tool.requests_get(url.format('moreinfo_jyxxlist'), headers)
            else:
                text = tool.requests_get(url.format(page), headers)
            html = HTML(text)
            detail = html.xpath('//*[@class="table ewb-engineer-main"]/tbody/tr')
            for li in detail:
                title = li.xpath('./td[1]/a/@title')[0]
                url_ = 'http://111.8.133.22:8000' + li.xpath('./td[1]/a/@href')[0]
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

    # 长沙市公共资源交易平台
    def jian(self):
        print('长沙市公共资源交易平台', 'http://fwpt.csggzy.cn')
        url_list = [
            # 房屋市政
            'http://fwpt.csggzy.cn/jyxxfjsz/index_{}.jhtml',
            # 交通工程
            'http://fwpt.csggzy.cn/jyxxjtgc/index_{}.jhtml',
            # 水利工程
            'http://fwpt.csggzy.cn/jyxxslgc/index_{}.jhtml',
            # 政府采购
            'http://fwpt.csggzy.cn/jyxxzfcg/index_{}.jhtml',
            # 医药采购
            'http://fwpt.csggzy.cn/jyxxyycg/index_{}.jhtml'
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
            detail = html.xpath('/html/body/div[4]/div[4]/div/div[3]/div[2]/ul/li')
            for li in detail:
                title = li.xpath('./p[1]/a/@title')[0]
                url_ = 'http://fwpt.csggzy.cn' + li.xpath('./p[1]/a/@href')[0]
                date_Today = li.xpath('./p[2]/text()')[0]
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

    # 长治市公共资源交易中心
    def jilin(self):
        print('长治市公共资源交易中心', 'http://ggzy.changzhi.gov.cn')
        url_list = [
            # 工程建设
            'http://ggzy.changzhi.gov.cn/jyxxJsgc/index_{}.htm',
            # 政府采购
            'http://ggzy.changzhi.gov.cn/jyxxZfcg/index_{}.htm',
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
            detail = html.xpath('//*[@id="main"]/div/div[4]/ul[2]/li')
            for li in detail:
                title = li.xpath('./a/@title')[0]
                url_ = 'http://ggzy.changzhi.gov.cn' + li.xpath('./a/@href')[0]
                url_ = re.findall('http.*?htm', url_)[0]
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

    # 朝阳市公共资源交易信息网 
    def jilinzf(self):
        print('朝阳市公共资源交易信息网', 'http://218.60.2.98')
        url_list = [
            # 建设工程
            'http://218.60.2.98/EpointWebBuilder/rest/frontAppCustomAction/getPageInfoListNew?' \
            'params= {"siteGuid":"abd5e1e1-ba0a-46d2-8af8-34b45279d94b","categoryNum":"003001","kw":"","pageIndex":%s,"pageSize":16}',
            # 政府采购
            'http://218.60.2.98/EpointWebBuilder/rest/frontAppCustomAction/getPageInfoListNew?' \
              'params= {"siteGuid":"abd5e1e1-ba0a-46d2-8af8-34b45279d94b","categoryNum":"003002","kw":"","pageIndex":%s,"pageSize":16}'
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
            code = str(page - 1)
            data = {}
            text = tool.requests_post_to(url % code, data, headers)
            detail = json.loads(text)['custom']['infodata']
            for li in detail:
                title = li['title'].replace("<font color='#0066FF'>", '').replace("</font>", '')
                if 'http' in li['infourl']:
                    continue
                url_ = 'http://218.60.2.98' + li['infourl']
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

    # 郴州市公共资源交易平台
    def jiayuguan(self):
        print('郴州市公共资源交易平台', 'http://czggzy.czs.gov.cn')
        url_list = [
            # 市本级
            #   工程建设
            #       招标公告
            'http://czggzy.czs.gov.cn/18360/18370/18371/18382/index.htm',
            #       招标信息
            'http://czggzy.czs.gov.cn/18360/18370/18371/18388/index.htm',
            #       中标公示
            'http://czggzy.czs.gov.cn/18360/18370/18371/18392/index.htm',
            #   政府采购
            #       采购公告
            'http://czggzy.czs.gov.cn/18360/18370/18372/18396/index.htm',
            #       结果公示
            'http://czggzy.czs.gov.cn/18360/18370/18372/18406/index.htm',
            #       更正答疑
            'http://czggzy.czs.gov.cn/18360/18370/18372/18409/index.htm'
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
            html = HTML(text)
            detail = html.xpath('//*[@class="left_list col-md-9"]/ul')
            for i in detail:
                for li in i.xpath('./li'):
                    title = li.xpath('./a/@title')[0]
                    url_ = url.replace('index.htm', li.xpath('./a/@href')[0])
                    date_Today = li.xpath('./span/text()')[0]
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
                            break
            url = url_list.pop(0)

    # 楚雄州公共资源交易平台
    def sichuan(self):
        print('楚雄州公共资源交易平台', 'http://www.cxggzy.cn')
        url_list = [
            # 市本级
            #   工程建设
            #       招标公告
            ['http://www.cxggzy.cn/jyxx/jsgcZbgg?currentPage={}','//*[@id="zbggForm"]/div[3]/table/tr'],
            #       变更公告
            ['http://www.cxggzy.cn/jyxx/jsgcBgtz?currentPage={}','//*[@id="bgtzForm"]/div[2]/table/tr'],
            #       评标结果公示
            ['http://www.cxggzy.cn/jyxx/jsgcpbjggs?currentPage={}','//*[@id="zbggForm"]/div[2]/table/tr'],
            #       中标结果
            ['http://www.cxggzy.cn/jyxx/jsgcZbjggs?currentPage={}','//*[@id="zbggForm"]/div[3]/table/tr'],
            #       异常公告
            ['http://www.cxggzy.cn/jyxx/jsgcZbyc?currentPage={}','//*[@id="ycggForm"]/div[2]/table/tr'],
            #   政府采购
            #       采购公告
            ['http://www.cxggzy.cn/jyxx/zfcg/cggg?currentPage={}','//*[@id="zbggForm"]/div[2]/table/tr'],
            #       变更通知
            ['http://www.cxggzy.cn/jyxx/zfcg/gzsx?currentPage={}','//*[@id="zbggForm"]/div[2]/table/tr'],
            #       结果公示
            ['http://www.cxggzy.cn/jyxx/zfcg/zbjggs?currentPage={}','//*[@id="zbggForm"]/div[2]/table/tr'],
            #       异常公示
            ['http://www.cxggzy.cn/jyxx/zfcg/zfcgYcgg?currentPage={}','//*[@id="ycggForm"]/div[2]/table/tr']
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
                    url_ = 'http://www.cxggzy.cn' + html.xpath(url[1] + '[{}]/td[3]/a/@href'.format(i + 1))[0]
                    date_Today = html.xpath(url[1] + '[{}]/td[4]/text()'.format(i + 1))[0]
                    if '招标' in date_Today or '采购' in date_Today:
                        date_Today = html.xpath(url[1] + '[{}]/td[5]/text()'.format(i + 1))[0]
                    if title == '':
                        title = html.xpath(url[1] + '[{}]/td[3]/@title'.format(i + 1))[0]
                except:
                    title = html.xpath(url[1] + '[{}]/td[4]/a/@title'.format(i + 1))[0]
                    url_ = 'http://www.cxggzy.cn' + html.xpath(url[1] + '[{}]/td[4]/a/@href'.format(i + 1))[0]
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

    # 大理州公共资源交易平台
    def weihai(self):
        print('大理州公共资源交易平台', 'https://www.dlggzy.cn')
        url_list = [
            # 市本级
            #   工程建设
            #       招标公告
            ['https://www.dlggzy.cn/jyxx/jsgcZbgg?currentPage={}','//*[@id="zbggForm"]/div[3]/table/tr'],
            #       变更公告
            ['https://www.dlggzy.cn/jyxx/jsgcBgtz?currentPage={}','//*[@id="bgtzForm"]/div[2]/table/tr'],
            #       评标结果公示
            ['https://www.dlggzy.cn/jyxx/jsgcpbjggs?currentPage={}','//*[@id="zbggForm"]/div[2]/table/tr'],
            #       中标结果
            ['https://www.dlggzy.cn/jyxx/jsgcZbjggs?currentPage={}','//*[@id="zbggForm"]/div[3]/table/tr'],
            #       异常公告
            ['https://www.dlggzy.cn/jyxx/jsgcZbyc?currentPage={}','//*[@id="ycggForm"]/div[2]/table/tr'],
            #   政府采购
            #       采购公告
            ['https://www.dlggzy.cn/jyxx/zfcg/cggg?currentPage={}','//*[@id="zbggForm"]/div[2]/table/tr'],
            #       变更通知
            ['https://www.dlggzy.cn/jyxx/zfcg/gzsx?currentPage={}','//*[@id="zbggForm"]/div[2]/table/tr'],
            #       结果公示
            ['https://www.dlggzy.cn/jyxx/zfcg/zbjggs?currentPage={}','//*[@id="zbggForm"]/div[2]/table/tr'],
            #       异常公示
            ['https://www.dlggzy.cn/jyxx/zfcg/zfcgYcgg?currentPage={}','//*[@id="ycggForm"]/div[2]/table/tr']
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
            text = tool.requests_get(url[0].format(page), headers)
            html = HTML(text)
            detail = html.xpath(url[1])
            for i in range(1, len(detail)):
                try:
                    title = html.xpath(url[1] + '[{}]/td[3]/a/@title'.format(i + 1))[0]
                    url_ = 'https://www.dlggzy.cn' + html.xpath(url[1] + '[{}]/td[3]/a/@href'.format(i + 1))[0]
                    date_Today = html.xpath(url[1] + '[{}]/td[4]/text()'.format(i + 1))[0]
                    if '招标' in date_Today or '采购' in date_Today:
                        date_Today = html.xpath(url[1] + '[{}]/td[5]/text()'.format(i + 1))[0]
                    if title == '':
                        title = html.xpath(url[1] + '[{}]/td[3]/@title'.format(i + 1))[0]
                except:
                    title = html.xpath(url[1] + '[{}]/td[4]/a/@title'.format(i + 1))[0]
                    url_ = 'https://www.dlggzy.cn' + html.xpath(url[1] + '[{}]/td[4]/a/@href'.format(i + 1))[0]
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

    # 大连市公共资源交易平台
    def anhui(self):
        print('大连市公共资源交易平台', 'http://ggzyjy.dl.gov.cn')
        url_list = [
            # 建设工程
                # 招标公告
            'http://ggzyjy.dl.gov.cn/TPFront/jyxx/071001/071001001/?pageing={}',
                # 中标公示
            'http://ggzyjy.dl.gov.cn/TPFront/jyxx/071001/071001002/?pageing={}',
                # 中标结果
            'http://ggzyjy.dl.gov.cn/TPFront/jyxx/071001/071001003/?pageing={}',
            # 政府采购
                # 采购公告
            'http://ggzyjy.dl.gov.cn/TPFront/jyxx/071002/071002001/?pageing={}',
                # 中标通知
            'http://ggzyjy.dl.gov.cn/TPFront/jyxx/071002/071002003/?pageing={}',
                # 单一来源
            'http://ggzyjy.dl.gov.cn/TPFront/jyxx/071002/071002005/?pageing={}'
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
            detail = html.xpath('/html/body/table/tbody/tr')
            for li in detail:
                title = li.xpath('./td[2]/a/text()')[0]
                url_ = 'http://ggzyjy.dl.gov.cn' + li.xpath('./td[2]/a/@href')[0]
                date_Today = li.xpath('./td[4]/text()')[0].replace('\r', '').replace('\t', '').replace('\n', '') \
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

    # 丹东市公共资源交易平台
    def yichun(self):
        print('丹东市公共资源交易平台', 'http://218.61.232.162')
        url_list = [
            # 建设工程
                # 招标公告
            'http://218.61.232.162/ddggzy/jyxx/002002/002002001/{}.html',
                # 中标公示
            'http://218.61.232.162/ddggzy/jyxx/002002/002002002/{}.html',
                # 中标结果
            'http://218.61.232.162/ddggzy/jyxx/002002/002002003/{}.html',
            # 政府采购
                # 采购公告
            'http://218.61.232.162/ddggzy/jyxx/002001/002001001/{}.html',
            'http://218.61.232.162/ddggzy/jyxx/002001/002001002/{}.html',
                # 中标通知
            'http://218.61.232.162/ddggzy/jyxx/002001/002001005/{}.html'
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
            if page == 1:
                text = tool.requests_get(url.format('tradetab'), headers)
            html = HTML(text)
            detail = html.xpath('/html/body/div/ul/li')
            for li in detail:
                title = li.xpath('string(./a)').replace('\r', '').replace('\t', '').replace('\n', '') \
                    .replace(' ', '')
                url_ = 'http://218.61.232.162' + li.xpath('./a/@href')[0]
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

    # 大同市公共资源交易中心
    def suqian(self):
        print('大同市公共资源交易中心', 'http://ggzyjy.dt.gov.cn')
        url_list = [
            'http://ggzyjy.dt.gov.cn/zyjyPortal/portal/noticelist?category=%E6%94%BF%E5%BA%9C%E9%87%87%E8%B4%AD&type=&other=&title=&page={}&rows=10'
                         ]
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36',
        }
        url = url_list.pop(0)
        page = 0
        ls = []
        while True:
            page += 1
            text = tool.requests_get(url, headers)
            detail = json.loads(text)['rows']
            for li in detail:
                title = li['title']
                url_ = 'http://ggzyjy.dt.gov.cn/zyjyPortal/portal/tradeEdit?id=' + li['id']
                date_Today = li['noticeSendTime'][:10]
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

    # 德宏州公共资源交易平台
    def bazhong(self):
        print('德宏州公共资源交易平台', 'https://jyzx.dh.gov.cn')
        url_list = [
            # 市本级
            #   工程建设
            #       招标公告
            ['https://jyzx.dh.gov.cn/jyxx/jsgcZbgg?currentPage={}','//*[@id="zbggForm"]/div[3]/table/tr'],
            #       变更公告
            ['https://jyzx.dh.gov.cn/jyxx/jsgcBgtz?currentPage={}','//*[@id="bgtzForm"]/div[2]/table/tr'],
            #       评标结果公示
            ['https://jyzx.dh.gov.cn/jyxx/jsgcpbjggs?currentPage={}','//*[@id="zbggForm"]/div[2]/table/tr'],
            #       中标结果
            ['https://jyzx.dh.gov.cn/jyxx/jsgcZbjggs?currentPage={}','//*[@id="zbggForm"]/div[3]/table/tr'],
            #       异常公告
            ['https://jyzx.dh.gov.cn/jyxx/jsgcZbyc?currentPage={}','//*[@id="ycggForm"]/div[2]/table/tr'],
            #   政府采购
            #       采购公告
            ['https://jyzx.dh.gov.cn/jyxx/zfcg/cggg?currentPage={}','//*[@id="zbggForm"]/div[2]/table/tr'],
            #       变更通知
            ['https://jyzx.dh.gov.cn/jyxx/zfcg/gzsx?currentPage={}','//*[@id="zbggForm"]/div[2]/table/tr'],
            #       结果公示
            ['https://jyzx.dh.gov.cn/jyxx/zfcg/zbjggs?currentPage={}','//*[@id="zbggForm"]/div[2]/table/tr'],
            #       异常公示
            ['https://jyzx.dh.gov.cn/jyxx/zfcg/zfcgYcgg?currentPage={}','//*[@id="ycggForm"]/div[2]/table/tr']
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
            if page == 20:
                print('日期不符, 正在切换类型')
                url = url_list.pop(0)
                page = 0
            text = tool.requests_get(url[0].format(page), headers)
            html = HTML(text)
            detail = html.xpath(url[1])
            for i in range(1, len(detail)):
                try:
                    title = html.xpath(url[1] + '[{}]/td[3]/a/@title'.format(i + 1))[0]
                    url_ = 'https://jyzx.dh.gov.cn' + html.xpath(url[1] + '[{}]/td[3]/a/@href'.format(i + 1))[0]
                    date_Today = html.xpath(url[1] + '[{}]/td[4]/text()'.format(i + 1))[0]
                    if '招标' in date_Today or '采购' in date_Today:
                        date_Today = html.xpath(url[1] + '[{}]/td[5]/text()'.format(i + 1))[0]
                    if title == '':
                        title = html.xpath(url[1] + '[{}]/td[3]/@title'.format(i + 1))[0]
                except:
                    title = html.xpath(url[1] + '[{}]/td[4]/a/@title'.format(i + 1))[0]
                    url_ = 'https://jyzx.dh.gov.cn' + html.xpath(url[1] + '[{}]/td[4]/a/@href'.format(i + 1))[0]
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

    # 迪庆州公共资源交易平台
    def changzhou(self):
        print('迪庆州公共资源交易平台', 'http://183.224.249.60:8001')
        url_list = [
            # 市本级
            #   工程建设
            #       招标公告
            ['http://183.224.249.60:8001/jyxx/jsgcZbgg?currentPage={}','//*[@id="zbggForm"]/div[3]/table/tr'],
            #       变更公告
            ['http://183.224.249.60:8001/jyxx/jsgcBgtz?currentPage={}','//*[@id="bgtzForm"]/div[2]/table/tr'],
            #       评标结果公示
            ['http://183.224.249.60:8001/jyxx/jsgcpbjggs?currentPage={}','//*[@id="zbggForm"]/div[2]/table/tr'],
            #       中标结果
            ['http://183.224.249.60:8001/jyxx/jsgcZbjggs?currentPage={}','//*[@id="zbggForm"]/div[3]/table/tr'],
            #       异常公告
            ['http://183.224.249.60:8001/jyxx/jsgcZbyc?currentPage={}','//*[@id="ycggForm"]/div[2]/table/tr'],
            #   政府采购
            #       采购公告
            ['http://183.224.249.60:8001/jyxx/zfcg/cggg?currentPage={}','//*[@id="zbggForm"]/div[2]/table/tr'],
            #       变更通知
            ['http://183.224.249.60:8001/jyxx/zfcg/gzsx?currentPage={}','//*[@id="zbggForm"]/div[2]/table/tr'],
            #       结果公示
            ['http://183.224.249.60:8001/jyxx/zfcg/zbjggs?currentPage={}','//*[@id="zbggForm"]/div[2]/table/tr'],
            #       异常公示
            ['http://183.224.249.60:8001/jyxx/zfcg/zfcgYcgg?currentPage={}','//*[@id="ycggForm"]/div[2]/table/tr']
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
            if page == 20:
                print('日期不符, 正在切换类型', date_Today)
                url = url_list.pop(0)
                page = 0
            text = tool.requests_get(url[0].format(page), headers)
            html = HTML(text)
            detail = html.xpath(url[1])
            for i in range(1, len(detail)):
                try:
                    title = html.xpath(url[1] + '[{}]/td[3]/a/@title'.format(i + 1))[0]
                    url_ = 'http://183.224.249.60:8001' + html.xpath(url[1] + '[{}]/td[3]/a/@href'.format(i + 1))[0]
                    date_Today = html.xpath(url[1] + '[{}]/td[4]/text()'.format(i + 1))[0]
                    if '招标' in date_Today or '采购' in date_Today:
                        date_Today = html.xpath(url[1] + '[{}]/td[5]/text()'.format(i + 1))[0]
                    if title == '':
                        title = html.xpath(url[1] + '[{}]/td[3]/@title'.format(i + 1))[0]
                except:
                    title = html.xpath(url[1] + '[{}]/td[4]/a/@title'.format(i + 1))[0]
                    url_ = 'http://183.224.249.60:8001' + html.xpath(url[1] + '[{}]/td[4]/a/@href'.format(i + 1))[0]
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

    # 鄂州市公共资源交易平台
    def guangdong(self):
        print('鄂州市公共资源交易平台', 'http://www.ezggzy.cn')
        url_list_to = [
            # 市本级
            #   工程建设
            #       招标公告
            'http://www.ezggzy.cn/jiaoyixinxi/queryJiaoYiXinXiPagination.do?bianHao=&gongChengLeiBie=&gongChengType=&gongShiType=10&page={}&rows=15&title=&type=10',
            #       评标结果
            'http://www.ezggzy.cn/jiaoyixinxi/queryJiaoYiXinXiPagination.do?bianHao=&gongChengLeiBie=&gongChengType=&gongShiType=180&page={}&rows=15&title=&type=10',
            #       中标结果
            'http://www.ezggzy.cn/jiaoyixinxi/queryJiaoYiXinXiPagination.do?bianHao=&gongChengLeiBie=&gongChengType=&gongShiType=50&page={}&rows=15&title=&type=10',
            #       变更公告
            'http://www.ezggzy.cn/jiaoyixinxi/queryJiaoYiXinXiPagination.do?bianHao=&gongChengLeiBie=&gongChengType=&gongShiType=130&page={}&rows=15&title=&type=10',
            #   政府采购
            #       采购公告
            'http://www.ezggzy.cn/jiaoyixinxi/queryJiaoYiXinXiPagination.do?bianHao=&gongChengLeiBie=&gongChengType=&gongShiType=70&page={}&rows=15&title=&type=20',
            #       中标公告
            'http://www.ezggzy.cn/jiaoyixinxi/queryJiaoYiXinXiPagination.do?bianHao=&gongChengLeiBie=&gongChengType=&gongShiType=50&page={}&rows=15&title=&type=20',
            #       变更公告
            'http://www.ezggzy.cn/jiaoyixinxi/queryJiaoYiXinXiPagination.do?bianHao=&gongChengLeiBie=&gongChengType=&gongShiType=130&page={}&rows=15&title=&type=20',
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
            text = json.loads(text)['rows']
            for li in text:
                title = li['title']
                if li['gongShiTypeText'] == '招标公告':
                    url_ = 'http://www.ezggzy.cn/jyw/jyw/showGongGao.do?ggGuid=' + li['yuanXiTongId']
                elif li['gongShiTypeText'] == '中标候选人公示':
                    url_ = 'http://www.ezggzy.cn/jiaoyixingxi/pbjg_view.html?guid=' + li['yuanXiTongId']
                elif li['gongShiTypeText'] == '中标公示':
                    url_ = 'http://www.ezggzy.cn/jiaoyixingxi/zbgs_view.html?guid=' + li['yuanXiTongId']
                elif li['gongShiTypeText'] == '失败公告':
                    url_ = 'http://www.ezggzy.cn/jiaoyixingxi/ycxx_view.html?guid=' + li['yuanXiTongId']
                date_Today = li['faBuShortTimeText'].replace('\n', '').replace('\r', '') \
                    .replace('\t', '').replace(' ', '').replace('[', '').replace(']', '')
                code = li['gongShiTypeText']
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

    # 阜新市公共资源交易网
    def guangdongzf(self):
        print('阜新市公共资源交易网', 'http://ggzy.fuxin.gov.cn')
        url_list = [
            # 建设工程
            'http://ggzy.fuxin.gov.cn/jsgc/{}.html',
            # 政府采购
            'http://ggzy.fuxin.gov.cn/zfcg/{}.html'
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
            if '503 Service Unavailable' in text:
                break
            html = HTML(text)
            detail = html.xpath('/html/body/div[2]/div[2]/div[2]/ul/li')
            for li in detail:
                title = li.xpath('./a/@title')[0]
                url_ = 'http://ggzy.fuxin.gov.cn' + li.xpath('./a/@href')[0]
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

    # 广西公共资源网
    def guangyuan(self):
        print('广西公共资源网', 'http://gxggzy.gxzf.gov.cn')
        url_list = [
            'http://gxggzy.gxzf.gov.cn/igs/front/search/list.html?&filter%5BDOCTITLE%5D=&pageNumber={}&pageSize=10&index=gxggzy_jyfw&type=jyfw&filter%5Bparentparentid%5D=&filter%5Bparentchnldesc%5D=&filter%5Bchnldesc%5D=&filter%5BSITEID%5D=234&orderProperty=PUBDATE&orderDirection=desc&filter%5BAVAILABLE%5D=true'
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
            detail = json.loads(text)['page']['content']
            for li in detail:
                title = li['DOCTITLE']
                url_ = li['DOCPUBURL']
                date_Today = li['PUBDATE'][:10].replace('\n', '').replace('\t', '').replace('\r', '') \
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

    # 贵州省招标投标公共服务平台
    def guangan(self):
        print('贵州省招标投标公共服务平台', 'http://ztb.guizhou.gov.cn')
        url_list = [
            'http://ztb.guizhou.gov.cn/api/trade/search?pubDate=all&region=5200&industry=all&prjType=all&noticeType=all&noticeClassify=all&pageIndex={}&args='
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
            text = json.loads(tool.requests_get(url.format(page), headers))
            detail = text['data']
            for li in detail:
                title = li['Title']
                url_ = 'http://ztb.guizhou.gov.cn/api/trade/' + str(li['Id'])
                date_Today = li['PubDate']
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

    # 鹤壁市公共资源交易平台
    def qingyang(self):
        print('鹤壁市公共资源交易平台', 'http://ggzy.hebi.gov.cn')
        url_list = [
            # 建设工程
                # 招标公告
            'http://ggzy.hebi.gov.cn/TPFront/gcjs/013001/?Paging={}',
                # 变更公示
            'http://ggzy.hebi.gov.cn/TPFront/gcjs/013002/?Paging={}',
                # 中标候选人
            'http://ggzy.hebi.gov.cn/TPFront/gcjs/013003/?Paging={}',
                # 中标结果
            'http://ggzy.hebi.gov.cn/TPFront/gcjs/013004/?Paging={}',
            # 政府采购
                # 采购公告
            'http://ggzy.hebi.gov.cn/TPFront/zfcg/014002/?Paging={}',
                # 变更公告
            'http://ggzy.hebi.gov.cn/TPFront/zfcg/014003/?Paging={}',
                # 结果公告
            'http://ggzy.hebi.gov.cn/TPFront/zfcg/014004/?Paging={}'
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
            if page == 20:
                print('日期不符, 正在切换类型...')
                url = url_list.pop(0)
                page = 0
            text = tool.requests_get(url.format(page), headers)
            html = HTML(text)
            detail = html.xpath('/html/body/table[5]/tr/td[3]/table/tr[3]/td/table/tr')
            for li in detail:
                try:
                    title = li.xpath('./td[2]/a/@title')[0]
                    url_ = 'http://ggzy.hebi.gov.cn' + li.xpath('./td[2]/a/@href')[0]
                    date_Today = li.xpath('./td[4]/text()')[0].replace('[', '').replace(']', '')
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

    # 河北招投标公共服务平台
    def zhangye(self):
        print('河北招投标公共服务平台', 'http://www.hebeieb.com')
        url_list = [
            # 建设工程
            # 招标公告
            'http://www.hebeieb.com/tender/xxgk/zbgg.do',
            # 变更公告
            'http://www.hebeieb.com/tender/xxgk/bggg.do',
            # 中标候选人
            'http://www.hebeieb.com/tender/xxgk/pbgs.do',
            # 中标结果
            'http://www.hebeieb.com/tender/xxgk/zhongbgg.do'
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
        data = {
            "page": '',
            "TimeStr": '',
            "allDq": "reset2",
            "allHy": "reset1",
            "AllPtName": '',
            "KeyStr": '',
            "KeyType": "ggname"
        }
        while True:
            if page == 0:
                data['page'] = ''
            else:
                data['page'] = str(page)
            page += 1
            text = tool.requests_post(url, data, headers)
            text = '<div class="AAA">' + text + '</div>'
            html = HTML(text)
            detail = html.xpath('//div[@class="AAA"]/div')
            for li in range(1, len(detail)):
                title = html.xpath('//div[@class="AAA"]/div[{}]/div/h4/a/@title'.format(li + 1))[0]
                url_ = 'http://www.hebeieb.com' + \
                      html.xpath('//div[@class="AAA"]/div[{}]/div/h4/a/@href'.format(li + 1))[0]
                categoryid = re.findall('categoryid=(.*?)&', url_)[0]
                infoid = re.findall('infoid=(.*?)&', url_)[0]
                url_ = 'http://www.hebeieb.com/infogk/newDetail.do?categoryid={}&infoid={}&laiyuan=[%E5%B9%B3%E5%8F%B0%E5%86%85]'.format(
                    categoryid, infoid)
                date_Today = html.xpath('//div[@class="AAA"]/div[{}]/div/h4/span/text()'.format(li + 1))[0].replace(
                    '\n', '').replace('\t', '').replace('\r', '') \
                    .replace(' ', '')
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

    # 河北交通招投标公共服务平台  网站打不开
    def xuzhou(self):
        print('河北交通招投标公共服务平台', 'http://ztbzx.hbsjtt.gov.cn')
        url_list = [
            # 建设工程
            # 招标公告
            'http://ztbzx.hbsjtt.gov.cn/Site/list.aspx?type=gg',
            # 中标结果
            'http://ztbzx.hbsjtt.gov.cn/Site/list.aspx?type=gs'
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
            "__VIEWSTATE": '',
            "__VIEWSTATEGENERATOR": '9C511D21',
            "__EVENTTARGET": "ctl00$ContentPlaceHolder1$AspNetPager1",
            "__EVENTARGUMENT": "2",
            "__EVENTVALIDATION": '',
            "ctl00$ContentPlaceHolder1$txtKeyWord": '',
            "ctl00$ContentPlaceHolder1$AspNetPager1_input": "1"
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
            data['ctl00$ContentPlaceHolder1$AspNetPager1_input'] = str(page - 1)
            data['__EVENTVALIDATION'] = html.xpath('//*[@id="__EVENTVALIDATION"]/@value')[0]
            detail = html.xpath('//div[@class="main_list"]/ul/li')
            for li in detail:
                title = li.xpath('./a/@title')[0]
                url_ = 'http://ztbzx.hbsjtt.gov.cn' + li.xpath('./a/@href')[0]
                date_Today = li.xpath('./span/text()')[0].replace('\n', '').replace('\t', '').replace('\r', '') \
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

    # 河南省电子招投标
    def dezhou(self):
        print('河南省电子招投标', 'http://hndzzbtb.hndrc.gov.cn')
        url_list = [
            'http://hndzzbtb.hndrc.gov.cn/services/hl/getSelect?response=application/json&pageIndex={}&pageSize=22&'
            'day=&sheng=x1&qu=&xian=&title=&timestart=&timeend=&categorynum=002001001&siteguid=3955b792-fb32-4dc1-8935-49ad516ae6db',
            'http://hndzzbtb.hndrc.gov.cn/services/hl/getSelect?response=application/json&pageIndex={}&pageSize=22'
            '&day=&sheng=x1&qu=&xian=&title=&timestart=&timeend=&categorynum=002002001&siteguid=3955b792-fb32-4dc1-8935-49ad516ae6db'
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
                title = li['title']
                url_ = 'http://hndzzbtb.hndrc.gov.cn' + li['href']
                date_Today = li['infodate'].replace('\n', '').replace('\t', '').replace('\r', '') \
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

    # 衡州市公共资源交易平台   网站打不开
    def chengdu(self):
        print('衡州市公共资源交易平台', 'http://www.qzggzy.com')
        url_list = [
            # 工程建设
            # 招标公告
            'http://www.qzggzy.com/jyxx/002001/002001001/{}.html',
            # 变更
            'http://www.qzggzy.com/jyxx/002001/002001002/{}.html',
            # 开标结果
            'http://www.qzggzy.com/jyxx/002001/002001003/{}.html',
            # 中标候选人
            'http://www.qzggzy.com/jyxx/002001/002001004/{}.html',
            # 中标结果
            'http://www.qzggzy.com/jyxx/002001/002001005/{}.html',
            # 政府采购
            # 采购公告
            'http://www.qzggzy.com/jyxx/002002/002002001/{}.html',
            # 结果公告
            'http://www.qzggzy.com/jyxx/002002/002002002/{}.html',
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
            if page == 1:
                text = tool.requests_get(url.format('trade'), headers)

            html = HTML(text)
            detail = html.xpath('/html/body/div[2]/div/div[2]/div/div[2]/ul/li')
            for li in detail:
                title = li.xpath('string(./div/a)').replace(' ', '').replace('\n', '').replace('\r', '').replace('\t',
                                                                                                                 '')
                url_ = 'http://www.qzggzy.com' + li.xpath('./div/a/@href')[0]
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

    # 红河州公共资源交易平台
    def yangzhou(self):
        print('红河州公共资源交易平台', 'https://www.hhzy.net')
        url_list = [
            # 市本级
            #   工程建设
            #       招标公告
            ['https://www.hhzy.net/jyxx/jsgcZbgg?currentPage={}','//*[@id="zbggForm"]/div[3]/table/tr'],
            #       变更公告
            ['https://www.hhzy.net/jyxx/jsgcBgtz?currentPage={}','//*[@id="bgtzForm"]/div[2]/table/tr'],
            #       评标结果公示
            ['https://www.hhzy.net/jyxx/jsgcpbjggs?currentPage={}','//*[@id="zbggForm"]/div[2]/table/tr'],
            #       中标结果
            ['https://www.hhzy.net/jyxx/jsgcZbjggs?currentPage={}','//*[@id="zbggForm"]/div[3]/table/tr'],
            #       异常公告
            ['https://www.hhzy.net/jyxx/jsgcZbyc?currentPage={}','//*[@id="ycggForm"]/div[2]/table/tr'],
            #   政府采购
            #       采购公告
            ['https://www.hhzy.net/jyxx/zfcg/cggg?currentPage={}','//*[@id="zbggForm"]/div[2]/table/tr'],
            #       变更通知
            ['https://www.hhzy.net/jyxx/zfcg/gzsx?currentPage={}','//*[@id="zbggForm"]/div[2]/table/tr'],
            #       结果公示
            ['https://www.hhzy.net/jyxx/zfcg/zbjggs?currentPage={}','//*[@id="zbggForm"]/div[2]/table/tr'],
            #       异常公示
            ['https://www.hhzy.net/jyxx/zfcg/zfcgYcgg?currentPage={}','//*[@id="ycggForm"]/div[2]/table/tr']
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
            text = tool.requests_get(url[0].format(page), headers)
            html = HTML(text)
            detail = html.xpath(url[1])
            for i in range(1, len(detail)):
                try:
                    title = html.xpath(url[1] + '[{}]/td[3]/a/@title'.format(i + 1))[0]
                    url_ = 'https://www.hhzy.net' + html.xpath(url[1] + '[{}]/td[3]/a/@href'.format(i + 1))[0]
                    date_Today = html.xpath(url[1] + '[{}]/td[4]/text()'.format(i + 1))[0]
                    if '招标' in date_Today or '采购' in date_Today:
                        date_Today = html.xpath(url[1] + '[{}]/td[5]/text()'.format(i + 1))[0]
                    if title == '':
                        title = html.xpath(url[1] + '[{}]/td[3]/@title'.format(i + 1))[0]
                except:
                    title = html.xpath(url[1] + '[{}]/td[4]/a/@title'.format(i + 1))[0]
                    url_ = 'https://www.hhzy.net' + html.xpath(url[1] + '[{}]/td[4]/a/@href'.format(i + 1))[0]
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

    # 怀化市公共资源交易平台
    def panzhihua(self):
        print('怀化市公共资源交易平台', 'http://ggzy.huaihua.gov.cn')
        url_list = [
            # 市本级
            #   工程建设
            #       招标公告
            'http://ggzy.huaihua.gov.cn/ggzyjyzx/c116108/{}.shtml',
            #       中标公示
            'http://ggzy.huaihua.gov.cn/ggzyjyzx/c116109/{}.shtml',
            #       更正公告
            'http://ggzy.huaihua.gov.cn/ggzyjyzx/c116110/{}.shtml',
            #       流标公告
            'http://ggzy.huaihua.gov.cn/ggzyjyzx/c116111/{}.shtml',
            #   政府采购
            #       采购公告
            'http://ggzy.huaihua.gov.cn/ggzyjyzx/c116112/{}.shtml',
            #       中标公告
            'http://ggzy.huaihua.gov.cn/ggzyjyzx/c116113/{}.shtml',
            #       更正公告
            'http://ggzy.huaihua.gov.cn/ggzyjyzx/c116114/{}.shtml',
            #       流标公告
            'http://ggzy.huaihua.gov.cn/ggzyjyzx/c116115/{}.shtml'
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
                text = tool.requests_get(url.format('list'), headers)
            else:
                text = tool.requests_get(url.format('list_' + str(page)), headers)
            html = HTML(text)
            detail = html.xpath('//*[@class="j-right-list-box"]/ul/li')
            for li in detail:
                title = li.xpath('./a/text()')[0].replace('\n', '').replace('\r', '').replace('\t', '').replace(' ', '')
                url_ = 'http://ggzy.huaihua.gov.cn' + li.xpath('./a/@href')[0]
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

    # 葫芦岛市公共资源交易网
    def xinyu(self):
        print('葫芦岛市公共资源交易网', 'http://www.hldggzyjyzx.com.cn')
        url_list = [
            # 建设工程
                # 招标公告
            'http://www.hldggzyjyzx.com.cn/jyxx/003001/003001001/{}.html',
                # 中标公示
            # 'http://www.hldggzyjyzx.com.cn/jyxx/003001/003001003/{}.html',
                # 中标结果
            'http://www.hldggzyjyzx.com.cn/jyxx/003001/003001004/{}.html',
            # 政府采购
                # 招标公告
            'http://www.hldggzyjyzx.com.cn/jyxx/003002/003002001/{}.html',
                # 更正
            'http://www.hldggzyjyzx.com.cn/jyxx/003002/003002002/{}.html',
                # 中标公示
            'http://www.hldggzyjyzx.com.cn/jyxx/003002/003002003/{}.html'
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
            if page == 1:
                text = tool.requests_get(url.format('thirdpage'), headers)
            else:
                text = tool.requests_get(url.format(page), headers)
            html = HTML(text)
            detail = html.xpath('/html/body/div[3]/div/div/div[2]/div/div[2]/ul/li')
            for li in detail:
                title = li.xpath('./div/a/text()')[0]
                url_ = 'http://www.hldggzyjyzx.com.cn' + \
                      li.xpath('./div/a/@href')[0]
                date_Today = li.xpath('./div/a/@href')[0][1:].split('/')[3]
                date_Today = date_Today[:4] + '-' + date_Today[4:6] + '-' + date_Today[6:]
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

    # 嘉兴市公共资源交易平台
    def wuxi(self):
        print('嘉兴市公共资源交易平台', 'http://www.jxzbtb.cn')
        url_list = [
            # 建设工程
            'http://www.jxzbtb.cn/jygg/003001/{}.html',
            # 政府采购
            'http://www.jxzbtb.cn/jygg/003002/{}.html'
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
            detail = html.xpath('/html/body/div[2]/div/div[2]/div/div[2]/ul/li')
            for li in detail:
                title = li.xpath('./div/a/@title')[0]
                url_ = 'http://www.jxzbtb.cn' + li.xpath('./div/a/@href')[0]
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

    # 吉林市公共资源交易网
    def rizhao(self):
        print('吉林市公共资源交易网', 'http://www.jlsggzyjy.gov.cn')
        url_list = ['http://www.jlsggzyjy.gov.cn/jlsztb/jyxx/003001/003001001/003001001001/?pageing={}',
                    # 变更
                    'http://www.jlsggzyjy.gov.cn/jlsztb/jyxx/003001/003001002/003001002001/?pageing={}',
                    # 中标
                    'http://www.jlsggzyjy.gov.cn/jlsztb/jyxx/003001/003001004/003001004001/?pageing={}',
                    # 候选人
                    'http://www.jlsggzyjy.gov.cn/jlsztb/jyxx/003001/003001003/003001003001/?pageing={}',
                    # 合同
                    'http://www.jlsggzyjy.gov.cn/jlsztb/jyxx/003001/003001005/003001005001/?pageing={}',
                    # 政府采购 # 招标
                    'http://www.jlsggzyjy.gov.cn/jlsztb/jyxx/003002/003002001/003002001001/?pageing={}',
                    # 变更
                    'http://www.jlsggzyjy.gov.cn/jlsztb/jyxx/003002/003002002/003002002001/?pageing={}',
                    # 中标
                    'http://www.jlsggzyjy.gov.cn/jlsztb/jyxx/003002/003002003/003002003001/?pageing={}',
                    # 合同
                    'http://www.jlsggzyjy.gov.cn/jlsztb/jyxx/003002/003002004/003002004001/?pageing={}'
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
            for li in html.xpath('//*[@class="ewb-com-items"]/li'):
                title = li.xpath('./div/a/text()')[0]
                url_ = 'http://www.jlsggzyjy.gov.cn' + li.xpath('./div/a/@href')[0]
                date_Today = li.xpath('./span/text()')[0].replace('\n', '').replace('\r', '').replace('\t', '').replace(
                    ' ', '').replace('"', '')
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

    # 济南市公共资源交易平台
    def zaozhuang(self):
        print('济南市公共资源交易平台', 'http://jnggzy.jinan.gov.cn')
        url_list = [
            # 市本级
            #   工程建设
            #       招标公告
            'http://jnggzy.jinan.gov.cn/jnggzyztb/front/search.do?area=&type=0&xuanxiang=%E6%8B%9B%E6%A0%87%E5%85%AC%E5%91%8A&subheading=&pagenum={}',
            #       中标公示
            'http://jnggzy.jinan.gov.cn/jnggzyztb/front/search.do?area=&type=0&xuanxiang=%E4%B8%AD%E6%A0%87%E5%85%AC%E5%91%8A&subheading=&pagenum={}',
            #   政府采购
            #       采购公告
            'http://jnggzy.jinan.gov.cn/jnggzyztb/front/search.do?area=&type=1&xuanxiang=%E6%8B%9B%E6%A0%87%E5%85%AC%E5%91%8A&subheading=&pagenum={}',
            #       中标公告
            'http://jnggzy.jinan.gov.cn/jnggzyztb/front/search.do?area=&type=1&xuanxiang=%E4%B8%AD%E6%A0%87%E5%85%AC%E5%91%8A&subheading=&pagenum={}',
            #       变更公告
            'http://jnggzy.jinan.gov.cn/jnggzyztb/front/search.do?area=&type=1&xuanxiang=%E5%8F%98%E6%9B%B4%E5%85%AC%E5%91%8A&subheading=&pagenum={}',
            #       废标公示
            'http://jnggzy.jinan.gov.cn/jnggzyztb/front/search.do?area=&type=1&xuanxiang=%E5%BA%9F%E6%A0%87%E5%85%AC%E5%91%8A&subheading=&pagenum={}'
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
            text = json.loads(text)['params']['str']
            html = HTML(text)
            detail = html.xpath('//ul/li')
            for li in detail:
                title = li.xpath('./a/@title')[0]
                try:
                    url_ = 'http://jnggzy.jinan.gov.cn/jnggzyztb/front/showNotice.do?iid=' + li.xpath('./a/@onclick')[
                        0].replace("showview('",
                                   '').replace("',1)", '') + '&xuanxiang=' + \
                          re.findall('xuanxiang=(.*?)&subheading', self.url)[0] + '&isnew=1'
                except:
                    url_ = 'http://jnggzy.jinan.gov.cn' + li.xpath('./a/@href')[0]
                try:
                    date_Today = li.xpath('./span[2]/text()')[0].replace('\n', '').replace('\r', '') \
                        .replace('\t', '').replace(' ', '').replace('[', '').replace(']', '')
                except:
                    date_Today = li.xpath('./span[2]/span[2]/text()')[0].replace('\n', '').replace('\r', '') \
                        .replace('\t', '').replace(' ', '').replace('[', '').replace(']', '')
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

    # 晋城市公共资源交易信息网
    def jiangsu(self):
        print('晋城市公共资源交易信息网', 'http://www.jcggzyfw.cn')
        url_list = ['http://www.jcggzyfw.cn/jyxxgc/index_{}.jhtml',
                    'http://www.jcggzyfw.cn/jyxxzc/index_{}.jhtml']

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
            if page == 20:
                return
            detail = HTML(text).xpath('/html/body/div[2]/div/div[2]/div/div[4]/div[1]/a')
            for li in detail:
                title = li.xpath('./p[1]/text()')[0].replace('\n', '').replace('\t', '').replace(' ', '')
                url_ = 'http://www.jcggzyfw.cn' + li.xpath('./@href')[0]
                date_Today = li.xpath('./p[2]/span/text()')[1].replace('\n', '').replace('\t', '').replace(' ', '') \
                    .replace('/', '-')
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

    # 荆门市公共资源交易平台
    def jiangxi(self):
        print('荆门市公共资源交易平台', 'http://zyjy.jingmen.gov.cn')
        url_list = [
            'http://zyjy.jingmen.gov.cn/xxfb/{}.html'
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
                text = tool.requests_get(url.format('level'), headers)
            else:
                text = tool.requests_get(url.format(page), headers)
            html = HTML(text)
            detail = html.xpath('//*[@id="info"]/li')
            for li in detail:
                title = li.xpath('./a/@title')[0]
                url_ = 'http://zyjy.jingmen.gov.cn' + li.xpath('./a/@href')[0]
                date_Today = li.xpath('./a/span[2]/text()')[0]
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

    # 晋中市公共资源交易平台
    def taizhou(self):
        print('晋中市公共资源交易平台', 'http://ggzy.sxjz.gov.cn')
        url_list = [
            # 政府采购
            'http://ggzy.sxjz.gov.cn/jygkzfcg/index_{}.jhtml',
            # 工程建设
            'http://ggzy.sxjz.gov.cn/jygkjsgc/index_{}.jhtml'
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
            detail = html.xpath('/html/body/div/div[2]/div/div[2]/div[2]/div[2]/ul/li')
            for li in detail:
                title = li.xpath('string(./a/p)')
                url_ = li.xpath('./a/@href')[0]
                date_Today = li.xpath('./div/p[4]/text()')[0]
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

    # 锦州市公共资源交易平台
    def luzhou(self):
        print('锦州市公共资源交易平台', 'http://ggzy.jz.gov.cn')
        url_list = [
            'http://ggzy.jz.gov.cn/jyxx/{}.html',
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
            if page == 1:
                text = tool.requests_get(url.format('moreinfojy'), headers)
            html = HTML(text)
            detail = html.xpath('//*[@id="infolist"]/li')
            for li in detail:
                title = li.xpath('./div/a/@title')[0]
                url_ = 'http://ggzy.jz.gov.cn' + li.xpath('./div/a/@href')[0]
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

    # 开封市公共资源交易平台
    def jining(self):
        print('开封市公共资源交易平台', 'http://www.kfsggzyjyw.cn')
        url_list = [
            # 建设工程
                # 招标公告
            'http://www.kfsggzyjyw.cn/jzbgg/index_{}.jhtml',
                # 变更公示
            'http://www.kfsggzyjyw.cn/jbggg/index_{}.jhtml',
                # 中标结果
            'http://www.kfsggzyjyw.cn/jszbgg/index_{}.jhtml',
            # 政府采购
                # 采购公告
            'http://www.kfsggzyjyw.cn/zcggg/index_{}.jhtml',
                # 变更公告
            'http://www.kfsggzyjyw.cn/zbggg/index_{}.jhtml',
                # 结果公告
            'http://www.kfsggzyjyw.cn/zfzbgg/index_{}.jhtml'
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
        while True:
            page += 1
            text = tool.requests_get(url.format(page), headers)
            html = HTML(text)
            detail = html.xpath('/html/body/div/div/div[12]/div[2]/div/div[2]/ul/li')
            for li in detail:
                title = li.xpath('./a/@title')[0]
                url_ = 'http://www.kfsggzyjyw.cn' + li.xpath('./a/@href')[0]
                date_Today = li.xpath('./a/em/text()')[0]
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

    # 昆明市公共资源交易平台
    def hubei(self):
        print('昆明市公共资源交易平台', 'https://www.kmggzy.com')
        url_list = [
            # 市本级
            #   工程建设
            #       招标公告
            ['["TrueLore.Web.WebUI.WebAjaxService","GetPageZBGGByCCGC",[{},15,"\xe6\x98\x86\xe6\x98\x8e\xe5\xb8\x82",'
            '"11,12,13,14,15,16,17,18,19,20","1","0","JSGC",1,"","","BDMCGGBT",""],null,null]1585878116379',
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
             'https://www.kmggzy.com/Jyweb/ZFCGView.aspx?isBG=0&guid={}&subType2=12&subType=2&type=%e4%ba%a4%e6%98%93%'
             'e4%bf%a1%e6%81%af&area=1&xxlb=%E4%BA%A4%E6%98%93%E4%BF%A1%E6%81%AF&IsShow=1'],
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
        headers = {
            'ajax-method': 'AjaxMethodFactory',
            # 'Cookie': 'ASP.NET_SessionId=irwyyayh3dtwq5zxunzlnq3x',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        }
        url = url_list.pop(0)
        page = 0
        ls = []
        url_to = 'https://www.kmggzy.com/TrueLoreAjax/TrueLore.Web.WebUI.AjaxHelper,TrueLore.Web.WebUI.ashx'
        while True:
            num = page * 15
            page += 1
            res = str(tool.requests_post(url_to, url[0].format(num), headers)).replace("'",
                                                                                                                 '"')
            res = res[1:-1].replace('\\r', '').replace('\\n', '').replace('\t', '').replace(' ', '').replace('\\', '')
            detail = json.loads(res)['data']
            for i in detail:
                try:
                    title = i['title']
                except:
                    title = i['zhaoBiao_XiangMu_Name']
                url_ = url[1].format(i['guid'])
                date_Today = i['publish_StartTime'][:10]
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

    # 拉萨市公共资源交易网
    def binzhou(self):
        print('拉萨市公共资源交易网', 'http://ggzy.lasa.gov.cn')
        url_list = [
            'http://ggzy.lasa.gov.cn/pub/jyxx/list-content?keyName=&term=1&areaCode=&menuCode=JYGCJS&typeCode=ZBGG&startTime=&endTime=&pageNo={}',
            'http://ggzy.lasa.gov.cn/pub/jyxx/list-content?keyName=&term=1&areaCode=&menuCode=JYGCJS&typeCode=PBJG&startTime=&endTime=&pageNo={}',
            'http://ggzy.lasa.gov.cn/pub/jyxx/list-content?keyName=&term=1&areaCode=&menuCode=JYGCJS&typeCode=TBTZ&startTime=&endTime=&pageNo={}',
            'http://ggzy.lasa.gov.cn/pub/jyxx/list-content?keyName=&term=1&areaCode=&menuCode=JYZFCG&typeCode=CGGG&startTime=&endTime=&pageNo={}',
            'http://ggzy.lasa.gov.cn/pub/jyxx/list-content?keyName=&term=1&areaCode=&menuCode=JYZFCG&typeCode=GZGG&startTime=&endTime=&pageNo={}',
            'http://ggzy.lasa.gov.cn/pub/jyxx/list-content?keyName=&term=1&areaCode=&menuCode=JYZFCG&typeCode=JGGG&startTime=&endTime=&typeCode=ZZGG&pageNo={}',
        ]
        headers = {
            'Cookie': 'Hm_lvt_776eb6c6b51e3da5075c361337f94338=1584946762,1586936167; TS0161614b=01761419df1159ee5d0dc3cd6f5029798f9f5622ce83a1a6b58545a766632b4b2c2ba8a9c608459776a8aa67978b0cd44c6b44f253; Hm_lpvt_776eb6c6b51e3da5075c361337f94338=1586936490',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        }
        url = url_list.pop(0)
        page = 0
        ls = []
        while True:
            text = tool.requests_get(url.format(page), headers)
            page += 1
            detail = HTML(text).xpath('//*[@class="list-ul"]/li')
            for li in detail:
                title = li.xpath('./a/text()')[0]
                date_Today = li.xpath('./span/text()')[0]
                url_ = 'http://ggzy.lasa.gov.cn' + li.xpath('./a/@href')[0]
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

    # 丽江市公共资源交易平台
    def zhangzhou(self):
        print('丽江市公共资源交易平台', 'https://www.ljggzyxx.cn')
        url_list = [
            # 市本级
            #   工程建设
            #       招标公告
            ['https://www.ljggzyxx.cn/jyxx/jsgcZbgg?currentPage={}','//*[@id="zbggForm"]/div[3]/table/tr'],
            #       变更公告
            ['https://www.ljggzyxx.cn/jyxx/jsgcBgtz?currentPage={}','//*[@id="bgtzForm"]/div[3]/table/tr'],
            #       评标结果公示
            ['https://www.ljggzyxx.cn/jyxx/jsgcpbjggs?currentPage={}','//*[@id="zbggForm"]/div[3]/table/tr'],
            #       中标结果
            ['https://www.ljggzyxx.cn/jyxx/jsgcZbjggs?currentPage={}','//*[@id="zbggForm"]/div[3]/table/tr'],
            #       异常公告
            ['https://www.ljggzyxx.cn/jyxx/jsgcZbyc?currentPage={}','//*[@id="ycggForm"]/div[2]/table/tr'],
            #   政府采购
            #       采购公告
            ['https://www.ljggzyxx.cn/jyxx/zfcg/cggg?currentPage={}','//*[@id="zbggForm"]/div[2]/table/tr'],
            #       变更通知
            ['https://www.ljggzyxx.cn/jyxx/zfcg/gzsx?currentPage={}','//*[@id="zbggForm"]/div[2]/table/tr'],
            #       结果公示
            ['https://www.ljggzyxx.cn/jyxx/zfcg/zbjggs?currentPage={}','//*[@id="zbggForm"]/div[2]/table/tr'],
            #       异常公示
            ['https://www.ljggzyxx.cn/jyxx/zfcg/zfcgYcgg?currentPage={}','//*[@id="ycggForm"]/div[2]/table/tr']
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
                    url_ = 'https://www.ljggzyxx.cn' + html.xpath(url[1] + '[{}]/td[3]/a/@href'.format(i + 1))[0]
                    try:
                        date_Today = html.xpath(url[1] + '[{}]/td[4]/text()'.format(i + 1))[0]
                        if '招标' in date_Today or '采购' in date_Today or date_Today == '':
                            date_Today = html.xpath(url[1] + '[{}]/td[5]/text()'.format(i + 1))[0]
                    except:
                        date_Today = html.xpath(url[1] + '[{}]/td[5]/text()'.format(i + 1))[0]
                    if title == '':
                        title = html.xpath(url[1] + '[{}]/td[3]/@title'.format(i + 1))[0]
                except:
                    title = html.xpath(url[1] + '[{}]/td[4]/a/@title'.format(i + 1))[0]
                    url_ = 'https://www.ljggzyxx.cn' + html.xpath(url[1] + '[{}]/td[4]/a/@href'.format(i + 1))[0]
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

    # 丽水市公共资源交易平台
    def weifang(self):
        print('丽水市公共资源交易平台', 'http://lssggzy.lishui.gov.cn')
        url_list = [
            # 市级2
            #   建设工程
            #       招标公告
            'http://lssggzy.lishui.gov.cn/lsweb/jyxx/071001/071001001/',
            #       候选人公示
            'http://lssggzy.lishui.gov.cn/lsweb/jyxx/071001/071001004/',
            #       中标公示
            'http://lssggzy.lishui.gov.cn/lsweb/jyxx/071001/071001005/',
            #   政府采购
            #       采购公告
            'http://lssggzy.lishui.gov.cn/lsweb/jyxx/071002/071002002/',
            #       更正公告
            'http://lssggzy.lishui.gov.cn/lsweb/jyxx/071002/071002003/',
            #       中标公告
            'http://lssggzy.lishui.gov.cn/lsweb/jyxx/071002/071002005/'
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
            detail = html.xpath('/html/body/div[3]/table/tr/td[3]/table/tr[2]/td/table/tr')
            for tr in detail[1:]:
                for li in tr.xpath('./td/table/tr[2]/td/table/tr'):
                    title = li.xpath('./td[2]/a/@title')[0]
                    url_ = 'http://lssggzy.lishui.gov.cn' + li.xpath('./td[2]/a/@href')[0]
                    date_Today = li.xpath('./td[3]/font/text()')[0]
                    if tool.Transformation(date_Today) > tool.Transformation(self.date):
                        continue
                    elif tool.Transformation(date_Today) == tool.Transformation(self.date):
                        ls.append(url_)
                    else:
                        if len(url_list) == 0:
                            return [len(ls), ls]
                        else:
                            continue
            url = url_list.pop(0)
            page = 0

    # 六盘水市公共资源交易平台
    def yantai(self):
        print('六盘水市公共资源交易平台', 'http://ggzy.gzlps.gov.cn')
        url_list = [
            # 市本级
            #   工程建设
            #       招标公告
            'http://ggzy.gzlps.gov.cn/jyxx/jsgc/jygg/{}.html',
            #       中标公示
            'http://ggzy.gzlps.gov.cn/jyxx/jsgc/jyjggs/{}.html',
            #       更正公告
            'http://ggzy.gzlps.gov.cn/jyxx/jsgc/xmcq/{}.html',
            #       流标公告
            'http://ggzy.gzlps.gov.cn/jyxx/jsgc/lbgs/{}.html',
            #   政府采购
            #       采购公告
            'http://ggzy.gzlps.gov.cn/jyxx/zfcg/cggg/{}.html',
            #       中标公告
            'http://ggzy.gzlps.gov.cn/jyxx/zfcg/zbcjgg/{}.html',
            #       更正公告
            'http://ggzy.gzlps.gov.cn/jyxx/zfcg/gzgg/{}.html',
            #       流标公告
            'http://ggzy.gzlps.gov.cn/jyxx/zfcg/fbgg/{}.html'
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

    # 娄底市公共资源交易平台
    def gansu(self):
        print('娄底市公共资源交易平台', 'http://ldggzy.hnloudi.gov.cn')
        url_list = [
            'http://ldggzy.hnloudi.gov.cn/ldjyzx/jyxx/{}.shtml',
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
                text = tool.requests_get(url.format('list'), headers)
            else:
                text = tool.requests_get(url.format('list_' + str(page)), headers)
            html = HTML(text)
            detail = html.xpath('/html/body/div[4]/div[2]/div[2]/ul/li')
            for li in detail:
                title = li.xpath('./a/text()')[0].replace('\n', '').replace('\r', '').replace('\t', '').replace(' ', '')
                url_ = 'http://ldggzy.hnloudi.gov.cn' + li.xpath('./a/@href')[0]
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

    # 漯河市公共资源交易平台
    def baiyin(self):
        print('漯河市公共资源交易平台', 'https://www.lhjs.cn')
        url_list = [
            # 建设工程
            # 招标公告
           'https://www.lhjs.cn/BidNotice/jsgc/zbgg?pageIndex={}',
            # 变更公告
            'https://www.lhjs.cn/BidNotice/jsgc/bggg?pageIndex={}',
            # 开标情况
            'https://www.lhjs.cn/BidNotice/jsgc/kbqk?pageIndex={}',
            # 中标候选人
            'https://www.lhjs.cn/BidNotice/jsgc/zbhxrgs?pageIndex={}',
            # 中标结果
            'https://www.lhjs.cn/BidNotice/jsgc/zbjggg?pageIndex={}',
            # 政府采购
            # 采购公告
            'https://www.lhjs.cn/BidNotice/zfcg/cggg?pageIndex={}',
            # 变更公告
            'https://www.lhjs.cn/BidNotice/zfcg/bggg?pageIndex={}',
            # 中标结果
            'https://www.lhjs.cn/BidNotice/zfcg/zbjggg?pageIndex={}'
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
            detail = html.xpath('/html/body/div[2]/div[3]/div[2]/div[2]/div[2]/ul/li')
            for li in detail:
                title = li.xpath('./a/@title')[0]
                url_ = 'https://www.lhjs.cn' + li.xpath('./a/@href')[0]
                date_Today = li.xpath('./a/span[1]/span[2]/text()')[0].replace('\r', '').replace('\t', '') \
                    .replace(' ', '').replace('\n', '').replace('发布时间：', '').replace('/', '-')
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

    # 洛阳市公共资源交易平台
    def yancheng(self):
        print('洛阳市公共资源交易平台', 'http://www.lyggzyjy.cn')
        url_list = [
            # 建设工程
            # 招标公告
            'http://www.lyggzyjy.cn/TPFront/jyxx/009001/009001001/',
            # 变更公告
            'http://www.lyggzyjy.cn/TPFront/jyxx/009001/009001002/',
            # 中标公示
            'http://www.lyggzyjy.cn/TPFront/jyxx/009001/009001003/',
            # 中标候选人
            'http://www.lyggzyjy.cn/TPFront/jyxx/009001/009001004/',
            # 政府采购
            # 采购公告
            'http://www.lyggzyjy.cn/TPFront/jyxx/009002/009002001/',
            # 变更公告
            'http://www.lyggzyjy.cn/TPFront/jyxx/009002/009002002/',
            # 结果公告
            'http://www.lyggzyjy.cn/TPFront/jyxx/009002/009002003/'
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
            html = HTML(text)
            detail = html.xpath('//*[@id="right"]/div/div')
            for i in detail:
                for j in i.xpath('./ul/li'):
                    title = j.xpath('./div/a/@title')[0]
                    url_ = 'http://www.lyggzyjy.cn' + j.xpath('./div/a/@href')[0]
                    date_Today = j.xpath('./span/text()')[0]
                    if tool.Transformation(date_Today) > tool.Transformation(self.date):
                        continue
                    elif tool.Transformation(date_Today) == tool.Transformation(self.date):
                        ls.append(url_)
                    else:
                        if len(url_list) == 0:
                            return [len(ls), ls]
                        else:
                            continue
            url = url_list.pop(0)
            page = 0

    # 满洲里市公共资源交易中心
    def meishan(self):
        print('满洲里市公共资源交易中心', 'http://www.mzlggzy.org.cn')
        url_list = [
            # 建设工程
            'http://www.mzlggzy.org.cn/engconst/index_{}.htm',
            # 政府采购
            'http://www.mzlggzy.org.cn/govproc/index_{}.htm',
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
            detail = html.xpath('/html/body/div[2]/div[1]/div/div[2]/form/ul/li')
            for li in detail:
                title = li.xpath('./a/@title')[0]
                url_ = 'http://www.mzlggzy.org.cn' + li.xpath('./a/@href')[0]
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

    # 南阳市公共资源交易平台
    def fuzhou(self):
        print('南阳市公共资源交易平台', 'http://www.nyggzyjy.cn')
        url_list = [
            # 建设工程
            # 招标公告
           'http://www.nyggzyjy.cn/TPFront/jyxx/004001/004001001/?Paging={}',
            # 变更公告
            'http://www.nyggzyjy.cn/TPFront/jyxx/004001/004001002/?Paging={}',
            # 中标候选人
            'http://www.nyggzyjy.cn/TPFront/jyxx/004001/004001003/?Paging={}',
            # 中标结果
            'http://www.nyggzyjy.cn/TPFront/jyxx/004001/004001004/?Paging={}',
            # 政府采购
            # 采购公告
            'http://www.nyggzyjy.cn/TPFront/jyxx/004002/004002001/?Paging={}',
            # 变更公告
            'http://www.nyggzyjy.cn/TPFront/jyxx/004002/004002002/?Paging={}',
            # 中标结果
            'http://www.nyggzyjy.cn/TPFront/jyxx/004002/004002003/?Paging={}'
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
            detail = html.xpath('//*[@class="right r"]/ul/li')
            for li in detail:
                title = li.xpath('./a/@title')[0]
                url_ = 'http://www.nyggzyjy.cn' + li.xpath('./a/@href')[0]
                date_Today = li.xpath('./a/span/text()')[0]
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

    # 内蒙古自治区工程项目招投标中心
    def liaocheng(self):
        print('内蒙古自治区工程项目招投标中心', 'http://www.nmggcztb.cn')
        url_list = [
            # 房建市政
                # 中标信息
            'http://www.nmggcztb.cn/e/index/zbgglb.php?t=w&page={}&cont=fjsz',
                # 招标变更
            'http://www.nmggcztb.cn/e/index/zbgglb.php?t=z&page={}&cont=fjsz',
                # 中标候选人公示
            'http://www.nmggcztb.cn/e/index/zbgglb.php?t=a&page={}&cont=fjsz',
                # 招标公告
            'http://www.nmggcztb.cn/e/index/zbgglb.php?t=n&page={}&cont=fjsz',
            # 水利
                # 中标信息
            'http://www.nmggcztb.cn/e/index/zbgglb.php?t=w&page={}&cont=sl',
                # 招标变更
            'http://www.nmggcztb.cn/e/index/zbgglb.php?t=z&page={}&cont=sl',
                # 中标候选人公示
            'http://www.nmggcztb.cn/e/index/zbgglb.php?t=a&page={}&cont=sl',
                # 招标公告
            'http://www.nmggcztb.cn/e/index/zbgglb.php?t=n&page={}&cont=sl',
            # 铁路
                # 中标信息
            'http://www.nmggcztb.cn/e/index/zbgglb.php?t=w&page={}&cont=tl',
                # 招标变更
            'http://www.nmggcztb.cn/e/index/zbgglb.php?t=z&page={}&cont=tl',
                # 中标候选人公示
            'http://www.nmggcztb.cn/e/index/zbgglb.php?t=a&page={}&cont=tl',
                # 招标公告
            'http://www.nmggcztb.cn/e/index/zbgglb.php?t=n&page={}&cont=tl',
            # 公路
                # 中标信息
            'http://www.nmggcztb.cn/e/index/zbgglb.php?t=w&page={}&cont=gl',
                # 招标变更
            'http://www.nmggcztb.cn/e/index/zbgglb.php?t=z&page={}&cont=gl',
                # 中标候选人公示
            'http://www.nmggcztb.cn/e/index/zbgglb.php?t=a&page={}&cont=gl',
                # 招标公告
            'http://www.nmggcztb.cn/e/index/zbgglb.php?t=n&page={}&cont=gl',
            # 其他
                # 中标信息
            'http://www.nmggcztb.cn/e/index/zbgglb.php?t=w&page={}&cont=qt',
                # 招标变更
            'http://www.nmggcztb.cn/e/index/zbgglb.php?t=z&page={}&cont=qt',
                # 中标候选人公示
            'http://www.nmggcztb.cn/e/index/zbgglb.php?t=a&page={}&cont=qt',
                # 招标公告
            'http://www.nmggcztb.cn/e/index/zbgglb.php?t=n&page={}&cont=qt',
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
            detail = json.loads(text)['L']
            for i in detail:
                title = i['2']
                type = re.findall('t=(.*?)&page', url)[0]
                if type == 'w':
                    url_ = 'http://www.nmggcztb.cn/gcxx/detail.php?n=3&id=' + i['0']
                elif type == 'z':
                    url_ = 'http://www.nmggcztb.cn/gcxx/detail.php?n=4&id=' + i['0']
                elif type == 'a':
                    url_ = 'http://www.nmggcztb.cn/gcxx/detail.php?n=2&id=' + i['0']
                elif type == 'n':
                    url_ = 'http://www.nmggcztb.cn/gcxx/detail.php?n=1&id=' + i['0']
                date_Today = i['Time']
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

    # 宁波市公共资源交易平台
    def putian(self):
        print('宁波市公共资源交易平台', 'http://bidding.ningbo.gov.cn')
        url_list = [
            # 工程建设
            # 招标公告
            'http://bidding.ningbo.gov.cn/cms/gcjszbgg/index_{}.htm',
            # 预中标
            'http://bidding.ningbo.gov.cn/cms/gcjsyzbgs/index_{}.htm',
            # 中标
            'http://bidding.ningbo.gov.cn/cms/gcjszbgg1/index_{}.htm',
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
            detail = html.xpath('//*[@id="channelBody"]/div[2]/ul/div[1]/li')
            for li in detail:
                title = li.xpath('./a/@title')[0]
                url_ = 'http://bidding.ningbo.gov.cn' + li.xpath('./a/@href')[0]
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

    # 怒江州公共资源交易平台
    def xian(self):
        print('怒江州公共资源交易平台', 'http://182.246.203.127:8001')
        url_list = [
            # 市本级
            #   工程建设
            #       招标公告
            ['http://182.246.203.127:8001/jyxx/jsgcZbgg?currentPage={}','//*[@id="zbggForm"]/div[3]/table/tr'],
            #       变更公告
            ['http://182.246.203.127:8001/jyxx/jsgcBgtz?currentPage={}','//*[@id="bgtzForm"]/div[2]/table/tr'],
            #       评标结果公示
            ['http://182.246.203.127:8001/jyxx/jsgcpbjggs?currentPage={}','//*[@id="zbggForm"]/div[2]/table/tr'],
            #       中标结果
            ['http://182.246.203.127:8001/jyxx/jsgcZbjggs?currentPage={}','//*[@id="zbggForm"]/div[3]/table/tr'],
            #       异常公告
            ['http://182.246.203.127:8001/jyxx/jsgcZbyc?currentPage={}','//*[@id="ycggForm"]/div[2]/table/tr'],
            #   政府采购
            #       采购公告
            ['http://182.246.203.127:8001/jyxx/zfcg/cggg?currentPage={}','//*[@id="zbggForm"]/div[2]/table/tr'],
            #       变更通知
            ['http://182.246.203.127:8001/jyxx/zfcg/gzsx?currentPage={}','//*[@id="zbggForm"]/div[2]/table/tr'],
            #       结果公示
            ['http://182.246.203.127:8001/jyxx/zfcg/zbjggs?currentPage={}','//*[@id="zbggForm"]/div[2]/table/tr'],
            #       异常公示
            ['http://182.246.203.127:8001/jyxx/zfcg/zfcgYcgg?currentPage={}','//*[@id="ycggForm"]/div[2]/table/tr']
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
                    url_ = 'http://182.246.203.127:8001' + html.xpath(url[1] + '[{}]/td[3]/a/@href'.format(i + 1))[
                        0]
                    date_Today = html.xpath(url[1] + '[{}]/td[4]/text()'.format(i + 1))[0]
                    if '招标' in date_Today or '采购' in date_Today:
                        date_Today = html.xpath(url[1] + '[{}]/td[5]/text()'.format(i + 1))[0]
                    if title == '':
                        title = html.xpath(url[1] + '[{}]/td[3]/@title'.format(i + 1))[0]
                except:
                    title = html.xpath(url[1] + '[{}]/td[4]/a/@title'.format(i + 1))[0]
                    url_ = 'http://182.246.203.127:8001' + html.xpath(url[1] + '[{}]/td[4]/a/@href'.format(i + 1))[
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

    # 盘锦市公共资源交易平台
    def xizang(self):
        print('盘锦市公共资源交易平台', 'http://202.97.171.17')
        url_list = [
            # 建设工程
                # 开标公告
            'http://202.97.171.175/jsgc/008001/{}.html',
                # 结果公告
            'http://202.97.171.175/jsgc/008003/{}.html',
                # 中标候选人
            'http://202.97.171.175/jsgc/008004/{}.html',
            # 政府采购
                # 开标公告
            'http://202.97.171.175/zfcg/007001/{}.html',
                # 更正公告
            'http://202.97.171.175/zfcg/007002/{}.html',
                # 结果公告
            'http://202.97.171.175/zfcg/007003/{}.html'
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
            detail = html.xpath('/html/body/div/ul/li')
            for li in detail:
                title = li.xpath('./a/@title')[0]
                url_ = 'http://202.97.171.175' + li.xpath('./a/@href')[0]
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

    # 西藏自治区政府采购网
    def xizangzf(self):
        print('西藏自治区政府采购网', 'http://www.pdsggzy.com')
        url_list = [
            # 建设工程
                # 招标公告
            'http://www.pdsggzy.com/gzbgg/index_{}.jhtml',
                # 变更公示
            'http://www.pdsggzy.com/gbcgg/index_{}.jhtml',
                # 中标结果
            'http://www.pdsggzy.com/gzbgs/index_{}.jhtml',
            # 政府采购
                # 采购公告
            'http://www.pdsggzy.com/zzbgg/index_{}.jhtml',
                # 变更公告
            'http://www.pdsggzy.com/zbcgg/index_{}.jhtml',
                # 结果公告
            'http://www.pdsggzy.com/zzbgs/index_{}.jhtml'
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
            detail = html.xpath('/html/body/div/div/div[9]/div[2]/div/div[2]/ul/li')
            for li in detail:
                title = li.xpath('./a/@title')[0]
                url_ = 'http://www.pdsggzy.com' + li.xpath('./a/@href')[0]
                date_Today = li.xpath('./a/em/text()')[0]
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

    # 普洱市公共资源交易平台
    def dazhou(self):
        print('普洱市公共资源交易平台', 'http://www.pesggzyjyxxw.com')
        url_list = [
            # 市本级
            #   工程建设
            #       招标公告
            ['http://www.pesggzyjyxxw.com/jyxx/jsgcZbgg?currentPage={}','//*[@id="zbggForm"]/div[3]/table/tr'],
            #       变更公告
            ['http://www.pesggzyjyxxw.com/jyxx/jsgcBgtz?currentPage={}','//*[@id="bgtzForm"]/div[3]/table/tr'],
            #       评标结果公示
            ['http://www.pesggzyjyxxw.com/jyxx/jsgcpbjggs?currentPage={}','//*[@id="zbggForm"]/div[2]/table/tr'],
            #       中标结果
            ['http://www.pesggzyjyxxw.com/jyxx/jsgcZbjggs?currentPage={}','//*[@id="zbggForm"]/div[3]/table/tr'],
            #       异常公告
            ['http://www.pesggzyjyxxw.com/jyxx/jsgcZbyc?currentPage={}','//*[@id="ycggForm"]/div[2]/table/tr'],
            #   政府采购
            #       采购公告
            ['http://www.pesggzyjyxxw.com/jyxx/zfcg/cggg?currentPage={}','//*[@id="zbggForm"]/div[2]/table/tr'],
            #       变更通知
            ['http://www.pesggzyjyxxw.com/jyxx/zfcg/gzsx?currentPage={}','//*[@id="zbggForm"]/div[2]/table/tr'],
            #       结果公示
            ['http://www.pesggzyjyxxw.com/jyxx/zfcg/zbjggs?currentPage={}','//*[@id="zbggForm"]/div[2]/table/tr'],
            #       异常公示
            ['http://www.pesggzyjyxxw.com/jyxx/zfcg/zfcgYcgg?currentPage={}','//*[@id="ycggForm"]/div[2]/table/tr']
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
            if len(detail) < 5:
                if 'bgtzForm' in url[1]:
                    url[1] = '//*[@id="bgtzForm"]/div[2]/table/tr'
            for i in range(1, len(detail)):
                try:
                    title = html.xpath(url[1] + '[{}]/td[3]/a/@title'.format(i + 1))[0]
                    url_ = 'http://www.pesggzyjyxxw.com' + html.xpath(url[1] + '[{}]/td[3]/a/@href'.format(i + 1))[
                        0]
                    try:
                        date_Today = html.xpath(url[1] + '[{}]/td[4]/text()'.format(i + 1))[0]
                        if '招标' in date_Today or '采购' in date_Today or date_Today == '':
                            date_Today = html.xpath(url[1] + '[{}]/td[5]/text()'.format(i + 1))[0]
                    except:
                        date_Today = html.xpath(url[1] + '[{}]/td[5]/text()'.format(i + 1))[0]
                    if title == '':
                        title = html.xpath(url[1] + '[{}]/td[3]/@title'.format(i + 1))[0]
                except:
                    title = html.xpath(url[1] + '[{}]/td[4]/a/@title'.format(i + 1))[0]
                    url_ = 'http://www.pesggzyjyxxw.com' + html.xpath(url[1] + '[{}]/td[4]/a/@href'.format(i + 1))[
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

    # 黔东南州公共资源交易平台
    def jinchang(self):
        print('黔东南州公共资源交易平台', 'http://ggzyjyzx.qdn.gov.cn')
        url_list = [
            # 市本级
            #   工程建设
            #       招标公告
            'http://ggzyjyzx.qdn.gov.cn/jyxx/gcjy_5806171/zbgg_5806172/{}.html',
            #       中标公示
            'http://ggzyjyzx.qdn.gov.cn/jyxx/gcjy_5806171/zbgs_5806174/{}.html',
            #       流标公告
            'http://ggzyjyzx.qdn.gov.cn/jyxx/gcjy_5806171/lbgs_5806175/{}.html',
            #   政府采购
            #       采购公告
            'http://ggzyjyzx.qdn.gov.cn/jyxx/zfcgjy_5806179/cggg_5806180/{}.html',
            #       中标公告
            'http://ggzyjyzx.qdn.gov.cn/jyxx/zfcgjy_5806179/zbgg_5806182/{}.html',
            #       更正公告
            'http://ggzyjyzx.qdn.gov.cn/jyxx/zfcgjy_5806179/bggg_5806181/{}.html',
            #       流标公告
            'http://ggzyjyzx.qdn.gov.cn/jyxx/zfcgjy_5806179/lbgs_5806183/{}.html'
        ]
        headers = {
            # 'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Content-Type': 'text/plain;charset=UTF-8',
            # 'X-Requested-With': 'XMLHttpRequest',
            'Origin': 'http://ggzy.jcs.gov.cn',
            # 'Cookie': 'userName=; number=2077661; Hm_lvt_1b8209d1dfbb21e021496ae1e24fe5c6=1613983154; Hm_lpvt_1b8209d1dfbb21e021496ae1e24fe5c6=1613983168; SERVERID=31cefde443981166256c9862ebb57c25|1613983175|1613983151',
            'Referer': 'http://ggzy.jcs.gov.cn/InfoPage/TradeInfomation.aspx?state=1,2,3',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
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

    # 黔南州公共资源交易平台
    def longnan(self):
        print('黔南州公共资源交易平台', 'http://ggzy.qiannan.gov.cn')
        url_list = [
            # 市本级
            #   工程建设
            #       招标公告
            'http://ggzy.qiannan.gov.cn/gcjs_500203/zbgg/{}.html',
            #       中标公示
            'http://ggzy.qiannan.gov.cn/gcjs_500203/zbgs/{}.html',
            #       更正公告
            'http://ggzy.qiannan.gov.cn/gcjs_500203/bgdycq/{}.html',
            #       流标公告
            'http://ggzy.qiannan.gov.cn/gcjs_500203/lbgs/{}.html',
            #   政府采购
            #       采购公告
            'http://ggzy.qiannan.gov.cn/zfcg_500203/zbgg_5060411/{}.html',
            #       中标公告
            'http://ggzy.qiannan.gov.cn/zfcg_500203/zbgs_5060412/{}.html',
            #       更正公告
            'http://ggzy.qiannan.gov.cn/zfcg_500203/bggg/{}.html',
            #       流标公告
            'http://ggzy.qiannan.gov.cn/zfcg_500203/fbgs/{}.html'
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
            detail = html.xpath('//*[@class="NewsList"]/ul/li')
            for li in detail:
                try:
                    title = li.xpath('./a/@title')[0]
                    url_ = li.xpath('./a/@href')[0]
                    date_Today = li.xpath('./span/text()')[0].replace('\n', '').replace('\r', '') \
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

    # 黔西南州公共资源交易平台
    def shanxi(self):
        print('黔西南州公共资源交易平台', 'http://ggzyjy.qxn.gov.cn')
        url_list = [
            # 市本级
            #   工程建设
            #       招标公告
            'http://ggzyjy.qxn.gov.cn/jyzx_500593/gcjs/jygg/{}.html',
            #       中标公示
            'http://ggzyjy.qxn.gov.cn/jyzx_500593/gcjs/jggs/{}.html',
            #   政府采购
            #       采购公告
            'http://ggzyjy.qxn.gov.cn/jyzx_500593/zfcg/jygg_5377519/{}.html',
            #       中标公告
            'http://ggzyjy.qxn.gov.cn/jyzx_500593/zfcg/jggs_5377520/{}.html',
            #       预公示
            'http://ggzyjy.qxn.gov.cn/jyzx_500593/zfcg/ygg/{}.html'
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
            if page == 20:
                print('日期不符, 正在切换类型')
                url = url_list.pop(0)
                page = 0
            if page == 1:
                text = tool.requests_get(url.format('index'), headers)
            else:
                text = tool.requests_get(url.format('index_' + str(page)), headers)
            html = HTML(text)
            detail = html.xpath('//*[@class="list"]/li')
            for li in detail:
                title = li.xpath('./a/@title')[0]
                url_ = li.xpath('./a/@href')[0]
                date_Today = li.xpath('./span/text()')[0].replace('\n', '').replace('\r', '') \
                    .replace('\t', '').replace(' ', '').replace('[', '').replace(']', '')
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

    # 青岛市公共资源交易平台
    def yaan(self):
        print('青岛市公共资源交易平台', 'https://ggzy.qingdao.gov.cn')
        url_list = [
            # 市本级
            #   工程建设
            #       招标公告
            'https://ggzy.qingdao.gov.cn/Tradeinfo-GGGSList/0-0-0?pageIndex={}',
            #       预中标
            'https://ggzy.qingdao.gov.cn/Tradeinfo-GGGSList/0-0-2?pageIndex={}',
            #       废标公告
            'https://ggzy.qingdao.gov.cn/Tradeinfo-GGGSList/0-0-3?pageIndex={}',
            #       中标公告
            'https://ggzy.qingdao.gov.cn/Tradeinfo-GGGSList/0-0-8?pageIndex={}',
            #   政府采购
            #       采购公告
            'https://ggzy.qingdao.gov.cn/Tradeinfo-GGGSList/1-1-0?pageIndex={}',
            #       变更公告
            'https://ggzy.qingdao.gov.cn/Tradeinfo-GGGSList/1-1-5?pageIndex={}',
            #       中标公告
            'https://ggzy.qingdao.gov.cn/Tradeinfo-GGGSList/1-1-2?pageIndex={}',
            #       废标公告
            'https://ggzy.qingdao.gov.cn/Tradeinfo-GGGSList/1-1-3?pageIndex={}'
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
            detail = HTML(text).xpath('//*[@class="info_con"]/table/tr')
            for li in detail:
                title = li.xpath('./td[1]/a/@title')[0]
                url_ = 'https://ggzy.qingdao.gov.cn' + li.xpath('./td[1]/a/@href')[0]
                date_Today = li.xpath('./td[2]/text()')[0].replace('\n', '').replace('\r', '') \
                    .replace('\t', '').replace(' ', '').replace('[', '').replace(']', '')
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

    # 曲靖市公共资源交易平台
    def longyan(self):
        print('曲靖市公共资源交易平台', 'http://jyxt.qjggzyxx.gov.cn')
        url_list = [
            # 市本级
            #   工程建设
            #       招标公告
            ['http://jyxt.qjggzyxx.gov.cn/jyxx/jsgcZbgg?currentPage={}','//*[@id="zbggForm"]/div[3]/table/tr'],
            #       变更公告
            ['http://jyxt.qjggzyxx.gov.cn/jyxx/jsgcBgtz?currentPage={}','//*[@id="bgtzForm"]/div[2]/table/tr'],
            #       评标结果公示
            ['http://jyxt.qjggzyxx.gov.cn/jyxx/jsgcpbjggs?currentPage={}','//*[@id="zbggForm"]/div[2]/table/tr'],
            #       中标结果
            ['http://jyxt.qjggzyxx.gov.cn/jyxx/jsgcZbjggs?currentPage={}','//*[@id="zbggForm"]/div[3]/table/tr'],
            #       异常公告
            ['http://jyxt.qjggzyxx.gov.cn/jyxx/jsgcZbyc?currentPage={}','//*[@id="ycggForm"]/div[2]/table/tr'],
            #   政府采购
            #       采购公告
            ['http://jyxt.qjggzyxx.gov.cn/jyxx/zfcg/cggg?currentPage={}','//*[@id="zbggForm"]/div[2]/table/tr'],
            #       变更通知
            ['http://jyxt.qjggzyxx.gov.cn/jyxx/zfcg/gzsx?currentPage={}','//*[@id="zbggForm"]/div[2]/table/tr'],
            #       结果公示
            ['http://jyxt.qjggzyxx.gov.cn/jyxx/zfcg/zbjggs?currentPage={}','//*[@id="zbggForm"]/div[2]/table/tr'],
            #       异常公示
            ['http://jyxt.qjggzyxx.gov.cn/jyxx/zfcg/zfcgYcgg?currentPage={}','//*[@id="ycggForm"]/div[2]/table/tr']
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
                    url_ = 'http://jyxt.qjggzyxx.gov.cn' + html.xpath(url[1] + '[{}]/td[3]/a/@href'.format(i + 1))[
                        0]
                    date_Today = html.xpath(url[1] + '[{}]/td[4]/text()'.format(i + 1))[0]
                    if '招标' in date_Today or '采购' in date_Today:
                        date_Today = html.xpath(url[1] + '[{}]/td[5]/text()'.format(i + 1))[0]
                    if title == '':
                        title = html.xpath(url[1] + '[{}]/td[3]/@title'.format(i + 1))[0]
                except:
                    title = html.xpath(url[1] + '[{}]/td[4]/a/@title'.format(i + 1))[0]
                    url_ = 'http://jyxt.qjggzyxx.gov.cn' + html.xpath(url[1] + '[{}]/td[4]/a/@href'.format(i + 1))[
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


