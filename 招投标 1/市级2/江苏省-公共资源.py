# -*- coding: utf-8 -*-
import datetime
import json
import random
import re
import time
import pymysql
import requests
from redis import StrictRedis
from scrapy import Selector
import ssl
import tool
from save_database import save_db
from proxies import proxise
pro = proxise()

ssl._create_default_https_context = ssl._create_unverified_context
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
}

def get_nativeplace(addrstr):
    if "玄武" in addrstr:
        return 5501.001
    elif "江宁" in addrstr:
        return 5501.01
    elif "六合" in addrstr:
        return 5501.011
    elif "溧水" in addrstr:
        return 5501.012
    elif "高淳" in addrstr:
        return 5501.013
    # elif "白下" in addrstr:
    #     return 5501.002
    elif "秦淮" in addrstr:
        return 5501.003
    elif "建邺" in addrstr:
        return 5501.004
    elif "鼓楼" in addrstr:
        return 5501.005
    elif "下关" in addrstr:
        return 5501.006
    elif "浦口" in addrstr:
        return 5501.007
    elif "栖霞" in addrstr:
        return 5501.008
    elif "雨花台" in addrstr:
        return 5501.009
    elif "南京" in addrstr:
        return 5501
    elif "梁溪区" in addrstr:
        return 5502.001
    # elif "南长" in addrstr:
    #     return 5502.002
    # elif "北塘" in addrstr:
    #     return 5502.003
    elif "锡山" in addrstr:
        return 5502.004
    elif "惠山" in addrstr:
        return 5502.005
    elif "滨湖" in addrstr:
        return 5502.006
    elif "江阴" in addrstr:
        return 5502.007
    elif "宜兴" in addrstr:
        return 5502.008
    elif "无锡" in addrstr:
        return 5502
    elif "鼓楼" in addrstr:
        return 5503.001
    elif "新沂" in addrstr:
        return 5503.01
    elif "邳州" in addrstr:
        return 5503.011
    elif "云龙" in addrstr:
        return 5503.002
    # elif "九里" in addrstr:
    #     return 5503.003
    elif "贾汪" in addrstr:
        return 5503.004
    elif "泉山" in addrstr:
        return 5503.005
    elif "丰县" in addrstr:
        return 5503.006
    elif "沛县" in addrstr:
        return 5503.007
    elif "铜山" in addrstr:
        return 5503.008
    elif "睢宁" in addrstr:
        return 5503.009
    elif "徐州" in addrstr:
        return 5503
    elif "天宁" in addrstr:
        return 5504.001
    elif "钟楼" in addrstr:
        return 5504.002
    # elif "戚墅堰" in addrstr:
    #     return 5504.003
    elif "新北" in addrstr:
        return 5504.004
    elif "武进" in addrstr:
        return 5504.005
    elif "溧阳" in addrstr:
        return 5504.006
    elif "金坛" in addrstr:
        return 5504.007
    elif "常州" in addrstr:
        return 5504
    # elif "沧浪" in addrstr: # todo:姑苏
    #     return 5505.001
    elif "吴江" in addrstr:
        return 5505.01
    elif "太仓" in addrstr:
        return 5505.011
    # elif "平江" in addrstr:
    #     return 5505.001
    # elif "金阊" in addrstr:
    #     return 5505.001
    elif "虎丘" in addrstr:
        return 5505.004
    elif "吴中" in addrstr:
        return 5505.005
    elif "相城" in addrstr:
        return 5505.006
    elif "常熟" in addrstr:
        return 5505.007
    elif "张家港" in addrstr:
        return 5505.008
    elif "昆山" in addrstr:
        return 5505.009
    elif "苏州" in addrstr:
        return 5505
    elif "崇川" in addrstr:
        return 5506.001
    elif "港闸" in addrstr:
        return 5506.002
    elif "海安" in addrstr:
        return 5506.003
    elif "如东" in addrstr:
        return 5506.004
    elif "启东" in addrstr:
        return 5506.005
    elif "如皋" in addrstr:
        return 5506.006
    elif "通州" in addrstr:
        return 5506.007
    elif "海门" in addrstr:
        return 5506.008
    elif "南通" in addrstr:
        return 5506
    elif "连云" in addrstr:
        return 5507.001
    # elif "新浦" in addrstr:
    #     return 5507.002
    elif "海州" in addrstr:
        return 5507.003
    elif "赣榆" in addrstr:
        return 5507.004
    elif "东海" in addrstr:
        return 5507.005
    elif "灌云" in addrstr:
        return 5507.006
    elif "灌南" in addrstr:
        return 5507.007
    elif "连云港" in addrstr:
        return 5507
    # elif "清河" in addrstr: #todo:清江浦  淮安区
    #     return 5508.001
    # elif "楚州" in addrstr:
    #     return 5508.002
    elif "淮阴" in addrstr:
        return 5508.003
    # elif "清浦" in addrstr:
    #     return 5508.004
    elif "涟水" in addrstr:
        return 5508.005
    elif "洪泽" in addrstr:
        return 5508.006
    elif "盱眙" in addrstr:
        return 5508.007
    elif "金湖" in addrstr:
        return 5508.008
    elif "淮安" in addrstr:
        return 5508
    elif "亭湖" in addrstr:
        return 5509.001
    elif "盐都" in addrstr:
        return 5509.002
    elif "响水" in addrstr:
        return 5509.003
    elif "滨海" in addrstr:
        return 5509.004
    elif "阜宁" in addrstr:
        return 5509.005
    elif "射阳" in addrstr:
        return 5509.006
    elif "建湖" in addrstr:
        return 5509.007
    elif "东台" in addrstr:
        return 5509.008
    elif "大丰" in addrstr:
        return 5509.009
    elif "盐城" in addrstr:
        return 5509
    elif "广陵" in addrstr:
        return 5510.001
    elif "邗江" in addrstr:
        return 5510.002
    # elif "郊区" in addrstr:
    #     return 5510.003
    elif "宝应" in addrstr:
        return 5510.004
    elif "仪征" in addrstr:
        return 5510.005
    elif "高邮" in addrstr:
        return 5510.006
    elif "江都" in addrstr:
        return 5510.007
    elif "扬州" in addrstr:
        return 5510
    elif "京口" in addrstr:
        return 5511.001
    elif "润州" in addrstr:
        return 5511.002
    elif "丹徒" in addrstr:
        return 5511.003
    elif "丹阳" in addrstr:
        return 5511.004
    elif "扬中" in addrstr:
        return 5511.005
    elif "句容" in addrstr:
        return 5511.006
    elif "镇江" in addrstr:
        return 5511
    elif "海陵" in addrstr:
        return 5512.001
    elif "高港" in addrstr:
        return 5512.002
    elif "兴化" in addrstr:
        return 5512.003
    elif "靖江" in addrstr:
        return 5512.004
    elif "泰兴" in addrstr:
        return 5512.005
    elif "姜堰" in addrstr:
        return 5512.006
    elif "泰州" in addrstr:
        return 5512
    elif "宿城" in addrstr:
        return 5513.001
    elif "宿豫" in addrstr:
        return 5513.001
    elif "沭阳" in addrstr:
        return 5513.001
    elif "泗阳" in addrstr:
        return 5513.001
    elif "泗洪" in addrstr:
        return 5513.001
    elif "宿迁" in addrstr:
        return 5513.001
    else:
        return 5500

def get_zhaobiaoinfo(title,zhaotime,infourl):
    print(infourl)
    resp = tool.requests_(infourl, headers)
    resp.encoding = "utf-8"
    sel = Selector(resp)
    item = {}
    item['zhao_time'] = zhaotime
    item['title'] = title
    item['info_url'] = infourl
    item['body'] = sel.xpath('//div[@class="ewb-trade-right l"]').extract_first()
    try:
        item['detail'] = item['body'].replace('\n', '').replace("\t", '').replace("\r", '').replace('\xa0', '').replace('\xc2', '').replace(' ', '')
    except:
        return
    item['senddate'] = int(time.time())
    item['mid'] = 1403
    item['resource'] = '江苏省公共资源交易网'
    item['typeid'] = tool.get_typeid(item['title'])
    list = re.findall('width="(.*?)"', item['body'])
    for i in list:
        item['body'] = item['body'].replace('width="{}"'.format(i), '')
    item['endtime'] = tool.get_endtime(item['detail'])
    if item['endtime'] == '':
        item['endtime'] = int(time.mktime(time.strptime(item['zhao_time'], "%Y-%m-%d")))
    else:
        try:
            item['endtime'] = int(time.mktime(time.strptime(item['endtime'], "%Y-%m-%d")))
        except:
            item['endtime'] = int(time.mktime(time.strptime(item['zhao_time'], "%Y-%m-%d")))
    item['nativeplace'] = get_nativeplace(item['title'] + item['detail'])
    item['infotype'] = tool.get_infotype(item['title'])
    item['shi'] = int(item['nativeplace'])  # 4502
    item['sheng'] = 5500
    item['email'] = ''
    item['tel'] = tool.get_tel(item['detail'])
    item['address'] = tool.get_address(item['detail'])
    item['linkman'] = tool.get_linkman(item['detail'])
    item['function'] = tool.get_function(item['detail'])  # detail["projectBudget"]
    item['click'] = random.randint(500, 1000)
    save_db(item)

def get_project(url):
    start = (datetime.datetime.now() - datetime.timedelta(days=3)).strftime("%Y-%m-%d 00:00:00")
    end = time.strftime('%Y-%m-%d 23:59:59', time.localtime())
    for i in range(0,6):
        print("*"*50)
        data = {
            'cl': '200',
            'cnum': '001',  # 分类号
            'fields': 'title',
            'highlights': 'title',
            'isBusiness': '1',
            'noParticiple': '1',
            'pn': i*20,  # 起始行
            'rn': '20',  # 记录数
            "sort": '{"infodatepx":"0"}',
            'ssort': 'title',
            'time': '[{"fieldName": "infodatepx", "startTime": "' + start + '", "endTime": "' + end + '"}]'
        }
        resp = tool.requests_post_to(url, data, headers)
        date = json.loads(resp)
        date = date['result']['records']
        now_time = tool.date
        for da in date:
            title = da['title']
            zhaotime = da['infodateformat']
            infourl = "http://jsggzy.jszwfw.gov.cn" + da['linkurl']
            if zhaotime == now_time:
                # print(title,zhaotime,infourl)
                time.sleep(random.randint(1,3))
                get_zhaobiaoinfo(title,zhaotime,infourl)
            else:
                print('日期不符', now_time)

if __name__ == '__main__':

    import traceback, os
    try:
        url = 'http://jsggzy.jszwfw.gov.cn/inteligentsearch/rest/esinteligentsearch/getFullTextDataNew'
        requests.adapters.DEFAULT_RETRIES = 5  # 增加重连次数
        s = requests.session()
        s.keep_alive = False  # 关闭多余连接
        requests.packages.urllib3.disable_warnings()
        get_project(url)
    except Exception as e:
        traceback.print_exc()
