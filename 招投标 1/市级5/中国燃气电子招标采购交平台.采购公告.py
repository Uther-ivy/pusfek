# -*- coding: utf-8 -*-
import base64
import json
import re
import time, html

import parsel
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 中国燃气电子招标采购交平台
class wenshan_ggzy:
    def __init__(self):
        self.url_list = [
            'https://zrzbcg.chinagasholdings.com/gg/cgggList', #采购公告
                                                              ]
        self.url = self.url_list.pop(0)
        self.headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'}
    def parse(self):
        date = tool.date
        # date = '2020-09-21'
        page = 0
        while True:
            data={
                'currentPage':page,
                'ggName':''
            }

            page += 1

            text = tool.requests_post(url=self.url, data=data ,headers=self.headers).replace('</tr>','</tr><tr>')
            print('*' * 20, page, '*' * 20)
            # print(text)
            #  解析数据
            html = parsel.Selector(text)
            # print(11, text)
            # time.sleep(6666)
            # 提取数据

            detail = html.css('.table_1>table>tbody>tr')[:15]

            #  遍历
            for li in detail:
                title = li.css('a ::attr(title)').get()
                print(title)
                date_Today = li.css('td:last-child ::text').get().strip()
                # id
                id = li.css('a ::attr(href)').get()
                # print(id)
                # 参数
                info_id = id.replace('/gg/ggDetail','').replace('&xinXiLaiYuan=3','')
                # print(info_id)
                # 详情页pson接口
                info_url = 'https://zrzbcg.chinagasholdings.com/zr-xunjia/common/nofilter/queryXiangMuByGuid.do'+info_id
                # print(info_url)
                # 展示页url
                url = 'https://zrzbcg.chinagasholdings.com'+id
                print(title, url, date_Today)
                #  三天内判断和去重

                if tool.Transformation(date) <= tool.Transformation(date_Today):
                    if tool.removal(title, date):
                        self.parse_detile(title, url, date_Today,id,info_url)
                    else:
                        print('【existence】', url)
                        continue
                else:
                    print('日期不符, 正在切换类型', date_Today)
                    self.url = self.url_list.pop(0)
                    page=0
                    break
            if page == 20:
                print('日期不符, 正在切换类型')
                self.url = self.url_list.pop(0)
                page=0




    def parse_detile(self, title, url, date,id,info_url):

        data={'guid':id}
        t = tool.requests_post_to(url=info_url,data=data, headers=self.headers)
        # print(t)
        # time.sleep(2222)
        url_html = json.loads(t)
        print(url_html)
        # print(base64.b64decode(url_html).decode())
        # 网页拼接

        if url_html['xiangMuName'] in url_html.keys():
            # base64.b64decode().decode()
            detail = f"""<div style="margin-top:-13px;">
    <table width="100%" border="0" class="de_tab1">
        <tbody>
        <tr>
            <td class="bg_td" style="width:14%;"><span class="cg_span">询价</span>项目名称：</td>
            <td colspan="3" class="text_left" data-bind="text:xiangMuName">{url_html['xiangMuName']}</td>
        </tr>
        <tr>
            <td rowspan="3" class="bg_td" style="width:14%;">询价项目编号信息：</td>
            <td class="bg_td" style="width:14%;">
                <span class="red"></span>项目所属范围：
            </td>
            <td colspan="3">
                <input type="radio" id="jiTuanNei" name="suoShuType" value="0" disabled="">{url_html['suoShuTypeText']}
                <input type="radio" id="jiTuanWai" name="suoShuType" value="1" checked="checked" disabled="">中燃集团外项目

            </td>
        </tr>
        
        <tr>
            <td class="bg_td"><span class="cg_span">询价</span>人名称：</td>
            <td colspan="3" class="text_left" id="caiGouRenName">{base64.b64decode(url_html['caiGouRenName']).decode()}</td>
        </tr>
        <tr>
            <td class="bg_td"><span class="cg_span">询价</span>人地址：</td>
            <td colspan="3" class="text_left" id="caiGouRenAddress">{base64.b64decode(url_html['caiGouRenAddress']).decode()}</td>
        </tr>
        <tr>
            <td class="bg_td">联系人：</td>
            <td style="width:36%;" class="text_left" id="caiGouRenLinkMan1">
                {url_html['lsXiangMuCaiLiaoSheBei'][0]['creatorName']}
            </td>
            <td class="bg_td" style="width:14%;">手机号：</td>
            <td style="width:36%;" class="text_left">
                <span data-bind="text:mobileGJQH">{url_html['mobileGJQH']}</span>
                <span id="caiGouRenLinkPhone1">''</span>
            </td>
        </tr>
        <tr>
            <td class="bg_td">采购方式：</td>
            <td colspan="3" class="text_left" data-bind="text:caiGouTypeText">{url_html['caiGouTypeText']}</td>
        </tr>

        <tr>
            <td class="bg_td">公告开始时间：</td>
            <td class="text_left" data-bind="text:gongGaoStartTimeText">{url_html['gongGaoStartTimeText']}</td>
            <td class="bg_td">公告截止时间：</td>
            <td class="text_left" data-bind="text:xunJiaEndTimeText">{url_html['xunJiaEndTimeText']}</td>
        </tr>

        <tr>
            <td class="bg_td">相关要求：</td>
            <td colspan="3" class="text_left" data-bind="text:xiangGuanYaoQiu"></td>
        </tr>
        </tbody>
    </table>
</div>"""
        else:    #另一个拼接
            detail = f"""<div style="margin-top:-13px;">
				<table width="100%" border="0" class="de_tab1">
					<tbody><tr>
						<td class="bg_td" style="width:14%;"><span class="cg_span">采购</span>项目名称：</td>
						<td colspan="3" class="text_left" data-bind="text:xiangMuName">{url_html['xiangMuName']}</td>
					</tr>
					<tr>
						<td class="bg_td"><span class="cg_span">采购</span>项目编号：</td>
						<td colspan="3" class="text_left" data-bind="text:xiangMuBianHao">{url_html['xiangMuBianHao']}</td>
					</tr>
					<tr>
						<td class="bg_td"><span class="cg_span">采购</span>人名称：</td>
						<td colspan="3" class="text_left" id="caiGouRenName">{base64.b64decode(url_html['caiGouRenName']).decode()}</td>
					</tr>
					<tr>
						<td class="bg_td"><span class="cg_span">采购</span>人地址：</td>
						<td colspan="3" class="text_left" id="caiGouRenAddress">{base64.b64decode(url_html['caiGouRenAddress']).decode()}</td>
					</tr>
					<tr>
						<td class="bg_td">联系人：</td>
						<td style="width:36%;" class="text_left" id="caiGouRenLinkMan1">{base64.b64decode(url_html['caiGouRenLinkMan']).decode()}</td>
						<td class="bg_td" style="width:14%;">手机号：</td>
						<td style="width:36%;" class="text_left"> <span data-bind="text:mobileGJQH"></span>
							<span id="caiGouRenLinkPhone1">{base64.b64decode(url_html['caiGouRenLinkPhone']).decode()}</span>
						</td>
					</tr>
					<tr>
						<td class="bg_td">公告开始时间：</td>
						<td class="text_left" data-bind="text:gongGaoStartTimeText">{url_html['gongGaoStartTime']}</td>
						<td class="bg_td">公告截止时间：</td>
						<td data-bind="text:zuiZhongGongGaoEndTimeText" class="text_left">{url_html['gongGaoEndTime']}</td>
					</tr>
					<tr>
						<td class="bg_td">提出异议截止时间：</td>
						<td class="text_left" data-bind="text:zuiZhongZhiYiEndTimeText">{url_html['zuiZhongZhiYiEndTimeText']}</td>
						<td class="bg_td">澄清回复截止时间：</td>
						<td class="text_left" data-bind="text:zuiZhongDaYiEndTimeText">{url_html['zuiZhongDaYiEndTimeText']}</td>
					</tr>
					<tr>
						<td class="bg_td">竞价开始时间：</td>
						<td class="text_left" colspan="3" data-bind="text:zuiZhongJingJiaStartTimeText">{url_html['zuiZhongJingJiaStartTimeText']}</td>
					</tr>
				</tbody>
				    
				</table>
			</div>"""

        # time.sleep(2222)


        # print(detail)

        # detail_html = etree.tostring(detail, method='HTML')
        # detail_html = html.unescape(detail_html.decode()).replace("display: none", '')
        # detail_text = url_html.xpath("string(//div[@class='content'])").replace('\xa0', '').replace('\n', '').\
        #     replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')
        if len(t) < 200:
            int('a')
        item = {}
        item['title'] = title.replace('\u2022', '')
        item['url'] = url
        item['date'] = date
        item['typeid'] = tool.get_typeid(item['title'])
        item['senddate'] = int(time.time())
        item['mid'] = 867
        item['infotype'] = tool.get_infotype(item['title'])
        item['body'] = tool.qudiao_width(detail)
        # item['body'] = item['body']
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
        item['tel'] = base64.b64decode(url_html['caiGouRenLinkPhone']).decode()
        item['email'] = ''
        item['address'] = base64.b64decode(url_html['caiGouRenAddress']).decode()
        print(item['address'])
        item['linkman'] = base64.b64decode(url_html['caiGouRenLinkMan']).decode()
        item['function'] = tool.get_function(detail)
        item['resource'] = '中国燃气电子招标采购交平台'
        item['nativeplace'] =tool.get_city(item['address'])
        item['shi'] = tool.get_city(item['address'])
        if len(str(int(float(item["shi"])))) == 4:
            item['sheng'] = int(str(item["shi"])[:2] + '00')
        elif len(str(int(item["shi"]))) == 5:
            item['sheng'] = int(str(item["shi"])[:3] + '00')
        else:
            item['sheng'] = 0
        item['removal'] = title
        item['winner'] = ' '
        print(item)
        # process_item(item)
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
    # str='6YKv6YO45YaA5Y2X5paw5Yy66ams5aS057uP5rWO5byA5Y+R5Yy65Lit5oSP5aSn6KGX5Lic5L6n44CB6KeE5YiS5qiq5LqU6Lev5YyX5L6nMTAj'
    # str='5rKz5YyX5Y2O6YCa54eD5rCU6K6+5aSH5pyJ6ZmQ5YWs5Y+4'
    # print(base64.b64decode(str).decode())
