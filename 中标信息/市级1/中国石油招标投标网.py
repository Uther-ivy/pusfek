# -*- coding: utf-8 -*-
import json,execjs
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item
from tool import get_city
# 中国石油招标投标网
class xinyang_ggzy:
    def __init__(self):
        self.url_list = [
           ['198','199'],['198','201']
        ]
        self.url = self.url_list.pop(0)
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
            'Cookie': 'JSESSIONID=4AF9C6A030C0B887DD4DEFBB4744FFF6'
        }
        # with open('../js/加密.js', 'r', encoding='utf-8') as f:
        #     date = f.read()
        # self.ctx = execjs.compile(date)

    def parse(self):
        date = tool.date
        # date = '2020-03-20'
        page =200
        url_to = 'https://www.cnpcbidding.com/cms/pmsbidInfo/listPageOut'
        while True:
            page += 1
            data = {"url":"./list.html","pid":"180","pageSize":15,"categoryId":"183","title":"","projectType":"","pageNo":page}
            # data['pid'] = self.url[0]
            # data['categoryId'] = self.url[1]
            # data['pageNo'] = page
            # data = self.ctx.call("encry", data)
            # print(data)
            text = json.loads(tool.requests_post_to(url_to, data, self.headers))
            # requestData = text['requestData']
            # encrypted = text['encrypted']
            # text = self.ctx.call("decrys", requestData, encrypted)
            # print('qqqqq',text)
            print('*' * 20, page, '*' * 20)
            detail = text['list']
            for li in detail:
                try:
                    title = li['projectname']
                    url = 'https://www.cnpcbidding.com/' + li['id']
                    date_Today = li['dateTime'].replace('\n', '').replace('\t', '').replace('\r', '') \
                        .replace(' ', '').replace('/', '-')
                    print(title, url, date_Today)
                    # time.sleep(666)
                    if '测试' in title:
                        continue
                    if tool.Transformation(date) <= tool.Transformation(date_Today):
                        self.parse_detile(title, url, date_Today)
                    else:
                        print('日期不符, 正在切换类型', date_Today)
                        return
                except Exception:
                    traceback.print_exc()

    def parse_detile(self, title, url, date):
        data = {"url":"./page.html","pid":"180","pageSize":15,"categoryId":"183","title":"","projectType":"","pageNo":1,"dataId":"63772609708"}
        data['dataId'] = url.replace('https://www.cnpcbidding.com/', '')
        url_to = 'https://www.cnpcbidding.com/cms/pmsbidInfo/detailsOut'
        print(url)
        text = json.loads(tool.requests_post_to(url_to, data, self.headers))
        # print(text)
        datas = text['list']
        htmldata = ''
        toubiaomingcheng = ''
        zhaobiaojigou = ''
        gongshijieshuriqi = ''
        gongshiriqi = ''
        lianxiren = ''
        dianhua = ''
        # print(len(datas))

        for data in datas:
            toubiaomingcheng=data.get('projectname')
            zhaobiaojigou=data.get('tenderagencyname')
            toubiaoren=data.get('tendername')
            biaoduan=data.get('packagename')
            biaoduanbaojia=data.get('quote')
            jishufen=data.get('technicalpoints')
            shangwufen=data.get('businesspoints')
            jiagefen=data.get('pricepoints')
            pingbiaozongfen=data.get('totalpoints')
            paiming=data.get('tenderOrder')
            gongshijieshuriqi=data.get('lastmodifydate')
            gongshiriqi=data.get('publicitydatestart')
            lianxiren=data.get('assignedusername','无')
            dianhua=data.get('resultcontactphone')
            htmldata+=f'''
                <tbody>
                        <th>{toubiaoren}</th>
                        <th>{biaoduan}</th>
                        <th>{biaoduanbaojia}</th>
                        <th>{jishufen}</th>
                        <th>{shangwufen}</th>
                        <th>{jiagefen}</th>
                        <th>{pingbiaozongfen}</th>
                        <th>{paiming}</th>
               </tbody>   
            '''
        html=f"""
            <div>
                <table border="='0.5" width="70%">
                    <p class="pj">招标投标项目名称:{toubiaomingcheng}</p>
                    <p class="jg">招标代理机构：{zhaobiaojigou}</p>
                    <tbody>
                        <td >投标人</td>
                        <td>标段	</td>
                        <td>标段报价(元)	</td>
                        <td>技术分</td>
                        <td>商务分</td>
                        <td>价格分</td>
                        <td>评标总分</td>
                        <td>排名</td>
                        <td>备注</td>
                    </tbody>
                        {htmldata}
                        
                </table>
                <p>公示日期：{gongshiriqi}</p>
                <p>公示结束日期：{gongshijieshuriqi}</p>
                <p>联系人：{lianxiren}</p>
                <p>代理机构电话：{dianhua}</p>

</div>
        """

        # if detail_html is None:
        #     return
        # detail_text = ''.join(re.findall('>(.*?)<', detail_html)) \
        #     .replace('\xa0', '').replace('\n', '').replace('\r', '').replace('\t', '') \
        #     .replace(' ', '').replace('\xa5', '').replace('\ufeff', '')
        # print(111, detail_text.replace('\xa0','').replace('\xa5',''))
        # time.sleep(6666)
        item = {}
        item['title'] = title.replace('\u2022', '')
        item['url'] = url
        item['date'] = date
        item['typeid'] = tool.get_typeid(item['title'])
        item['senddate'] = int(time.time())
        item['mid'] = 867
        # print(detail_html)
        item['nativeplace'] = tool.get_title_city(item['title'])
        if item['nativeplace'] == 0:
            item['nativeplace'] = tool.more(item['title'])
        item['infotype'] = tool.get_infotype(item['title'])
        item['body'] = tool.qudiao_width(html)
        item['endtime'] = tool.get_endtime(gongshijieshuriqi)
        if item['endtime'] == '':
            item['endtime'] = int(time.mktime(time.strptime(date, "%Y-%m-%d")))
        else:
            try:
                item['endtime'] = int(time.mktime(time.strptime(item['endtime'], "%Y-%m-%d")))
            except:
                item['endtime'] = int(time.mktime(time.strptime(date, "%Y-%m-%d")))
        item['tel'] = tool.get_tel(html)
        item['email'] = ''
        item['address'] = ''
        item['linkman'] = tool.get_linkman(html)
        item['function'] =''
        item['winner'] = tool.get_winner(html)
        item['resource'] = '中国石油招标投标网'
        item["shi"] = int(str(item["nativeplace"]).split('.')[0])
        if len(str(int(item["shi"]))) == 4:
            item['sheng'] = int(str(item["shi"])[:2] + '00')
        elif len(str(int(item["shi"]))) == 5:
            item['sheng'] = int(str(item["shi"])[:3] + '00')
        else:
            item['sheng'] = 0
        item['removal']= title
        process_item(item)
        # print(item)
        # print(item['title'], item['url'], item['nativeplace'])
if __name__ == '__main__':
    import traceback, os
    try:
        jl = xinyang_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
        tool.send_error('报错文件：' + str(os.path.basename(__file__)) + '报错信息：' + str(e))