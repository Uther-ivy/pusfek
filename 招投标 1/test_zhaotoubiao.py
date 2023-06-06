import json

import requests


def run():
    # proxy =replace_ip()
    # print(proxy)
    session = requests.Session()
    url = 'https://ec.ceec.net.cn/HomeInfo/ProjectList.aspx'
    print(url)
    data = {"_bigtype_base64": "WgBCAEcARwA=", "_smalltype_base64": "aAB3AA==", "_pageIndex": 2, "_pageSize": 20}
    header = {
        
# 'Accept': '*/*',
# 'Accept-Encoding': 'gzip, deflate, br',
# 'Accept-Language': 'zh-CN,zh;q=0.9',
# 'Connection': 'keep-alive',
# 'Content-Length': '95',
# 'Content-Type': 'text/plain; charset=UTF-8',
# 'Cookie': 'HWWAFSESID=f43be7924576499ccf; HWWAFSESTIME=1673417603440',
# 'Host': 'ec.ceec.net.cn',
# 'Origin': 'https://ec.ceec.net.cn',
# 'Referer': 'https://ec.ceec.net.cn/HomeInfo/ProjectList.aspx',
# 'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
# 'sec-ch-ua-mobile': '?0',
# 'sec-ch-ua-platform': '"Windows"',
# 'Sec-Fetch-Dest': 'empty',
# 'Sec-Fetch-Mode': 'cors',
# 'Sec-Fetch-Site': 'same-origin',
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
# 'X-AjaxPro-Method': 'getdata',
        
    
        
        }
    reslist = session.options(url, headers=header, verify=False)
    print(reslist.status_code)

def run1():
        # proxy =replace_ip()
        # print(proxy)
        session = requests.Session()
        # url='https://www.cdt-ec.com/notice/moreController/toMore?globleType=0'
        # reslist = session.get(url).content.decode()
        # print(reslist)
        import uuid
        url = 'https://cf.aliyun.com/nocaptcha/analyze.jsonp'
        str(uuid.uuid4())

        data = {
            'a': "CF_APP_WAF",
            'asyn': 0,
            'callback': "jsonp_017842576744580696",
            'lang': "cn",
            'n': "225!cJTY0pzWooia8HRSioXogOAXi+ljrqtQokHIHC3NZnjuTFlvtfo0+STEJKOnvTf1AYe/2l+lVnrW87cRbcjVNn5O1aCVW+PViw1KrX1popsioJiRDG/+f460Qk0UDMzhfiN2TEVuqHfeSJ3wDGHzfeGeuiTuhXdqGz5t0dQ1jcI4oL3jDGHzfeG0QEDdFMXSkNvgofDdjxfhoeiK29thj7hQuo01K/+zMCB3HfiSYsE3HnuE5Ig4AcclWTMke5d4fiFRGU4KjcI4oJijDlH+fej0Bz0KDIFE5LLHbFYNw8Ihn9oiV1H2xb0uCUe6yL1BCZ+VZt3vAXgDHql/0RKDmB08WRcfyXAlOkd5FvTq2grTbewzhd7GshocR00NS2JqvKEUK+wOx2I/J6M/VZvkMeCvpaQq9y1Rml+InjTYA5ribbqV/NkO6QuvOCqu/XXNuE/40me8jcfroJiRDwOIzAqo7+WdDMXhfo0vKMXa+JUzMV5gIj+/FN/xN4DVETM4gN9H7l+7wQHD1JGli2ZVpYBdg8qfrAzPrJmIskaTezTuBogWmSMcD5mfGvGyzcCh3K3HbBLheI/KbLiagbpS+xOcAK5BHTiHIqBK3ZFk+YN6yO3JkBQlRZxn0BDJDWneazUY1SQ854mX7Ib9HGxZKIeg49T04DMKhSBwtTJhwwfzfGYBSU14pLLFiq9iBx+WS6D2XsdjlU397w8KjGYw0D/5nZaIO6u5yn8RFXaZWCQTih7aJDu7UhclzDECJMNpQU+4jwhRJ5xm/ozEXNgZ/382aNtpcnpR108nn/esqrJ56lcV/EHN27HO/nsoYTEO9Gr1FVW7XE/u3d8X30xceKuge7o6FKSExS4fDaS3kwSIkW5ci7jxwkVo6parAvAxvVZ+0FJxmbuxK8FE9z77gCOrK5tTE/ugGFeewYwAoEj57o79ZtKKhoRpaftZhMrPnQIfaf/IYh30kZUaAbni49zaPn2ZXcjEVwl8ezKOIVd8qM3dWZjodnXgd5idzBHeg7qTUsXM0EOJnNfMq7YsPJ4L6IKWKxjvGtu9pU3MzzXvCSwHTAyX/RjN3QnhwkvcmUta4lbfD74Lfi/LiYNx/bsAnJz679XB5Vfyrab2LyPFKX3UdE++t6ceEkHTOgUs0u5fa7TMQcfHubCkFRvFdMEgf0/kER9ASkfALMOsIYyG8OUJDCFrha1t8L3gYBFtryBB5dAPR1O3JMhJO58u7SNlGLQZ23p5JruYCYmYD9HXxcCm6lDe15S+8Lbujaphlx0PxkjtbzIQNKOMrOrAB1v7u4PowqNwwywSTRF25ea+CCMOVsD6emAz+2TBMEmJrwUwuQY13T5GeUQVku4V9js7DwEaCHPmDSPReTDXEbaL69MsChI6YA0KL34tLGXsoRKuJknkUJ6OnboW/yC8D0gIULZJWucGIQD/yZhVlT2M+YhJjInlg3/lnVWF462sVu+N5i/bLSv9DWGV41TtvXdXiRbM2oavtcx3r9hZ6nJbQI5nshudVDI3X01xFyMNaCAdiOgOQWdJnWCrMoauJ6eTIraICZQRtgCuYUVRp2Hgjfu0YdtyrXhlDOvhH39DUcCWvkOtSWCCHL2P24FxP9lW7OZ3cDJw0nDDf5q3hXlhaEyS4LnE7Wwmg3KQoieZ/xbupyG9CoU/xKsCz+oXZs3x5yvjfPw0yC1hbK6Nmtew0cxiQiZCOgCZGTBCd4cVZpaYrfQPxM2s9C8zQmjUgDK1WEmVlvdG1yfDciWf6Qe/+X1k3eoSGBaZ1RSAmr2n3oaLuZoIbFtr/4gkjydxRm5xPx8VMhP2qHtaU9gG4Atdz20vX8bBgqTdS/rmAU/7q4NOM4muGFrPi2Dc4ByoOORR05mv8SMz06RU2fttabrmtceHf9boV7ZywTDKRtro4u7NJS98h1hzhho5GSKBK1+R0Pw5voF8T0no82C91V+IIrcpGJ9hbm6=",
            'p': "{\"key1\":\"code100\",\"user\":\"default\",\"umidToken\":\"GF31FFA61DE424AC3207FFEF656BC15D051F80DBC19789F643F\",\"ncSessionID\":\"5e70deca3ddd\"}",
            'scene': "register",
            't': "98644a12-e8f7-4dd7-935d-c22335ee4092",
            'v': 1
        }
        reslist = session.get(url, params=data).content.decode()
        # print(session.cookies)
        print(reslist)
        print(random.random())

