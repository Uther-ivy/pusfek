# -*- coding: utf-8 -*-
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
# from save_database import process_item

# 河北省招投标公共服务平台
# tool.send_error('报错文件：'+str(os.path.basename(__file__))+'报错信息：'+str(e))
class xinyang_ggzy:
    def __init__(self):
        self.url_list = [
            # 建设工程
            # 招标公告
            'http://www.hebeieb.com/tender/xxgk/zbgg.do',
            # 变更公告
            'http://www.hebeieb.com/tender/xxgk/bggg.do',
            # 中标候选人
            'http://www.hebeieb.com/tender/xxgk/pbgs.do',
            # 中标结果
            'http://www.hebeieb.com/tender/xxgk/zhongbgg.do'
        ]
        self.url = self.url_list.pop(0)
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        }

    def parse(self):
        date = tool.date
        # date = '2020-03-20'
        page = 0
        data = {
            "page": '',
            "TimeStr": '',
            "allDq": "reset2",
            "allHy": "reset1",
            "AllPtName": '',
            "KeyStr": '',
            "KeyType": "ggname"
        }
        while True:
            if page == 0:
                data['page'] = ''
            else:
                data['page'] = str(page)
            page += 1
            text = tool.requests_post(self.url, data, self.headers)
            text = '<div class="AAA">' + text + '</div>'
            print('*' * 20, page, '*' * 20)
            html = HTML(text)
            # print(html.xpath('//div[@class="AAA"]/div[1]/text()')[0])
            # print(11, text)
            # time.sleep(6666)
            detail = html.xpath('//div[@class="AAA"]/div')
            for li in range(1,len(detail)):
                title = html.xpath('//div[@class="AAA"]/div[{}]/div/h4/a/@title'.format(li+1))[0]
                url = 'http://www.hebeieb.com' + \
                      html.xpath('//div[@class="AAA"]/div[{}]/div/h4/a/@href'.format(li + 1))[0]
                categoryid = re.findall('categoryid=(.*?)&', url)[0]
                infoid = re.findall('infoid=(.*?)&', url)[0]
                # print(categoryid, infoid)
                # time.sleep(6666)
                url = 'http://www.hebeieb.com/infogk/newDetail.do?categoryid={}&infoid={}&laiyuan=[%E5%B9%B3%E5%8F%B0%E5%86%85]'.format(categoryid, infoid)
                date_Today = html.xpath('//div[@class="AAA"]/div[{}]/div/h4/span/text()'.format(li+1))[0].replace('\n', '').replace('\t', '').replace('\r', '')\
                    .replace(' ', '')
                # print(title, url, date_Today)
                # time.sleep(666)
                if '测试' in title:
                    continue
                if tool.Transformation(date) <= tool.Transformation(date_Today):
                    if tool.removal(title, date):
                        self.parse_detile(title, url, date_Today)
                    else:
                        print('【existence】', url)
                        continue
                else:
                    print('日期不符, 正在切换类型', date_Today)
                    self.url = self.url_list.pop(0)
                    page = 0
                    break
            if page == 20:
                self.url = self.url_list.pop(0)
                break

    def parse_detile(self, title, url, date):
        print(url)
        url_html = etree.HTML(tool.requests_get(url, self.headers))
        detail = url_html.xpath('//*[@id="article_con"]/div')[0]
        detail_html = etree.tostring(detail, method='HTML')
        detail_html = html.unescape(detail_html.decode()).replace('\xa0', '').replace('\ufeff', '')
        detail_text = url_html.xpath('string(//*[@id="article_con"]/div)') \
            .replace('\xa0', '').replace('\n', '').replace('\r', '').replace('\t', '') \
            .replace(' ', '').replace('\xa5', '').replace('\ufeff', '')
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
        item['body'] = detail_html
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
        item['resource'] = '河北省招投标公共服务平台'
        item['shi'] = int(str(item["nativeplace"]).split('.')[0])
        item['sheng'] = 2000
        item['removal']= title
        # process_item(item)
        print(item['body'])

    def get_nativeplace(self, addr):
        city = ''
        city_lists = [ ['2001.001', '长安区'], ['2001.01', '行唐县'], ['2001.011', '灵寿县'], ['2001.012', '高邑县'], ['2001.013', '深泽县'], ['2001.014', '赞皇县'], ['2001.015', '无极县'], ['2001.016', '平山县'], ['2001.017', '元氏县'], ['2001.018', '赵县'], ['2001.019', '辛集'], ['2001.020', '东开发区'], ['2001.002', '桥东区'], ['2001.02', '藁城'], ['2001.021', '晋州'], ['2001.022', '新乐'], ['2001.023', '鹿泉'], ['2001.003', '桥西区'], ['2001.004', '新华区'], ['2001.005', '井陉矿区'], ['2001.006', '裕华区'], ['2001.007', '井陉县'], ['2001.008', '正定县'], ['2001.009', '栾城县'], ['2002.001', '路南区'], ['2002.01', '迁西县'], ['2002.011', '玉田县'], ['2002.012', '唐海县'], ['2002.013', '遵化'], ['2002.014', '迁安'], ['2002.015', '曹妃甸区'], ['2002.016', '海港开发区'], ['2002.002', '路北区'], ['2002.003', '古冶区'], ['2002.004', '开平区'], ['2002.005', '丰南区'], ['2002.006', '丰润区'], ['2002.007', '滦县'], ['2002.008', '滦南县'], ['2002.009', '乐亭县'],  ['2003.001', '海港区'], ['2003.002', '山海关区'], ['2003.003', '北戴河区'], ['2003.004', '青龙满族自治县'], ['2003.005', '昌黎县'], ['2003.006', '抚宁县'], ['2003.007', '卢龙县'], ['2004.001', '辖区'], ['2004.01', '涉县'], ['2004.011', '磁县'], ['2004.012', '肥乡县'], ['2004.013', '永年县'], ['2004.014', '邱县'], ['2004.015', '鸡泽县'], ['2004.016', '广平县'], ['2004.017', '馆陶县'], ['2004.018', '魏县'], ['2004.019', '曲周县'], ['2004.002', '邯山区'], ['2004.02', '武安'], ['2004.003', '丛台区'], ['2004.004', '复兴区'], ['2004.005', '峰峰矿区'], ['2004.006', '邯郸县'], ['2004.007', '临漳县'], ['2004.008', '成安县'], ['2004.009', '大名县'],  ['2005.001', '桥东区'], ['2005.01', '宁晋县'], ['2005.011', '巨鹿县'], ['2005.012', '新河县'], ['2005.013', '广宗县'], ['2005.014', '平乡县'], ['2005.015', '威县'], ['2005.016', '清河县'], ['2005.017', '临西县'], ['2005.018', '南宫'], ['2005.019', '沙河'], ['2005.002', '桥西区'], ['2005.003', '邢台县'], ['2005.004', '临城县'], ['2005.005', '内丘县'], ['2005.006', '柏乡县'], ['2005.007', '隆尧县'], ['2005.008', '任县'], ['2005.009', '南和县'], ['2006.001', '新区'], ['2006.01', '唐县'], ['2006.011', '高阳县'], ['2006.012', '容城县'], ['2006.013', '涞源县'], ['2006.014', '望都县'], ['2006.015', '安新县'], ['2006.016', '易县'], ['2006.017', '曲阳县'], ['2006.018', '蠡县'], ['2006.019', '顺平县'], ['2006.002', '北区'], ['2006.02', '博野县'], ['2006.021', '雄县'], ['2006.022', '涿州'], ['2006.023', '定州'], ['2006.024', '安国'], ['2006.025', '高碑店'], ['2006.026', '竞秀区'], ['2006.027', '莲池区'], ['2006.003', '南区'], ['2006.004', '满城县'], ['2006.005', '清苑县'], ['2006.006', '涞水县'], ['2006.007', '阜平县'], ['2006.008', '徐水县'], ['2006.009', '定兴县'],  ['2007.001', '桥东区'], ['2007.01', '蔚县'], ['2007.011', '阳原县'], ['2007.012', '怀安县'], ['2007.013', '万全县'], ['2007.014', '怀来县'], ['2007.015', '涿鹿县'], ['2007.016', '赤城县'], ['2007.017', '崇礼县'], ['2007.002', '桥西区'], ['2007.003', '宣化区'], ['2007.004', '下花园区'], ['2007.005', '宣化县'], ['2007.006', '张北县'], ['2007.007', '康保县'], ['2007.008', '沽源县'], ['2007.009', '尚义县'],  ['2008.001', '双桥区'], ['2008.01', '宽城满族自治'], ['2008.011', ' 围场满族蒙古族自治县'], ['2008.002', '双滦区'], ['2008.003', '鹰手营子矿区'], ['2008.004', '承德县'], ['2008.005', '兴隆县'], ['2008.006', '平泉县'], ['2008.007', '滦平县'], ['2008.008', '隆化县'], ['2008.009', '丰宁满族自治县'], ['2009.001', '安次区'], ['2009.01', '三河'], ['2009.002', '广阳区'], ['2009.003', '固安县'], ['2009.004', '永清县'], ['2009.005', '香河县'], ['2009.006', '大城县'], ['2009.007', '文安县'], ['2009.008', '大厂回族自治县'], ['2009.009', '霸州'],  ['2010.001', '桃城区'], ['2010.01', '冀州'], ['2010.011', '深州'], ['2010.002', '枣强县'], ['2010.003', '武邑县'], ['2010.004', '武强县'], ['2010.005', '饶阳县'], ['2010.006', '安平县'], ['2010.007', '故城县'], ['2010.008', '景县'], ['2010.009', '阜城县'],['2011.001', '新华区'], ['2011.01', '吴桥县'], ['2011.011', '献县'], ['2011.012', '孟村回族自治县'], ['2011.013', '泊头'], ['2011.014', '任丘'], ['2011.015', '黄骅'], ['2011.016', '河间'], ['2011.002', '运河区'], ['2011.003', '沧县'], ['2011.004', '青县'], ['2011.005', '东光县'], ['2011.006', '海兴县'], ['2011.007', '盐山县'], ['2011.008', '肃宁县'], ['2011.009', '南皮县']]
        city_list = [['2001', '石家庄'], ['2002', '唐山'], ['2003', '秦皇岛'], ['2004', '邯郸'], ['2005', '邢台'],['2006', '保定'] , ['2007', '张家口'],['2008', '承德'], ['2009', '廊坊'], ['2010', '衡水'], ['2011', '沧州']]
        for i in city_list:
            if i[1] in addr:
                city = int(i[0])
                for y in city_lists:
                    if y[1] in addr:
                        if int(float(y[0]))==int(city):
                            city=float(y[0])
                break

        if city == '':
            city = 2000
        return city
if __name__ == '__main__':
    import traceback, os
    try:
        jl = xinyang_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
        tool.send_error('报错文件：'+str(os.path.basename(__file__))+'报错信息：'+str(e))