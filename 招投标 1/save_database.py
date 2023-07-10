# -*- coding: utf-8 -*-
import time, re
import pymysql, tool
import random, traceback

# 保存招投标信息
conn = pymysql.connect(host='47.92.73.25', user='duxie', passwd='jtkpwangluo.com', port=3306, db='ytb')
# conn = pymysql.connect(host='192.168.1.53', port=3306, database="ztb", user='root', password='10036'
#                             , charset="utf8")
cursor = conn.cursor()


def redis_save(item):
    pass
    # item['removal'] = item['removal'].replace('\r', '').replace('\n', '').replace('\t', '').replace(' ', '')
    # with open('../log/' + item['date'] + '.txt', 'a', encoding='utf-8') as f:
    #     f.write(item['removal'] + '\n')


def mc_matching_title(title):
    # 去掉标题中的项目编号
    title_num = re.findall('[a-zA-Z]\d{12}', title)
    if len(title_num) != 0:
        title_ = title.replace(title_num[0], '')
        title = title_
    title = title.replace(' ', '')
    replace_ls = [
        '施工招标公告', '公开招标公告', '总承包招标公告', '招标公告', '候选中标公告', '中标公告', '废标公告', '竞争性磋商公告',
        '中标结果公告', '中标结果公示', '施工中标候选人公示', '中标候选人公示变更', '中标候选人公示', '竞争性磋商交易公告',
        '更正结果公告', '询价公告', '中标侯选人公示', '预中标公示', '中候选人公告', '候选人公示', '异常结果公告', '中标（成交）结果公告',
        '成交结果', '成交供应商', '成交工程', '招标评定报告',
        '结果公告', '更正（澄清）公告', '信息更正公告', '中标更正公告', '更正公告', '竞争性谈判公告', '竞争性谈判', '中标公示', '[更正/澄清公告]', '[澄清公告]',
        '【澄清公告】', '单一来源公告', '单一来源采购', '单一来源', '-披露公告', '披露公告', '竞争性磋商', '公开招标', '异常结果公示',
        '项目公告', '成交公告', '澄清公告', '出让公告', '竞争谈判公告', '谈判公告', '[变更公告]', '变更公告', '中标人公告',
        '交易公告', '成交公示', '磋商公告', '异常公告', '中标候选人', '中标（成交）公示', '补遗书', '中止公告',
        '中选公告', '终止公告', '恢复公告', '变更项目', '招标文件', '中标结果', '资格预审公告', '比选招标',
        '更正公示', '补充公告', '补充规划', '中标候选公示', '流标公告', '中标(成交)公告', '二次招标', '邀请招标',
        '招标代理机构', '比选公告', '交易信息', '延期开标', '重新招标', '中标人公示', '中标（成交）公告', '中标公选人公示', '结果公示',
        '取消中标资格', '二次公告', '三次公告', '（二次）', '（三次）', '补充项目', '监理招标', '二次招标', '三次招标'
    ]
    for t in replace_ls:
        title = title.replace(t, '').replace('"', "'")
    ls = ['招标', '成交', '施工', '暂停', '澄清', '[]', '【】', '二次', '公告', '公示', '更正', '()', '（）', '三次']
    for i in ls:
        if title.endswith(i):
            title = title[:-2]
            break

    ls = ['[]', '【】', '()', '（）']
    for i in ls:
        if title.startswith(i):
            title = title[2:]
            break

    ls = ['-', '的', '等']
    for i in ls:
        if title.endswith(i):
            title = title[:-1]
            break
    return title


def process_item(item):
    time.sleep(1)
    # print('item',item)
    try:
        try:
            conn.ping()
        except:
            conn()
        item['title'] = item['title'].replace(' ', '')
        if '测试' in item['title']:
            print('测试数据', item['url'])
            return True
        entry_name = mc_matching_title(item['title'])
        type_id = item['typeid'][0]
        item['typeid'] = [str(i) for i in item['typeid']]
        item['typeid'] = ','.join(item['typeid'])
        item['title'] = item['title'].replace(' ', '')
        sql = """insert into `dede_arctiny`(`typeid`, `senddate`, `mid`, `infotype`, `nativeplace`, `url`, `title`, `function`,`shi`,`sheng`,`entry_name`) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        cursor.execute(sql, (
            item["typeid"], item["senddate"], item["mid"], item["infotype"], item["nativeplace"], item["url"],
            item["title"], item["function"], item["shi"], item["sheng"], entry_name))
        aid = cursor.lastrowid
        conn.commit()

        try:
            conn.ping()
        except:
            conn()
        sqlstr = """insert into `{}`(`aid`, `typeid`, `mid` ,`title`,  `senddate`, `nativeplace`, `infotype`, `body`, `endtime`, `tel`, `email`, `address`, `linkman`,`function`, `url`, `resource`, `click`,`shi`,`sheng`)
                                      values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        if type_id in [16, 13, 77, 76, 73, 65, 64, 63, 74, 75, 19, 18, 17, 131, 132, 133, 134, 135, 136, 137, 138, 139,
                       140,
                       141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159,
                       160, 161, 162,
                       163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181,
                       182, 183, 184, 185,
                       186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204,
                       205, 206, 207,
                       208, 209, 210, 211, 212, 213, 214, 215, 216, 217, 218, 219, 220]:  # 施工总承包
            db = "dede_addoninfos1"
        elif type_id in [21, 22, 80, 38, 37, 36, 35, 34, 33, 32, 31, 30, 29, 28, 27, 26, 25, 24, 87,
                         23]:  # 工程设计
            db = "dede_addoninfos2"
        elif type_id in [39, 40, 51, 50, 49, 48, 47, 46, 45, 44, 43, 42, 41, 86]:  # 施工劳务
            db = "dede_addoninfos3"
        elif type_id in [69, 70, 78, 90, 91, 92, 67, 71, 83, 84, 15, 66, 91, 90, 84, 83, 78, 71, 70, 69, 68,
                         67, 92, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117,
                         118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 68]:  # 专业承包
            db = "dede_addoninfos4"
        elif type_id in [14, 52, 89, 60, 59, 58, 57, 56, 55, 54, 53, 93]:  # 工程监理
            db = "dede_addoninfos5"
        elif type_id == 20:  # 招标变更
            db = "dede_addoninfos6"
        elif type_id == 72:  # 材料采购
            db = "dede_addoninfos7"
        elif type_id == 81:  # 工程造价
            db = "dede_addoninfos8"
        else:
            db = "dede_addoninfos9"  # 土地规划
        sql2 = sqlstr.format(db)
        try:
            try:
                conn.ping()
            except:
                conn()
            cursor.execute(sql2, (
                aid, item["typeid"], item["mid"], item["title"],
                item["senddate"], item["nativeplace"], item["infotype"], item["body"], item["endtime"],
                item["tel"],
                item["email"],
                item["address"], item["linkman"], item["function"], item["url"],
                item["resource"], random.randint(500, 1000), item["shi"], item["sheng"]))
            conn.commit()
            redis_save(item)
            print("[插入成功]", item["typeid"], item["mid"], item["title"],
                  item["senddate"], item["nativeplace"], item["date"], item["infotype"],
                  item["endtime"], item["tel"],
                  item["email"],
                  item["address"], item["linkman"], item["function"], item["url"],
                  item["resource"])
            print("-" * 100)
            time.sleep(3)
        except pymysql.err.OperationalError:
            print("pymysql.err.OperationalError: (2013, 'Lost connection to MySQL server during query')")
            try:
                conn.ping()
            except:
                conn()
            sql = """DELETE FROM dede_arctiny WHERE id = {}""".format(aid)
            cursor.execute(sql)
            conn.commit()
        except Exception as e:
            traceback.print_exc()
            print(e)
            try:
                conn.ping()
            except:
                conn()
            sql = """DELETE FROM dede_arctiny WHERE id = {}""".format(aid)
            cursor.execute(sql)
            conn.commit()
    except Exception as e:
        conn.rollback()
        try:
            print(item)
        except:
            pass
        err = ["[插入失败]", e]
        print(err)
        with open('error.txt', 'a') as f:
            f.write(item["url"])
            f.write('\r\n')
    # conn.close()
    # cursor.close()
    return item


def save_db(item):
    # mysql = pymysql.connect(host='47.92.73.25', user='duxie', passwd='jtkpwangluo.com', port=7306,db='ytb')
    # mysql = pymysql.connect(host='localhost', user='root', passwd='123456', port=3306, db='local')
    if tool.removal(item['title'], item['zhao_time']):
        print("打开mysql")
        try:
            conn.ping()
        except:
            conn()
        item['title'] = item['title'].replace(' ', '')
        entry_name = mc_matching_title(item['title'])
        type_id = item['typeid'][0]
        item['typeid'] = [str(i) for i in item['typeid']]
        item['typeid'] = ','.join(item['typeid'])
        try:
            conn.ping()
        except:
            conn()
        sql = "insert into `dede_arctiny`(`typeid`, `senddate`, `mid`, `title`, `function`, `nativeplace`,`infotype`, `url`, `shi`,`sheng`, `entry_name`) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql, (
            item['typeid'], item['senddate'], item['mid'], item['title'], item['function'], item['nativeplace'],
            item['infotype'], item['info_url'], item['shi'], item['sheng'], entry_name))
        conn.commit()
        print("[dede_arctiny,插入成功]：", item['typeid'], item['title'])
        aid = cursor.lastrowid
        try:
            conn.ping()
        except:
            conn()
        sqlstr = "insert into `{}`(`aid`, `typeid`, `mid` ,`click`,`title`, `body`, `senddate`, `nativeplace`, `infotype`,`endtime`,`tel`,`email`,`address`,`linkman`, `function`,`url`, `resource`, `sheng`,`shi`)values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        if type_id in [16, 13, 77, 76, 73, 65, 64, 63, 74, 75, 19, 18, 17, 131, 132, 133, 134, 135, 136, 137, 138,
                       139, 140,
                       141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158,
                       159, 160, 161, 162,
                       163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180,
                       181, 182, 183, 184, 185,
                       186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203,
                       204, 205, 206, 207,
                       208, 209, 210, 211, 212, 213, 214, 215, 216, 217, 218, 219, 220]:  # 施工总承包
            db = "dede_addoninfos1"

        elif type_id in [21, 22, 80, 38, 37, 36, 35, 34, 33, 32, 31, 30, 29, 28, 27, 26, 25, 24, 87, 23]:  # 工程设计
            db = "dede_addoninfos2"

        elif type_id in [39, 40, 51, 50, 49, 48, 47, 46, 45, 44, 43, 42, 41, 86]:  # 施工劳务
            db = "dede_addoninfos3"
        elif type_id in [69, 70, 78, 90, 91, 92, 67, 71, 83, 84, 15, 66, 91, 90, 84, 83, 78, 71, 70, 69, 68, 67,
                         92, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119,
                         120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 68]:  # 专业承包
            db = "dede_addoninfos4"
        elif type_id in [14, 52, 89, 60, 59, 58, 57, 56, 55, 54, 53, 93]:  # 工程监理
            db = "dede_addoninfos5"
        elif type_id == 20:  # 招标变更
            db = "dede_addoninfos6"
        elif type_id == 72:  # 材料采购
            db = "dede_addoninfos7"
        elif type_id == 81:  # 工程造价
            db = "dede_addoninfos8"
        else:
            db = "dede_addoninfos9"  # 土地规划
        sql2 = sqlstr.format(db)
        try:
            try:
                conn.ping()
            except:
                conn()
            cursor.execute(sql2, (
                aid, item['typeid'], item['mid'], item['click'], item['title'], item['body'], item['senddate'],
                item['nativeplace'], item['infotype'], item['endtime'], item['tel'], item['email'],
                item['address'], item['linkman'], item['function'], item['info_url'], item['resource'],
                item['sheng'], item['shi']))
            conn.commit()
            print(db + ",[插入成功]：", item['typeid'], item['title'])
            print("-" * 100)
        except pymysql.err.OperationalError:
            print("pymysql.err.OperationalError: (2013, 'Lost connection to MySQL server during query')")
            try:
                conn.ping()
            except:
                conn()
            sql = """DELETE FROM dede_arctiny WHERE id = {}""".format(aid)
            cursor.execute(sql)
            conn.commit()
        except Exception as e:
            traceback.print_exc()
            print(e)
            sql = """DELETE FROM dede_arctiny WHERE id = {}""".format(aid)
            cursor.execute(sql)
            conn.commit()
        # conn.close()
        # cursor.close()
    else:
        print("该内容已存在，" + item['info_url'])
# conn.close()
# cursor.close()
if __name__ == '__main__':

    item={'title': '【中标公告】镇江市第一人民医院口腔3合1摄片设备采购中标结果公告', 'url': 'http://www.ggzy.gov.cn/information/html/b/320000/0202/202306/20/003203378569e09d45c992b1c41ad558b612.shtml', 'date': '2023-06-20', 'typeid': '72', 'senddate': 1687249377, 'mid': 867, 'nativeplace': '5511.001', 'infotype': 2000, 'body': '<div id="mycontent">\n<div class="detail_content"><meta http-equiv="X-UA-Compatible" content="IE=edge"> <style tyle="text/css"> .title{ text-align:left; font-size:14pt; } .title1{ text-align:left; font-size:14pt; } .content{ text-align:left; font-size:14pt; } .content1{ align:right; font-size:14pt; } .tablep{ text-align:left; font-size:14pt; border-collapse:collapse } </style> <br> <br> <table  style="line-height: 1.5; font-family: " font-size: border="0" cellpadding="10"> <tbody> <tr> <td colspan="3"> <div class="title">一、项目编号：<u>ZJZCFSDZ-(2023)公字第0090号</u></div> </td> </tr> <tr> <td colspan="3"> <div class="title">二、项目名称：<u> 镇江市第一人民医院口腔3合1摄片设备采购 </u></div> </td> </tr> <tr> <td colspan="3"> <div class="title">三、中标（成交）信息</div> </td> </tr> <tr> <td colspan="3"> <div class="content"> 供应商名称：<u> 镇江京丹医疗器械有限公司 </u><br> </div> </td> </tr> <tr> <td colspan="3"> <div class="content"> 供应商地址：<u> 镇江市京口区谷阳路199号沃得雅苑2-104 </u><br> </div> </td> </tr> <tr> <td colspan="3"> <div class="content"> 中标金额：<u> 480000.00(元) </u><br> </div> </td> </tr> <tr> <td colspan="3"> <div class="title">四、主要标的信息</div> </td> </tr> <tr> <td colspan="3"> <div class="title1">货物类标的</div> </td> </tr> <tr> <td> <table  class="tablep" border="1" cellspacing="0" cellpadding="10"> <tbody> <tr> <td>名称</td> <td>品牌</td> <td>规格型号</td> <td>数量</td> <td>单价</td> </tr> <tr> <td>镇江市第一人民医院口腔3合1摄片设备采购</td> <td>美亚光电</td> <td>SS-X9010Dpro-3DE</td> <td>1</td> <td>480000.0</td> </tr> </tbody> </table> </td> </tr> <tr> <td colspan="3"> <div class="title">五、评审专家（单一来源采购人员）名单：<u> 韦孔明;秦芳;朱镇;薛国庆;张光建; </u></div> </td> </tr> <tr> <td colspan="3"> <div class="title">六、代理服务收费标准及金额：<u> 2450.00 </u></div> </td> </tr> <tr> <td colspan="3"> <div class="title">七、公告期限</div> </td> </tr> <tr> <td colspan="3"> <div class="content"> 自本公告发布之日起1个工作日。<br> </div> </td> </tr> <tr> <td colspan="3"> <div class="title">八、其他补充事宜</div> </td> </tr> <tr> <td> <table  class="tablep" border="1" cellspacing="0" cellpadding="10"> <tbody> <tr> <td>供应商名称</td> <td>得分</td> <td>排名</td> </tr> <tr> <td>镇江京丹医疗器械有限公司</td> <td>92.6</td> <td>1</td> </tr> <tr> <td>镇江纬凡医疗器械有限公司</td> <td>77.63</td> <td>2</td> </tr> <tr> <td>无锡国耀众康商贸有限公司</td> <td>77.38</td> <td>3</td> </tr> </tbody> </table> </td> </tr> <tr> <td colspan="3"> <div class="content"> 无<br> </div> </td> </tr> <tr> <td colspan="3"> <div class="title">九、凡对本次公告内容提出询问，请按以下方式联系。</div> </td> </tr> <tr> <td colspan="3"> <div class="content"> 1.采购人信息<br> </div> </td> </tr> <tr> <td colspan="3"> <div class="content"> 名称：<u> 镇江市第一人民医院 </u><br> </div> </td> </tr> <tr> <td colspan="3"> <div class="content"> 地址：<u> 镇江市润州区电力路8号 </u><br> </div> </td> </tr> <tr> <td colspan="3"> <div class="content"> 联系方式：<u> 0511-88917939 </u><br> </div> </td> </tr> <tr> <td colspan="3"> <div class="content"> 2.采购代理机构信息 <br> </div> </td> </tr> <tr> <td colspan="3"> <div class="content"> 名称：<u> 苏世建设管理集团有限公司 </u><br> </div> </td> </tr> <tr> <td colspan="3"> <div class="content"> 地址：<u> 镇江市运河路21号1幢301室 </u><br> </div> </td> </tr> <tr> <td colspan="3"> <div class="content"> 联系方式：<u> 0511-88833166 </u><br> </div> </td> </tr> <tr> <td colspan="3"> <div class="content"> 3.项目联系方式 <br> </div> </td> </tr> <tr> <td colspan="3"> <div class="content"> 项目联系人：<u> 袁工 </u><br> </div> </td> </tr> <tr> <td colspan="3"> <div class="content"> 电\u3000话：<u> 13052901388 </u><br> </div> </td> </tr> </tbody> </table> <div align="right"><span style="font-size: 14pt;">苏世建设管理集团有限公司</span></div> <div align="right"><span style="font-size: 14pt;">2023年06月20日</span></div></div>\n</div>\n', 'endtime': 1687190400, 'tel': '', 'email': '', 'address': '镇江市运河路21号1幢301室', 'linkman': '袁工', 'function': 0, 'resource': '全国公共资源交易平台', 'shi': 5511, 'sheng': 5500, 'removal': '【中标公告】镇江市第一人民医院口腔3合1摄片设备采购中标结果公告'}

    # process_item(item)