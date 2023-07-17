import json

import redis
import requests

from spider.redis_company import RedisDeduplication

session = requests.session()

def list_parse():
    dedup = RedisDeduplication()
    region_code=['110000','120000','130000','140000','150000','210000','220000',
    '230000',
    '310000',
    '320000',
    '330000',
    '340000',
    '350000',
    '360000',
    '370000',
    '410000',
    '420000',
    '430000',
    '440000',
    '450000',
    '460000',
    '500000',
    '510000',
    '520000',
    '530000',
    '540000',
    '610000',
    '620000',
    '630000',
    '640000',
    '650000']
    # [["2022-06-20","2023-06-20"],["2020-06-20","2022-06-20"],["2018-06-20","2020-06-20"],["2013-06-20","2018-06-20"],["2008-06-20","2013-06-20"],["","2008-06-20"]]:
    for region in region_code:
        for esdate in  [["2022-06-20","2023-06-20"],["2020-06-20","2022-06-20"],["2018-06-20","2020-06-20"],["2013-06-20","2018-06-20"],["2008-06-20","2013-06-20"],["","2008-06-20"]]:
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
                           "region": region,
                           "opscope": "",
                           "ltype": "",
                           "page_size": 100,
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
