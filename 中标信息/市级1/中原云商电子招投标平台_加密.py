# -*- coding: utf-8 -*-
import base64
import json
import re
import time, html
import urllib.parse

import pytesseract
from PIL import Image
from lxml import etree
import tool
from save_database import process_item

# 中原云商电子招投标平台.jpg
class alashan_ggzy:
    def __init__(self):
        self.url_code = [
            'https://bid.zyepp.com/EpointWebBuilder/rest/infolist/geInfoListZZ'
            # 'http://bid.zyepp.com/zbzq/{}.html',
            # 'http://bid.zyepp.com/fzbzq/{}.html'
        ]
        self.url = self.url_code.pop(0)
        self.headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            # 'Cookie': 'isInitAreaCode=null; _gscu_653689772=78282348u2bs1g18; _gscbrs_653689772=1; UM_distinctid=16f78f570621fa-0e76a94f9f3d2d-e343166-1fa400-16f78f570631fc; _gscs_653689772=t782895054fvlkv12|pv:14; CNZZDATA1260595804=985342442-1578282342-%7C1578291895',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
        }

    def img_recognition(self):

        tokenurl = 'https://bid.zyepp.com/EpointWebBuilder/rest/getOauthInfoAction/getNoUserAccessToken'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'}
        res = tool.requests_post(tokenurl,data=None,headers=headers)
        get_token = json.loads(res)['custom']['access_token']
        print(get_token)
        headers = {
            'Authorization': f'Bearer {get_token}',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'}
        getcode = 'https://bid.zyepp.com/EpointWebBuilder/rest/frontAppNotNeedLoginAction/getVerificationCode?params=%7B%22width%22%3A%22100%22%2C%22height%22%3A%2240%22%2C%22codeNum%22%3A%224%22%2C%22interferenceLine%22%3A%221%22%2C%22codeGuid%22%3A%22%22%7D'
        # data ='params=%7B%22siteGuid%22%3A%227eb5f7f1-9041-43ad-8e13-8fcb82ea831a%22%2C%22ImgGuid%22%3A%2266748e96-9f07-475e-879b-518701914862%22%2C%22YZM%22%3A%223w5e%22%7D'
        res = tool.requests_post(getcode,data=None, headers=headers)
        custom = json.loads(res)['custom']
        imgCode = (custom['imgCode']).replace('data:image/jpg;base64,', '')
        guid = custom['verificationCodeGuid']
        with open('中原云商电子招投标平台.jpg', 'wb') as w:
            w.write(base64.b64decode(imgCode))
        image = Image.open('中原云商电子招投标平台.jpg')
        image = image.convert('L')
        # image = image.convert('1')
        count = 175
        table = []
        for i in range(256):
            if i < count:
                table.append(0)
            else:
                table.append(1)
        image = image.point(table, '1')
        ymz = pytesseract.image_to_string(image).strip()
        print(ymz)
        img_yzm = re.findall(r'[\d\w]+', ymz)[0]
        print(img_yzm,len(img_yzm))
        if len(img_yzm) == 4:
            params = 'params=' + urllib.parse.quote(
                '{"siteGuid":"7eb5f7f1-9041-43ad-8e13-8fcb82ea831a","ImgGuid":"'+guid+'","YZM":"'+ymz+'"}')
            url = 'https://bid.zyepp.com/EpointWebBuilder/rest/frontAppNotNeedLoginAction/pageListVerify'
            text=tool.requests_post_param(url, self.headers, param=params)
            print(text)
            return ymz,guid
        else:
            self.img_recognition()


        # pagelist = 'https://bid.zyepp.com/EpointWebBuilder/rest/frontAppNotNeedLoginAction/pageListVerify'
        # jsondata = json.loads(reslist.decode())

    def parse(self):
        date = tool.date
        page=0
        while True:
            try:
                print('*' * 20, page, '*' * 20)
                if page == 0:
                    data='params='+urllib.parse.quote('{"categorynum":"001004","sdt":"","edt":"","tbsdt":"","tbedt":"","title":"","cgzz":"","cgfs":"","pageSize":40,"pageIndex":"0","siteguid":"7eb5f7f1-9041-43ad-8e13-8fcb82ea831a","YZM":"","ImgGuid":""}')
                    text = tool.requests_post_param(self.url, self.headers, param=data)
                else:
                    yzm,guid=self.img_recognition()
                    params = 'params=' + urllib.parse.quote(
                        '{"categorynum":"001004","sdt":"","edt":"","tbsdt":"","tbedt":"","title":"","cgzz":"","cgfs":"","pageSize":40,"pageIndex":"' + str(page) + '","siteguid":"7eb5f7f1-9041-43ad-8e13-8fcb82ea831a","YZM":"{' + yzm + '}","ImgGuid":"{' + guid + '}"}')
                    text = tool.requests_post_param(self.url, self.headers, param=params)
                print(text)
                page += 1
                detail = json.loads(text)
                for data in detail.get('Table'):
                    title = data.get('title2').replace('\u2022', '').replace('\r', '').replace('\n', '').replace('\t', '').replace(' ', '')
                    url = 'http://bid.zyepp.com' +data.get('infourl')
                    date_Today = data.get('tbenddate').replace('\r', '').replace('\n', '').replace('\t', '').replace(' ', '')
                    print(title, url, date_Today)
                    # time.sleep(666)
                    if tool.Transformation(date) <= tool.Transformation(date_Today):
                        # if tool.removal(title, date):
                            self.parse_detile(title, url, date_Today)

                        # else:
                        #     print('【existence】', url)
                        #     continue
                    else:
                        print('日期不符, 正在切换类型...', date_Today)
                        return
            except Exception:
                traceback.print_exc()


    def parse_detile(self, title, url, date):
        print(url)
        url_text = tool.requests_get(url, self.headers)
        url_html = etree.HTML(url_text)
        detail = url_html.xpath('//*[@id="leftcontent"]')[0]
        detail_html = etree.tostring(detail, method='HTML')
        detail_html = html.unescape(detail_html.decode())
        detail_text = url_html.xpath('string(//*[@id="leftcontent"])').replace('\xa0', '').replace(
            '\n', '').replace('\r', '').replace('\t',
                                                '').replace(
            ' ', '').replace('\xa5', '')
        print(detail_text)
        item = {}
        item['title'] = title.replace('\u2022', '')
        item['url'] = url
        item['date'] = date
        item['typeid'] = tool.get_typeid(item['title'])
        item['senddate'] = int(time.time())
        item['mid'] = 867
        item['nativeplace'] = float(tool.get_title_city(item['title']))
        if item['nativeplace'] == 0:
            item['nativeplace'] = float(tool.more(item['title'] +detail_text))
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
        item['winner'] = tool.get_winner(detail_text)
        item['address'] = tool.get_address(detail_text)
        item['linkman'] = tool.get_linkman(detail_text)
        item['function'] = tool.get_function(detail_text)
        item['resource'] = '中原云商电子招投标平台'
        item["shi"] = int(item["nativeplace"])
        if len(str(item["nativeplace"])) == 4:
            item['sheng'] = int(str(item["nativeplace"])[:2] + '00')
        elif len(str(item["nativeplace"])) == 5:
            item['sheng'] = int(str(item["nativeplace"])[:3] + '00')
        else:
            item['sheng'] = 0
        item['removal']= title
        process_item(item)
        # print(item['nativeplace'], item['title'])

if __name__ == '__main__':
    import traceback, os
    try:
        jl = alashan_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()

