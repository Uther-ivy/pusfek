# -*- coding: utf-8 -*-
import json
import re
import time, html
from lxml import etree
import tool
from save_database import process_item

# E招冀成
class alashan_ggzy:
    def __init__(self):
        self.url_code = [
            'http://www.hebeibidding.com/EpointWebBuilder/rest/GgSearchAction/getInfoMationList'
        ]
        self.url = self.url_code.pop(0)
        self.headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Cookie': 'sid=5B36EB33000F4B4BB4BFB3C3F2343069; userGuid=538255343; oauthClientId=admin; oauthLoginUrl=http://192.168.164.241:96/membercenter/login.html?redirect_uri=; oauthLogoutUrl=; oauthPath=http://127.0.0.1:8080/EpointWebBuilder; noOauthRefreshToken=35798b444bf8fab7f85f33640702e77b; noOauthAccessToken=cb87e3a0fdf3a81ce8d6a94a5b5e49d3',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'
        }
        self.data={
            'siteGuid': '7eb5f7f1-9041-43ad-8e13-8fcb82ea831a',
            'categoryNum': '007001001',
            'xiaqucode':"" ,
            'pageIndex': {},
            'pageSize': '12'
      }

    def parse(self):
        date = tool.date
        # date = '2020-01-06'
        page = 0
        while True:
            page += 1
            self.data['pageIndex']=page
            print('*' * 20, page, '*' * 20)
            resp = tool.requests_post(self.url,self.data, self.headers)
            html = json.loads(resp)
            detail = html['custom']
            for li in detail:
                try:
                    c = li.xpath('./a/font/text()')[0]
                except:
                    c = ''
                title = (li['title'])
                url = 'http://www.hebeibidding.com' + (li['infourl'])
                date_Today=(li['infodate'])
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
            detail = url_html.xpath('//div[@class="paragraph-box"]')[0]
            detail_html = etree.tostring(detail, method='HTML')
            detail_html = html.unescape(detail_html.decode())
            detail_text =''.join(url_html.xpath("//div[@class='paragraph-box']//text()")).replace('\xa0', '').replace('\n', '').replace('\r', '').replace('\t',
                                                                                                                      '').replace(
                ' ', '').replace('\xa5', '')
        except Exception as e:
            print(f'{e}Sorry, Page Not Found')
            return
        item = {}
        item['title'] = title.replace('\u2022', '')
        item['url'] = url
        item['date'] = date
        item['typeid'] = tool.get_typeid(item['title'])
        item['senddate'] = int(time.time())
        item['mid'] = 867
        # item['nativeplace'] = self.get_nativeplace(item['title']+detail_text)
        item['nativeplace'] = tool.get_title_city(item['title'])
        if item['nativeplace']==0:
            item['nativeplace'] = tool.more(detail_text)
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
        item['resource'] = 'E招冀成'
        item['shi'] = int(str(item['nativeplace']).split('.')[0])
        item['sheng'] = 2000
        item['removal']= title
        process_item(item)
        # print(item['nativeplace'], item['title'])

    def get_nativeplace(self, addr):
        city_list = [['2001', '石家庄市'], ['2001.001', '长安区'], ['2001.01', '行唐县'], ['2001.011', '灵寿县'], ['2001.012', '高邑县'], ['2001.013', '深泽县'], ['2001.014', '赞皇县'], ['2001.015', '无极县'], ['2001.016', '平山县'], ['2001.017', '元氏县'], ['2001.018', '赵县'], ['2001.019', '辛集市'], ['2001.020', '东开发区'], ['2001.002', '桥东区'], ['2001.02', '藁城市'], ['2001.021', '晋州市'], ['2001.022', '新乐市'], ['2001.023', '鹿泉市'], ['2001.003', '桥西区'], ['2001.004', '新华区'], ['2001.005', '井陉矿区'], ['2001.006', '裕华区'], ['2001.007', '井陉县'], ['2001.008', '正定县'], ['2001.009', '栾城县'], ['2002', '唐山市'], ['2002.001', '路南区'], ['2002.01', '迁西县'], ['2002.011', '玉田县'], ['2002.012', '唐海县'], ['2002.013', '遵化市'], ['2002.014', '迁安市'], ['2002.015', '曹妃甸区'], ['2002.016', '海港开发区'], ['2002.002', '路北区'], ['2002.003', '古冶区'], ['2002.004', '开平区'], ['2002.005', '丰南区'], ['2002.006', '丰润区'], ['2002.007', '滦县'], ['2002.008', '滦南县'], ['2002.009', '乐亭县'], ['2003', '秦皇岛市'], ['2003.001', '海港区'], ['2003.002', '山海关区'], ['2003.003', '北戴河区'], ['2003.004', '青龙满族自治县'], ['2003.005', '昌黎县'], ['2003.006', '抚宁县'], ['2003.007', '卢龙县'], ['2004', '邯郸市'], ['2004.001', '市辖区'], ['2004.01', '涉县'], ['2004.011', '磁县'], ['2004.012', '肥乡县'], ['2004.013', '永年县'], ['2004.014', '邱县'], ['2004.015', '鸡泽县'], ['2004.016', '广平县'], ['2004.017', '馆陶县'], ['2004.018', '魏县'], ['2004.019', '曲周县'], ['2004.002', '邯山区'], ['2004.02', '武安市'], ['2004.003', '丛台区'], ['2004.004', '复兴区'], ['2004.005', '峰峰矿区'], ['2004.006', '邯郸县'], ['2004.007', '临漳县'], ['2004.008', '成安县'], ['2004.009', '大名县'], ['2005', '邢台市'], ['2005.001', '桥东区'], ['2005.01', '宁晋县'], ['2005.011', '巨鹿县'], ['2005.012', '新河县'], ['2005.013', '广宗县'], ['2005.014', '平乡县'], ['2005.015', '威县'], ['2005.016', '清河县'], ['2005.017', '临西县'], ['2005.018', '南宫市'], ['2005.019', '沙河市'], ['2005.002', '桥西区'], ['2005.003', '邢台县'], ['2005.004', '临城县'], ['2005.005', '内丘县'], ['2005.006', '柏乡县'], ['2005.007', '隆尧县'], ['2005.008', '任县'], ['2005.009', '南和县'], ['2006', '保定市'], ['2006.001', '新市区'], ['2006.01', '唐县'], ['2006.011', '高阳县'], ['2006.012', '容城县'], ['2006.013', '涞源县'], ['2006.014', '望都县'], ['2006.015', '安新县'], ['2006.016', '易县'], ['2006.017', '曲阳县'], ['2006.018', '蠡县'], ['2006.019', '顺平县'], ['2006.002', '北市区'], ['2006.02', '博野县'], ['2006.021', '雄县'], ['2006.022', '涿州市'], ['2006.023', '定州市'], ['2006.024', '安国市'], ['2006.025', '高碑店市'], ['2006.026', '竞秀区'], ['2006.027', '莲池区'], ['2006.003', '南市区'], ['2006.004', '满城县'], ['2006.005', '清苑县'], ['2006.006', '涞水县'], ['2006.007', '阜平县'], ['2006.008', '徐水县'], ['2006.009', '定兴县'], ['2007', '张家口市'], ['2007.001', '桥东区'], ['2007.01', '蔚县'], ['2007.011', '阳原县'], ['2007.012', '怀安县'], ['2007.013', '万全县'], ['2007.014', '怀来县'], ['2007.015', '涿鹿县'], ['2007.016', '赤城县'], ['2007.017', '崇礼县'], ['2007.017', '崇礼区'], ['2007.002', '桥西区'], ['2007.003', '宣化区'], ['2007.004', '下花园区'], ['2007.005', '宣化县'], ['2007.006', '张北县'], ['2007.007', '康保县'], ['2007.008', '沽源县'], ['2007.009', '尚义县'], ['2008', '承德市'], ['2008.001', '双桥区'], ['2008.01', '宽城满族自治'], ['2008.011', ' 围场满族蒙古族自治县'], ['2008.002', '双滦区'], ['2008.003', '鹰手营子矿区'], ['2008.004', '承德县'], ['2008.005', '兴隆县'], ['2008.006', '平泉县'], ['2008.007', '滦平县'], ['2008.008', '隆化县'], ['2008.009', '丰宁满族自治县'], ['2009', '廊坊市'], ['2009.001', '安次区'], ['2009.01', '三河市'], ['2009.002', '广阳区'], ['2009.003', '固安县'], ['2009.004', '永清县'], ['2009.005', '香河县'], ['2009.006', '大城县'], ['2009.007', '文安县'], ['2009.008', '大厂回族自治县'], ['2009.009', '霸州市'], ['2010', '衡水市'], ['2010.001', '桃城区'], ['2010.01', '冀州市'], ['2010.011', '深州市'], ['2010.002', '枣强县'], ['2010.003', '武邑县'], ['2010.004', '武强县'], ['2010.005', '饶阳县'], ['2010.006', '安平县'], ['2010.007', '故城县'], ['2010.008', '景县'], ['2010.009', '阜城县'], ['2011', '沧州市'], ['2011.001', '新华区'], ['2011.01', '吴桥县'], ['2011.011', '献县'], ['2011.012', '孟村回族自治县'], ['2011.013', '泊头市'], ['2011.014', '任丘市'], ['2011.015', '黄骅市'], ['2011.016', '河间市'], ['2011.002', '运河区'], ['2011.003', '沧县'], ['2011.004', '青县'], ['2011.005', '东光县'], ['2011.006', '海兴县'], ['2011.007', '盐山县'], ['2011.008', '肃宁县'], ['2011.009', '南皮县']]
        for i in city_list:
            if i[1] in addr:
                return float(i[0])
        return 2000

if __name__ == '__main__':
    import traceback, os
    try:
        jl = alashan_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
        if 'pop from empty list'!=str(e):
            print('报错')
            traceback.print_exc()
            with open('error_name.txt', 'a+', encoding='utf-8')as f:
                f.write(str(os.path.basename(__file__)))
                f.write('\n')
                f.write(str(traceback.format_exc()))
                f.write('\n')
        else:
            with open('success.txt', 'a+', encoding='utf-8')as f:
                f.write(str(os.path.basename(__file__)))
                f.write('\n')
                f.write(str('无连接抓取'))
                f.write('\n')

