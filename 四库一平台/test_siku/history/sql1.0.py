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

db=PooledDB(
    creator=pymysql,
    blocking=True,
    maxconnections=100,
    maxshared=100,
    host='47.92.73.25',
    user='python',
    passwd='Kp123...',
    db='yqc',
    port=3306,
    charset="utf8"
)

#local_test
# db=PooledDB(
#     creator=pymysql,
#     blocking=True,
#     maxconnections=100,
#     maxshared=100,
#     host='localhost',
#     user='root',
#     passwd='root',
#     db='uther_test',
#     port=3306,
#     charset="utf8"
# )




# fwqdb = pymysql.connect(
#     host='47.92.73.25',
#     port=3306,
#     user='python',
#     password='Kp123...',
#     database='yqc',
#     charset='utf8'
# )


#查找cityid
def findcityid(name):
    with open('../../auto/yunqi_city.json', 'r', encoding='utf8') as r:
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
#查找typeid
def findtypeid(cert):
    typedata=[{'id':98,	'typename':'环境工程监理'},
    {'id':99,	'typename':'勘察企业'},
    {'id':100,	'typename':'设计企业'},
    {'id':101,	'typename':'建筑业企业'},
    {'id':102,	'typename':'监理企业'},
    {'id':103,	'typename':'招标代理机构'},
    {'id':104,	'typename':'设计与施工一体化企业'},
    {'id':105,  'typename':'造价咨询企业'},
    {'id':106,	'typename':'其他类型'}]
    for tyid in typedata:
        if cert in tyid['typename']:
            # print(type(tyid), tyid)
            return tyid['id']

#增加数据
def insertdata(typeid,qymc,tyshxydm,qyfr,zclx,nativeplace,xxdz,xiangmu,zizhi,rynum,m_id):
    pooldb = db.connection()
    cur = pooldb.cursor()
    sql = "insert into " \
          "yunqi_addon17(typeid,qymc,tyshxydm,qyfr,zclx,nativeplace,xxdz,xiangmu,zizhi,rynum,m_id) " \
          "values " \
          "(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"

    cur.execute(sql, (typeid,qymc,tyshxydm,qyfr,zclx,nativeplace,xxdz,xiangmu,zizhi,rynum,m_id))
    # db.commit()
    return cur.fetchone()

#查询企业信息
def searchdb(qymc):
    pooldb = db.connection()
    cur = pooldb.cursor()
    sql = "select aid,tyshxydm from yunqi_addon17 where (qymc='{}')".format(qymc)
    cur.execute(sql)
    # cur.commit()
    # print(cur.fetchone())
    # data=cur.fetchone()
    # print('searchdb:',data,type(data))
    return  cur.fetchone()


def insertzzlx(kid, zzlb, zzzsh, zzmc, fzrq, zsyxq, fzjg):
    pooldb = db.connection()
    cur = pooldb.cursor()
    sql = "insert into " \
          "yunqi_addon17_zzlx(kid, zzlb, zzzsh, zzmc, fzrq, zsyxq, fzjg) " \
          "values " \
          "(%s,%s,%s,%s,%s,%s,%s);"

    cur.execute(sql, (kid, zzlb, zzzsh, zzmc, fzrq, zsyxq, fzjg))
    cur.fetchone()
    return cur.fetchone()

#获取zzlb的号码
def searchzzlb(zzmc):
    with open('../../auto/yunqi_addon17_zzlb.json', 'r', encoding='utf8') as r:
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


#关联项目
def insertaddoninfos(fid, typeid, mid, title, senddate, linkman, pnumber, ztzmoney, lxwh, sjxmnumber, zzjgdm, jsxz, tarea,lxjb):
    pooldb = db.connection()
    cur = pooldb.cursor()
    sql = "insert into " \
          "yunqi_addoninfos(fid,typeid,mid,title,senddate,linkman,pnumber,ztzmoney,lxwh,sjxmnumber,zzjgdm,jsxz,tarea,tzsbh,lxjb)"\
        "values"\
            "('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(fid,typeid,mid,title,senddate,linkman,pnumber,ztzmoney,lxwh,sjxmnumber,zzjgdm,jsxz,tarea,"''",lxjb)
    # print(sql)
    cur.execute(sql)



# def search_type(name):
#     cur = fwqdb.cursor()
#     sql = "select id from yunqi_arctype where (typename=%s)"
#     cur.execute(sql, name)
#     db.commit()
    # print(cur.fetchall())
    # return cur.fetchone()

#人员表
def inertaddon18(fid, typeid, name, sex, idcard, cardname, leixing, companyid, zsbh, zyyzh, yxq):
    pooldb = db.connection()
    cur = pooldb.cursor()
    sql = "insert into " \
          "yunqi_addon18(fid, typeid, name, sex, idcard, cardname, leixing, companyid, zsbh, zyyzh, yxq) " \
          "values " \
          "(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"

    cur.execute(sql, (fid, typeid, name, sex, idcard, cardname, leixing, companyid, zsbh, zyyzh, yxq))



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

    cur.execute(sql, (fid,aid))



def insert_qx(aid,prjnum):
    pooldb = db.connection()
    cur = pooldb.cursor()
    sql = "insert into " \
          "yunqi_qx(aid, xid) " \
          "values " \
          "(%s,%s);"

    cur.execute(sql, (aid,prjnum))


#查看人员证件类型id
def search_typeid(typename):
    with open('../../auto/yunqi_arctype.json', 'r', encoding='utf8') as r:
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


#插入项目参与单位与负责人
def insert_cydw(kid,qid,qymc,tyshxydm,name,idnum):
    pooldb = db.connection()
    cur = pooldb.cursor()
    sql="insert into " \
          "yunqi_addoninfos_cydw(kid,qid,qymc,tyshxydm,name,idnum) " \
          "values " \
          "(%s,%s,%s,%s,%s,%s);"
    cur.execute(sql, (kid,qid,qymc,tyshxydm,name,idnum))

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


def searchzmc(kid,zzmc):
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


def run(data,fil):
    try:
        # 插入yunqi_addon17
        base = data.get('base')
        message = data.get('messagecount')
        certs = data.get('cert')
        cityid = base['regionFullname']
        projects = data.get('project')
        if "省" in cityid:
            cityid = re.findall(r'[\W\-?](\S+)', cityid)[0]
        certType = certs[0]['certType']
        # print(typeid)
        if '资质' in certType:
            typename = re.findall(r'([\S]+)资质', certType)
            tyid = findtypeid(typename[0])
        tyshxydm = base['corpCode']
        typeid = tyid
        qymc = base['corpName']
        if searchdb(qymc):
            print(qymc,'exist!')
        else:
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
            print(typeid,py, qymc, tyshxydm, qyfr, zclx, nativeplace, xxdz, xiangmu, zizhi, rynum, m_id)
            insertdata(typeid, qymc, tyshxydm, qyfr, zclx, nativeplace, xxdz, xiangmu, zizhi, rynum, m_id)
            print('addon17,入库完成')

        # 插入资质表 addon17_zzlx
        kid = searchdb(qymc)[0]
        for cert in certs:
            zzmc = cert.get('certName')
            print(zzmc)
            if searchzmc(kid,zzmc):
                print(zzmc, 'exist!')
            else:
                zzlb = searchzzlb(zzmc)
                # print(kid)
                zzzsh = cert['certId']
                fzrq = int(time.mktime(time.strptime(cert['organDate'], "%Y-%m-%d")))
                zsyxq = int(time.mktime(time.strptime(cert['endDate'], "%Y-%m-%d")))
                fzjg = cert['organName']
                print(kid, zzlb, zzzsh, zzmc, fzrq, zsyxq, fzjg)
                insertzzlx(kid, zzlb, zzzsh, zzmc, fzrq, zsyxq, fzjg)
                print("addon17_zzlx, 入库完成")

        # addon18插入人员
        fid = kid
        for reg in data.get('regporson'):
            if reg['zhtype'].split(',')[0] == '土建':
                typeid = '94'
            elif reg['zhtype'].split(',')[0] =='不分专业':
                typeid = '0'
            else:
                typeid = search_typeid(reg['zhtype'].split(','))[0]
            zyyzh = reg['zyyz']
            if searchperson(zyyzh):
                print(f'peple {zyyzh} exist')
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
                print(f"{name}入库完成")
            aid = searchperson(zyyzh)[0]
            if searchqr(aid):
                print(aid, 'exist')
            else:
                insert_qr(fid, aid)  # 企业 人员
                print(f'{aid} qr关联入库完成')

        # 插入yunqi_addoninfos项目表
        for pro in projects:
            project = pro.get('prodetail')
            pnumber = project.get('prjNum')
            print(pnumber)
            if searchpnumber(pnumber):
                print(pnumber, 'exist')
                # continue
            else:
                fid = kid
                typeid = tyid
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
                print(f'{aid} qx关联入库完成')

    except Exception as e:
        # with open(file=f"company_base/companydb{fil}.json", mode="a", encoding="utf-8") as w:
        #     w.write(str(data) + '\n')
        # w.close()
        logging.debug(f"add db problem{e}\n{traceback.format_exc()}")


if __name__ == '__main__':
    # fil = str(datetime.datetime.today().strftime('%Y-%m-%d'))
    fil = '2023-02-14'
    # test(fil)
    # flies = f'./company_base/companydb{fil}.json'
    # with open(file=flies, mode="r", encoding="utf-8") as r:
    #     datas = r.readlines()
    datas = [
       "{'base': {'legalMan': '易炳权', 'corpName': '北京华夏石化工程监理有限公司', 'corpCode': '91110105101163896D', 'id': '002105291240555735', 'address': '北京市朝阳区雅成一里19号楼15层1801', 'regionFullname': '北京市', 'qyRegType': '其他有限责任公司'}, 'messagecount': {'certCount': 6, 'regPersonCount': 80, 'projectCount': 72}, 'cert': [{'certType': '监理资质', 'certName': '工程监理港口与航道工程专业乙级', 'organDate': '2018-01-21', 'endDate': '2023-12-31', 'organName': '北京市住房和城乡建设委员会', 'certId': 'E211007204', 'corpName': '北京华夏石化工程监理有限公司', 'corpCode': '91110105101163896D'}, {'certType': '监理资质', 'certName': '工程监理机电安装工程专业乙级', 'organDate': '2018-01-21', 'endDate': '2023-12-31', 'organName': '北京市住房和城乡建设委员会', 'certId': 'E211007204', 'corpName': '北京华夏石化工程监理有限公司', 'corpCode': '91110105101163896D'}, {'certType': '监理资质', 'certName': '工程监理电力工程专业甲级', 'organDate': '2019-08-01', 'endDate': '2024-08-01', 'organName': '住房和城乡建设部', 'certId': 'E111007207', 'corpName': '北京华夏石化工程监理有限公司', 'corpCode': '91110105101163896D'}, {'certType': '监理资质', 'certName': '工程监理市政公用工程专业甲级', 'organDate': '2019-08-01', 'endDate': '2024-08-01', 'organName': '住房和城乡建设部', 'certId': 'E111007207', 'corpName': '北京华夏石化工程监理有限公司', 'corpCode': '91110105101163896D'}, {'certType': '监理资质', 'certName': '工程监理房屋建筑工程专业甲级', 'organDate': '2019-08-01', 'endDate': '2024-08-01', 'organName': '住房和城乡建设部', 'certId': 'E111007207', 'corpName': '北京华夏石化工程监理有限公司', 'corpCode': '91110105101163896D'}, {'certType': '监理资质', 'certName': '工程监理化工石油工程专业甲级', 'organDate': '2019-08-01', 'endDate': '2024-08-01', 'organName': '住房和城乡建设部', 'certId': 'E111007207', 'corpName': '北京华夏石化工程监理有限公司', 'corpCode': '91110105101163896D'}], 'regporson': [{'name': '李佰棉', 'id': '002105291838538576', 'zsbh': '00721536', 'zhtype': '房屋建筑工程,机电安装工程', 'sfz': '220381**********1X', 'gsname': '北京华夏石化工程监理有限公司', 'sex': 0, 'zyyz': '11021133', 'reg_end': 1751472000, 'zsdj': '注册监理工程师'}, {'name': '张天', 'id': '002105291843246749', 'zsbh': '00628957', 'zhtype': '化工石油工程,房屋建筑工程', 'sfz': '430302**********15', 'gsname': '北京华夏石化工程监理有限公司', 'sex': 0, 'zyyz': '11018890', 'reg_end': 1727020800, 'zsdj': '注册监理工程师'}, {'name': '黄培海', 'id': '002105291844498818', 'zsbh': '00479064', 'zhtype': '机电安装工程,化工石油工程', 'sfz': '512501**********5X', 'gsname': '北京华夏石化工程监理有限公司', 'sex': 0, 'zyyz': '51012065', 'reg_end': 1706371200, 'zsdj': '注册监理工程师'}, {'name': '刘吉宏', 'id': '002105291846696161', 'zsbh': '00718215', 'zhtype': '化工石油工程,港口与航道工程', 'sfz': '620321**********52', 'gsname': '北京华夏石化工程监理有限公司', 'sex': 0, 'zyyz': '11021069', 'reg_end': 1749312000, 'zsdj': '注册监理工程师'}, {'name': '徐伟', 'id': '002105291846770504', 'zsbh': '00532504', 'zhtype': '化工石油工程,机电安装工程', 'sfz': '120109**********15', 'gsname': '北京华夏石化工程监理有限公司', 'sex': 0, 'zyyz': '41008792', 'reg_end': 1760284800, 'zsdj': '注册监理工程师'}, {'name': '刘国瑜', 'id': '002105291846770714', 'zsbh': '建[造]11061125000608', 'zhtype': '房屋建筑工程,化工石油工程', 'sfz': '120109**********38', 'gsname': '北京华夏石化工程监理有限公司', 'sex': 0, 'zyyz': 'B11061125000608', 'reg_end': 1798646400, 'zsdj': '一级注册造价工程师'}, {'name': '张金涛', 'id': '002105291846771020', 'zsbh': '00538345', 'zhtype': '化工石油工程,市政公用工程', 'sfz': '410901**********57', 'gsname': '北京华夏石化工程监理有限公司', 'sex': 0, 'zyyz': '11016528', 'reg_end': 1764000000, 'zsdj': '注册监理工程师'}, {'name': '靳伟', 'id': '002105291846771048', 'zsbh': '京1112011201119084', 'zhtype': '房屋建筑工程,化工石油工程', 'sfz': '410503**********19', 'gsname': '北京华夏石化工程监理有限公司', 'sex': 0, 'zyyz': '京1112011201119084', 'reg_end': 1720713600, 'zsdj': '一级注册建造师'}, {'name': '马志友', 'id': '002105291846772723', 'zsbh': '00415919', 'zhtype': '机电安装工程,化工石油工程', 'sfz': '130323**********15', 'gsname': '北京华夏石化工程监理有限公司', 'sex': 0, 'zyyz': '11012735', 'reg_end': 1711987200, 'zsdj': '注册监理工程师'}, {'name': '邰宏杰', 'id': '002105291846772891', 'zsbh': '京1112006200807445', 'zhtype': '电力工程,化工石油工程', 'sfz': '210711**********14', 'gsname': '北京华夏石化工程监理有限公司', 'sex': 0, 'zyyz': '京1112006200807445', 'reg_end': 1720713600, 'zsdj': '一级注册建造师'}, {'name': '陈伟强', 'id': '002105291846773340', 'zsbh': '00486527', 'zhtype': '房屋建筑工程,化工石油工程', 'sfz': '130631**********39', 'gsname': '北京华夏石化工程监理有限公司', 'sex': 0, 'zyyz': '11014904', 'reg_end': 1713974400, 'zsdj': '注册监理工程师'}, {'name': '包鸿延', 'id': '002105291846773824', 'zsbh': '00227122', 'zhtype': '化工石油工程,房屋建筑工程', 'sfz': '622827**********10', 'gsname': '北京华夏石化工程监理有限公司', 'sex': 0, 'zyyz': '11005979', 'reg_end': 1753718400, 'zsdj': '注册监理工程师'}, {'name': '祝卫东', 'id': '002105291846774292', 'zsbh': '00432531', 'zhtype': '房屋建筑工程,化工石油工程', 'sfz': '220222**********14', 'gsname': '北京华夏石化工程监理有限公司', 'sex': 0, 'zyyz': '22003898', 'reg_end': 1740326400, 'zsdj': '注册监理工程师'}, {'name': '蒋浙梁', 'id': '002105291846774326', 'zsbh': '00437890', 'zhtype': '化工石油工程,房屋建筑工程', 'sfz': '230206**********14', 'gsname': '北京华夏石化工程监理有限公司', 'sex': 0, 'zyyz': '33013808', 'reg_end': 1747929600, 'zsdj': '注册监理工程师'}, {'name': '王彬', 'id': '002105291846774686', 'zsbh': '00553564', 'zhtype': '化工石油工程,房屋建筑工程', 'sfz': '230321**********35', 'gsname': '北京华夏石化工程监理有限公司', 'sex': 0, 'zyyz': '11017114', 'reg_end': 1676563200, 'zsdj': '注册监理工程师'}, {'name': '王长城', 'id': '002105291846775404', 'zsbh': '京1112011201119085', 'zhtype': '港口与航道工程,电力工程', 'sfz': '413022**********16', 'gsname': '北京华夏石化工程监理有限公司', 'sex': 0, 'zyyz': '京1112011201119085', 'reg_end': 1720281600, 'zsdj': '一级注册建造师'}, {'name': '李卫', 'id': '002105291846776257', 'zsbh': '00330982', 'zhtype': '市政公用工程,港口与航道工程', 'sfz': '430603**********17', 'gsname': '北京华夏石化工程监理有限公司', 'sex': 0, 'zyyz': '11010715', 'reg_end': 1695657600, 'zsdj': '注册监理工程师'}, {'name': '刘平顺', 'id': '002105291846777330', 'zsbh': '00506143', 'zhtype': '化工石油工程,房屋建筑工程', 'sfz': '622426**********18', 'gsname': '北京华夏石化工程监理有限公司', 'sex': 0, 'zyyz': '11015567', 'reg_end': 1734969600, 'zsdj': '注册监理工程师'}, {'name': '朱孔祥', 'id': '002105291846777994', 'zsbh': '00540596', 'zhtype': '市政公用工程,化工石油工程', 'sfz': '371312**********10', 'gsname': '北京华夏石化工程监理有限公司', 'sex': 0, 'zyyz': '11016625', 'reg_end': 1765209600, 'zsdj': '注册监理工程师'}, {'name': '白海东', 'id': '002105291846789790', 'zsbh': '京1332011201228080', 'zhtype': '化工石油工程,房屋建筑工程', 'sfz': '130228**********1X', 'gsname': '北京华夏石化工程监理有限公司', 'sex': 0, 'zyyz': '京1332011201228080', 'reg_end': 1720713600, 'zsdj': '一级注册建造师'}, {'name': '张亮', 'id': '002105291846793154', 'zsbh': '00576598', 'zhtype': '化工石油工程,房屋建筑工程', 'sfz': '210702**********13', 'gsname': '北京华夏石化工程监理有限公司', 'sex': 0, 'zyyz': '11017542', 'reg_end': 1694016000, 'zsdj': '注册监理工程师'}, {'name': '刘玉强', 'id': '002105291846810054', 'zsbh': '京1132016201824357', 'zhtype': '化工石油工程,房屋建筑工程', 'sfz': '130903**********10', 'gsname': '北京华夏石化工程监理有限公司', 'sex': 0, 'zyyz': '京1132016201824357', 'reg_end': 1748707200, 'zsdj': '一级注册建造师'}, {'name': '沈刚', 'id': '002105291846811627', 'zsbh': '00506144', 'zhtype': '机电安装工程,化工石油工程', 'sfz': '210404**********13', 'gsname': '北京华夏石化工程监理有限公司', 'sex': 0, 'zyyz': '11015568', 'reg_end': 1734969600, 'zsdj': '注册监理工程师'}, {'name': '张瑞', 'id': '002105291846811922', 'zsbh': '00191723', 'zhtype': '港口与航道工程,电力工程', 'sfz': '120109**********13', 'gsname': '北京华夏石化工程监理有限公司', 'sex': 0, 'zyyz': '11004505', 'reg_end': 1744560000, 'zsdj': '注册监理工程师'}, {'name': '刘雪梅', 'id': '002105291846812352', 'zsbh': '00477050', 'zhtype': '电力工程,市政公用工程', 'sfz': '150204**********25', 'gsname': '北京华夏石化工程监理有限公司', 'sex': 1, 'zyyz': '50004551', 'reg_end': 1704297600, 'zsdj': '注册监理工程师'}, {'name': '王凯', 'id': '002105291846812611', 'zsbh': '京1112016201908534', 'zhtype': '市政公用工程,房屋建筑工程', 'sfz': '232302**********18', 'gsname': '北京华夏石化工程监理有限公司', 'sex': 0, 'zyyz': '京1112016201908534', 'reg_end': 1766851200, 'zsdj': '一级注册建造师'}, {'name': '王抚顺', 'id': '002105291846812829', 'zsbh': '00394812', 'zhtype': '化工石油工程,市政公用工程', 'sfz': '120109**********31', 'gsname': '北京华夏石化工程监理有限公司', 'sex': 0, 'zyyz': '11006714', 'reg_end': 1677945600, 'zsdj': '注册监理工程师'}, {'name': '张金亮', 'id': '002105291846812862', 'zsbh': '00525369', 'zhtype': '化工石油工程,电力工程', 'sfz': '230125**********33', 'gsname': '北京华夏石化工程监理有限公司', 'sex': 0, 'zyyz': '11016294', 'reg_end': 1752595200, 'zsdj': '注册监理工程师'}, {'name': '贾晓锋', 'id': '002105291846813318', 'zsbh': '00469736', 'zhtype': '电力工程,化工石油工程', 'sfz': '370305**********11', 'gsname': '北京华夏石化工程监理有限公司', 'sex': 0, 'zyyz': '23001794', 'reg_end': 1689696000, 'zsdj': '注册监理工程师'}, {'name': '陆松鹤', 'id': '002105291846813487', 'zsbh': '00568965', 'zhtype': '化工石油工程,机电安装工程', 'sfz': '340403**********11', 'gsname': '北京华夏石化工程监理有限公司', 'sex': 0, 'zyyz': '11017434', 'reg_end': 1687449600, 'zsdj': '注册监理工程师'}, {'name': '李文乾', 'id': '002105291846814392', 'zsbh': '京1122013201408523', 'zhtype': '港口与航道工程,化工石油工程', 'sfz': '210623**********97', 'gsname': '北京华夏石化工程监理有限公司', 'sex': 0, 'zyyz': '京1122013201408523', 'reg_end': 1743868800, 'zsdj': '一级注册建造师'}, {'name': '葛永文', 'id': '002105291846814842', 'zsbh': '00278516', 'zhtype': '房屋建筑工程,市政公用工程', 'sfz': '330104**********13', 'gsname': '北京华夏石化工程监理有限公司', 'sex': 0, 'zyyz': '33002654', 'reg_end': 1744646400, 'zsdj': '注册监理工程师'}, {'name': '朱良', 'id': '002105291846815548', 'zsbh': '00524483', 'zhtype': '机电安装工程,港口与航道工程', 'sfz': '320222**********72', 'gsname': '北京华夏石化工程监理有限公司', 'sex': 0, 'zyyz': '11016284', 'reg_end': 1750694400, 'zsdj': '注册监理工程师'}, {'name': '丁威', 'id': '002105291846816072', 'zsbh': '京1112015201533914', 'zhtype': '电力工程,化工石油工程', 'sfz': '430682**********1X', 'gsname': '北京华夏石化工程监理有限公司', 'sex': 0, 'zyyz': '京1112015201533914', 'reg_end': 1720713600, 'zsdj': '一级注册建造师'}, {'name': '武延天', 'id': '002105291846816545', 'zsbh': '00601250', 'zhtype': '化工石油工程,房屋建筑工程', 'sfz': '142301**********10', 'gsname': '北京华夏石化工程监理有限公司', 'sex': 0, 'zyyz': '11017854', 'reg_end': 1716134400, 'zsdj': '注册监理工程师'}, {'name': '易炳权', 'id': '002105291846816811', 'zsbh': '00191741', 'zhtype': '电力工程,港口与航道工程', 'sfz': '120109**********18', 'gsname': '北京华夏石化工程监理有限公司', 'sex': 0, 'zyyz': '11004521', 'reg_end': 1744646400, 'zsdj': '注册监理工程师'}, {'name': '李子方', 'id': '002105291846816950', 'zsbh': '00601130', 'zhtype': '房屋建筑工程,化工石油工程', 'sfz': '410728**********12', 'gsname': '北京华夏石化工程监理有限公司', 'sex': 0, 'zyyz': '11017740', 'reg_end': 1716134400, 'zsdj': '注册监理工程师'}, {'name': '刘志杰', 'id': '002105291846817029', 'zsbh': '00433540', 'zhtype': '电力工程,化工石油工程', 'sfz': '130428**********70', 'gsname': '北京华夏石化工程监理有限公司', 'sex': 0, 'zyyz': '11013256', 'reg_end': 1743350400, 'zsdj': '注册监理工程师'}, {'name': '张志民', 'id': '002105291846817949', 'zsbh': '京1422009201311546', 'zhtype': '市政公用工程,化工石油工程', 'sfz': '420601**********35', 'gsname': '北京华夏石化工程监理有限公司', 'sex': 0, 'zyyz': '京1422009201311546', 'reg_end': 1763740800, 'zsdj': '一级注册建造师'}, {'name': '张超', 'id': '002105291846818050', 'zsbh': '00463390', 'zhtype': '机电安装工程,化工石油工程', 'sfz': '210402**********11', 'gsname': '北京华夏石化工程监理有限公司', 'sex': 0, 'zyyz': '21008651', 'reg_end': 1690732800, 'zsdj': '注册监理工程师'}, {'name': '陈保国', 'id': '002105291846818154', 'zsbh': '00547939', 'zhtype': '市政公用工程,房屋建筑工程', 'sfz': '410811**********76', 'gsname': '北京华夏石化工程监理有限公司', 'sex': 0, 'zyyz': '11016771', 'reg_end': 1768838400, 'zsdj': '注册监理工程师'}, {'name': '刘建楠', 'id': '002105291846818555', 'zsbh': '京1112013201323899', 'zhtype': '化工石油工程,电力工程', 'sfz': '130902**********30', 'gsname': '北京华夏石化工程监理有限公司', 'sex': 0, 'zyyz': '京1112013201323899', 'reg_end': 1757260800, 'zsdj': '一级注册建造师'}, {'name': '薄晓强', 'id': '002105291846819077', 'zsbh': '00302756', 'zhtype': '化工石油工程,市政公用工程', 'sfz': '140102**********12', 'gsname': '北京华夏石化工程监理有限公司', 'sex': 0, 'zyyz': '33006002', 'reg_end': 1689955200, 'zsdj': '注册监理工程师'}, {'name': '艾文', 'id': '002105291846857324', 'zsbh': '00572541', 'zhtype': '化工石油工程,房屋建筑工程', 'sfz': '362423**********15', 'gsname': '北京华夏石化工程监理有限公司', 'sex': 0, 'zyyz': '37020245', 'reg_end': 1690473600, 'zsdj': '注册监理工程师'}, {'name': '王毛毛', 'id': '002105291847880559', 'zsbh': '00519504', 'zhtype': '化工石油工程,房屋建筑工程', 'sfz': '410825**********30', 'gsname': '北京华夏石化工程监理有限公司', 'sex': 0, 'zyyz': '11016121', 'reg_end': 1745424000, 'zsdj': '注册监理工程师'}, {'name': '孙国斌', 'id': '002105291910276072', 'zsbh': '00330983', 'zhtype': '港口与航道工程,机电安装工程', 'sfz': '370502**********14', 'gsname': '北京华夏石化工程监理有限公司', 'sex': 0, 'zyyz': '11010716', 'reg_end': 1715529600, 'zsdj': '注册监理工程师'}, {'name': '田洪伟', 'id': '002105291910276951', 'zsbh': '00485548', 'zhtype': '房屋建筑工程,化工石油工程', 'sfz': '150403**********15', 'gsname': '北京华夏石化工程监理有限公司', 'sex': 0, 'zyyz': '44018105', 'reg_end': 1712592000, 'zsdj': '注册监理工程师'}, {'name': '刘康', 'id': '002105291910284841', 'zsbh': '00588265', 'zhtype': '化工石油工程,房屋建筑工程', 'sfz': '370305**********34', 'gsname': '北京华夏石化工程监理有限公司', 'sex': 0, 'zyyz': '11010647', 'reg_end': 1710086400, 'zsdj': '注册监理工程师'}, {'name': '孙寿红', 'id': '002105291910288058', 'zsbh': '00565255', 'zhtype': '机电安装工程,港口与航道工程', 'sfz': '230203**********12', 'gsname': '北京华夏石化工程监理有限公司', 'sex': 0, 'zyyz': '11011022', 'reg_end': 1733932800, 'zsdj': '注册监理工程师'}, {'name': '李承群', 'id': '002105291910295472', 'zsbh': '00600860', 'zhtype': '化工石油工程,电力工程', 'sfz': '370305**********17', 'gsname': '北京华夏石化工程监理有限公司', 'sex': 0, 'zyyz': '37021809', 'reg_end': 1716134400, 'zsdj': '注册监理工程师'}, {'name': '陈志刚', 'id': '002105291914336578', 'zsbh': '00191730', 'zhtype': '电力工程,化工石油工程', 'sfz': '430603**********34', 'gsname': '北京华夏石化工程监理有限公司', 'sex': 0, 'zyyz': '11004522', 'reg_end': 1744560000, 'zsdj': '注册监理工程师'}, {'name': '郭士川', 'id': '002105291915476222', 'zsbh': '京1232015201607265', 'zhtype': '电力工程,化工石油工程', 'sfz': '230207**********13', 'gsname': '北京华夏石化工程监理有限公司', 'sex': 0, 'zyyz': '京1232015201607265', 'reg_end': 1747238400, 'zsdj': '一级注册建造师'}, {'name': '王世昌', 'id': '002106112315433701', 'zsbh': '京1112019202004150', 'zhtype': '化工石油工程,电力工程', 'sfz': '130903**********17', 'gsname': '北京华夏石化工程监理有限公司', 'sex': 0, 'zyyz': '京1112019202004150', 'reg_end': 1744560000, 'zsdj': '一级注册建造师'}, {'name': '周平安', 'id': '002106152254554288', 'zsbh': '00610483', 'zhtype': '化工石油工程,房屋建筑工程', 'sfz': '622827**********17', 'gsname': '北京华夏石化工程监理有限公司', 'sex': 0, 'zyyz': '33023651', 'reg_end': 1717862400, 'zsdj': '注册监理工程师'}, {'name': '赵世阳', 'id': '002111142146370135', 'zsbh': '00639793', 'zhtype': '房屋建筑工程,化工石油工程', 'sfz': '220104**********14', 'gsname': '北京华夏石化工程监理有限公司', 'sex': 0, 'zyyz': '11005776', 'reg_end': 1731168000, 'zsdj': '注册监理工程师'}, {'name': '葛朝峰', 'id': '002111142146371409', 'zsbh': '00637060', 'zhtype': '化工石油工程,房屋建筑工程', 'sfz': '140311**********33', 'gsname': '北京华夏石化工程监理有限公司', 'sex': 0, 'zyyz': '37024149', 'reg_end': 1731168000, 'zsdj': '注册监理工程师'}, {'name': '张云峰', 'id': '002112032221844642', 'zsbh': '00650999', 'zhtype': '房屋建筑工程,化工石油工程', 'sfz': '320723**********15', 'gsname': '北京华夏石化工程监理有限公司', 'sex': 0, 'zyyz': '11019518', 'reg_end': 1732723200, 'zsdj': '注册监理工程师'}, {'name': '郑荫林', 'id': '002112302212868771', 'zsbh': '00656868', 'zhtype': '化工石油工程,机电安装工程', 'sfz': '210211**********31', 'gsname': '北京华夏石化工程监理有限公司', 'sex': 0, 'zyyz': '11020154', 'reg_end': 1734883200, 'zsdj': '注册监理工程师'}, {'name': '张领新', 'id': '002201182312421080', 'zsbh': '00662712', 'zhtype': '电力工程,机电安装工程', 'sfz': '130126**********13', 'gsname': '北京华夏石化工程监理有限公司', 'sex': 0, 'zyyz': '22006011', 'reg_end': 1736438400, 'zsdj': '注册监理工程师'}, {'name': '许军', 'id': '002202082329576501', 'zsbh': '00668636', 'zhtype': '房屋建筑工程,机电安装工程', 'sfz': '320705**********12', 'gsname': '北京华夏石化工程监理有限公司', 'sex': 0, 'zyyz': '32090913', 'reg_end': 1737734400, 'zsdj': '注册监理工程师'}, {'name': '高立华', 'id': '002209150009494235', 'zsbh': '00727893', 'zhtype': '机电安装工程,化工石油工程', 'sfz': '612424**********33', 'gsname': '北京华夏石化工程监理有限公司', 'sex': 0, 'zyyz': '11021340', 'reg_end': 1757260800, 'zsdj': '注册监理工程师'}, {'name': '尚军程', 'id': '002209150009494944', 'zsbh': '00727819', 'zhtype': '机电安装工程,房屋建筑工程', 'sfz': '622424**********13', 'gsname': '北京华夏石化工程监理有限公司', 'sex': 0, 'zyyz': '11021273', 'reg_end': 1757260800, 'zsdj': '注册监理工程师'}, {'name': '包苟丁', 'id': '002209150009495267', 'zsbh': '00727813', 'zhtype': '房屋建筑工程,化工石油工程', 'sfz': '622827**********30', 'gsname': '北京华夏石化工程监理有限公司', 'sex': 0, 'zyyz': '11021267', 'reg_end': 1757260800, 'zsdj': '注册监理工程师'}, {'name': '武立新', 'id': '002209150009495640', 'zsbh': '00727883', 'zhtype': '市政公用工程,化工石油工程', 'sfz': '232122**********18', 'gsname': '北京华夏石化工程监理有限公司', 'sex': 0, 'zyyz': '11021330', 'reg_end': 1757260800, 'zsdj': '注册监理工程师'}, {'name': '靳伟', 'id': '002105291846771048', 'zsbh': '京1112011201119084', 'zhtype': '建筑工程', 'sfz': '410503**********19', 'gsname': '北京华夏石化工程监理有限公司', 'sex': 0, 'zyyz': '京1112011201119084', 'reg_end': 1720713600, 'zsdj': '一级注册建造师'}, {'name': '邰宏杰', 'id': '002105291846772891', 'zsbh': '京1112006200807445', 'zhtype': '机电工程,建筑工程', 'sfz': '210711**********14', 'gsname': '北京华夏石化工程监理有限公司', 'sex': 0, 'zyyz': '京1112006200807445', 'reg_end': 1720713600, 'zsdj': '一级注册建造师'}, {'name': '陈伟强', 'id': '002105291846773340', 'zsbh': '00486527', 'zhtype': '建筑工程', 'sfz': '130631**********39', 'gsname': '北京华夏石化工程监理有限公司', 'sex': 0, 'zyyz': '11014904', 'reg_end': 1713974400, 'zsdj': '注册监理工程师'}, {'name': '王长城', 'id': '002105291846775404', 'zsbh': '京1112011201119085', 'zhtype': '建筑工程', 'sfz': '413022**********16', 'gsname': '北京华夏石化工程监理有限公司', 'sex': 0, 'zyyz': '京1112011201119085', 'reg_end': 1720281600, 'zsdj': '一级注册建造师'}, {'name': '白海东', 'id': '002105291846789790', 'zsbh': '京1332011201228080', 'zhtype': '建筑工程', 'sfz': '130228**********1X', 'gsname': '北京华夏石化工程监理有限公司', 'sex': 0, 'zyyz': '京1332011201228080', 'reg_end': 1720713600, 'zsdj': '一级注册建造师'}, {'name': '张亮', 'id': '002105291846793154', 'zsbh': '00576598', 'zhtype': '建筑工程', 'sfz': '210702**********13', 'gsname': '北京华夏石化工程监理有限公司', 'sex': 0, 'zyyz': '11017542', 'reg_end': 1694016000, 'zsdj': '注册监理工程师'}, {'name': '刘玉强', 'id': '002105291846810054', 'zsbh': '京1132016201824357', 'zhtype': '机电工程', 'sfz': '130903**********10', 'gsname': '北京华夏石化工程监理有限公司', 'sex': 0, 'zyyz': '京1132016201824357', 'reg_end': 1748707200, 'zsdj': '一级注册建造师'}, {'name': '王凯', 'id': '002105291846812611', 'zsbh': '京1112016201908534', 'zhtype': '机电工程', 'sfz': '232302**********18', 'gsname': '北京华夏石化工程监理有限公司', 'sex': 0, 'zyyz': '京1112016201908534', 'reg_end': 1766851200, 'zsdj': '一级注册建造师'}, {'name': '李文乾', 'id': '002105291846814392', 'zsbh': '京1122013201408523', 'zhtype': '机电工程', 'sfz': '210623**********97', 'gsname': '北京华夏石化工程监理有限公司', 'sex': 0, 'zyyz': '京1122013201408523', 'reg_end': 1743868800, 'zsdj': '一级注册建造师'}, {'name': '葛永文', 'id': '002105291846814842', 'zsbh': '00278516', 'zhtype': '建筑工程', 'sfz': '330104**********13', 'gsname': '北京华夏石化工程监理有限公司', 'sex': 0, 'zyyz': '33002654', 'reg_end': 1744646400, 'zsdj': '注册监理工程师'}, {'name': '丁威', 'id': '002105291846816072', 'zsbh': '京1112015201533914', 'zhtype': '机电工程', 'sfz': '430682**********1X', 'gsname': '北京华夏石化工程监理有限公司', 'sex': 0, 'zyyz': '京1112015201533914', 'reg_end': 1720713600, 'zsdj': '一级注册建造师'}, {'name': '张志民', 'id': '002105291846817949', 'zsbh': '京1422009201311546', 'zhtype': '机电工程', 'sfz': '420601**********35', 'gsname': '北京华夏石化工程监理有限公司', 'sex': 0, 'zyyz': '京1422009201311546', 'reg_end': 1763740800, 'zsdj': '一级注册建造师'}, {'name': '刘建楠', 'id': '002105291846818555', 'zsbh': '京1112013201323899', 'zhtype': '机电工程', 'sfz': '130902**********30', 'gsname': '北京华夏石化工程监理有限公司', 'sex': 0, 'zyyz': '京1112013201323899', 'reg_end': 1757260800, 'zsdj': '一级注册建造师'}, {'name': '艾文', 'id': '002105291846857324', 'zsbh': '00572541', 'zhtype': '水利水电工程', 'sfz': '362423**********15', 'gsname': '北京华夏石化工程监理有限公司', 'sex': 0, 'zyyz': '37020245', 'reg_end': 1690473600, 'zsdj': '注册监理工程师'}, {'name': '刘德运', 'id': '002105291847923551', 'zsbh': '建[造]14221100015847', 'zhtype': '机电工程', 'sfz': '410822**********38', 'gsname': '北京华夏石化工程监理有限公司', 'sex': 0, 'zyyz': 'B14221100015847', 'reg_end': 1788710400, 'zsdj': '一级注册造价工程师'}, {'name': '姜秀锋', 'id': '002105291848216296', 'zsbh': '京1212015201511881', 'zhtype': '建筑工程', 'sfz': '210213**********19', 'gsname': '北京华夏石化工程监理有限公司', 'sex': 0, 'zyyz': '京1212015201511881', 'reg_end': 1724428800, 'zsdj': '一级注册建造师'}, {'name': '张伟涛', 'id': '002105291902065154', 'zsbh': '00746527', 'zhtype': '市政公用工程', 'sfz': '130627**********15', 'gsname': '北京华夏石化工程监理有限公司', 'sex': 0, 'zyyz': '50003420', 'reg_end': 1764259200, 'zsdj': '注册监理工程师'}, {'name': '陈大伟', 'id': '002105291910264117', 'zsbh': '00367031', 'zhtype': '机电工程', 'sfz': '230103**********35', 'gsname': '北京华夏石化工程监理有限公司', 'sex': 0, 'zyyz': '22003296', 'reg_end': 1744560000, 'zsdj': '注册监理工程师'}, {'name': '张之平', 'id': '002105291910268208', 'zsbh': '00338740', 'zhtype': '机电工程', 'sfz': '120111**********12', 'gsname': '北京华夏石化工程监理有限公司', 'sex': 0, 'zyyz': '11004518', 'reg_end': 1744646400, 'zsdj': '注册监理工程师'}, {'name': '陈志刚', 'id': '002105291914336578', 'zsbh': '00191730', 'zhtype': '机电工程', 'sfz': '430603**********34', 'gsname': '北京华夏石化工程监理有限公司', 'sex': 0, 'zyyz': '11004522', 'reg_end': 1744560000, 'zsdj': '注册监理工程师'}, {'name': '郭士川', 'id': '002105291915476222', 'zsbh': '京1232015201607265', 'zhtype': '建筑工程', 'sfz': '230207**********13', 'gsname': '北京华夏石化工程监理有限公司', 'sex': 0, 'zyyz': '京1232015201607265', 'reg_end': 1747238400, 'zsdj': '一级注册建造师'}, {'name': '王世昌', 'id': '002106112315433701', 'zsbh': '京1112019202004150', 'zhtype': '机电工程', 'sfz': '130903**********17', 'gsname': '北京华夏石化工程监理有限公司', 'sex': 0, 'zyyz': '京1112019202004150', 'reg_end': 1744560000, 'zsdj': '一级注册建造师'}, {'name': '刘国瑜', 'id': '002105291846770714', 'zsbh': '建[造]11061125000608', 'zhtype': '土建', 'sfz': '120109**********38', 'gsname': '北京华夏石化工程监理有限公司', 'sex': 0, 'zyyz': 'B11061125000608', 'reg_end': 1798646400, 'zsdj': '一级注册造价工程师'}, {'name': '刘德运', 'id': '002105291847923551', 'zsbh': '建[造]14221100015847', 'zhtype': '安装', 'sfz': '410822**********38', 'gsname': '北京华夏石化工程监理有限公司', 'sex': 0, 'zyyz': 'B14221100015847', 'reg_end': 1788710400, 'zsdj': '一级注册造价工程师'}, {'name': '陈志刚', 'id': '002105291914336578', 'zsbh': '00191730', 'zhtype': '土建', 'sfz': '430603**********34', 'gsname': '北京华夏石化工程监理有限公司', 'sex': 0, 'zyyz': '11004522', 'reg_end': 1744560000, 'zsdj': '注册监理工程师'}], 'project': [{'prodetail': {'dataSource': 4, 'isMajor': 0, 'countyNum': 441351, 'cityNum': 441300, 'provinceNum': 440000, 'invPropertyNum': '103', 'dataLevel': 'C', 'prjFunctionNum': '700', 'prjPropertyNum': '001', 'prjApprovalLevelNum': '004', 'prjTypeNum': '01', 'prjSize': '15380.91㎡', 'buildCorpCode': 'MA556RMB-B', 'buildCorpName': '恒力石化（惠州）有限公司', 'prjApprovalDepart': '大亚湾工贸局', 'prjApprovalNum': '2020-441303-26-03-092403', 'address': '大亚湾石化区J1地块', 'prjName': '恒力石化(惠州)有限公司年产250万吨PTA-1项目(PTA主装置变配电室)', 'prjNum': '4413512109270002', 'prjCode': '2020-441303-26-03-092403', 'cREATEDATE': '2021-09-26', 'endDate': '2021-12-10', 'beginDate': '2021-04-20', 'prjApprovalDate': '2020-10-19', 'allArea': 331750.0, 'allInvest': 650000.0, 'nationalPercentTage': 0.0, 'provincePrjNum': '4413512109260102'}}, {'prodetail': {'countyNum': 420118, 'cityNum': 420100, 'provinceNum': 420000, 'dataLevel': 'C', 'prjApprovalLevelNum': '004', 'prjTypeNum': '01', 'buildCorpCode': '76463877-6', 'buildCorpName': '艾菲发动机零件（武汉）有限公司', 'prjApprovalNum': '2014010037250358', 'prjName': '艾菲发动机零件（武汉）有限公司二期厂房扩建', 'prjNum': '4201181502280101', 'cREATEDATE': '2015-02-28', 'allArea': 0.0, 'allInvest': 1700.0, 'provincePrjNum': '4201181502280102'}}, {'prodetail': {'countyNum': 420114, 'cityNum': 420100, 'provinceNum': 420000, 'dataLevel': 'C', 'prjApprovalLevelNum': '004', 'prjTypeNum': '01', 'buildCorpCode': '30374454-1', 'buildCorpName': '中法武汉生态示范城投资开发有限公司', 'prjApprovalNum': '蔡发改社会【2017】7号', 'prjName': '中法武汉生态示范城规划展示馆', 'prjNum': '4201141705050103', 'cREATEDATE': '2017-05-05', 'allArea': 0.0, 'allInvest': 20830.43, 'provincePrjNum': '4201141705050115'}}, {'prodetail': {'countyNum': 440301, 'cityNum': 440300, 'provinceNum': 440000, 'dataLevel': 'D', 'prjFunctionNum': '099', 'prjPropertyNum': '001', 'prjApprovalLevelNum': '003', 'prjTypeNum': '99', 'prjSize': '总投资额:59599万元；总面积为:80927.5平方米', 'buildCorpCode': '61883297-6', 'buildCorpName': '中国南山开发（集团）股份有限公司', 'prjApprovalNum': '深发改核准(2011)0234号', 'prjName': '南山宝湾物流中心项目', 'prjNum': '4403011409029904', 'cREATEDATE': '2014-09-02', 'allArea': 0.0, 'allInvest': 0.0, 'provincePrjNum': '4403011409029903'}}, {'prodetail': {'countyNum': 330402, 'cityNum': 330400, 'provinceNum': 330000, 'dataLevel': 'D', 'prjFunctionNum': '302', 'prjPropertyNum': '001', 'prjApprovalLevelNum': '004', 'prjTypeNum': '01', 'prjSize': '新建建筑面积76409.32m2，改建建筑面积34210.32m2', 'projectPlanNum': '建字第330402201600063号', 'buildPlanNum': '（2006）浙规证0450019', 'buildCorpName': '嘉兴颐莫尚置业有限公司', 'prjApprovalNum': '南外备发[2016]01号、南行审投外备[2016]03号', 'prjName': '欧尚超市嘉兴南湖店二期工程项目', 'prjNum': '3304021610120101', 'cREATEDATE': '2016-10-12', 'allArea': 76409.32, 'allInvest': 50000.0, 'provincePrjNum': '3304021610120101'}}, {'prodetail': {'countyNum': 310120, 'cityNum': 310000, 'provinceNum': 310000, 'dataLevel': 'A', 'prjFunctionNum': '999', 'prjPropertyNum': '001', 'prjApprovalLevelNum': '002', 'prjTypeNum': '99', 'prjSize': '本工程建设规模为6万立方米/日', 'buildCorpCode': '72946971-9', 'buildCorpName': '上海星火中法供水有限公司', 'prjApprovalNum': '沪发改环资（2013）118号', 'prjName': '星火水厂6万立方米/日深度处理和排泥水处理工程', 'prjNum': '3101201308209901', 'cREATEDATE': '2013-08-20', 'allArea': 0.0, 'allInvest': 7478.0, 'provincePrjNum': '1301FX0011'}}, {'prodetail': {'countyNum': 440902, 'cityNum': 440900, 'provinceNum': 440000, 'dataLevel': 'D', 'prjFunctionNum': '700', 'prjPropertyNum': '001', 'prjApprovalLevelNum': '004', 'prjTypeNum': '99', 'prjSize': '1.规划用地面积：205321.18平方米\n2.总建筑面积：8586.47平方米\n3.计容总建筑、构筑物面积：126474.50平方米\n4.基地面积：92228.49平方米\n5.容积率：0.61\n6.建筑密度：44.92%\n7.绿地率：20.00%\n8.建筑高度：14.50米', 'buildCorpCode': 'MA4UNFK7-2', 'buildCorpName': '茂名天源石化有限公司', 'prjApprovalNum': '2016-440902-26-03-006031', 'prjName': '10万吨/年丙烯项目', 'prjNum': '4409021807139901', 'cREATEDATE': '2018-07-13', 'allArea': 283000.0, 'allInvest': 34000.0, 'provincePrjNum': '4409021806299901'}}, {'prodetail': {'dataSource': 3, 'isMajor': 0, 'countyNum': 511921, 'cityNum': 511900, 'provinceNum': 510000, 'invPropertyNum': '100', 'dataLevel': 'D', 'prjFunctionNum': '300', 'prjPropertyNum': '001', 'prjTypeNum': '01', 'buildCorpCode': '915100007422747640', 'buildCorpName': '中国石油化工股份有限公司西南油气分公司', 'prjApprovalDepart': '/', 'address': '四川省巴中市通江县陈河镇', 'prjName': '陈河河坝气田嘉二气藏河坝101井区产能建设项目', 'prjNum': '5119212102040001', 'cREATEDATE': '2021-01-29', 'prjApprovalDate': '1900-01-01', 'allArea': 1805.0, 'allInvest': 853.51, 'provincePrjNum': '5119212101290102'}}, {'prodetail': {'cityNum': 469040, 'provinceNum': 460000, 'dataLevel': 'D', 'prjFunctionNum': '999', 'prjPropertyNum': '001', 'prjTypeNum': '01', 'projectPlanNum': '建字第2016-001号', 'buildPlanNum': '地字第2014-012号', 'buildCorpName': '海南汉地石油化工有限公司', 'prjName': '150万吨/年特种油及15万吨/年医药食品级白油项目之办公楼', 'prjNum': '4690401609080101', 'cREATEDATE': '2016-09-08', 'beginDate': '2017-05-11', 'allArea': 13610.55, 'allInvest': 7800.0, 'provincePrjNum': '4690401609080101'}}, {'prodetail': {'dataSource': 1, 'isMajor': 0, 'countyNum': 220214, 'cityNum': 220200, 'provinceNum': 220000, 'invPropertyNum': '103', 'dataLevel': 'C', 'prjFunctionNum': '700', 'prjPropertyNum': '001', 'prjApprovalLevelNum': '004', 'prjTypeNum': '01', 'cXXMInfo': '无', 'jZJNInfo': '屋面建筑和构筑物施工及使用过程中，合理使用能源，尽可能降低能耗。', 'prjSize': '总占地面积约30748.66平米，地上总建筑面积约21760.2平方米。20万吨/年丙烯腈含氰废水预处理装置以及配套污（油）泥、废液焚烧装置；园区工业污水处理装置；综合处理水量约750万吨/年。', 'fundSource': '企业自筹', 'buildCorpCode': '91220203MA84M5930T', 'buildCorpName': '吉林万邦达环保技术有限公司', 'prjApprovalDepart': '吉林市龙潭区发展和改革局', 'prjApprovalNum': '2021060822020303102697', 'address': '吉林省吉林市龙潭区八家子单元洛水街东侧', 'prjName': '吉林化工园区绿色循环经济资源综合利用项目', 'prjNum': '2202142202240008', 'prjCode': '2106-220203-04-01-950623', 'cREATEDATE': '2021-07-09', 'prjApprovalDate': '2021-06-08', 'allArea': 21760.2, 'allInvest': 51300.0, 'nationalPercentTage': 0.0, 'locationY': 43.937, 'locationX': 126.526, 'provincePrjNum': '2202142107270101'}}, {'prodetail': {'countyNum': 652223, 'cityNum': 652200, 'provinceNum': 650000, 'dataLevel': 'D', 'prjFunctionNum': '012', 'prjPropertyNum': '001', 'prjApprovalLevelNum': '004', 'prjTypeNum': '02', 'prjSize': '小型', 'projectPlanNum': '652223201800049', 'buildCorpCode': 'MA77QQHC-5', 'buildCorpName': '新疆宣东能源有限公司', 'prjApprovalNum': '2018  28', 'prjName': '新疆广汇清洁炼化至宣力环保能源煤气输送临时管线项目', 'prjNum': '6522231810200003', 'cREATEDATE': '2018-07-17', 'endDate': '2018-11-17', 'beginDate': '2018-05-02', 'allArea': 6556.46, 'allInvest': 4499.0, 'provincePrjNum': '652223201807170201'}}, {'prodetail': {'cityNum': 110000, 'provinceNum': 110000, 'dataLevel': 'D', 'prjTypeNum': '99', 'buildCorpName': '中国石油化工股份有限公司北京石油分公司', 'prjName': '康庄油库改造工程(监理)', 'prjNum': '1100001907091899', 'cREATEDATE': '2009-08-20', 'allInvest': 41.3, 'provincePrjNum': '11022920090031'}}, {'prodetail': {'countyNum': 440301, 'cityNum': 440300, 'provinceNum': 440000, 'dataLevel': 'D', 'prjFunctionNum': '100', 'prjPropertyNum': '001', 'prjApprovalLevelNum': '003', 'prjTypeNum': '01', 'prjSize': '总投资额:300000万元；总面积为:平方米', 'buildCorpCode': '61883297-6', 'buildCorpName': '中国南山开发（集团）股份有限公司', 'prjApprovalNum': '深南山发改核准(2016)0026号', 'prjName': '赤湾地铁站城市综合体项目', 'prjNum': '4403011612130102', 'cREATEDATE': '2016-12-13', 'allArea': 1.0, 'allInvest': 0.0, 'provincePrjNum': '4403011612130102'}}, {'prodetail': {'countyNum': 330101, 'cityNum': 330100, 'provinceNum': 330000, 'dataLevel': 'D', 'prjTypeNum': '01', 'projectPlanNum': '建字第330100201200447号', 'buildCorpName': '杭州市燃气集团有限公司', 'prjName': '杭州市东部LNG应急气源站', 'prjNum': '3301011304020103', 'cREATEDATE': '2013-04-02', 'provincePrjNum': '3301251304020101'}}, {'prodetail': {'dataSource': 4, 'isMajor': 0, 'countyNum': 440305, 'cityNum': 440300, 'provinceNum': 440000, 'invPropertyNum': '100', 'dataLevel': 'B', 'prjFunctionNum': '999', 'prjPropertyNum': '099', 'prjApprovalLevelNum': '003', 'prjTypeNum': '99', 'prjSize': '该项目地块位于南山区招商街道赤湾片区，北邻港航路，西接赤湾三路，南邻赤湾六路，东邻花香街，用地性质为二类居住用地，总用地面积11154.49平方米，拟建设2栋住宅楼，总建筑面积约76025.6平方米，其中计规定建筑面积50206平方米（住宅50106平方米、物业服务用房100平方米），地上核增面积约为2797.6平方米，地下核增面积约为23022平方米。', 'buildCorpCode': 'MA5FDRK8-8', 'buildCorpName': '深圳市海越锦实业发展有限公司', 'prjApprovalDepart': '深圳市发展和改革委员会', 'prjApprovalNum': '2108-440305-04-01-333721', 'address': '赤湾六路北侧、港航路西侧', 'prjName': '赤湾琅玥湾佳园', 'prjNum': '4403052108180003', 'prjCode': '2108-440305-04-01-333721', 'cREATEDATE': '2021-08-16', 'prjApprovalDate': '2021-08-16', 'allInvest': 133293.0, 'nationalPercentTage': 0.0, 'provincePrjNum': '4403052108169913'}}, {'prodetail': {'countyNum': 330901, 'cityNum': 330900, 'provinceNum': 330000, 'dataLevel': 'C', 'prjFunctionNum': '700', 'prjPropertyNum': '001', 'prjApprovalLevelNum': '002', 'prjTypeNum': '01', 'prjSize': '工程主要建设内容包括2座16万m3 LNG储罐及配套罐内设施和LNG外输工艺系统设施。考虑到与新增储罐配套及工艺调峰需求，LNG工艺系统拟增加150万吨/年的气化外输能力，50万吨T/年的液态外输能力，二期规模为200万吨/年，总投资约24亿元人民币，计划于2020年10月建成投产。', 'projectPlanNum': '建字第聚【2019】003号', 'buildCorpCode': '913309000692086510', 'buildCorpName': '新奥（舟山）液化天然气有限公司', 'prjApprovalNum': '浙发改能源【2018】568号', 'prjName': '浙江舟山液化天然气（LNG）接收及加注站 二期项目', 'prjNum': '3309011904270002', 'cREATEDATE': '2019-04-26', 'allArea': 5621.22, 'allInvest': 4840.0, 'provincePrjNum': '3309011904260101'}}, {'prodetail': {'countyNum': 121120, 'cityNum': -1, 'provinceNum': 120000, 'dataLevel': 'D', 'prjFunctionNum': '999', 'prjPropertyNum': '001', 'prjTypeNum': '01', 'prjSize': '4134.70平方米', 'projectPlanNum': '2015保税建证0007', 'buildPlanNum': '2014保税地证1018', 'buildCorpName': '道达尔(天津)工业有限公司', 'prjApprovalNum': '津保发改许可[2014]57号', 'prjName': '道达尔润滑脂生产加工、仓储项目监理', 'prjNum': '1211201504280101', 'cREATEDATE': '2015-04-28', 'endDate': '2016-03-01', 'beginDate': '2015-04-30', 'allArea': 4134.7, 'allInvest': 114.48, 'provincePrjNum': 'HJL20150804200520663'}}, {'prodetail': {'countyNum': 150625, 'cityNum': 150600, 'provinceNum': 150000, 'dataLevel': 'D', 'prjFunctionNum': '700', 'prjPropertyNum': '001', 'prjApprovalLevelNum': '002', 'prjTypeNum': '01', 'prjSize': '75000平方米', 'buildCorpCode': '69592228-9', 'buildCorpName': '内蒙古伊泰化工有限责任公司', 'prjApprovalNum': '内发改产业字[2012]2431号', 'prjName': '内蒙古伊泰化工有限责任公司120万吨/年精细化学品项目建筑、安装工程', 'prjNum': '1506251712270103', 'cREATEDATE': '2017-12-27', 'allArea': 75000.0, 'allInvest': 5799.01, 'provincePrjNum': 'B15062517122701005'}}, {'prodetail': {'dataSource': 4, 'isMajor': 0, 'countyNum': 220214, 'cityNum': 220200, 'provinceNum': 220000, 'invPropertyNum': '103', 'dataLevel': 'C', 'prjFunctionNum': '011', 'prjPropertyNum': '001', 'prjTypeNum': '01', 'prjSize': '管道长度：58米', 'buildCorpCode': '91220203MA84M5930T', 'buildCorpName': '吉林万邦达环保技术有限公司', 'prjApprovalDepart': '吉林市龙潭区发展和改革局', 'address': '龙潭区珠江路', 'prjName': '吉林化工园区绿色循环经济资源综合利用项目', 'prjNum': '2202142206010001', 'prjCode': '2106-220203-04-01-950623', 'cREATEDATE': '2022-05-15', 'prjApprovalDate': '2021-06-08', 'allArea': 20281.2, 'allInvest': 51300.0, 'provincePrjNum': '2202142205310101'}}, {'prodetail': {'countyNum': 440305, 'cityNum': 440300, 'provinceNum': 440000, 'dataLevel': 'D', 'prjFunctionNum': '999', 'prjPropertyNum': '099', 'prjApprovalLevelNum': '003', 'prjTypeNum': '99', 'prjSize': '该项目土地类别为R2，二类居住用地。总用地面积11157平方米，拟建设2栋住宅楼，总建筑面积为73112.5平方米，其中计容建筑面积50206.5平方米；不计容建筑面积约22906平方米（包含地下室建筑面积约13727平方米）。项目南侧为赤湾六路，西侧为赤湾三路。', 'buildCorpCode': '618832976', 'buildCorpName': '中国南山开发（集团）股份有限公司', 'prjApprovalNum': '2018-440305-70-02-719006', 'prjName': '赤湾庙北03-02-10地块项目', 'prjNum': '4403051907190041', 'cREATEDATE': '2019-07-11', 'allArea': 0.0, 'allInvest': 51704.0, 'provincePrjNum': '4403051811229911'}}, {'prodetail': {'dataSource': 4, 'isMajor': 0, 'countyNum': 441351, 'cityNum': 441300, 'provinceNum': 440000, 'invPropertyNum': '103', 'dataLevel': 'C', 'prjFunctionNum': '700', 'prjPropertyNum': '001', 'prjApprovalLevelNum': '004', 'prjTypeNum': '01', 'prjSize': '新建海水泵房及J1地块、J2地块、M1-1地块等地基处理工程', 'buildCorpCode': 'MA556RMB-B', 'buildCorpName': '恒力石化（惠州）有限公司', 'prjApprovalDepart': '无', 'prjApprovalNum': '大亚湾工贸局', 'address': '惠州市大亚湾石化区J1地块、J2地块、M1-1地块、M1-2地块', 'prjName': '恒力石化PTA仓库、海水泵房及主项目基坑工程(海水泵房)', 'prjNum': '4413512012310001', 'prjCode': '2020-441303-26-03-103763', 'cREATEDATE': '2020-12-30', 'endDate': '2022-02-18', 'beginDate': '2020-12-18', 'prjApprovalDate': '2020-11-20', 'allArea': 2903.0, 'allInvest': 2880.0, 'nationalPercentTage': 0.0, 'provincePrjNum': '4413512012300101'}}, {'prodetail': {'countyNum': 420116, 'cityNum': 420100, 'provinceNum': 420000, 'dataLevel': 'C', 'prjApprovalLevelNum': '004', 'prjTypeNum': '01', 'buildCorpCode': '914201163035996', 'buildCorpName': '武汉传祥物联网技术有限公司', 'prjApprovalNum': '20170116588900034', 'prjName': '中国智能骨干网武汉黄陂核心节点项目（二期）', 'prjNum': '4201161707110101', 'cREATEDATE': '2017-07-11', 'allArea': 0.0, 'allInvest': 19000.0, 'provincePrjNum': '4201161707110115'}}, {'prodetail': {'countyNum': 330101, 'cityNum': 330100, 'provinceNum': 330000, 'dataLevel': 'D', 'prjTypeNum': '01', 'buildCorpName': '玫琳凯（中国）化妆品有限公司', 'prjName': '扩建生产厂房', 'prjNum': '3301011404030104', 'cREATEDATE': '2014-04-03', 'provincePrjNum': '3301251404030101'}}, {'prodetail': {'countyNum': 320581, 'cityNum': 320500, 'provinceNum': 320000, 'dataLevel': 'D', 'prjFunctionNum': '999', 'prjPropertyNum': '001', 'prjApprovalLevelNum': '   ', 'prjTypeNum': '01', 'buildCorpCode': 'MA1TF6E1-0', 'buildCorpName': '常熟市尚源房地产开发有限公司', 'prjApprovalNum': '常发改核(2018)6号', 'prjName': '常熟市2017A-015号地块商住用房项目', 'prjNum': '3205811806050177', 'cREATEDATE': '2018-06-05', 'allArea': 254007.6, 'allInvest': 300015.79, 'provincePrjNum': '3205811802050104'}}, {'prodetail': {'provinceNum': 320000, 'prjNum': '3205811806050177', 'prjApprovalNum': '常发改核(2018)6号', 'cityNum': 320500, 'prjPropertyNum': '001', 'prjName': '常熟市2017A-015号地块商住用房项目', 'provincePrjNum': '3205811802050104', 'cREATEDATE': '2018-06-05', 'prjFunctionNum': '999', 'prjTypeNum': '01', 'allInvest': 300015.79, 'buildCorpName': '常熟市尚源房地产开发有限公司', 'buildCorpCode': 'MA1TF6E1-0', 'allArea': 254007.6, 'prjApprovalLevelNum': '   ', 'countyNum': 320581, 'dataLevel': 'D'}}, {'prodetail': {'provinceNum': 320000, 'prjNum': '3205811806050177', 'prjApprovalNum': '常发改核(2018)6号', 'cityNum': 320500, 'prjPropertyNum': '001', 'prjName': '常熟市2017A-015号地块商住用房项目', 'provincePrjNum': '3205811802050104', 'cREATEDATE': '2018-06-05', 'prjFunctionNum': '999', 'prjTypeNum': '01', 'allInvest': 300015.79, 'buildCorpName': '常熟市尚源房地产开发有限公司', 'buildCorpCode': 'MA1TF6E1-0', 'allArea': 254007.6, 'prjApprovalLevelNum': '   ', 'countyNum': 320581, 'dataLevel': 'D'}}, {'prodetail': {'provinceNum': 320000, 'prjNum': '3205811806050177', 'prjApprovalNum': '常发改核(2018)6号', 'cityNum': 320500, 'prjPropertyNum': '001', 'prjName': '常熟市2017A-015号地块商住用房项目', 'provincePrjNum': '3205811802050104', 'cREATEDATE': '2018-06-05', 'prjFunctionNum': '999', 'prjTypeNum': '01', 'allInvest': 300015.79, 'buildCorpName': '常熟市尚源房地产开发有限公司', 'buildCorpCode': 'MA1TF6E1-0', 'allArea': 254007.6, 'prjApprovalLevelNum': '   ', 'countyNum': 320581, 'dataLevel': 'D'}}, {'prodetail': {'countyNum': 420118, 'cityNum': 420100, 'provinceNum': 420000, 'dataLevel': 'C', 'prjApprovalLevelNum': '004', 'prjTypeNum': '01', 'buildCorpCode': '07050734-1', 'buildCorpName': '武汉亚洲医院有限公司', 'prjApprovalNum': '武经开发改核【2015】2号', 'prjName': '武汉亚洲医院', 'prjNum': '4201181507030101', 'cREATEDATE': '2015-07-03', 'allArea': 0.0, 'allInvest': 101555.23, 'provincePrjNum': '4201181507030101'}}, {'prodetail': {'countyNum': 310112, 'cityNum': 310000, 'provinceNum': 310000, 'dataLevel': 'A', 'prjFunctionNum': '004', 'prjPropertyNum': '001', 'prjApprovalLevelNum': '004', 'prjTypeNum': '01', 'buildCorpCode': '05931502-3', 'buildCorpName': '液化空气（中国）研发有限公司', 'prjApprovalNum': '闵发改产核【2014】8号', 'prjName': '低温制冷设备制造及工艺开发项目', 'prjNum': '3101121402240101', 'cREATEDATE': '2014-02-24', 'allArea': 15717.0, 'allInvest': 15211.0, 'provincePrjNum': '1402MH0034'}}, {'prodetail': {'countyNum': 150625, 'cityNum': 150600, 'provinceNum': 150000, 'dataLevel': 'D', 'prjFunctionNum': '   ', 'prjPropertyNum': '   ', 'prjApprovalLevelNum': '   ', 'prjTypeNum': '01', 'prjSize': '6529.84平方米', 'buildCorpName': '内蒙古伊泰化工有限责任公司', 'prjName': '尾气制氢、第三循环水装置', 'prjNum': '1506251706070118', 'cREATEDATE': '2017-06-07', 'allArea': 6529.84, 'allInvest': 2939.86, 'provincePrjNum': '1506251706070121'}}, {'prodetail': {'dataSource': 4, 'isMajor': 0, 'countyNum': 441351, 'cityNum': 441300, 'provinceNum': 440000, 'invPropertyNum': '200', 'dataLevel': 'C', 'prjFunctionNum': '700', 'prjPropertyNum': '001', 'prjApprovalLevelNum': '002', 'prjTypeNum': '99', 'prjSize': '508900平方米', 'buildCorpCode': 'MA52TDXD-D', 'buildCorpName': '埃克森美孚（惠州）化工有限公司', 'prjApprovalDepart': '广东省发展和改革委员会', 'prjApprovalNum': '2019-441303-26-02-005879', 'address': '惠州市大亚湾石化区', 'prjName': '埃克森美孚惠州乙烯一期项目强夯工程(三标段)', 'prjNum': '4413512106190003', 'prjCode': '2019-441303-26-02-005879', 'cREATEDATE': '2021-06-18', 'endDate': '2021-12-31', 'beginDate': '2021-06-20', 'prjApprovalDate': '2021-02-18', 'allArea': 3170000.0, 'allInvest': 8500.0, 'nationalPercentTage': 0.0, 'provincePrjNum': '4413512106189901'}}, {'prodetail': {'countyNum': 110229, 'cityNum': 110000, 'provinceNum': 110000, 'dataLevel': 'D', 'prjTypeNum': '01', 'prjSize': '6', 'projectPlanNum': '2009规（延）建字0022号', 'buildCorpCode': '-', 'buildCorpName': '中国石油化工股份有限公司北京石油分公司', 'prjName': '康庄油库改造工程', 'prjNum': '1102290908140101', 'cREATEDATE': '2009-08-14', 'endDate': '2009-10-15', 'beginDate': '2009-08-01', 'allInvest': 1249.88, 'provincePrjNum': '11022920090024'}}, {'prodetail': {'dataSource': 4, 'isMajor': 0, 'countyNum': 220214, 'cityNum': 220200, 'provinceNum': 220000, 'invPropertyNum': '103', 'dataLevel': 'C', 'prjFunctionNum': '700', 'prjPropertyNum': '001', 'prjTypeNum': '01', 'prjSize': '建设规模：总占地面积30748.66平米，地上总建筑面积约21760.2平方米。20万吨/年丙烯腈含氰废水预处理装置以及配套污（油）泥、废液焚烧装置；园区工业污水处理装置；综合处理水量约750万吨/年。主要建设内容：建设办公楼约4293平方米；厂房约13700.6平方米；池体约12890平方米；罐区约4501.26平方米。购置安装分离沉淀加药装置、蒸发器、焚烧炉、臭氧系统、冷却塔、循环水处理装置、膜分离系统、格栅、搅拌机、泵类、气动阀门等设备约680台套。', 'buildCorpCode': '91220203MA84M5930T', 'buildCorpName': '吉林万邦达环保技术有限公司', 'prjApprovalDepart': '吉林市龙潭区发展和改革局', 'address': '龙潭区汉江路', 'prjName': '吉林化工园区绿色循环经济资源综合利用项目', 'prjNum': '2202142202240009', 'prjCode': '2106-220203-04-01-950623', 'cREATEDATE': '2021-11-18', 'prjApprovalDate': '2021-06-08', 'allArea': 20281.2, 'allInvest': 51300.0, 'provincePrjNum': '2202142111190101'}}, {'prodetail': {'countyNum': 210212, 'cityNum': 210200, 'provinceNum': 210000, 'dataLevel': 'D', 'prjTypeNum': '01', 'prjSize': '48686.57平方米', 'buildCorpName': '中石化催化剂大连有限公司', 'prjName': '中石化催化剂大连有限公司催化剂大连基地（一期）建设', 'prjNum': '2102121511120101', 'cREATEDATE': '2015-11-12', 'allArea': 48686.57, 'allInvest': 21540.42, 'provincePrjNum': '210212201511121001'}}, {'prodetail': {'countyNum': 440414, 'cityNum': 440400, 'provinceNum': 440000, 'dataLevel': 'D', 'prjFunctionNum': '800', 'prjPropertyNum': '001', 'prjApprovalLevelNum': '003', 'prjTypeNum': '99', 'prjSize': '年产10万吨水性树脂、年产4万吨改性聚氨酯树脂', 'buildCorpCode': '06218595-2', 'buildCorpName': '万华化学（广东）有限公司', 'prjApprovalNum': '130404265910254', 'prjName': '万华化学(广东)有限公司特种聚氨酯项目', 'prjNum': '4404141611189901', 'cREATEDATE': '2016-11-18', 'allArea': 230000.0, 'allInvest': 100240.0, 'provincePrjNum': '4404141611189901'}}, {'prodetail': {'dataSource': 1, 'isMajor': 1, 'countyNum': 350122, 'cityNum': 350100, 'provinceNum': 350000, 'invPropertyNum': '100', 'dataLevel': 'C', 'prjFunctionNum': '800', 'prjPropertyNum': '001', 'prjApprovalLevelNum': '004', 'prjTypeNum': '01', 'prjSize': '建设40万吨/年聚酰胺一体化生产线，其中第一期建设包括1条20万吨/年聚酰胺生产线，配套1条20万吨/年己内酰胺生产线、20万吨/环己酮生产线、40万吨/年发烟硫酸生产线、公用工程和辅助生产装置。第二期建设包括1条20万吨/年聚酰胺生产线，配套1条20万吨/年己内酰胺生产线、20万吨/环己酮生产线及公用工程和辅助生产装置；主工艺采用德国吉玛工艺、瑞士伊文达工艺、荷兰皇家帝斯曼HPO工艺，技术水平国际先进。', 'fundSource': '企业自有及银行贷款', 'projectPlanNum': '-', 'buildPlanNum': '-', 'buildCorpCode': '91350122062297284K', 'buildCorpName': '福建申远新材料有限公司', 'prjApprovalDepart': '连江县发展和改革局', 'prjApprovalNum': '闽发改备[2013]A12076', 'address': '福建省福州市连江县可门工业园区', 'prjName': '年产40万吨聚酰胺一体化项目', 'prjNum': '3501222107220004', 'prjCode': '2018-350122-26-03-007365', 'cREATEDATE': '2021-07-21', 'prjApprovalDate': '2013-11-11', 'allInvest': 911137.77, 'nationalPercentTage': 0.0, 'provincePrjNum': '3501222107210191'}}, {'prodetail': {'dataSource': 4, 'isMajor': 0, 'countyNum': 440414, 'cityNum': 440400, 'provinceNum': 440000, 'invPropertyNum': '102', 'dataLevel': 'C', 'prjFunctionNum': '700', 'prjPropertyNum': '003', 'prjApprovalLevelNum': '004', 'prjTypeNum': '01', 'prjSize': '建筑面积17017平方米，占地面积7718平方米。项目生产10万吨/年水性树脂。包括：PUD、PA、OH-PA。总设计产能10万吨/年，其中PUD生产线2.1万吨/年、PA线7.55万吨/年、OHPA线0.35万吨/年、低挥发丙烯酸乳液8万吨/年。主要设备反应釜采用外夹套、外盘管形式，另外，塔类选择丙酮回收塔和尾气吸收塔。项目总投资：37104.00万元   项目资本金：7420.80万元\n其中：土建投资：7332.00万元  设备及技术投资14080.00万元；进口设备用汇：0.00万美元', 'buildCorpCode': '06218595-5', 'buildCorpName': '万华化学（广东）有限公司', 'prjApprovalDepart': '高栏港经济区发展和改革局', 'prjApprovalNum': '440404-26-03-804499', 'address': '石油化工区平湾三路东北侧', 'prjName': '万华化学(广东)有限公司水性树脂二期项目', 'prjNum': '4404142006280004', 'prjCode': '2018-440404-26-03-804499', 'cREATEDATE': '2020-06-24', 'prjApprovalDate': '2018-04-16', 'allArea': 17017.0, 'allInvest': 37104.0, 'nationalPercentTage': 100.0, 'provincePrjNum': '4404142006240101'}}, {'prodetail': {'countyNum': 121120, 'cityNum': -1, 'provinceNum': 120000, 'dataLevel': 'D', 'prjFunctionNum': '999', 'prjPropertyNum': '001', 'prjTypeNum': '01', 'prjSize': '4134.70平方米', 'projectPlanNum': '2015津保建证0007', 'buildPlanNum': '2014保税地证1018', 'buildCorpName': '道达尔(天津)工业有限公司', 'prjApprovalNum': '津保发改许可[2014]37号', 'prjName': '道达尔润滑脂生产加工、仓储项目施工', 'prjNum': '1211201507100101', 'cREATEDATE': '2015-07-10', 'endDate': '2016-03-01', 'beginDate': '2015-07-25', 'allArea': 4134.7, 'allInvest': 900.0, 'provincePrjNum': 'ZB20150710200030950'}}, {'prodetail': {'countyNum': 440301, 'cityNum': 440300, 'provinceNum': 440000, 'dataLevel': 'D', 'prjFunctionNum': '100', 'prjPropertyNum': '001', 'prjApprovalLevelNum': '003', 'prjTypeNum': '01', 'prjSize': '总建筑面积138340平方米', 'buildCorpCode': 'MA5EM1UD-9', 'buildCorpName': '赤湾科技（深圳）有限公司', 'prjApprovalNum': '深南山发改核准(2018)0002号', 'prjName': '南山赤湾科苑项目', 'prjNum': '4403011804260101', 'cREATEDATE': '2018-04-26', 'allArea': 0.0, 'allInvest': 200000.0, 'provincePrjNum': '4403011804260101'}}, {'prodetail': {'countyNum': 440890, 'cityNum': 440800, 'provinceNum': 440000, 'dataLevel': 'D', 'prjFunctionNum': '100', 'prjPropertyNum': '001', 'prjApprovalLevelNum': '004', 'prjTypeNum': '01', 'prjSize': '占地60000平方米，总建筑面积77867平方米，其中一期50585平方米，二期27282平方米，主要建筑倒班公寓楼（18层5栋、14层7栋）42171平方米、1层体育馆3600平方米、食堂综合楼6816平方米、服务配套中心320平方米）', 'buildCorpCode': '59006190-2', 'buildCorpName': '中科（广东）炼化有限公司', 'prjApprovalNum': '2017-440800-47-03-004493', 'prjName': '中科合资广东炼化一体化项目职工之家项目', 'prjNum': '4408901804260101', 'cREATEDATE': '2018-04-26', 'allArea': 77867.0, 'allInvest': 31443.65, 'provincePrjNum': '4408901804260101'}}, {'prodetail': {'countyNum': 310105, 'cityNum': 310000, 'provinceNum': 310000, 'dataLevel': 'A', 'prjFunctionNum': '999', 'prjPropertyNum': '006', 'prjApprovalLevelNum': '004', 'prjTypeNum': '99', 'prjSize': '在租赁的蒲松北路10号（新泾港旧区改造地块一期）进行家乐福长宁店室内装修安装工程，装修安装工程总建筑面积：15239 m2，总投资1500万元。', 'buildCorpCode': '60732082-8', 'buildCorpName': '上海联家超市有限公司', 'prjApprovalNum': '20170901', 'prjName': '家乐福上海天山西路店内装修工程', 'prjNum': '3101051710169902', 'cREATEDATE': '2017-10-16', 'allArea': 0.0, 'allInvest': 1500.0, 'provincePrjNum': '1702CN0142'}}, {'prodetail': {'countyNum': 440803, 'cityNum': 440800, 'provinceNum': 440000, 'dataLevel': 'D', 'prjFunctionNum': '099', 'prjPropertyNum': '003', 'prjApprovalLevelNum': '004', 'prjTypeNum': '99', 'prjSize': '1.本项目共7座储罐，罐区库容3.85万立方米，分别为10000立方米储罐1个(汽油), 8000立方米储罐1个(汽油), 6500立方米储罐1个(柴油), 5000立方米储罐1个(柴油), 3000立方米储罐3个(2柴1汽)。2.油泵棚72平方米，高4.4米;雨水池97.2平方米;隔油池150立方米。\n', 'buildCorpCode': '61780584-5', 'buildCorpName': '湛江凌志润滑油有限公司', 'prjApprovalNum': '140803589010042/湛霞发改字(2016)7号', 'prjName': '湛江凌志润滑油有限公司油库工程', 'prjNum': '4408031607289901', 'cREATEDATE': '2016-07-28', 'allArea': 1696.0, 'allInvest': 21010.0, 'provincePrjNum': '4408031607289901'}}, {'prodetail': {'dataSource': 1, 'isMajor': 0, 'cityNum': 469040, 'provinceNum': 460000, 'invPropertyNum': '100', 'dataLevel': 'D', 'prjFunctionNum': '999', 'prjPropertyNum': '099', 'prjTypeNum': '99', 'buildCorpCode': '其它', 'buildCorpName': '中国石化海南炼油化工有限公司', 'prjApprovalDepart': '无', 'address': '炼油厂区及洋浦石化功能区', 'prjName': '100万吨/年乙烯及炼油改扩建工程', 'prjNum': '4600002009040004', 'cREATEDATE': '2020-08-28', 'prjApprovalDate': '1900-01-01', 'allArea': 120000.0, 'allInvest': 2810000.0, 'provincePrjNum': '4690402008280101'}}, {'prodetail': {'countyNum': 330101, 'cityNum': 330100, 'provinceNum': 330000, 'dataLevel': 'D', 'prjTypeNum': '01', 'buildCorpName': '玫琳凯（中国）化妆品有限公司', 'prjName': '扩建生产厂房工程项目桩基', 'prjNum': '3301011311280103', 'cREATEDATE': '2013-11-28', 'provincePrjNum': '3301251311280102'}}, {'prodetail': {'dataSource': 4, 'isMajor': 0, 'countyNum': 440404, 'cityNum': 440400, 'provinceNum': 440000, 'invPropertyNum': '102', 'dataLevel': 'C', 'prjFunctionNum': '999', 'prjPropertyNum': '001', 'prjApprovalLevelNum': '004', 'prjTypeNum': '99', 'prjSize': '建筑面积715.95平方米，占地面积578.05平方米。本项目内容为增设RTO设备、板框压滤设备、变配电室等配套设施，优化环保处理能力，提高生产效益。主要设备是RTO设备及板框压滤机等。', 'buildCorpCode': '06218595-2', 'buildCorpName': '万华化学（广东）有限公司', 'prjApprovalDepart': '珠海市金湾区发展和改革局', 'prjApprovalNum': '2112-440404-04-05-629469', 'address': '珠海市金湾区南水镇石化六路1004号', 'prjName': '万华广东园区环保改造项目', 'prjNum': '4404042209140002', 'prjCode': '2112-440404-04-05-629469', 'cREATEDATE': '2022-09-09', 'endDate': '2022-10-31', 'beginDate': '2022-08-15', 'prjApprovalDate': '2021-12-27', 'allArea': 594.8, 'allInvest': 1316.0, 'nationalPercentTage': 100.0, 'provincePrjNum': '4404042209090002'}}, {'prodetail': {'countyNum': 310115, 'cityNum': 310000, 'provinceNum': 310000, 'dataLevel': 'A', 'prjFunctionNum': '999', 'prjPropertyNum': '001', 'prjApprovalLevelNum': '004', 'prjTypeNum': '99', 'buildCorpCode': '83448653-7', 'buildCorpName': '中国石油化工股份有限公司上海高桥分公司', 'prjApprovalNum': '石化股份计【2007】406号', 'prjName': '120万吨/年催化汽油吸附脱硫装置', 'prjNum': '3101150805049901', 'cREATEDATE': '2008-05-04', 'allArea': 4458.6, 'allInvest': 23148.0, 'provincePrjNum': '0801PD0016'}}, {'prodetail': {'countyNum': 330101, 'cityNum': 330100, 'provinceNum': 330000, 'dataLevel': 'D', 'prjTypeNum': '01', 'buildCorpName': '玫琳凯（中国）化妆品有限公司', 'prjName': '扩建生产厂房工程项目桩基', 'prjNum': '3301011311280104', 'cREATEDATE': '2013-11-28', 'provincePrjNum': '3301251311280101'}}, {'prodetail': {'countyNum': 420114, 'cityNum': 420100, 'provinceNum': 420000, 'dataLevel': 'C', 'prjApprovalLevelNum': '004', 'prjTypeNum': '01', 'buildCorpCode': '30374454-1', 'buildCorpName': '中法武汉生态示范城投资开发有限公司', 'prjApprovalNum': '蔡发改社会【2017】40号', 'prjName': '中法武汉生态示范城文化活动和培训中心', 'prjNum': '4201141706150102', 'cREATEDATE': '2017-06-15', 'allArea': 0.0, 'allInvest': 7476.73, 'provincePrjNum': '4201141706150118'}}, {'prodetail': {'countyNum': 210212, 'cityNum': 210200, 'provinceNum': 210000, 'dataLevel': 'D', 'prjFunctionNum': '099', 'prjPropertyNum': '099', 'prjTypeNum': '01', 'buildCorpName': '中石化催化剂大连有限公司', 'prjApprovalNum': '旅发改【2013】88号', 'prjName': '催化剂大连基地（一期）建设', 'prjNum': '2102121409180102', 'cREATEDATE': '2014-09-18', 'allArea': 82754.0, 'allInvest': 66629.26, 'provincePrjNum': '21021220140918880'}}, {'prodetail': {'countyNum': 440313, 'cityNum': 440300, 'provinceNum': 440000, 'dataLevel': 'D', 'prjFunctionNum': '300', 'prjPropertyNum': '001', 'prjApprovalLevelNum': '003', 'prjTypeNum': '01', 'prjSize': '前海深港青年梦工场二期项目位于前海合作区11单元08街坊，东临梦工场一期，西临梦海大道，北临前湾一路，南临地铁九号线梦海站C出口及城市支路。总用地面积9688.41平方米，其中建设用地9377.15平方米，景观用地311.26平方米，拟建总建筑面积约19900㎡，主要功能为办公及配套。项目暂定总投资2.3亿元，其中建安工程费1.84亿元，资金来源为财政性资金', 'buildCorpCode': '587917503', 'buildCorpName': '深圳市前海开发投资控股有限公司', 'prjApprovalNum': '深前海会纪〔2018〕84号', 'prjName': '前海深港青年梦工场二期(暂定名)', 'prjNum': '4403131907030031', 'cREATEDATE': '2018-09-27', 'allArea': 0.0, 'allInvest': 23000.0, 'provincePrjNum': '4403131808240101'}}, {'prodetail': {'dataSource': 4, 'isMajor': 0, 'countyNum': 440305, 'cityNum': 440300, 'provinceNum': 440000, 'invPropertyNum': '200', 'dataLevel': 'B', 'prjFunctionNum': '100', 'prjPropertyNum': '001', 'prjApprovalLevelNum': '003', 'prjTypeNum': '01', 'prjSize': '项目总投资18510万元', 'buildCorpCode': '34277604-4', 'buildCorpName': '深圳市海鹏锦投资发展有限公司', 'prjApprovalDepart': '深圳市发展和改革委员会', 'prjApprovalNum': '深南山发改核准(2017)0002号', 'address': '深圳市南山区招商街道赤湾园区', 'prjName': '赤湾13-02地块项目', 'prjNum': '4403052004300177', 'prjCode': '440305-2018-48-01-a00031', 'cREATEDATE': '2018-03-12', 'prjApprovalDate': '2018-03-12', 'allInvest': 18510.0, 'nationalPercentTage': 0.0, 'provincePrjNum': '4403051803120103'}}, {'prodetail': {'dataSource': 4, 'isMajor': 0, 'countyNum': 441351, 'cityNum': 441300, 'provinceNum': 440000, 'invPropertyNum': '103', 'dataLevel': 'C', 'prjFunctionNum': '700', 'prjPropertyNum': '001', 'prjApprovalLevelNum': '004', 'prjTypeNum': '01', 'prjSize': '4271.6㎡', 'buildCorpCode': 'MA556RMB-B', 'buildCorpName': '恒力石化（惠州）有限公司', 'prjApprovalDepart': '大亚湾工贸局', 'prjApprovalNum': '2020-441303-26-03-092406', 'address': '大亚湾石化区J1地块', 'prjName': '恒力石化(惠州)有限公司年产250万吨PTA-2项目(PTA-2空压机厂房1、PTA-2空压机厂房2)', 'prjNum': '4413512109270001', 'prjCode': '2020-441303-26-03-092406', 'cREATEDATE': '2021-09-26', 'endDate': '2021-12-10', 'beginDate': '2021-04-01', 'prjApprovalDate': '2020-10-19', 'allArea': 331750.0, 'allInvest': 410000.0, 'nationalPercentTage': 0.0, 'provincePrjNum': '4413512109260101'}}, {'prodetail': {'countyNum': 310100, 'cityNum': 310000, 'provinceNum': 310000, 'dataLevel': 'A', 'prjFunctionNum': '999', 'prjPropertyNum': '001', 'prjApprovalLevelNum': '002', 'prjTypeNum': '99', 'prjSize': '7.5万吨/年三元乙丙橡胶主体工程及相关配套设施', 'buildCorpCode': '59642350-5', 'buildCorpName': '上海中石化三井弹性体有限公司', 'prjApprovalNum': '沪化管[2012]35号', 'prjName': '中石化三井化学7.5万吨/年三元乙丙橡胶合资项目', 'prjNum': '3101001208299901', 'cREATEDATE': '2012-08-29', 'allArea': 69553.0, 'allInvest': 191080.0, 'provincePrjNum': '12HGKQ0028'}}, {'prodetail': {'dataSource': 2, 'isMajor': 0, 'countyNum': 120226, 'cityNum': 120000, 'provinceNum': 120000, 'invPropertyNum': '103', 'dataLevel': 'D', 'prjFunctionNum': '700', 'prjPropertyNum': '099', 'prjTypeNum': '01', 'prjSize': '92061平方米', 'fundSource': '企业自筹:22000万元，银行贷款:37733万元', 'buildCorpCode': '9112011835156027X5', 'buildCorpName': '天津港北建通成国际物流有限公司', 'prjApprovalDepart': '天津东疆保税港区管理委员会', 'prjApprovalNum': '津东保自贸审【2019】11号', 'address': '东疆港保税区西藏路和澳洲北路交口东南侧', 'prjName': '天津港北建通成国际物流有限公司京津物流园仓储物流项目', 'prjNum': '1202262006010001', 'cREATEDATE': '2020-05-03', 'endDate': '2021-12-01', 'beginDate': '2020-05-01', 'prjApprovalDate': '2019-09-25', 'allInvest': 59733.0, 'provincePrjNum': '1200001909200010'}}, {'prodetail': {'countyNum': 121134, 'cityNum': -1, 'provinceNum': 120000, 'dataLevel': 'D', 'prjFunctionNum': '099', 'prjPropertyNum': '001', 'prjApprovalLevelNum': '004', 'prjTypeNum': '02', 'prjSize': '48442.80平方米', 'buildCorpCode': '35156027X', 'buildCorpName': '天津港北建通成国际物流有限公司', 'prjApprovalNum': '津东保自贸审[2017]10号、津东保自贸审[2017]31号', 'prjName': '京津物流园项目一期', 'prjNum': '1211341801090204', 'cREATEDATE': '2018-01-09', 'beginDate': '2018-08-01', 'allArea': 48442.8, 'allInvest': 40974.63, 'provincePrjNum': '1213404120180001'}}, {'prodetail': {'countyNum': 420118, 'cityNum': 420100, 'provinceNum': 420000, 'dataLevel': 'C', 'prjApprovalLevelNum': '004', 'prjTypeNum': '01', 'buildCorpCode': '32217897-9', 'buildCorpName': '东风佛吉亚汽车内饰有限公司', 'prjApprovalNum': '2015010037250211', 'prjName': '东风佛吉亚汽车内饰项目', 'prjNum': '4201181506260101', 'cREATEDATE': '2015-06-26', 'allArea': 0.0, 'allInvest': 46860.0, 'provincePrjNum': '4201181506260108'}}, {'prodetail': {'dataSource': 1, 'isMajor': 0, 'countyNum': 650522, 'cityNum': 650500, 'provinceNum': 650000, 'invPropertyNum': '103', 'dataLevel': 'C', 'prjFunctionNum': '700', 'prjPropertyNum': '001', 'prjTypeNum': '01', 'buildPlanNum': '65222320190039', 'buildCorpCode': 'MA77QQHC-5', 'buildCorpName': '新疆宣东能源有限公司', 'prjApprovalDepart': '伊吾县发改委', 'prjApprovalNum': '伊发改产业备【2018】21号', 'address': '淖毛湖工业园区', 'prjName': '新疆宣东能源有限公司35万吨/年轻质煤焦油精深加工项目（一期）', 'prjNum': '6505222101190001', 'cREATEDATE': '2020-09-15', 'endDate': '2020-10-31', 'beginDate': '2020-05-03', 'prjApprovalDate': '2020-05-03', 'allLength': 0.0, 'allArea': 50383.08, 'allInvest': 12500.0, 'locationY': 43.710536, 'locationX': 95.045585, 'provincePrjNum': '650522202009150101'}}, {'prodetail': {'dataSource': 4, 'isMajor': 0, 'countyNum': 220214, 'cityNum': 220200, 'provinceNum': 220000, 'invPropertyNum': '103', 'dataLevel': 'D', 'prjFunctionNum': '011', 'prjPropertyNum': '001', 'prjTypeNum': '02', 'prjSize': '管道长度：453米', 'buildCorpCode': '91220203MA84M5930T', 'buildCorpName': '吉林万邦达环保技术有限公司', 'prjApprovalDepart': '吉林市龙潭区发展和改革局', 'address': '龙潭区汉江路、洛水街', 'prjName': '吉林化工园区绿色循环经济资源综合利用项目', 'prjNum': '2202142205250001', 'prjCode': '2106-220203-04-01-950623', 'cREATEDATE': '2022-05-15', 'prjApprovalDate': '2021-06-08', 'allArea': 20281.2, 'allInvest': 51300.0, 'provincePrjNum': '2202142205240201'}}, {'prodetail': {'countyNum': 110113, 'cityNum': 110000, 'provinceNum': 110000, 'dataLevel': 'D', 'prjTypeNum': '02', 'prjSize': '34350', 'projectPlanNum': '2006规建市政字0154，0155，0196号', 'buildCorpCode': '-', 'buildCorpName': '中国石油化工股份有限公司北京石油分公司', 'prjName': '环北京成品油管道工程及燕山—首都机场航煤输送管道工程、林河桥—机场6号门段', 'prjNum': '1101131907310879', 'cREATEDATE': '2006-06-16', 'endDate': '2006-09-18', 'beginDate': '2006-06-18', 'allArea': 34350.0, 'allInvest': 1610.0, 'provincePrjNum': '[2006]施市政字1100号'}}, {'prodetail': {'countyNum': 150625, 'cityNum': 150600, 'provinceNum': 150000, 'dataLevel': 'D', 'prjFunctionNum': '700', 'prjPropertyNum': '001', 'prjApprovalLevelNum': '002', 'prjTypeNum': '01', 'prjSize': '7635.19平方米', 'buildCorpCode': '69592228-9', 'buildCorpName': '内蒙古伊泰化工有限责任公司', 'prjApprovalNum': '内发改产业字[2012]2431号', 'prjName': '内蒙古伊泰化工有限责任公司120万吨/年精细化学品项目建筑、安装工程', 'prjNum': '1506251712270102', 'cREATEDATE': '2017-12-27', 'allArea': 7635.19, 'allInvest': 13955.61, 'provincePrjNum': 'B15062517122701004'}}, {'prodetail': {'countyNum': 310115, 'cityNum': 310000, 'provinceNum': 310000, 'dataLevel': 'A', 'prjFunctionNum': '999', 'prjPropertyNum': '002', 'prjApprovalLevelNum': '002', 'prjTypeNum': '99', 'buildCorpCode': '71093941-8', 'buildCorpName': '欧莱雅（中国）有限公司', 'prjApprovalNum': '沪金管项核[2012]27号', 'prjName': '欧莱雅（中国）研发和创新中心扩建项目', 'prjNum': '3101151206209901', 'cREATEDATE': '2012-06-20', 'allArea': 8587.0, 'allInvest': 9800.0, 'provincePrjNum': '12JQPD0023'}}, {'prodetail': {'countyNum': 310114, 'cityNum': 310000, 'provinceNum': 310000, 'dataLevel': 'A', 'prjFunctionNum': '009', 'prjPropertyNum': '003', 'prjApprovalLevelNum': '004', 'prjTypeNum': '01', 'prjSize': '根据工艺流程需要的钢结构连廊，其中地上面积623平方米，地下面积0平方米。', 'buildCorpCode': '58060033-5', 'buildCorpName': '阿里巴巴（上海）物联网技术有限公司', 'prjApprovalNum': '31011458060033520171D3101001', 'prjName': '中国智能骨干网上海嘉定项目钢结构连廊改造工程', 'prjNum': '3101141705090101', 'cREATEDATE': '2017-05-09', 'allArea': 623.0, 'allInvest': 8000.0, 'provincePrjNum': '1702JD0103'}}, {'prodetail': {'countyNum': 520119, 'cityNum': 520110, 'provinceNum': 520000, 'dataLevel': 'D', 'prjFunctionNum': '700', 'prjPropertyNum': '001', 'prjApprovalLevelNum': '003', 'prjTypeNum': '01', 'prjSize': '149499.91', 'buildCorpCode': '91520191MA6ECHY17H', 'buildCorpName': '贵阳双龙宝湾华业国际物流有限公司', 'prjApprovalNum': '2017-520116-59-03-411429', 'prjName': '宝湾华业贵阳智慧物流园项目', 'prjNum': '5201191812250001', 'cREATEDATE': '2018-12-24', 'endDate': '1900-01-01', 'beginDate': '1900-01-01', 'allArea': 80338.8, 'allInvest': 9000.0, 'provincePrjNum': '5201191812240117'}}, {'prodetail': {'dataSource': 2, 'isMajor': 0, 'countyNum': 120116, 'cityNum': 120000, 'provinceNum': 120000, 'invPropertyNum': '103', 'dataLevel': 'D', 'prjFunctionNum': '100', 'prjPropertyNum': '001', 'prjTypeNum': '01', 'prjSize': '40731.07平方米', 'fundSource': '企业自筹:22000万元', 'buildCorpCode': '91120116592938202F', 'buildCorpName': '天津中渔置业有限公司', 'prjApprovalDepart': '中心天津生态城行政审批局', 'prjApprovalNum': '津生固投发【2019】106号', 'address': '天津市生态城海容路95号', 'prjName': '天津中渔农产品冷链综合项目', 'prjNum': '1201162012310002', 'cREATEDATE': '2020-12-31', 'endDate': '2022-12-31', 'beginDate': '2021-01-04', 'prjApprovalDate': '2019-12-30', 'allInvest': 22000.0, 'provincePrjNum': '1200002012280016'}}, {'prodetail': {'countyNum': 420711, 'cityNum': 420700, 'provinceNum': 420000, 'dataLevel': 'C', 'prjFunctionNum': '700', 'prjApprovalLevelNum': '004', 'prjTypeNum': '01', 'prjSize': '建设规模：项目占地200亩，建成后实现每年货物吞吐量100万吨。建设内容：整体规划建设六栋高标准高架库及其配套设施，总面积76553.2平方米。', 'buildCorpCode': '914207003524157', 'buildCorpName': '武汉宝湾物流鄂州有限公司', 'prjApprovalNum': '2017-420796-59-03-105468', 'prjName': '鄂州葛店宝湾物流中心项目', 'prjNum': '4207111709050101', 'cREATEDATE': '2017-09-05', 'allArea': 76553.2, 'allInvest': 22500.0, 'provincePrjNum': '4207111806270106'}}, {'prodetail': {'countyNum': 310115, 'cityNum': 310000, 'provinceNum': 310000, 'dataLevel': 'A', 'prjFunctionNum': '999', 'prjPropertyNum': '006', 'prjApprovalLevelNum': '001', 'prjTypeNum': '99', 'buildCorpName': '中国石化上海高桥石油化工公司', 'prjApprovalNum': '石化股份计(2005)219号', 'prjName': '上海高桥分公司加工进口油适应性改造工程', 'prjNum': '3101150507289901', 'cREATEDATE': '2005-07-28', 'allArea': 0.0, 'allInvest': 110476.0, 'provincePrjNum': '0501PD0047'}}], 'badcredit': [], 'goodcredit': [], 'black': [], 'punishlist': [], 'chage': {}}"

        ]
    for line in datas:
        data = eval(line.lstrip().strip().replace('\n', ''))
        print(type(data),data)
        run(data,fil)





    # data_list = [
    #     {
    #         'base': {
    #             'legalMan': '田雪微',
    #             'corpName': '中铭亚舟（北京）建设工程有限公司',
    #             'corpCode': '91110115MABQF7E27E',
    #             'id': '002210222024414765',
    #             'address': '北京市大兴区海鑫路8号院4号楼2层(集群注册)',
    #             'regionFullname': '北京市',
    #             'qyRegType': '有限责任公司（自然人投资或控股）'
    #         },
    #         'messagecount': {
    #             'certCount': 3,
    #             'regPersonCount': 0,
    #             'projectCount': 0
    #         },
    #         'cert': [
    #             {
    #                 'certType': '建筑业企业资质',
    #                 'certName': '建筑装修装饰工程专业承包二级',
    #                 'organDate': '2022-10-21',
    #                 'endDate': '2027-10-20',
    #                 'organName': '北京市住房和城乡建设委员会',
    #                 'certId': 'D311791980',
    #                 'corpName': '中铭亚舟（北京）建设工程有限公司',
    #                 'corpCode': '91110115MABQF7E27E'
    #             },
    #             {
    #                 'certType': '建筑业企业资质',
    #                 'certName': '防水防腐保温工程专业承包二级',
    #                 'organDate': '2022-10-21',
    #                 'endDate': '2027-10-20',
    #                 'organName': '北京市住房和城乡建设委员会',
    #                 'certId': 'D311791980',
    #                 'corpName': '中铭亚舟（北京）建设工程有限公司',
    #                 'corpCode': '91110115MABQF7E27E'
    #             },
    #             {
    #                 'certType': '建筑业企业资质',
    #                 'certName': '特种工程(结构补强)专业承包不分等级',
    #                 'organDate': '2022-10-21',
    #                 'endDate': '2027-10-20',
    #                 'organName': '北京市住房和城乡建设委员会',
    #                 'certId': 'D311791980',
    #                 'corpName': '中铭亚舟（北京）建设工程有限公司',
    #                 'corpCode': '91110115MABQF7E27E'
    #             }
    #         ],
    #         'regporson': [],
    #         'project': [],
    #         'badcredit': [],
    #         'goodcredit': [],
    #         'black': [],
    #         'punishlist': [],
    #         'chage': {}
    #     }
    # ]
    # run(data_list)

    # list1={'asc': True, 'current': 1, 'limit': 15, 'offset': 0, 'offsetCurrent': 0, 'openSort': True, 'optimizeCount': False, 'pages': 14, 'records': [{'prjnum': '1101161907310119', 'corprolenum': 2, 'corpname': '北京中奥建工程设计有限公司', 'corpcode': '662164397', 'corpid': '002105291241617653'}, {'prjnum': '1101161907310119', 'corprolenum': 3, 'corpname': '北京双盈达建设有限公司', 'corpcode': '802888398', 'personname': '李雪玲', 'idcardtypenum': '1', 'corpid': '002105291240541899', 'idcard': '130102**********2X'}, {'prjnum': '1101161907310119', 'corprolenum': 4, 'corpname': '北京中外建工程管理有限公司', 'corpcode': '101144177', 'personname': '张青松', 'idcardtypenum': '1', 'corpid': '002105291313940891'}], 'searchCount': True, 'size': 15, 'total': 200}
    # list2={
    #     "asc": True,
    #     "current": 1,
    #     "limit": 15,
    #     "offset": 0,
    #     "offsetCurrent": 0,
    #     "openSort": True,
    #     "optimizeCount": False,
    #     "pages": 14,
    #     "records": [{
    #         "prjnum": "1301082203180001",
    #         "unitcode": "1301082203180001-001",
    #         "subprjname": "1#商务办公楼",
    #         "invest": 9010.00,
    #         "buildheight": 71.70,
    #         "buildarea": 20155.69
    #     }, {
    #         "prjnum": "1301082203180001",
    #         "unitcode": "1301082203180001-002",
    #         "subprjname": "2#商务办公楼",
    #         "prjlevelnum": "312",
    #         "invest": 9010.00,
    #         "buildheight": 90.00,
    #         "buildarea": 23448.04
    #     }],
    #     "searchCount": True,
    #     "size": 15,
    #     "total": 200
    # }
    #
    #
    #

    # for data in data_list:
    #     print(data)
    #     for ss in data['regporson']:
    #         print(type(ss), ss)


    # print(searchzzlb('防水防腐保温工程专业承包二级'))
                #检查数据哪里变化，就该哪
        # searchdb(tyshxydm)


# typeid=re.findall(r'([\S]+)资质','建筑业企业资质')
# print(typeid)
