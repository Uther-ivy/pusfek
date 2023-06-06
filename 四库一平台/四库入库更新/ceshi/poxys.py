import logging
import traceback

import requests
import json
import time
import redis
# redisconn = redis.Redis(host='192.168.1.66', port=6379, db=2, password='1214')
# while True:
#     url = 'http://api.xdaili.cn/xdaili-api//greatRecharge/getGreatIp?spiderId=069181704df943ee9213ce0aa266124e&orderno=YZ202210191416PSDtRW&returnType=2&count=10'
#     try:
#         print('开始抓取代理...')
#         text = requests.get(url, timeout=120).text
#         print(text)
#         response = json.loads(text)
#         # ip = {'http': '{}:{}'.format(response['RESULT']['wanIp'], response['RESULT']['proxyport'])}
#         # print(ip)
#         # redisconn.set('ip_ygY0', json.dumps(ip))
#         proxys = {
#             'http': f"http://{response['RESULT']['wanIp']}:{response['RESULT']['proxyport']}",
#             'https':f"https://{response['RESULT']['wanIp']}:{response['RESULT']['proxyport']}"
#         }
#         with open(file=f"poxy.txt", mode="a", encoding="utf-8") as w:
#             # p = json.loads(redisconn.get("ip_03"))['http']
#             data = w.write(str(proxys) + '\n')
#         #     print('完成')
#         date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
#         print('存储成功',proxys, date)
#         time.sleep(400)
#     except Exception as e:
#         print("出错", e.args)
#         time.sleep(30)
#         continue


# while True:
#     url = 'http://api.xdaili.cn/xdaili-api//greatRecharge/getGreatIp?spiderId=069181704df943ee9213ce0aa266124e&orderno=YZ202210191416PSDtRW&returnType=2&count=10'
#     try:
#         print('开始抓取代理...')
#         text = requests.get(url, timeout=120).text
#         print(text)
#         response = json.loads(text)
#         ip = {'http': 'http://{}:{}'.format(response['RESULT']['wanIp'], response['RESULT']['proxyport'])}
#         redisconn.set('ip_ygY0', json.dumps(ip))
#         date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
#         print('存储成功', ip, date)
#         time.sleep(400)
#     except Exception as e:
#         print("出错", e.args)
#         time.sleep(30)
#         continue


def replace_ip():
    print("ip获取中")
    headers2 = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'
    }
    redisconn = redis.Redis(host='192.168.1.66', port=6379, db=1)
    url = 'http://api.xdaili.cn/xdaili-api//greatRecharge/getGreatIp?spiderId=069181704df943ee9213ce0aa266124e&orderno=YZ202210191416PSDtRW&returnType=2&count=1'
    while True:
        try:
            text_ = requests.get(url, headers=headers2, timeout=60).text
            response = json.loads(text_)
            print(response)
            res=response['RESULT'][0]
            ip = {'http': 'http://{}:{}'.format(res['ip'], res['port'])}
            redisconn.set(f'ip_03', json.dumps(ip))
            print('存储成功', ip)
            time.sleep(400)# break
        except Exception as e:
            logging.error(f"获取失败{e}\n{traceback.format_exc()}")
            time.sleep(20)
            continue

replace_ip()