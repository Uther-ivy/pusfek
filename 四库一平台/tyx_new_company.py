import json

import redis
import requests

from spider.redis_company import RedisDeduplication

session = requests.session()

def list_parse():
    dedup = RedisDeduplication()
    for page in range(1,501):
        print('*'*20,page,'*'*20)
        url = f'http://139.224.15.208/api/main-search/'
        print(url)
        payload = {"entstatus": "",
                   "enttype": "", "nic": "E",
                   "esdate_start": "2018-06-13",
                   "esdate_end": "2020-06-13", "regcap_start": "",
                   "regcap_end": "", "region": "", "opscope": "",
                   "ltype": "", "page_size": 20, "page_index": page}
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
        }
        # data_list = session.get(url,headers=headers)
        data_list = json.loads(session.post(url, headers=headers, data=payload).content.decode())
        for db in data_list.get('data').get('list'):
            print([db.get('entname'),db.get('uniscid')])
            dedup.add('new_company_name', str(db.get('entname')))
            dedup.add('new_company_organization', str(db.get('uniscid')))

list_parse()
