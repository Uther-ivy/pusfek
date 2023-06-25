# -*-coding:utf-8 -*-
import base64
import datetime
import json
import logging
import math
import os
import random
import re
import threading
import time
import traceback
import urllib.request
from base64 import b64encode, b64decode
from http import cookiejar
from multiprocessing import Process
from urllib.parse import quote

import bs4
import execjs
import pymysql
import pytesseract
import requests
import urllib3
import xlwt
from PIL  import Image
from dbutils.pooled_db import PooledDB
from redis.client import StrictRedis



def replace_ip():
    print("ip获取中")
    headers2 = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'
    }
    url = 'http://api2.xkdaili.com/tools/XApi.ashx?apikey=XK856A0B599311BA6A85&qty=1&format=json&split=0&sign=5ef92dedf192e4c668afc6fd3e3c428b'
    url = 'http://api.xdaili.cn/xdaili-api//privateProxy/getDynamicIP/DD20222184456nmpwuS/ef63bb2fd5b411ec874b7cd30ad3a9d6?returnType=2'
    proxys={}
    try:
        text_ = requests.get(url, headers=headers2, timeout=60).text
        response = json.loads(text_)
        print(response)
        # res=response['RESULT']
        res = response['data'][0]
        ip1 = 'http://{}:{}'.format(res['ip'], res['port'])
        ip2 = 'http://{}:{}'.format(res['ip'], res['port'])
        # redisconn.set(f'ip_{ip_num}', json.dumps(ip))
        proxys['http'] = ip1
        proxys['https'] = ip2
        # time.sleep(400)# break
        print(proxys)
        return proxys
    except Exception as e:
        logging.error(f"获取失败{e}\n{traceback.format_exc()}")
        time.sleep(20)
        # continue
def run():
    # proxy =replace_ip()
    # print(proxy)
    session=requests.session()
    url = f'http://39.107.102.206:8087/permission/getSecretKey'
    print(url)
    payload = {"entstatus":"",
               "enttype":"","nic":"E",
               "esdate_start":"2022-06-13",
               "esdate_end":"2023-06-13","regcap_start":"",
               "regcap_end":"","region":"","opscope":"",
               "ltype":"","page_size":20,"page_index":3}
    headers={
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
             }
    # data_list = session.get(url,headers=headers)
    data=session.post(url,headers=headers).content.decode()
    print(data)

#
def BeautifulStoneSoup():
    # proxy =replace_ip()
    # print(proxy)
    session = requests.Session()
    url='https://ggzyjyzx.tl.gov.cn/tlsggzy/ShowInfo/Jysearch.aspx?zbfs=&fbdate=all&ywtype=006&jyly=&infotype=001&Eptr3=&Paging=2'

    header={
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        # 'Accept-Encoding': 'gzip, deflate, br',
        # 'Accept-Language': 'zh-CN,zh;q=0.9',
        # 'Connection': 'keep-alive',
        # 'Host': 'ggzyjyzx.tl.gov.cn',
        # 'Referer': 'https://ggzyjyzx.tl.gov.cn/tlsggzy/ShowInfo/Jysearch.aspx?infotype=001&fbdate=all&jyly=&ywtype=006&zbfs=',
       'Cookie': 'SECKEY_ABVK=VDv6v2vrBRGOYjyP6kSLl5i1i+kke5jqZ5/OnoV3jfU%3D; __jsluid_h=d525b4d004b68e81fe72c796e31dde94; __jsluid_s=c476ebb02fd134c84087a6c8a6d50de3; __jsl_clearance_s=1678932720.391|0|A%2Be%2B9kKBTMC1YE6byFmg9Ue5eAc%3D; ASP.NET_SessionId=osv4jd3rdzv4lgsvje2xyevo',
       'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
    }
    data = {

    }
    reslist = session.post(url,headers=header ).content.decode()
    jsondata =json.loads(reslist)

    caiGouRenAddress=jsondata.get('caiGouRenAddress')
    caiGouRenLinkPhone=jsondata.get('caiGouRenLinkPhone')
    caiGouRenLinkMan=jsondata.get('caiGouRenLinkMan')
    caiGouRenName=jsondata.get('caiGouRenName')
    xunJiaStartTimeText=jsondata.get('gongGaoStartTimeText')
    xunJiaEndTimeText=jsondata.get('gongGaoEndTimeText')
    xiangMuBianHao=jsondata.get('xiangMuBianHao')
    lsXiangMuCaiLiaoSheBei=jsondata.get('lsXiangMuCaiLiaoSheBei')
    for detail in lsXiangMuCaiLiaoSheBei:
        print(detail)
    html='<html>' \
             '<meta charset="UTF-8">' \
             '<table>' \
                ''     \
             '</table>' \
         '</html>'
    soup=bs4.BeautifulStoneSoup(html)
    table=soup.find("table")
   #.insert(1, base64.b64decode(caiGouRenAddress).decode())

    table.insert(1,soup.new_tag("tb"))
    table.insert(2,soup.new_tag("tb"))
    table.insert(3,soup.new_tag("tb"))

    table.insert(1, base64.b64decode(caiGouRenAddress).decode())
    table.insert(3, base64.b64decode(caiGouRenLinkPhone).decode())
    table.insert(5, base64.b64decode(caiGouRenLinkMan).decode())

    print(soup)
    time.sleep(222)
    print(base64.b64decode(caiGouRenAddress).decode())
    print(base64.b64decode(caiGouRenLinkPhone).decode())
    print(base64.b64decode(caiGouRenLinkMan).decode())
    print(base64.b64decode(caiGouRenName).decode())
    print(xunJiaStartTimeText)
    print(xunJiaEndTimeText)
    print(xiangMuBianHao)
def get_cookie():
        url = f'https://www.cdt-ec.com/potal-web/pendingGxnotice/selectall?pagesize=8'
        # print('*' * 20, page, '*' * 20)
        data = {
            'page': 2,
            'limit': 10,
            'messagetype': 0,
            'startDate': '',
            'endDate': ''

        }
        cookies='ckkoie.txt'
        cookie=cookiejar.MozillaCookieJar(cookies)
        handler=urllib.request.HTTPCookieProcessor(cookie)
        openr=urllib.request.build_opener(handler)
        resp=openr.open(url,data)
        cookie.save()
        print(resp)


def regex():
    all_db = [{'districtName': '远安市', 'articleId': 'cgyxgg_c60156831f3444088ff4c56dba9931ae', 'publishDate': 1667923200000,
               'procurement': '金口街道办事处2022年12(至)12月政府采购意向', 'title': '葛店镇民政办公室2022年12(至)12月政府采购意向',
               'detail': [{'proname': '湖北省远安县杨家堂矿区锂矿普查', 'price': '920',
                           'require': '开展杨家堂锂矿地质勘查工作，编制杨家堂锂矿地质勘查报告。', 'futher': '2022-12',
                           'comment': '本项目专门面向中小微企业采购'}]}]

    for data in all_db:
        print(data)
        # data=eval(data)
        title = data.get('title').replace('中共','')
        if '镇' in title:  # if
            districtName = re.findall('(\w+镇).*', title)
            if '县' in districtName[0]:
                districtName = re.findall('县(\w+镇)', districtName[0])
            elif '市' in title:
                districtName = re.findall('市(\w+镇).*', title)
        elif '县' in title:  # if
            districtName = re.findall('(\w+县).*', title)
            if '市' in districtName[0]:
                districtName = re.findall('市(\w+县)', districtName[0])
        elif '区' in title:
            districtName = re.findall('(\w+区)', title)
            if '市' in districtName[0]:
                districtName = re.findall('市(\w+区)', districtName[0])
        elif '市' in title:
            districtName = re.findall('(\w+市).*', title)
        else:
            districtName = '湖北省'


        print(districtName)
        mid=re.findall('([\d]+)',data['articleId'])
        print(mid)

def dict_text():
    headers={
        'Content-Type': 'json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'

    }
    if headers.get('Content-Type'):
        headers.pop('Content-Type')
    print(headers)
def pinyin_test():
    from pypinyin import lazy_pinyin

    print(lazy_pinyin('四月是你的谎言'))
def uuid():
    import uuid
    str(uuid.uuid4())
def io_test(text):
    time.sleep(1)
    print(text,threading.current_thread().name)
    with open(file=f"../四库一平台/企业名称/{text}", mode="r", encoding="utf-8") as r:
        read= r.readlines()
    for a in read:
        print(a)
        # return read
    r.close()
def thread_test():
    text=os.listdir('../四库一平台/企业名称')
    print(text)
    for re in text:
        thread = threading.Thread(target=io_test,args=(re,))
        thread.start()
        print(thread.name)
        # thread.join()
    # io_test(text)

def process_test():

    def test2():
        print('process_2')
    def test3():
        print('process_3')
    lis=[]
    for i in range(10):
        p = Process(target=thread_test)
        p.start()
        lis.append(p)
        # time.sleep(1)  # 1秒中之后，立即结束子进程
        # p.terminate()
    for li in lis:
        li.join()
# def chatgpt():
    # import openai
    # openai.api_key = "YOUR API KEY"
    # model_engine = "text-davinci-002"
    # prompt = "Hi, how are you doing today?"
    # completions = openai.Completion.create(
    #     engine=model_engine,
    #     prompt=prompt,
    #     max_tokens=1024,
    #     n=1,
    #     stop=None,
    #     temperature=0.7,
    # )
    # message = completions.choices[0].text
    # print(message)
def base64_decode():
    ss='5bm/6KW/55yB5rKz5rGg5biC572X5Z+O5Y6/5Lic6Zeo6ZWH5LiA5bmz6LevNDAtNDTlj7c='
    print(base64.b64decode(ss).decode())


def doc_html():
    htmldata = f'''
                    <tbody>
                            <th>{toubiaoren}</th>
                            <th>{biaoduan}</th>
                            <th>{biaoduanbaojia}</th>
                            <th>{jishufen}</th>
                            <th>{shangwufen}</th>
                            <th>{jiagefen}</th>
                            <th>{pingbiaozongfen}</th>
                            <th>{paiming}</th>
                   </tbody>   
                '''
    html = f"""
                <div>
                    <table border="='0.5" width="70%">
                        <p class="pj">招标投标项目名称:{toubiaomingcheng}</p>
                        <p class="jg">招标代理机构：{zhaobiaojigou}</p>
                        <tbody>
                            <td >投标人</td>
                            <td>标段	</td>
                            <td>标段报价(元)	</td>
                            <td>技术分</td>
                            <td>商务分</td>
                            <td>价格分</td>
                            <td>评标总分</td>
                            <td>排名</td>
                            <td>备注</td>
                        </tbody>
                            {htmldata}

                    </table>
                    <p>公示日期：{gongshiriqi}</p>
                    <p>公示结束日期：{gongshijieshuriqi}</p>
                    <p>联系人：{lianxiren}</p>
                    <p>代理机构电话：{dianhua}</p>

    </div>
            """

def img_recognition():
    session = requests.Session()
    tokenurl='https://bid.zyepp.com/EpointWebBuilder/rest/getOauthInfoAction/getNoUserAccessToken'
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'}
    res=session.post(tokenurl, headers).content.decode()
    get_token=json.loads(res)['custom']['access_token']
    print(get_token)
    headers = {
        'Authorization': f'Bearer {get_token}',
        # 'Cookie': f'HWWAFSESTIME=1681096055386; noOauthAccessToken=f0f818706bcdacedcb8a9dd095a1dfc2; pageViewNum=16; sid=51DD427B9D46473ABBB418F2A7FD579C; XsP1ZwLDfbxnS=5dBAXpGOxMbXeXAjOvKD9Ck48Pj3.N9Ppghj.b8.3OSMtxW2NA6MbQcKfrr6ZRvwujrCzNot2BgAJXbpi3swmWA; userGuid=1047923792; oauthClientId=admin; oauthPath=http://172.16.0.34:8080/EpointWebBuilder; oauthLoginUrl=http://127.0.0.1:1112/membercenter/login.html?redirect_uri=; oauthLogoutUrl=; HWWAFSESID=1b860731d37a994cee; HWWAFSESTIME=1681096055386; uuid_aeecbc90-b7d9-11ed-abd1-1d76e963c6be=662640fb-0140-4fb0-949b-9cdedd0701c4; href=https%3A%2F%2Fbid.zyepp.com%2Fzbzq%2F001001%2F20230410%2Fd69350e2-4d0a-465b-a0a1-f60e41997599.html; accessId=aeecbc90-b7d9-11ed-abd1-1d76e963c6be; noOauthRefreshToken=07e32f765c564d865c52fe1c23f1be10; noOauthAccessToken=f0f818706bcdacedcb8a9dd095a1dfc2; qimo_seosource_0=%E7%AB%99%E5%86%85; qimo_seokeywords_0=; qimo_seosource_aeecbc90-b7d9-11ed-abd1-1d76e963c6be=%E7%AB%99%E5%86%85; qimo_seokeywords_aeecbc90-b7d9-11ed-abd1-1d76e963c6be=; qimo_xstKeywords_aeecbc90-b7d9-11ed-abd1-1d76e963c6be=; pageViewNum=17',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'}
    getcode = 'https://bid.zyepp.com/EpointWebBuilder/rest/frontAppNotNeedLoginAction/getVerificationCode?params=%7B%22width%22%3A%22100%22%2C%22height%22%3A%2240%22%2C%22codeNum%22%3A%224%22%2C%22interferenceLine%22%3A%221%22%2C%22codeGuid%22%3A%22%22%7D'
    # data ='params=%7B%22siteGuid%22%3A%227eb5f7f1-9041-43ad-8e13-8fcb82ea831a%22%2C%22ImgGuid%22%3A%2266748e96-9f07-475e-879b-518701914862%22%2C%22YZM%22%3A%223w5e%22%7D'
    res = session.post(getcode, headers=headers).content.decode()
    custom=json.loads(res)['custom']
    imgCode=(custom['imgCode']).replace('data:image/jpg;base64,','')
    guid=custom['verificationCodeGuid']
    print(imgCode)
    print(guid)
    print(base64.b64decode(imgCode))
    with open('中原云商电子招投标平台.jpg', 'wb') as w:
        w.write(base64.b64decode(imgCode))
    image=Image.open('中原云商电子招投标平台.jpg')
    image = image.convert('L')
    # image = image.convert('1')
    count = 180
    table = []
    for i in range(256):
        if i < count:
            table.append(0)
        else:
            table.append(1)
    print(table)
    image = image.point(table, '1')

    img_rec= pytesseract.image_to_string(image).strip()
    # re.findall(r'',img_rec)
    print(img_rec)

    pagelist='https://bid.zyepp.com/EpointWebBuilder/rest/frontAppNotNeedLoginAction/pageListVerify'

    param='params='+urllib.parse.quote('{"siteGuid":"7eb5f7f1-9041-43ad-8e13-8fcb82ea831a","ImgGuid":"'+guid+'","YZM":"'+img_rec+'"}')
    # res=session.post(pagelist,headers=headers).content.decode()
    print(param)
    # jsondata = json.loads(reslist.decode())

def wirte_xls():

    with open('../四库一平台/test_siku/companyname/河北二级.txt', 'r', encoding='utf-8') as r:
        datalist=r.readlines()

    print(datalist)
    # time.sleep(2222)
    book = xlwt.Workbook(encoding="utf-8", style_compression=0)
    sheet = book.add_sheet('河北二级数据', cell_overwrite_ok=True)
    caption = ['company', 'phone', 'email', 'address']
    print()
    for i in range(0, len(caption)):
        sheet.write(0, i, caption[i])
    print(len(datalist))

    for i in range(len(datalist)):

        print(type(datalist[i]),datalist[i])
        # time.sleep(2222)

        if '[' in datalist[i]:
            for j in range(len(caption)):
                print(i+1,j,eval(datalist[i])[j])
                sheet.write(i+1,j,eval(datalist[i])[j])  # 写入一行数据

        else:
            style = xlwt.easyxf('font: bold on')
            sheet.write(i + 1, 0, datalist[i], style)


    book.save('./河北二级数据.xls')  # 保存



def parameter_setting():
    start = 0
    paramters=list()
    for a in range(100):
        end = start + 1500
        if int(datetime.datetime.now().day) % 2 == 0:
            paramters.append(f'company_list[{start}:{end}]')
        else:
            paramters.append(f'company_list[{end}:{start}:-1]')
        start = end
    print(paramters)


if __name__ == '__main__':
    start=time.time()
    print(start)
    # pinyin_test()
    # print(jiemi_('8lr7FkeuVfbi9O6o+zpsL5vX0Ordls4t3s53kk7WsQr2IX+Lvfxvu+iHT9MmWA2h+hxiU2ZZPzGO0F7NVbc/qItxGeJAWn5awObErrYTnCgJXVEmYn+gJmqkLWJ/8K58+31M4tS7MLGXiX0Nt8jdCRtM62LLDgslBRuthVk/BOO+WvzzH2XAXTEuhWp+r5QUL9WzazA8fZsMydMFf4ASy5s3swPSx43yDId5cntoDM04xB0tjN5Iqk0ADHjY3RD5OrCmlELcBHwUF0ZPbA9WoR4rJfi/Dy5I3cpirrd7C1HI1ayKb1mIJf/PtnxTjxigKpL2ufXdwRWMMMU90ZVBsshA9e1g4XPydsG7A1urcnzu7Lt37unx+gF0bnmBzeeJjfU23nu+qSpDFqGQXJCRfGWn+4G1qh6BwPMOoc8tFrs5vUFOhCto9xvSgN6p/ubA'))
    # print(jiemi_('95780ba0943730051dccb5fe3918f9fe1b6f2130681f99d5620c5497aa480f130cfc405ce24fe9ec2b5f5141a9fbf9ed5fde5a1fc51762e01b3bdd0b880292123ca63a4c2b83215997eca55212b1b646d7e57845dec2737abdedca80e6de4faa9c301ee7ea4405617a98139bade7879559ec2306251039dea030ff6f4e227a272d5773a7a71f897e5a74f090ab564e53a3c7e6ec8d2909dbb7d6f4c94ac10fe31bd863e7c0ce0f14c3e3469c16930752c9c549628ae1786ba89888ca81805c7a1012e65793afbb43b4b7624c361d8cb562e8f54b46e38b1df4366fd40c72c15600d61e8f39fcc299b159d7998c4598167f1e291297e6f887df2f851e6dc0e056f3fcff2843006d31da40b3c1c89b0dd4903c47bd1fb623aa6641d49be9043e9cd5ebbb5ee18e723b0a9e1d060f02598cc65eaad1ed9b0c7c0c2e89c61d18b043a0bab5b5353e3e01a322a139075ea153389e4cf656b6ed04a48e57c3b9cd999fab65fe03d6fc374caf65c49ac5aeefb5a7d67fa87a78028ff530a98fdb96d9a7bb543c4bbf7bc2534a168e3975e4ac2a8f96859a98c124f555f2a400fb5c3b8f445fd9de77fa34cb60cd9dbd2bafa39d37802fc558d06d8e199234da9c1c271277fff9fd7b59b9d058860dab062e56132404e972d3dd0810079f56ec7dbc892378bca1ae9acb194ffbf4cdc5516a4453e422697be7bfb9b71e5bd1513d6b2a5163841870eb2e3ad6d0102fe810fdd62972942b416b89ba52a9441d293a73160512fa667ba47fd6b4c22e9ff35e06385fd1ab747b7655507feebea7226e6a1e85b585f32b53edcb603f73757bd95bbb32c4c1e337de79830aaf5338c7e705ff852bd5ed1fbdb629a9e795e25aa5aeb82696be86c7278f70d7af6a5e7ee75cf5d3f8291fbb575fc4f38c6c2c5301e7792ed5df7ec508d55b0aa4eaa18219ba5589c087cfeb6960bfd7f31bd5c27d8fe5fb18c0d33a416062e437c55067516178b3162dfbf5ce6ba4b3c348e2b9b70c4b26a7f207004a003253a2f96c9b87fc31824d053f1d702cbe2df9135cd557fbb0fd956c457da36d9aedc8c4c48a7673d143a364293a13cc7187693ebf499ac28d0c9fae35cc73134dfecfb46097a5e216470690e5f54452f2b03a864200cfba94a6b39b969878d1aa4774fe0aebda734ffe71431424d2f019321de1c22579c7fa4a4dba2aad7261336a45a627b2ba8c2e688cfc6253d77c886690f23e23cb7eb22df7ccd8bee2b601a8dfaa7198bc7e2ab44de9556c9615d7139cf505bb4902fa4f189d3fed6d72830fec4509108c6d12827fea4ff24be13a4ac4834eef2d519e1f68047820573e90e1326cf45c668008793a0a9207d810f1d0a301da1f61200085d0a23b7c1bdc537fc06fc5e2a247e20087fccc2cfd2f3f3941d6c46f753338059b145f789a28f59f54a2938da8cd2072ee764f75a0509d5c2c43e0a9a73753290db4782d898e3f0d72d2fd4455bb0b08cfc187e46a0e0a5bd40d815b66628b5ff11e24d5ba9137fb4076b149afb23be34bceaf5c2c6c54f6f9c9e0231e6026298549a4a3467266dc7488780e3019a17bb4700d666d9725a1d085b0bb388868225d42e41d28059dcba7294795814d8a4fced52c5214f77ba4b09b5e672472330cf111c3680aec7b5ec584f735ebf0116333506e29c8226990f3c844f7c385b5662f252a229af61537ecdb184191af331c2a45e125862ea8b20a41461582468eb9c6831094c13923ef6dfccdef21edd8797974b92d4ef844acab0bdc6a173fbb4d7eccd6e415c11bdd5c244a1088d83121398b9a48e826c6ee9d1d9b50e318a8de6ee9970108313797f2d661be368d9e812aa68166675edf831c6ec5d3d37c62f59d880544b79fdea5f5eaaad27512d6f6db00ef8c8d4df77e6ebd784ba2cda3078777a3f52e27847b766e557636357c33a1087480e2dd55bcca6143e9685f982042fb68b1a40f72b07aae1fc2dba5d89b959f7bd584167e953bb9a40ac0625fcd7942aa021f5cbca0545869d78b285ca2482a246a963bed3e2159ec3baf25a8eeed280b966be103bc4fae89fc03b0614ea9682934d408a7b57b2d7d3dd39a2de184e49e7a18013ff523df424e29a04830cb64bfb06dfd80aaba6410b7d98a083ae9a654197a615401c29f449035e03426ff332c236a64427edc102e32fe6ed8e8a9ee4272d82d29073a75a25beea2bb15201b27fe07d0efda45e17a886aa462321a0d32a0e84b7c8aef9976cff2635db113187d22dc527115f1bd65740c9cd3c4e3d66cc4d75bc0c0290e2f454a0872c544a65aff8ed88c5523f742ffc4f6a01ec5088aba67df65afbddab6fd096fc955db14fcece43cc7f03fb2dbfa3befb8a4d06c266e554caa8bf1b8af0f7b61adf50fc63835feccd05d6bf78a8cc928f37ca8c51295c671f9e046277706cbec635842d894f262261d13cf61072d2f900fa06d041f37b443b47b74428219485dd41b2a455d693c2fce87c7d52b8f4c0d90fdfe3867e7b9bc1ae2fcc7b5e6f9d7c7c2720322c5fd6209a1bd2b07e8273b72283183e08f1e24b2e847451d455882497d3c866382fe6ef506933f21eb5065f3ca7eff0830269994846b53b11664a9e0196c96501efd26e6602f8db69174558cc28a2d693eaa8712f882603535c16af2c5748d9d0c2ce36b353f200a9d446a6b98b49629e301c1028d1cd89593f60db869762c865f9247b8c47bc16558ab11a188806329984ad67d994ab3d3f400549b15ac45532225fda68f8b04a1dd22601290d8e8433fef1192dcbc22e56db588e8e950e65a26f64d77ec12bcce504c958561c2e187f038e4453f893c1b8c664f13dec2f30a380e5502588601a3aa18b2c225cdc5269f9e9d96838c92e9e00c5eb95f4e3f3e8983a3937a67eaf1751cdcf0807b47f49854d44a19fb0fcab6c076f491d20df205d958974c78de0edb659ec26d4cac553ee933c8973a2d41cb9f7f5e5e6af045ae95c171b6b14d81e026f9b01e96bbcf67a288b18205b59dbf673876707188f2473c6f0281af1448dab3a91beba35dd7b46d1e72e8303a315be473194b6fbab28f7344724a0ecbbabc3b1faa1b17d44720ac073dbb6bf6a55922461be96d46867c7737bc8d964e7c13f7f91da2f2fcbe24301aeb40948c69fee9babba2ed470339bb80f0a6230ba8fa80900b699aa26b25e0c350da3ef5e832e2d3f6e5698bafe53f4610d9d34bfb574834200b64f785441b6368e45885c6179b6bf7593e8713a285ebe32e2cafe8147edbc66a3aeb7306b10aaec9991713745e73ac031bccb90fa176cf49223c5fd075ecf740a6e24569bb26390beffb7fdebab8bc60e61dfecb2a6867c06b123cbf1b85c1980c3bbb18a7a1141018e58ac5f8805a3648e95ec6e42dd66bbfd573058f71a5effbabc2f67d0e2a4d95f9669665d8e16d26dfe8cc19e287eb7a90ed9f2f21d906b1b0fb6f7f0823f7eb1fb88c628da76f3e69886052f5c2245b640a2191785d01e913fd8a3fd9c2408db9c69997778b8833bf042d42508036ffdc112225a18a453d5802ef8e70452da29e3057d2bc4965ccf49fb8e30bd0c887525e82de3269e258b139e15d5f35a2329ba00f78e5180a38c4a82c0d3aa835739ccec78196db548bd5a331274608e2ef7ebc701d314e91cbb3c81e1d00e9e1467997d5ab8216bbd15171a5d8074da75819bb42ff5b33078b8172de4d3f9db044b3079f32e955c3d97c446ff4057cdce498b8e6d1ac8b5dcd7e5fea1dcdc67d985488fd87a24d6ca98aacecdce96291df5ed00c79fa6eaa42310c101e8fdca1b6eb5c966143f4ce5b61d227391e6a6f8e347a8313795ecbfdafce334b101e4bfaae9359f6ca06bca568f9c9ae2b7bbfb95a612e2b574643ee711de77cc165db2dd0dbcbb0abba887a66a17b4a855bf175042ce8623ca77d3741ddd10ac484955225ee622a8140d7c702c623465da1075a9a5918ad336be58e08aac7b7e11fad929cc59d9c13b3ad53b8e6c292b5fd9190c2fc891d0d18c7316056daff1f98b29579adbdd72247f8c8caf81b6524fdd0bb96f6729a0c7d45775ae2cb716cf93e326fe50feafefb133da96bbb7b409eb72612697a593718a2df67a305a1a7f831a290755eb106845d54ec314bc3da70ad3caeea524838e415fd6cc3dbd92adf2105b61a288b8c5fdbf7e1d51530010a26efdc173bab2140bb5e4265d5ea9ff440f6a7f7f6faaebb00d2ea673045e50d66d0fd74c3b5aff6010c831d72a49a74b47451c424242f1750c196f9b5d32aa82d3d147dca1fcf2200bd251ed600ab475b8bd6414ee1c56491b04c93b5acc9ef1ad70be2f1f131a54053996c0c269d6dec19851722fbfc9d74917b8ab8763b07ec36c5ee1f86535af9b8f7524b956c6dd7157ad350cc8fb0cb6874970677080dee8f37d7fa3e22d3328766a0e84d74bf4687082569b562b58265111c8b1c5a3c277e03f33c490eb75c1c132723e5de83782eb976c5f0aa7dbcd8fcd79b124eeb7d2844bc0063e96563de0b172295cd21ff9b446b0a641f90b208ba9d40394af9498c2b113836047676af914de6cf559df285b30d844cceb8f392b70a63dd9adb9e1ea7221f8f025a69107f14e670584d776d85f226d39e5429989f27b0ba77e54fbee476dce617cc0b722960c0709c90aec8bf83bafe7244f9b60ab889fe16232d589ae6373e908c2da415bc5f1478b1824e3f980d2279a9734d377e1158619c16ed3487cac9fdc75d6a4cd86046d24bed41005c4c7e560d5dcd96da19cfc4e11ca7187f7bfaf2564fb28fdedd17e8b5341344dea6062b79cc'))
    # get_cookie()
    # dict_text()
    # wirte_xls()
    # lis.append(p)
    # thread_test()
    # uuid()
    # parameter_setting()
    # times()
    # pop_test()
    # urllibtest()
    # run()


    # img_recognition()

    # process_test()
    # readis()
    # replace_ip()
    # base64_decode()
    # nodejs()
    times()
    # runjs()
    # regex()
    # mid = str(time.time() * 1000)
    # print(mid)
    # print(int(mid[::2]))
    print(time.time()-start)
