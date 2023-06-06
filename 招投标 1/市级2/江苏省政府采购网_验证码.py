# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 江苏省政府采购网
class baoshan_ggzy:
    def __init__(self):
        self.url_list = [
            'http://www.ccgp-jiangsu.gov.cn/pss/jsp/search_cggg.jsp?cgr=&xmbh=&qy=320000&pqy=&sd={}&ed={}&dljg=&cglx=&bt=&code=nznu&nr=&cgfs=&page={}'
        ]
        self.url = self.url_list.pop(0)
        self.headers = {
            'Cookie': 'homeid=1a444a31-e460-47ff-9931-1c075c0f3cd8',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        }

    def parse(self):
        date = tool.date
        # date = '2021-06-17'
        page = 0
        while True:
            page += 1
            text = tool.requests_get(self.url.format(tool.Transformation(date)*1000-86400*1000*10, tool.Transformation(date)*1000+86400*1000, page), self.headers)
            print(text)
            time.sleep(2222)
            print('*' * 20, page, '*' * 20)
            detail = json.loads(text)['result']['list']
            for li in detail:
                title = li['title'].replace('\n', '').replace('\r', '')\
                    .replace('\t', '').replace(' ', '')
                url = 'http://www.ccgp-jiangsu.gov.cn/jiangsu/js_cggg/details.html?gglb={}&ggid={}'.format(li['ggCode'], li['id'])
                date_Today = li['publishDate'][:10].replace('\n', '').replace('\r', '')\
                    .replace('\t', '').replace(' ', '').replace('.', '-')
                if '测试' in title:
                    continue
                # print(title, url, date_Today)
                # time.sleep(666)
                if tool.Transformation(date) <= tool.Transformation(date_Today):
                    if tool.removal(title, date):
                        self.parse_detile(title, url, date_Today)
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

    def parse_detile(self, title, url, date):
        print(url)
        u = 'http://www.ccgp-jiangsu.gov.cn/pss/jsp/relevantCgggGetById.jsp?ggid='+url.split('ggid=')[1]
        t = tool.requests_get(u, self.headers)
        t_json = json.loads(t)
        try:
            detail_html = t_json['data']['content']
        except:
            purchaseWay = t_json['data']['extend']['purchaseWay']
            if purchaseWay == 'cgfs001':
                purchaseWay = "公开招标"
            elif purchaseWay == "cgfs002" :
                purchaseWay ="邀请招标"
            elif purchaseWay == "cgfs003" :
                purchaseWay ="竞争性谈判"
            elif purchaseWay == "cgfs004" :
                purchaseWay ="询价"
            elif purchaseWay == "cgfs005" :
                purchaseWay ="单一来源"
            elif purchaseWay == "cgfs006" :
                purchaseWay ="协议供货"
            elif purchaseWay == "cgfs007" :
                purchaseWay ="定点采购"
            elif purchaseWay == "cgfs008" :
                purchaseWay ="竞争性磋商"
            elif purchaseWay == "cgfs009" :
                purchaseWay ="电子卖场"
            else:
                purchaseWay = ''
            try:
                contractMoney = str(t_json['data']['extend']['contractMoney']) + '元'
            except:
                contractMoney = '0万元'
            try:
                fj_name = t_json['data']['files'][0]['url']
            except:
                fj_name = '-'
            try:
                fj_value = t_json['data']['files'][0]['name']
            except:
                fj_value = '-'
            detail_html='''<div class="article_p">
                                <p style="font-weight: bold;">一、合同编号：<span style="font-weight: normal;" id="contractCode">'''+t_json['data']['extend']['contractCode']+'''</span></p>
                                <p style="font-weight: bold;">二、合同名称：<span style="font-weight: normal;" id="contractName">'''+t_json['data']['extend']['contractName']+'''</span></p>
                                <p style="font-weight: bold;">三、项目编号(或招标编号、政府采购计划编号、采购计划备案号</p>
                                <p style="font-weight: bold;padding-left: 30px;">等、如有)：<span style="font-weight: normal;" id="htProjNumber">'''+t_json['data']['projNumber']+'''</span></p>
                                <p style="font-weight: bold;">四、项目名称：<span style="font-weight: normal;" id="htProjName">'''+t_json['data']['projName']+'''</span></p>
                                <p style="font-weight: bold;">五、合同主体</p>
                                <p style="padding-left: 30px;">采购人（甲方）：<span id="htbuyerName">'''+t_json['data']['extend']['buyerName']+'''</span></p>
                                <p style="padding-left: 30px;">地址：<span id="buyerAddress">'''+t_json['data']['extend']['buyerAddr']+'''</span></p>
                                <p style="padding-left: 30px;">联系方式：<span id="buyerPhone">'''+t_json['data']['extend']['buyerContact']+'''</span></p>
                                <p style="padding-left: 30px;">供应商（乙方）：<span id="supplyName">'''+t_json['data']['extend']['supplyName']+'''</span></p>
                                <p style="padding-left: 30px;">地址：<span id="supplyAddress">'''+t_json['data']['extend']['supplyAddr']+'''</span></p>
                                <p style="padding-left: 30px;">联系方式：<span id="supplyPhone">'''+t_json['data']['extend']['supplyContact']+'''</span></p>

                                <p style="font-weight: bold;">六、合同主要信息</p>
                                <p style="padding-left: 30px;">主要标的信息：<span id="htmainMsg">'''+t_json['data']['extend']['objectName']+'''</span></p>
                                <p style="padding-left: 30px;">规格型号（或服务要求）：<span id="htsize">'''+t_json['data']['extend']['objectModel']+'''</span></p>
                                <p style="padding-left: 30px;">联系方式：<span id="htpnone">'''+t_json['data']['extend']['supplyContact']+'''</span></p>
                                <p style="padding-left: 30px;">主要标的数量：<span id="htnum">'''+t_json['data']['extend']['objectNum']+'''</span></p>
                                <p style="padding-left: 30px;">主要标的单价：<span id="heprice">'''+t_json['data']['extend']['objectUnitPrice']+'''元</span></p>
                                <p style="padding-left: 30px;">合同金额：<span id="contractMoney">'''+contractMoney+'''</span></p>
                                <p style="padding-left: 30px;">履约期限、地点等简要信息：<span id="htEdDate">'''+t_json['data']['extend']['perForm']+'''</span></p>
                                <p style="padding-left: 30px;">采购方式：<span id="purchaseWay">'''+purchaseWay+'''</span></p>
                                <p style="font-weight: bold;">七、合同签订日期：<span style="font-weight: normal;" id="signDate">'''+t_json['data']['extend']['signDate'][:10]+'''</span></p>
                                <p style="font-weight: bold;">八、合同公告日期：<span style="font-weight: normal;" id="htggrq">'''+t_json['data']['publishDate'][:10]+'''</span></p>
                                <p style="font-weight: bold;">九、其他补充事宜：<span style="font-weight: normal;" id="other"></span></p>
                                <div id="fj13">附件：<a class="as" href="'''+fj_name+'''">'''+fj_value+'''</a></div>
                                <div class="dy_close_btn">
                                    <p class="dy_close_btn_txt">
                                        “江苏政府采购网”是中国政府采购网江苏分网，是江苏省级唯一的政府采购信息发布网络媒体。“江苏政府采购网”发布的所有招投标信息，未经书面许可其他任何网站和个人不得转载。否则，“江苏政府采购网”将追究转载者的法律责任。
                                    </p>
                                </div>
                            </div>'''
        detail_text = ''.join(re.findall('>(.*?)<', detail_html)).replace('\xa0', '').replace('\n', '').\
            replace('\r', '').replace('\t', '').replace(' ', '').replace('\xa5', '')

        item = {}
        item['title'] = title.replace('\u2022', '')
        item['url'] = url
        item['date'] = date
        item['typeid'] = tool.get_typeid(item['title'])
        item['senddate'] = int(time.time())
        item['mid'] = 867
        item['nativeplace'] = self.get_nativeplace(item['title'])
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
        item['address'] = tool.get_address(detail_text)
        item['linkman'] = tool.get_linkman(detail_text)
        item['function'] = tool.get_function(detail_text)
        item['resource'] = '江苏省政府采购网'
        item['shi'] = int(item['nativeplace'])
        item['sheng'] = 5500
        item['removal']= title
        process_item(item)

    def get_nativeplace(self, addr):
        city = ''
        city_list = [['5501', '南京市'], ['5501.001', '武区'], ['5501.01', '江宁区'], ['5501.011', '六合区'], ['5501.012', '溧水县'], ['5501.013', '高淳县'], ['5501.002', '白下区'], ['5501.003', '秦淮区'], ['5501.004', '建邺区'], ['5501.005', '鼓楼区'], ['5501.006', '下关区'], ['5501.007', '浦口区'], ['5501.008', '栖霞区'], ['5501.009', '雨花台区'], ['5502', '无锡市'], ['5502.001', '崇安区'], ['5502.002', '南长区'], ['5502.003', '北塘区'], ['5502.004', '锡山区'], ['5502.005', '惠山区'], ['5502.006', '滨湖区'], ['5502.007', '江阴市'], ['5502.008', '宜兴市'], ['5503', '徐州市'], ['5503.001', '鼓楼区'], ['5503.01', '新沂市'], ['5503.011', '邳州市'], ['5503.002', '云龙区'], ['5503.003', '九里区'], ['5503.004', '贾汪区'], ['5503.005', '泉山区'], ['5503.006', '丰县'], ['5503.007', '沛县'], ['5503.008', '铜山县'], ['5503.009', '睢宁县'], ['5504', '常州市'], ['5504.001', '天宁区'], ['5504.002', '钟楼区'], ['5504.003', '戚墅堰区'], ['5504.004', '新北区'], ['5504.005', '武进区'], ['5504.006', '溧阳市'], ['5504.007', '金坛市'], ['5505', '苏州市'], ['5505.001', '沧浪区'], ['5505.01', '吴江市'], ['5505.011', '太仓市'], ['5505.002', '平江区'], ['5505.003', '金阊区'], ['5505.004', '虎丘区'], ['5505.005', '吴中区'], ['5505.006', '相城区'], ['5505.007', '常熟市'], ['5505.008', '张家港市'], ['5505.009', '昆山市'], ['5506', '南通市'], ['5506.001', '崇川区'], ['5506.002', '港闸区'], ['5506.003', '海安县'], ['5506.004', '如东县'], ['5506.005', '启东市'], ['5506.006', '如皋市'], ['5506.007', '通州市'], ['5506.008', '海门市'], ['5507', '连云港市'], ['5507.001', '连云区'], ['5507.002', '新浦区'], ['5507.003', '海州区'], ['5507.004', '赣榆县'], ['5507.005', '东海县'], ['5507.006', '灌云县'], ['5507.007', '灌南县'], ['5508', '淮安市'], ['5508.001', '清河区'], ['5508.002', '楚州区'], ['5508.003', '淮阴区'], ['5508.004', '清浦区'], ['5508.005', '涟水县'], ['5508.006', '洪泽县'], ['5508.007', '盱眙县'], ['5508.008', '金湖县'], ['5509', '盐城市'], ['5509.001', '亭湖区'], ['5509.002', '盐都区'], ['5509.003', '响水县'], ['5509.004', '滨海县'], ['5509.005', '阜宁县'], ['5509.006', '射阳县'], ['5509.007', '建湖县'], ['5509.008', '东台市'], ['5509.009', '大丰市'], ['5510', '扬州市'], ['5510.001', '广陵区'], ['5510.002', '邗江区'], ['5510.003', '郊区'], ['5510.004', '宝应县'], ['5510.005', '仪征市'], ['5510.006', '高邮市'], ['5510.007', '江都市'], ['5511', '镇江市'], ['5511.001', '京口区'], ['5511.002', '润州区'], ['5511.003', '丹徒区'], ['5511.004', '丹阳市'], ['5511.005', '扬中市'], ['5511.006', '句容市'], ['5512', '泰州市'], ['5512.001', '海陵区'], ['5512.002', '高港区'], ['5512.003', '兴化市'], ['5512.004', '靖江市'], ['5512.005', '泰兴市'], ['5512.006', '姜堰市'], ['5513', '宿迁市'], ['5513.001', '宿城区'], ['5513.002', '宿豫区'], ['5513.003', '沭阳县'], ['5513.004', '泗阳县'], ['5513.005', '泗洪县']]

        for i in city_list:
            if i[1] in addr:
                city = float(i[0])
                break
        if city == '':
            city = 5500
        return city

if __name__ == '__main__':

    import traceback, os
    try:
        jl = baoshan_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
