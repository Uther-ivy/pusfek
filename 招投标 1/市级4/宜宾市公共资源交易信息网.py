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

# 宜宾市公共资源交易信息网
class wenshan_ggzy:
    def __init__(self):
        self.url_list = [
            'https://ggzy.yibin.gov.cn/ggfwptwebapi/Web/service', #工程招标
           ]
        self.url = self.url_list.pop(0)
        self.headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'}
    def parse(self):
        date = tool.date
        # date = '2020-09-21'
        page = 0
        while True:
            page += 1
            data = {"action": "pageTongYong_SouSuo", "pageIndex": page, "pageSize": 10, "xiangMu_LeiXing": "",
                    "xinXi_LeiXing": "102", "title": ""}
            text = tool.requests_post_to(url=self.url, headers=self.headers,data=data)
            print('*' * 20, page, '*' * 20)
            html = json.loads(text)
            # print(11, text)
            # time.sleep(6666)
            detail = html["data"]
            for li in detail:
                title = li["zhaoBiao_XiangMu_Name"]
                date_Today = li["publish_StartTime"].split(' ')[0]
                guid = li["guid"]
                url = 'https://ggzy.yibin.gov.cn/ggfwptwebapi/Web/service'
                # print(title, url, date_Today)
                # time.sleep(666)
                # self.parse_detile(title, url, date_Today,guid)
                if tool.Transformation(date) <= tool.Transformation(date_Today):
                    if tool.removal(title, date):
                        self.parse_detile(title, url, date_Today,guid)
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

    def parse_detile(self, title, url, date,guid):
        print(url)
        data2 = {"action": "getGCJS_ZhaoBiao_GongGao", "guid": guid}
        t = tool.requests_post_to(url=url,headers=self.headers,data=data2)
        # print(t)
        # time.sleep(2222)
        url_html = json.loads(t)
        ZhaoBiao_TiaoJian = url_html["data"]["zhaoBiao_GongGao"]["ZhaoBiao_TiaoJian"]
        ZhaoBiao_FanWei = url_html["data"]["zhaoBiao_GongGao"]["ZhaoBiao_FanWei"]
        ZiGe_YaoQiu = url_html["data"]["zhaoBiao_GongGao"]["ZiGe_YaoQiu"]
        GongGao_MeiJie = url_html["data"]["zhaoBiao_GongGao"]["GongGao_MeiJie"]
        DiJiao_FangShi = url_html["data"]["zhaoBiao_GongGao"]["DiJiao_FangShi"]
        TouBiao_EndTime = url_html["data"]["zhaoBiao_GongGao"]["TouBiao_EndTime"]
        Publish_StartTime = url_html["data"]["zhaoBiao_GongGao"]["Publish_StartTime"]
        Publish_EndTime = url_html["data"]["zhaoBiao_GongGao"]["Publish_EndTime"]
        index_url = f"https://ggzy.yibin.gov.cn/#/transactionListDetail?guid={guid}&leiXing=102"
        detail =f'''
    <div data-v-1be13ad8="" data-v-282a978c="" class="w-full h-full text-[#1F2329] tenderAnnouncementBox" toubiaoren_list="" detaildata="[object Object]" relationlink="[object Object]"><p data-v-1be13ad8="" class="title">1.招标条件：</p> <p data-v-1be13ad8="" class="content">{ZhaoBiao_TiaoJian}</p> <p data-v-1be13ad8="" class="title">2.项目概况与招标范围：</p> <p data-v-1be13ad8="" class="content">{ZhaoBiao_FanWei}</p> <p data-v-1be13ad8="" class="title">3.投标人资格要求：</p> <p data-v-1be13ad8="" class="content">{ZiGe_YaoQiu}</p> <p data-v-1be13ad8="" class="title">4.招标文件的获取：</p> <p data-v-1be13ad8="" class="content">
    4.1 凡有意参加投标者，请于 {Publish_StartTime} 至
    {Publish_EndTime}
    （电子招标文件的获取，不受获取截止时间限制，任何时间段均可获取），登录宜宾市公共资源交易信息网（https://ggzy.yibin.gov.cn/），凭数字证书和密码获取招标文件及其它招标资料。另，可通过本项目招标公告附件，免费获取招标文件。
  </p> <p data-v-1be13ad8="" class="content">4.2 招标人不提供邮购招标文件服务。</p> <p data-v-1be13ad8="" class="title">5.交易平台技术服务费：</p> <p data-v-1be13ad8="" class="content">
    5.1 本项目（或本标段）交易平台技术服务费 170
    元。投标人须先缴纳技术服务费，再缴纳投标保证金，且须在投标保证金缴纳截止时间前，通过宜宾市建设工程网上招投标系统缴纳技术服务费（流程为：登录宜宾市建设工程网上招投标系统——进入“网上投标-缴纳技术服务费”页面——选择项目标段——点击缴费后使用支付宝扫码完成支付——支付成功后，重新点击“网上投标-缴纳技术服务费”，选择打印相应项目的《技术服务费缴纳回执》。成功缴纳技术服务费以系统出具的缴纳回执为准）。
  </p> <p data-v-1be13ad8="" class="content">
    5.2
    投标人缴纳的电子化交易平台技术服务费由相应电子交易平台建设运营商收取。投标人可在成功支付技术服务费后，在“网上投标-技术服务费自助开票”页面选择对应项目标段填写完善普通税务发票开票信息，并在线获取相应电子发票。
  </p> <p data-v-1be13ad8="" class="title">6.投标文件的递交：</p> <p data-v-1be13ad8="" class="content">
    6.1 投标文件递交的截止时间（投标截止时间，下同）为
    {TouBiao_EndTime}。
  </p> <p data-v-1be13ad8="" class="content">
    6.2 电子投标文件递交方式： {DiJiao_FangShi}。
  </p> <p data-v-1be13ad8="" class="content">
    6.3
    逾期递交的或者未按指定方式递交或未送达指定地点的投标文件，招标人不予受理。
  </p> <p data-v-1be13ad8="" class="title">7.发布公告的媒介：</p> <p data-v-1be13ad8="" class="content"> {GongGao_MeiJie}</p> <div data-v-1be13ad8="" class="bg-[#F2F3F5] h-[50px] leading-[50px] w-full text-[18px] text-[#1F2329] px-[12px] font-semibold mt-[24px] shadow-box">
    招标文件附件：
  </div> <div data-v-1be13ad8="" class="el-table w-full el-table--fit el-table--border el-table--enable-row-hover el-table--enable-row-transition"><div class="hidden-columns"><div data-v-1be13ad8=""></div> <div data-v-1be13ad8=""></div> <div data-v-1be13ad8=""></div> <div data-v-1be13ad8=""></div></div><div class="el-table__header-wrapper"><table cellspacing="0" cellpadding="0" border="0" class="el-table__header" style="width: 1319px;"><colgroup><col name="el-table_2_column_6" width="80"><col name="el-table_2_column_7" width="413"><col name="el-table_2_column_8" width="413"><col name="el-table_2_column_9" width="413"></colgroup><thead class=""><tr class=""><th colspan="1" rowspan="1" class="el-table_2_column_6     is-leaf bg-[#F2F3F5] h-[50px] font-semibold text-[#1F2329] text-[18px] el-table__cell"><div class="cell">序号</div></th><th colspan="1" rowspan="1" class="el-table_2_column_7     is-leaf bg-[#F2F3F5] h-[50px] font-semibold text-[#1F2329] text-[18px] el-table__cell"><div class="cell">标段名称</div></th><th colspan="1" rowspan="1" class="el-table_2_column_8     is-leaf bg-[#F2F3F5] h-[50px] font-semibold text-[#1F2329] text-[18px] el-table__cell"><div class="cell">标段编号</div></th><th colspan="1" rowspan="1" class="el-table_2_column_9     is-leaf bg-[#F2F3F5] h-[50px] font-semibold text-[#1F2329] text-[18px] el-table__cell"><div class="cell">文件名称</div></th></tr></thead></table></div><div class="el-table__body-wrapper is-scrolling-none"><table cellspacing="0" cellpadding="0" border="0" class="el-table__body" style="width: 1319px;"><colgroup><col name="el-table_2_column_6" width="80"><col name="el-table_2_column_7" width="413"><col name="el-table_2_column_8" width="413"><col name="el-table_2_column_9" width="413"></colgroup><tbody><tr class="el-table__row min-h-[48px] font-normal text-[#1F2329] text-[16px]"><td rowspan="1" colspan="1" class="el-table_2_column_6   el-table__cell"><div class="cell"><div>1</div></div></td><td rowspan="1" colspan="1" class="el-table_2_column_7   el-table__cell"><div class="cell">方案设计、初步设计</div></td><td rowspan="1" colspan="1" class="el-table_2_column_8   el-table__cell"><div class="cell">CPQFJ2023030024001</div></td><td rowspan="1" colspan="1" class="el-table_2_column_9   el-table__cell"><div class="cell"><span data-v-1be13ad8="" class="cursor-pointer hover:text-[#317BEA]">（招标）（招标）（招标）文脉二期四标段_招标文件_CPQFJ2023030024.ZBJ</span></div></td></tr><!----></tbody></table><!----><!----></div><!----><!----><!----><!----><div class="el-table__column-resize-proxy" style="display: none;"></div></div></div>
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
        item['resource'] = '宜宾市公共资源交易信息网'
        item['shi'] = 6507
        item['sheng'] = 6500
        item['removal']= title
        # print(item["body"])
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



