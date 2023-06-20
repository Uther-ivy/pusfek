import json

import redis
import requests

from spider.redis_company import RedisDeduplication

session = requests.session()

def list_parse():
    dedup = RedisDeduplication()

    for esdate in [["2018-06-20","2020-06-20"],["2013-06-20","2018-06-19"],["","2008-06-20"]]:#[["2022-06-20","2023-06-20"],["2020-06-20","2022-06-20"],]
        for page in range(1,501):
            print('*'*20,page,'*'*20)
            url = f'http://139.224.15.208/api/main-search/'
            print(url)
            payload = {"entstatus": "",
                       "enttype": "",
                       "nic": "E",
                       "esdate_start": esdate[0],
                       "esdate_end": esdate[1],
                       "regcap_start": "",
                       "regcap_end": "",
                       "region": "110000",
                       "opscope": "",
                       "ltype": "",
                       "page_size": 80,
                       "page_index": page}
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
            }
            res = session.post(url, headers=headers, data=payload)
            if res.status_code==200:
                data_list = json.loads(res.content.decode())
                for db in data_list.get('data').get('list'):
                    print(db)
                    dedup.add('new_company_name', str(db.get('entname')))
                    dedup.add('new_company_organization', str(db.get('uniscid')))
            else:
                break
list_parse()
