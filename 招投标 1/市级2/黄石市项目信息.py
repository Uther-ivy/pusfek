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

def get_nativeplace(place):
    city = ''
    citys = [['9000','湖北省'],['9001','武汉市'],['9001.001','江岸区'],['9001.01','蔡甸区'],['9001.011','江夏区'],['9001.012','黄陂区'],['9001.013','新洲区'],['9001.002','江汉区'],['9001.003','乔口区'],['9001.004','汉阳区'],['9001.005','武昌区'],['9001.006','青山区'],['9001.007','洪山区'],['9001.008','东西湖区'],['9001.009','汉南区'],['9002','黄石市']  ,['9002.001','黄石港区'],['9002.002','西塞山区'],['9002.003','下陆区'],['9002.004','铁山区'],['9002.005','阳新县'],['9002.006','大冶市'],['9003','十堰市'],['9003.001','茅箭区'],['9003.002','张湾区'],['9003.003','郧　县'],['9003.004','郧西县'],['9003.005','竹山县'],['9003.006','竹溪县'],['9003.007','房　县'],['9003.008','丹江口市'],['9004','宜昌市'],['9004.001','西陵区'],['9004.01','五峰土家族自治县'],['9004.011','宜都市'],['9004.012','当阳市'],['9004.013','枝江市'],['9004.002','伍家岗区'],['9004.003','点军区'],['9004.004','?亭区'],['9004.005','夷陵区'],['9004.006','远安县'],['9004.007','兴山县'],['9004.008','秭归县'],['9004.009','长阳土家族自治县'],['9005','襄樊市'],['9005.001','襄城区'],['9005.002','樊城区'],['9005.003','襄阳区'],['9005.004','南漳县'],['9005.005','谷城县'],['9005.006','保康县'],['9005.007','老河口市'],['9005.008','枣阳市'],['9005.009','宜城市'],['9006','鄂州市'],['9006.001','梁子湖区'],['9006.002','华容区'],['9006.003','鄂城区'],['9007','荆门市'],['9007.001','钟祥市'],['9007.002','沙洋县'],['9007.003','京山县'],['9007.004','掇刀区'],['9007.005','东宝区'],['9008','孝感市'],['9008.001','安陆市'],['9008.002','应城市'],['9008.003','云梦县'],['9008.004','大悟县'],['9008.005','孝昌县'],['9008.006','孝南区'],['9008.007','汉川市'],['9009','荆州市'],['9009.001','沙市区'],['9009.002','荆州区'],['9009.003','公安县'],['9009.004','监利县'],['9009.005','江陵县'],['9009.006','石首市'],['9009.007','洪湖市'],['9009.008','松滋市'],['9010','黄冈市'],['9010.001','州区'],['9010.01','武穴市'],['9010.002','团风县'],['9010.003','红安县'],['9010.004','罗田县'],['9010.005','英山县'],['9010.006','浠水县'],['9010.007','蕲春县'],['9010.008','黄梅县'],['9010.009','麻城市'],['9011','咸宁市'],['9011.001','咸安区'],['9011.002','嘉鱼县'],['9011.003','通城县'],['9011.004','崇阳县'],['9011.005','通山县'],['9011.006','赤壁市'],['9012','随州市'],['9012.001','曾都区'],['9012.002','广水市'],['9013','恩施土家族苗族自治州'],['9013.001','恩施市'],['9013.002','利川市'],['9013.003','建始县'],['9013.004','巴东县'],['9013.005','宣恩县'],['9013.006','咸丰县'],['9013.007','来凤县'],['9013.008','鹤峰县'],['9014','省直辖行政单位'],['9014.001','仙桃市'],['9014.002','潜江市'],['9014.003','天门市'],['9014.004','神农架林区']]
    for i in citys:
        if i[1] in place:
            city = float(i[0])
            break
    if city == '':
        city = 9002
    return city

def get_zhaobiaoinfo(info_url,title,zhao_time):
    print(info_url)
    resp = requests.get(info_url, headers=headers,verify=False, proxies=pro,timeout=20)
    resp.encoding = "UTF-8"
    sel = Selector(resp)
    item = {}
    item['zhao_time'] = zhao_time
    item['title'] = title
    item['info_url'] = info_url
    try:
        item['body'] = sel.xpath('//div[@id="gcjs"]').extract_first().replace("display: none","")
    except:
        item['body'] = sel.xpath('//div[@id="zfcg"]').extract_first().replace("display: none","")
    item['detail'] = item['body'].replace('\n', '').replace("\t", '').replace("\r", '').replace('\xa0', '').replace('\xc2', '').replace(' ', '')
    item['senddate'] = int(time.time())
    item['mid'] = 1403
    item['typeid'] = tool.get_typeid(title)
    list = re.findall('width="(.*?)"', item['body'])
    for i in list:
        item['body'] = item['body'].replace('width="{}"'.format(i), '')
    item['endtime'] = tool.get_endtime(item['detail'])
    if item['endtime'] == '':
        item['endtime'] = int(time.mktime(time.strptime(zhao_time, "%Y-%m-%d")))
    else:
        try:
            item['endtime'] = int(time.mktime(time.strptime(item['endtime'], "%Y-%m-%d")))
        except:
            item['endtime'] = int(time.mktime(time.strptime(zhao_time, "%Y-%m-%d")))
    item['nativeplace'] = get_nativeplace(title + item['detail'])
    item['infotype'] = tool.get_infotype(title)
    item['shi'] = int(item['nativeplace'])  # 4502
    item['sheng'] = 9000
    item['email'] = ''
    item['tel'] = tool.get_tel(item['detail'])
    item['address'] = tool.get_address(item['detail'])
    item['linkman'] = tool.get_linkman(item['detail'])
    item['function'] = tool.get_function(item['detail'])  # detail["projectBudget"]
    item['click'] = random.randint(500, 1000)
    item['resource'] = "黄石市公共资源交易网"
    save_db(item)

def get_project(url):
    data = {'page': '1'}
    resp = requests.post(url,data=data,proxies=pro,verify=False,timeout=20)
    results = json.loads(resp.text)
    project_info = results['rows']
    for pro_info in project_info:
        now_time = tool.date
        # now_time = '2021-07-27'
        zhao_time = pro_info['publishTime'].split(" ")[0]
        if tool.Transformation(now_time) <= tool.Transformation(zhao_time):
            if '9005001001' in url:
                info_url = "https://www.hsztbzx.com/front/project/list/9005001001/detail?id=" + pro_info['id']
            else:
                info_url = "https://www.hsztbzx.com/front/project/list/9005002007/detail?id=" + pro_info['id']
            try:
                title = pro_info['bidSectionName'].replace(' ','')
            except:
                title = pro_info['projectName'].replace(' ','')
            get_zhaobiaoinfo(info_url,title,zhao_time)
        else:
            print('日期不符', zhao_time)
            break


if __name__ == '__main__':
    url_ls = [
        "https://www.hsztbzx.com/front/project/list/9005001001/list",
        'https://www.hsztbzx.com/front/project/list/9005002007/list'
    ]
    requests.adapters.DEFAULT_RETRIES = 5  # 增加重连次数
    s = requests.session()
    s.keep_alive = False  # 关闭多余连接
    requests.packages.urllib3.disable_warnings()
    for i in url_ls:
        get_project(i)
