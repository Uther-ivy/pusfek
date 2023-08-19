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
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'}
    pngurl=f'https://zfcg.czt.fujian.gov.cn/freecms/verify/verifyCode.do?createTypeFlag=n&name=notice&{int(float(time.time()))}'
    res = session.get(pngurl, headers=headers).content
    print(res)
    # print(base64.b64decode(imgCode))
    with open('fujian.png', 'wb') as w:
        w.write(res)
    image=Image.open('fujian.png')
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


# def pojie_yzm():
#         # 读取背景图片和缺口图片
#         bg_img = cv2.imread('bg.jpg')  # 背景图片
#         tp_img = cv2.imread('tp.png')  # 缺口图片
#         # 识别图片边缘
#         bg_edge = cv2.Canny(bg_img, 100, 200)
#         tp_edge = cv2.Canny(tp_img, 100, 200)
#         # 转换图片格式
#         bg_pic = cv2.cvtColor(bg_edge, cv2.COLOR_GRAY2RGB)
#         tp_pic = cv2.cvtColor(tp_edge, cv2.COLOR_GRAY2RGB)
#         # 缺口匹配
#         res = cv2.matchTemplate(bg_pic, tp_pic, cv2.TM_CCOEFF_NORMED)
#         min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)  # 寻找最优匹配
#         # 绘制方框
#         th, tw = tp_pic.shape[:2]
#         tl = max_loc  # 左上角点的坐标
#         br = (tl[0] + tw, tl[1] + th)  # 右下角点的坐标
#         cv2.rectangle(bg_img, tl, br, (0, 0, 255), 2)  # 绘制矩形
#         cv2.imwrite('out.jpg', bg_img)  # 保存在本地
#
#         # 返回缺口的X坐标
#         return tl[0]




if __name__ == '__main__':
    # img_recognition()


    ss="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"

    print(base64.b64decode(ss))
    with open('中国石油招投标网加密.png', 'wb') as w:
        w.write(base64.b64decode(ss))
    image = Image.open('中国石油招投标网加密.png')
    image = image.convert('1')
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
    img_rec = pytesseract.image_to_string(image).strip()
    # re.findall(r'',img_rec)
    print(img_rec)
