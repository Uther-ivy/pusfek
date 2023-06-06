# -*- coding: utf-8 -*-
import json
from redis import StrictRedis


def proxise():
    redisconn = StrictRedis(host='192.168.0.106', db=7, port=6379, password="1214")
    prox_ = json.loads(redisconn.get("ip"))['http']
    pro_ = {'http': prox_}
    return pro_
    # return {}
