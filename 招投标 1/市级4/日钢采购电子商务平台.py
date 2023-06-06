# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
import datetime
from save_database import process_item

# 日钢采购电子商务平台
class wenshan_ggzy:
    def __init__(self):
        self.url_list = [
            'https://ep.rizhaosteel.com/api/bid/getBidList', #工程招标
           ]
        self.url = self.url_list.pop(0)
        self.headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'}
    def parse(self):
        date = tool.date
        # date = '2020-09-21'
        page = 0
        while True:
            page += 1
            data={"loading":True,"msg":"请稍候","_source":"PC","pageIndex":page,"pageSize":10,"projectMethod":"B","orderBy":"","asc":False,"searchKey":None}
            text = tool.requests_post_to(url=self.url, headers=self.headers,data=data)
            print('*' * 20, page, '*' * 20)
            html = json.loads(text)
            # print(11, text)
            # time.sleep(6666)
            detail = html["items"]
            for li in detail:
                title = li["projectname"]
                projectNo = li["projectno"]
                date_Today = li["senddate"][:4] + '-' + li["senddate"][4:6] + '-' + li["senddate"][6:8]
                url = 'https://ep.rizhaosteel.com/api/bid/getBidDetail'

                # print(title, url, date_Today)
                # time.sleep(666)
                # self.parse_detile(title, url, date_Today,projectNo)
                if tool.Transformation(date) <= tool.Transformation(date_Today):
                    if tool.removal(title, date):
                        self.parse_detile(title, url, date_Today,projectNo)
                    else:
                        print('【existence】', url)
                        continue
                else:
                    print('日期不符, 正在切换类型', date_Today)
                    self.url = self.url_list.pop(0)
                    page = 0
                    break
            if page == 20:
                print('日期不符, 正在切换类型')
                self.url = self.url_list.pop(0)
                break

    def parse_detile(self, title, url, date,projectNo):
        print(url)
        data2 = {"loading": True, "msg": "请稍候", "_source": "PC", "projectNo": projectNo, "pageSize": 10,
                 "pageIndex": 1}
        t = tool.requests_post_to(url=url,headers=self.headers,data=data2)
        # print(t)
        # time.sleep(2222)
        url_html = json.loads(t)
        projectname = url_html["bidDetail"]["projectname"]
        notice = url_html["bidDetail"]["notice"]
        payWay = url_html["bidDetail"]["payWay"]
        sremark = url_html["bidDetail"]["sremark"]
        deptname = url_html["bidDetail"]["deptname"]
        inventoryName = url_html["bidDetail"]["inventoryName"]
        sendDateShow = url_html["bidDetail"]["sendDateShow"]
        isSignUp = url_html["bidDetail"]["isSignUp"]
        sendTimeShow = url_html["bidDetail"]["sendTimeShow"]
        bidEndDateShow = url_html["bidDetail"]["bidEndDateShow"]
        bidEndTimeShow = url_html["bidDetail"]["bidEndTimeShow"]
        index_url=f'https://ep.rizhaosteel.com/bid/forecastDetail?projectNo={projectNo}'
        detail = f'''
            <div id="RZ"><div class="bg_f3f3f3"><div class="w1200 of"><div class="fl" style="width: 925px;"><div class="bg_f3f3f3 lh40 of" style="border-left: 1px solid rgb(222, 222, 222); border-right: 1px solid rgb(222, 222, 222);"><div class="fl c_blue"><i class="f10 iconfont icon-triangle-tright fl ml5"></i> <span class="fl">预报名公告</span> <span class="c_333 ml10"> {projectname}</span></div></div> <div class="bd_gray bg_fff yubaoming-table pr"><img src="/statics/img/icon/red_line.png" alt="" class="pa" style="left: 0px; top: 0px;"> <span class="c_fff pa disib w60 tl" style="transform: rotate(-45deg);">{isSignUp}</span> <table><colgroup><col style="width: 140px;"> <col style="width: 321px;"> <col style="width: 140px;"> <col style="width: 321px;"></colgroup> <tbody><tr><td>项目编号</td> <td>BO23030092</td> <td>项目分类</td> <td>{inventoryName}</td></tr> <tr><td>招标部门</td> <td>{deptname}</td> <td>发布时间</td> <td>{sendDateShow} {sendTimeShow}</td></tr> <tr><td>报名起止时间</td> <td>{sendDateShow} {sendTimeShow} ~ {bidEndDateShow} {bidEndTimeShow}
            </td> <td>附件</td> <td><div><a class="c_blue"> 报名后可见 </a></div></td></tr></tbody></table></div></div> <div class="fl" style="width: 274px;"><div class="yubaoming"><div class="pt50 ml15 mb20">距离预报名截止时间还剩：</div> <div class="new_tile h40 c_fff ml15"><span class="num num0"></span> <span class="num num3"></span> <span class="num num0"></span> <span class="num num7"></span> <span class="num num0"></span> <span class="num num5"></span> <span class="num num1"></span> <span class="num num3"></span></div> <div class="tc pb20"><!----> <a href="/provider/login" class="bg_blue h32 lh32 b_r_5 c_fff w160">登录后报名</a> <a href="/provider/register/">没有账号？点我注册</a> <!----> <!----> <!----> <!----> <!----></div></div></div></div> <div class="w1200"><div class="bg_fff bd_gray mt10" style="display: none;"><div class="tc f15 fb lh60"><img src="/statics/img/icon/xuqiu.png" alt="" width="35px"> 需求明细</div> <div class="pl10 pr10"><div class="el-table table_main_style el-table--fit el-table--enable-row-hover" style="width: 100%;"><div class="hidden-columns"></div><div class="el-table__header-wrapper"><table cellspacing="0" cellpadding="0" border="0" class="el-table__header"><colgroup><col name="gutter" width="0"></colgroup><thead class="has-gutter"><tr class=""><th class="gutter" style="width: 0px; display: none;"></th></tr></thead></table></div><div class="el-table__body-wrapper is-scrolling-none"><table cellspacing="0" cellpadding="0" border="0" class="el-table__body"><colgroup></colgroup><tbody><!----></tbody></table><div class="el-table__empty-block" style="height: 100%;"><span class="el-table__empty-text">暂无数据</span></div><!----></div><!----><!----><!----><!----><div class="el-table__column-resize-proxy" style="display: none;"></div></div> <div class="page mt10 mb10 of"><div class="fr el-pagination is-background"><span class="el-pagination__total">共 0 条</span><span class="el-pagination__sizes"><div class="el-select el-select--mini"><!----><div class="el-input el-input--mini el-input--suffix"><!----><input type="text" readonly="readonly" autocomplete="off" placeholder="请选择" class="el-input__inner"><!----><span class="el-input__suffix"><span class="el-input__suffix-inner"><i class="el-select__caret el-input__icon el-icon-arrow-up"></i><!----><!----><!----><!----><!----></span><!----></span><!----><!----></div><div class="el-select-dropdown el-popper" style="display: none;"><div class="el-scrollbar" style=""><div class="el-select-dropdown__wrap el-scrollbar__wrap" style="margin-bottom: -17px; margin-right: -17px;"><ul class="el-scrollbar__view el-select-dropdown__list"><!----><li class="el-select-dropdown__item selected"><span>10条/页</span></li><li class="el-select-dropdown__item"><span>30条/页</span></li><li class="el-select-dropdown__item"><span>50条/页</span></li><li class="el-select-dropdown__item"><span>100条/页</span></li></ul></div><div class="el-scrollbar__bar is-horizontal"><div class="el-scrollbar__thumb" style="transform: translateX(0%);"></div></div><div class="el-scrollbar__bar is-vertical"><div class="el-scrollbar__thumb" style="transform: translateY(0%);"></div></div></div><!----></div></div></span><button type="button" disabled="disabled" class="btn-prev"><i class="el-icon el-icon-arrow-left"></i></button><ul class="el-pager"><li class="number active">1</li><!----><!----><!----></ul><button type="button" disabled="disabled" class="btn-next"><i class="el-icon el-icon-arrow-right"></i></button></div></div></div></div> <div class="bg_fff bd_gray mt10"><div class="tc f15 fb lh60"><img src="/statics/img/icon/gonggao.png" alt="" width="35px"> 公告说明</div> <div class="bd_gray bg_fff yubaoming-table pr"><table><colgroup><col style="width: 140px;"> <col style="width: 782px;"></colgroup> <tbody><tr><td>项目概况</td> <td><div>{notice}</div></td></tr> <tr><td>资质要求</td> <td>{payWay}
            </td></tr> <tr><td>技术要求</td> <td>{sremark}
            </td></tr> <tr><td>联系人/联系方式</td> <td><a class="c_blue"> 报名后可见 </a></td></tr></tbody></table></div></div></div></div> <div class="el-dialog__wrapper" style="display: none;"><div role="dialog" aria-modal="true" aria-label="当前项目不具备投标资格" class="el-dialog el-dialog--center" style="margin-top: 15vh; width: 300px;"><div class="el-dialog__header"><span class="el-dialog__title">当前项目不具备投标资格</span><button type="button" aria-label="Close" class="el-dialog__headerbtn"><i class="el-dialog__close el-icon el-icon-close"></i></button></div><!----><!----></div></div> <div class="el-dialog__wrapper" style="display: none;"><div role="dialog" aria-modal="true" aria-label="快捷报名" class="el-dialog el-dialog--center" style="margin-top: 15vh; width: 340px;"><div class="el-dialog__header"><span class="el-dialog__title">快捷报名</span><button type="button" aria-label="Close" class="el-dialog__headerbtn"><i class="el-dialog__close el-icon el-icon-close"></i></button></div><!----><div class="el-dialog__footer"><span class="dialog-footer"><button type="button" class="el-button el-button--primary"><!----><!----><span>确认报名</span></button> <button type="button" class="el-button el-button--default"><!----><!----><span>取 消</span></button></span></div></div></div></div>
            '''

        # detail_html = etree.tostring(detail, method='HTML')
        # detail_html = html.unescape(detail_html.decode()).replace("display: none", '')
        # detail_text = url_html.xpath('string(//div[@class="v_news_content"])').replace('\xa0', '').replace('\n', '').\
        #     replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
        if len(detail) < 200:
            int('a')
        item = {}
        item['title'] = title.replace('\u2022', '')
        item['url'] = index_url
        item['date'] = date
        item['typeid'] = tool.get_typeid(item['title'])
        item['senddate'] = int(time.time())
        item['mid'] = 867
        item['nativeplace'] = self.get_nativeplace(item['title'])
        item['infotype'] = tool.get_infotype(item['title'])
        item['body'] = tool.qudiao_width(detail)
        item['body'] = item['body']
        # print(item['body'].replace('\xa0', '').replace('\xa5', '').replace('\xb3', ''))
        # time.sleep(6666)
        item['endtime'] = tool.get_endtime(detail)
        if item['endtime'] == '':
            item['endtime'] = int(time.mktime(time.strptime(date, "%Y-%m-%d")))
        else:
            try:
                item['endtime'] = int(time.mktime(time.strptime(item['endtime'], "%Y-%m-%d")))
            except:
                item['endtime'] = int(time.mktime(time.strptime(date, "%Y-%m-%d")))
        item['tel'] = tool.get_tel(detail)
        item['email'] = ''
        item['address'] = tool.get_address(detail)
        item['linkman'] = tool.get_linkman(detail)
        item['function'] = tool.get_function(detail)
        item['resource'] = '日钢采购电子商务平台'
        item['shi'] = 6507
        item['sheng'] = 6500
        item['removal']= title
        # print(item["url"])
        process_item(item)
    def get_nativeplace(self, addr):
        city = ''
        city_list = [['6507.001', '铜官山区'], ['6507.002', '狮子山区'], ['6507.003', '郊区'], ['6507.004', '铜陵县']]

        for i in city_list:
            if i[1] in addr:
                city = float(i[0])
                break
        if city == '':
            city = 6507
        return city

if __name__ == '__main__':
    import os,traceback
    try:
        jl = wenshan_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
        tool.send_error('报错文件：'+str(os.path.basename(__file__))+'报错信息：'+str(e))



