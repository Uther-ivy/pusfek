import requests, traceback
import json
import time
import redis
redisconn = redis.Redis('192.168.1.57', db=7, port=6379, password='1214')
while True:
    url = 'http://api.xdaili.cn/xdaili-api/privateProxy/getDynamicIP/DD20222186589rg06pn/3f8d161ab72711ec874b7cd30ad3a9d6?returnType=2'
    try:
        print('开始抓取代理...')
        text = requests.get(url, timeout=120).text
        print(text)
        response = json.loads(text)
        # print(response)
        ip = {'http': 'http://{}:{}'.format(response['RESULT']['wanIp'], response['RESULT']['proxyport'])}
        redisconn.set('ip', json.dumps(ip))
        date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        print('存储成功', ip, date)
        time.sleep(1800)
        # time.sleep(240)
    except Exception as e:
        # traceback.print_exc()
        print("出错", e.args)
        time.sleep(30)
        # continue







