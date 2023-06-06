import json
import logging
import random
import re
import time
import traceback
import urllib.parse

import redis
import requests as requests

from zhixingxinxi.bdsxspider import bdzxspider

if __name__ == '__main__':
    fil = '60'
    flies = f'企业名称/{fil}.txt'
    spider=bdzxspider()
    # name = '北京百度建筑装饰工程有限公司'  # 公司名或人名
    # card = ''  # 身份证或组织机构代码9113010057****7053
    line = ''
    try:

        with open(file=flies, mode="r", encoding="utf-8") as r:
            data = r.readlines()
            # print(data)
        # data=['北京百度建筑装饰工程有限公司']
        spider.replace_ip()
        try:
            for line in data:
                print(type(line), line)
                zhixingdb = spider.bdzhixin(line.strip())
                print(zhixingdb)
                if zhixingdb:
                    with open(file=f"zhixingxinxi/zhixing{fil}.txt", mode="a", encoding="utf-8") as w:
                        data = w.write(str(zhixingdb) + '\n')
                    print('完成')

                else:
                    with open(file=f"zhixingxinxi/meizhixing{fil}.txt", mode="a", encoding="utf-8") as w:
                        data = w.write(str(line))
                        print(line, '没搜到')
            w.close()
        except Exception as e:
            print(e)
        r.close()
    except Exception as e:
        logging.error(f"{line}获取失败{e}\n{traceback.format_exc()}")
