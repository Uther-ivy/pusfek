# -*- coding: utf-8 -*-
import json
import re
import time, html

import execjs
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 玉林市公共资源交易中心
class wenshan_ggzy:
    def __init__(self):
        self.domain_name = 'https://ec.minmetals.com.cn'
        self.url_list = [
            'https://ec.minmetals.com.cn/open/homepage/zbs/by-lx-page'
        ]
        self.url = self.url_list.pop(0)
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',

        }
    def get_code(self):
        url = 'https://ec.minmetals.com.cn/open/homepage/public'
        # res=tool.requests_post(url, data=None, headers=self.headers)
        # print(res)
        data=r'''
var v, b = {
            decode: function(e) {
                var t;
                if (void 0 === d) {
                    var n = "0123456789ABCDEF"
                      , r = " \f\n\r\t \u2028\u2029";
                    for (d = {},
                    t = 0; t < 16; ++t)
                        d[n.charAt(t)] = t;
                    for (n = n.toLowerCase(),
                    t = 10; t < 16; ++t)
                        d[n.charAt(t)] = t;
                    for (t = 0; t < r.length; ++t)
                        d[r.charAt(t)] = -1
                }
                var o = []
                  , i = 0
                  , s = 0;
                for (t = 0; t < e.length; ++t) {
                    var a = e.charAt(t);
                    if ("=" == a)
                        break;
                    if (a = d[a],
                    -1 != a) {
                        if (void 0 === a)
                            throw new Error("Illegal character at offset " + t);
                        i |= a,
                        ++s >= 2 ? (o[o.length] = i,
                        i = 0,
                        s = 0) : i <<= 4
                    }
                }
                if (s)
                    throw new Error("Hex encoding incomplete: 4 bits missing");
                return o
            }
        }
function g(e) {
        var t;
        if (void 0 === v) {
            var n = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
                , r = "= \f\n\r\t \u2028\u2029";
            for (v = Object.create(null),
                     t = 0; t < 64; ++t)
                v[n.charAt(t)] = t;
            for (v["-"] = 62,
                     v["_"] = 63,
                     t = 0; t < r.length; ++t)
                v[r.charAt(t)] = -1
        }
        var o = []
            , i = 0
            , s = 0;
        for (t = 0; t < e.length; ++t) {
            var a = e.charAt(t);
            if ("=" == a)
                break;
            if (a = v[a],
            -1 != a) {
                if (void 0 === a)
                    throw new Error("Illegal character at offset " + t);
                i |= a,
                    ++s >= 4 ? (o[o.length] = i >> 16,
                        o[o.length] = i >> 8 & 255,
                        o[o.length] = 255 & i,
                        i = 0,
                        s = 0) : i <<= 6
            }
        }
        switch (s) {
            case 1:
                throw new Error("Base64 encoding incomplete: at least 2 bits missing");
            case 2:
                o[o.length] = i >> 10;
                break;
            case 3:
                o[o.length] = i >> 16,
                    o[o.length] = i >> 8 & 255;
                break
        }
        return o
    }

'''
        # print(data)
        res='MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCyIlvDj+fpEh6man5KXuP2v05zxS7o9A5yTbDsKdGcBZ8730VVzFO3iX/OGYygKCWtSzlsUKaD0ygo9+7n8KBljTccA/h36/ONIluwqGULRyPFdODwM+EEqCNswdlGGU/DK1FSGxwpJXL0bvaZrSGbFiGz/mzjJ+dBbOsmjaT5yQIDAQAB'
        dedata = execjs.compile(data).call('g',res)
        print(dedata)
    def parse(self):
        date = tool.date
        # date = '2020-09-27'
        page = 0
        while True:
            page += 1
            data = {

            'param': ''
          }
            text = tool.session_post(self.url, data)
            print('*' * 20, page, '*' * 20)
            print(11, text.replace('\ufffd', ' ').replace('\u30fb', ' '))
            # time.sleep(6666)
            detail = json.loads(text)['result']['result']
            for li in detail:
                title = li['title']
                id= li['id']
                url = f'https://ec.sinopec.com/f/supp/notice/bidNotice.do?id={id}'
                date_Today = int(li['createdate']['time']/1000)
                if 'http' not in url:
                    url = self.domain_name + url
                print(title, url, date_Today)
                # time.sleep(666)
                if tool.Transformation(date) >= date_Today:
                    if tool.removal(title, date):
                        self.parse_detile(title, url, date_Today)
                    else:
                        print('【existence】', url)
                        continue
                else:
                    print('日期不符, 正在切换类型', date_Today, self.url)
                    self.url = self.url_list.pop(0)
                    page = 0
                    break
            if page == 20:
                self.url = self.url_list.pop(0)
                page = 0

    def parse_detile(self, title, url, date):
        print(url)
        t = tool.requests_get(url, self.headers).replace('\xa9', '').replace('<br>&nbsp;&nbsp;', '')\
            .replace('</o:p><', '').replace('<o:p><', '')
        # print(t)
        # time.sleep(2222)
        url_html = etree.HTML(t)
        detail = url_html.xpath("//div[@class='wrap']/div")[0]
        detail_html = etree.tostring(detail, method='HTML')
        detail_html = html.unescape(detail_html.decode()).replace("display: none", '').replace("\u2022", '').replace('\xa0', '')
        detail_text = detail_html.replace('\xa0', '').replace('\n',
                                                                                                             ''). \
            replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
        # if len(detail_html) < 200:
        #     int('a')
        item = {}
        item['title'] = title.replace('\u2022', '')
        item['url'] = url
        item['date'] = date
        item['typeid'] = tool.get_typeid(item['title'])
        item['senddate'] = int(time.time())
        item['mid'] = 867
        item['nativeplace'] = float(tool.get_title_city(item['title']))
        item['infotype'] = tool.get_infotype(item['title'])
        item['body'] = tool.qudiao_width(detail_html)
        item['endtime'] = tool.get_endtime(detail_text)
        if item['endtime'] == '':
            print(date)
            item['endtime'] =date
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
        item['resource'] = '中国五矿'
        item["shi"] = int(item["nativeplace"])
        if len(str(item["nativeplace"])) == 4:
            item['sheng'] = int(str(item["nativeplace"])[:2] + '00')
        elif len(str(item["nativeplace"])) == 5:
            item['sheng'] = int(str(item["nativeplace"])[:3] + '00')
        else:
            item['sheng'] = 0
        item['removal']= title
        # process_item(item)
        print(item)


if __name__ == '__main__':
    import traceback,os
    try:
        jl = wenshan_ggzy()
        jl.get_code()
        # jl.parse()

    except Exception as e:
        traceback.print_exc()
        tool.send_error('报错文件：'+str(os.path.basename(__file__))+'报错信息：'+str(e))


