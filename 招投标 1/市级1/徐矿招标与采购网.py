# -*- coding: utf-8 -*-
import json
import re
import time, html
from lxml import etree
import tool
from save_database import process_item

# 徐矿招标与采购网
class alashan_ggzy:
    def __init__(self):
        self.url_code = [
            'http://bid.xkjt.net/bid_ol/bulletinWeb/getTenderBulletinList.do?purchase=2&type=1&sortDesc=2&pageIndex={}&pageSize=11',
            'http://bid.xkjt.net/bid_ol/bulletinWeb/getTenderBulletinList.do?purchase=2&type=2&sortDesc=2&pageIndex={}&pageSize=11',
            'http://bid.xkjt.net/bid_ol/bulletinWeb/getTenderBulletinList.do?purchase=2&type=3&sortDesc=2&pageIndex={}&pageSize=11',
            'http://bid.xkjt.net/bid_ol/bulletinWeb/getChangeBulletinList.do?sortDesc=2&pageIndex={}&pageSize=11',
            'http://bid.xkjt.net/bid_ol/bulletinWeb/getsingleBulletinList.do?sortDesc=2&pageIndex={}&pageSize=11',
            'http://bid.xkjt.net/bid_ol/bulletinWeb/getTenderBulletinList.do?purchase=3&sortDesc=2&pageIndex={}&pageSize=11',
            'http://bid.xkjt.net/bid_ol/awardWeb/getWinCandidateBulletinList.do?type=1&sortDesc=2&pageIndex={}&pageSize=11',
            'http://bid.xkjt.net/bid_ol/awardWeb/getWinCandidateBulletinList.do?type=2&sortDesc=2&pageIndex={}&pageSize=11',
            'http://bid.xkjt.net/bid_ol/awardWeb/getWinCandidateBulletinList.do?type=3&sortDesc=2&pageIndex={}&pageSize=11',
            'http://bid.xkjt.net/bid_ol/awardWeb/getWinResultNoticeList.do?type=1&sortDesc=2&pageIndex={}&pageSize=11',
            'http://bid.xkjt.net/bid_ol/awardWeb/getWinResultNoticeList.do?type=2&sortDesc=2&pageIndex={}&pageSize=11',
            'http://bid.xkjt.net/bid_ol/awardWeb/getWinResultNoticeList.do?type=3&sortDesc=2&pageIndex={}&pageSize=11',
        ]
        self.url = self.url_code.pop(0)
        self.headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Cookie': 'SESSION=0ae3aba8-4507-4d56-92aa-03d82bdcd0cb',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
        }

    def parse(self):
        date = tool.date
        # date = '2021-04-07'
        page = 0
        while True:
            page += 1
            print('*' * 20, page, '*' * 20)
            text = tool.requests_get(self.url.format(page), self.headers)
            # print(111, self.url.format(page), text)
            # time.sleep(6666)
            detail = json.loads(text)['list']
            for li in detail:
                try:
                    title = li['bulletinName']
                except:
                    title = li['publicityName']
                url = li['id']
                #http://bid.xkjt.net/bid_ol/awardWeb/detail.do?id=d3e1c23546cc46189298125c25a18e1a
                #http://bid.xkjt.net/bid_ol/bulletinWeb/detail.do?id=7059d77cf55e430794c61c7b0728c822
                url_code = re.findall('bid_ol/(.*?)/get', self.url)[0]
                url = 'http://bid.xkjt.net/bid_ol/{}/detail.do?id={}'.format(url_code, li['id'])
                date_Today = li['bulletinIssueTime'][:10].replace('\r', '').replace('\t', '').replace(' ', '')
                if '-' not in date_Today:
                    date_Today = date_Today[:4] + '-' + date_Today[4:6] + '-' + date_Today[6:8]
                # print(title, url, date_Today)
                # time.sleep(666)
                if tool.Transformation(date) <= tool.Transformation(date_Today):
                    if tool.removal(title, date):
                        self.parse_detile(title, url, date_Today)
                    else:
                        print('【existence】', url)
                        continue
                else:
                    print('日期不符, 正在切换类型...', date_Today, self.url)
                    self.url = self.url_code.pop(0)
                    page = 0
                    break


    def parse_detile(self, title, url, date):
        print(url)
        url_text = tool.requests_get(url, self.headers)
        url_html = etree.HTML(url_text)
        try:
            detail = url_html.xpath('//*[@id="bulletinContent"]/div')[0]
            detail_html = etree.tostring(detail, method='HTML')
            detail_html = html.unescape(detail_html.decode()).replace('\xa0', '')
            detail_text = url_html.xpath('string(//*[@id="bulletinContent"]/div)').replace('\xa0', '').replace('\n', '').replace('\r', '').replace('\t',
                                                                                                                      '').replace(
                ' ', '').replace('\xa5', '')
        except:
            detail = url_html.xpath('//*[@id="bulletinContent"]')[0]
            detail_html = etree.tostring(detail, method='HTML')
            detail_html = html.unescape(detail_html.decode()).replace('\xa0', '')
            detail_text = url_html.xpath('string(//*[@id="bulletinContent"])').replace('\xa0', '').replace('\n',
                                                                                                               '').replace(
                '\r', '').replace('\t',
                                  '').replace(
                ' ', '').replace('\xa5', '')
        item = {}
        item['title'] = title.replace('\u2022', '')
        item['url'] = url
        item['date'] = date
        item['typeid'] = tool.get_typeid(item['title'])
        item['senddate'] = int(time.time())
        item['mid'] = 867
        item['nativeplace'] = float(tool.get_city(item['title']))
        if item['nativeplace'] == 0:
            item['nativeplace'] = float(tool.more(item['title']+detail_text))
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
        item['resource'] = '徐矿招标与采购网'
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
        if 'pop from empty list'!=str(e):
            print('报错')
            with open('../error_name.txt', 'a+', encoding='utf-8')as f:
                f.write(str(os.path.basename(__file__)))
                f.write('\n')
                f.write(str(traceback.format_exc()))
                f.write('\n')
        else:
            with open('../success.txt', 'a+', encoding='utf-8')as f:
                f.write(str(os.path.basename(__file__)))
                f.write('\n')
                f.write(str('无连接抓取'))
                f.write('\n')

