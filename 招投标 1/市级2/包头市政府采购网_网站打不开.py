# -*- coding: utf-8 -*-
import json
import re, pytesseract
import time, html
import requests
from PIL import Image
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item
from selenium import webdriver

# 包头市政府采购网
class baotou_zfcg:
    def __init__(self):
        self.url_list = [
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
        self.url = self.url_list.pop(0)

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

    def parse(self):
        date = tool.date
        # date = '2020-01-07'
        page = 0
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
        driver.get(self.url)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
            'Cookie': 'UM_distinctid=16f7d9a380334c-09e791f4fa51bd-e343166-1fa400-16f7d9a380437f; JSESSIONID=' +
                      driver.get_cookies()[0]['value'] + '; CNZZDATA1278039014=1257312036-1578357560-%7C1578373994'
        }
        while True:
            page += 1
            print('*' * 20, page, '*' * 20)
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
                url = 'http://zfcg.baotou.gov.cn/portal/documentView.do?method=view&id={}&ver=null'.format(
                    tr.xpath('./td[2]/a/@href')[0].replace('/viewer.do?id=', ''))
                date_Today = tr.xpath('./td[3]/text()')[0][:10]
                if tool.Transformation(date) <= tool.Transformation(date_Today):
                    if tool.removal(title, date):
                        self.parse_detile(title, url, date, headers)
                        # print(title, url, date_Today)
                    else:
                        print('【existence】', url)
                        continue
                else:
                    print('日期不符, 正在切换类型...', date_Today)
                    self.url = self.url_list.pop(0)
                    driver.get(self.url)
                    page = 0
                    break
            if page != 0:
                time.sleep(1)
                driver.find_element_by_xpath('//*[@class="compactToolbar"]/table/tbody/tr[1]/td[4]/a').click()
            if page == 20:
                self.url = self.url_list.pop(0)
                driver.get(self.url)
                break
            driver.close()
    def parse_detile(self, title, url, date, headers):
        print(url)
        url_text = tool.requests_get(url, headers)
        url_html = etree.HTML(url_text)
        detail = url_html.xpath('/html/body/table')[0]
        detail_html = etree.tostring(detail, method='HTML')
        detail_html = html.unescape(detail_html.decode())
        detail_text = url_html.xpath('string(/html/body/table)').replace('\xa0', '').replace('\n', '').replace(
            '\r', '').replace('\t', '').replace(' ', '').replace('\xa5','')
        # print(detail_text)
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
        width_list = re.findall('width="(.*?)"', item["body"])
        for i in width_list:
            item["body"] = item["body"].replace('width="{}"'.format(i), '')
        width_list = re.findall('WIDTH: (.*?)pt;', item["body"])
        for i in width_list:
            item["body"] = item["body"].replace('WIDTH: {}pt;'.format(i), '')
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
        item['resource'] = '包头市政府采购网'
        item['shi'] = 3002
        item['sheng'] = 3000
        item['removal']= title
        process_item(item)
        # print(item)

    def get_nativeplace(self, addr):
        city = ''
        city_list = [['3002.001', '东河区'], ['3002.002', '昆都仑区'], ['3002.003', '青山区'], ['3002.004', '石拐区'], ['3002.005', '白云矿区'], ['3002.006', '九原区'], ['3002.007', '土默特右旗'], ['3002.008', '固阳县'], ['3002.009', '达尔罕茂明安联合旗']]

        for i in city_list:
            if i[1] in addr:
                city = float(i[0])
                break
        if city == '':
            city = 3002
        return city
if __name__ == '__main__':
    import traceback, os
    try:
        jl = baotou_zfcg()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
        tool.send_error('报错文件：'+str(os.path.basename(__file__))+'报错信息：'+str(e))
