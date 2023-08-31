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
    # time.sleep(1)
    print('item',item)
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
            print(sql2)
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
            print(sql2)
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
    # ss=pymysql.connect(host='47.92.73.25', user='duxie', passwd='jtkpwangluo.com', port=3306, db='ytb')
    # print(ss.ping())
    item={'title': '建胜镇龙桥花苑小区四、五组团屋面渗水整改结果公告','url': 'https://www.gec123.com/notices/detail/1271127698445602816', 'date': 1692945128000, 'typeid': [13, 66],'senddate': 1693210392, 'mid': 867, 'nativeplace': 0, 'infotype': 2000,'body': '<style type="text/css">\r\n        h4{\r\n            font-size: 24px;\r\n        }\r\n        p{\r\n            margin: 0 20px 10px ;\r\n            font-size: 18px;\r\n        }\r\n    </style>\r\n    \t\t\t\t\t\r\n\t\t\t\t\t<div class="wrap-post" >\r\n\r\n  <h3 id = "titlecandel" style="text-align: center;">建胜镇龙桥花苑小区四、五组团屋面渗水整改结果公告\r\n    \r\n    </h3>\r\n         <h3 id = "datecandel" style="text-align:center;font-size:16px;font-weight:100">发布日期： 2023年8月25日</h3>\r\n      \r\n    <h4>一、采购方式：<span style="font-size:18px">竞争性比选</span> \r\n    </h4>\r\n    <h4>二、评审日期：<span style="font-size:18px"> 2023年8月24日</span> </h4>\r\n    <h4 style="margin-bottom:-10px">三、公告日期：<span style="font-size:18px"> 2023年8月25日</span> </h4>\r\n    <br/>\r\n       \t \t   \t \t    \t\t<h4>四、结果</h4>\r\n    \t   \t \t                     <div class="panel panel-danger">\r\n        <div class="panel-heading">分包号：1</div>\r\n                <table class="table">\r\n           <th  style="font-sie:18px;!important;font-weight:100;text-align: center;width:30%">分包内容</th>\r\n            <th style="font-sie:18px;!important;font-weight:100;text-align: center;width:10%">金额（元）</th>\r\n            <th style="font-sie:18px;!important;font-weight:100;text-align: center;width:10%">成交供应商</th>\r\n            <th style="font-sie:18px;!important;font-weight:100;text-align: center;width:10%">地址</th>\r\n            <th style="font-sie:18px;!important;font-weight:100;text-align: center;width:20%">单价、数量及规格型号</th>\r\n            <th  style="font-sie:18px;!important;font-weight:100;text-align: center;width:20%">其他要求</th>\r\n                         <tr>\r\n                <td  style="font-sie:18px;!important;font-weight:100;text-align: center;vertical-align: middle">建胜镇龙桥花苑小区四、五组团屋面渗水整改</td>\r\n                 <td style="font-sie:18px;!important;font-weight:100;text-align: center;color:red;vertical-align: middle" >869,799.60</td>\r\n                <td style="font-sie:18px;!important;font-weight:100;text-align: center;vertical-align: middle">重庆全成晟建设工程有限公司</td>\r\n                <td style="font-sie:18px;!important;font-weight:100;text-align: center;vertical-align: middle" class="price">重庆市垫江县大石乡人民政府1楼108号</td>\r\n                <td style="font-sie:18px;!important;font-weight:100;text-align: center;vertical-align: middle">\r\n                单价：869,799.60                <br>数量：1.0                <br>规格型号：详见竞争性比选文件               </td>\r\n                <td style="font-sie:18px;!important;font-weight:100;text-align: center;vertical-align: middle">详见竞争性比选文件</td>\r\n            </tr>\r\n                    </table>\r\n           </div>\r\n             \r\n       \r\n\r\n    \r\n        <h4>五、评审小组成员名单</h4>\r\n   \r\n   <p>梁宾 、欧娟 、王德智</p>\r\n\t\t\r\n        \r\n \t\t\r\n\t\r\n\t\r\n\t\r\n        <h4>六、联系人</h4>\r\n    \t\r\n         <p>采购人：重庆市大渡口区建胜镇回龙桥社区居民委员会</p>\r\n    <p>采购经办人：顾老师</p>\r\n    <p>采购人电话：023-68083816</p>\r\n        <p>采购人地址：重庆市大渡口区建胜镇回龙桥社区</p>\r\n        \r\n     \t\r\n    <p>代理机构：重庆佳德工程项目管理有限公司</p>    <p>代理机构经办人：王老师</p>    <p>代理机构电话：023-67885486</p>        <p>代理机构地址：重庆市两江新区栖霞路4幢1单元18楼</p> \t   \r\n        \r\n     <div style="margin-bottom: 20px">\r\n        <hr style="background-color: #ddd;height: 1px">\r\n        <h3 style="display: inline-block">免责声明：</h3>\r\n        <span style="font-size:18px;">采购人在本页面发布的任何信息应当真实、有效、完整，并对发布的信息承担相应法律责任。</span>\r\n        <hr style="background-color:#ddd;height: 1px">\r\n    </div>\r\n\t\r\n   \r\n\r\n</div>\r\n\r\n\r\n\r\n\r\n','endtime': 1692945128, 'tel': '023-67885486', 'email': '', 'address': '重庆市两江新区栖霞路4幢1单元18楼</p>','linkman': '', 'function': 0, 'resource': '行采家', 'shi': 0, 'sheng': 0,'removal': '建胜镇龙桥花苑小区四、五组团屋面渗水整改结果公告', 'winner': ''}

