# -*- coding: utf-8 -*-
import json
import random
import re
import time, html
from lxml import etree
import tool
from save_database import process_item

# 上海地铁采购电子商务平台
class alashan_ggzy:
    def __init__(self):
        self.url_code = [
            # 'http://eps.shmetro.com/portal/DispatchAction.do?efFormEname=PF9001&type=00&orgCode=STJT',
            # 'http://eps.shmetro.com/portal/DispatchAction.do?efFormEname=PF9001&type=10&orgCode=STJT',
            # 'http://eps.shmetro.com/portal/DispatchAction.do?efFormEname=PF9001&type=20&orgCode=STJT',
            # 'http://eps.shmetro.com/portal/DispatchAction.do?efFormEname=PF9001&type=60&orgCode=STJT',
            'http://eps.shmetro.com/portal/DispatchAction.do?efFormEname=PF9001&type=50&orgCode=STJT',
            # 'http://eps.shmetro.com/portal/DispatchAction.do?efFormEname=PF9001&type=40&orgCode=STJT'
        ]
        self.url = self.url_code.pop(0)
        self.headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            # 'Cookie': 'isInitAreaCode=null; _gscu_653689772=78282348u2bs1g18; _gscbrs_653689772=1; UM_distinctid=16f78f570621fa-0e76a94f9f3d2d-e343166-1fa400-16f78f570631fc; _gscs_653689772=t782895054fvlkv12|pv:14; CNZZDATA1260595804=985342442-1578282342-%7C1578291895',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
        }

    def parse(self):
        date = tool.date
        # date = '2020-01-06'
        page = 0
        detail=''
        while True:
            page += 1
            print('*' * 20, page, '*' * 20)
            if page == 1:
                text = tool.requests_get(self.url, self.headers).replace('&#x2f;', '/')
                detail = json.loads(re.findall('var __ei=(.*?);.*?var __eiInfo', text, re.S)[0])['blocks']['edit']['rows']

            elif page  > 71:
                url='http://eps.shmetro.com/portal/EiService'
                rows=json.dumps(detail)
                eiinfo = '{attr:{`totalcount`:844,`limit`:10,`efCurButtonEname`:``,`totalPageCount`:85,`packageName`:``,`efFormEname`:`PF9001`,`efCurFormEname`:`PF9001`,`efFormStyle`:`00`,`efFormCname`:`在线交易`,`serviceName`:`PF9001`,`__$$DIAGNOSE$$__`:``,`efFormButtonDesc`:``,`efFormLoadPath`:`/PF/PF9001.jsp`,`currentPage`:' + str(
                    page) + ',`efFormPopup`:``,`methodName`:`initLoad`,``:`null`,`efFormTime`:``,`efFormInfoTag`:``,`efSecurityToken`:`3Z4NNX9W70EXM8XRRYDD4J4UN`,`COOKIE`:`uoNosce3KsloUmvPWOZOCsTs02AKntPvly77jvMZiQjKn9vLVuBO!-1081333352!1681088694199`,`query`:`  查 询  `,`ef_grid_result_jumpto`:`2`,`perPageRecord`:`10`,`type`:`50`,`title`:``,`startRecCreateTime`:``,`endRecCreateTime`:``,`offset`:' + str(
                    (page - 1) * 10) + ',`orgCode`:`STJT`},blocks:{edit:{attr:{},meta:{attr:{},columns:[{name:`noticeNo`,descName:`公告主键`,type:`N`,scaleLength:0},{name:`noticeTitle`,descName:`公告标题`,type:`C`,scaleLength:0},{name:`noticeTime`,descName:`发布时间`,type:`C`,scaleLength:0},{name:`browseCs`,descName:`浏览次数`,type:`C`,scaleLength:0},{name:`laiyuan`,descName:`公告来源`,type:`C`,scaleLength:0},{name:`isCredit`,descName:`是否信用招标`,type:`C`,scaleLength:0}]},' \
                    'rows:'+str(rows)+'},inqu_status:{attr:{},meta:{attr:{},columns:[{name:`title`,descName:``,type:`C`,scaleLength:0},{name:`startRecCreateTime`,descName:``,type:`C`,scaleLength:0},{name:`endRecCreateTime`,descName:``,type:`C`,scaleLength:0}]},rows:[[``,``,``]]}}}',
                print(eiinfo)
                params= {
                    'service': 'PF9001',
                    'method': 'query',
                    'eiinfo': eiinfo,
                    'efSecurityToken': '3Z4NNX9W70EXM8XRRYDD4J4UN'}
                text=tool.requests_post_param(url,self.headers,param=params)
                detail = json.loads(text)['blocks']['edit']['rows']
                print(detail)
            else:
                continue
                # time.sleep(222)
                # text = tool.requests_get(self.url.format('index_'+str(page)), self.headers).replace('&#x2f;', '/')
            # print(detail)

            for li in detail:
                try:
                    title = li[1]
                    url = 'http://eps.shmetro.com/portal/DispatchAction.do?efFormEname=PF9003&&inqu_status-0-noticeNo={}&inqu_status-0-type=2&inqu_status-0-status={}'.format(li[0], li[4])
                    date_Today = li[2][:4]+'-'+li[2][4:6]+ '-' +li[2][6:]
                    print(title, url, date_Today)

                    if tool.Transformation(date) <= tool.Transformation(date_Today):
                        # if tool.removal(title, date):
                            time.sleep(1 + random.random() * 10)
                            self.parse_detile(title, url, date_Today)
                        # else:
                            # print('【existence】', url)
                            # continue
                    else:
                        print('日期不符, 正在切换类型...', date_Today, self.url)
                        return
                except Exception:
                    traceback.print_exc()

    def parse_detile(self, title, url, date):
        print(url)

        url_text = tool.requests_get(url, self.headers)
        url_html = etree.HTML(url_text)
        detail = url_html.xpath('//*[@id="printSection"]/dl/div')[0]

        if detail:
            detail_html = etree.tostring(detail, method='HTML')
            detail_html = html.unescape(detail_html.decode())
            detail_text = url_html.xpath('string(//*[@id="printSection"]/dl/div)').replace('\xa0', '').replace('\n', '').replace('\r', '').replace('\t',
                                                                                                                      '').replace(
                ' ', '').replace('\xa5', '')
            item = {}
            item['title'] = title.replace('\u2022', '')
            item['url'] = url
            item['date'] = date
            item['typeid'] = tool.get_typeid(item['title'])
            item['senddate'] = int(time.time())
            item['mid'] = 867
            item['nativeplace'] = self.get_nativeplace(item['title']+detail_text)
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
            item['resource'] = '上海地铁采购电子商务平台'
            item['shi'] = 5000
            item['sheng'] = 5000
            item['removal']= title
            process_item(item)
        # print(item['nativeplace'], item['title'])

    def get_nativeplace(self, addr):
        city_list = [['5001', '黄浦区'], ['5002', '卢湾区'], ['5003', '徐汇区'], ['5004', '长宁区'], ['5005', '静安区'], ['5006', '普陀区'], ['5007', '闸北区'], ['5008', '虹口区'], ['5009', '杨浦区'], ['5010', '闵行区'], ['5011', '宝山区'], ['5012', '嘉定区'], ['5013', '浦东新区'], ['5014', '金山区'], ['5015', '松江区'], ['5016', '青浦区'], ['5017', '南汇区'], ['5018', '奉贤区'], ['5019', '崇明县']]

        for i in city_list:
            if i[1] in addr:
                return float(i[0])
        return 5000

if __name__ == '__main__':
    import traceback, os
    try:
        jl = alashan_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
        if 'pop from empty list'!=str(e):
            print('报错')
            with open('error_name.txt','a+',encoding='utf-8')as f:
                f.write(str(os.path.basename(__file__)))
                f.write('\n')
                f.write(str(traceback.format_exc()))
                f.write('\n')
        else:
            with open('success.txt','a+',encoding='utf-8')as f:
                f.write(str(os.path.basename(__file__)))
                f.write('\n')
                f.write(str('无连接抓取'))
                f.write('\n')

