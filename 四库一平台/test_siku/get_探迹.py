import json
import logging
import math
import random
import re
import time
import traceback
from binascii import a2b_hex

import requests
import xlwt
from Crypto.Cipher import AES

import ip_proxys
from spider.sql import insert_skid


class get_company(object):

    def __init__(self):
        self._session=requests.session()
        self.proxys = {
            'http': '',
            'https': ''
        }
        self.headers= {
'Accept':'*/*',
# 'Accept-Encoding':'gzip, deflate, br',
'Accept-Language':'zh-CN,zh;q=0.9',
'Cache-Control':'no-cache',
'Connection':'keep-alive',
# 'Content-Length':'430',
'Content-Type':'multipart/form-data; boundary=----WebKitFormBoundaryEGfqTUD58B4f5QzH',
'Cookie':'Hm_lvt_402a6e64fccc38b600a1b33b9d06c425=1689125282; DISTINCT_ID=5d4520d4-d5f6-41ba-aca0-e8154674e60d; tg_referrer_source=https%3A%2F%2Fuser.tungee.com%2F; SecurityCenterDuId=Ilg4NEFRNEpMekVkeVJGaGNGb2tRR0pVPSI.F4-rmA.owN0RqvOHafKUxkv7aqSbhFOf0w; _co_i=5fcdf3e3d450cc1407280a8b; tg_gather_browser=1; __last_enter_version=qcs; Hm_lpvt_402a6e64fccc38b600a1b33b9d06c425=1689142102; CGISessionId=eyJzaWQiOiJPR1kwWVRsaU0yUXRZVFkxT1MwME1tVmpMV0ZpTWprdFlqVXlNbVl4TXpGaVlXTmsiLCJjaGFubmVsIjoid2ViIiwiX2ZyZXNoIjpmYWxzZX0.ZK5DUg.zohKDp8SfDHd5MKRRbFq9c_jai8; accountCenterSessionId=.eJwlj81OwzAQhN_F5x7seLu2-wDlQqgQhcqnyPbuqknTICUpv-LdseAymjl80jffamKmbklv3K2vHWW1kzQuvFFdT2qnChAAWAcWsEBxJkCWlC1h1k3I5MUiat9wYdugSBHA5CzoioQaAUPDlaVtQCm49Vkq5wUSuFqSbkhr4YTFAbB1BN76IMlkNOR1URtVzmmaeKwy75zrXv7EDndRx-PYt83jGo_RHJ60bq8vw_1p37fDZY3D82d7jR_t176Pp4dLBTuZeTmr3Trf6r_bwvP_R4TEJhlPJQUw6LgKmKBJ_fwC6_pUsQ.F4_U0w.NOi6h7toqu4U8I76SY_FsaypiR8',
# 'Cookie':'Hm_lvt_402a6e64fccc38b600a1b33b9d06c425=1689125282; DISTINCT_ID=5d4520d4-d5f6-41ba-aca0-e8154674e60d; tg_referrer_source=https%3A%2F%2Fuser.tungee.com%2F; SecurityCenterDuId=Ilg4NEFRNEpMekVkeVJGaGNGb2tRR0pVPSI.F4-rmA.owN0RqvOHafKUxkv7aqSbhFOf0w; _co_i=5fcdf3e3d450cc1407280a8b; tg_gather_browser=1; __last_enter_version=qcs; Hm_lpvt_402a6e64fccc38b600a1b33b9d06c425=1689133846; CGISessionId=eyJzaWQiOiJPR1kwWVRsaU0yUXRZVFkxT1MwME1tVmpMV0ZpTWprdFlqVXlNbVl4TXpGaVlXTmsiLCJjaGFubmVsIjoid2ViIiwiX2ZyZXNoIjpmYWxzZX0.ZK4jKA.PK2W39j2oTEsnOqLEVI1oV0Fqms; accountCenterSessionId=.eJwlj8tOwzAQRf_F6y78mI7tfEDZNFSIQuVV5MeMmjQNUpLyFP-Ogc3o6krn6syXyOc4TTSKRrxREhvR9aXmDAUAjAUDmCFb5SFxTKZgktqn4tggSqcpk9HInBkwWgOyIr4ej15TZcvWI2fcusSVcwwRbA1R6iIlU8RsAcjYAs44z1ElVMXJ_CvCMy1n0azzjTZiIirdEl-pW1-6kkTDcVxqv_zpHu6CDMexb_XDGo5BHR6lbK_Pw_6069vhsobh6aO9hvf2c9eH0_2lzt8Wmv9_RYikonIlRw8KLVUR5WUR3z8B2FSx.F4-0qQ.HLJhOMOOh3OV_WHEcb8CCfzEsU8',
# 'Cookie':'Hm_lvt_402a6e64fccc38b600a1b33b9d06c425=1689125282; DISTINCT_ID=5d4520d4-d5f6-41ba-aca0-e8154674e60d; tg_referrer_source=https%3A%2F%2Fuser.tungee.com%2F; SecurityCenterDuId=Ilg4NEFRNEpMekVkeVJGaGNGb2tRR0pVPSI.F4-rmA.owN0RqvOHafKUxkv7aqSbhFOf0w; _co_i=5fcdf3e3d450cc1407280a8b; tg_gather_browser=1; __last_enter_version=qcs; Hm_lpvt_402a6e64fccc38b600a1b33b9d06c425=1689141815; CGISessionId=eyJzaWQiOiJPR1kwWVRsaU0yUXRZVFkxT1MwME1tVmpMV0ZpTWprdFlqVXlNbVl4TXpGaVlXTmsiLCJjaGFubmVsIjoid2ViIn0.ZK5CNA.r_6ri19DS9GYeSdwa5eoj4W4G2M; accountCenterSessionId=.eJwdjs1qwzAQhN9F5x4ka7OS8gDpJW4oTRt0MpJ2l9hxXLCd_tJ3r8hlmIH54PtVt4Xnrie1VQiJTTKeSgpg0LEPYoIm9aA6mXk5q-0637iu-70AAYB1YAELFGcCZEnZEmbdhExeLKL2DRe2DYoUAUzOgq5IqBEwNFxZ2gSUghufpXJeIIGrJemGtBZOWBwAW0fgbTVKJqMhr0vVmpipW9IHd-t7R1ltJY1LFSznNE08VslPzvW33IUPj1HH49i3zfMaj9EcXrRur2_D_rTr2-GyxuH1u73Gr_Zn18fT00X9_QPSTFSx.F4_TtA.scrPyIPM-voWNcN4AfLfeVUbqHM',
'Host':'qcs.tungee.com',
'Origin':'https://qcs.tungee.com',
'Pragma':'no-cache',
'Referer':'https://qcs.tungee.com/customer-group/qualification-new?mode=0&page=1&size=50',
'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        }

    def replace_ip(self):
        print("ip获取中")
        proxy = ip_proxys.replace_ip()
        self.proxys = {
            'http': proxy,
            'https': proxy
        }

    def req_(self, url, method, data=None, param=None):
        # time.sleep(5 + random.random() * 5)
        prox = self.proxys
        if method == 'get':
            res = self._session.get(url=url, headers=self.headers, data=data, params=param, proxies=prox, verify=False,
                                    timeout=60)
        else:
            res = self._session.post(url=url, headers=self.headers, data=data, params=param, proxies=prox, verify=False,
                                     timeout=60)
        if res.status_code == requests.codes.ok:
            res_data = res.content.decode()
            return res_data

    def request_(self, url, method, data=None, param=None):
        try:
            res = self.req_(url, method, data, param)
        except Exception as e:
            print(e)
            logging.info("proxy disabled！！！ change proxy")
            # time.sleep(random.random() * 10)
            self.replace_ip()
            res = self.req_(url, method, data, param)
        return res



    # 建设工程企业list
    def channel_info(self):
        try:
            begin=0
            end=200
            for page in range(math.ceil(10000/200)):
                print('*'*30,page,'*'*20)
                channel_url = f"https://qcs.tungee.com/cgi/qualification-agent-data/api/qualification-new/search"
                data={'mode': 0,'begin': begin,'end': end,'filter': '{"address":[["河北省"]]}','onlyArchEntNoArchQual': 0}
                print(data)
                data = self.request_(channel_url,method='post',param=data)
                begin += 200
                end += 200
                print(data)
                if data:
                    for res in json.loads(data).get('data').get('items'):
                        company_contact=[]
                        print(res)
                        _id=res.get('_id')
                        cpmpanyname=res.get('name')
                        legal = res.get['legalRepresentative']
                        company_contact.append(cpmpanyname)
                        company_contact.append(legal)
                        uplock=f'https://qcs.tungee.com/cgi/qualification-agent-common/api/lead/unlock?source=14&enterprise_id={_id}&entity_type=enterprise'
                        self._session.put(uplock)
                        phoneurl=f'https://qcs.tungee.com/cgi/qualification-agent-common/api/lead/contacts?enterprise_id={_id}&type=company&multi_version_type=qualification_agent'
                        detail = self.request_(phoneurl, method='get')
                        for contact in json.loads(detail).get('contacts'):
                            way=contact.get('contact_label')
                            company_contact.append(way)
                        print(company_contact)

                        yield company_contact
                    else:
                        print('没数据了')
                        break
                else:
                    print('没数据了')
                    break


        except Exception as e:
            logging.error(f"获取失败{e}\n{traceback.format_exc()}")


if __name__ == '__main__':
    spider = get_company()
    spider.replace_ip()
    row=0
    book = xlwt.Workbook(encoding="utf-8")
    sheet = book.add_sheet('资质新办')
    for comname  in spider.channel_info():
        print(comname)
        for i in range(len(comname)):
            sheet.write(row, i, comname[i], )  # 写入一行数据
        print(comname, 'perform')
        row+=1
        book.save("company_contact.xls")# 保存
