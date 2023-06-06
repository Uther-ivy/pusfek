# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
import tool
from save_database import process_item

# 深圳市住房和建设局
class shenzhen_jzj:
    def __init__(self):
        self.url_code = [
            # 招标公告
            'https://www.szjsjy.com.cn:8001/jyw/queryGongGaoList.do?rows=10&page={}',
            # 定标结果
            'https://www.szjsjy.com.cn:8001/jyw/queryDBJieGuoList.do?rows=10&page={}',
            # 中标公告
            'https://www.szjsjy.com.cn:8001/jyw/queryZBJieGuoList.do?rows=10&page={}',
        ]
        self.url = self.url_code.pop(0)
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
        }

    def parse(self):
        date = tool.date
        # date = '2020-01-02'
        page = 0
        while True:
            page += 1
            print('*' * 20, page, '*' * 20)
            text = tool.requests_get(self.url.format(page), self.headers).replace('var gongGaoList=', '').replace('var dbList=', '').replace('var zbList=', '')[:-1]
            # print(111, text)
            # time.sleep(666)
            detail = json.loads(text)['rows']
            for i in detail:
                if 'GongGao' in self.url:
                    title = i['gcName']
                    url = 'https://www.szjsjy.com.cn:8001/jyw/showGongGao.do?ggGuid={}&gcbh=&bdbhs='.format(i['ggGuid'])
                    date_Today = i['ggStartTime2'].replace('"', '')[:10]
                elif 'DBJieGuo' in self.url:
                    url = 'https://www.szjsjy.com.cn:8001/jyw/queryDbJieGuoByGuid.do?guid={}'.format(i['dbJieGuoGuid'])
                    title = i['bdName']
                    date_Today = i['createTime2'].replace('"', '')[:10]
                elif 'ZBJieGuo' in self.url:
                    url = 'https://www.szjsjy.com.cn:8001/jyw/queryZbgs.do?guid={}&ggGuid=&bdGuid='.format(i['dbZhongBiaoJieGuoGuid'])
                    title = i['bdName']
                    date_Today = i['fabuTime2'].replace('"', '')[:10]
                # print(title, url, date_Today)
                # time.sleep(666)
                if tool.Transformation(date) <= tool.Transformation(date_Today):
                    if tool.removal(title, date):
                        self.parse_detile(title, url, date_Today)
                    else:
                        print('【existence】', url)
                        continue
                else:
                    print('日期不符, 正在切换类型...', date_Today)
                    self.url = self.url_code.pop(0)
                    page = 0
                    break

    def parse_detile(self, title, url, date):
        print(url)
        if 'showGongGao' in url:
            url_text = json.loads(tool.requests_get(url, self.headers))['html']
            url_html = etree.HTML(url_text)
            detail_text = url_html.xpath('string(.)').replace('\xa0', '').replace('\n', '').replace('\r', '').replace('\t',
                                                                                                                      '').replace(
                ' ', '').replace('\xa5', '')
        elif 'queryDbJieGuoByGuid' in url:
            html_table = ''' <table width="100%" border="0" class="de_tab1">
                    <tr >
                      <td class="bg_td">公告名称：</td>
                      <td  id="ggName">{}</td>
                      </tr>
                    <tr>
                      <td class="bg_td">标段编号：</td>
                      <td id="bdBH">{}</td>
                    </tr>
                    <tr>
                      <td class="bg_td">标段名称：</td>
                      <td id="bdName">{}</td>
                    </tr>
                    <tr>
                      <td class="bg_td">建设单位：</td>
                      <td id="zbRName">{}</td>
                    </tr>
                    <tr>
                      <td class="bg_td">定标时间：</td>
                      <td id="dbTime">{}</td>
                    </tr>
                    <tr>
                        <td class="bg_td">中标候选人：</td>
                        <td id="zbName">{}</td>
                    </tr>
                    <tr>
                      <td class="bg_td">入围方式：</td>
                      <td id="rwfs">{}</td>
                    </tr>
                    <tr>
                      <td class="bg_td">定标方法：</td>
                      <td id="dbBanFa">{}</td>
                    </tr>
                    <tr>
                      <td class="bg_td">联系人：</td>
                      <td id="lianXiRenName">{}</td>
                    </tr>
                    <tr>
                      <td class="bg_td">联系电话：</td>
                      <td id="lianXiRenPhone">{}</td>
                   </tr>
             </table>'''
            url_json = json.loads(tool.requests_get(url, self.headers))
            if 'rwFangShi' in url_json:
                rwFangShi = url_json['rwFangShi']
            else:
                rwFangShi = '无'
            try:
                dbBanFa = url_json['dbBanFa']
            except:
                dbBanFa = '无'
            try:
                url_text = html_table.format(title, url_json['bd']['bdBH'], url_json['bd']['bdName'],
                                  url_json['bd']['gc']['zbRName'], url_json['createTime2'], url_json['zbName'],
                                  rwFangShi, dbBanFa, url_json['lianxiren'], url_json['lianxirenphone'],)
            except:
                return
            url_html = etree.HTML(url_text)
            detail_text = url_html.xpath('string(.)').replace('\xa0', '').replace('\n', '').replace('\r', '').replace(
                '\t',
                '').replace(
                ' ', '').replace('\xa5', '')
            # print(url_text, url)
            # time.sleep(6666)
        elif 'queryZbgs' in url:
            html_table = '''<div class="detail_contect">
                        <div id="zbgk">
                            <h3 class="index_title1 with150">
                                <strong>中标公示</strong>
                            </h3>
                            <table width="100%" border="0" class="de_tab1">
                                <tr>
                                    <td class="bg_td">招标项目编号：</td>
                                    <td colspan="3"><span id="gcBH">{}</span></td>
                                </tr>
                                <tr>
                                    <td class="bg_td">招标项目名称：</td>
                                    <td colspan="3"><span id="gcName">{}</span></td>
                                </tr>
                                <tr>
                                    <td class="bg_td">标段名称：</td>
                                    <td colspan="3"><span id="bdName">{}</span></td>
                                </tr>
                                <tr>
                                    <td class="bg_td">项目编号：</td>
                                    <td colspan="3"><span id="xmBH">{}</span></td>
                                </tr>
                                <tr>
                                    <td class="bg_td">项目名称：</td>
                                    <td colspan="3"><span id="xmName">{}</span></td>
                                </tr>
                                <tr>
                                    <td class="bg_td">公示时间：</td>
                                    <td colspan="3"><span id="zbgsStartTime">{}</span> 至 <span id="zbgsEndTime">{}</span></td>
                                </tr>
                                <tr>
                                    <td class="bg_td">招标人：</td>
                                    <td colspan="3"><span id="zbRName">{}</span></td>
                                </tr>
                                <tr>
                                    <td class="bg_td">招标代理机构：</td>
                                    <td colspan="3"><span id="zbdlJG">{}</span></td>
                                </tr>
                                <tr>
                                    <td class="bg_td">招标方式：</td>
                                    <td colspan="3"><span id="zbFangShi">{}</span></td>
                                </tr>
                            </table>
                        </div>
                        <div id="zbdl">
                            <h3 class="index_title1 with150">
                                <strong class="s1">中标人信息</strong>
                            </h3>
                            <table width="100%" border="0" class="de_tab2">
                                <tr>
                                    <td class="bg_td">中标人：</td>
                                    <td colspan="3"><b><span id="tbrName">{}</span></b></td>
                                </tr>
                                <tr class="yx">
                                    <td class="bg_td">中标价：</td>
                                    <td colspan="3"><b><span id="zhongBiaoJE">{}</span></b></td>
                                </tr>
                                <tr class="sg_jl yx">
                                    <td class="bg_td">中标工期：</td>
                                    <td colspan="3"><span id="zhongBiaoGQ">{}</span></td>
                                </tr>
                                <tr class="sg_jl yx">
                                    <td class="bg_td">项目经理：</td>
                                    <td colspan="3"><span id="xiangMuJiLi">{}</span></td>
                                </tr>
                                <tr class="sg_jl yx">
                                    <td class="bg_td">资格等级：</td>
                                    <td colspan="3"><span id="ziGeDengJi">{}</span></td>
                                </tr>
                                <tr class="sg_jl yx">
                                    <td class="bg_td">资格证书：</td>
                                    <td colspan="3"><span id="ziGeZhengShu">{}</span></td>
                                </tr>
                                <tr class="yx">
                                    <td class="bg_td">是否暂定金额：</td>
                                    <td colspan="3"><span id="isZanDingJinE">{}</span></td>
                                </tr>
                            </table>
                        </div>
                        <div id="wxts">
                            <h3 class="red">特别提示：</h3>
                            <div class="">
                                <dl class="">
                                    <dt>根据市政府及市纪检、监察部门的部署，为严厉打击建筑市场围标串标违法犯罪行为，欢迎社会各界以及参与本工程招标投标活动的单位和个人，积极署名举报围标串标违法犯罪行为并提供线索和证据。对提供有效线索和证据的，公安机关及有关部门将立即介入调查。</dt>
                                </dl>
                            </div>
                        </div>
                    </div>'''
            url_json = json.loads(tool.requests_get(url, self.headers))
            if url_json['bd']['gc']['zbFangShi'] == 1:
                zbFangShi = '公开招标'
            else:
                print('招标方式', url)
                zbFangShi = ''
                # time.sleep(6666)
            if url_json['isZanDingJinE'] is None:
                isZanDingJinE = '否'
            else:
                print('是否暂定金额', url, url_json['isZanDingJinE'])
                isZanDingJinE = ''
                # time.sleep(6666)
            url_text = html_table.format(url_json['bdBH'], url_json['bdName'], url_json['bdName'], url_json['bd']['xm']['xm_BH'],
                              url_json['bd']['xm']['xm_Name'], url_json['zbgsStartTime2'], url_json['zbgsEndTime2'],
                              url_json['zbrAndLht'], url_json['zbdlJG'], zbFangShi,
                              url_json['tbrName1'], url_json['tongYongZhongBiaoJia'], url_json['zhongBiaoGQ'],
                              url_json['xiangMuJiLi'],url_json['ziGeDengJi'],url_json['ziGeZhengShu'],
                              isZanDingJinE,)
            url_html = etree.HTML(url_text)
            detail_text = url_html.xpath('string(.)').replace('\xa0', '').replace('\n', '').replace('\r', '').replace(
                '\t',
                '').replace(
                ' ', '').replace('\xa5', '')
            # print(url_text, url)
            # time.sleep(6666)
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
        item['body'] = tool.qudiao_width(url_text)
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
        item['resource'] = '深圳市住房和建设局'
        item['shi'] = 10003
        item['sheng'] = 10000
        item['removal']= title
        process_item(item)

    def get_nativeplace(self, addr):
        city = ''
        city_list = [['10003.001', '罗湖区'], ['10003.002', '福田区'], ['10003.003', '南山区'], ['10003.004', '宝安区'], ['10003.005', '龙岗区'], ['10003.006', '盐田区'], ['10003.007', '坪山区']]

        for i in city_list:
            if i[1] in addr:
                city = float(i[0])
                break
        if city == '':
            city = 10003
        return city

if __name__ == '__main__':
    import traceback, os
    try:
        jl = shenzhen_jzj()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
        tool.send_error('报错文件：'+str(os.path.basename(__file__))+'报错信息：'+str(e))


