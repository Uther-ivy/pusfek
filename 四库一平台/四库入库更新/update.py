import json
import pymysql
import time
import re
import os
import logging
import traceback

db = pymysql.connect(
    host='localhost',
    port=3306,
    user='root',
    password='root',
    database='uther_test',
    charset='utf8'
)
fwqdb = pymysql.connect(
    host='47.92.73.25',
    port=3306,
    user='duxie',
    password='jtkpwangluo.com',
    database='yqc',
    charset='utf8'
)
def insertqr(aid,rid):
    cur = db.cursor()
    sql = "insert into " \
          "yunqi_qr(aid,rid) " \
          "values " \
          "(%s,%s);"
    cur.execute(sql, (aid, rid))
    xid = cur.lastrowid
    db.commit()
    cur.fetchone()
def insertqx(aid,xid):
    cur = db.cursor()
    sql = "insert into " \
          "yunqi_qx(aid,xid) " \
          "values " \
          "(%s,%s);"
    cur.execute(sql, (aid, xid))
    xid = cur.lastrowid
    db.commit()
    cur.fetchone()
def tate(name):
    try:
        pattern = '([0-9,?]+\.[0-9]+)'
        matches = re.search(pattern, name)
        return matches.group()
    except:
        return 0
def insertproject(title,linkman,pnumber,ztzmoney,sjxmnumber,zzjgdm,prjSize):
    cur = db.cursor()
    sql = "insert into " \
          "yunqi_addoninfos(title,linkman, pnumber, ztzmoney, sjxmnumber, zzjgdm, tarea,tzsbh) " \
          "values " \
          "(%s,%s,%s,%s,%s,%s,%s,%s);"
    print(prjSize)
    cur.execute(sql, (title, linkman, pnumber, ztzmoney, sjxmnumber, zzjgdm, prjSize,"''"))
    xid=cur.lastrowid
    db.commit()
    cur.fetchone()
    # print(xid)
    return xid

def project(data,aid):
   pro= data["project"]
   if pro is not None:
       for i in pro:
           j=i["prodetail"]
           if ("allInvest" in j):
               allInvest = j["allInvest"]
           else:
               allInvest = 0
           if ("buildCorpName" in j):
               buildCorpName = j["buildCorpName"]
           else:
               buildCorpName = ""
           if("buildCorpCode" in j):
               buildCorpCode=j["buildCorpCode"]
           else:
               buildCorpCode=""
           if("buildPlanNum" in j):
               buildPlanNum=j["buildPlanNum"]
           else:
               buildPlanNum=""
           if("allArea" in j):
               prjSize=j["allArea"]
           else:
               prjSize=0
           xid=insertproject(j["prjName"],buildCorpName,buildPlanNum,allInvest,j["provincePrjNum"],buildCorpCode,prjSize)
           insertqx(aid,xid)
def insertperson(name, sex, idcard, cardname, leixing, companyid, zsbh,zyyzh,yxq,typeid):

    cur = db.cursor()
    sql = "insert into " \
          "yunqi_addon18(name,sex, idcard, cardname, leixing, companyid, zsbh,zyyzh,yxq,typeid) " \
          "values " \
          "(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
    cur.execute(sql, (name, sex, idcard, cardname, leixing, companyid, zsbh,zyyzh,yxq,typeid))
    rid = cur.lastrowid
    db.commit()
    cur.fetchone()

    return rid
def person_type(name):
    try:
        return  yunqi_typeids[name] if yunqi_typeids[name] else 13
    except:
        return  13
def leixing(name):
    try:
        return json_data[name]
    except:
        return 0
def person(data,aid):
    regporson=data["regporson"];
    for i in regporson:
        reg_end = int(i["reg_end"])
        leix=leixing(i["zsdj"])
        typeid=int(person_type(i["zhtype"]))
        rid=insertperson(i["name"],i["sex"],1,i["sfz"],leix,i["gsname"],i["zsbh"],i["zyyz"],reg_end,int(typeid))
        insertqr(aid,rid)
#获取zzlb的号码 ，
def searchzzlb(zzmc):
    cur = fwqdb.cursor()
    sql = "select id from yunqi_addon17_zzlb where (pron=%s)"
    cur.execute(sql, zzmc)
    db.commit()
    # print(cur.fetchall())
    return cur.fetchone()

def insertzzlx(kid, zzlb, zzzsh, zzmc, fzrq, zsyxq, fzjg):
    cur = db.cursor()
    sql = "insert into " \
          "yunqi_addon17_zzlx(kid, zzlb, zzzsh, zzmc, fzrq, zsyxq, fzjg) " \
          "values " \
          "(%s,%s,%s,%s,%s,%s,%s);"
    cur.execute(sql, (kid, zzlb, zzzsh, zzmc, fzrq, zsyxq, fzjg))
    db.commit()
    cur.fetchone()
    return cur.fetchone()
def zzlx(data,aid):
    cursor = db.cursor()
    sql="DELETE FROM yunqi_addon17_zzlx where kid = %d" %(aid)
    cursor.execute(sql)
    db.commit()
    cert=data["cert"]
    for i in cert:

        fzrq = int(time.mktime(time.strptime(i['organDate'], "%Y-%m-%d")))
        zsyxq = int(time.mktime(time.strptime(i['endDate'], "%Y-%m-%d")))
        try:
            searchzzlb(i["certName"])[0]
        except Exception as e:
            print(e)
            with open('addon17_zzlb.txt','a', encoding='utf8')as w:
                w.write('yunqi_addon17_zzlb没有：'+i["certName"]+'\n')
            w.close()
            continue
        insertzzlx(aid, searchzzlb(i["certName"])[0], i["certId"], i['certName'],  fzrq , zsyxq, i["organName"])

# def update_yunqi_addon17(data,aid):
#     cursor = fwqdb.cursor()
#     xiangmu=data["messagecount"]['projectCount']
#     zizhi =data["messagecount"]['certCount']
#     rynum=data["messagecount"]['regPersonCount']
#     sql="update yunqi_addon17 set xiangmu=%d , zizhi= %d ,rynum=%d where aid = %d "%(xiangmu,zizhi,rynum,aid)
#     cursor.execute(sql)
#     cursor.close()
#     zzlx(data,aid)


#企业信息
def qymc(data):
    cursor=fwqdb.cursor()
    if("corpName" in data["base"]):
        conpany = data["base"]["corpName"]
    else:
        conpany = data["base"][0]["name"]
    sql="SELECT aid from yunqi_addon17 where qymc= '%s' "%(conpany)

    cursor.execute(sql)
    one = cursor.fetchone()  # 获取一条数据
    cursor.close()

    if not one is None :
        zzlx(data,one[0])
        person(data,one[0])
        project(data,one[0])
    else:
        print("添加新企业")


def run():

    path = './成功1'
    for file_name in os.listdir(path):
        flies = f'成功1/{file_name}'
        # flies = f'成功/companydb50.json'
        print(file_name)
        time.sleep(5)
        with open(file=flies, mode="r", encoding="utf-8") as r:
            data = r.readlines()
        #     print(data)
            for line in data:
                print(line.replace('\n',''))
                json1 = eval(line.strip())
                # print(json1)
                qymc(json1)
def test():
    data = [
        {'base': {'legalMan': '张建权', 'corpName': '河北旭禾建筑装饰工程有限公司', 'corpCode': '91130105MA07XQNN9N',
                  'id': '002106161904112743', 'address': '河北省石家庄市新华区和平西路315号301室',
                  'regionFullname': '河北省-石家庄市', 'qyRegType': '有限责任公司（自然人投资或控股）'},
         'messagecount': {'certCount': 2, 'regPersonCount': 11, 'projectCount': 0}, 'cert': [
            {'certType': '建筑业企业资质', 'certName': '建筑工程施工总承包三级', 'organDate': '2021-06-16',
             'endDate': '2026-06-15', 'organName': '石家庄市行政审批局', 'certId': 'D313223237',
             'corpName': '河北旭禾建筑装饰工程有限公司', 'corpCode': '91130105MA07XQNN9N'},
            {'certType': '建筑业企业资质', 'certName': '建筑装修装饰工程专业承包二级', 'organDate': '2022-04-15',
             'endDate': '2027-04-14', 'organName': '河北省住房和城乡建设厅', 'certId': 'D213237110',
             'corpName': '河北旭禾建筑装饰工程有限公司', 'corpCode': '91130105MA07XQNN9N'}], 'regporson': [
            {'name': '房力维', 'id': '002105291825350633', 'zsbh': '冀213152026355', 'zhtype': '建筑工程',
             'sfz': '130124**********13', 'gsname': '河北旭禾建筑装饰工程有限公司', 'sex': 0, 'zyyz': '冀213152026355',
             'reg_end': 1703088000, 'zsdj': '二级注册建造师'},
            {'name': '李桂芝', 'id': '002105291825352474', 'zsbh': '冀213192215409', 'zhtype': '建筑工程',
             'sfz': '130125**********46', 'gsname': '河北旭禾建筑装饰工程有限公司', 'sex': 1, 'zyyz': '冀213192215409',
             'reg_end': 1750435200, 'zsdj': '二级注册建造师'},
            {'name': '鲁翠明', 'id': '002105291825357748', 'zsbh': '冀213111928532', 'zhtype': '建筑工程',
             'sfz': '130133**********1X', 'gsname': '河北旭禾建筑装饰工程有限公司', 'sex': 0, 'zyyz': '冀213111928532',
             'reg_end': 1671724800, 'zsdj': '二级注册建造师'},
            {'name': '王小兵', 'id': '002105291837378402', 'zsbh': '冀213192129426', 'zhtype': '建筑工程',
             'sfz': '130630**********15', 'gsname': '河北旭禾建筑装饰工程有限公司', 'sex': 0, 'zyyz': '冀213192129426',
             'reg_end': 1714924800, 'zsdj': '二级注册建造师'},
            {'name': '史增良', 'id': '002105291837383780', 'zsbh': '冀213131808138', 'zhtype': '建筑工程',
             'sfz': '132301**********34', 'gsname': '河北旭禾建筑装饰工程有限公司', 'sex': 0, 'zyyz': '冀213131808138',
             'reg_end': 1672416000, 'zsdj': '二级注册建造师'},
            {'name': '王大鹏', 'id': '002105291837390926', 'zsbh': '冀213142005756', 'zhtype': '建筑工程',
             'sfz': '131127**********7X', 'gsname': '河北旭禾建筑装饰工程有限公司', 'sex': 0, 'zyyz': '冀213142005756',
             'reg_end': 1682438400, 'zsdj': '二级注册建造师'},
            {'name': '闫德学', 'id': '002105291838393088', 'zsbh': '冀213081455053', 'zhtype': '建筑工程',
             'sfz': '132430**********14', 'gsname': '河北旭禾建筑装饰工程有限公司', 'sex': 0, 'zyyz': '冀213081455053',
             'reg_end': 1686153600, 'zsdj': '二级注册建造师'},
            {'name': '殷永军', 'id': '002105291858733280', 'zsbh': '冀213172129480', 'zhtype': '建筑工程',
             'sfz': '130525**********12', 'gsname': '河北旭禾建筑装饰工程有限公司', 'sex': 0, 'zyyz': '冀213172129480',
             'reg_end': 1715011200, 'zsdj': '二级注册建造师'},
            {'name': '王惠娟', 'id': '002110152352476785', 'zsbh': '冀213202143086', 'zhtype': '建筑工程,市政公用工程',
             'sfz': '130129**********22', 'gsname': '河北旭禾建筑装饰工程有限公司', 'sex': 1, 'zyyz': '冀213202143086',
             'reg_end': 1728662400, 'zsdj': '二级注册建造师'},
            {'name': '李国丽', 'id': '002203242257086254', 'zsbh': '冀213212209477', 'zhtype': '建筑工程',
             'sfz': '132326**********6X', 'gsname': '河北旭禾建筑装饰工程有限公司', 'sex': 1, 'zyyz': '冀213212209477',
             'reg_end': 1742486400, 'zsdj': '二级注册建造师'},
            {'name': '刘丹', 'id': '002210030019100310', 'zsbh': '冀213212220396', 'zhtype': '机电工程',
             'sfz': '130927**********29', 'gsname': '河北旭禾建筑装饰工程有限公司', 'sex': 1, 'zyyz': '冀213212220396',
             'reg_end': 1759075200, 'zsdj': '二级注册建造师'}], 'project': [], 'badcredit': [], 'goodcredit': [],
         'black': [], 'punishlist': [], 'chage': []}

    ]
    for line in data:
        print(line)
        qymc(line)


if __name__ == '__main__':
    with open('yunqi_persontype.json', 'r', encoding='utf8') as fp:
        json_data = json.load(fp)
    with open('yunqi_typeids.json', 'r', encoding='utf8') as fp:
        yunqi_typeids = json.load(fp)
    # run()
    test()



