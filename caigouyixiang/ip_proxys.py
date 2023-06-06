import logging

import requests, traceback
import json
import time
import redis
def replace_ip():
    # redisconn = redis.Redis(host='127.0.0.1', port=6379, db=7, password='1214')
    print("ip获取中")
    url = 'http://api2.xkdaili.com/tools/XApi.ashx?apikey=XK2C1C3E708F5D494F17&qty=1&format=json&split=0&iv=0&sign=07f208e19a95015125b82b5019350d4e'
    headers2 = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'
    }
    try:
        text_ = requests.get(url, headers=headers2, timeout=60).text
        response = json.loads(text_)
        print(response)
        # res=response['RESULT']
        res = response['data'][0]
        ip_proxy = 'http://{}:{}'.format(res['ip'], res['port'])
        # redisconn.set(f'ip_{ip_num}', json.dumps(ip))
        print(ip_proxy)
        return ip_proxy
    except Exception as e:
        logging.error(f"获取失败{e}\n{traceback.format_exc()}")
        time.sleep(20)
    # continue



if __name__ == '__main__':

    replace_ip()





