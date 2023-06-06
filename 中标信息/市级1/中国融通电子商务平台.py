# -*- coding: utf-8 -*-
import json
import re
import time, html
from lxml import etree
import tool
from save_database import process_item
# 中国融通电子商务平台
class alashan_ggzy:
    def __init__(self):
        self.url_code = [
            # f'https://www.ronghw.cn/api/visitor/eb/summary/ann?v={int(time.time()*1000)}',
            f'https://www.ronghw.cn/api/visitor/eb/bid/pubWinResultList?v={int(time.time()*1000)}',
        ]
        self.url = self.url_code.pop(0)
        self.headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
        }
    def parse(self):
        date = tool.date
        # date = '2021-08-10'
        page = 21
        while True:
            page += 1
            data = {'pageNo': page,
                    'pageSize': 10,
                    'title': " ",
                    'projectCode': " ",
                    'procurementType': " "
                    }
            print('*' * 20, page, '*' * 20)
            html = tool.requests_post_to(url=self.url,data=data,headers=self.headers)
            # print(111, text)
            # time.sleep(666)
            detail = json.loads(html)['result']['records']
            for li in detail:
                try:
                    title = li['title']
                    if title is None:
                        title = li['projectName']
                    businessid=li['businessId']
                    projectid=li['projectId']
                    date_Today = li['sendTime'].split(' ')[0]
                    url2=li["htmlAttachUrl"]
                    if tool.Transformation(date) <= tool.Transformation(date_Today):
                        if url2:
                            url = f'https://www.ronghw.cn/file-eb/previewAttach?identify={url2}&descargar=false?v={int(time.time() * 1000)}'
                            showurl = f"https://www.ronghw.cn/eb/notice/{li['noticeMappingId']}?from=nonbid"
                            print(title, showurl, date_Today)
                            self.parse_detile(title, url, date_Today, showurl)
                        else:
                            url=f'https://www.ronghw.cn/api/visitor/websiteAnnouncement/getDetail/pubWinResultInfo?v={int(time.time() * 1000)}'
                            showurl=f'https://www.ronghw.cn/anouncement/nonBid/resultDetail?publicityId={businessid}&projectId={projectid}'
                            data={"publicityId":businessid,"projectId":projectid}
                            print(title,showurl,date_Today)
                            self.parse_detial_json(title, url, date_Today, showurl,data)
                    else:
                        print('日期不符, 正在切换类型...', tool.Time_stamp_to_date(date_Today))
                        return
                except Exception:
                    traceback.print_exc()


    def parse_detile(self, title, url, date,showurl):
        print(url)
        t = tool.requests_get(url, self.headers)
        # print(t)
        if '抱歉，系统发生了错误！' in t:
            print('抱歉，系统发生了错误！')
            return
        url_html = etree.HTML(t)
        detail = url_html.xpath('//html')[0]
        detail_html = etree.tostring(detail,encoding="utf-8")
        detail_html = html.unescape(detail_html.decode()).replace('\xa0', '').replace('\ufeff', '')
        detail_text = ''.join(url_html.xpath('//table[@id="tblInfo"]//td[not(ancestor::html)]//text()')) \
            .replace('\xa0', '').replace('\n', '').replace('\r', '').replace('\t', '') \
            .replace(' ', '').replace('\xa5', '').replace('\ufeff', '')

        # if 'annList' in self.url or 'purchaseAnnList' in self.url:
        #     data = {"announceId":annId,"projectId":globalType,"tabId":"annList","tabName":"招标公告"}
        #     url_text = tool.requests_post_to(
        #         'https://www.ronghw.cn/api/visitor/websiteAnnouncement/getDetail/annInfo?v=1628846093107', data,
        #         self.headers)
        #     url_json = json.loads(json.loads(url_text)['result'])
        #     detail_html = '''<table>
        #                         <tr>
        #                             <td>项目编号</td>
        #                             <td>'''+url_json['projectCode']+'''</td>
        #                             <td>项目名称</td>
        #                             <td>'''+url_json['projectName']+'''</td>
        #                         </tr>
        #                         <tr>
        #                             <td>采购类型</td>
        #                             <td>'''+url_json['procurementType']+'''</td>
        #                             <td>采购企业</td>
        #                             <td>'''+url_json['bidCompanyName']+'''</td>
        #                         </tr>
        #                         <tr>
        #                             <td>报名截止时间</td>
        #                             <td>'''+tool.Time_stamp_to_date_to(url_json['signUpEndTime'])+'''</td>
        #                             <td>开标时间</td>
        #                             <td>'''+tool.Time_stamp_to_date_to(url_json['bidOpenTime'])+'''</td>
        #                         </tr>
        #                         <tr>
        #                             <td>联系人</td>
        #                             <td>'''+url_json['linkMan']+'''</td>
        #                             <td>联系电话</td>
        #                             <td>'''+url_json['tel']+'''</td>
        #                         </tr>
        #                         <tr>
        #                             <td>邮箱</td>
        #                             <td>'''+url_json['email']+'''</td>
        #                         </tr>
        #                         <tr>
        #                             <td>公告文件</td>
        #                             <td><a href="'''+url_json['fileUrl']+'''">'''+url_json['fileName']+'''</a></td>
        #                         </tr>
        #                     </table>'''
        # elif 'changeAnnList' in self.url:
        #     data = {"announceChangeId":annId,"projectId":globalType}
        #     url_text = tool.requests_post_to(
        #         'https://www.ronghw.cn/api/visitor/websiteAnnouncement/getDetail/changeAnnInfo?v=1628846521149', data,
        #         self.headers)
        #     url_json = json.loads(json.loads(url_text)['result'])
        #     detail_html = '''<table>
        #                                 <tr>
        #                                     <td>项目编号</td>
        #                                     <td> ''' + url_json['projectCode'] + '''</td>
        #                                     <td>项目名称</td>
        #                                     <td> ''' + url_json['projectName'] + '''</td>
        #                                 </tr>
        #                                 <tr>
        #                                     <td>采购类型</td>
        #                                     <td> ''' + url_json['procurementType'] + '''</td>
        #                                     <td>采购企业</td>
        #                                     <td> ''' + url_json['bidCompanyName'] + '''</td>
        #                                 </tr>
        #                                 <tr>
        #                                     <td>报名截止时间</td>
        #                                     <td> ''' + tool.Time_stamp_to_date_to(url_json['signUpEndTime']) + '''</td>
        #                                     <td>开标时间</td>
        #                                     <td> ''' + tool.Time_stamp_to_date_to(url_json['bidOpenTime']) + '''</td>
        #                                 </tr>
        #                                 <tr>
        #                                     <td>公告首次发布时间</td>
        #                                     <td> ''' + tool.Time_stamp_to_date_to(url_json['startSendTime']) + '''</td>
        #                                     <td>联系人</td>
        #                                     <td> ''' + url_json['linkMan'] + ''' </td>
        #                                 </tr>
        #                                 <tr>
        #                                     <td>邮箱</td>
        #                                     <td> ''' + url_json['email'] + ''' </td>
        #                                     <td>联系电话</td>
        #                                     <td> ''' + url_json['tel'] + ''' </td>
        #                                 </tr>
        #                                 <tr>
        #                                     <td>公告文件</td>
        #                                     <td><a href="''' + url_json['fileUrl'] + '''">''' + url_json[
        #     'fileName'] + '''</a></td>
        #                                 </tr>
        #                                 </table>'''
        # elif 'candidateList' in self.url:
        #     data = {"candidateId":annId,"projectId":globalType}
        #     url_text = tool.requests_post_to(
        #         'https://www.ronghw.cn/api/visitor/websiteAnnouncement/getDetail/candidateInfo?v=1628901645854', data,
        #         self.headers)
        #     url_json = json.loads(json.loads(url_text)['result'])
        #     detail_html = '''<table>
        #                                             <tr>
        #                                                 <td>项目编号</td>
        #                                                 <td>''' + url_json['projectCode'] + '''</td>
        #                                                 <td>项目名称</td>
        #                                                 <td>''' + url_json['projectName'] + '''</td>
        #                                             </tr>
        #                                             <tr>
        #                                                 <td>采购类型</td>
        #                                                 <td>''' + url_json['procurementType'] + '''</td>
        #                                                 <td>采购企业</td>
        #                                                 <td>''' + url_json['bidCompanyName'] + '''</td>
        #                                             </tr>
        #                                             <tr>
        #                                                 <td>公示期</td>
        #                                                 <td>''' + tool.Time_stamp_to_date_to(
        #         url_json['publicStartTime']) + '''至''' + tool.Time_stamp_to_date_to(
        #         url_json['publicEndTime']) + '''</td>
        #                                             </tr>
        #                                             <tr><td>中标候选人信息列表</td></tr>
        #                                             <tr>
        #                                                 <th><div>标段编号</div></th>
        #                                                 <th><div>标段名称</div></th>
        #                                                 <th><div>中标人企业名称</div></th>
        #                                             </tr>
        #                                             <tr>
        #                                                 <td>''' + url_json['cList'][0]['packCode'] + '''</td>
        #                                                 <td>''' + url_json['cList'][0]['packName'] + '''</td>
        #                                                 <td>''' + url_json['cList'][0]['companyName'] + '''</td>
        #                                             </tr>
        #                                             <tr>
        #                                                 <td>公告文件</td>
        #                                                 <td><a href="''' + url_json['fileUrl'] + '''">''' + url_json[
        #                       'fileName'] + '''</a></td>
        #                                             </tr>
        #                                             </table>'''
        # else:
        #     data = {"publicityId":annId,"projectId":globalType}
        #     url_text = tool.requests_post_to(
        #         'https://www.ronghw.cn/api/visitor/websiteAnnouncement/getDetail/pubWinResultInfo?v=1628901907594', data,
        #         self.headers)
        #     url_json = json.loads(json.loads(url_text)['result'])
        #     detail_html = '''<table>
        #                                                         <tr>
        #                                                             <td>项目编号</td>
        #                                                             <td>''' + url_json['projectCode'] + '''</td>
        #                                                             <td>项目名称</td>
        #                                                             <td>''' + url_json['projectName'] + '''</td>
        #                                                         </tr>
        #                                                         <tr>
        #                                                             <td>采购类型</td>
        #                                                             <td>''' + url_json['procurementType'] + '''</td>
        #                                                             <td>采购企业</td>
        #                                                             <td>''' + url_json['bidCompanyName'] + '''</td>
        #                                                         </tr>
        #                                                         <tr>
        #                                                             <td>公示期</td>
        #                                                             <td>''' + tool.Time_stamp_to_date_to(
        #         url_json['publicStartTime']) + '''至''' + tool.Time_stamp_to_date_to(
        #         url_json['publicEndTime']) + '''</td>
        #                                                         </tr>
        #                                                         <tr><td>成交候选人信息列表</td></tr>
        #                                                         <tr>
        #                                                             <th><div>标段编号</div></th>
        #                                                             <th><div>标段名称</div></th>
        #                                                             <th><div>成交人候选人名称</div></th>
        #                                                         </tr>
        #                                                         <tr>
        #                                                             <td>''' + url_json['cList'][0]['packCode'] + '''</td>
        #                                                             <td>''' + url_json['cList'][0]['packName'] + '''</td>
        #                                                             <td>''' + url_json['cList'][0]['companyName'] + '''</td>
        #                                                         </tr>
        #                                                         <tr>
        #                                                             <td>公告文件</td>
        #                                                             <td><a href="''' + url_json['fileUrl'] + '''">''' + \
        #                   url_json[
        #                       'fileName'] + '''</a></td>
        #                                                         </tr>
        #                                                         </table>'''
        # detail_text = ''.join(re.findall('>(.*?)<', detail_html, re.S)).replace('\xa0', '').replace('\n',
        #                                                                                                    '').replace(
        #     '\r', '').replace('\t',
        #                       '').replace(
        #     ' ', '').replace('\xa5', '')
        item = {}
        item['title'] = title.replace('\u2022', '')
        item['url'] = showurl
        item['date'] = date
        item['typeid'] = tool.get_typeid(item['title'])
        item['senddate'] = int(time.time())
        item['mid'] = 867
        item['nativeplace'] = float(tool.get_title_city(item['title']))
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
        item['resource'] = '中国融通电子商务平台'
        item["shi"] = int(item["nativeplace"])
        if len(str(int(item["shi"]))) == 4:
            item['sheng'] = int(str(item["shi"])[:2] + '00')
        elif len(str(int(item["shi"]))) == 5:
            item['sheng'] = int(str(item["shi"])[:3] + '00')
        else:
            item['sheng'] = 0
        item['removal']= title
        process_item(item)
        # print(item)

    def parse_detial_json(self, title, url, date, showurl,data):
        print(url)
        t = tool.requests_post_to(url,data=data, headers=self.headers)
        detail=eval(json.loads(t)['result'])
        print(detail)
        filename=detail.get('fileName')
        pdf_url=detail.get('fileUrl')
        zbname=[]
        for name in detail.get('cList'):
            zbname.append(name.get('companyName'))
        html=f'<a href="{pdf_url}">{filename}</a>'
        endtime=detail.get('createTime')
        if '抱歉，系统发生了错误！' in t:
            print('抱歉，系统发生了错误！')
            return
        # time.sleep(10000)
        # url_html = etree.HTML(t)
        # detail = url_html.xpath('//html')[0]
        # detail_html = etree.tostring(detail, encoding="utf-8")
        # detail_html = html.unescape(detail_html.decode()).replace('\xa0', '').replace('\ufeff', '')
        # detail_text = ''.join(url_html.xpath('//table[@id="tblInfo"]//td[not(ancestor::html)]//text()')) \
        #     .replace('\xa0', '').replace('\n', '').replace('\r', '').replace('\t', '') \
        #     .replace(' ', '').replace('\xa5', '').replace('\ufeff', '')


        item = {}
        item['title'] = title.replace('\u2022', '')
        item['url'] = showurl
        item['date'] = date
        item['typeid'] = tool.get_typeid(item['title'])
        item['senddate'] = int(time.time())
        item['mid'] = 867
        item['nativeplace'] = float(tool.get_title_city(item['title']))
        if item['nativeplace'] == 0:
            item['nativeplace'] = float(tool.more(item['title']))
        item['infotype'] = tool.get_infotype(item['title'])
        item['body'] = tool.qudiao_width(html)
        item['endtime'] = endtime
        if item['endtime'] == '':
            item['endtime'] = int(time.mktime(time.strptime(date, "%Y-%m-%d")))
        else:
            try:
                item['endtime'] = int(time.mktime(time.strptime(item['endtime'], "%Y-%m-%d")))
            except:
                item['endtime'] = int(time.mktime(time.strptime(date, "%Y-%m-%d")))
        item['tel'] = ''
        item['email'] = ''
        item['winner'] = str(zbname)
        item['address'] = ''
        item['linkman'] = ''
        item['function'] = 0
        item['resource'] = '中国融通电子商务平台'
        item["shi"] = int(item["nativeplace"])
        if len(str(int(item["shi"]))) == 4:
            item['sheng'] = int(str(item["shi"])[:2] + '00')
        elif len(str(int(item["shi"]))) == 5:
            item['sheng'] = int(str(item["shi"])[:3] + '00')
        else:
            item['sheng'] = 0
        item['removal'] = title
        process_item(item)


if __name__ == '__main__':
    import traceback, os
    try:
        jl = alashan_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
