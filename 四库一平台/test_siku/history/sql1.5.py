# -*-coding:utf-8 -*-
import datetime
import logging
import re
import threading
import time
import traceback
import pymysql
from dbutils.pooled_db import PooledDB
# from sikuyipingminspider import read_file


# db = pymysql.connect(
#     host='47.92.73.25',
#     port=3306,
#     user='python',
#     password='Kp123...',
#     database='yqc',
#     charset='utf8',
# )
from pypinyin import lazy_pinyin

# db=PooledDB(
#     creator=pymysql,
#     blocking=True,
#     maxconnections=100,
#     maxshared=100,
#     host='47.92.73.25',
#     user='python',
#     passwd='Kp123...',
#     db='yqc',
#     port=3306,
#     charset="utf8"
# )
#
# local_test
db = PooledDB(
    creator=pymysql,
    blocking=True,
    maxconnections=100,
    maxshared=100,
    host='localhost',
    user='root',
    passwd='root',
    db='uther_test',
    port=3306,
    charset="utf8"
)


# fwqdb = pymysql.connect(
#     host='47.92.73.25',
#     port=3306,
#     user='python',
#     password='Kp123...',
#     database='yqc',
#     charset='utf8'
# )


# 查找cityid
def findcityid(name):
    with open('yunqi_city.json', 'r', encoding='utf8') as r:
        lines = eval(r.read())
        # print(lines)
    for lis in lines.get('RECORDS'):
        # print(lis['typename'],type(lis['typename']))
        if name in lis['name']:
            print(lis['name'], lis['id'])
            return lis['id']
    # cur = fwqdb.cursor()
    # sql = "SELECT id FROM yunqi_city WHERE name LIKE %s"
    # cur.execute(sql, city)
    # nativeplace = cur.fetchone()
    # print(type(nativeplace), nativeplace[0])
    # db.commit()
    # return nativeplace[0]


# 查找typeid
def findtypeid(cert):
    print(cert)
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
            print(type(tyid),cert, tyid)
            return tyid['id']


# 增加数据
def insertdata(typeid, qymc, tyshxydm, qyfr, zclx, nativeplace, xxdz, xiangmu, zizhi, rynum, m_id):
    pooldb = db.connection()
    cur = pooldb.cursor()
    sql = "insert into " \
          "yunqi_addon17(typeid,qymc,tyshxydm,qyfr,zclx,nativeplace,xxdz,xiangmu,zizhi,rynum,m_id) " \
          "values " \
          "(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"

    cur.execute(sql, (typeid, qymc, tyshxydm, qyfr, zclx, nativeplace, xxdz, xiangmu, zizhi, rynum, m_id))
    pooldb.commit()
    return cur.fetchone()


# 查询企业信息
def searchdb(qymc):
    pooldb = db.connection()
    cur = pooldb.cursor()
    sql = "select aid,tyshxydm from yunqi_addon17 where (qymc='{}')".format(qymc)
    cur.execute(sql)
    # cur.commit()
    # print(cur.fetchone())
    # data=cur.fetchone()
    # print('searchdb:',data,type(data))
    return cur.fetchone()


def insertzzlx(kid, zzlb, zzzsh, zzmc, fzrq, zsyxq, fzjg):
    pooldb = db.connection()
    cur = pooldb.cursor()
    sql = "insert into " \
          "yunqi_addon17_zzlx(kid, zzlb, zzzsh, zzmc, fzrq, zsyxq, fzjg) " \
          "values " \
          "(%s,%s,%s,%s,%s,%s,%s);"

    cur.execute(sql, (kid, zzlb, zzzsh, zzmc, fzrq, zsyxq, fzjg))
    pooldb.commit()
    cur.fetchone()
    return cur.fetchone()


# 获取zzlb的号码
def searchzzlb(zzmc):
    with open('yunqi_addon17_zzlb.json', 'r', encoding='utf8') as r:
        lines = eval(r.read())
        # print(lines)
        for lis in lines.get('RECORDS'):
            # print(lis['pron'],type(lis['pron']))
            if zzmc in lis['pron']:
                print(lis['pron'], lis['parent_id'])
                return lis['parent_id']
    # cur = fwqdb.cursor()
    # sql = "select parent_id from yunqi_addon17_zzlb where (pron=%s)"
    # cur.execute(sql, zzmc)
    # db.commit()
    # print(cur.fetchall())
    # return cur.fetchone()


# 关联项目
def insertaddoninfos(fid, typeid, mid, title, senddate, linkman, pnumber, ztzmoney, lxwh, sjxmnumber, zzjgdm, jsxz,
                         tarea, lxjb):
    pooldb = db.connection()
    cur = pooldb.cursor()
    sql = "insert into " \
          "yunqi_addoninfos(fid,typeid,mid,title,senddate,linkman,pnumber,ztzmoney,lxwh,sjxmnumber,zzjgdm,jsxz,tarea,tzsbh,lxjb)" \
          "values" \
          "('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(fid, typeid, mid,
                                                                                                title,
                                                                                                senddate, linkman,
                                                                                                pnumber, ztzmoney,
                                                                                                lxwh,
                                                                                                sjxmnumber, zzjgdm,
                                                                                                jsxz, tarea, "''",
                                                                                                lxjb)
    # print(sql)
    cur.execute(sql)

    pooldb.commit()

# def search_type(name):
#     cur = fwqdb.cursor()
#     sql = "select id from yunqi_arctype where (typename=%s)"
#     cur.execute(sql, name)
#     db.commit()
# print(cur.fetchall())
# return cur.fetchone()

# 人员表
def inertaddon18(fid, typeid, name, sex, idcard, cardname, leixing, companyid, zsbh, zyyzh, yxq):
    pooldb = db.connection()
    cur = pooldb.cursor()
    sql = "insert into " \
          "yunqi_addon18(fid, typeid, name, sex, idcard, cardname, leixing, companyid, zsbh, zyyzh, yxq) " \
          "values " \
          "(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"

    cur.execute(sql, (fid, typeid, name, sex, idcard, cardname, leixing, companyid, zsbh, zyyzh, yxq))
    pooldb.commit()


def searchperson(zyyzh):
    pooldb = db.connection()
    cur = pooldb.cursor()
    sql = "select aid from yunqi_addon18 where (zyyzh=%s)"
    cur.execute(sql, zyyzh)

    return cur.fetchone()


def insert_qr(fid, aid):
    pooldb = db.connection()
    cur = pooldb.cursor()
    sql = "insert into " \
          "yunqi_qr(aid, rid) " \
          "values " \
          "(%s,%s);"

    cur.execute(sql, (fid, aid))
    pooldb.commit()


def insert_qx(aid, prjnum):
    pooldb = db.connection()
    cur = pooldb.cursor()
    sql = "insert into " \
          "yunqi_qx(aid, xid) " \
          "values " \
          "(%s,%s);"

    cur.execute(sql, (aid, prjnum))
    pooldb.commit()


# 查看人员证件类型id
def search_typeid(typename):
    with open('yunqi_arctype.json', 'r', encoding='utf8') as r:
        lines = eval(r.read())
        # print(lines)
    for lis in lines.get('RECORDS'):
        # print(lis['typename'],type(lis['typename']))
        for name in typename:
            if name in lis.get('typename'):
                print(lis['typename'], lis['id'])
                return lis['id']

    # cur = fwqdb.cursor()
    # sql = "select id from yunqi_arctype where typename  LIKE '{}{}{}'".format('%',typename,'%')
    # print(sql)
    # cur.execute(sql)
    # db.commit()
    # print(cur.fetchall())
    # return cur.fetchone()


def search_aid(pnumber):
    pooldb = db.connection()
    cur = pooldb.cursor()
    sql = "select aid from yunqi_addoninfos where (pnumber=%s)"
    cur.execute(sql, pnumber)
    return cur.fetchone()


# 插入项目参与单位与负责人
def insert_cydw(kid, qid, qymc, tyshxydm, name, idnum):
    pooldb = db.connection()
    cur = pooldb.cursor()
    print(kid, qid, qymc, tyshxydm, name, idnum)
    sql = "insert into yunqi_addoninfos_cydw(kid,qid,qymc,tyshxydm,name,idnum) " \
          "values (%s,%s,%s,%s,%s,%s);"
    cur.execute(sql, (kid, qid, qymc, tyshxydm, name, idnum))
    pooldb.commit()
    # print(cur.execute(sql,(kid,qid,qymc,tyshxydm,name,idnum)))


# print(cur.execute(sql,(kid,qid,qymc,tyshxydm,name,idnum)))
# print('wancheng')
# def search_prjtitle(num):
#     cur = db.cursor()
#     sql = "select aid from yunqi_qx where (pnumber=%s)"
#     cur.execute(sql, name)
#     db.commit()
#     return cur.fetchone()


# def updatetpeple(typeid, qymc, tyshxydm, qyfr, zclx, nativeplace, xxdz, xiangmu, zizhi, rynum, m_id):
#     pooldb_test.py = db.connection()
# cur = pooldb_test.py.cursor()
# sql = "insert into " \
#       "yunqi_addoninfos_cydw(kid,qid,qymc,tyshxydm,name,idnum) " \
#       "values " \
#       "(%s,%s,%s,%s,%s,%s);"
# cur.execute(sql, (typeid, qymc, tyshxydm, qyfr, zclx, nativeplace, xxdz, xiangmu, zizhi, rynum, m_id))


def searchzmc(kid, zzmc):
    pooldb = db.connection()
    cur = pooldb.cursor()
    sql = f"select id from yunqi_addon17_zzlx where (kid='{kid}'and zzmc='{zzmc}')"
    cur.execute(sql)
    return cur.fetchone()


def searchpnumber(pnumber):
    pooldb = db.connection()
    cur = pooldb.cursor()
    sql = f"select aid from yunqi_addoninfos where (pnumber='{pnumber}')"
    cur.execute(sql)
    return cur.fetchone()


def searchqr(aid):
    pooldb = db.connection()
    cur = pooldb.cursor()
    sql = f"select aid from yunqi_qr where (rid='{aid}')"
    cur.execute(sql)
    return cur.fetchone()


def searchqx(aid):
    pooldb = db.connection()
    cur = pooldb.cursor()
    sql = f"select aid from yunqi_qx where (xid='{aid}')"
    cur.execute(sql)
    return cur.fetchone()


def search_cydw(kid, qymc):
    pooldb = db.connection()
    cur = pooldb.cursor()
    sql = "select * from yunqi_addoninfos_cydw " \
          "where " \
          f"(kid='{kid}' and qymc='{qymc}')"
    cur.execute(sql)
    return cur.fetchone()

def Transformation(date):
    times=int(time.mktime(time.strptime(date, "%Y-%m-%d")))
    return times


def searchht(dj_number):
    pooldb = db.connection()
    cur = pooldb.cursor()
    sql = "select * from yunqi_addoninfos_ht " \
          "where " \
          f"(dj_number = '{dj_number}')"
    cur.execute(sql)
    return cur.fetchone()


def insert_ht(kid,ba_number, ht_type, dj_number, money, fb_qymc, cb_qymc, cb_id, type, build, fb_xydm, cb_xydm, lh_qymc,
              lh_xydm, register_time, signing_time, source):
    pooldb = db.connection()
    cur = pooldb.cursor()
    sql = "insert into yunqi_addoninfos_ht(kid,ba_number, ht_type, dj_number, money, fb_qymc, cb_qymc, cb_id, type, build, fb_xydm, cb_xydm, lh_qymc, lh_xydm, register_time, signing_time, source) " \
          "values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
    cur.execute(sql, (kid,ba_number, ht_type, dj_number, money, fb_qymc, cb_qymc, cb_id, type, build, fb_xydm, cb_xydm, lh_qymc,
              lh_xydm, register_time, signing_time, source))
    pooldb.commit()


def searchjgys(babh,sjbabh):
    pooldb = db.connection()
    cur = pooldb.cursor()
    sql = "select * from yunqi_addoninfos_jgys " \
          "where " \
          f"(babh = '{babh}' and sjbabh='{sjbabh}')"
    cur.execute(sql)
    return cur.fetchone()


def insert_jgys(kid, babh, sjbabh, sjzj, sjmj, sjkgrq, jgys, xqurl):
    pooldb = db.connection()
    cur = pooldb.cursor()
    sql = "insert into yunqi_addoninfos_jgys(kid, babh, sjbabh, sjzj, sjmj, sjkgrq, jgys, xqurl) " \
          "values (%s,%s,%s,%s,%s,%s,%s,%s);"
    cur.execute(sql, (kid, babh, sjbabh, sjzj, sjmj, sjkgrq, jgys, xqurl))
    pooldb.commit()


def searchsgxk(sgbh, sjbh):
    pooldb = db.connection()
    cur = pooldb.cursor()
    sql = "select * from yunqi_addoninfos_sgxk " \
          "where " \
          f"(sgbh = '{sgbh}' and sjbh='{sjbh}')"
    cur.execute(sql)
    return cur.fetchone()


def insert_sgxk(kid, pid, sgbh, sjbh, htje, mj, fzrq, xqurl):
    pooldb = db.connection()
    cur = pooldb.cursor()
    sql = "insert into yunqi_addoninfos_sgxk(kid, pid, sgbh, sjbh, htje, mj, fzrq, xqurl) " \
          "values (%s,%s,%s,%s,%s,%s,%s,%s);"
    cur.execute(sql, (kid, pid, sgbh, sjbh, htje, mj, fzrq, xqurl))
    pooldb.commit()



def search_dt(number):
    pooldb = db.connection()
    cur = pooldb.cursor()
    sql = "select * from yunqi_addoninfos_dt " \
          "where " \
          f"(number = '{number}')"
    cur.execute(sql)
    return cur.fetchone()


def insert_dt(kid, title, number, cost, area, height, structure, grade, up_area, dw_area,
              layer, down_layer, long, wide,protect, scale, other, ztb_number, sg_number, xk_number,
              zl_number, aq_number, shock, green, green_type, shocks, limit, set, rebar, steel):
    pooldb = db.connection()
    cur = pooldb.cursor()
    sql = "insert into yunqi_addoninfos_dt (kid, title, number, cost, area, height, structure, grade, up_area, dw_area,layer, down_layer, `long`, wide,protect, scale, other, ` ztb_number`, sg_number, xk_number,zl_number, aq_number, shock, green, green_type, shocks, `limit`, `set`, rebar, steel)" \
          "values " \
          f"(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"



    cur.execute(sql,
                (kid, title, number, cost, area,height, structure, grade, up_area, dw_area,
                 layer, down_layer,long,wide,protect, scale, other, ztb_number, sg_number, xk_number,
                 zl_number, aq_number, shock, green, green_type, shocks, limit, set, rebar, steel))
    pooldb.commit()
    # ""


def search_sgtsc(sgtschgbh):
    pooldb = db.connection()
    cur = pooldb.cursor()
    sql = "select * from yunqi_addoninfos_sgtsc " \
          "where " \
          f"(sgtschgbh = '{sgtschgbh}')"
    cur.execute(sql)
    return cur.fetchone()


def insert_sgtsc(kid, pid, sgtschgbh, sjbh, kcdw, kcdw_sf, kcdw_dm, sjdw, sjdw_sf, sjdw_dm, sgdw, sgdw_sf, sgdw_dm,
                 scjg, scjg_dm, guimo, wcrq, xqurl, endtime, jsgm, one, count, startime, lh, xftime, xfhg, xfjg, rftime,
                 rfhj, rfjg, lerver):
    pooldb = db.connection()
    cur = pooldb.cursor()
    sql = "insert into yunqi_addoninfos_sgtsc (kid, pid, sgtschgbh, sjbh, kcdw, kcdw_sf, kcdw_dm, sjdw, sjdw_sf, sjdw_dm, sgdw, sgdw_sf, sgdw_dm, scjg, scjg_dm, guimo, wcrq, xqurl, endtime, jsgm, one, count, startime, lh, xftime, xfhg, xfjg, rftime, rfhj, rfjg, lerver)" \
          "values " \
          f"(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"

    cur.execute(sql,
                (kid, pid, sgtschgbh, sjbh, kcdw, kcdw_sf, kcdw_dm, sjdw, sjdw_sf, sjdw_dm, sgdw, sgdw_sf, sgdw_dm,
                 scjg, scjg_dm, guimo, wcrq, xqurl, endtime, jsgm, one, count, startime, lh, xftime, xfhg, xfjg, rftime,
                 rfhj, rfjg, lerver))
    pooldb.commit()


def search_ztb(tzsbh):
    pooldb = db.connection()
    cur = pooldb.cursor()
    sql = "select * from yunqi_addoninfos_ztb " \
          "where " \
          f"(tzsbh = '{tzsbh}')"
    cur.execute(sql)
    return cur.fetchone()


def insert_ztb(kid, pid, zblx, zbfs, zbdw, zbrq, zbje, tzsbh, sjbh, xqurl):
    pooldb = db.connection()
    cur = pooldb.cursor()
    sql = "insert into yunqi_addoninfos_ztb(kid, pid, zblx, zbfs, zbdw, zbrq, zbje, tzsbh, sjbh, xqurl) " \
          "values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
    cur.execute(sql, (kid, pid, zblx, zbfs, zbdw, zbrq, zbje, tzsbh, sjbh, xqurl))
    pooldb.commit()


# def run(data, fil):
#     try:

    # except Exception as e:
    #     # with open(file=f"company_base/companydb{fil}.json", mode="a", encoding="utf-8") as w:
    #     #     w.write(str(data) + '\n')
    #     # w.close()
    #     logging.error(f"add db problem{e}\n{traceback.format_exc()}")
#
# 插入yunqi_addon17
def table_yunqi_addon17(base, message,certs):
        base = base.get('base')
        message = message.get('messagecount')
        cert = certs.get('cert')
        tyshxydm = base['corpCode']
        certType = cert[0]['certType']
        typeid=106
        if '资质' in certType:
            typename = re.findall(r'([\S]+)资质', certType)
            typeid = findtypeid(typename[0])

        qymc = base['corpName']
        if searchdb(qymc):
            print(f'yunqi_addon17 {qymc} exist!')
        else:
            cityid = base['regionFullname']
            if "省" in cityid:
                cityid = re.findall(r'[\W\-?](\S+)', cityid)[0]
            qyfr = base.get('legalMan', '')
            zclx = base['qyRegType']
            nativeplace = findcityid(cityid)
            xxdz = base['address']
            xiangmu = message['projectCount']
            zizhi = message['certCount']
            rynum = message['regPersonCount']
            py = ''
            m_id = 10036
            for pin in lazy_pinyin(qymc):
                py += pin
            print(typeid, py, qymc, tyshxydm, qyfr, zclx, nativeplace, xxdz, xiangmu, zizhi, rynum, m_id)
            insertdata(typeid, qymc, tyshxydm, qyfr, zclx, nativeplace, xxdz, xiangmu, zizhi, rynum, m_id)
            print(f'addon17{qymc}入库完成')

# 插入资质表 addon17_zzlx
def table_yunqi_addon17_zzlx(kid,qymc,certs):

    for cert in certs:
        zzmc = cert.get('certName')
        if searchzmc(kid, zzmc):
            print(f'zzlx {zzmc} exist!')
        else:
            zzlb = searchzzlb(zzmc)
            # print(kid)
            zzzsh = cert['certId']
            fzrq = int(time.mktime(time.strptime(cert['organDate'], "%Y-%m-%d")))
            zsyxq = int(time.mktime(time.strptime(cert['endDate'], "%Y-%m-%d")))
            fzjg = cert['organName']
            print(kid, zzlb, zzzsh, zzmc, fzrq, zsyxq, fzjg)
            insertzzlx(kid, zzlb, zzzsh, zzmc, fzrq, zsyxq, fzjg)
            print(f"addon17_zzlx {zzmc} 入库完成")
    return   kid

# addon18插入人员
def table_yunqi_addon18(kid,reg):
    fid = kid
    # for reg in data.get('regporson'):
    if reg['zhtype'].split(',')[0] == '土建':
        typeid = '94'
    elif reg['zhtype'].split(',')[0] == '不分专业':
        typeid = '0'
    else:
        typeid = search_typeid(reg['zhtype'].split(','))[0]
    zyyzh = reg['zyyz']
    if searchperson(zyyzh):
        print(f'inertaddon18 {zyyzh} exist')
    else:
        zsbh = reg['zsbh']
        # print(type(regtpye),regtpye)
        name = reg['name']
        sex = reg['sex']
        idcard = 1
        if not reg['sfz']:
            idcard = 0
        cardname = reg['sfz']
        leixing = ''
        companyid = reg['gsname']
        yxq = reg['reg_end']
        print(fid, typeid, name, sex, idcard, cardname, leixing, companyid, zsbh, zyyzh, yxq)
        inertaddon18(fid, typeid, name, sex, idcard, cardname, leixing, companyid, zsbh, zyyzh, yxq)
        print(f"inertaddon18 {name}入库完成")
    aid = searchperson(zyyzh)[0]
    if searchqr(aid):
        print(aid, 'exist')
    else:
        insert_qr(fid, aid)  # 企业 人员
        print(f'qr {aid} 关联入库完成')

# 插入yunqi_addoninfos项目表
def table_yunqi_addoninfos(kid,cert,project):
    # for pro in projects:
    #     project = pro.get('prodetail')
    pnumber = project.get('prjNum')
    print(pnumber)
    if searchpnumber(pnumber):
        print(pnumber, 'exist')
        # continue
    else:
        fid = kid
        certType = cert[0]['certType']
        typeid = 106
        if '资质' in certType:
            typename = re.findall(r'([\S]+)资质', certType)
            typeid = findtypeid(typename[0])
        # typeid = tyid
        mid = 10036
        senddate = int(time.time())
        title = project.get('prjName')
        linkman = project.get('buildCorpName')
        ztzmoney = project.get('allInvest', 0.0)
        sjxmnumber = project.get('provincePrjNum')
        lxwh = project.get('prjApprovalNum')
        zzjgdm = project.get('buildCorpCode')
        jsxz = '新建'
        lxjb = project.get('prjApprovalLevelNum')
        tarea = project.get('allArea', 0.0)
        # insertaddoninfos()
        insertaddoninfos(fid, typeid, mid, title, senddate, linkman, pnumber, ztzmoney, lxwh, sjxmnumber,
                         zzjgdm, jsxz, tarea, lxjb)
        print(f"{title}入库完成")
        # print(pnumber)

    aid = search_aid(pnumber)
    if searchqx(pnumber):
        print(f'qx project {pnumber} exist')
    else:
        insert_qx(aid, pnumber)
        print(f'qx {aid} 关联入库完成')


        yunqi_addoninfos_cydw(aid,) # 插入参与单位与相关负责人yunqi_addoninfos_cydw

        yunqi_addoninfos_ht() # 插入合同登记 yunqi_addoninfos_ht

        yunqi_addoninfos_jgys() # 插入竣工验收yunqi_addoninfos_jgys

        yunqi_addoninfos_sgxk()# 插入施工许可信息yunqi_addoninfos_sgxk

        yunqi_addoninfos_dt() # 插入工程项目单体信息yunqi_addoninfos_dt

        yunqi_addoninfos_sgtsc() # 插入施工图审查yunqi_addoninfos_sgtsc


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


# 插入参与单位与相关负责人yunqi_addoninfos_cydw
def yunqi_addoninfos_cydw(jointhing):

    for jointhing in pro.get('jointhing'):
        kid = aid[0]
        qid = searchdb(base['corpName'])[0]
        qymc = jointhing.get('corpname', '-')
        tyshxydm = jointhing.get('corpcode', '-', )
        name = jointhing.get('personname', '-')
        idnum = jointhing.get('idcard', '-')
        if search_cydw(kid, qymc):
            print(f'cydw project {qymc} exist')
        else:
            print(kid, qid, qymc, tyshxydm, name, idnum)
            insert_cydw(kid, qid, qymc, tyshxydm, name, idnum)
            print(f'cydw 插入{qymc}成功')

# 插入合同登记 yunqi_addoninfos_ht
def yunqi_addoninfos_ht():
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
        kid = aid[0]  # '项目id',
        ba_number = contract.get('provinceContractNum')
        ht_type = ''
        for typeid in contractType:
            if typeid['id'] == contract.get('contractTypeNum'):
                ht_type = typeid['name']
        dj_number = contract.get('recordNum')
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
        createdate = contract.get('createDate')
        if '-' in str(createdate):
            register_time = createdate
        else:
            register_time = datetime.datetime.fromtimestamp(createdate / 1000).strftime("%Y-%m-%d")

        signing_time = contract.get('contractDate')
        source = contract.get('dataSource')
        if source:
            for sourcetypes in dataSourceTypes:
                if sourcetypes['id'] == str(source):
                    source = sourcetypes['name']
        else:
            source = '-'
        if searchht(dj_number):
            print(f'ht {dj_number} exist')
        else:
            print(kid, ba_number, ht_type, dj_number, money, fb_qymc, cb_qymc, cb_id, type, build, fb_xydm, cb_xydm,
                  lh_qymc, lh_xydm, register_time, signing_time, source)
            insert_ht(kid, ba_number, ht_type, dj_number, money, fb_qymc, cb_qymc, cb_id, type, build, fb_xydm,
                      cb_xydm, lh_qymc, lh_xydm, register_time, signing_time, source)
            print(f'ht 插入{dj_number}成功')

 # 插入竣工验收 yunqi_addoninfos_jgys
def yunqi_addoninfos_jgys():
    for finish in pro.get('finish'):
        kid = searchdb(base['corpName'])[0]
        babh = finish.get('prjFinishNum')
        sjbabh = finish.get('provincePrjFinishNum')
        sjzj = finish.get('factCost')
        sjmj = finish.get('factArea')
        sjkgrq = int(finish.get('cREATEDATE') / 1000)
        jgys = int(Transformation(finish.get('eDate')))
        xqurl = ''
        if searchjgys(babh, sjbabh):
            print(f'jgys {babh} exist')
        else:
            print(kid, babh, sjbabh, sjzj, sjmj, sjkgrq, jgys, xqurl)
            insert_jgys(kid, babh, sjbabh, sjzj, sjmj, sjkgrq, jgys, xqurl)
            print(f'jgys 插入{babh}成功')

 # 插入施工图审查 yunqi_addoninfos_sgtsc
def yunqi_addoninfos_sgtsc():
    for censor in pro.get('censor'):
        # print(censor)
        kid = searchdb(base['corpName'])[0]
        pid = aid[0]
        sgtschgbh = censor.get('censorNum', '-')
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
        wcrq = censor.get('createDate', 0)
        if '-' in str(wcrq):
            wcrq = Transformation(wcrq)
        elif len(str(wcrq)) == 13:
            wcrq = int(wcrq / 1000)
        else:
            wcrq = int(wcrq)
        xqurl = '-'
        endtime = censor.get('censorEDate', '0')
        print(endtime)
        if len(str(endtime)) == 13:
            endtime = int(endtime / 1000)

        jsgm = censor.get('prjSize', '-')
        one = censor.get('oneCensorIsPass', '-')
        count = censor.get('oneCensorWfqtContent', 0)
        if count == '无' or count == ' ':
            count = 0
        else:
            count = count
        startime = censor.get('createDate', '0')
        if '-' in str(startime):
            startime = Transformation(startime)
        else:
            startime = int(startime)
        lh = censor.get('oneCensorWfqtCount', '-')
        xftime = censor.get('', '-')
        xfhg = censor.get('', '-')
        xfjg = censor.get('', '-')
        rftime = censor.get('', '-')
        rfhj = censor.get('', '-')
        rfjg = censor.get('', '-')
        lerver = censor.get('dataLevel', '-')
        if search_sgtsc(sgtschgbh):
            print(f'sgtsc {sgtschgbh} exist')
        else:
            print(kid, pid, sgtschgbh, sjbh, kcdw, kcdw_sf, kcdw_dm, sjdw, sjdw_sf, sjdw_dm, sgdw, sgdw_sf,
                  sgdw_dm, scjg, scjg_dm, guimo, wcrq, xqurl, endtime, jsgm, one, count, startime, lh, xftime,
                  xfhg, xfjg, rftime, rfhj, rfjg, lerver)
            insert_sgtsc(kid, pid, sgtschgbh, sjbh, kcdw, kcdw_sf, kcdw_dm, sjdw, sjdw_sf, sjdw_dm, sgdw, sgdw_sf,
                         sgdw_dm, scjg, scjg_dm, guimo, wcrq, xqurl, endtime, jsgm, one, count, startime, lh,
                         xftime,
                         xfhg, xfjg, rftime, rfhj, rfjg, lerver)
            print(f'sgtsc 插入{sgtschgbh}成功')

# 插入工程项目单体信息yunqi_addoninfos_dt
def yunqi_addoninfos_dt():
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
    nuits = pro.get('unit')
    if nuits:
        for unit in nuits:
            # print(unit)
            kid = aid[0]
            title = unit.get('subprjname')
            number = unit.get('unitcode', '-')
            cost = unit.get('invest', '0.0')
            area = unit.get('floorbuildarea', '0.0')
            height = unit.get('structureheight', '0.0')
            structure = '-'
            for structuretype in prstructuretypes:
                if structuretype['id'] == unit.get('structuretypenum'):
                    structure = structuretype['name']
            grade = '-'
            for prjlevel in prjLevels:
                if prjlevel['id'] == unit.get('prjlevelnum'):
                    grade = prjlevel['name']
            up_area = unit.get('pjrsize', '0.0').replace('平方米', '')
            dw_area = unit.get('rfbottomarea', '0.0')
            layer = unit.get('floorcount', 0)
            down_layer = unit.get('bottomfloorcount', 0)
            long = '0.0'
            wide = '0.0'
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
            # time.sleep(222)
            print(kid)
            if search_dt(number):
                print(f'dt {qymc} exist')
            else:
                print(kid, title, number, cost, area, height, structure, grade, up_area, dw_area, layer, down_layer,
                      long, wide, protect, scale, other, ztb_number, sg_number, xk_number, zl_number, aq_number,
                      shock, green, green_type, shocks, limit, set, rebar, steel)
                insert_dt(kid, title, number, cost, area, height, structure, grade, up_area, dw_area, layer,
                          down_layer, long, wide, protect, scale, other, ztb_number, sg_number, xk_number,
                          zl_number, aq_number, shock, green, green_type, shocks, limit, set, rebar, steel)
                print(f'dt 插入{qymc}成功')

# 插入施工许可信息yunqi_addoninfos_sgxk
def yunqi_addoninfos_sgxk():
    licencedata = pro.get('licence')
    if licencedata:
        for licence in licencedata:
            kid = searchdb(base['corpName'])[0]
            pid = aid[0]
            sgbh = licence.get('builderLicenceNum', '-')
            sjbh = licence.get('projectPlanNum', '0')
            htje = licence.get('contractMoney', '0')
            mj = licence.get('area', '0.0')
            fzrq = int(licence.get('createDate') / 1000)
            xqurl = ''
            if searchsgxk(sgbh, sjbh):
                print(f'sgxk {sgbh} exist')
            else:
                print(kid, pid, sgbh, sjbh, htje, mj, fzrq, xqurl)
                insert_sgxk(kid, pid, sgbh, sjbh, htje, mj, fzrq, xqurl)
                print(f'sgxk insert{sgbh} ')


# 插入施工图审查yunqi_addoninfos_ztb
def yunqi_addoninfos_ztb():

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
        kid = searchdb(base['corpName'])[0]
        pid = aid[0]
        zblx = tender.get('tenderClassNum')
        for ptender in prtenderclasss:
            if ptender['id'] == zblx:
                zblx = ptender.get('name')
        zbfs = tender.get('tenderTypeNum')
        for tendertype in prtendertypes:
            if tendertype['id'] == zbfs:
                zbfs = tendertype.get('name')
        zbdw = tender.get('tenderCorpName', '-')
        zbrq = tender.get('tenderResultDate')
        if '-' in zbrq:
            zbrq = Transformation(zbrq)
        zbje = tender.get('tenderMoney', '0')
        tzsbh = tender.get('tenderNum', '-')
        sjbh = tender.get('provinceTenderNum', '-')
        xqurl = tender.get('', '-')
        if search_ztb(tzsbh):
            print(f'ztb {tzsbh} exist')
        else:
            print(kid, pid, zblx, zbfs, zbdw, zbrq, zbje, tzsbh, sjbh, xqurl)
            insert_ztb(kid, pid, zblx, zbfs, zbdw, zbrq, zbje, tzsbh, sjbh, xqurl)
            print(f'ztb 插入{tzsbh}成功')

# def run(data, fil):
    #     try:
    #         # 插入yunqi_addon17
    #
    #
    #         certs = data.get('cert')
    #         projects = data.get('project')
    #
    #         # print(typeid)
    #
    #
    #
    #         # 插入资质表 addon17_zzlx
    #         kid = searchdb(qymc)[0]
    #         for cert in certs:
    #             zzmc = cert.get('certName')
    #             print(zzmc)
    #             if searchzmc(kid, zzmc):
    #                 print(f'zzlx {zzmc} exist!')
    #             else:
    #                 zzlb = searchzzlb(zzmc)
    #                 # print(kid)
    #                 zzzsh = cert['certId']
    #                 fzrq = int(time.mktime(time.strptime(cert['organDate'], "%Y-%m-%d")))
    #                 zsyxq = int(time.mktime(time.strptime(cert['endDate'], "%Y-%m-%d")))
    #                 fzjg = cert['organName']
    #                 print(kid, zzlb, zzzsh, zzmc, fzrq, zsyxq, fzjg)
    #                 insertzzlx(kid, zzlb, zzzsh, zzmc, fzrq, zsyxq, fzjg)
    #                 print(f"addon17_zzlx {zzmc} 入库完成")
    #
    #         # addon18插入人员
    #         fid = kid
    #         for reg in data.get('regporson'):
    #             if reg['zhtype'].split(',')[0] == '土建':
    #                 typeid = '94'
    #             elif reg['zhtype'].split(',')[0] == '不分专业':
    #                 typeid = '0'
    #             else:
    #                 typeid = search_typeid(reg['zhtype'].split(','))[0]
    #             zyyzh = reg['zyyz']
    #             if searchperson(zyyzh):
    #                 print(f'inertaddon18 {zyyzh} exist')
    #             else:
    #                 zsbh = reg['zsbh']
    #                 # print(type(regtpye),regtpye)
    #                 name = reg['name']
    #                 sex = reg['sex']
    #                 idcard = 1
    #                 if not reg['sfz']:
    #                     idcard = 0
    #                 cardname = reg['sfz']
    #                 leixing = ''
    #                 companyid = reg['gsname']
    #                 yxq = reg['reg_end']
    #                 print(fid, typeid, name, sex, idcard, cardname, leixing, companyid, zsbh, zyyzh, yxq)
    #                 inertaddon18(fid, typeid, name, sex, idcard, cardname, leixing, companyid, zsbh, zyyzh, yxq)
    #                 print(f"inertaddon18 {name}入库完成")
    #             aid = searchperson(zyyzh)[0]
    #             if searchqr(aid):
    #                 print(aid, 'exist')
    #             else:
    #                 insert_qr(fid, aid)  # 企业 人员
    #                 print(f'qr {aid} 关联入库完成')
    #
    #         # 插入yunqi_addoninfos项目表
    #         listaa = []
    #         for pro in projects:
    #             project = pro.get('prodetail')
    #             pnumber = project.get('prjNum')
    #             title = project.get('prjName')
    #             print(title)
    #             if searchpnumber(pnumber):
    #                 print(pnumber, 'exist')
    #                 # continue
    #             else:
    #                 fid = kid
    #                 typeid = tyid
    #                 mid = 10036
    #                 senddate = int(time.time())
    #                 linkman = project.get('buildCorpName')
    #                 ztzmoney = project.get('allInvest', 0.0)
    #                 sjxmnumber = project.get('provincePrjNum')
    #                 lxwh = project.get('prjApprovalNum')
    #                 zzjgdm = project.get('buildCorpCode')
    #                 jsxz = '新建'
    #                 lxjb = project.get('prjApprovalLevelNum')
    #                 tarea = project.get('allArea', 0.0)
    #                 # insertaddoninfos()
    #                 insertaddoninfos(fid, typeid, mid, title, senddate, linkman, pnumber, ztzmoney, lxwh, sjxmnumber,
    #                                  zzjgdm, jsxz, tarea, lxjb)
    #                 print(f"{title}入库完成")
    #                 # print(pnumber)
    #             aid = search_aid(pnumber)
    #
    #             if searchqx(pnumber):
    #                 print(f'qx project {pnumber} exist')
    #             else:
    #                 insert_qx(aid, pnumber)
    #                 print(f'qx {aid} 关联入库完成')
    #
    #             # 插入参与单位与相关负责人yunqi_addoninfos_cydw
    #
    #             for jointhing in pro.get('jointhing'):
    #                 kid = aid[0]
    #                 qid = searchdb(base['corpName'])[0]
    #                 qymc = jointhing['corpname']
    #                 tyshxydm = jointhing['corpcode']
    #                 name = jointhing.get('personname', '-')
    #                 idnum = jointhing.get('idcard', '-')
    #                 if search_cydw(kid, qymc):
    #                     print(f'cydw project {qymc} exist')
    #                 else:
    #                     print(kid, qid, qymc, tyshxydm, name, idnum)
    #                     insert_cydw(kid, qid, qymc, tyshxydm, name, idnum)
    #                     print(f'cydw 插入{qymc}成功')
    #
    #             # 插入工程项目单体信息yunqi_addoninfos_dt
    #             prstructuretypes = [
    #                 {'id': "001",'name': "砖混结构"},
    #                 {'id': "002",'name': "底框结构"},
    #                 {'id': "003",'name': "框架结构"},
    #                 {'id': "004",'name': "框架－剪力墙结构"},
    #                 {'id': "005",'name': "剪力墙结构"},
    #                 {'id': "006",'name': "板柱-剪力墙结构"},
    #                 {'id': "007",'name': "短肢墙剪力墙结构"},
    #                 {'id': "008",'name': "部分框支剪力墙结构"},
    #                 {'id': "009",'name': "框-筒体结构"},
    #                 {'id': "010",'name': "筒中筒结构"},
    #                 {'id': "011",'name': "异型柱框架结构"},
    #                 {'id': "012",'name': "复杂高层结构"},
    #                 {'id': "013",'name': "混合结构"},
    #                 {'id': "014",'name': "钢结构"},
    #                 {'id': "015",'name': "排架结构"},
    #                 {'id': "016",'name': "木结构"},
    #                 {'id': "099",'name': "其他"}
    #             ]
    #             prjLevels = [
    #                 {'id': "201",'name': "甲级"},
    #                 {'id': "202",'name': "乙级"},
    #                 {'id': "203",'name': "丙级"},
    #                 {'id': "310",'name': "特级"},
    #                 {'id': "311",'name': "一级"},
    #                 {'id': "312",'name': "二级"},
    #                 {'id': "313",'name': "三级"},
    #                 {'id': "321",'name': "大型"},
    #                 {'id': "322",'name': "中型"},
    #                 {'id': "323",'name': "小型"}
    #             ]
    #             greenBuildingLevels = [
    #                 {'id': "001",'name': "一星级"},
    #                 {'id': "002",'name': " 二星级"},
    #                 {'id': "003",'name': "三星级"}
    #             ]
    #             seismicintensityScales = [
    #                 {'id': "001",'name': "不设防"},
    #                 {'id': "002",'name': "6度"},
    #                 {'id': "003",'name': "7度"},
    #                 {'id': "004",'name': "8度"},
    #                 {'id': "005",'name': "9度"}]
    #             for unit in pro.get('unit'):
    #                 kid=aid[0]
    #                 title=unit.get('subprjname')
    #                 number=unit.get('unitcode')
    #                 cost=unit.get('invest')
    #                 area=unit.get('floorbuildarea')
    #                 height=unit.get('structureheight')
    #                 structure='-'
    #                 for structure in prstructuretypes:
    #                     if structure['id'] == unit.get('structuretypenum'):
    #                         structure  = typeid['name']
    #                 grade='-'
    #                 for prjlevel in prjLevels:
    #                     if prjlevel['id'] == unit.get('prjlevelnum'):
    #                         grade  = prjlevel['name']
    #                 up_area=unit.get('pjrsize')
    #                 dw_area=unit.get('rfbottomarea')
    #                 layer=unit.get('floorcount')
    #                 down_layer=unit.get('bottomfloorcount')
    #                 long='-'
    #                 wide='-'
    #                 protect=unit.get('rfbottomarea')
    #                 scale='-'
    #                 other='-'
    #                 ztb_number='-'
    #                 sg_number=unit.get('censornum')
    #                 xk_number=unit.get('builderlicencenum')
    #                 zl_number=unit.get('qualitynum')
    #                 aq_number=unit.get('safenum')
    #                 shock=unit.get('isshockisolationbuilding')
    #                 green=unit.get('isgreenbuilding')
    #                 green_type='-'
    #                 for greenlevel in greenBuildingLevels:
    #                     if greenlevel['id'] == unit.get('greenbuidinglevel'):
    #                         green_type = greenlevel['name']
    #                 shocks='-'
    #                 for Scales in seismicintensityScales:
    #                     if Scales['id'] == unit.get('seismicintensityscale'):
    #                         shocks = Scales['name']
    #                 limit=unit.get('issuperhightbuilding')
    #                 set=unit.get('suitecount')
    #                 rebar='-'
    #                 steel='-'
    #                 print(kid, title, number, cost, area, height, structure, grade, up_area, dw_area, layer, down_layer,
    #                       long, wide, protect, scale, other, ztb_number, sg_number, xk_number, zl_number, aq_number, shock,
    #                       green, green_type, shocks, limit, set, rebar, steel)
    #                 time.sleep(222)
    #                 # if search_dt(number):
    #                 #     print(f'dt {qymc} exist')
    #                 # else:
    #                 #     print(kid,title,number,cost,area,height,structure,grade,up_area,dw_area,layer,down_layer,long,wide,protect,scale,other,ztb_number,sg_number,xk_number,zl_number,aq_number,shock,green,green_type,shocks,limit,set,rebar,steel)
    #                 #     insert_dt(kid,title,number,cost,area,height,structure,grade,up_area,dw_area,layer,down_layer,long,wide,protect,scale,other,ztb_number,sg_number,xk_number,zl_number,aq_number,shock,green,green_type,shocks,limit,set,rebar,steel)
    #                 #     print(f'dt 插入{qymc}成功')
    #
    #             # 插入合同登记 yunqi_addoninfos_ht
    #             contractType = [
    #                 {'id': "100", 'name': "勘察"},
    #                 {'id': "200", 'name': "设计"},
    #                 {'id': "301", 'name': "施工总包"},
    #                 {'id': "302", 'name': "施工分包"},
    #                 {'id': "303", 'name': "施工劳务"},
    #                 {'id': "400", 'name': "监理"},
    #                 {'id': "600", 'name': "工程总承包"},
    #                 {'id': "700", 'name': "项目管理"},
    #                 {'id': "800", 'name': "全过程工程咨询"},
    #                 {'id': "900", 'name': "其他"}
    #             ]
    #             dataSourceTypes = [
    #                 {'id': "1", 'name': "业务办理"},
    #                 {'id': "2", 'name': "信息登记"},
    #                 {'id': "3", 'name': "历史业绩补录"},
    #                 {'id': "4", 'name': "共享交换"}
    #             ]
    #             for contract in pro.get('contract'):
    #                 kid = aid[0]  # '项目id',
    #                 ba_number = contract.get('provinceContractNum')
    #                 ht_type = ''
    #                 for typeid in contractType:
    #                     if typeid['id'] == contract.get('contractTypeNum'):
    #                         ht_type = typeid['name']
    #                 dj_number = contract.get('recordNum')
    #                 money = contract.get('contractMoney')
    #                 fb_qymc = contract.get('propietorCorpName','-')
    #                 cb_qymc = contract.get('contractorCorpName','-')
    #                 cb_id = searchdb(cb_qymc)
    #                 if cb_id:
    #                     cb_id=cb_id[0]
    #                 type = contract.get('dataLevel')
    #                 build = contract.get('prjSize')
    #                 fb_xydm = contract.get('propietorCorpCode','-')
    #                 cb_xydm = contract.get('contractorCorpCode','-')
    #                 lh_qymc = contract.get('unitecontractorCorpName', '-')
    #                 lh_xydm = contract.get('unitepropietorCorpName', '-')
    #                 createdate = contract.get('createDate')
    #                 if '-' in str(createdate):
    #                     register_time = createdate
    #                 else:
    #                     register_time = datetime.datetime.fromtimestamp(createdate / 1000).strftime("%Y-%m-%d")
    #
    #                 signing_time = contract.get('contractDate')
    #                 # if '-'in str(contractdate):
    #                 #     signing_time = Transformation(contractdate)
    #                 # else:
    #                 #     signing_time = contractdate
    #                 source = contract.get('dataSource')
    #                 if source:
    #                     for sourcetypes in dataSourceTypes:
    #                         if sourcetypes['id'] == str(source):
    #                             source = sourcetypes['name']
    #                 else:
    #                     source='-'
    #                 if searchht(dj_number):
    #                     print(f'ht {dj_number} exist')
    #                 else:
    #                     print(kid, ba_number, ht_type,dj_number, money, fb_qymc, cb_qymc,cb_id,type,build,fb_xydm,cb_xydm,lh_qymc,lh_xydm,register_time,signing_time,source)
    #                     insert_ht(kid,ba_number, ht_type,dj_number, money, fb_qymc, cb_qymc,cb_id,type,build,fb_xydm,cb_xydm,lh_qymc,lh_xydm,register_time,signing_time,source)
    #                     print(f'ht 插入{dj_number}成功')
    #
    #             # 插入竣工验收yunqi_addoninfos_jgys
    #             for finish in pro.get('finish'):
    #                 kid=searchdb(base['corpName'])[0]
    #                 babh=finish.get('prjFinishNum')
    #                 sjbabh=finish.get('provincePrjFinishNum')
    #                 sjzj=finish.get('factCost')
    #                 sjmj=finish.get('factArea')
    #                 sjkgrq= int(finish.get('cREATEDATE')/1000)
    #                 jgys= int(Transformation(finish.get('eDate')))
    #                 xqurl=''
    #                 if searchjgys(babh,sjbabh):
    #                     print(f'jgys {babh} exist')
    #                 else:
    #                     print(kid, babh, sjbabh, sjzj, sjmj, sjkgrq, jgys, xqurl)
    #                     insert_jgys(kid, babh, sjbabh, sjzj, sjmj, sjkgrq, jgys, xqurl)
    #                     print(f'jgys 插入{babh}成功')
    #
    #
    #
    #             # 插入施工图审查yunqi_addoninfos_sgtsc
    #             # for censor in pro.get('censor'):
    #             #     kid=searchdb(base['corpName'])[0]
    #             #     pid=aid[0]
    #             #     sgtschgbh=censor.get('censorNum')
    #             #     sjbh=censor.get('provinceCensorNum')
    #             #     kcdw=censor.get('')
    #             #     kcdw_sf=censor.get('')
    #             #     kcdw_dm=censor.get('')
    #             #     sjdw=censor.get('')
    #             #     sjdw_sf=censor.get('')
    #             #     sjdw_dm=censor.get('')
    #             #     sgdw=censor.get('')
    #             #     sgdw_sf=censor.get('')
    #             #     sgdw_dm=censor.get('')
    #             #     scjg=censor.get('')
    #             #     scjg_dm=censor.get('')
    #             #     guimo=censor.get('')
    #             #     wcrq=censor.get('')
    #             #     xqurl=censor.get('')
    #             #     endtime=censor.get('')
    #             #     jsgm=censor.get('')
    #             #     one=censor.get('')
    #             #     count=censor.get('')
    #             #     startime=censor.get('')
    #             #     lh=censor.get('')
    #             #     xftime=censor.get('')
    #             #     xfhg=censor.get('')
    #             #     xfjg=censor.get('')
    #             #     rftime=censor.get('')
    #             #     rfhj=censor.get('')
    #             #     rfjg=censor.get('')
    #             #     lerver=censor.get('')
    #
    #         # 插入施工许可信息yunqi_addoninfos_sgxk
    #             print(pro.get('licence'))
    #             licencedata=pro.get('licence')
    #             if licencedata:
    #                 for licence in licencedata:
    #                     kid=searchdb(base['corpName'])[0]
    #                     pid=aid[0]
    #                     sgbh=licence.get('builderLicenceNum','-')
    #                     sjbh=licence.get('projectPlanNum','0')
    #                     htje=licence.get('contractMoney','0')
    #                     mj=licence.get('area','0.0')
    #                     fzrq=int(licence.get('createDate')/1000)
    #                     xqurl=''
    #                     print(kid, pid, sgbh, sjbh, htje, mj, fzrq, xqurl)
    #                     if searchsgxk(sgbh,sjbh):
    #                         print(f'sgxk {sgbh} exist')
    #                     else:
    #                         print(kid,pid,sgbh,sjbh,htje,mj,fzrq,xqurl)
    #                         insert_sgxk(kid,pid,sgbh,sjbh,htje,mj,fzrq,xqurl)
    #                         print(f'sgxk insert{sgbh} ')
    #         print(len(listaa), listaa)
    #
    #
    #
    #     except Exception as e:
    #         # with open(file=f"company_base/companydb{fil}.json", mode="a", encoding="utf-8") as w:
    #         #     w.write(str(data) + '\n')
    #         # w.close()
    #         logging.debug(f"add db problem{e}\n{traceback.format_exc()}")

if __name__ == '__main__':
    # fil = str(datetime.datetime.today().strftime('%Y-%m-%d'))
    fil = '0'
    # test(fil)
    flies = f'./company_data/companydb{fil}.json'
    with open(file=flies, mode="r", encoding="utf-8") as r:
        datas = r.readlines()

    for line in datas:
        data = eval(line.lstrip().strip().replace('\n', ''))
        print(type(data), data)
        run(data, fil)
    # print(type(datas), datas)
    # datas = []
