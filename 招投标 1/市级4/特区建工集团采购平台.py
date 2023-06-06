# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 特区建工集团采购平台
class wenshan_ggzy:
    def __init__(self):
        self.url_list = [
            'https://zcpt.szcg.cn/group-tendering/officialwebsite/project/page?announcementType=1&tenderProjectType=D02&size=10&current={}&ext=', #招标公告
                    ]
        self.url = self.url_list.pop(0)
        self.headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'}
    def parse(self):
        date = tool.date
        # date = '2020-09-21'
        page = 0
        while True:
            page += 1
            text = tool.requests_get(url=self.url.format(page), headers=self.headers)
            print('*' * 20, page, '*' * 20)
            html = json.loads(text)
            # print(11, text)
            # time.sleep(6666)
            detail = html["data"]["records"]
            for li in detail:
                title = li["announcementName"]
                date_Today = li["releaseTime"].split(' ')[0]
                projectId = li["projectId"]
                url = f'https://zcpt.szcg.cn/group-tendering/officialwebsite/project/announcementInfoDetail/{projectId}'
                # print(title, url, date_Today)
                # time.sleep(666)
                # self.parse_detile(title, url, date_Today,projectId)
                if tool.Transformation(date) <= tool.Transformation(date_Today):
                    if tool.removal(title, date):
                        self.parse_detile(title, url, date_Today,projectId)
                    else:
                        print('【existence】', url)
                        continue
                else:
                    print('日期不符, 正在切换类型', date_Today)
                    self.url = self.url_list.pop(0)
                    break
            if page == 20:
                print('日期不符, 正在切换类型')
                self.url = self.url_list.pop(0)
                break

    def parse_detile(self, title, url, date,projectId):
        print(url)
        t = tool.requests_get(url=url, headers=self.headers)
        # print(t)
        # time.sleep(2222)
        url_html = json.loads(t)
        projectName = url_html["data"]["projectInfo"]["projectName"]
        tenderProjectTypeDesc = url_html["data"]["projectInfo"]["tenderProjectTypeDesc"]
        purchaseProcessDesc = url_html["data"]["projectInfo"]["purchaseProcessDesc"]
        tenderModeDesc = url_html["data"]["projectInfo"]["tenderModeDesc"]
        tenderOrganizeFormDesc = url_html["data"]["projectInfo"]["tenderOrganizeFormDesc"]
        gradeMethodDesc = url_html["data"]["projectInfo"]["gradeMethodDesc"]
        qualificationMethodDesc = url_html["data"]["projectInfo"]["qualificationMethodDesc"]
        fundSourceDesc = url_html["data"]["projectInfo"]["fundSourceDesc"]
        try:
            quotationMethodDesc = url_html["data"]["projectInfo"]["quotationMethodDesc"]
        except:
            quotationMethodDesc = ""
        address = url_html["data"]["projectInfo"]["address"]
        industriesLatterTypeDesc = url_html["data"]["projectInfo"]["industriesLatterTypeDesc"]
        industriesNumberTypeDesc = url_html["data"]["projectInfo"]["industriesNumberTypeDesc"]
        tendererContent = url_html["data"]["projectInfo"]["tendererContent"]
        packageName = url_html["data"]["projectInfo"]["packageName"]
        legalPerson = url_html["data"]["projectInfo"]["legalPerson"]
        connector = url_html["data"]["projectInfo"]["connector"]
        companyAddress = url_html["data"]["projectInfo"]["companyAddress"]
        foreignContactPhone = url_html["data"]["projectInfo"]["foreignContactPhone"]
        superviseDeptName = url_html["data"]["projectInfo"]["superviseDeptName"]
        packageLatterTypeDesc = url_html["data"]["projectInfo"]["packageLatterTypeDesc"]
        projectNo = url_html["data"]["projectInfo"]["projectNo"]
        name = url_html["data"]["announcementVO"]["baseInfo"]["name"]
        startTime = url_html["data"]["announcementVO"]["baseInfo"]["startTime"]
        publishTime = url_html["data"]["announcementVO"]["baseInfo"]["publishTime"]
        message = url_html["data"]["announcementVO"]["baseInfo"]["message"]
        tenderDocGetTime = url_html["data"]["announcementVO"]["detail"]["tenderDocGetTime"]
        tenderDocDeadLine = url_html["data"]["announcementVO"]["detail"]["tenderDocDeadLine"]
        tenderQuestionDeadline = url_html["data"]["announcementVO"]["detail"]["tenderQuestionDeadline"]
        tenderAnswerDeadline = url_html["data"]["announcementVO"]["detail"]["tenderAnswerDeadline"]
        bidDocReferEndTime = url_html["data"]["announcementVO"]["detail"]["bidDocReferEndTime"]
        openBidTime = url_html["data"]["announcementVO"]["detail"]["openBidTime"]
        bidAcquisitionPlace = url_html["data"]["announcementVO"]["detail"]["bidAcquisitionPlace"]
        bidOpenPlace = url_html["data"]["announcementVO"]["detail"]["bidOpenPlace"]
        days = url_html["data"]["announcementVO"]["detail"]["days"]
        bidScope = url_html["data"]["announcementVO"]["detail"]["bidScope"]
        bidQualification = url_html["data"]["announcementVO"]["detail"]["bidQualification"]
        durationDescription = url_html["data"]["announcementVO"]["detail"]["durationDescription"]
        supervisorPhone = url_html["data"]["announcementVO"]["detail"]["supervisorPhone"]
        applyStartTime = url_html["data"]["announcementVO"]["detail"]["applyStartTime"]
        applyEndTime = url_html["data"]["announcementVO"]["detail"]["applyEndTime"]

        index_url=f'https://zcpt.szcg.cn/detail/{projectId}'
        detail = f'''
    <div data-v-9f03e88e="" data-v-c3ed891c="" class="container"><div data-v-9f03e88e="" class="table-title">项目基本信息</div> <table data-v-9f03e88e="" class="pure-table pure-table-bordered"><tr data-v-9f03e88e=""><td data-v-9f03e88e="">项目名称</td> <td data-v-9f03e88e="">{projectName}</td> <td data-v-9f03e88e="">项目编号</td> <td data-v-9f03e88e=""><span data-v-9f03e88e="">{projectNo}</span></td></tr> <tr data-v-9f03e88e=""><td data-v-9f03e88e="">项目类型</td> <td data-v-9f03e88e="">{tenderProjectTypeDesc}</td> <td data-v-9f03e88e="">采购方式</td> <td data-v-9f03e88e="">{tenderModeDesc}</td></tr> <tr data-v-9f03e88e=""><td data-v-9f03e88e="">采购流程</td> <td data-v-9f03e88e="">{purchaseProcessDesc}</td> <td data-v-9f03e88e="">组织形式</td> <td data-v-9f03e88e="">{tenderOrganizeFormDesc}</td></tr> <tr data-v-9f03e88e=""><td data-v-9f03e88e="">项目地址</td> <td data-v-9f03e88e="">{address}</td> <td data-v-9f03e88e="">项目所在区域</td> <td data-v-9f03e88e=""></td></tr> <tr data-v-9f03e88e=""><td data-v-9f03e88e="">项目行业分类</td> <td data-v-9f03e88e=""><span data-v-9f03e88e="">{industriesLatterTypeDesc}</span> <span data-v-9f03e88e="">/{industriesNumberTypeDesc}</span></td> <td data-v-9f03e88e="">资格审查方式</td> <td data-v-9f03e88e="">{qualificationMethodDesc}</td></tr> <tr data-v-9f03e88e=""><td data-v-9f03e88e="">资金来源</td> <td data-v-9f03e88e="">{fundSourceDesc}</td> <td data-v-9f03e88e="">深圳市属国企项目</td> <td data-v-9f03e88e="">是</td></tr> <tr data-v-9f03e88e=""><td data-v-9f03e88e="">战略应急物资</td> <td data-v-9f03e88e="" colspan="3">
          否
        </td></tr> <tr data-v-9f03e88e=""><td data-v-9f03e88e="">项目概况</td> <td data-v-9f03e88e="" colspan="3">
          {tendererContent}
        </td></tr></table> <!----> <!----> <div data-v-9f03e88e="" class="table-title">标段/包信息</div> <table data-v-9f03e88e="" class="pure-table pure-table-bordered"><tr data-v-9f03e88e=""><td data-v-9f03e88e="">标段/包名称</td> <td data-v-9f03e88e="">{projectName}</td> <td data-v-9f03e88e="">标段/包分类</td> <td data-v-9f03e88e=""><span data-v-9f03e88e="">{packageLatterTypeDesc}</span></td></tr> <tr data-v-9f03e88e=""><td data-v-9f03e88e="">报价方式</td> <td data-v-9f03e88e="">
            {quotationMethodDesc}
          </td> <td data-v-9f03e88e="">是否评定分离</td> <td data-v-9f03e88e=""><span data-v-9f03e88e="">否</span></td></tr> <!----> <!----> <tr data-v-9f03e88e=""><td data-v-9f03e88e="">评审办法</td> <td data-v-9f03e88e="" colspan="3"><span data-v-9f03e88e="">{gradeMethodDesc}</span></td></tr> <tr data-v-9f03e88e=""><td data-v-9f03e88e="">是否缴纳保证金</td> <td data-v-9f03e88e="">否</td> <td data-v-9f03e88e="">联合体投标</td> <td data-v-9f03e88e=""><span data-v-9f03e88e="">不允许</span></td></tr> <!----></table> <div data-v-9f03e88e="" class="table-title">公告信息</div> <table data-v-9f03e88e="" class="pure-table pure-table-bordered"><tr data-v-9f03e88e=""><td data-v-9f03e88e="">招标公告名称</td> <td data-v-9f03e88e="">{name}</td> <td data-v-9f03e88e="">发布地点</td> <td data-v-9f03e88e=""><span data-v-9f03e88e="">集团官网、阳光采购平台</span></td></tr> <tr data-v-9f03e88e=""><td data-v-9f03e88e="">招标公告发布时间</td> <td data-v-9f03e88e="" colspan="3">
        {startTime}
      </td></tr> <!----> <tr data-v-9f03e88e=""><td data-v-9f03e88e="">招标公告信息</td> <td data-v-9f03e88e="" colspan="3">
        {message}
      </td></tr> <tr data-v-9f03e88e=""><td data-v-9f03e88e="">招标公告附件</td> <td data-v-9f03e88e="" colspan="3"></td></tr></table> <div data-v-9f03e88e="" class="table-title">招标信息</div> <table data-v-9f03e88e="" class="pure-table pure-table-bordered"><colgroup data-v-9f03e88e=""><col data-v-9f03e88e="" style="background-color: rgb(248, 248, 248);"> <col data-v-9f03e88e=""> <col data-v-9f03e88e="" style="background-color: rgb(248, 248, 248);"> <col data-v-9f03e88e=""></colgroup> <!----> <tr data-v-9f03e88e=""><td data-v-9f03e88e="">报名开始时间：</td> <td data-v-9f03e88e="">{tenderDocGetTime}</td> <td data-v-9f03e88e="">报名截止时间：</td> <td data-v-9f03e88e="">{applyEndTime}</td></tr> <tr data-v-9f03e88e=""><td data-v-9f03e88e="">文件获取开始时间</td> <td data-v-9f03e88e="">{applyStartTime}</td> <td data-v-9f03e88e="">文件获取截止时间</td> <td data-v-9f03e88e="">{tenderDocDeadLine}</td></tr> <tr data-v-9f03e88e=""><td data-v-9f03e88e="">递交投标文件截止时间</td> <td data-v-9f03e88e="">{tenderQuestionDeadline}</td> <td data-v-9f03e88e="">质疑截止时间</td> <td data-v-9f03e88e="">{bidDocReferEndTime}</td></tr> <tr data-v-9f03e88e=""><td data-v-9f03e88e="">答疑截止时间</td> <td data-v-9f03e88e="">{tenderAnswerDeadline}</td> <td data-v-9f03e88e="">开标时间</td> <td data-v-9f03e88e="">{openBidTime}</td></tr> <tr data-v-9f03e88e=""><td data-v-9f03e88e="">标书获取地点</td> <td data-v-9f03e88e="" colspan="3">
        {bidAcquisitionPlace}
      </td></tr> <tr data-v-9f03e88e=""><td data-v-9f03e88e="">开标地点</td> <td data-v-9f03e88e="" colspan="3">
        {bidOpenPlace}
      </td></tr> <tr data-v-9f03e88e=""><td data-v-9f03e88e="">服务期/交货期/工期</td> <td data-v-9f03e88e="" colspan="3">{days}天</td></tr> <tr data-v-9f03e88e=""><td data-v-9f03e88e="">服务期/交货期/工期说明</td> <td data-v-9f03e88e="" colspan="3">
        {durationDescription}
      </td></tr> <tr data-v-9f03e88e=""><td data-v-9f03e88e="">招标/采购范围</td> <td data-v-9f03e88e="" colspan="3">
        {bidScope}
      </td></tr> <tr data-v-9f03e88e=""><td data-v-9f03e88e="">资格条件</td> <td data-v-9f03e88e="" colspan="3">
        {bidQualification}
      </td></tr> <tr data-v-9f03e88e=""><td data-v-9f03e88e="">监督人</td> <td data-v-9f03e88e="">{superviseDeptName}</td> <td data-v-9f03e88e="">监督人电话</td> <td data-v-9f03e88e="">{supervisorPhone}</td></tr></table> <div data-v-9f03e88e="" class="table-title">采购单位信息</div> <table data-v-9f03e88e="" class="pure-table pure-table-bordered"><tr data-v-9f03e88e=""><td data-v-9f03e88e="">单位名称</td> <td data-v-9f03e88e="">{legalPerson}</td> <td data-v-9f03e88e="">单位地址</td> <td data-v-9f03e88e=""><span data-v-9f03e88e="">{companyAddress}</span></td></tr> <tr data-v-9f03e88e=""><td data-v-9f03e88e="">单位联系人</td> <td data-v-9f03e88e="">{connector}</td> <td data-v-9f03e88e="">采购人联系电话</td> <td data-v-9f03e88e="">{foreignContactPhone}</td></tr></table></div>
    '''

        # detail_html = etree.tostring(detail, method='HTML')
        # detail_html = html.unescape(detail_html.decode()).replace("display: none", '')
        # detail_text = url_html.xpath('string(//div[@class="detail-box"])').replace('\xa0', '').replace('\n', '').\
        #     replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
        if len(t) < 200:
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
        item['resource'] = '特区建工集团采购平台'
        item['shi'] = 6507
        item['sheng'] = 6500
        item['removal'] = title
        # print(item)
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



