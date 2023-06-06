# -*- coding: utf-8 -*-
import time, re
import pymysql, tool
import random, traceback

# 保存招投标信息
conn = pymysql.connect(host='47.92.73.25', user='python', passwd='Kp123...', port=3306, db='yqc')
# conn = pymysql.connect(host='127.0.0.1', port=3306, db="uther_test", user='root', password='root', charset="utf8")
cursor=conn.cursor()


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

def search_title(title):
    sql = f"select * from yunqi_ztb where title ='{title}'"
    cursor.execute(sql)
    data=cursor.fetchone()
    return data



def process_item(item):
    time.sleep(1)
    print('item',item)
    try:
        if '测试' in item['title']:
            print('测试数据', item['url'])
            return True
        title=item['title']
        if search_title(title):
            print(f'mysql {title} exist')
        else:
            try:
                conn.ping()
            except:
                conn()

            sql = "insert into " \
                  "yunqi_ztb(mid ,title, senddate, nativeplace, infotype, body, endtime, tel, email, address, linkman,function, url, resource, click,shi,sheng,gl)" \
                  "values " \
                  "(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sql, (item["mid"], item["title"],
                    item["senddate"], item["nativeplace"], item["infotype"], item["body"], item["endtime"],
                    item["tel"],item["email"],item["address"], item["linkman"], item["function"], item["url"],
                    item["resource"], random.randint(500, 1000), item["shi"], item["sheng"],item["winner"]))
            conn.commit()
            # redis_save(item)
            print("[插入成功]", item["mid"], item["title"],
                      item["senddate"], item["nativeplace"], item["date"], item["infotype"],item["endtime"], item["tel"],
                  item["email"],item["address"], item["linkman"], item["function"], item["url"],item["resource"])
            print("-" * 100)
            time.sleep(4)
    # except pymysql.err.OperationalError:
    #     print("pymysql.err.OperationalError: (2013, 'Lost connection to MySQL server during query')")

    except Exception as e:
        traceback.print_exc()
    # conn.close()
    # cursor.close()
    return item


def save_db(item):
    # mysql = pymysql.connect(host='47.92.73.25', user='duxie', passwd='jtkpwangluo.com', port=7306,db='ytb')
    # mysql = pymysql.connect(host='localhost', user='root', passwd='123456', port=3306, db='local')
    # if tool.removal(item['title'], item['zhao_time']):
    #     print("打开mysql")
        item['title'] = item['title'].replace(' ', '')
        # item['typeid'] = [str(i) for i in item['typeid']]
        # item['typeid'] = ','.join(item['typeid'])
        sql = "insert into yunqi_ztb(`mid` ,`click`,`title`, `body`, `senddate`, `nativeplace`, `infotype`,`endtime`,`tel`,`email`,`address`,`linkman`, `function`,`url`, `resource`, `sheng`,`shi`)values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        try:
            try:
                conn.ping()
            except:
                conn()
            cursor.execute(sql, (
                item['mid'], item['click'], item['title'], item['body'], item['senddate'],
                item['nativeplace'], item['endtime'], item['tel'], item['email'],
                item['address'], item['linkman'], item['function'], item['info_url'], item['resource'],
                item['sheng'], item['shi']))
            conn.commit()
            print( ",[插入成功]：", item['title'])
            print("-" * 100)

        except Exception as e:
            traceback.print_exc()

        # conn.close()
        # cursor.close()
# conn.close()
# cursor.close()
if __name__ == '__main__':

    item=[
    {'title': '福建省宁化县隆陂水库引调水工程施工监理', 'url': 'http://smggzy.sm.gov.cn/smwz/InfoDetail/?InfoID=a75f2a1f-1493-41b9-a37e-6168c5cdfef5&CategoryNum=022001005', 'date': '2019-03-25', 'typeid': [14,87,84], 'senddate': 1680863562, 'mid': 867, 'nativeplace': 7004.005, 'infotype': 2001, 'body': '<div class="ewb-show-con" id="mainContent">\r\n                    <!--EpointContent-->\r\n                    <p align="center" style=\'margin: 0cm -19.65pt 0pt 0cm; text-align: center; line-height: 19.5pt; font-family: "Times New Roman","serif"; font-size: 10.5pt; -ms-text-justify: inter-ideograph;\'><span><b><span style="font-family: 宋体; font-size: 16pt;">福建省宁化县隆陂水库引调水工</span></b></span><span><b><span style="font-family: 宋体; font-size: 16pt;">程施工监理</span></b></span></p>\n<p align="center" style=\'margin: 0cm -19.65pt 0pt 0cm; text-align: center; line-height: 19.5pt; font-family: "Times New Roman","serif"; font-size: 10.5pt; -ms-text-justify: inter-ideograph;\'><span><b><span style="font-family: 宋体; font-size: 16pt;">中标结果公告</span></b></span></p>\n<p style=\'margin: 0cm 0cm 0pt; text-align: justify; line-height: 19.5pt; text-indent: 32pt; font-family: "Times New Roman","serif"; font-size: 10.5pt; -ms-text-justify: inter-ideograph;\'>\xa0</p>\n<p style=\'margin: 0cm 0cm 0pt; text-align: justify; line-height: 19.5pt; font-family: "Times New Roman","serif"; font-size: 10.5pt; -ms-text-justify: inter-ideograph;\'><span><b><span style="font-size: 12pt;"><span>\xa0\xa0\xa0\xa0\xa0\xa0\xa0 </span></span></b></span><span><span><b><u><span style="font-family: 宋体; font-size: 12pt;">福建平诚工程造价咨询有限公司</span></u></b></span></span><span><span style="font-family: 宋体; font-size: 12pt;">受<b><u>宁化县翠城水务有限公司</u></b>的委托，对<b><u>福建省宁化县隆陂水库引调水工程施工监理</u></b>进行公开招标，本项目于</span></span><span><b><span style="font-size: 12pt;">2019</span></b></span><span><b><span style="font-family: 宋体; font-size: 12pt;">年</span></b></span><span><b><span style="font-size: 12pt;">3</span></b></span><span><b><span style="font-family: 宋体; font-size: 12pt;">月</span></b></span><span><b><span style="font-size: 12pt;">20</span></b></span><span><b><span style="font-family: 宋体; font-size: 12pt;">日</span></b></span><span style="font-family: 宋体; font-size: 12pt;">开标、评标，开评标会结束后根据有关法律、法规要求，对中标候选人进行公示，公示期为</span><span style="font-size: 12pt;">2019</span><span style="font-family: 宋体; font-size: 12pt;">年</span><span style="font-size: 12pt;">3</span><span style="font-family: 宋体; font-size: 12pt;">月</span><span style="font-size: 12pt;">20</span><span style="font-family: 宋体; font-size: 12pt;">日至</span><span style="font-size: 12pt;">2019</span><span style="font-family: 宋体; font-size: 12pt;">年</span><span style="font-size: 12pt;">3</span><span style="font-family: 宋体; font-size: 12pt;">月</span><span style="font-size: 12pt;">23</span><span style="font-family: 宋体; font-size: 12pt;">日，在公示期间，未收到各投标单位对本次招标候选人提出复议的书面材料，本司将中标结果公告在福建省公共资源交易电子公共服务平台及三明市公共资源交易中心电子交易平台发布，相关事项如下：</span></p>\n<p style=\'margin: 0cm 0cm 0pt; text-align: justify; line-height: 19.5pt; font-family: "Times New Roman","serif"; font-size: 10.5pt; -ms-text-justify: inter-ideograph;\'><span style="font-family: 宋体; font-size: 12pt;">一、项目概况</span><span style="font-size: 12pt;"> </span></p>\n<p style=\'margin: 0cm 0cm 0pt; text-align: justify; line-height: 19.5pt; text-indent: 24pt; font-family: "Times New Roman","serif"; font-size: 10.5pt; -ms-text-justify: inter-ideograph;\'><span><span style="font-family: 宋体; font-size: 12pt;">招标项目名称：<span>福建省宁化县隆陂水库引调水工程施工监理</span></span></span></p>\n<p style=\'margin: 0cm 0cm 0pt; text-align: justify; line-height: 19.5pt; text-indent: 24pt; font-family: "Times New Roman","serif"; font-size: 10.5pt; -ms-text-justify: inter-ideograph;\'><span><span style="font-family: 宋体; font-size: 12pt;">招标人：<span>宁化县翠城水务有限公司</span></span></span></p>\n<p style=\'margin: 0cm 0cm 0pt; text-align: justify; line-height: 19.5pt; text-indent: 24pt; font-family: "Times New Roman","serif"; font-size: 10.5pt; -ms-text-justify: inter-ideograph;\'><span style="font-family: 宋体; font-size: 12pt;">招标方式</span><span style="font-size: 12pt;">: </span><span style="font-family: 宋体; font-size: 12pt;">公开招标</span></p>\n<p style=\'margin: 0cm 0cm 0pt; text-align: justify; line-height: 19.5pt; font-family: "Times New Roman","serif"; font-size: 10.5pt; -ms-text-justify: inter-ideograph;\'><span style="font-family: 宋体; font-size: 12pt;">二、中标人名称及相关内容：</span></p>\n<p style=\'margin: 0cm 0cm 0pt; text-align: justify; line-height: 19.5pt; text-indent: 24pt; font-family: "Times New Roman","serif"; font-size: 10.5pt; -ms-text-justify: inter-ideograph;\'><span style="font-family: 宋体; font-size: 12pt;">中标人：三明市联盛工程咨询监理有限公司；中标价：</span><span style="font-size: 12pt;">618968</span><span style="font-family: 宋体; font-size: 12pt;">元；</span></p>\n<p style=\'margin: 0cm 0cm 0pt; text-align: justify; line-height: 19.5pt; font-family: "Times New Roman","serif"; font-size: 10.5pt; -ms-text-justify: inter-ideograph;\'><span><span style="font-family: 宋体; font-size: 12pt;">三、确定为废标的投标人名称及原因：<u>无</u></span></span></p>\n<p style=\'margin: 0cm 0cm 0pt; text-align: justify; line-height: 19.5pt; font-family: "Times New Roman","serif"; font-size: 10.5pt; -ms-text-justify: inter-ideograph;\'><span style="font-family: 宋体; font-size: 12pt;">四、中标结果公示期：</span><span style="font-size: 12pt;">2019</span><span style="font-family: 宋体; font-size: 12pt;">年</span><span style="font-size: 12pt;">3</span><span style="font-family: 宋体; font-size: 12pt;">月</span><span style="font-size: 12pt;">25</span><span style="font-family: 宋体; font-size: 12pt;">日至</span><span style="font-size: 12pt;">2019</span><span style="font-family: 宋体; font-size: 12pt;">年</span><span style="font-size: 12pt;">4</span><span style="font-family: 宋体; font-size: 12pt;">月</span><span style="font-size: 12pt;">3</span><span style="font-family: 宋体; font-size: 12pt;">日</span></p>\n<p style=\'margin: 0cm 0cm 0pt; text-align: justify; line-height: 19.5pt; font-family: "Times New Roman","serif"; font-size: 10.5pt; -ms-text-justify: inter-ideograph;\'><span style="font-family: 宋体; font-size: 12pt;">五、联系方式</span></p>\n<p style=\'margin: 0cm 0cm 0pt; text-align: justify; line-height: 19.5pt; text-indent: 24pt; font-family: "Times New Roman","serif"; font-size: 10.5pt; -ms-text-justify: inter-ideograph;\'><span><span style="font-family: 宋体; font-size: 12pt;">招标单位名称：<span>宁化县翠城水务有限公司</span></span></span></p>\n<p style=\'margin: 0cm 0cm 0pt; text-align: justify; line-height: 19.5pt; text-indent: 24pt; font-family: "Times New Roman","serif"; font-size: 10.5pt; -ms-text-justify: inter-ideograph;\'><span style="font-family: 宋体; font-size: 12pt;">地</span><span><span style="font-size: 12pt;"> <span>\xa0\xa0\xa0\xa0</span></span></span><span style="font-family: 宋体; font-size: 12pt;">址：宁化县翠江镇财富源附属四楼</span></p>\n<p style=\'margin: 0cm 0cm 0pt; text-align: justify; line-height: 19.5pt; text-indent: 24pt; font-family: "Times New Roman","serif"; font-size: 10.5pt; -ms-text-justify: inter-ideograph;\'><span style="font-family: 宋体; font-size: 12pt;">联系人：</span><span style="font-size: 12pt;">\xa0</span><span style="font-family: 宋体; font-size: 12pt;">罗先生</span><span style="font-family: 宋体; font-size: 12pt;">电话：</span><span style="font-size: 12pt;">0598-6666116</span></p>\n<p style=\'margin: 0cm 0cm 0pt; text-align: justify; line-height: 19.5pt; font-family: "Times New Roman","serif"; font-size: 10.5pt; -ms-text-justify: inter-ideograph;\'>\xa0</p>\n<p style=\'margin: 0cm 0cm 0pt; text-align: justify; line-height: 19.5pt; text-indent: 24pt; font-family: "Times New Roman","serif"; font-size: 10.5pt; -ms-text-justify: inter-ideograph;\'><span style="font-family: 宋体; font-size: 12pt;">招标代理机构：</span><span style="font-family: 宋体; font-size: 12pt;">福建平诚工程造价咨询有限公司</span><span><span style="font-family: 宋体; font-size: 12pt;"><span>\xa0\xa0\xa0\xa0 </span></span></span></p>\n<p align="left" style=\'margin: 0cm 0cm 0pt; text-align: left; line-height: 19.5pt; text-indent: 23.5pt; font-family: "Times New Roman","serif"; font-size: 10.5pt; -ms-text-justify: inter-ideograph; tab-stops: 25.5pt 45.0pt 55.0pt;\'><span><span style="font-family: 宋体; font-size: 12pt;">电话：<span>15280235085</span></span></span></p>\n<p style=\'margin: 0cm 0cm 0pt; text-align: justify; line-height: 19.5pt; text-indent: 24pt; font-family: "Times New Roman","serif"; font-size: 10.5pt; -ms-layout-grid-mode: char; -ms-text-justify: inter-ideograph;\'><span><span style="font-family: 宋体; font-size: 12pt;">联系人：<span>王先生<b><u> </u></b></span></span></span></p>\n<p style=\'margin: 0cm 0cm 0pt; text-align: justify; line-height: 19.5pt; font-family: "Times New Roman","serif"; font-size: 10.5pt; -ms-text-justify: inter-ideograph;\'>\xa0</p>\n<p style=\'margin: 0cm 0cm 0pt; text-align: justify; line-height: 19.5pt; font-family: "Times New Roman","serif"; font-size: 10.5pt; -ms-text-justify: inter-ideograph;\'><span style="font-family: 宋体; font-size: 12pt;">六、监督单位及电话：</span></p>\n<p style=\'margin: 0cm 0cm 0pt; text-align: justify; line-height: 19.5pt; text-indent: 21.25pt; font-family: "Times New Roman","serif"; font-size: 10.5pt; -ms-text-justify: inter-ideograph;\'><span style="font-family: 宋体; font-size: 12pt;">招投标监督机构名称：宁化县水利局</span></p>\n<p style=\'margin: 0cm 0cm 0pt; text-align: justify; line-height: 19.5pt; text-indent: 21.25pt; font-family: "Times New Roman","serif"; font-size: 10.5pt; -ms-text-justify: inter-ideograph;\'><span style="font-family: 宋体; font-size: 12pt;">联系电话：</span><span style="font-size: 12pt;">0598-6822578</span></p>\n<p style=\'margin: 0cm 0cm 0pt; text-align: justify; line-height: 19.5pt; font-family: "Times New Roman","serif"; font-size: 10.5pt; -ms-text-justify: inter-ideograph;\'><span><u><span style="font-size: 12pt;"><p><span style="text-decoration: none;"><br>\n</span></p></span></u></span></p>\n<p style=\'margin: 0cm 0cm 0pt; text-align: justify; line-height: 19.5pt; text-indent: 24pt; font-family: "Times New Roman","serif"; font-size: 10.5pt; -ms-text-justify: inter-ideograph;\'><span style="font-family: 宋体; font-size: 12pt;">本项目中标结果现予以公示，接受社会监督，公示期内，投标人和其他利害关系人有权向招标人提出疑义或可按《工程建设项目招标投标活动投诉处理办法》（七部委第</span><span style="font-size: 12pt;">11</span><span style="font-family: 宋体; font-size: 12pt;">号令）的相关规定向监管该项目的招投标监督机构进行投诉。</span></p>\n<p style=\'margin: 0cm 0cm 0pt; text-align: justify; line-height: 19.5pt; text-indent: 24pt; font-family: "Times New Roman","serif"; font-size: 10.5pt; -ms-text-justify: inter-ideograph;\'>\xa0</p>\n<p style=\'margin: 0cm 0cm 0pt; text-align: justify; line-height: 19.5pt; text-indent: 24pt; font-family: "Times New Roman","serif"; font-size: 10.5pt; -ms-text-justify: inter-ideograph;\'><span><span style="font-size: 12pt;"><span>\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0 </span>2019</span></span><span style="font-family: 宋体; font-size: 12pt;">年</span><span style="font-size: 12pt;">3</span><span style="font-family: 宋体; font-size: 12pt;">月</span><span style="font-size: 12pt;">25</span><span style="font-family: 宋体; font-size: 12pt;">日</span><span><b><span style="font-size: 16pt;"><span>\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0 </span></span></b></span></p>\r\n                    <!--EpointContent-->\r\n            </div>\r\n            ', 'endtime': 1554220800, 'tel': '0598-6822578', 'email': '', 'winner': ['三明市联盛工程咨询监理有限公司'], 'address': '宁化县翠江镇财富源附属四楼', 'linkman': '罗先生', 'function': 0, 'resource': '三明市公共资源交易网', 'shi': 7004, 'sheng': 7000, 'removal': '福建省宁化县隆陂水库引调水工程施工监理[中标公示]'},
    {'title': '明溪县明源水厂及渔塘溪生态水系综合治理工程监理招标异常公告','url': 'http://smggzy.sm.gov.cn/smwz/InfoDetail/?InfoID=1de65976-c03d-41db-8deb-c450bf546e6a&CategoryNum=022001005','date': '2019-03-29', 'typeid': [14], 'senddate': 1680863556, 'mid': 867, 'nativeplace': 7004.003,'infotype': 1501,'body': '<div class="ewb-show-con" id="mainContent">\r\n                    <!--EpointContent-->\r\n                    <p align="center" style=\'margin: 0cm 0cm 10pt; text-align: center; font-family: "Tahoma","sans-serif"; font-size: 11pt; -ms-layout-grid-mode: char;\'><span style=\'background: white; font-family: "微软雅黑","sans-serif"; font-size: 14pt;\'>明溪县明源水厂及渔塘溪生态水系综合治理工程监理</span></p>\r\n<p align="center" style=\'margin: 0cm 0cm 10pt; text-align: center; font-family: "Tahoma","sans-serif"; font-size: 11pt; -ms-layout-grid-mode: char;\'><span style=\'font-family: "微软雅黑","sans-serif"; font-size: 14pt;\'>流标公示</span></p>\r\n<p style="background: white; margin: 0cm 0cm 0pt 37.5pt; line-height: 20.25pt; font-family: 宋体; font-size: 12pt;"><span style="font-size: 15pt;">\xa0</span></p>\r\n<p align="right" style="background: white; margin: 0cm 0cm 0pt; text-align: right; line-height: 20.25pt; font-family: 宋体; font-size: 12pt;"><span>招标编号<span>:</span></span><span style="background: white; color: blue; font-size: 14pt;"> </span><span>E3504210401100022001</span><span>\xa0</span></p>\r\n<p style="background: white; margin: 0cm 0cm 0pt; line-height: 21.75pt; text-indent: 24pt; font-family: 宋体; font-size: 12pt;"><strong><span style="font-family: 宋体;">1</span></strong><strong><span style="font-family: 宋体;">、招标工程项目概况</span></strong></p>\r\n<p style="background: white; margin: 0cm 0cm 0pt; line-height: 21.75pt; text-indent: 24pt; font-family: 宋体; font-size: 12pt;"><span>工程项目名称：<u>明溪县明源水厂及渔塘溪生态水系综合治理工程监理</u></span></p>\r\n<p style="background: white; margin: 0cm 0cm 0pt; line-height: 21.75pt; text-indent: 24pt; font-family: 宋体; font-size: 12pt;"><span>招标人：<u><span>\xa0</span>福建省明溪县珩城水业有限公司</u></span></p>\r\n<p style="background: white; margin: 0cm 0cm 0pt; line-height: 21.75pt; text-indent: 24pt; font-family: 宋体; font-size: 12pt;"><span>招标方式<span>:<u>\xa0</u></span><u>公开招标<span>\xa0</span></u></span></p>\r\n<p style="background: white; margin: 0cm 0cm 0pt; line-height: 21.75pt; text-indent: 24pt; font-family: 宋体; font-size: 12pt;"><b><span>2</span></b><b><span>、<strong><span style="font-family: 宋体;">招标失败原因</span></strong></span></b></p>\r\n<p style="background: white; margin: 0cm 0cm 0pt; line-height: 21.75pt; text-indent: 24pt; font-family: 宋体; font-size: 12pt;"><span>本招标项目投标截止时间为<u><span>2019</span></u>年<u><span>3</span></u>月<u><span>29</span></u>日<u><span>9</span>时<span>00</span></u>分，投标截止时递交投标文件的投标人少于<span>3</span>个。</span></p>\r\n<p style="background: white; margin: 0cm 0cm 0pt; line-height: 21.75pt; text-indent: 24pt; font-family: 宋体; font-size: 12pt;"><strong><span style="font-family: 宋体;">3</span></strong><strong><span style="font-family: 宋体;">、公示时间</span></strong></p>\r\n<p style="background: white; margin: 0cm 0cm 0pt; line-height: 21.75pt; text-indent: 24pt; font-family: 宋体; font-size: 12pt;"><span>公示期为<u><span>2019</span></u>年<u><span>3</span></u>月<u><span>29</span></u>日至<u><span>2019</span></u>年<u><span>4</span></u>月<u><span>1</span></u>日。</span></p>\r\n<p style="background: white; margin: 0cm 0cm 0pt; line-height: 21.75pt; text-indent: 24pt; font-family: 宋体; font-size: 12pt;"><strong><span style="font-family: 宋体;">4</span></strong><strong><span style="font-family: 宋体;">、联系方式</span></strong></p>\r\n<p style="background: white; margin: 0cm 0cm 0pt; line-height: 21.75pt; text-indent: 24pt; font-family: 宋体; font-size: 12pt;"><span>招标人：<u><span>\xa0</span>福建省明溪县珩城水业有限公司</u></span></p>\r\n<p style="background: white; margin: 0cm 0cm 0pt; line-height: 21.75pt; text-indent: 24pt; font-family: 宋体; font-size: 12pt;"><span>办公地址：<u><span>\xa0</span>雪峰镇青年路<span>688</span>号<span>\xa0</span></u></span></p>\r\n<p style="background: white; margin: 0cm 0cm 0pt; line-height: 21.75pt; text-indent: 24pt; font-family: 宋体; font-size: 12pt;"><span>邮政编码：<u><span>\xa0365200\xa0</span></u>，联系电话：<u><span>\xa018020853958\xa0</span></u></span></p>\r\n<p style="background: white; margin: 0cm 0cm 0pt; line-height: 21.75pt; text-indent: 24pt; font-family: 宋体; font-size: 12pt;"><span>联系人：<u><span>\xa0</span>梁先生<span>\xa0\xa0</span></u></span></p>\r\n<p style="background: white; margin: 0cm 0cm 0pt; line-height: 21.75pt; text-indent: 24pt; font-family: 宋体; font-size: 12pt;"><span>\xa0</span></p>\r\n<p style="background: white; margin: 0cm 0cm 0pt; line-height: 21.75pt; text-indent: 24pt; font-family: 宋体; font-size: 12pt;"><span>招标代理机构：<u><span>\xa0</span>福建平诚工程造价咨询有限公司<span>\xa0</span></u></span></p>\r\n<p style="background: white; margin: 0cm 0cm 0pt; line-height: 21.75pt; text-indent: 24pt; font-family: 宋体; font-size: 12pt;"><span>办公地址：<u><span>\xa0</span>三明市梅列区东新四路海峡银行十四楼<span>\xa0</span></u></span></p>\r\n<p style="background: white; margin: 0cm 0cm 0pt; line-height: 21.75pt; text-indent: 24pt; font-family: 宋体; font-size: 12pt;"><span>邮政编码：<u><span>\xa0366100\xa0</span></u>，联系电话：<u><span>\xa00598-6629809</span></u></span></p>\r\n<p style="background: white; margin: 0cm 0cm 0pt; line-height: 21.75pt; text-indent: 24pt; font-family: 宋体; font-size: 12pt;"><span>联系人：<u><span>\xa0</span>王先生<span>\xa0</span></u></span></p>\r\n<p style="background: white; margin: 0cm 0cm 0pt; line-height: 21.75pt; text-indent: 24pt; font-family: 宋体; font-size: 12pt;"><span>\xa0</span></p>\r\n<p style="background: white; margin: 0cm 0cm 0pt; line-height: 21.75pt; text-indent: 24pt; font-family: 宋体; font-size: 12pt;"><span>监督机构名称：<u><span>\xa0</span>明溪县住房和城乡规划建设局、明溪县水利局<span>\xa0</span></u></span></p>\r\n<p style="background: white; margin: 0cm 0cm 0pt; line-height: 21.75pt; text-indent: 24pt; font-family: 宋体; font-size: 12pt;"><span>办公地址：<u><span>\xa0</span>明溪县中山路<span>846</span>号、明溪县青年路<span>2</span>号<span>\xa0\xa0</span></u></span></p>\r\n<p style="background: white; margin: 0cm 0cm 0pt; line-height: 21.75pt; text-indent: 24pt; font-family: 宋体; font-size: 12pt;"><span>联系电话：<u><span>\xa00598-2818891</span><span>、<span>0598-2813540</span></span><span>\xa0</span></u></span></p>\r\n<p style="background: white; margin: 0cm 0cm 0pt; line-height: 21.75pt; text-indent: 24pt; font-family: 宋体; font-size: 12pt;"><span>\xa0</span></p>\r\n<p style="background: white; margin: 0cm 0cm 0pt; line-height: 21.75pt; text-indent: 246pt; font-family: 宋体; font-size: 12pt;"><span>日期：<u><span>2019</span></u>年<u><span>\xa03\xa0</span></u>月<u><span>\xa029\xa0</span></u>日</span></p>\r\n<p style=\'margin: 0cm 0cm 10pt; line-height: 11pt; font-family: "Tahoma","sans-serif"; font-size: 11pt; -ms-layout-grid-mode: char;\'>\xa0</p>\r\n                    <!--EpointContent-->\r\n            </div>\r\n            ','endtime': 1553788800, 'tel': '18020853958', 'email': '', 'winner': None, 'address': '', 'linkman': '','function': 0, 'resource': '三明市公共资源交易网', 'shi': 7004, 'sheng': 7000,'removal': '明溪县明源水厂及渔塘溪生态水系综合治理工程监理招标异常公告'},

    ]
    for i in item:

        process_item(i)