# -*- coding: utf-8 -*-
import json
import re
import time, html
from lxml import etree
import tool
from save_database import process_item


# 阿拉善公共资源交易网
class alashan_ggzy:
    def __init__(self):
        self.url_code = [
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
        self.code = self.url_code.pop(0)
        self.headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Cookie': 'isInitAreaCode=null; _gscu_653689772=78282348u2bs1g18; _gscbrs_653689772=1; UM_distinctid=16f78f570621fa-0e76a94f9f3d2d-e343166-1fa400-16f78f570631fc; _gscs_653689772=t782895054fvlkv12|pv:14; CNZZDATA1260595804=985342442-1578282342-%7C1578291895',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
        }

    def parse(self):
        date = tool.date
        # date = '2020-01-06'
        page = 0
        while True:
            page += 1
            url = 'http://www.alsggzyjy.cn/PublicServer/commonAnnouncementAction/getCommonAnnouncementList.do?businessType={}&announcementType={}&page={}&rows=15&areaCode=152900'
            if self.code[0] == '003' and self.code[1] == '2':
                url = 'http://www.alsggzyjy.cn/PublicServer/commonAnnouncementAction/getAnnsByBulletinList.do?businessType={}&announcementType={}&page={}&rows=15&areaCode=152900'
            print('*' * 20, page, '*' * 20)
            text = tool.requests_get(url.format(self.code[1], self.code[0], page), self.headers)
            # print(url.format(self.code[1], self.code[0], page))
            # print(111, text)
            # time.sleep(666)
            detail = json.loads(text)['data']['list']
            for i in detail:
                title = i['title']
                url = 'http://www.alsggzyjy.cn/PublicServer/public/commonAnnouncement/showDetail.html?businessType=2&sidebarIndex={}&id='.format(
                    int(self.code[0][2]) + 1) + i['id']
                date_Today = i['publishTime'][:10]
                # print(title, url, date_Today)
                # time.sleep(666)
                if tool.Transformation(date) <= tool.Transformation(date_Today):
                    if tool.removal(title, date):
                        self.parse_detile(title, url, date_Today)
                    else:
                        print('【existence】', url)
                        continue
                else:
                    print('日期不符, 正在切换类型...', date_Today, self.code)
                    self.code = self.url_code.pop(0)
                    page = 0
                    break
            if page == 20:
                self.code = self.url_code.pop(0)
                page = 0

    def parse_detile(self, title, url, date):
        print(url)
        url_p = 'http://www.alsggzyjy.cn/PublicServer/commonAnnouncementAction/selectPublishAnnouncementById.do'
        url_code = re.findall('id=(.*?)==', url + '==')[0]
        data = {'id': url_code}
        url_post = json.loads(tool.requests_post(url_p, data, self.headers))['data']['announcement']['content']
        url_html = etree.HTML(url_post)
        detail_text = url_html.xpath('string(.)').replace('\xa0', '').replace('\n', '').replace('\r', '').replace('\t',
                                                                                                                  '').replace(
            ' ', '').replace('\xa5', '')
        # print(detail_text.replace('\xa0','').replace('\xa5',''))
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
        item['body'] = url_post
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
        item['resource'] = '阿拉善公共资源交易网'
        item['shi'] = 3012
        item['sheng'] = 3000
        item['removal']= title
        process_item(item)

    def get_nativeplace(self, addr):
        city = ''
        city_list = [['3012', '阿拉善盟'], ['3012.001', '阿拉善左旗'], ['3012.002', '阿拉善右旗'], ['3012.003', '额济纳旗']]

        for i in city_list:
            if i[1] in addr:
                city = float(i[0])
                break
        if city == '':
            city = 3012
        return city

if __name__ == '__main__':
    import traceback, os
    try:
        jl = alashan_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
        tool.send_error('报错文件：'+str(os.path.basename(__file__))+'报错信息：'+str(e))


