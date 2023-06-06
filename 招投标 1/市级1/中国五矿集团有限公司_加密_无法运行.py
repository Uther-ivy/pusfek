# -*- coding: utf-8 -*-
import json
import re
import time, html, execjs
from lxml import etree
import tool
from save_database import process_item


# 中国五矿集团有限公司
class alashan_ggzy:
    def __init__(self):
        self.url_code = [
            'https://ec.mcc.com.cn/b2b/web/two/indexinfoAction.do?currpage={}&actionType={}&xxposition=cgxx&xxmc=&fbrq1=&fbrq2=',
            'https://ec.mcc.com.cn/b2b/web/two/indexinfoAction.do?currpage={}&xxposition=cqgg&actionType={}&pubdesc=&audittime=&audittime2=',
            'https://ec.mcc.com.cn/b2b/web/two/indexinfoAction.do?currpage={}&actionType={}&xxposition=zhongbgg&pubdesc=&releasedate1=&releasedate2='
        ]
        self.url = self.url_code.pop(0)
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Cookie': 'SUNWAY-ESCM-COOKIE=83eeefce-e27e-4eec-9768-3fdeaddf9cd8; JSESSIONID=qe-0g1tmv7cS6lM_Ltxw2gsHJ5JJOt8ruVuRIlKVX_FjbR69oakD!1884797896',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
        }

    def get_url(self, url_code):
        ls = '''function showNouseDepartmentMessage(sbbm){	
                  return 'https://ec.mcc.com.cn/b2b/web/two/indexinfoAction.do?actionType=showNouseDepartmentDetail&sbbm='+sbbm;   
                }
                function showCgxjMessage(xjbm){
                  return "https://ec.mcc.com.cn/b2b/web/two/indexinfoAction.do?actionType=showCgxjDetail&xjbm="+xjbm;
                }
                //
                function showZbsMessage(inviteid){
                  return "https://ec.mcc.com.cn/b2b/web/two/indexinfoAction.do?actionType=showZbsDetail&inviteid="+inviteid;
                }


                function showCgwzMessage(xqbh){
                  return "https://ec.mcc.com.cn/b2b/web/two/indexinfoAction.do?actionType=showUrgentDetail&xxbh="+xqbh;
                }

                function showWxwzMessage(gybh){
                  return "https://ec.mcc.com.cn/b2b/web/two/indexinfoAction.do?actionType=showSaleDetail&xxbh="+gybh;
                }

                function showOldMaterialMessage(xqbh){
                  return "https://ec.mcc.com.cn/b2b/web/two/indexinfoAction.do?actionType=showOldMaterialDetail&xxbh="+xqbh;
                }

                function showInvalidMaterialMessage(xqbh){
                  return "https://ec.mcc.com.cn/b2b/web/two/indexinfoAction.do?actionType=showInvalidMaterialDetail&xxbh="+xqbh;
                }


                function showXcpMessage(dwbm,xh){
                  return "https://ec.mcc.com.cn/b2b/web/two/indexinfoAction.do?actionType=showNewProductDetail&dwbm="+dwbm+"&xh="+xh;
                }

                function showYzbgsMessage(publicitycode,inviteid){
                  return "https://ec.mcc.com.cn/b2b/web/two/indexinfoAction.do?actionType=showYzbgsDetail&xxbh="+publicitycode+"&inviteid="+inviteid;
                }
                //
                function showZhongbggMessage(publicitycode,inviteid){
                  return "https://ec.mcc.com.cn/b2b/web/two/indexinfoAction.do?actionType=showZhongbggDetail&xxbh="+publicitycode+"&inviteid="+inviteid;
                }
                //
                function showCqggMessage(publicitycode){
                  return "https://ec.mcc.com.cn/b2b/web/two/indexinfoAction.do?actionType=showCqggDetail&xxbh="+publicitycode;
                }
                function showPxjgmessage(pbbm){
                  return "https://ec.mcc.com.cn/b2b/web/two/indexinfoAction.do?actionType=showPxjgDetail&xxbh="+pbbm;
                }
                function showCgxjMessage(xjbm){
                  return "https://ec.mcc.com.cn/b2b/web/two/indexinfoAction.do?actionType=showCgxjDetail&xjbm="+xjbm;
                }

                function showMessage(xxbh){
                  return "https://ec.mcc.com.cn/b2b/web/two/indexinfoAction.do?actionType=showMessage&xxbh="+xxbh;
                }

                function showZgysDetail(zgyswjbm){
                  return "https://ec.mcc.com.cn/b2b/web/two/indexinfoAction.do?actionType=showZgysDetail&zgyswjbm="+zgyswjbm;
                }
                '''
        url_js = execjs.compile(ls)
        return url_js.call(url_code[0], url_code[1])

    def parse(self):
        date = tool.date
        # date = '2021-04-08'
        page = 0
        code = tool.requests_get('https://ec.mcc.com.cn/logonAction.do', self.headers)
        code_ls = re.findall('''</ol>.*?<a href="javascript:void\(0\);" onclick="toPage\('(.*?)','(.*?)'\);return false;"><img''', code, re.S)
        while True:
            page += 1
            cc = ''
            print('*' * 20, page, '*' * 20)
            for c in code_ls:
                if c[1] in self.url:
                    cc = c[0]
                    break
            text = tool.requests_get(self.url.format(page, cc), self.headers)
            text = text.replace('<td class="txtLeft">', '<tr><td class="txtLeft">')
            detail = etree.HTML(text).xpath('//*[@class="datatlb"]/tr')
            print(len(detail))
            for li in detail[1:]:
                try:
                    title = li.xpath('./td[1]/a/@title')[0]
                    url_ls = li.xpath('./td[1]/a/@onclick')[0].replace("'", '').replace(")", '').split('(')
                except:
                    continue
                url = self.get_url(url_ls)
                date_Today = li.xpath('./td[2]/text()')[0]
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
                    break



    def parse_detile(self, title, url, date):
        print(url)
        url_text = tool.requests_get(url, self.headers)
        url_html = etree.HTML(url_text)
        try:
            detail = url_html.xpath('/html/body/div[4]')[0]
            detail_html = etree.tostring(detail, method='HTML')
            detail_html = html.unescape(detail_html.decode()).replace('\xa0', '')
            detail_text = url_html.xpath('string(/html/body/div[4])').replace('\xa0', '').replace('\n', '').replace(
                '\r', '').replace('\t',
                                  '').replace(
                ' ', '').replace('\xa5', '')
        except:
            return
        item = {}
        item['title'] = title.replace('\u2022', '')
        item['url'] = url
        item['date'] = date
        item['typeid'] = tool.get_typeid(item['title'])
        item['senddate'] = int(time.time())
        item['mid'] = 867
        item['nativeplace'] = float(tool.get_title_city(item['title']))
        if item['nativeplace'] == 0:
            item['nativeplace'] = float(tool.more(item['title'] + detail_text))
        item['infotype'] = tool.get_infotype(item['title'])
        item['body'] = tool.qudiao_width(detail_html)
        ht_ = '''<div class="tips">
  	<div class="tips_prt"><a href="javascript:void(0)" onclick="preview()">【打印本页】</a></div>
    <div class="tips_cls"><a href="javascript:void(0)" onclick="window.close();">【关闭本页】</a></div>
  </div>'''
        item['body'] = item['body'].replace(ht_, '')
        ht_ = '''<div class="foot">







<p style="height: 23px"><a href="/b2b/web/two/indexinfoAction.do?actionType=aboutUs">关于我们</a>
                  |
                  <a href="/b2b/web/two/indexinfoAction.do?actionType=aboutUsMap">网站地图</a>
                  |
                  <a href="/b2b/web/two/indexinfoAction.do?actionType=aboutWzsm">网站声明</a>
                  |
                  <a href="/b2b/web/two/indexinfoAction.do?actionType=aboutUs">帮助中心</a>
                  |
                  <a href="/b2b/web/two/indexinfoAction.do?actionType=aboutUsLink">联系我们</a></p>
<p style="height: 31px">版权所有：<a href="http://www.mcc.com.cn" target="_blank">中国冶金科工集团有限公司</a>    网站管理：<a href="http://ec.mcc.com.cn" target="_blank">中国冶金科工集团有限公司采购中心</a>   技术支持：<a href="http://www.sunwayworld.com" target="_blank">北京三维天地科技有限公司</a>    </p>
<div>运维电话：010-60163313     运维时间：周一至周五 9:00-11:00 14:00-16:00    </div>

</div>'''
        item['body'] = item['body'].replace(ht_, '')
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
        item['resource'] = '中国五矿集团有限公司'
        item["shi"] = int(item["nativeplace"])
        if len(str(item["nativeplace"])) == 4:
            item['sheng'] = int(str(item["nativeplace"])[:2] + '00')
        elif len(str(item["nativeplace"])) == 5:
            item['sheng'] = int(str(item["nativeplace"])[:3] + '00')
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
