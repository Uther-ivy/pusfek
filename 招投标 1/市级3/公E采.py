# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 玉林市公共资源交易中心
class wenshan_ggzy:
    def __init__(self):
        self.domain_name = 'http://www.cfcpn.com'
        self.url_list = [

        ]

        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',

        }

    def parse(self):
        date = tool.date
        # date = '2020-09-27'
        page = 0
        while True:
            page += 1
            url=f'https://www.enjoy5191.com/api/GetDataHandler.ashx?ieTime={int(time.time()*10)}&in_FILLING_ORGANIZATION=x30001,x30002&method=Web.GYC_GetProjectList&pageindex={page}&pagesize=15&in_big_type=D%2CQ&NAME=&AREA_CODE=35&PUBLISHED_TIME_START=2012-12-29&PUBLISHED_TIME_END=2022-12-27&STATUS=&TENDERER_NAME=&CODE=&UNIT_NAME=&TENDER_PROJECT_WAY=%E5%85%AC%E5%BC%80%E6%8B%9B%E6%A0%87'
            payload = {
                'noticeType':  1,
                'pageSize': 10,
                'pageNo': page,
                'noticeState': 1,
                'isValid': 1,
                'orderBy': 'publish_time desc'

                }
            text = tool.requests_get(url , self.headers)
            print('*' * 20, page, '*' * 20)
            # print(11, text.replace('\ufffd', ' ').replace('\u30fb', ' '))
            # time.sleep(6666)
            detail = json.loads(text)['data']
            for li in detail:
                title = li['NAME']
                cid= li['SOURCE_ID']
                url = li['URL']
                city=li['AREANAME']
                date_Today = li['PUBLISHED_TIME']
                if 'http' not in url:
                    url = self.domain_name + url
                print(title, url, date_Today)
                # time.sleep(666)
                # endtime=re.findall(r'\d{4}-\d{2}-\d{2}', li['endtime'])[0]
                date_Today = re.findall(r'\d{4}-\d{2}-\d{2}', date_Today)[0]
                if tool.Transformation(date) <= tool.Transformation(date_Today):
                    if tool.removal(title, date):
                        self.parse_detile(title, url, date_Today,city,cid)
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

    def parse_detile(self, title, url, date,city,cid):
        jsonurl=f'https://qycg.enjoy5191.com/Search/GetData?ieTime={int(time.time()*1000)}&method=Search.GetProInfoReleaseByID&project_id={cid}'
        print(jsonurl)
        data={
            'id': cid,
            'isDetail': 1
        }
        t = tool.requests_get(jsonurl, self.headers).replace('\xa9', '').replace('<br>&nbsp;&nbsp;', '')\
            .replace('</o:p><', '').replace('<o:p><', '')
        # print(t)
        for data in json.loads(t)['data']['data']:
            # print(data)
            cdata=data['VALUE'].replace('\\','').replace('true','True').replace('false','False')
            jsondata=eval(cdata)
            # print(type(jsondata))
            # for data in jsondata['BidPacket']:
            #     print(data)
            htmls=f"""
        <div data-v-20b3b080="">
    <p data-v-20b3b080="">项目所在地区：<span data-v-20b3b080="" class="fill">{jsondata['ADMINISTRATIVE_AREA']}</span></p>
    <p data-v-20b3b080="">招标条件</p>
    <p data-v-20b3b080="" class="text-indent2">
        受<span data-v-20b3b080="" class="fill">{jsondata['SUPERVISE_DEPT']}</span>委托，<span data-v-20b3b080="" class="fill">{jsondata['PURCHASER_AGENCY_NAME']}</span>对<span
            data-v-20b3b080="" class="fill">{jsondata['NOTICE_TITLE']}</span>项目组织进行<span
            data-v-20b3b080="" class="fill">{jsondata['PURCHASE_METHOD']}</span>，项目资金为<span data-v-20b3b080=""
                                                                            class="fill">{jsondata['FUND_SOURCE']}</span>。本项目已具备招标条件，
        现欢迎国内合格的投标人前来投标。
    </p>
    <p data-v-20b3b080="">项目概况和招标范围</p>
    <p data-v-20b3b080="">
        规模：<span data-v-20b3b080="" class="fill">{jsondata['PROGRAM_BUDGET']}</span></p>
    <p data-v-20b3b080="">
        范围：本招标项目划分为<span data-v-20b3b080="" class="fill">{jsondata['BidPacket'][0]['Sort']}</span>个合同包，本次招标为其中的：
    </p>
    <p data-v-20b3b080="" class="text-indent2">
        合同包<span data-v-20b3b080="" class="fill">{jsondata['BidPacket'][0]['SerialNumber']}</span>： 项目名称：
        <span data-v-20b3b080="" class="fill">{jsondata['BidPacket'][0]['Name']}</span>
        ，采购预算：<span data-v-20b3b080="" class="fill">{jsondata['PROGRAM_BUDGET']}</span> ，项目内容：<span data-v-20b3b080="" class="fill">{jsondata['BidPacket'][0]['Content']}</span>
    </p>
    
    <p data-v-20b3b080="">招标文件的获取</p>
    <p data-v-20b3b080="" class="text-indent2">
        1、获取时间：从<span data-v-20b3b080="" class="fill">{jsondata['TENDER_SELLING_START_TIME']}</span>到<span data-v-20b3b080=""
                                                                                               class="fill">{jsondata['TENDER_SELLING_END_TIME']}</span>
    </p>
    <p data-v-20b3b080="" class="text-indent2">2、获取方式：</p>
    <p data-v-20b3b080="" class="text-indent2">
        文件售价：
        </p>
    <p data-v-20b3b080="" class="text-indent2"><span data-v-20b3b080="" class="fill">{jsondata['TENDER_DOC_GET_METHOD']}</span>
    </p>
    <p data-v-20b3b080="">投标文件的递交</p>
    <p data-v-20b3b080="" class="text-indent2">
        1、递交截止时间：<span data-v-20b3b080="" class="fill">{jsondata['DEPOSIT_SUBMISSION_END_TIME']}</span></p>
    <p data-v-20b3b080="" class="text-indent2">
        2、递交方式及地点：<span data-v-20b3b080=""
                               class="fill">{jsondata['RESPONSEFILE_WAY_ADDRESS']}</span></p>
    <p data-v-20b3b080="">
        开标时间及地点
    </p>
    <p data-v-20b3b080="" class="text-indent2">
        1、开标时间：<span data-v-20b3b080="" class="fill">{jsondata['DEPOSIT_SUBMISSION_END_TIME']}</span></p>
    <p data-v-20b3b080="" class="text-indent2">
        2、开标地点：<span data-v-20b3b080="" class="fill">{jsondata['BID_OPEN_PLACE']}</span></p>
    <p data-v-20b3b080="">七、其他</p>
    <p data-v-20b3b080="" class="text-indent2"><span data-v-20b3b080="" class="fill">{jsondata['BID_OTHERS']}</span></p>
    <p data-v-20b3b080="">八、监督部门</p>
    <p data-v-20b3b080="" class="text-indent2"><span data-v-20b3b080="" class="fill">{jsondata['SUPERVISE_DEPT']}</span></p>
    <p data-v-20b3b080="">九、联系方式</p>
    <p data-v-20b3b080="" class="text-indent2">
        1、招标人：<span data-v-20b3b080="" class="fill">{jsondata['SUPERVISE_DEPT']}</span></p>
    <p data-v-20b3b080="" class="text-indent2">
        地址：<span data-v-20b3b080="" class="fill">{jsondata['PURCHASER_ADDRESS']}</span></p>
    <p data-v-20b3b080="" class="text-indent2">
        联系人：<span data-v-20b3b080="" class="fill">{jsondata['PURCHASER_CONTACTOR']}</span></p>
    <p data-v-20b3b080="" class="text-indent2">
        联系电话：<span data-v-20b3b080="" class="fill">{jsondata['PURCHASER_INFORMATION']}</span></p>
    <p data-v-20b3b080="" class="text-indent2">
        2、招标代理机构：<span data-v-20b3b080="" class="fill">{jsondata['PURCHASER_AGENCY_NAME']}</span></p>
    <p data-v-20b3b080="" class="text-indent2">
        地址：<span data-v-20b3b080="" class="fill">{jsondata['PURCHASER_AGENCY_ADDRESS']}</span></p>
    <p data-v-20b3b080="" class="text-indent2">
        联系人：<span data-v-20b3b080="" class="fill">{jsondata['PURCHASER_AGENCY_CONTACTOR']}</span></p>
    <p data-v-20b3b080="" class="text-indent2">
        联系电话：<span data-v-20b3b080="" class="fill">{jsondata['PURCHASER_AGENCY_INFORMATION']}</span></p> <!----></div>
            
            """
            # time.sleep(2222)
            detail = etree.HTML(htmls)
            detail_html = etree.tostring(detail, method='HTML')
            detail_html = html.unescape(detail_html.decode()).replace("display: none", '').replace("\u2022", '').replace('\xa0', '')
            detail_text = detail_html.replace('\xa0', '').replace('\n',''). \
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
            item['nativeplace'] = float(tool.get_title_city(city))
            item['infotype'] = tool.get_infotype(item['title'])
            item['body'] = tool.qudiao_width(detail_text)

            item['endtime'] = tool.get_endtime(date)
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
            item['resource'] = '公E采'
            item["shi"] = int(item["nativeplace"])
            if len(str(item["nativeplace"])) == 4:
                item['sheng'] = int(str(item["nativeplace"])[:2] + '00')
            elif len(str(item["nativeplace"])) == 5:
                item['sheng'] = int(str(item["nativeplace"])[:3] + '00')
            else:
                item['sheng'] = 0
            item['removal']= title
            process_item(item)
            # print(item)


if __name__ == '__main__':
    import traceback,os
    try:
        jl = wenshan_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
        tool.send_error('报错文件：'+str(os.path.basename(__file__))+'报错信息：'+str(e))


