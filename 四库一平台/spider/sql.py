# -*-coding:utf-8 -*-
import datetime
import re
import time
import traceback
import pymysql
from dbutils.pooled_db import PooledDB
from pypinyin import lazy_pinyin


db = PooledDB(
        creator=pymysql,
        blocking=True,
        maxconnections=30,
        maxshared=30,
        ping=1,
        host='120.211.70.99',
        user='root',
        passwd='zx1234',
        db='new',
        port=3306,
        charset="utf8"
    )
# db = PooledDB(
#     creator=pymysql,
#     blocking=True,
#     maxconnections=15,
#     maxshared=10,
#     host='localhost',
#     user='root',
#     passwd='',
#     db='uther',
#     port=3306,
#     charset="utf8"
# )
def Transformation(date):
    print(date)
    if '1970-01-01' in str(date):
        times = 0
    if '1900-01-01' in str(date):
        times = 0
    elif '-' in str(date):
        times = int(time.mktime(time.strptime(date, "%Y-%m-%d")))
    elif len(str(date)) == 13:
        times = int(date) / 1000
    else:
        times = int(date)

    return times


def str_date(date):
    if '-' in str(date):
        str_times = date
    elif len(str(date)) == 13:
        str_times = datetime.datetime.fromtimestamp(date / 1000).strftime("%Y-%m-%d")
    else:
        str_times = '1970-01-01'

    return str_times


# 查找cityid
def findcityid(name):
    if name == 0:
        return 0
    if "-" in name:
        cityid = re.findall(r'(\w+)\-(\w+)', name)[0]
        city=cityid[1]
    else:
        city = re.findall(r'(\w+)', name)[0]
    print(city)
    # print(city,len(cityid))
    with open('spider/yunqi_city.json', 'r', encoding='utf8') as r:
        lines = eval(r.read())
        # print(lines)
    for lis in lines.get('RECORDS'):
        # print(lis)
        if city in lis['name']:
            print(lis['name'], lis['id'])
            return lis['id']


def get_region(regid):
    print(regid)
    region = [
        {'region_id': '110000', 'region_fullname': '北京市'},
        {'region_id': '120000', 'region_fullname': '天津市'},
        {'region_id': '130000', 'region_fullname': '河北省'},
        {'region_id': '140000', 'region_fullname': '山西省'},
        {'region_id': '150000', 'region_fullname': '内蒙古自治区'},
        {'region_id': '210000', 'region_fullname': '辽宁省'},
        {'region_id': '220000', 'region_fullname': '吉林省'},
        {'region_id': '230000', 'region_fullname': '黑龙江省'},
        {'region_id': '310000', 'region_fullname': '上海市'},
        {'region_id': '320000', 'region_fullname': '江苏省'},
        {'region_id': '330000', 'region_fullname': '浙江省'},
        {'region_id': '340000', 'region_fullname': '安徽省'},
        {'region_id': '350000', 'region_fullname': '福建省'},
        {'region_id': '360000', 'region_fullname': '江西省'},
        {'region_id': '370000', 'region_fullname': '山东省'},
        {'region_id': '410000', 'region_fullname': '河南省'},
        {'region_id': '420000', 'region_fullname': '湖北省'},
        {'region_id': '430000', 'region_fullname': '湖南省'},
        {'region_id': '440000', 'region_fullname': '广东省'},
        {'region_id': '450000', 'region_fullname': '广西壮族自治区'},
        {'region_id': '460000', 'region_fullname': '海南省'},
        {'region_id': '500000', 'region_fullname': '重庆市'},
        {'region_id': '510000', 'region_fullname': '四川省'},
        {'region_id': '520000', 'region_fullname': '贵州省'},
        {'region_id': '530000', 'region_fullname': '云南省'},
        {'region_id': '540000', 'region_fullname': '西藏自治区'},
        {'region_id': '610000', 'region_fullname': '陕西省'},
        {'region_id': '620000', 'region_fullname': '甘肃省'},
        {'region_id': '630000', 'region_fullname': '青海省'},
        {'region_id': '640000', 'region_fullname': '宁夏回族自治区'},
        {'region_id': '650000', 'region_fullname': '新疆维吾尔自治区'},
        {'region_id': '650000', 'region_fullname': '新疆建设兵团'},
        {'region_id': '110100', 'region_name': '北京市', 'region_fullname': '北京市-北京市'},
        {'region_id': '120100', 'region_name': '天津市', 'region_fullname': '天津市-天津市'},
        {'region_id': '120200', 'region_name': '天津市', 'region_fullname': '天津市-天津市'},
        {'region_id': '130100', 'region_name': '石家庄', 'region_fullname': '河北省-石家庄市'},
        {'region_id': '130200', 'region_name': '唐山', 'region_fullname': '河北省-唐山市'},
        {'region_id': '130300', 'region_name': '秦皇岛', 'region_fullname': '河北省-秦皇岛市'},
        {'region_id': '130400', 'region_name': '邯郸', 'region_fullname': '河北省-邯郸市'},
        {'region_id': '130500', 'region_name': '邢台', 'region_fullname': '河北省-邢台市'},
        {'region_id': '130600', 'region_name': '保定', 'region_fullname': '河北省-保定市'},
        {'region_id': '130700', 'region_name': '张家口', 'region_fullname': '河北省-张家口市'},
        {'region_id': '130800', 'region_name': '承德', 'region_fullname': '河北省-承德市'},
        {'region_id': '130900', 'region_name': '沧州', 'region_fullname': '河北省-沧州市'},
        {'region_id': '131000', 'region_name': '廊坊', 'region_fullname': '河北省-廊坊市'},
        {'region_id': '131100', 'region_name': '衡水', 'region_fullname': '河北省-衡水市'},
        {'region_id': '140100', 'region_name': '太原', 'region_fullname': '山西省-太原市'},
        {'region_id': '140200', 'region_name': '大同', 'region_fullname': '山西省-大同市'},
        {'region_id': '140300', 'region_name': '阳泉', 'region_fullname': '山西省-阳泉市'},
        {'region_id': '140400', 'region_name': '长治', 'region_fullname': '山西省-长治市'},
        {'region_id': '140500', 'region_name': '晋城', 'region_fullname': '山西省-晋城市'},
        {'region_id': '140600', 'region_name': '朔州', 'region_fullname': '山西省-朔州市'},
        {'region_id': '140700', 'region_name': '晋中', 'region_fullname': '山西省-晋中市'},
        {'region_id': '140800', 'region_name': '运城', 'region_fullname': '山西省-运城市'},
        {'region_id': '140900', 'region_name': '忻州', 'region_fullname': '山西省-忻州市'},
        {'region_id': '141000', 'region_name': '临汾', 'region_fullname': '山西省-临汾市'},
        {'region_id': '141100', 'region_name': '吕梁', 'region_fullname': '山西省-吕梁市'},
        {'region_id': '150100', 'region_name': '呼和浩特', 'region_fullname': '内蒙古自治区-呼和浩特市'},
        {'region_id': '150200', 'region_name': '包头', 'region_fullname': '内蒙古自治区-包头市'},
        {'region_id': '150300', 'region_name': '乌海', 'region_fullname': '内蒙古自治区-乌海市'},
        {'region_id': '150400', 'region_name': '赤峰', 'region_fullname': '内蒙古自治区-赤峰市'},
        {'region_id': '150500', 'region_name': '通辽', 'region_fullname': '内蒙古自治区-通辽市'},
        {'region_id': '150600', 'region_name': '鄂尔多斯', 'region_fullname': '内蒙古自治区-鄂尔多斯市'},
        {'region_id': '150700', 'region_name': '呼伦贝尔', 'region_fullname': '内蒙古自治区-呼伦贝尔市'},
        {'region_id': '150800', 'region_name': '巴彦淖尔', 'region_fullname': '内蒙古自治区-巴彦淖尔市'},
        {'region_id': '150900', 'region_name': '乌兰察布', 'region_fullname': '内蒙古自治区-乌兰察布市'},
        {'region_id': '152200', 'region_name': '兴安盟', 'region_fullname': '内蒙古自治区-兴安盟'},
        {'region_id': '152500', 'region_name': '锡林郭勒盟', 'region_fullname': '内蒙古自治区-锡林郭勒盟'},
        {'region_id': '152900', 'region_name': '阿拉善盟', 'region_fullname': '内蒙古自治区-阿拉善盟'},
        {'region_id': '210100', 'region_name': '沈阳', 'region_fullname': '辽宁省-沈阳市'},
        {'region_id': '210200', 'region_name': '大连', 'region_fullname': '辽宁省-大连市'},
        {'region_id': '210300', 'region_name': '鞍山', 'region_fullname': '辽宁省-鞍山市'},
        {'region_id': '210400', 'region_name': '抚顺', 'region_fullname': '辽宁省-抚顺市'},
        {'region_id': '210500', 'region_name': '本溪', 'region_fullname': '辽宁省-本溪市'},
        {'region_id': '210600', 'region_name': '丹东', 'region_fullname': '辽宁省-丹东市'},
        {'region_id': '210700', 'region_name': '锦州', 'region_fullname': '辽宁省-锦州市'},
        {'region_id': '210800', 'region_name': '营口', 'region_fullname': '辽宁省-营口市'},
        {'region_id': '210900', 'region_name': '阜新', 'region_fullname': '辽宁省-阜新市'},
        {'region_id': '211000', 'region_name': '辽阳', 'region_fullname': '辽宁省-辽阳市'},
        {'region_id': '211100', 'region_name': '盘锦', 'region_fullname': '辽宁省-盘锦市'},
        {'region_id': '211200', 'region_name': '铁岭', 'region_fullname': '辽宁省-铁岭市'},
        {'region_id': '211300', 'region_name': '朝阳', 'region_fullname': '辽宁省-朝阳市'},
        {'region_id': '211400', 'region_name': '葫芦岛', 'region_fullname': '辽宁省-葫芦岛市'},
        {'region_id': '220100', 'region_name': '长春', 'region_fullname': '吉林省-长春市'},
        {'region_id': '220200', 'region_name': '吉林', 'region_fullname': '吉林省-吉林市'},
        {'region_id': '220300', 'region_name': '四平', 'region_fullname': '吉林省-四平市'},
        {'region_id': '220400', 'region_name': '辽源', 'region_fullname': '吉林省-辽源市'},
        {'region_id': '220500', 'region_name': '通化', 'region_fullname': '吉林省-通化市'},
        {'region_id': '220600', 'region_name': '白山', 'region_fullname': '吉林省-白山市'},
        {'region_id': '220700', 'region_name': '松原', 'region_fullname': '吉林省-松原市'},
        {'region_id': '220800', 'region_name': '白城', 'region_fullname': '吉林省-白城市'},
        {'region_id': '222400', 'region_name': '延边朝鲜族自治州', 'region_fullname': '吉林省-延边朝鲜族自治州'},
        {'region_id': '230100', 'region_name': '哈尔滨', 'region_fullname': '黑龙江省-哈尔滨市'},
        {'region_id': '230200', 'region_name': '齐齐哈尔', 'region_fullname': '黑龙江省-齐齐哈尔市'},
        {'region_id': '230300', 'region_name': '鸡西', 'region_fullname': '黑龙江省-鸡西市'},
        {'region_id': '230400', 'region_name': '鹤岗', 'region_fullname': '黑龙江省-鹤岗市'},
        {'region_id': '230500', 'region_name': '双鸭山', 'region_fullname': '黑龙江省-双鸭山市'},
        {'region_id': '230600', 'region_name': '大庆', 'region_fullname': '黑龙江省-大庆市'},
        {'region_id': '230700', 'region_name': '伊春', 'region_fullname': '黑龙江省-伊春市'},
        {'region_id': '230800', 'region_name': '佳木斯', 'region_fullname': '黑龙江省-佳木斯市'},
        {'region_id': '230900', 'region_name': '七台河', 'region_fullname': '黑龙江省-七台河市'},
        {'region_id': '231000', 'region_name': '牡丹江', 'region_fullname': '黑龙江省-牡丹江市'},
        {'region_id': '231100', 'region_name': '黑河', 'region_fullname': '黑龙江省-黑河市'},
        {'region_id': '231200', 'region_name': '绥化', 'region_fullname': '黑龙江省-绥化市'},
        {'region_id': '232700', 'region_name': '大兴安岭地区', 'region_fullname': '黑龙江省-大兴安岭地区'},
        {'region_id': '310100', 'region_name': '上海', 'region_fullname': '上海市-上海市'},
        {'region_id': '320100', 'region_name': '南京', 'region_fullname': '江苏省-南京市'},
        {'region_id': '320200', 'region_name': '无锡', 'region_fullname': '江苏省-无锡市'},
        {'region_id': '320300', 'region_name': '徐州', 'region_fullname': '江苏省-徐州市'},
        {'region_id': '320400', 'region_name': '常州', 'region_fullname': '江苏省-常州市'},
        {'region_id': '320500', 'region_name': '苏州', 'region_fullname': '江苏省-苏州市'},
        {'region_id': '320600', 'region_name': '南通', 'region_fullname': '江苏省-南通市'},
        {'region_id': '320700', 'region_name': '连云港', 'region_fullname': '江苏省-连云港市'},
        {'region_id': '320800', 'region_name': '淮安', 'region_fullname': '江苏省-淮安市'},
        {'region_id': '320900', 'region_name': '盐城', 'region_fullname': '江苏省-盐城市'},
        {'region_id': '321000', 'region_name': '扬州', 'region_fullname': '江苏省-扬州市'},
        {'region_id': '321100', 'region_name': '镇江', 'region_fullname': '江苏省-镇江市'},
        {'region_id': '321200', 'region_name': '泰州', 'region_fullname': '江苏省-泰州市'},
        {'region_id': '321300', 'region_name': '宿迁', 'region_fullname': '江苏省-宿迁市'},
        {'region_id': '330100', 'region_name': '杭州', 'region_fullname': '浙江省-杭州市'},
        {'region_id': '330200', 'region_name': '宁波', 'region_fullname': '浙江省-宁波市'},
        {'region_id': '330300', 'region_name': '温州', 'region_fullname': '浙江省-温州市'},
        {'region_id': '330400', 'region_name': '嘉兴', 'region_fullname': '浙江省-嘉兴市'},
        {'region_id': '330500', 'region_name': '湖州', 'region_fullname': '浙江省-湖州市'},
        {'region_id': '330600', 'region_name': '绍兴', 'region_fullname': '浙江省-绍兴市'},
        {'region_id': '330700', 'region_name': '金华', 'region_fullname': '浙江省-金华市'},
        {'region_id': '330800', 'region_name': '衢州', 'region_fullname': '浙江省-衢州市'},
        {'region_id': '330900', 'region_name': '舟山', 'region_fullname': '浙江省-舟山市'},
        {'region_id': '331000', 'region_name': '台州', 'region_fullname': '浙江省-台州市'},
        {'region_id': '331100', 'region_name': '丽水', 'region_fullname': '浙江省-丽水市'},
        {'region_id': '340100', 'region_name': '合肥', 'region_fullname': '安徽省-合肥市'},
        {'region_id': '340200', 'region_name': '芜湖', 'region_fullname': '安徽省-芜湖市'},
        {'region_id': '340300', 'region_name': '蚌埠', 'region_fullname': '安徽省-蚌埠市'},
        {'region_id': '340400', 'region_name': '淮南', 'region_fullname': '安徽省-淮南市'},
        {'region_id': '340500', 'region_name': '马鞍山', 'region_fullname': '安徽省-马鞍山市'},
        {'region_id': '340600', 'region_name': '淮北', 'region_fullname': '安徽省-淮北市'},
        {'region_id': '340700', 'region_name': '铜陵', 'region_fullname': '安徽省-铜陵市'},
        {'region_id': '340800', 'region_name': '安庆', 'region_fullname': '安徽省-安庆市'},
        {'region_id': '341000', 'region_name': '黄山', 'region_fullname': '安徽省-黄山市'},
        {'region_id': '341100', 'region_name': '滁州', 'region_fullname': '安徽省-滁州市'},
        {'region_id': '341200', 'region_name': '阜阳', 'region_fullname': '安徽省-阜阳市'},
        {'region_id': '341300', 'region_name': '宿州', 'region_fullname': '安徽省-宿州市'},
        {'region_id': '341500', 'region_name': '六安', 'region_fullname': '安徽省-六安市'},
        {'region_id': '341600', 'region_name': '亳州', 'region_fullname': '安徽省-亳州市'},
        {'region_id': '341700', 'region_name': '池州', 'region_fullname': '安徽省-池州市'},
        {'region_id': '341800', 'region_name': '宣城', 'region_fullname': '安徽省-宣城市'},
        {'region_id': '350100', 'region_name': '福州', 'region_fullname': '福建省-福州市'},
        {'region_id': '350200', 'region_name': '厦门', 'region_fullname': '福建省-厦门市'},
        {'region_id': '350300', 'region_name': '莆田', 'region_fullname': '福建省-莆田市'},
        {'region_id': '350400', 'region_name': '三明', 'region_fullname': '福建省-三明市'},
        {'region_id': '350500', 'region_name': '泉州', 'region_fullname': '福建省-泉州市'},
        {'region_id': '350600', 'region_name': '漳州', 'region_fullname': '福建省-漳州市'},
        {'region_id': '350700', 'region_name': '南平', 'region_fullname': '福建省-南平市'},
        {'region_id': '350800', 'region_name': '龙岩', 'region_fullname': '福建省-龙岩市'},
        {'region_id': '350900', 'region_name': '宁德', 'region_fullname': '福建省-宁德市'},
        {'region_id': '360100', 'region_name': '南昌', 'region_fullname': '江西省-南昌市'},
        {'region_id': '360200', 'region_name': '景德镇', 'region_fullname': '江西省-景德镇市'},
        {'region_id': '360300', 'region_name': '萍乡', 'region_fullname': '江西省-萍乡市'},
        {'region_id': '360400', 'region_name': '九江', 'region_fullname': '江西省-九江市'},
        {'region_id': '360500', 'region_name': '新余', 'region_fullname': '江西省-新余市'},
        {'region_id': '360600', 'region_name': '鹰潭', 'region_fullname': '江西省-鹰潭市'},
        {'region_id': '360700', 'region_name': '赣州', 'region_fullname': '江西省-赣州市'},
        {'region_id': '360800', 'region_name': '吉安', 'region_fullname': '江西省-吉安市'},
        {'region_id': '360900', 'region_name': '宜春', 'region_fullname': '江西省-宜春市'},
        {'region_id': '361000', 'region_name': '抚州', 'region_fullname': '江西省-抚州市'},
        {'region_id': '361100', 'region_name': '上饶', 'region_fullname': '江西省-上饶市'},
        {'region_id': '370100', 'region_name': '济南', 'region_fullname': '山东省-济南市'},
        {'region_id': '370200', 'region_name': '青岛', 'region_fullname': '山东省-青岛市'},
        {'region_id': '370300', 'region_name': '淄博', 'region_fullname': '山东省-淄博市'},
        {'region_id': '370400', 'region_name': '枣庄', 'region_fullname': '山东省-枣庄市'},
        {'region_id': '370500', 'region_name': '东营', 'region_fullname': '山东省-东营市'},
        {'region_id': '370600', 'region_name': '烟台', 'region_fullname': '山东省-烟台市'},
        {'region_id': '370700', 'region_name': '潍坊', 'region_fullname': '山东省-潍坊市'},
        {'region_id': '370800', 'region_name': '济宁', 'region_fullname': '山东省-济宁市'},
        {'region_id': '370900', 'region_name': '泰安', 'region_fullname': '山东省-泰安市'},
        {'region_id': '371000', 'region_name': '威海', 'region_fullname': '山东省-威海市'},
        {'region_id': '371100', 'region_name': '日照', 'region_fullname': '山东省-日照市'},
        {'region_id': '371200', 'region_name': '莱芜', 'region_fullname': '山东省-莱芜市'},
        {'region_id': '371300', 'region_name': '临沂', 'region_fullname': '山东省-临沂市'},
        {'region_id': '371400', 'region_name': '德州', 'region_fullname': '山东省-德州市'},
        {'region_id': '371500', 'region_name': '聊城', 'region_fullname': '山东省-聊城市'},
        {'region_id': '371600', 'region_name': '滨州', 'region_fullname': '山东省-滨州市'},
        {'region_id': '371700', 'region_name': '菏泽', 'region_fullname': '山东省-菏泽市'},
        {'region_id': '410100', 'region_name': '郑州', 'region_fullname': '河南省-郑州市'},
        {'region_id': '410200', 'region_name': '开封', 'region_fullname': '河南省-开封市'},
        {'region_id': '410300', 'region_name': '洛阳', 'region_fullname': '河南省-洛阳市'},
        {'region_id': '410400', 'region_name': '平顶山', 'region_fullname': '河南省-平顶山市'},
        {'region_id': '410500', 'region_name': '安阳', 'region_fullname': '河南省-安阳市'},
        {'region_id': '410600', 'region_name': '鹤壁', 'region_fullname': '河南省-鹤壁市'},
        {'region_id': '410700', 'region_name': '新乡', 'region_fullname': '河南省-新乡市'},
        {'region_id': '410800', 'region_name': '焦作', 'region_fullname': '河南省-焦作市'},
        {'region_id': '410900', 'region_name': '濮阳', 'region_fullname': '河南省-濮阳市'},
        {'region_id': '411000', 'region_name': '许昌', 'region_fullname': '河南省-许昌市'},
        {'region_id': '411100', 'region_name': '漯河', 'region_fullname': '河南省-漯河市'},
        {'region_id': '411200', 'region_name': '三门峡', 'region_fullname': '河南省-三门峡市'},
        {'region_id': '411300', 'region_name': '南阳', 'region_fullname': '河南省-南阳市'},
        {'region_id': '411400', 'region_name': '商丘', 'region_fullname': '河南省-商丘市'},
        {'region_id': '411500', 'region_name': '信阳', 'region_fullname': '河南省-信阳市'},
        {'region_id': '411600', 'region_name': '周口', 'region_fullname': '河南省-周口市'},
        {'region_id': '411700', 'region_name': '驻马店', 'region_fullname': '河南省-驻马店市'},
        {'region_id': '419000', 'region_name': '省直辖县级行政区划', 'region_fullname': '河南省-省直辖县级行政区划'},
        {'region_id': '420100', 'region_name': '武汉', 'region_fullname': '湖北省-武汉市'},
        {'region_id': '420200', 'region_name': '黄石', 'region_fullname': '湖北省-黄石市'},
        {'region_id': '420300', 'region_name': '十堰', 'region_fullname': '湖北省-十堰市'},
        {'region_id': '420500', 'region_name': '宜昌', 'region_fullname': '湖北省-宜昌市'},
        {'region_id': '420600', 'region_name': '襄阳', 'region_fullname': '湖北省-襄阳市'},
        {'region_id': '420700', 'region_name': '鄂州', 'region_fullname': '湖北省-鄂州市'},
        {'region_id': '420800', 'region_name': '荆门', 'region_fullname': '湖北省-荆门市'},
        {'region_id': '420900', 'region_name': '孝感', 'region_fullname': '湖北省-孝感市'},
        {'region_id': '421000', 'region_name': '荆州', 'region_fullname': '湖北省-荆州市'},
        {'region_id': '421100', 'region_name': '黄冈', 'region_fullname': '湖北省-黄冈市'},
        {'region_id': '421200', 'region_name': '咸宁', 'region_fullname': '湖北省-咸宁市'},
        {'region_id': '421300', 'region_name': '随州', 'region_fullname': '湖北省-随州市'},
        {'region_id': '422800', 'region_name': '恩施土家族苗族自治州','region_fullname': '湖北省-恩施土家族苗族自治州'},
        {'region_id': '429000', 'region_name': '省直辖县级行政区划', 'region_fullname': '湖北省-省直辖县级行政区划'},
        {'region_id': '430100', 'region_name': '长沙', 'region_fullname': '湖南省-长沙市'},
        {'region_id': '430200', 'region_name': '株洲', 'region_fullname': '湖南省-株洲市'},
        {'region_id': '430300', 'region_name': '湘潭', 'region_fullname': '湖南省-湘潭市'},
        {'region_id': '430400', 'region_name': '衡阳', 'region_fullname': '湖南省-衡阳市'},
        {'region_id': '430500', 'region_name': '邵阳', 'region_fullname': '湖南省-邵阳市'},
        {'region_id': '430600', 'region_name': '岳阳', 'region_fullname': '湖南省-岳阳市'},
        {'region_id': '430700', 'region_name': '常德', 'region_fullname': '湖南省-常德市'},
        {'region_id': '430800', 'region_name': '张家界', 'region_fullname': '湖南省-张家界市'},
        {'region_id': '430900', 'region_name': '益阳', 'region_fullname': '湖南省-益阳市'},
        {'region_id': '431000', 'region_name': '郴州', 'region_fullname': '湖南省-郴州市'},
        {'region_id': '431100', 'region_name': '永州', 'region_fullname': '湖南省-永州市'},
        {'region_id': '431200', 'region_name': '怀化', 'region_fullname': '湖南省-怀化市'},
        {'region_id': '431300', 'region_name': '娄底', 'region_fullname': '湖南省-娄底市'},
        {'region_id': '433100', 'region_name': '湘西土家族苗族自治州','region_fullname': '湖南省-湘西土家族苗族自治州'},
        {'region_id': '440100', 'region_name': '广州', 'region_fullname': '广东省-广州市'},
        {'region_id': '440200', 'region_name': '韶关', 'region_fullname': '广东省-韶关市'},
        {'region_id': '440300', 'region_name': '深圳', 'region_fullname': '广东省-深圳市'},
        {'region_id': '440400', 'region_name': '珠海', 'region_fullname': '广东省-珠海市'},
        {'region_id': '440500', 'region_name': '汕头', 'region_fullname': '广东省-汕头市'},
        {'region_id': '440600', 'region_name': '佛山', 'region_fullname': '广东省-佛山市'},
        {'region_id': '440700', 'region_name': '江门', 'region_fullname': '广东省-江门市'},
        {'region_id': '440800', 'region_name': '湛江', 'region_fullname': '广东省-湛江市'},
        {'region_id': '440900', 'region_name': '茂名', 'region_fullname': '广东省-茂名市'},
        {'region_id': '441200', 'region_name': '肇庆', 'region_fullname': '广东省-肇庆市'},
        {'region_id': '441300', 'region_name': '惠州', 'region_fullname': '广东省-惠州市'},
        {'region_id': '441400', 'region_name': '梅州', 'region_fullname': '广东省-梅州市'},
        {'region_id': '441500', 'region_name': '汕尾', 'region_fullname': '广东省-汕尾市'},
        {'region_id': '441600', 'region_name': '河源', 'region_fullname': '广东省-河源市'},
        {'region_id': '441700', 'region_name': '阳江', 'region_fullname': '广东省-阳江市'},
        {'region_id': '441800', 'region_name': '清远', 'region_fullname': '广东省-清远市'},
        {'region_id': '441900', 'region_name': '东莞', 'region_fullname': '广东省-东莞市'},
        {'region_id': '442000', 'region_name': '中山', 'region_fullname': '广东省-中山市'},
        {'region_id': '445100', 'region_name': '潮州', 'region_fullname': '广东省-潮州市'},
        {'region_id': '445200', 'region_name': '揭阳', 'region_fullname': '广东省-揭阳市'},
        {'region_id': '445300', 'region_name': '云浮', 'region_fullname': '广东省-云浮市'},
        {'region_id': '450100', 'region_name': '南宁', 'region_fullname': '广西壮族自治区-南宁市'},
        {'region_id': '450200', 'region_name': '柳州', 'region_fullname': '广西壮族自治区-柳州市'},
        {'region_id': '450300', 'region_name': '桂林', 'region_fullname': '广西壮族自治区-桂林市'},
        {'region_id': '450400', 'region_name': '梧州', 'region_fullname': '广西壮族自治区-梧州市'},
        {'region_id': '450500', 'region_name': '北海', 'region_fullname': '广西壮族自治区-北海市'},
        {'region_id': '450600', 'region_name': '防城港', 'region_fullname': '广西壮族自治区-防城港市'},
        {'region_id': '450700', 'region_name': '钦州', 'region_fullname': '广西壮族自治区-钦州市'},
        {'region_id': '450800', 'region_name': '贵港', 'region_fullname': '广西壮族自治区-贵港市'},
        {'region_id': '450900', 'region_name': '玉林', 'region_fullname': '广西壮族自治区-玉林市'},
        {'region_id': '451000', 'region_name': '百色', 'region_fullname': '广西壮族自治区-百色市'},
        {'region_id': '451100', 'region_name': '贺州', 'region_fullname': '广西壮族自治区-贺州市'},
        {'region_id': '451200', 'region_name': '河池', 'region_fullname': '广西壮族自治区-河池市'},
        {'region_id': '451300', 'region_name': '来宾', 'region_fullname': '广西壮族自治区-来宾市'},
        {'region_id': '451400', 'region_name': '崇左', 'region_fullname': '广西壮族自治区-崇左市'},
        {'region_id': '460100', 'region_name': '海口', 'region_fullname': '海南省-海口市'},
        {'region_id': '460200', 'region_name': '三亚', 'region_fullname': '海南省-三亚市'},
        {'region_id': '460300', 'region_name': '三沙', 'region_fullname': '海南省-三沙市'},
        {'region_id': '460400', 'region_name': '儋州', 'region_fullname': '海南省-儋州市'},
        {'region_id': '469000', 'region_name': '省直辖县级行政区划', 'region_fullname': '海南省-省直辖县级行政区划'},
        {'region_id': '500100', 'region_name': '重庆', 'region_fullname': '重庆市-重庆市'},
        {'region_id': '500200', 'region_name': '县', 'region_fullname': '重庆市-重庆市'},
        {'region_id': '510100', 'region_name': '成都', 'region_fullname': '四川省-成都市'},
        {'region_id': '510300', 'region_name': '自贡', 'region_fullname': '四川省-自贡市'},
        {'region_id': '510400', 'region_name': '攀枝花', 'region_fullname': '四川省-攀枝花市'},
        {'region_id': '510500', 'region_name': '泸州', 'region_fullname': '四川省-泸州市'},
        {'region_id': '510600', 'region_name': '德阳', 'region_fullname': '四川省-德阳市'},
        {'region_id': '510700', 'region_name': '绵阳', 'region_fullname': '四川省-绵阳市'},
        {'region_id': '510800', 'region_name': '广元', 'region_fullname': '四川省-广元市'},
        {'region_id': '510900', 'region_name': '遂宁', 'region_fullname': '四川省-遂宁市'},
        {'region_id': '511000', 'region_name': '内江', 'region_fullname': '四川省-内江市'},
        {'region_id': '511100', 'region_name': '乐山', 'region_fullname': '四川省-乐山市'},
        {'region_id': '511300', 'region_name': '南充', 'region_fullname': '四川省-南充市'},
        {'region_id': '511400', 'region_name': '眉山', 'region_fullname': '四川省-眉山市'},
        {'region_id': '511500', 'region_name': '宜宾', 'region_fullname': '四川省-宜宾市'},
        {'region_id': '511600', 'region_name': '广安', 'region_fullname': '四川省-广安市'},
        {'region_id': '511700', 'region_name': '达州', 'region_fullname': '四川省-达州市'},
        {'region_id': '511800', 'region_name': '雅安', 'region_fullname': '四川省-雅安市'},
        {'region_id': '511900', 'region_name': '巴中', 'region_fullname': '四川省-巴中市'},
        {'region_id': '512000', 'region_name': '资阳', 'region_fullname': '四川省-资阳市'},
        {'region_id': '513200', 'region_name': '阿坝藏族羌族自治州', 'region_fullname': '四川省-阿坝藏族羌族自治州'},
        {'region_id': '513300', 'region_name': '甘孜藏族自治州', 'region_fullname': '四川省-甘孜藏族自治州'},
        {'region_id': '513400', 'region_name': '凉山彝族自治州', 'region_fullname': '四川省-凉山彝族自治州'},
        {'region_id': '520100', 'region_name': '贵阳', 'region_fullname': '贵州省-贵阳市'},
        {'region_id': '520200', 'region_name': '六盘水', 'region_fullname': '贵州省-六盘水市'},
        {'region_id': '520300', 'region_name': '遵义', 'region_fullname': '贵州省-遵义市'},
        {'region_id': '520400', 'region_name': '安顺', 'region_fullname': '贵州省-安顺市'},
        {'region_id': '520500', 'region_name': '毕节', 'region_fullname': '贵州省-毕节市'},
        {'region_id': '520600', 'region_name': '铜仁', 'region_fullname': '贵州省-铜仁市'},
        {'region_id': '522300', 'region_name': '黔西南布依族苗族自治州','region_fullname': '贵州省-黔西南布依族苗族自治州'},
        {'region_id': '522600', 'region_name': '黔东南苗族侗族自治州','region_fullname': '贵州省-黔东南苗族侗族自治州'},
        {'region_id': '522700', 'region_name': '黔南布依族苗族自治州','region_fullname': '贵州省-黔南布依族苗族自治州'},
        {'region_id': '530100', 'region_name': '昆明', 'region_fullname': '云南省-昆明市'},
        {'region_id': '530300', 'region_name': '曲靖', 'region_fullname': '云南省-曲靖市'},
        {'region_id': '530400', 'region_name': '玉溪', 'region_fullname': '云南省-玉溪市'},
        {'region_id': '530500', 'region_name': '保山', 'region_fullname': '云南省-保山市'},
        {'region_id': '530600', 'region_name': '昭通', 'region_fullname': '云南省-昭通市'},
        {'region_id': '530700', 'region_name': '丽江', 'region_fullname': '云南省-丽江市'},
        {'region_id': '530800', 'region_name': '普洱', 'region_fullname': '云南省-普洱市'},
        {'region_id': '530900', 'region_name': '临沧', 'region_fullname': '云南省-临沧市'},
        {'region_id': '532300', 'region_name': '楚雄彝族自治州', 'region_fullname': '云南省-楚雄彝族自治州'},
        {'region_id': '532500', 'region_name': '红河哈尼族彝族自治州','region_fullname': '云南省-红河哈尼族彝族自治州'},
        {'region_id': '532600', 'region_name': '文山壮族苗族自治州', 'region_fullname': '云南省-文山壮族苗族自治州'},
        {'region_id': '532800', 'region_name': '西双版纳傣族自治州', 'region_fullname': '云南省-西双版纳傣族自治州'},
        {'region_id': '532900', 'region_name': '大理白族自治州', 'region_fullname': '云南省-大理白族自治州'},
        {'region_id': '533100', 'region_name': '德宏傣族景颇族自治州','region_fullname': '云南省-德宏傣族景颇族自治州'},
        {'region_id': '533300', 'region_name': '怒江傈僳族自治州', 'region_fullname': '云南省-怒江傈僳族自治州'},
        {'region_id': '533400', 'region_name': '迪庆藏族自治州', 'region_fullname': '云南省-迪庆藏族自治州'},
        {'region_id': '540100', 'region_name': '拉萨', 'region_fullname': '西藏自治区-拉萨市'},
        {'region_id': '540200', 'region_name': '日喀则', 'region_fullname': '西藏-日喀则市'},
        {'region_id': '540300', 'region_name': '昌都', 'region_fullname': '西藏-昌都市'},
        {'region_id': '540400', 'region_name': '林芝', 'region_fullname': '西藏-林芝市'},
        {'region_id': '540500', 'region_name': '山南', 'region_fullname': '西藏-山南市'},
        {'region_id': '542400', 'region_name': '那曲地区', 'region_fullname': '西藏自治区-那曲地区'},
        {'region_id': '542500', 'region_name': '阿里地区', 'region_fullname': '西藏自治区-阿里地区'},
        {'region_id': '610100', 'region_name': '西安', 'region_fullname': '陕西省-西安市'},
        {'region_id': '610200', 'region_name': '铜川', 'region_fullname': '陕西省-铜川市'},
        {'region_id': '610300', 'region_name': '宝鸡', 'region_fullname': '陕西省-宝鸡市'},
        {'region_id': '610400', 'region_name': '咸阳', 'region_fullname': '陕西省-咸阳市'},
        {'region_id': '610500', 'region_name': '渭南', 'region_fullname': '陕西省-渭南市'},
        {'region_id': '610600', 'region_name': '延安', 'region_fullname': '陕西省-延安市'},
        {'region_id': '610700', 'region_name': '汉中', 'region_fullname': '陕西省-汉中市'},
        {'region_id': '610800', 'region_name': '榆林', 'region_fullname': '陕西省-榆林市'},
        {'region_id': '610900', 'region_name': '安康', 'region_fullname': '陕西省-安康市'},
        {'region_id': '611000', 'region_name': '商洛', 'region_fullname': '陕西省-商洛市'},
        {'region_id': '620100', 'region_name': '兰州', 'region_fullname': '甘肃省-兰州市'},
        {'region_id': '620200', 'region_name': '嘉峪关', 'region_fullname': '甘肃省-嘉峪关市'},
        {'region_id': '620300', 'region_name': '金昌', 'region_fullname': '甘肃省-金昌市'},
        {'region_id': '620400', 'region_name': '白银', 'region_fullname': '甘肃省-白银市'},
        {'region_id': '620500', 'region_name': '天水', 'region_fullname': '甘肃省-天水市'},
        {'region_id': '620600', 'region_name': '武威', 'region_fullname': '甘肃省-武威市'},
        {'region_id': '620700', 'region_name': '张掖', 'region_fullname': '甘肃省-张掖市'},
        {'region_id': '620800', 'region_name': '平凉', 'region_fullname': '甘肃省-平凉市'},
        {'region_id': '620900', 'region_name': '酒泉', 'region_fullname': '甘肃省-酒泉市'},
        {'region_id': '621000', 'region_name': '庆阳', 'region_fullname': '甘肃省-庆阳市'},
        {'region_id': '621100', 'region_name': '定西', 'region_fullname': '甘肃省-定西市'},
        {'region_id': '621200', 'region_name': '陇南', 'region_fullname': '甘肃省-陇南市'},
        {'region_id': '622900', 'region_name': '临夏回族自治州', 'region_fullname': '甘肃省-临夏回族自治州'},
        {'region_id': '623000', 'region_name': '甘南藏族自治州', 'region_fullname': '甘肃省-甘南藏族自治州'},
        {'region_id': '630100', 'region_name': '西宁', 'region_fullname': '青海省-西宁市'},
        {'region_id': '630200', 'region_name': '海东', 'region_fullname': '青海省-海东市'},
        {'region_id': '632200', 'region_name': '海北藏族自治州', 'region_fullname': '青海省-海北藏族自治州'},
        {'region_id': '632300', 'region_name': '黄南藏族自治州', 'region_fullname': '青海省-黄南藏族自治州'},
        {'region_id': '632500', 'region_name': '海南藏族自治州', 'region_fullname': '青海省-海南藏族自治州'},
        {'region_id': '632600', 'region_name': '果洛藏族自治州', 'region_fullname': '青海省-果洛藏族自治州'},
        {'region_id': '632700', 'region_name': '玉树藏族自治州', 'region_fullname': '青海省-玉树藏族自治州'},
        {'region_id': '632800', 'region_name': '海西蒙古族藏族自治州','region_fullname': '青海省-海西蒙古族藏族自治州'},
        {'region_id': '640100', 'region_name': '银川', 'region_fullname': '宁夏回族自治区-银川市'},
        {'region_id': '640200', 'region_name': '石嘴山', 'region_fullname': '宁夏回族自治区-石嘴山市'},
        {'region_id': '640300', 'region_name': '吴忠', 'region_fullname': '宁夏回族自治区-吴忠市'},
        {'region_id': '640400', 'region_name': '固原', 'region_fullname': '宁夏回族自治区-固原市'},
        {'region_id': '640500', 'region_name': '中卫', 'region_fullname': '宁夏回族自治区-中卫市'},
        {'region_id': '650100', 'region_name': '乌鲁木齐', 'region_fullname': '新疆维吾尔自治区-乌鲁木齐市'},
        {'region_id': '650200', 'region_name': '克拉玛依', 'region_fullname': '新疆维吾尔自治区-克拉玛依市'},
        {'region_id': '650400', 'region_name': '吐鲁番', 'region_fullname': '新疆-吐鲁番市'},
        {'region_id': '650500', 'region_name': '哈密', 'region_fullname': '新疆-哈密市'},
        {'region_id': '652300', 'region_name': '昌吉回族自治州', 'region_fullname': '新疆维吾尔自治区-昌吉回族自治州'},
        {'region_id': '652700', 'region_name': '博尔塔拉蒙古自治州','region_fullname': '新疆维吾尔自治区-博尔塔拉蒙古自治州'},
        {'region_id': '652800', 'region_name': '巴音郭楞蒙古自治州','region_fullname': '新疆维吾尔自治区-巴音郭楞蒙古自治州'},
        {'region_id': '652900', 'region_name': '阿克苏地区', 'region_fullname': '新疆维吾尔自治区-阿克苏地区'},
        {'region_id': '653000', 'region_name': '克孜勒苏柯尔克孜自治州','region_fullname': '新疆维吾尔自治区-克孜勒苏柯尔克孜自治州'},
        {'region_id': '653100', 'region_name': '喀什地区', 'region_fullname': '新疆维吾尔自治区-喀什地区'},
        {'region_id': '653200', 'region_name': '和田地区', 'region_fullname': '新疆维吾尔自治区-和田地区'},
        {'region_id': '654000', 'region_name': '伊犁哈萨克自治州','region_fullname': '新疆维吾尔自治区-伊犁哈萨克自治州'},
        {'region_id': '654200', 'region_name': '塔城地区', 'region_fullname': '新疆维吾尔自治区-塔城地区'},
        {'region_id': '654300', 'region_name': '阿勒泰地区', 'region_fullname': '新疆维吾尔自治区-阿勒泰地区'},
        {'region_id': '659000', 'region_name': '自治区直辖县级行政区划','region_fullname': '新疆维吾尔自治区-自治区直辖县级行政区划'},
        {'region_id': '650100', 'region_name': '乌鲁木齐', 'region_fullname': '新疆维吾尔自治区-乌鲁木齐市'},
        {'region_id': '650200', 'region_name': '克拉玛依', 'region_fullname': '新疆维吾尔自治区-克拉玛依市'},
        {'region_id': '650400', 'region_name': '吐鲁番', 'region_fullname': '新疆-吐鲁番市'},
        {'region_id': '650500', 'region_name': '哈密', 'region_fullname': '新疆-哈密市'},
        {'region_id': '652300', 'region_name': '昌吉回族自治州', 'region_fullname': '新疆维吾尔自治区-昌吉回族自治州'},
        {'region_id': '652700', 'region_name': '博尔塔拉蒙古自治州','region_fullname': '新疆维吾尔自治区-博尔塔拉蒙古自治州'},
        {'region_id': '652800', 'region_name': '巴音郭楞蒙古自治州','region_fullname': '新疆维吾尔自治区-巴音郭楞蒙古自治州'},
        {'region_id': '652900', 'region_name': '阿克苏地区', 'region_fullname': '新疆维吾尔自治区-阿克苏地区'},
        {'region_id': '653000', 'region_name': '克孜勒苏柯尔克孜自治州','region_fullname': '新疆维吾尔自治区-克孜勒苏柯尔克孜自治州'},
        {'region_id': '653100', 'region_name': '喀什地区', 'region_fullname': '新疆维吾尔自治区-喀什地区'},
        {'region_id': '653200', 'region_name': '和田地区', 'region_fullname': '新疆维吾尔自治区-和田地区'},
        {'region_id': '654000', 'region_name': '伊犁哈萨克自治州','region_fullname': '新疆维吾尔自治区-伊犁哈萨克自治州'},
        {'region_id': '654200', 'region_name': '塔城地区', 'region_fullname': '新疆维吾尔自治区-塔城地区'},
        {'region_id': '654300', 'region_name': '阿勒泰地区', 'region_fullname': '新疆维吾尔自治区-阿勒泰地区'},
        {'region_id': '659000', 'region_name': '自治区直辖县级行政区划','region_fullname': '新疆维吾尔自治区-自治区直辖县级行政区划'}
              ]
    for lis in region:
        if lis.get('region_id')==regid:
            cityname=lis.get('region_fullname')
            print(cityname)
            return cityname

# 获取zzlb的号码
def searchzzlb(zzmc):
    with open('spider/yunqi_addon17_zzlb.json', 'r', encoding='utf8') as r:
        lines = eval(r.read())
        # print(lines)
        for lis in lines.get('RECORDS'):
            # print(lis['pron'],type(lis['pron']))
            if zzmc in lis['pron']:
                print(lis['pron'], lis['parent_id'])
                return lis


# 查看人员证件类型id
def search_typeid(typename):
    with open('spider/yunqi_arctype.json', 'r', encoding='utf8') as r:
        lines = eval(r.read())
        # print(lines)
    for lis in lines.get('RECORDS'):
        for name in typename:
            if name in lis.get('typename'):
                print(lis['typename'], lis['id'])
                return lis['id']


def search_person_certid(personcert):
    with open('spider/yunqi_persontype.json', 'r', encoding='utf8') as r:
        lines = eval(r.read())
    for lis in lines.get('RECORDS'):
        # print(lis['pron'],type(lis['pron']))
        if personcert in lis['name']:
            print(lis['id'], lis['name'])
            return lis['id']



# 查找typeid
def findtypeid(cert):
    typedata = [
        {'id': 98, 'typename': '环境工程监理'},
        {'id': 99, 'typename': '勘察企业'},
        {'id': 100, 'typename': '设计企业'},
        {'id': 101, 'typename': '建筑业企业'},
        {'id': 102, 'typename': '监理企业'},
        {'id': 103, 'typename': '招标代理机构'},
        {'id': 104, 'typename': '设计与施工一体化企业'},
        {'id': 105, 'typename': '造价咨询企业'},
        {'id': 106, 'typename': '其他类型'}]
    for tyid in typedata:
        if cert in tyid['typename']:
            # print(type(tyid), tyid)
            return tyid['id']

def pooldb_conn():
    try:
        pooldb = db.connection()
        return pooldb
    except Exception as e:
        traceback.format_exc()
        pooldb_conn()

def close_mysql(cur,pooldb):
    cur.close()
    pooldb.close()

def excute_mysql(sql, params=None, commit=False):

        pooldb = pooldb_conn()
        cur = pooldb.cursor()
        try:
            cur.execute(sql,params)
            if commit:
                pooldb.commit()
            data = cur.fetchone()
            return data
        except Exception as e:
            print(f"Error: {e}\n {sql}")
            print(traceback.format_exc())
        finally:
            close_mysql(cur,pooldb)



def search_yunqi_cai():

    sql = "select name from yunqi_cai;"
    data= excute_mysql(sql)
    return data


def search_cai(name):
    sql = f"select * from yunqi_cai where (name = '{name}');"
    data = excute_mysql(sql)
    return data

def insert_cai(name, times):
    sql = f"insert into yunqi_cai(name, time) values ('{name}', '{times}');"
    excute_mysql(sql,  commit=True)


def updata_cai(name, times):
    sql = f"update yunqi_cai set time='{times}' where name='{name}';"
    excute_mysql(sql, commit=True)

def del_cname(cname):
    sql = "delete from yunqi_cai where name=%s;"
    excute_mysql(sql, (cname),commit=True)

#查看四库all id
def serch_siku():
    pooldb = db.connection()
    cur = pooldb.cursor()
    sql = f"select cname,skid from siku_id ;"
    cur.execute(sql)
    data = cur.fetchall()
    cur.close()
    pooldb.close()
    return data


def serch_siku_id(cname):
    sql = f"select cname,skid from siku_id where (cname = '{cname}');"
    data = excute_mysql(sql)
    return data

def inster_siku_id(cname,skid):
    sql = "insert into siku_id(cname,skid) values (%s,%s);"
    excute_mysql(sql, (cname,skid),True)


# 增加数据
def insertdata(typeid, qymc, tyshxydm, qyfr, zclx, nativeplace, xxdz,zzlb, xiangmu, zizhi, rynum, m_id):
    sql = "insert into " \
          "yunqi_addon17(typeid,qymc,tyshxydm,qyfr,zclx,nativeplace,xxdz,zzlb,xiangmu,zizhi,rynum,m_id) " \
          "values " \
          "(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"

    excute_mysql(sql, (typeid, qymc, tyshxydm, qyfr, zclx, nativeplace, xxdz, zzlb,xiangmu, zizhi, rynum, m_id),True)

def upadtebase(zzlb,aid):
    sql = f"update yunqi_addon17 set zzlb='{zzlb}' where aid='{aid}';"
    excute_mysql(sql, commit=True)


# 查询企业信息
def searchdb(qymc):
    sql = "select aid,tyshxydm,xiangmu,zizhi,rynum from yunqi_addon17 where (qymc='{}')".format(qymc)
    data = excute_mysql(sql)
    return data



def insertzzlx(kid, zzlb, zzzsh, zzmc, fzrq, zsyxq, fzjg):
    sql = "insert into " \
          "yunqi_addon17_zzlx(kid, zzlb, zzzsh, zzmc, fzrq, zsyxq, fzjg) " \
          "values " \
          "(%s,%s,%s,%s,%s,%s,%s);"
    excute_mysql(sql, (kid, zzlb, zzzsh, zzmc, fzrq, zsyxq, fzjg),True)

def delete_zzlx(kid):
    sql = f"delete from yunqi_addon17_zzlx where (kid='{kid}')"
    excute_mysql(sql,commit=True)


def searchzmc(kid,zzmc):
    sql = f"select * from yunqi_addon17_zzlx where (kid='{kid}'and zzmc='{zzmc}')"
    data=excute_mysql(sql)
    return data

# 人员表
def inertaddon18(fid, typeid, name, sex, idcard, cardname, leixing, companyid, zsbh, zyyzh, yxq):
    sql = "insert into " \
          "yunqi_addon18(fid, typeid, name, sex, idcard, cardname, leixing, companyid, zsbh, zyyzh, yxq) " \
          "values " \
          "(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
    excute_mysql(sql, (fid, typeid, name, sex, idcard, cardname, leixing, companyid, zsbh, zyyzh, yxq),True)


def searchperson(zyyzh,name):
    sql = f"select aid , leixing from yunqi_addon18 where (zyyzh='{zyyzh}' and name='{name}')"
    data=excute_mysql(sql)
    return data

def update_person_cert(aid,leixing):
    sql = f"update yunqi_addon18 set leixing='{leixing}' where aid='{aid}';"
    excute_mysql(sql, commit=True)


def insert_qr(fid, aid):
    sql = "insert into yunqi_qr(aid, rid) values (%s,%s);"
    excute_mysql(sql, (fid, aid),True)


def insert_qx(aid, xid):
    sql = "insert into yunqi_qx(aid, xid) values (%s,%s);"

    excute_mysql(sql, (aid, xid),True)
def searchqr(aid):
    sql = f"select aid from yunqi_qr where (rid='{aid}')"
    data = excute_mysql(sql)
    return data


def searchqx(xid):
    sql = f"select aid from yunqi_qx where (xid='{xid}')"
    data = excute_mysql(sql)
    return data

def search_aid(pnumber):
    sql = f"select aid from yunqi_addoninfos where (pnumber='{pnumber}')"
    data=excute_mysql(sql)
    return data


# def searchpnumber(pnumber,title):
#     sql = f"-- select aid from yunqi_addoninfos where (pnumber='{pnumber}'and title='{title}')"
#     data = excute_mysql(sql)
#     return data



# 关联项目
def insertaddoninfos(fid, typeid, mid, title, senddate, nativeplace,linkman, pnumber, ztzmoney, lxwh, sjxmnumber, zzjgdm, jsxz,
                     tarea, lxjb):

    sql = "insert into " \
          "yunqi_addoninfos(fid,typeid,mid,title,senddate,nativeplace,linkman,pnumber,ztzmoney,lxwh,sjxmnumber,zzjgdm,jsxz,tarea,tzsbh,lxjb)" \
          " values " \
          "(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    excute_mysql(sql, (fid, typeid, mid, title, senddate,nativeplace, linkman, pnumber, ztzmoney, lxwh, sjxmnumber, zzjgdm, jsxz,tarea, "''", lxjb),True)

def updataaddoninfos(pnumber,nativeplace):
    sql = f"update yunqi_addoninfos set nativeplace='{nativeplace}' where pnumber='{pnumber}';"
    excute_mysql(sql, commit=True)

def search_cydw(kid, qymc):
    sql = f"select * from yunqi_addoninfos_cydw where (kid='{kid}' and qymc='{qymc}')"
    data = excute_mysql(sql)
    return data

# 插入项目参与单位与负责人
def insert_cydw(title, kid, qid, qymc, tyshxydm, name, idnum, role):
    sql = "insert into yunqi_addoninfos_cydw(title,kid, qid, qymc, tyshxydm, name, idnum,role) " \
          "values (%s,%s,%s,%s,%s,%s,%s,%s);"
    excute_mysql(sql, (title, kid, qid, qymc, tyshxydm, name, idnum, role),True)

def searchht(dj_number):
    sql = f"select * from yunqi_addoninfos_ht where (dj_number = '{dj_number}')"
    data = excute_mysql(sql)
    return data

def insert_ht(kid, ba_number, ht_type, dj_number, money, fb_qymc, cb_qymc, cb_id, type, build, fb_xydm, cb_xydm,
              lh_qymc,lh_xydm, register_time, signing_time, source):
    sql = "insert into yunqi_addoninfos_ht(kid,ba_number, ht_type, dj_number, money, fb_qymc, cb_qymc, cb_id, type, build, fb_xydm, cb_xydm, lh_qymc, lh_xydm, register_time, signing_time, source) " \
          "values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
    excute_mysql(sql, (kid, ba_number, ht_type, dj_number, money, fb_qymc, cb_qymc, cb_id, type, build, fb_xydm, cb_xydm, lh_qymc,
    lh_xydm, register_time, signing_time, source),True)





def searchjgys(babh, sjbabh):
    sql = f"select * from yunqi_addoninfos_jgys where (babh = '{babh}' and sjbabh='{sjbabh}')"
    data = excute_mysql(sql)
    return data


def insert_jgys(kid, babh, sjbabh, sjzj, sjmj, sjkgrq, jgys, xqurl):
    sql = "insert into yunqi_addoninfos_jgys(kid, babh, sjbabh, sjzj, sjmj, sjkgrq, jgys, xqurl) " \
          "values (%s,%s,%s,%s,%s,%s,%s,%s);"
    excute_mysql(sql, (kid, babh, sjbabh, sjzj, sjmj, sjkgrq, jgys, xqurl),True)


def searchsgxk(sgbh, sjbh):
    sql = f"select * from yunqi_addoninfos_sgxk where (sgbh = '{sgbh}' and sjbh='{sjbh}')"
    data = excute_mysql(sql)
    return data


def insert_sgxk(kid, pid, sgbh, sjbh, htje, mj, fzrq, xqurl):
    sql = "insert into yunqi_addoninfos_sgxk(kid, pid, sgbh, sjbh, htje, mj, fzrq, xqurl) " \
          "values (%s,%s,%s,%s,%s,%s,%s,%s);"
    excute_mysql(sql, (kid, pid, sgbh, sjbh, htje, mj, fzrq, xqurl),True)


def search_dt(number):
    sql = f"select * from yunqi_addoninfos_dt where (number = '{number}')"
    data = excute_mysql(sql)
    return data

def insert_dt(kid, title, number, cost, area, height, structure, grade, up_area, dw_area,
              layer, down_layer, long, wide, protect, scale, other, ztb_number, sg_number, xk_number,
              zl_number, aq_number, shock, green, green_type, shocks, limit, set, rebar, steel):
    sql = "insert into yunqi_addoninfos_dt (kid, title, number, cost, area, height, structure, grade, up_area, dw_area,layer, down_layer, `long`, wide,protect, scale, other, ` ztb_number`, sg_number, xk_number,zl_number, aq_number, shock, green, green_type, shocks, `limit`, `set`, rebar, steel)" \
          "values " \
          f"(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
    excute_mysql(sql, (kid, title, number, cost, area, height, structure, grade, up_area, dw_area,
                      layer, down_layer, long, wide, protect, scale, other, ztb_number, sg_number, xk_number,
                      zl_number, aq_number, shock, green, green_type, shocks, limit, set, rebar, steel),True)


def search_sgtsc(sgtschgbh):
    sql = f"select * from yunqi_addoninfos_sgtsc where (sgtschgbh = '{sgtschgbh}')"
    data = excute_mysql(sql)
    return data


def insert_sgtsc(kid, pid, sgtschgbh, sjbh, kcdw, kcdw_sf, kcdw_dm, sjdw, sjdw_sf, sjdw_dm, sgdw, sgdw_sf, sgdw_dm,
                 scjg, scjg_dm, guimo, wcrq, xqurl, endtime, jsgm, one, startime, lh, xftime, xfhg, xfjg, rftime,
                 rfhj, rfjg, lerver):

    sql = "insert into yunqi_addoninfos_sgtsc (kid, pid, sgtschgbh, sjbh, kcdw, kcdw_sf, kcdw_dm, sjdw, sjdw_sf, sjdw_dm, sgdw, sgdw_sf, sgdw_dm, scjg, scjg_dm, guimo, wcrq, xqurl, endtime, jsgm, one, startime, lh, xftime, xfhg, xfjg, rftime, rfhj, rfjg, lerver)" \
          "values " \
          f"(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"

    excute_mysql(sql,
                (kid, pid, sgtschgbh, sjbh, kcdw, kcdw_sf, kcdw_dm, sjdw, sjdw_sf, sjdw_dm, sgdw, sgdw_sf, sgdw_dm,
                 scjg, scjg_dm, guimo, wcrq, xqurl, endtime, jsgm, one, startime, lh, xftime, xfhg, xfjg, rftime,
                 rfhj, rfjg, lerver),True)



def search_ztb(tzsbh):
    sql = f"select * from yunqi_addoninfos_ztb where (tzsbh = '{tzsbh}')"
    data = excute_mysql(sql)
    return data


def insert_ztb(kid, pid, zblx, zbfs, zbdw, zbrq, zbje, tzsbh, sjbh, xqurl):

    sql = "insert into yunqi_addoninfos_ztb(kid, pid, zblx, zbfs, zbdw, zbrq, zbje, tzsbh, sjbh, xqurl) " \
          "values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
    excute_mysql(sql, (kid, pid, zblx, zbfs, zbdw, zbrq, zbje, tzsbh, sjbh, xqurl),True)


def search_sgxcaqy(idnum, tyshxydm):

    sql = f"select * from yunqi_addoninfos_sgxcaqy where (idnum = '{idnum}'and tyshxydm ='{tyshxydm}')"
    data = excute_mysql(sql)
    return data


def insert_sgxcaqy(title, kid, pid, qymc, tyshxydm, name, idnum, aqxkzbh, sgxkzbh, usertype):

    sql = "insert into yunqi_addoninfos_sgxcaqy(title,kid, pid, qymc, tyshxydm, name, idnum, aqxkzbh, sgxkzbh,usertype) " \
          "values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
    excute_mysql(sql, (title, kid, pid, qymc, tyshxydm, name, idnum, aqxkzbh, sgxkzbh, usertype),True)


def search_sgxcglr(name, title):

    sql = f"select * from yunqi_addoninfos_sgxcglr where (name = '{name}'and title='{title}');"
    data = excute_mysql(sql)
    return data


def insert_sgxcglr(title, kid, pid, tyshxydm, name, idnum, ssqy, sgxkzbh, gwmc, zsbh, zsyxq, fzdw):
    

    sql = "insert into yunqi_addoninfos_sgxcglr(title, kid, pid, tyshxydm, name, idnum, ssqy, sgxkzbh, gwmc, zsbh, zsyxq, fzdw) " \
          "values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
    excute_mysql(sql, (title, kid, pid, tyshxydm, name, idnum, ssqy, sgxkzbh, gwmc, zsbh, zsyxq, fzdw),True)


def search_sgxctzzyr(name):

    sql = f"select * from yunqi_addoninfos_sgxctzzyr where (name = '{name}');"
    data = excute_mysql(sql)
    return data

def insert_sgxctzzyr(title, kid, pid, name, idnum, ssqy, tyshxydm, sgxkzbh, gz, zsbh, zsyxq, fzdw):

    sql = "insert into yunqi_addoninfos_sgxctzzyr(title, kid, pid, name, idnum, ssqy, tyshxydm, sgxkzbh, gz, zsbh, zsyxq, fzdw) " \
          "values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
    excute_mysql(sql, (title, kid, pid, name, idnum, ssqy, tyshxydm, sgxkzbh, gz, zsbh, zsyxq, fzdw),True)


def search_sgxcjxsb(sbbabh):

    sql = f"select * from yunqi_addoninfos_sgxcjxsb where (sbbabh = '{sbbabh}');"
    data = excute_mysql(sql)
    return data


def insert_sgxcjxsb(title, kid, pid, jxsbmc, cqdw, jxmodel, sgxkzbh, sydw, sybw, acdw, sbbabh, jhjcsj, jhccsj):

    sql = "insert into yunqi_addoninfos_sgxcjxsb(title, kid, pid, jxsbmc, cqdw, jxmodel, sgxkzbh, sydw, sybw, acdw, sbbabh, jhjcsj, jhccsj) " \
          "values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
    excute_mysql(sql, (title, kid, pid, jxsbmc, cqdw, jxmodel, sgxkzbh, sydw, sybw, acdw, sbbabh, jhjcsj, jhccsj),True)


def search_zyry(IDCARD,CENSORNUM,SPECIALTYTYP):

    sql = f"select * from yunqi_addoninfos_zyry where (IDCARD = '{IDCARD}'and CENSORNUM= '{CENSORNUM}'and SPECIALTYTYP='{SPECIALTYTYP}');"
    data = excute_mysql(sql)
    return data


def insert_zyry(kid, CORPNAME, IDCARD, SPECIALTYTYP, TBWORKDUTYDIC, SPE, TECHTITLELEVEL, CORPID, PRJNUM, CORPCODE,
                USERID, USERNAME, CENSORNUM, IDCARDTYPENUM):

    sql = "insert into yunqi_addoninfos_zyry(kid, CORPNAME, IDCARD, SPECIALTYTYP, TBWORKDUTYDIC, SPE, TECHTITLELEVEL, CORPID, PRJNUM, CORPCODE, USERID, USERNAME, CENSORNUM, IDCARDTYPENUM) " \
          "values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
    excute_mysql(sql, (kid, CORPNAME, IDCARD, SPECIALTYTYP, TBWORKDUTYDIC, SPE, TECHTITLELEVEL, CORPID, PRJNUM, CORPCODE,
                USERID, USERNAME, CENSORNUM, IDCARDTYPENUM),True)


# def updatetpeple(typeid, qymc, tyshxydm, qyfr, zclx, nativeplace, xxdz, xiangmu, zizhi, rynum, m_id):
# pooldb_test.py=db.connection()
#     cur = pooldb_test.py.cursor()
# sql = "insert into " \
#       "yunqi_addoninfos_cydw(kid,qid,qymc,tyshxydm,name,idnum) " \
#       "values " \
#       "(%s,%s,%s,%s,%s,%s);"
# cur.execute(sql, (typeid, qymc, tyshxydm, qyfr, zclx, nativeplace, xxdz, xiangmu, zizhi, rynum, m_id))





# 插入 yunqi_cai
def insert_yunqi_cai(name, times):
    if search_cai(name):
        print(f'cai {name} is exist')
        updata_cai(name, times)
        print(f'updata {name} time')
    else:
        print(name, times)
        print(f'cai {name} 入库完成')
        insert_cai(name, times)

#存入四库id
def insert_skid(cname,skid):
    if serch_siku_id(cname):
        print(f'{cname}siku_id is exist')
    else:
        inster_siku_id(cname, skid)
        print(f'{cname}siku_id 入库完成')


# 插入yunqi_addon17
def insert_base(data):
    print(data)
    base = data.get('base')
    message = data.get('messagecount')
    certs = data.get('cert')
    xxdz = base['address']
    cityid = base.get('regionFullname')
    if cityid:
        cityid = cityid.replace('-省直辖县级行政区划', '')
        if '新疆生产建设兵团'in cityid:
            cityid='新疆维吾尔自治区'
    else:
        cityid = re.findall(r'(\w+自治区|\w+省|\w+市|\w+县)', xxdz)
        if cityid:
            cityid=cityid[0]
        else:
            cityid=0
    print(cityid)
    nativeplace = findcityid(cityid)
    certType = certs[0]['certType']
    if '资质' in certType:
        typename = re.findall(r'([\S]+)资质', certType)
        tyid = findtypeid(typename[0])
    # time.sleep(2222)
    typeid = tyid
    tyshxydm = base['corpCode']
    qymc = base['corpName']
    qyfr = base.get('legalMan', '')
    zclx = base.get('qyRegType','')
    xiangmu = message.get('projectCount')
    zizhi = message.get('certCount')
    rynum = message.get('regPersonCount')
    zzl=searchzzlb(certs[0].get('certName'))
    if zzl:
        zzlb=zzl.get('id')
    else:
        zzlb=0
    print(zzlb)
    m_id = 10036
    py = ''
    for pin in lazy_pinyin(qymc):
        py += pin
    print("addon17:", typeid, py, qymc, tyshxydm, qyfr, zclx, nativeplace, xxdz,zzlb, xiangmu, zizhi, rynum, m_id)
    id = searchdb(qymc)
    if id:
        print(f'企业基本信息yunqi_addon17 {qymc} exist!')
        upadtebase(zzlb,id[0])
    else:
        insertdata(typeid, qymc, tyshxydm, qyfr, zclx, nativeplace, xxdz, zzlb, xiangmu, zizhi, rynum, m_id)
        id = searchdb(qymc)
        print(f'企业基本信息addon17{qymc}入库完成')


    # 插入资质表 addon17_zzlx
    kid=id[0]
    print(kid)
    for cert in certs:
        print(cert)
        zzmc = cert.get('certName')
        zzlbid = searchzzlb(zzmc)
        if zzlbid:
            zzlb =zzlbid.get('parent_id')
            print('zzzzzzzzzzzzzzzzzzzzzzzzz:',zzlb)
        else:
            zzlb=0
        zzzsh =cert.get('certId')
        fzrq = Transformation(cert.get('organDate','0'))
        zsyxq = Transformation(cert.get('endDate','0'))
        fzjg = cert['organName']
        print('zzlx:', kid, zzlb, zzzsh, zzmc, fzrq, zsyxq, fzjg)
        if searchzmc(kid,zzmc):
            print(f'资质addon17_zzlx {qymc} exist!')
        else:
            insertzzlx(kid, zzlb, zzzsh, zzmc, fzrq, zsyxq, fzjg)
            print(f"资质addon17_zzlx {zzmc} 入库完成")

    # return {'typeid': typeid, 'qymc': qymc, 'kid': kid}


# addon18插入人员
def insert_addon18(reg,cname):
    print(cname)
    fid = searchdb(cname)[0]
    if fid:
        if reg.get('zhtype').split(',')[0] == '土建':
            typeid = '94'
        else:
            typeid = search_typeid(reg.get('zhtype').split(','))
            if not typeid:
                typeid = '0'
        zyyzh = reg.get('zyyz')
        zsbh = reg.get('zsbh')
        name = reg.get('name')
        sex = reg.get('sex')
        idcard = 1
        if not reg.get('sfz'):
            idcard = 0
        cardname = reg.get('sfz')
        leixing =search_person_certid(reg.get('zsdj'))
        if leixing ==None:
            with open('./person_cert_log.txt','a',encoding='utf8')as w:
                w.write(str(reg.get('zsdj'))+'\n')
            w.close()
        companyid = reg.get('gsname')
        yxq = reg.get('reg_end')
        print('addon18:', fid, typeid, name, sex, idcard, cardname, leixing, companyid, zsbh, zyyzh, yxq)
        personid=searchperson(zyyzh,name)
        if personid:
            if personid[1]:
                print(personid[1])
                print(f'人员inertaddon18 {name} exist')
            else:
                update_person_cert(personid[0],leixing)
                print(f'人员update_cert {name} 入库完成')
        else:
            inertaddon18(fid, typeid, name, sex, idcard, cardname, leixing, companyid, zsbh, zyyzh, yxq)
            print(f"人员inertaddon18 {name}入库完成")
            personid = searchperson(zyyzh, name)
        aid = personid[0]
        if searchqr(aid):
            print('qx', aid, 'exist')
        else:
            insert_qr(fid, aid)  # 企业 人员
            print(f'qr {aid} 关联入库完成')


# 插入项目表yunqi_addoninfos
def insert_addoninfos(pro, cname):
    # 插入项目表yunqi_addoninfos
    print(pro)
    project = pro.get('prodetail')
    Propertys = [
        {'id': "001", 'name': "新建"},
        {'id': "002", 'name': "改建"},
        {'id': "003", 'name': "扩建"},
        {'id': "004", 'name': "恢复"},
        {'id': "005", 'name': "迁建"},
        {'id': "006", 'name': "拆除"},
        {'id': "099", 'name': "其他"}]
    prTypes = [
        {'id': "01", 'name': 13},
        {'id': "02", 'name': 18}
    ]
    fid = searchdb(cname)[0]#企业id
    pnumber = project.get('prjNum')
    title = project.get('prjName')
    typeid =13
    for prtype in prTypes:
        if prtype['id'] == project.get('prjTypeNum'):
            typeid = prtype['name']
    mid = 10036
    senddate = int(time.time())
    cityid=get_region(str(project.get('cityNum')))
    print(cityid)
    if cityid:
        nativeplace = findcityid(cityid)
    else:
        nativeplace=0.0
    # print('ssssssssssssssssssssssssss:',cityid,nativeplace)
    linkman = project.get('buildCorpName', '-')
    ztzmoney = project.get('allInvest', 0.0)
    sjxmnumber = project.get('provincePrjNum', '-')
    lxwh = project.get('prjApprovalNum', '-')
    zzjgdm = project.get('buildCorpCode', '-')
    jsxz = '-'
    for property in Propertys:
        if property['id'] == project.get('prjPropertyNum','099'):
            jsxz = property['name']
    lxjb = project.get('prjApprovalLevelNum', '-')
    tarea = project.get('allArea', 0.0)
    # insertaddoninfos()
    print('addoninfos:', fid, typeid, mid, title, senddate, nativeplace,linkman, pnumber, ztzmoney, lxwh, sjxmnumber,
          zzjgdm, jsxz, tarea, lxjb)
    # time.sleep(222222)
    aid=search_aid(pnumber)
    if aid:
        print('项目表yunqi_addoninfos', pnumber, 'exist')
        updataaddoninfos(pnumber,nativeplace)
        # continue
    else:
        insertaddoninfos(fid, typeid, mid, title, senddate, nativeplace,linkman, pnumber, ztzmoney, lxwh, sjxmnumber,
                         zzjgdm, jsxz, tarea, lxjb)
        print(f"项目表yunqi_addoninfos{pnumber}入库完成")
        aid = search_aid(pnumber)
        # print(pnumber)
    xid = aid
    if searchqx(xid[0]):
        print(f'qx {xid} exist')
    else:
        insert_qx(fid, xid)
        print(f'qx {xid} 关联入库完成')

    # 插入参与单位与相关负责人yunqi_addoninfos_cydw
    if pro.get('jointhing'):
        corproles = [
            {'id': "1", 'name': "勘察企业"},
            {'id': "2", 'name': "设计企业"},
            {'id': "3", 'name': "施工企业"},
            {'id': "4", 'name': "监理企业"},
            {'id': "5", 'name': "工程总承包单位"},
            {'id': "6", 'name': "质量检测机构"},
            {'id': "99", 'name': "其他"}

        ]
        for jointhing in pro.get('jointhing'):
            qid = fid #企业id
            kid = xid[0]
            qymc = jointhing.get('corpname', '-')
            tyshxydm = jointhing.get('corpcode', '-', )
            name = jointhing.get('personname', '-')
            idnum = jointhing.get('idcard', '-')
            role = '其他'
            for corrole in corproles:
                if corrole['id'] == jointhing.get('idcardtypenum'):
                    role = corrole['name']
            print('addoninfos_cydw:', title, kid, qid, qymc, tyshxydm, name, idnum, role)
            if search_cydw(kid, qymc):
                print(f'参与单位与相关负责人_cydw  {qymc} exist')
            else:
                insert_cydw(title, kid, qid, qymc, tyshxydm, name, idnum, role)
                print(f'参与单位与相关负责人_cydw 插入{qymc}成功')

    # 插入合同登记 yunqi_addoninfos_ht
    if pro.get('contract'):
        contractType = [
            {'id': "100", 'name': "勘察"},
            {'id': "200", 'name': "设计"},
            {'id': "301", 'name': "施工总包"},
            {'id': "302", 'name': "施工分包"},
            {'id': "303", 'name': "施工劳务"},
            {'id': "400", 'name': "监理"},
            {'id': "600", 'name': "工程总承包"},
            {'id': "700", 'name': "项目管理"},
            {'id': "800", 'name': "全过程工程咨询"},
            {'id': "900", 'name': "其他"}
        ]
        dataSourceTypes = [
            {'id': "1", 'name': "业务办理"},
            {'id': "2", 'name': "信息登记"},
            {'id': "3", 'name': "历史业绩补录"},
            {'id': "4", 'name': "共享交换"}
        ]
        for contract in pro.get('contract'):
            dj_number = contract.get('recordNum')
            kid = xid[0]  # '项目id',
            ba_number = contract.get('provinceContractNum')
            ht_type = ''
            for typeid in contractType:
                if typeid['id'] == contract.get('contractTypeNum'):
                    ht_type = typeid['name']
            money = contract.get('contractMoney')
            fb_qymc = contract.get('propietorCorpName', '-')
            cb_qymc = contract.get('contractorCorpName', '-')
            cb_id = searchdb(cb_qymc)
            if cb_id:
                cb_id = cb_id[0]
            type = contract.get('dataLevel')
            build = contract.get('prjSize')
            fb_xydm = contract.get('propietorCorpCode', '-')
            cb_xydm = contract.get('contractorCorpCode', '-')
            lh_qymc = contract.get('unitecontractorCorpName', '-')
            lh_xydm = contract.get('unitepropietorCorpName', '-')
            register_time = str_date(contract.get('createDate', ''))
            signing_time = str_date(contract.get('contractDate', ''))
            source = contract.get('dataSource', '-')
            for sourcetypes in dataSourceTypes:
                if sourcetypes['id'] == str(source):
                    source = sourcetypes['name']
            print('addoninfos_ht:', kid, ba_number, ht_type, dj_number, money, fb_qymc, cb_qymc, cb_id, type, build,
                  fb_xydm, cb_xydm,
                  lh_qymc, lh_xydm, register_time, signing_time, source)
            if searchht(dj_number):
                print(f'合同登记 {dj_number} exist')
            else:
                insert_ht(kid, ba_number, ht_type, dj_number, money, fb_qymc, cb_qymc, cb_id, type, build, fb_xydm, cb_xydm,
                          lh_qymc, lh_xydm, register_time, signing_time, source)
                print(f'合同登记 插入{dj_number}成功')

    # 插入竣工验收yunqi_addoninfos_jgys
    if pro.get('finish'):
        for finish in pro.get('finish'):
            babh = finish.get('prjFinishNum')
            sjbabh = finish.get('provincePrjFinishNum')
            kid = fid
            sjzj = finish.get('factCost', 0.0)
            sjmj = finish.get('factArea', 0.0)
            sjkgrq = Transformation(finish.get('cREATEDATE', '0'))
            jgys = Transformation(finish.get('eDate', '0'))
            xqurl = ''
            print('addoninfos_jgys:', kid, babh, sjbabh, sjzj, sjmj, sjkgrq, jgys, xqurl)
            if searchjgys(babh, sjbabh):
                print(f'竣工验收 {babh} exist')
            else:
                insert_jgys(kid, babh, sjbabh, sjzj, sjmj, sjkgrq, jgys, xqurl)
                print(f'竣工验收 插入{babh}成功')

    # 插入施工许可信息yunqi_addoninfos_sgxk
    if pro.get('licence'):
        for licence in pro.get('licence'):
            kid = fid
            pid = xid[0]
            sgbh = licence.get('builderLicenceNum', '-')
            sjbh = licence.get('projectPlanNum', '0')
            htje = licence.get('contractMoney', '0')
            mj = licence.get('area', '0.0')
            fzrq = Transformation(licence.get('createDate','0'))
            xqurl = ''
            print('addoninfos_sgxk:', kid, pid, sgbh, sjbh, htje, mj, fzrq, xqurl)
            if searchsgxk(sgbh, sjbh):
                print(f'施工许可 sgxk {sgbh} exist')
            else:
                insert_sgxk(kid, pid, sgbh, sjbh, htje, mj, fzrq, xqurl)
                print(f'施工许可 sgxk insert{sgbh} ')

    # 插入工程项目单体信息yunqi_addoninfos_dt
    if pro.get('unit'):
        prstructuretypes = [
            {'id': "001", 'name': "砖混结构"},
            {'id': "002", 'name': "底框结构"},
            {'id': "003", 'name': "框架结构"},
            {'id': "004", 'name': "框架－剪力墙结构"},
            {'id': "005", 'name': "剪力墙结构"},
            {'id': "006", 'name': "板柱-剪力墙结构"},
            {'id': "007", 'name': "短肢墙剪力墙结构"},
            {'id': "008", 'name': "部分框支剪力墙结构"},
            {'id': "009", 'name': "框-筒体结构"},
            {'id': "010", 'name': "筒中筒结构"},
            {'id': "011", 'name': "异型柱框架结构"},
            {'id': "012", 'name': "复杂高层结构"},
            {'id': "013", 'name': "混合结构"},
            {'id': "014", 'name': "钢结构"},
            {'id': "015", 'name': "排架结构"},
            {'id': "016", 'name': "木结构"},
            {'id': "099", 'name': "其他"}
        ]
        prjLevels = [
            {'id': "201", 'name': "甲级"},
            {'id': "202", 'name': "乙级"},
            {'id': "203", 'name': "丙级"},
            {'id': "310", 'name': "特级"},
            {'id': "311", 'name': "一级"},
            {'id': "312", 'name': "二级"},
            {'id': "313", 'name': "三级"},
            {'id': "321", 'name': "大型"},
            {'id': "322", 'name': "中型"},
            {'id': "323", 'name': "小型"}
        ]
        greenBuildingLevels = [
            {'id': "001", 'name': "一星级"},
            {'id': "002", 'name': " 二星级"},
            {'id': "003", 'name': "三星级"}
        ]
        seismicintensityScales = [
            {'id': "001", 'name': "不设防"},
            {'id': "002", 'name': "6度"},
            {'id': "003", 'name': "7度"},
            {'id': "004", 'name': "8度"},
            {'id': "005", 'name': "9度"}]
        for unit in pro.get('unit'):
            number = unit.get('unitcode', '-')
            kid = xid[0]
            title = unit.get('subprjname')
            cost = unit.get('invest', '0.0')
            area = unit.get('buildarea', '0.0')
            if area == '无':
                area = '0.0'
            height = unit.get('buildheight', '0.0')
            structure = unit.get('structuretypenum', '-')
            for structuretype in prstructuretypes:
                if structuretype['id'] == structure:
                    structure = structuretype['name']
            grade = unit.get('prjlevelnum', '-')
            for prjlevel in prjLevels:
                if prjlevel['id'] == grade:
                    grade = prjlevel['name']
            up_area = unit.get('floorbuildarea', '0.0').replace('平方米', '').replace('无', '0.0')
            dw_area = unit.get('rfbottomarea', '0.0')
            layer = unit.get('floorcount', 0)
            if '层' in str(layer):
                layer = layer.replace('层', '')
                if '、' in layer:
                    layer = len(layer.split('、'))
            else:
                layer = 0
            down_layer = unit.get('bottomfloorcount', 0)
            if '层' in str(down_layer):
                down_layer = down_layer.replace('层', '')
                if '、' in down_layer:
                    down_layer = len(down_layer.split('、'))
            else:
                down_layer = 0
            long = unit.get('subprojectlength', 0.0)
            wide = unit.get('subprojectspan', 0.0)
            protect = unit.get('rfbottomarea', '0.0')
            scale = '-'
            other = '-'
            ztb_number = '-'
            sg_number = unit.get('censornum', '-')
            xk_number = unit.get('builderlicencenum', '-')
            zl_number = unit.get('qualitynum', '-')
            aq_number = unit.get('safenum', '-')
            shock = unit.get('isshockisolationbuilding', '-')
            green = unit.get('isgreenbuilding', '-')
            green_type = '-'
            for greenlevel in greenBuildingLevels:
                if greenlevel['id'] == unit.get('greenbuidinglevel'):
                    green_type = greenlevel['name']
            shocks = '-'
            for Scales in seismicintensityScales:
                if Scales['id'] == unit.get('seismicintensityscale'):
                    shocks = Scales['name']
            limit = unit.get('issuperhightbuilding')
            set = unit.get('suitecount')
            rebar = '-'
            steel = '-'
            print('addoninfos_dt:', kid, title, number, cost, area, height, structure, grade, up_area, dw_area, layer,
                  down_layer, long, wide, protect, scale, other, ztb_number, sg_number, xk_number, zl_number, aq_number,
                  shock, green, green_type, shocks, limit, set, rebar, steel)

            if search_dt(number):
                print(f'工程项目单体 dt {number} exist')
            else:
                insert_dt(kid, title, number, cost, area, height, structure, grade, up_area, dw_area, layer, down_layer,
                          long, wide, protect, scale, other, ztb_number, sg_number, xk_number, zl_number, aq_number, shock,
                          green, green_type, shocks, limit, set, rebar, steel)
                print(f'工程项目单体 dt 插入{number}成功')
    
    # 插入施工图审查yunqi_addoninfos_sgtsc
    if pro.get('censor'):
        for censor in pro.get('censor'):
            sgtschgbh = censor.get('censorNum', '-')
            kid = fid
            pid = xid[0]
            sjbh = censor.get('provinceCensorNum', '-')
            kcdw = censor.get('', '-')
            kcdw_sf = censor.get('', '-')
            kcdw_dm = censor.get('', '-')
            sjdw = censor.get('', '-')
            sjdw_sf = censor.get('', '-')
            sjdw_dm = censor.get('', '-')
            sgdw = censor.get('', '-')
            sgdw_sf = censor.get('', '-')
            sgdw_dm = censor.get('', '-')
            scjg = censor.get('censorCorpName', '-')
            scjg_dm = censor.get('censorCorpCode', '-')
            guimo = censor.get('', '-')
            wcrq = Transformation(censor.get('createDate', '0'))
            xqurl = '-'
            endtime = Transformation(censor.get('censorEDate', '0'))
            # print(endtime)
            jsgm = censor.get('prjSize', '-')
            one = censor.get('oneCensorIsPass', '-')
            startime = Transformation(censor.get('createDate', '0'))
            lh = censor.get('oneCensorWfqtCount', '-')
            xftime = censor.get('', '-')
            xfhg = censor.get('', '-')
            xfjg = censor.get('', '-')
            rftime = censor.get('', '-')
            rfhj = censor.get('', '-')
            rfjg = censor.get('', '-')
            lerver = censor.get('dataLevel', '-')
            print('addoninfos_dt:', kid, pid, sgtschgbh, sjbh, kcdw, kcdw_sf, kcdw_dm, sjdw, sjdw_sf, sjdw_dm, sgdw,
                  sgdw_sf,
                  sgdw_dm, scjg, scjg_dm, guimo, wcrq, xqurl, endtime, jsgm, one, startime, lh, xftime,
                  xfhg, xfjg, rftime, rfhj, rfjg, lerver)
            if search_sgtsc(sgtschgbh):
                print(f'施工图审查 sgtsc {sgtschgbh} exist')
            else:

                insert_sgtsc(kid, pid, sgtschgbh, sjbh, kcdw, kcdw_sf, kcdw_dm, sjdw, sjdw_sf, sjdw_dm, sgdw,
                             sgdw_sf, sgdw_dm, scjg, scjg_dm, guimo, wcrq, xqurl, endtime, jsgm, one, startime, lh,
                             xftime, xfhg, xfjg, rftime, rfhj, rfjg, lerver)
                print(f'施工图审查 sgtsc 插入{sgtschgbh}成功')

    # 插入招投标yunqi_addoninfos_ztb
    if pro.get('tender'):
        prtenderclasss = [
            {'id': "001", 'name': "勘察"},
            {'id': "002", 'name': "设计"},
            {'id': "003", 'name': "施工"},
            {'id': "004", 'name': "监理"},
            {'id': "006", 'name': "工程总承包"},
            {'id': "007", 'name': "项目管理"},
            {'id': "010", 'name': "全过程工程咨询"},
            {'id': "011", 'name': "其他"}
        ]
        prtendertypes = [
            {'id': "001", 'name': "公开招标"},
            {'id': "002", 'name': "邀请招标"},
            {'id': "003", 'name': "直接委托"},
            {'id': "099", 'name': "其他"}
        ]
        for tender in pro.get('tender'):
            tzsbh = tender.get('tenderNum', '-')
            kid = fid
            pid = xid[0]
            zblx = tender.get('tenderClassNum')
            for ptender in prtenderclasss:
                if ptender['id'] == zblx:
                    zblx = ptender.get('name')
            zbfs = tender.get('tenderTypeNum')
            for tendertype in prtendertypes:
                if tendertype['id'] == zbfs:
                    zbfs = tendertype.get('name')
            zbdw = tender.get('tenderCorpName', '-')
            zbrq = '0'
            zbje = tender.get('tenderMoney', '0')
            sjbh = tender.get('provinceTenderNum', '-')
            xqurl = '-'
            print('addoninfos_ztb:', kid, pid, zblx, zbfs, zbdw, zbrq, zbje, tzsbh, sjbh, xqurl)
            if search_ztb(tzsbh):
                print(f'招投标 ztb {tzsbh} exist')
            else:
                insert_ztb(kid, pid, zblx, zbfs, zbdw, zbrq, zbje, tzsbh, sjbh, xqurl)
                print(f'招投标 ztb 插入{tzsbh}成功')

    # 插入施工现场安全专业人员addoninfos_sgxcaqy
    if pro.get('safeuser'):
        userTypes = [
            {'id': "1", 'name': "主要负责人"},
            {'id': "2", 'name': "项目负责人"},
            {'id': "3", 'name': "安全员"}]
        for safeuser in pro.get('safeuser'):
            idnum = safeuser.get('iDCard')
            tyshxydm = safeuser.get('corpCode')
            name = safeuser.get('userName')
            if search_sgxcaqy(idnum, tyshxydm):
                print(f'安全员 sgxcaqy {name} exist')
            else:
                kid = fid  # 企业id
                pid = xid[0]  # 项目id
                qymc = safeuser.get('corpName')
                aqxkzbh = safeuser.get('certID', '-')
                sgxkzbh = safeuser.get('builderLicenceNum', '-')
                usertype = str(safeuser.get('userType'))
                for utype in userTypes:
                    if utype['id'] == usertype:
                        usertype = utype.get('name')
                print(title, kid, pid, qymc, tyshxydm, name, idnum, aqxkzbh, sgxkzbh, usertype)
                insert_sgxcaqy(title, kid, pid, qymc, tyshxydm, name, idnum, aqxkzbh, sgxkzbh, usertype)
                print(f'安全员 sgxcaqy 插入{name}成功')


    # 施工现场管理人员addoninfos_sgxcglr
    if pro.get('manageuser'):
        for manageuser in pro.get('manageuser'):
            name = manageuser.get('userName', '-')
            title = title
            kid = fid  # 企业id
            pid = xid[0]  # 项目id
            tyshxydm = manageuser.get('corpCode', '-')
            idnum = manageuser.get('iDCard', '-')
            ssqy = manageuser.get('corpName', '-')
            sgxkzbh = manageuser.get('', '-')
            gwmc = manageuser.get('postName', '-')
            zsbh = manageuser.get('postcertNum', '-')
            zsyxq = Transformation(manageuser.get('certendDate', '0'))
            fzdw = manageuser.get('organName', '-')
            print('addoninfos_sgxcglr:', title, kid, pid, tyshxydm, name, idnum, ssqy, sgxkzbh, gwmc, zsbh, zsyxq, fzdw)
            if search_sgxcglr(name, title):
                print(f'现场管理人员 sgxcglr {name} exist')
            else:
                insert_sgxcglr(title, kid, pid, tyshxydm, name, idnum, ssqy, sgxkzbh, gwmc, zsbh, zsyxq, fzdw)
                print(f'现场管理人员 sgxcglr 插入{name}成功')


    # 施工现场特种作业人员addoninfos_sgxctzzyr
    if pro.get('operation'):
        workTypes = [
            {'id': "000", 'name': "其他"},
            {'id': "010", 'name': "砌筑工（建筑瓦工、瓦工）"},
            {'id': "011", 'name': "窑炉修筑工"},
            {'id': "020", 'name': "钢筋工"},
            {'id': "030", 'name': "架子工"},
            {'id': "031", 'name': "附着升降脚手架安装拆卸工"},
            {'id': "032", 'name': "高处作业吊篮操作工"},
            {'id': "033", 'name': "高处作业吊篮安装拆卸工"},
            {'id': "040", 'name': "混凝土工"},
            {'id': "041", 'name': "混凝土搅拌工"},
            {'id': "042", 'name': "混凝土浇筑工"},
            {'id': "043", 'name': "混凝土模具工"},
            {'id': "050", 'name': "模板工（混凝土模板工）"},
            {'id': "060", 'name': "机械设备安装工"},
            {'id': "070", 'name': "通风工"},
            {'id': "080", 'name': "安装起重工（起重工、起重装卸机械操作工）"},
            {'id': "090", 'name': "安装钳工"},
            {'id': "100", 'name': "电气设备安装调试工"},
            {'id': "110", 'name': "管道工（管工）"},
            {'id': "120", 'name': "变电安装工"},
            {'id': "130", 'name': "建筑电工"},
            {'id': "131", 'name': "弱电工"},
            {'id': "140", 'name': "司泵工"},
            {'id': "150", 'name': "挖掘铲运和桩工机械司机"},
            {'id': "151", 'name': "推土（铲运）机驾驶员（推土机司机）"},
            {'id': "152", 'name': "挖掘机驾驶员（土石方挖掘机司机）"},
            {'id': "153", 'name': "桩工（打桩工）"},
            {'id': "160", 'name': "桩机操作工"},
            {'id': "170", 'name': "起重信号工（起重信号司索工）"},
            {'id': "180", 'name': "建筑起重机械安装拆卸工"},
            {'id': "190", 'name': "装饰装修工"},
            {'id': "191", 'name': "抹灰工"},
            {'id': "192", 'name': "油漆工"},
            {'id': "193", 'name': "镶贴工"},
            {'id': "194", 'name': "涂裱工"},
            {'id': "195", 'name': "装饰装修木工"},
            {'id': "196", 'name': "室内装饰设计师"},
            {'id': "200", 'name': "室内成套设施安装工"},
            {'id': "210", 'name': "建筑门窗幕墙安装工"},
            {'id': "211", 'name': "幕墙安装工（建筑幕墙安装工）"},
            {'id': "212", 'name': "建筑门窗安装工"},
            {'id': "220", 'name': "幕墙制作工"},
            {'id': "230", 'name': "防水工"},
            {'id': "240", 'name': "木工"},
            {'id': "241", 'name': "手工木工"},
            {'id': "242", 'name': "精细木工"},
            {'id': "250", 'name': "石工（石作业工）"},
            {'id': "270", 'name': "电焊工（焊工）"},
            {'id': "280", 'name': "爆破工"},
            {'id': "290", 'name': "除尘工"},
            {'id': "300", 'name': "测量放线工（测量工、工程测量员）"},
            {'id': "305", 'name': "质检员"},
            {'id': "310", 'name': "线路架设工"},
            {'id': "320", 'name': "古建筑传统石工（石雕工、砧细工）"},
            {'id': "330", 'name': "古建筑传统瓦工（砧刻工、砌花街工、泥塑工、古建瓦工）"},
            {'id': "340", 'name': "古建筑传统彩画工（彩绘工）"},
            {'id': "350", 'name': "古建筑传统木工（木雕工、匾额工）"},
            {'id': "360", 'name': "古建筑传统油工（推光漆工、古建油漆）"},
            {'id': "380", 'name': "金属工"},
            {'id': "401", 'name': "水暖工"},
            {'id': "404", 'name': "沥青混凝土推铺机操作工"},
            {'id': "405", 'name': "沥青工"},
            {'id': "406", 'name': "筑炉工"},
            {'id': "407", 'name': "工程机械修理工"},
            {'id': "408", 'name': "道路巡视养护工（道路养护工）"},
            {'id': "409", 'name': "桥隧巡视养护工"},
            {'id': "410", 'name': "中小型机械操作工"},
            {'id': "411", 'name': "管涵顶进工"},
            {'id': "412", 'name': "盾构机操作工"},
            {'id': "413", 'name': "筑路工"},
            {'id': "414", 'name': "桥隧工"},
            {'id': "415", 'name': "城市管道安装工"},
            {'id': "416", 'name': "起重驾驶员（含塔式、门式、桥式等起重机驾驶员）"},
            {'id': "418", 'name': "试验工"},
            {'id': "419", 'name': "中央空调系统运行操作员"},
            {'id': "420", 'name': "智能楼宇管理员"},
            {'id': "421", 'name': "电梯安装维修工"},
            {'id': "422", 'name': "建筑模型制作工"},
            {'id': "423", 'name': "接触网工"},
            {'id': "424", 'name': "物业管理员"},
            {'id': "425", 'name': "房地产经纪人"},
            {'id': "426", 'name': "房地产策划师"},
            {'id': "427", 'name': "雕塑翻制工"},
            {'id': "428", 'name': "司钻员"},
            {'id': "429", 'name': "描述员"},
            {'id': "430", 'name': "土工试验员"},
            {'id': "431", 'name': "建筑外墙保温安装工"},
            {'id': "432", 'name': "仪表安装调试工"},
            {'id': "433", 'name': "空调安装调试工"},
            {'id': "434", 'name': "安装铆工"},
            {'id': "435", 'name': "消防安装工"},
            {'id': "436", 'name': "防腐保温工"},
            {'id': "437", 'name': "构件装配工"},
            {'id': "438", 'name': "构件制作工"},
            {'id': "439", 'name': "预埋工"},
            {'id': "440", 'name': "灌浆工"},
            {'id': "501", 'name': "绿化工（园林绿化工）"},
            {'id': "502", 'name': "花卉工（花卉园艺工）"},
            {'id': "503", 'name': "园林植保工"},
            {'id': "504", 'name': "展出动物保育员（观赏动物饲养员）"},
            {'id': "505", 'name': "育苗工"},
            {'id': "506", 'name': "构件制作工"},
            {'id': "507", 'name': "假山工"},
            {'id': "508", 'name': "花艺环境设计师"},
            {'id': "601", 'name': "保洁员"},
            {'id': "602", 'name': "机动清扫工（道路清扫工）"},
            {'id': "603", 'name': "垃圾清运工"},
            {'id': "604", 'name': "垃圾处理工"},
            {'id': "605", 'name': "环卫垃圾运输装卸工"},
            {'id': "606", 'name': "环卫机动车修理工"},
            {'id': "607", 'name': "环卫化验工"},
            {'id': "608", 'name': "环卫公厕管理保洁工"},
            {'id': "609", 'name': "环卫船舶轮机员"},
            {'id': "610", 'name': "环卫机动车驾驶员"},
            {'id': "701", 'name': "预液化石油气罐工埋工"},
            {'id': "702", 'name': "液化石油气机械修理工"},
            {'id': "703", 'name': "液化石油气钢瓶检修工"},
            {'id': "704", 'name': "液化石油气库站运行工"},
            {'id': "705", 'name': "液化石油气罐区运行工"},
            {'id': "706", 'name': "燃气压力容器焊工"},
            {'id': "707", 'name': "燃气输送工"},
            {'id': "708", 'name': "燃气管道工"},
            {'id': "709", 'name': "燃气用具修理工"},
            {'id': "710", 'name': "燃气净化工"},
            {'id': "711", 'name': "燃气化验工"},
            {'id': "712", 'name': "燃气调压工"},
            {'id': "713", 'name': "燃气表装修工"},
            {'id': "714", 'name': "燃气用具安装检修工"},
            {'id': "715", 'name': "燃气供应服务员/供气营销员"},
            {'id': "716", 'name': "管道燃气客服员"},
            {'id': "717", 'name': "瓶装气客服员"},
            {'id': "718", 'name': "燃气储运工"},
            {'id': "719", 'name': "液化天然气储运工"},
            {'id': "720", 'name': "燃气管网运行工"},
            {'id': "721", 'name': "燃气用户安装检修工"},
            {'id': "722", 'name': "压缩天然气场站运行工"},
            {'id': "723", 'name': "燃气输配场站运行工"},
            {'id': "724", 'name': "配煤工"},
            {'id': "725", 'name': "焦炉调温工"},
            {'id': "726", 'name': "炼焦煤气炉工"},
            {'id': "727", 'name': "热力司炉工"},
            {'id': "728", 'name': "热力运行工"},
            {'id': "729", 'name': "焦炉维护工"},
            {'id': "730", 'name': "机械煤气发生炉工"},
            {'id': "731", 'name': "煤焦车司机"},
            {'id': "732", 'name': "胶带机输送工"},
            {'id': "733", 'name': "冷凝鼓风工"},
            {'id': "734", 'name': "水煤气炉工"},
            {'id': "735", 'name': "生活燃煤供应工"},
            {'id': "736", 'name': "煤制气工"},
            {'id': "737", 'name': "重油制气工（油制气工）"},
            {'id': "738", 'name': "锅炉操作工"},
            {'id': "739", 'name': "供热管网系统运行工"},
            {'id': "740", 'name': "热力管网运行工"},
            {'id': "741", 'name': "供热生产调度工"},
            {'id': "742", 'name': "热力站运行工"},
            {'id': "743", 'name': "中继泵站运行工"},
            {'id': "801", 'name': "变配电运行工"},
            {'id': "802", 'name': "泵站机电设备维修工"},
            {'id': "803", 'name': "水生产处理工"},
            {'id': "804", 'name': "自来水生产工"},
            {'id': "805", 'name': "水质检验工"},
            {'id': "806", 'name': "水井工"},
            {'id': "807", 'name': "供水调度员"},
            {'id': "808", 'name': "供水管道工"},
            {'id': "809", 'name': "供水泵站运行工"},
            {'id': "810", 'name': "供水营销员"},
            {'id': "811", 'name': "供水仪表工"},
            {'id': "812", 'name': "供水稽查员"},
            {'id': "813", 'name': "供水客户服务员"},
            {'id': "814", 'name': "供水设备维修钳工"},
            {'id': "815", 'name': "水表装修工"},
            {'id': "816", 'name': "排水管道工"},
            {'id': "817", 'name': "排水巡查员"}, {'id': "818", 'name': "排水调度工"},
            {'id': "819", 'name': "排水泵站运行工"},
            {'id': "820", 'name': "排水客户服务员"},
            {'id': "821", 'name': "排水仪表工"},
            {'id': "822", 'name': "城镇污水处理工（污水处理工）"},
            {'id': "823", 'name': "排水化验检测工"},
            {'id': "824", 'name': "污泥处理工"},
            {'id': "901", 'name': "白蚁防治工"}
        ]
        for operation in pro.get('operation'):
            name = operation.get('userName')
            title = title
            kid = fid  # 企业id
            pid = xid[0]  # 项目id
            idnum = operation.get('iDCard', '-')
            ssqy = operation.get('corpName', '-')
            tyshxydm = operation.get('corpCode', '-')
            sgxkzbh = '-'
            gz = operation.get('workTypeNum', '000')
            for worktype in workTypes:
                if worktype['id'] == gz:
                    gz = worktype.get('name')
            zsbh = operation.get('certNum', '-')
            zsyxq = 0
            fzdw = '-'
            print('addoninfos_sgxctzzyr:', title, kid, pid, name, idnum, ssqy, tyshxydm, sgxkzbh, gz, zsbh, zsyxq, fzdw)
            if search_sgxctzzyr(name):
                print(f'特种作业人员 sgxctzzyr {name} exist')
            else:

                insert_sgxctzzyr(title, kid, pid, name, idnum, ssqy, tyshxydm, sgxkzbh, gz, zsbh, zsyxq, fzdw)
                print(f'特种作业人员 sgxctzzyr 插入{name}成功')


    # 施工现场机械设备addoninfos_sgxcjxsb
    if pro.get('mechanics'):
        for mechanics in pro.get('mechanics'):
            sbbabh = mechanics.get('recordNum', '-')
            title = title
            kid = fid  # 企业id
            pid = xid[0] # 项目id
            jxsbmc = mechanics.get('mechanicsname', '-')
            cqdw = mechanics.get('havecorpName', '-')
            jxmodel = mechanics.get('model', '-')
            sgxkzbh = mechanics.get('', '-')
            sydw = mechanics.get('usecorpName', '-')
            sybw = mechanics.get('usePosition', '-')
            acdw = mechanics.get('incorpName', '-')
            jhjcsj = Transformation(mechanics.get('inDate', '0'))
            jhccsj = Transformation(mechanics.get('outDate', '0'))
            print('addoninfos_sgxcjxsb:', title, kid, pid, jxsbmc, cqdw, jxmodel, sgxkzbh, sydw, sybw, acdw, sbbabh, jhjcsj,
                  jhccsj)
            if search_sgxcjxsb(sbbabh):
                print(f'现场机械设备 sgxcjxsb {sbbabh} exist')
            else:
                insert_sgxcjxsb(title, kid, pid, jxsbmc, cqdw, jxmodel, sgxkzbh, sydw, sybw, acdw, sbbabh, jhjcsj, jhccsj)
                print(f'现场机械设备 sgxcjxsb 插入{sbbabh}成功')
    
    #专业人员名单 addoninfos_zyry
    if pro.get('censor_user'):
        userSpecialTypes = [
            {
                'id': "01",
                'name': "岩土工程勘察"
            }, {
                'id': "02",
                'name': "岩土工程设计"
            }, {
                'id': "03",
                'name': "水文地质"
            }, {
                'id': "04",
                'name': "工程测量"
            }, {
                'id': "05",
                'name': "岩土测试检测"
            }, {
                'id': "07",
                'name': "岩土监测"
            }, {
                'id': "08",
                'name': "室内试验"
            }, {
                'id': "09",
                'name': "建筑"
            }, {
                'id': "10",
                'name': "结构"
            }, {
                'id': "11",
                'name': "给水排水"
            }, {
                'id': "12",
                'name': "暖通空调"
            }, {
                'id': "13",
                'name': "电气"
            }, {
                'id': "14",
                'name': "防护"
            }, {
                'id': "15",
                'name': "防化"
            }, {
                'id': "16",
                'name': "通信"
            }, {
                'id': "17",
                'name': "动力"
            }, {
                'id': "18",
                'name': "自控"
            }, {
                'id': "19",
                'name': "机械"
            }, {
                'id': "20",
                'name': "通信信号"
            }, {
                'id': "21",
                'name': "站场"
            }, {
                'id': "22",
                'name': "道路"
            }, {
                'id': "23",
                'name': "线路"
            }, {
                'id': "24",
                'name': "桥梁"
            }, {
                'id': "25",
                'name': "园林"
            }, {
                'id': "26",
                'name': "环保"
            }, {
                'id': "27",
                'name': "概预算"
            }, {
                'id': "28",
                'name': "工程经济"
            }, {
                'id': "99",
                'name': "其他"
            }]
        prUserRole = [
            {
                'id': "001",
                'name': "项目负责人"
            }, {
                'id': "002",
                'name': "专业负责人"
            }, {
                'id': "003",
                'name': "主要设计人"
            }, {
                'id': "004",
                'name': "图审机构项目负责人"
            }, {
                'id': "005",
                'name': "图审机构审定人"
            }, {
                'id': "006",
                'name': "图审机构审查人从事专业名称"
            }]
        for censoruser in pro.get('censor_user'):
            kid = xid[0]#项目id
            CORPNAME = censoruser.get('corpname','-')
            IDCARD= censoruser.get('idcard','-')
            SPECIALTYTYP= censoruser.get('specialtytypnum','99')
            for SpecialType in  userSpecialTypes:
                if SpecialType['id'] == SPECIALTYTYP:
                    SPECIALTYTYP = SpecialType.get('name')
            TBWORKDUTYDIC= censoruser.get('prjduty')
            for workduty in  prUserRole:
                if workduty['id'] == TBWORKDUTYDIC:
                    TBWORKDUTYDIC = workduty.get('name')
            SPE= '-'
            TECHTITLELEVEL= '-'
            CORPID= censoruser.get('corpcode','-')
            PRJNUM= censoruser.get('prjnum','-')
            CORPCODE= censoruser.get('corpcode','-')
            USERID= censoruser.get('userid','-')
            USERNAME= censoruser.get('username','-')
            CENSORNUM= censoruser.get('censornum','-')
            IDCARDTYPENUM= 1
            print(kid,CORPNAME,IDCARD,SPECIALTYTYP,TBWORKDUTYDIC,SPE,TECHTITLELEVEL,CORPID,PRJNUM,CORPCODE,USERID,USERNAME,CENSORNUM,IDCARDTYPENUM)
            if search_zyry(IDCARD,CENSORNUM,SPECIALTYTYP):

                print(f'现场机械设备 sgxcjxsb {USERNAME} exist')
            else:
                insert_zyry(kid,CORPNAME,IDCARD,SPECIALTYTYP,TBWORKDUTYDIC,SPE,TECHTITLELEVEL,CORPID,PRJNUM,CORPCODE,USERID,USERNAME,CENSORNUM,IDCARDTYPENUM)
                print(f'专业技术人员 zyry  插入{USERNAME}完成 ')

    # 插入施工图审查yunqi_addoninfos_wf

    # censor_err=pro.get('censor_err')
    # print(censor_err)
    # if censor_err:
    #     for censorerr in censor_err:
    #
    #         fid=''
    #         sgsc=censorerr.get('','-')
    #         wf=censorerr.get('','-')
    #         sc=censorerr.get('','-')
    #         qz=censorerr.get('','-')
    #         qw=censorerr.get('','-')
    #         print(fid,sgsc,wf,sc,qz,qw)

    # except Exception as e:
    #
    #     with open(file=f"company_base/companydb{fil}.json", mode="a", encoding="utf-8") as w:
    #         w.write(str(data) + '\n')
    #     w.close()
    #     logging.error(f"add db problem{e}\n{traceback.format_exc()}")


if __name__ == '__main__':
    fil = str(datetime.datetime.today().strftime('%Y-%m-%d'))
    # data={'base': {'legalMan': '刘银川', 'corpName': '新疆华宇星建设工程有限公司', 'corpCode': '91650100MA775EDJX8', 'id': '002105291335084697', 'address': '新疆图木舒克市前海西街27号（双创中心）', 'regionFullname': '新疆生产建设兵团-第三师', 'qyRegType': '有限责任公司（自然人投资或控股）'}, 'messagecount': {'certCount': 2, 'regPersonCount': 9, 'projectCount': 0}, 'cert': [{'certType': '建筑业企业资质', 'certName': '电力工程施工总承包三级', 'organDate': '2022-12-29', 'endDate': '2023-12-31', 'organName': '新疆生产建设兵团住房和城乡建设局', 'certId': 'D266006420', 'corpName': '新疆华宇星建设工程有限公司', 'corpCode': '91650100MA775EDJX8'}, {'certType': '建筑业企业资质', 'certName': '电力工程施工总承包三级', 'organDate': '2021-12-24', 'endDate': '2023-12-31', 'organName': '乌鲁木齐市建设局（乌鲁木齐市人民防空办公室）', 'certId': 'D365019422', 'corpName': '新疆华宇星建设工程有限公司', 'corpCode': '91650100MA775EDJX8'}], 'regporson': [], 'project': [], 'badcredit': [], 'goodcredit': [], 'black': [], 'punishlist': [], 'chage': []}
    # data={'base': {'legalMan': '米玛桑布', 'corpName': '西藏中海建设工程有限公司', 'corpCode': '91540100MA6T10ND2E', 'id': '002105291313938434', 'address': '拉萨市扎囊县株洲路贡康小区10号', 'qyRegType': '有限责任公司（自然人投资或控股）'}, 'messagecount': {'certCount': 3, 'regPersonCount': 7, 'projectCount': 1}, 'cert': [{'certType': '建筑业企业资质', 'certName': '水利水电工程施工总承包三级', 'organDate': '2021-01-02', 'endDate': '2023-12-31', 'organName': '山南市住房和城乡建设局', 'certId': 'D354007018', 'corpName': '西藏中海建设工程有限公司', 'corpCode': '91540100MA6T10ND2E'}, {'certType': '建筑业企业资质', 'certName': '市政公用工程施工总承包三级', 'organDate': '2021-01-02', 'endDate': '2023-12-31', 'organName': '山南市住房和城乡建设局', 'certId': 'D354007018', 'corpName': '西藏中海建设工程有限公司', 'corpCode': '91540100MA6T10ND2E'}, {'certType': '建筑业企业资质', 'certName': '建筑工程施工总承包三级', 'organDate': '2021-01-02', 'endDate': '2023-12-31', 'organName': '山南市住房和城乡建设局', 'certId': 'D354007018', 'corpName': '西藏中海建设工程有限公司', 'corpCode': '91540100MA6T10ND2E'}], 'regporson': [], 'project': [], 'badcredit': [], 'goodcredit': [], 'black': [], 'punishlist': [], 'chage': []}
    data={'base': {'legalMan': '洛拥', 'corpName': '昌都察雅县利民建筑有限责任公司', 'corpCode': '915403007419282012', 'id': '002105291258788829', 'address': '昌都镇聚盛街91号', 'qyRegType': '有限责任公司（自然人投资或控股）'}, 'messagecount': {'certCount': 5, 'regPersonCount': 3, 'projectCount': 0}, 'cert': [{'certType': '建筑业企业资质', 'certName': '公路工程施工总承包二级', 'organDate': '2020-06-22', 'endDate': '2025-06-22', 'organName': '西藏自治区住房和城乡建设厅', 'certId': 'D254002763', 'corpName': '昌都察雅县利民建筑有限责任公司', 'corpCode': '915403007419282012'}, {'certType': '建筑业企业资质', 'certName': '市政公用工程施工总承包三级', 'organDate': '2020-09-07', 'endDate': '2025-09-07', 'organName': '昌都市住房和城乡建设局', 'certId': 'D354164411', 'corpName': '昌都察雅县利民建筑有限责任公司', 'corpCode': '915403007419282012'}, {'certType': '建筑业企业资质', 'certName': '公路路基工程专业承包三级', 'organDate': '2020-09-07', 'endDate': '2025-09-07', 'organName': '昌都市住房和城乡建设局', 'certId': 'D354164411', 'corpName': '昌都察雅县利民建筑有限责任公司', 'corpCode': '915403007419282012'}, {'certType': '建筑业企业资质', 'certName': '建筑工程施工总承包三级', 'organDate': '2020-09-07', 'endDate': '2025-09-07', 'organName': '昌都市住房和城乡建设局', 'certId': 'D354164411', 'corpName': '昌都察雅县利民建筑有限责任公司', 'corpCode': '915403007419282012'}, {'certType': '建筑业企业资质', 'certName': '水利水电工程施工总承包三级', 'organDate': '2020-09-07', 'endDate': '2025-09-07', 'organName': '昌都市住房和城乡建设局', 'certId': 'D354164411', 'corpName': '昌都察雅县利民建筑有限责任公司', 'corpCode': '915403007419282012'}], 'regporson': [], 'project': [], 'badcredit': [], 'goodcredit': [], 'black': [], 'punishlist': [], 'chage': []}

    insert_base(data)