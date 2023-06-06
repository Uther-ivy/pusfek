import json
import logging
import math
import random
import threading
import time
import traceback

from urllib.parse import quote

import execjs
import requests

import ip_proxys
from 四库一平台.test_siku.sql import searchdb


def read_file(file):
    with open(file=file, mode="r", encoding="utf-8") as r:
        datas = r.readlines()
    r.close()
    return datas


def wirte_file(file,name,cid):
    with open(file=file, mode="a", encoding="utf-8") as w:
        w.write(str({'cname':name,'cid':cid})+'\n')
    w.close()

class MinSpider(object):
    def __init__(self,ip_num):

        self._session = requests.Session()
        self.headers = {
            'Host': 'sky.mohurd.gov.cn',
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0.1; Redmi 4 Build/MMB29M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/78.0.3904.62 XWEB/2577 MMWEBSDK/200701 Mobile Safari/537.36 MMWEBID/8001 MicroMessenger/7.0.17.1720(0x2700113F) Process/appbrand0 WeChat/arm64 NetType/WIFI Language/zh_CN ABI/arm64',
            'Referer': 'https://servicewechat.com/wx8f070e7958a940d1/48/page-frame.html',
            'citycode': '',
            'token': 't_58dc8b534b9140aab20aebe097184feb',
            'Accept-Encoding': 'gzip, deflate, br',
            'content-type': 'application/json'
        }
        self.ip_num=ip_num
        # self.cid_list=[]
        self.proxys = {}
        self.psproxys = {}
        self.pjproxys = {}


    def replace_ip(self,types=None):
        proxy = ip_proxys.replace_ip()
        if types=='person':
            self.psproxys={
            'http': proxy,
            'https': proxy
        }
        elif types =='project':
            self.pjproxys = {
                'http': proxy,
                'https': proxy
                }
        else:
            self.proxys = {
            'http': proxy,
            'https': proxy
            }
    def company_dict(self):
        company_dict = {
            'base': [],
            'messagecount': [],
            'cert': [],
            'regporson': [],
            'project': [],
            'badcredit': [],
            'goodcredit': [],
            'black': [],
            'punishlist': [],
            'chage': []
        }

        return company_dict

    def jiemi_(self, data):
        js_infos = '''function deCrypt(t) {
            Object.defineProperty(exports, "__esModule", {
            value: !0
        }), exports.deCrypt = exports.enCrypt = void 0;
            var e = require("./js/38B128C16AECE6CF5ED740C61D4FAC62.js"), r = e.enc.Hex.parse("cd3b2e6d63473cadda38a9106b6b4e07");
            console.log(r)
            var p = e.AES.decrypt(t, r, {
                mode: e.mode.ECB,
                padding: e.pad.Pkcs7,
            });
            utf8String = e.enc.Utf8.stringify(p);
            return utf8String;
        }

        module.exports.init = function (arg1) {
            //调用函数，并返回
            console.log(deCrypt(arg1));
        };'''

        dedata = execjs.compile(js_infos).call('deCrypt', data)
        # 读取结果
        print('解密完成')
        return dedata

    def req_(self, url,types):
        if types=='person':
            proxy = self.psproxys
        elif types == 'project':
            proxy = self.pjproxys
        else:
            proxy = self.proxys
        print('request:',types)
        res = self._session.get(url=url, headers=self.headers, proxies=proxy, verify=False, timeout=60)
        if res.status_code == requests.codes.ok:
            res_data = json.loads(res.content)
            return res_data

    def request_(self, url,types="default"):
        try:
            print('首次连接')
            res = self.req_(url,types)
            if res.get('status') == 4001:  # {'message': '服务器忙。。。。 请稍后重试！', 'status': 4001}
                logging.info('the server is busying。。。。')
                time.sleep(20+random.random() * 10)
                self.replace_ip(types)
                res = self.req_(url, types)

        except ConnectionResetError as cre:
            logging.info(f"{cre}\n{traceback.format_exc()}")
            time.sleep(40 + random.random() * 10)
            self.replace_ip(types)
            res = self.req_(url, types)
        except Exception as e:

            logging.info(f"proxy disabled！！！ change proxy\n{e}\n{traceback.format_exc()}")
            time.sleep(20 + random.random() * 10)
            self.replace_ip(types)
            res = self.req_(url, types)
            # print(res)
        return res
    # 建设工程企业list
    def channel_info(self):
        companylist = []
        try:
            for page in range(20):
                channel_url = f"https://sky.mohurd.gov.cn/skyapi/api/statis/getResult?_t=0.6526977008668777&pageNumber={page}&pageSize=10&keys=corp%2Fdata_search%2Fpage"
                resdata = json.loads(self.jiemi_(self.request_(channel_url)['data']))[0]['data']
                # print(resdata)
                if resdata.get('records'):
                    for res in resdata['records']:
                        if res['id'] not in companylist:
                            # print(type(res), res)
                            companylist.append(res['id'])
            # print(len(companylist))
            return companylist

        except Exception as e:
            logging.error(f"获取失败{e}\n{traceback.format_exc()}")

    # 首页公司信息
    def get_company_info(self, cid):
        detail_url = f"https://sky.mohurd.gov.cn/skyapi/api/statis/getExtResult?_t=0.9219150372692497&keys=corp%2Fcorp_detail%2Fdetail&corpId={cid}"
        resdata = json.loads(self.jiemi_(self.request_(detail_url)['data']))[0]['data'][0]
        # print(type(resdata), resdata)
        print(resdata)
        return resdata

    # 名下人员，资质，项目数量
    def get_detail_info(self, cid):
        url = f"https://sky.mohurd.gov.cn/skyapi/api/statis/getResult?_t=0.771112245605825&keys=corp%2Fcorp_detail_count%2Fcount&corpId={cid}"
        resdata = json.loads(self.jiemi_(self.request_(url)['data']))[0]['data'][0]
        # print(type(resdata), resdata)
        return resdata

    # 资质数
    def get_cert_info(self, cid, cert):
        certlist = []


        for page in range(math.ceil(cert / 15)):
            cert_url = f'https://sky.mohurd.gov.cn/skyapi/api/statis/getResult?_t=0.5691723407797857&keys=corp%2Fcorp_detail_cert%2Fpage&pageNumber={page + 1}&pageSize=15&corpId={cid}'
            cert_data = json.loads(self.jiemi_(self.request_(cert_url)['data']))[0]['data']['records']
            for cert in cert_data:
                certlist.append(cert)
        # print(certlist)
        return certlist  # print(type(cert_data), cert_data)


    # 注册人员数
    def get_person_info(self,kid, cid):
        perlist = []

        person_url = f'https://sky.mohurd.gov.cn/skyapi/api/statis/getResult?_t=0.919334082096418&keys=corp%2Fcorp_detail_regperson%2Fcount&corpId={cid}'
        person_data = json.loads(self.jiemi_(self.request_(person_url)['data']))[0]['data']
        # print(type(person_data), person_data)
        for data in person_data:
            code = data['regTypeCode']
            count = data['count']
            for page in range(math.ceil(count / 15)):

                self.replace_ip('person')
                ps_thread=threading.Thread(target=self.get_certificate,args=(kid,cid,code,page,perlist))
                print('project:',ps_thread.name)
                ps_thread.start()
                ps_thread.join()
            # perlist.append(thread)
            # self.get_certificate(cid, code,count, perlist)
        return perlist

    # 公司历史业绩
    def get_project_info(self,kid,certs, project,cid):
        projectlist = []
        try:
            for page in range(math.ceil(project / 15)):
                ptype='project'
                project_url = f'https://sky.mohurd.gov.cn/skyapi/api/statis/getResult?_t=0.3891597792453172&keys=corp%2Fcorp_detail_project%2Fpage&provinceNum=&cityNum=&countyNum=&projectType=&pageNumber={page + 1}&pageSize=15&corpId={cid}'
                resdata = json.loads(self.jiemi_(self.request_(project_url)['data']))[0]['data']['records']
                for prodict in resdata:
                    pid = prodict['prjNum']
                    pj_thread = threading.Thread(target=self.get_project_data, args=(kid,certs,pid,projectlist,ptype))
                    pj_thread.start()
                    pj_thread.join()
        except Exception as e:
            logging.error(f"历史业绩获取失败{e}\n{traceback.format_exc()}")
        return projectlist

    def get_project_data(self,kid,certs,pid,projectlist,ptype):
        self.replace_ip(ptype)
        detail_dict = {}
        try:
            prodetail = self.get_project_detail(kid, certs)  # 项目详情
            jointhing = self.get_jointhing(pid,ptype)
            unit = self.get_unit(pid,ptype)
            tender = self.get_tender(pid,ptype)
            contract = self.get_contract(pid,ptype)
            censor = self.get_censor(pid,ptype)
            # censor_user = self.get_censor_user(pid,ptype)app错误
            censor_err = self.get_censor_err(pid,ptype)
            licence = self.get_licence(pid,ptype)
            # qualitycheck = self.get_qualitycheck(pid,ptype)
            # safecheck = self.get_safecheck(pid,ptype)
            # safeuser = self.get_safeuser(pid,ptype)
            # manageuser = self.get_manageuser(pid,ptype)
            # operation = self.get_operation(pid,ptype)
            # mechanics = self.get_mechanics(pid,ptype)
            # spotcheck = self.get_spotcheck(pid,ptype)
            # superviser = self.get_superviser(pid,ptype)
            finish = self.get_finish(pid,ptype)
            # check = self.get_check(pid,ptype)
            detail_dict['prodetail'] = prodetail
            detail_dict['jointhing'] = jointhing
            detail_dict['unit'] = unit
            detail_dict['tender'] = tender
            detail_dict['contract'] = contract
            detail_dict['censor'] = censor
            # detail_dict['censor_user'] = censor_user
            detail_dict['censor_err'] = censor_err
            detail_dict['licence'] = licence
            # detail_dict['qualitycheck'] = qualitycheck
            # detail_dict['safecheck'] = safecheck
            # detail_dict['safeuser'] = safeuser
            # detail_dict['manageuser'] = manageuser
            # detail_dict['operation'] = operation
            # detail_dict['mechanics'] = mechanics
            # detail_dict['spotcheck'] = spotcheck
            # detail_dict['superviser'] = superviser
            detail_dict['finish'] = finish

            # detail_dict['check'] = check
                # print(f'project——{}:',detail_dict)
            projectlist.append(detail_dict)
            # return projectlist
        except Exception as e:
            logging.error(f"历史业绩获取失败{e}\n{traceback.format_exc()}")

    # 建造师等级及人员
    def get_certificate(self, kid,cid, code,page, perlist):

        url = f"https://sky.mohurd.gov.cn/skyapi/api/statis/getResult?_t=0.287965522231608&keys=corp%2Fcorp_detail_regperson_type%2Fpage&pageNumber={page + 1}&pageSize=15&corpId={cid}&regTypeCode={code}"
        rdata = json.loads(self.jiemi_(self.request_(url,types='person')['data']))[0]['data']['records']
        # print(rdata)
        # self.search_person()
        for plist in rdata:
            name = plist['personName']
            id = plist['id']
            zhtype = plist['regZyName']
            sfz = plist['idCard']
            url = f'https://sky.mohurd.gov.cn/skyapi/api/statis/getExtResult?_t=0.05171223342463582&keys=person%2Fdetail%2Fdetail&id={id}'
            p_info = json.loads(self.jiemi_(self.request_(url,types='person')['data']))[0]['data']
            # print(p_info)
            gsname = p_info[0]['corpName']
            sex = 0
            if p_info[0]['ry_sex'] == 'RY_XB_002':
                sex = 1

            url = f'https://sky.mohurd.gov.cn/skyapi/api/data/getPersonRegZyInfo/{id}?_t=0.8553082962527838'
            data_info = json.loads(self.jiemi_(self.request_(url,types='person')['data']))[0]
            # print(data_info)
            zsbh = data_info['regNo']
            zyyz = data_info['sealCode']
            zsdj = data_info['zclbName']
            # reg_start = int(time.mktime(time.strptime(data_info['zczyList'][0]['regSdate'], "%Y-%m-%d")))
            reg_end = int(time.mktime(time.strptime(data_info['zczyList'][0]['regEdate'], "%Y-%m-%d")))
            # print(time_info)
            pdict = {
                'name': name,
                'id': id,
                'zsbh': zsbh,
                'zhtype': zhtype,
                'sfz': sfz,
                'gsname': gsname,
                'sex': sex,
                'zyyz': zyyz,
                # 'reg_start': reg_start,
                'reg_end': reg_end,
                'zsdj': zsdj
            }

            print(pdict)
            # print(name,id,zsbh,zhtype,sfz,gsname,sex,zyyz, reg_start,reg_end)
            perlist.append(pdict)
        # return perlist

    # 项目详情
    def get_project_detail(self,cid,ptype):
        project_url = f'https://sky.mohurd.gov.cn/skyapi/api/statis/getExtResult?_t=0.49148925513478625&keys=prj%2Fdata_search%2Fdetail&prjNum={cid}'
        resdata = json.loads(self.jiemi_(self.request_(project_url,types=ptype)['data']))[0]['data'][0]
        return resdata

    # 参与单位及负责人
    def get_jointhing(self, cid,ptype):
        project_url = f'https://sky.mohurd.gov.cn/skyapi/api/statis/getResult?_t=0.16085749173162478&keys=prj%2Fmanager%2Fpage&pageNumber=1&pageSize=15&prjnum={cid}'
        resdata = json.loads(self.jiemi_(self.request_(project_url,types=ptype)['data']))[0]['data']['records']
        # print(resdata)
        return resdata

    # 单体信息
    def get_unit(self, cid,ptype):
        print(cid)
        project_url = f'https://sky.mohurd.gov.cn/skyapi/api/statis/getResult?_t=0.025606408014731352&keys=prj%2Funit%2Fpage&pageNumber=1&pageSize=15&prjNum={cid}'
        resdata = json.loads(self.jiemi_(self.request_(project_url,types=ptype)['data']))[0]['data']['records']
        print(resdata)
        reslist=[]
        if resdata:
           for unitid in resdata:
                print(unitid.get('unitcode'))
                undet=self.get_unit_details(unitid.get('unitcode'),ptype)
                print(type(undet),undet)
                reslist.append(undet)
        return  reslist




    def get_unit_details(self,unitid,ptype):
        project_url=f'https://sky.mohurd.gov.cn/skyapi/api/statis/getResult?_t=0.12660224780431828&keys=prj%2Funit%2Fdetail&unitcode={unitid}'
        resdata = json.loads(self.jiemi_(self.request_(project_url,types=ptype)['data']))[0]['data'][0]
        print(resdata)
        return resdata

    # 投标信息
    def get_tender(self, cid,ptype):
        project_url = f'https://sky.mohurd.gov.cn/skyapi/api/statis/getResult?_t=0.2749589031852593&keys=prj%2Ftender%2Fpage&pageNumber=1&pageSize=15&prjNum={cid}'
        resdata = json.loads(self.jiemi_(self.request_(project_url,types=ptype)['data']))[0]['data']['records']
        # print(resdata)
        return resdata

    # 合同登记信息
    def get_contract(self, cid,ptype):
        project_url = f'https://sky.mohurd.gov.cn/skyapi/api/statis/getResult?_t=0.08226842717177196&keys=prj%2Fcontract%2Fpage&pageNumber=1&pageSize=15&prjNum={cid}'
        resdata = json.loads(self.jiemi_(self.request_(project_url,types=ptype)['data']))[0]['data']['records']
        # print(resdata)
        return resdata

    # 施工图审查信息
    def get_censor(self, cid,ptype):
        project_url = f'https://sky.mohurd.gov.cn/skyapi/api/statis/getResult?_t=0.5077815811924857&keys=prj%2Fcensor%2Fpage&pageNumber=1&pageSize=15&prjNum={cid}'
        resdata = json.loads(self.jiemi_(self.request_(project_url,types=ptype)['data']))[0]['data']['records']
        # print(resdata)
        return resdata

    # 专业人员信息
    def get_censor_user(self, cid,ptype):
        project_url = f'https://sky.mohurd.gov.cn/skyapi/api/statis/getResult?_t=0.5096184092674556&keys=prj%2Fcensor_user%2Fpage&pageNumber=1&pageSize=15&prjNum={cid}'
        resdata=json.loads(self.jiemi_(self.request_(project_url, types=ptype)['data']))[0]['data']['records']
        return resdata

    # 违反强制性准则
    def get_censor_err(self, cid,ptype):
        project_url = f'https://sky.mohurd.gov.cn/skyapi/api/statis/getResult?_t=0.1940685153360886&keys=prj%2Fcensor_err%2Fpage&pageNumber=1&pageSize=15&prjNum={cid}'
        resdata = json.loads(self.jiemi_(self.request_(project_url,types=ptype)['data']))[0]['data']['records']
        # print(resdata)
        return resdata

    # 施工许可信息
    def get_licence(self, cid,ptype):
        project_url = f'https://sky.mohurd.gov.cn/skyapi/api/statis/getResult?_t=0.8678336277289931&keys=prj%2Flicence%2Fpage&pageNumber=1&pageSize=15&prjNum={cid}'
        resdata = json.loads(self.jiemi_(self.request_(project_url,types=ptype)['data']))[0]['data']['records']
        if resdata:
            return resdata

    # 质量监督信息
    def get_qualitycheck(self, cid,ptype):
        project_url = f'https://sky.mohurd.gov.cn/skyapi/api/statis/getResult?_t=0.8037222305375264&keys=prj%2Flicence_qualitycheck%2Fpage&pageNumber=1&pageSize=15&prjNum={cid}'
        res = json.loads(self.jiemi_(self.request_(project_url,types=ptype)['data']))
        # print("qualitycheck:",res)
        if res:
            resdata=res[0]['data']['records']
            return resdata

    # 安全监督信息
    def get_safecheck(self, cid,ptype):
        project_url = f'https://sky.mohurd.gov.cn/skyapi/api/statis/getResult?_t=0.4460070042614246&keys=prj%2Flicence_safecheck%2Fpage&pageNumber=1&pageSize=15&prjNum={cid}'
        resdata = json.loads(self.jiemi_(self.request_(project_url,types=ptype)['data']))[0]['data']['records']
        # print(resdata)
        return resdata

    # 安全员信息
    def get_safeuser(self, cid,ptype):
        project_url = f'https://sky.mohurd.gov.cn/skyapi/api/statis/getResult?_t=0.4208115153141241&keys=prj%2Flicence_safeuser%2Fpage&pageNumber=1&pageSize=15&prjNum={cid}'
        resdata = json.loads(self.jiemi_(self.request_(project_url,types=ptype)['data']))[0]['data']['records']
        # print(resdata)
        return resdata

    # 现场管理人员信息
    def get_manageuser(self, cid,ptype):
        project_url = f'https://sky.mohurd.gov.cn/skyapi/api/statis/getResult?_t=0.8043556217645476&keys=prj%2Flicence_manageuser%2Fpage&pageNumber=1&pageSize=15&prjNum={cid}'
        resdata = json.loads(self.jiemi_(self.request_(project_url,types=ptype)['data']))[0]['data']['records']
        # print(resdata)
        return resdata

    # 特种作业人员信息
    def get_operation(self, cid,ptype):
        project_url = f'https://sky.mohurd.gov.cn/skyapi/api/statis/getResult?_t=0.8950097299633917&keys=prj%2Flicence_operationworker%2Fpage&pageNumber=1&pageSize=15&prjNum={cid}'
        resdata = json.loads(self.jiemi_(self.request_(project_url,types=ptype)['data']))[0]['data']['records']
        # print(resdata)
        return resdata

    # 特种作业机器信息
    def get_mechanics(self, cid,ptype):
        project_url = f'https://sky.mohurd.gov.cn/skyapi/api/statis/getResult?_t=0.5076202964425607&keys=prj%2Flicence_mechanics%2Fpage&pageNumber=1&pageSize=15&prjNum={cid}'
        resdata = json.loads(self.jiemi_(self.request_(project_url,types=ptype)['data']))[0]['data']['records']
        # print(resdata)
        return resdata

    # 施工现场检查信息
    def get_spotcheck(self, cid,ptype):
        project_url = f'https://sky.mohurd.gov.cn/skyapi/api/statis/getResult?_t=0.9649136199195407&keys=prj%2Flicence_spotcheck%2Fpage&pageNumber=1&pageSize=15&prjNum={cid}'
        resdata = json.loads(self.jiemi_(self.request_(project_url,types=ptype)['data']))[0]['data']['records']
        # print(resdata)
        return resdata

    # 施工现场监理人员信息
    def get_superviser(self, cid,ptype):
        project_url = f'https://sky.mohurd.gov.cn/skyapi/api/statis/getResult?_t=0.7484262378289745&keys=prj%2Flicence_superviser%2Fpage&pageNumber=1&pageSize=15&prjNum={cid}'
        resdata = json.loads(self.jiemi_(self.request_(project_url,types=ptype)['data']))[0]['data']['records']
        # print(resdata)
        return resdata

    # 竣工验收备案信息
    def get_finish(self, cid,ptype):
        project_url = f'https://sky.mohurd.gov.cn/skyapi/api/statis/getResult?_t=0.6405781635025845&keys=prj%2Ffinish_manage%2Fpage&pageNumber=1&pageSize=15&prjNum={cid}'
        resdata = json.loads(self.jiemi_(self.request_(project_url,types=ptype)['data']))[0]['data']['records']
        # print(resdata)
        return resdata

    # 竣工验收信息
    def get_check(self, cid,ptype):
        project_url = f'https://sky.mohurd.gov.cn/skyapi/api/statis/getResult?_t=0.660163618023065&keys=prj%2Ffinish_check%2Fpage&pageNumber=1&pageSize=15&prjNum={cid}'
        resdata = json.loads(self.jiemi_(self.request_(project_url,types=ptype)['data']))[0]['data']['records']
        # print(resdata)
        return resdata

    # 不良行为
    def get_badcredit(self, cid):
        url = f"https://sky.mohurd.gov.cn/skyapi/api/statis/getResult?_t=0.3687942491768832&keys=corp%2Fbad_credit%2Fpage&pageNumber=1&pageSize=15&corpId={cid}"
        resdata = json.loads(self.jiemi_(self.request_(url)['data']))[0]['data']['records']
        # print(type(resdata), resdata)
        return resdata

    # 良好行为
    def get_goodcredit(self, cid):
        url = f"https://sky.mohurd.gov.cn/skyapi/api/statis/getResult?_t=0.3605943555443578&keys=corp%2Fgood_credit%2Fpage&pageNumber=1&pageSize=15&corpId={cid}"
        resdata = json.loads(self.jiemi_(self.request_(url)['data']))[0]['data']['records']
        # print(type(resdata), resdata)
        return resdata

    # 黑名单
    def get_black(self, cid):
        url = f"https://sky.mohurd.gov.cn/skyapi/api/statis/getResult?_t=0.9221325093407371&keys=corp%2Fblack%2Fpage&pageNumber=1&pageSize=15&corpId={cid}"
        resdata = json.loads(self.jiemi_(self.request_(url)['data']))[0]['data']['records']
        # print(type(resdata), resdata)
        return resdata

    # 失信联合惩戒记录
    def get_punishlist(self, cid):
        url = f"https://sky.mohurd.gov.cn/skyapi/api/statis/getResult?_t=0.27022203908076303&keys=corp%2Fpunishlist%2Fpage&pageNumber=1&pageSize=15&corpId={cid}"
        resdata = json.loads(self.jiemi_(self.request_(url)['data']))[0]['data']['records']
        # print(type(resdata), resdata)
        return resdata

    # 变更记录
    def get_change(self, cid):
        url = f"https://sky.mohurd.gov.cn/skyapi/api/data/getCorpChangeRecordInfo/{cid}?_t=0.2796823120326173&pageNumber=1&pageSize=15"
        resdata = self.jiemi_(self.request_(url)['data'])
        # print(type(eval(resdata)), resdata)
        return eval(resdata)

    def get_company_id(self,companyname,fil):
        #  namelist = ['江苏常腾建设工程有限公司']
        print(companyname)
        name=companyname.replace('\n','')
        url = f"https://sky.mohurd.gov.cn/skyapi/api/statis/getResult?_t=0.41493411788348533&keys=corp%2Fdata_search%2Fpage&qyTypeCode=&aptCode=&regionNum=&pageNumber=1&pageSize=15&keyWord={quote(name)}"
        resdata = json.loads(self.jiemi_(self.request_(url)['data']))[0]['data']['records']
        print(resdata)
        if len(resdata) > 0:
            for data in resdata:
                companydata = {}
                companydata['cname'] = data['corpName']
                companydata['corcode'] = data['corpCode']
                companydata['cid'] = data["id"]
                return companydata
        else:
            # with open(file=f"company_base/error{fil}.txt", mode="a", encoding="utf-8") as w:
            #     w.write(str(companyname))
                print(companyname, '没搜到')
            # w.close()


    def companysearch(self,cid,fil,name):
        try:
            company_data = self.company_dict()
            get_company_base = self.get_company_info(cid)  # 基础信息
            get_detail_info = self.get_detail_info(cid)  # 名下人员，资质，项目数量
            companyname=get_company_base.get('base').get('corpName')
            certnum = get_detail_info['certCount']
            personnum = get_detail_info['regPersonCount']
            projectnum = get_detail_info['projectCount']
            if certnum > 0:
                company_data['cert'] = self.get_cert_info(cid, certnum)
            kid = searchdb(companyname)[0]
            if personnum > 0:
                company_data['regporson'] = self.get_person_info(kid,cid)
            if projectnum > 0:
                company_data['project'] = self.get_project_info(kid,company_data['cert'], projectnum,cid)



            badcredit = self.get_badcredit(cid)  # 不良行为
            goodcredit = self.get_goodcredit(cid)  # 良好行为
            black = self.get_black(cid)  # 黑名单
            punishlist = self.get_punishlist(cid)  # 失信联合惩戒记录
            chage = self.get_change(cid)  # 变更记录

            company_data['base'] = get_company_base
            company_data['messagecount'] = get_detail_info
            company_data['badcredit'] = badcredit
            company_data['goodcredit'] = goodcredit
            company_data['black'] = black
            company_data['punishlist'] = punishlist
            company_data['chage'] = chage
            # wirte_file(wirtefile,company_data)
            print(company_data)
            # run(company_data,fil)
            # print(f'{name} has saved the companydb{ip_num}.json')
        except Exception as e:
            # logging.error(f"{name}获取失败{e}\n{traceback.format_exc()}")
            # file=f"./company_name/errorcompany{fil}.txt"
            # wirte_file(file,name,cid)
            print(name, '获取失败',e)




# def autorun():
#     all_data = []
#     company_id = ['002110271912206133', '002105291240526173']
#     for cid in company_id:  # spider.channel_info():
#         try:
#             all_data.append(companysearch(cid))
#             companysearch(cid)
#             print(all_data)
        # except Exception as e:
        #     logging.error(f"获取失败{e}\n{traceback.format_exc()}")
        #     continue
    # print(all_data)
    # return all_data

    # run(all_data)
    # return all_dat
    #
