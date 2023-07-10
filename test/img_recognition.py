import base64
import json
import time
import urllib
from urllib import parse

import pytesseract
import requests
import urllib3
from PIL import Image

import main


def img_recognition():
    session = requests.Session()
    # tokenurl='https://bid.zyepp.com/EpointWebBuilder/rest/getOauthInfoAction/getNoUserAccessToken'
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'}
    # res=session.post(tokenurl, headers).content.decode()
    # get_token=json.loads(res)['custom']['access_token']
    # print(get_token)
    # headers = {
    #     'Authorization': f'Bearer {get_token}',
    #     'Cookie': f'HWWAFSESTIME=1681096055386; noOauthAccessToken=f0f818706bcdacedcb8a9dd095a1dfc2; pageViewNum=16; sid=51DD427B9D46473ABBB418F2A7FD579C; XsP1ZwLDfbxnS=5dBAXpGOxMbXeXAjOvKD9Ck48Pj3.N9Ppghj.b8.3OSMtxW2NA6MbQcKfrr6ZRvwujrCzNot2BgAJXbpi3swmWA; userGuid=1047923792; oauthClientId=admin; oauthPath=http://172.16.0.34:8080/EpointWebBuilder; oauthLoginUrl=http://127.0.0.1:1112/membercenter/login.html?redirect_uri=; oauthLogoutUrl=; HWWAFSESID=1b860731d37a994cee; HWWAFSESTIME=1681096055386; uuid_aeecbc90-b7d9-11ed-abd1-1d76e963c6be=662640fb-0140-4fb0-949b-9cdedd0701c4; href=https%3A%2F%2Fbid.zyepp.com%2Fzbzq%2F001001%2F20230410%2Fd69350e2-4d0a-465b-a0a1-f60e41997599.html; accessId=aeecbc90-b7d9-11ed-abd1-1d76e963c6be; noOauthRefreshToken=07e32f765c564d865c52fe1c23f1be10; noOauthAccessToken=f0f818706bcdacedcb8a9dd095a1dfc2; qimo_seosource_0=%E7%AB%99%E5%86%85; qimo_seokeywords_0=; qimo_seosource_aeecbc90-b7d9-11ed-abd1-1d76e963c6be=%E7%AB%99%E5%86%85; qimo_seokeywords_aeecbc90-b7d9-11ed-abd1-1d76e963c6be=; qimo_xstKeywords_aeecbc90-b7d9-11ed-abd1-1d76e963c6be=; pageViewNum=17',
    #     'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'}
    pngurl=f'https://zfcg.czt.fujian.gov.cn/freecms/verify/verifyCode.do?createTypeFlag=n&name=notice&{int(float(time.time()))}'
    res = session.get(pngurl, headers=headers).content
    # print(res)
    # time.sleep(222)
    # custom=json.loads(res)['custom']
    # imgCode=(custom['imgCode']).replace('data:image/jpg;base64,','')
    # guid=custom['verificationCodeGuid']
    # print(imgCode)
    # print(guid)
    # print(base64.b64decode(imgCode))
    with open('fujian.jpg', 'wb') as w:
        w.write(res)
    image=Image.open('fujian.jpg')
    image = image.convert('L')
    # image = image.convert('1')
    count = 120
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

    # param='params='+parse.quote('{"siteGuid":"7eb5f7f1-9041-43ad-8e13-8fcb82ea831a","ImgGuid":"'+guid+'","YZM":"'+img_rec+'"}')
    # res=session.post(pagelist,headers=headers).content.decode()
    # print(param)
    # jsondata = json.loads(reslist.decode())


if __name__ == '__main__':
    img_recognition()
