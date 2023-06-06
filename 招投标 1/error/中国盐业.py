# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# 玉林市公共资源交易中心
class wenshan_ggzy:
    def __init__(self):
        self.domain_name = ' https://zyhsf.youzhicai.com'
        self.url_list = [
        ]
        self.headers = {

        'X-CSRF-TOKEN': 'D0gpYmN3YMxEuy6CUZfchm9P6NVnjY9sxqcREATr',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        # 'Cookie': 'Hm_lvt_9511d505b6dfa0c133ef4f9b744a16da=1670490580; __root_domain_v=.youzhicai.com; _qddaz=QD.328070490722309; Hm_lpvt_9511d505b6dfa0c133ef4f9b744a16da=1670549209; XSRF-TOKEN=eyJpdiI6IjI2UXk1NEQ5dkgxTHNkSGs5NDlsUHc9PSIsInZhbHVlIjoiSXgwSGxsc1E3STM4UzhFSHA3ZW95UmRNY3IybWVPQmc2VjloNnBSVThwbUZcL2ZlK2JPWlRGcGxsMXI0WmlcL2lGcFVTWlI0QzZzVlRJNnRpYXdRelNzUT09IiwibWFjIjoiMTU2MjQ2NDZhYWNjMWY1OWEwOTVkMGFlMDUzMmJkNWRkZTk2ODFkNTI1MWY0ODk0ODA4ZmZkZTQxMTE3MjA0YiJ9; laravel_session=eyJpdiI6IjVUYmNCQURscWVINXlJXC9oUW03bzhBPT0iLCJ2YWx1ZSI6ImRnMUJUXC9vUnJFYUFqczR3NFFjXC9PbHBVaGN6Tk1XZEh5aTVcL09kSW5jbTBzVnNHTkt5djBYekR4ajE2RnJUdjA3NnRIcFZVbENvdU9EdVwvaGMzUVNwUT09IiwibWFjIjoiZjY2ZWIzOTk5NTk5MWNmODUzZTk4MTE1MjVjYTIzYjM1ZTgxNzg1Nzk2Y2JjNDcwOTRiNmE0YmJjYmY0YmFkZCJ9'
        # 'Cookie': '__root_domain_v=.youzhicai.com; _qddaz=QD.328070490722309; Hm_lvt_9511d505b6dfa0c133ef4f9b744a16da=1675414433; Hm_lpvt_9511d505b6dfa0c133ef4f9b744a16da=1675414433; XSRF-TOKEN=eyJpdiI6IkZMaVprVVZ1b01jZENmS08xZG5YOWc9PSIsInZhbHVlIjoiUHFxOFQ3WnlcL2J6NExDbml6RStURk5CNnRSczN2alZ3XC90bmNrd3JVQU5kNmxUanJCamJIUUxPZTgrSUdPclZha0pCNHpaNSsxWGh6Z3k1QkNNK3pFUT09IiwibWFjIjoiOTY4Y2I1MDYwMTJjODRhNzJhYTEzYzg2YmM5MWMwZjI0ZWQzYWMzNDM0YTI2NGY0NTMyNmQzYTg4ZmU1M2Q4MyJ9; laravel_session=eyJpdiI6IjFTcE95RU5BQldWNUJhd1lKTG5Nd0E9PSIsInZhbHVlIjoiMjYxWFg1TnRzMFUxOFFHaUR6d1RIcmdtSEIwSXBqXC9uUk1BXC9OOUpuMnFcLzdXUnRNRGt0RE9EUlltd284TURcL1M2dTVOUEFUdlU0SlIwOTVZcEtldWJ3PT0iLCJtYWMiOiI4YzkyNDcwMWViOTQ2NjUzOTZlZTcyMWI0NGQ4YmY2NzFkYWFmMTA4MDViZGI0OGZlNTU5YWU1ZDdmMDg2NThjIn0%3D'
        'cookie': 'laravel_session=eyJpdiI6ImN2VEtlUk12XC9paXhQUzJQYmFoSEZ3PT0iLCJ2YWx1ZSI6IlNOZ2dFQ0E1c0hiR0NvMWhvUUtkNVZSU2hJaSt0SHh5c0I4NDVmenNGZHkxTUdWeEc4OHBDdHNXYWg4MXBLV0x1dzNaUElJeTBzM1c5Tnp5OFVmZ1NRPT0iLCJtYWMiOiI1ZTljYWQ5NWY3YTg2ZTc1YjEzZWJkMmNhOTVhM2RjZTI2N2Y4N2M2OGYzZGFmMzFjY2ZmMWQ4ZDcwYTFhN2EzIn0%3D'

        }

    def parse(self):
        date = tool.date
        # date = '2020-09-27'
        page = 0
        while True:
            page += 1
            url=f'https://zyhsf.youzhicai.com/newtopic/data-list'
            data={

                'pageIndex': page,
                'id': '8312F123-CC36-F700-91DA-D7E911B8EB3D',
                'type': 1,
                'companyId':'',
                'title': '',
                'ntype': '',
                'start_time': '',
                'end_time': '',
                'child': ''


            }
            text = requests.session().post(url ,params=data, headers=self.headers).content.decode('utf-8-sig')
            print('*' * 20, page, '*' * 20)
            print(11, text)
            detail = json.loads(text)['list']
            print(detail)
            # time.sleep(6666)
            for li in detail:
                title = li['noticeTitle']
                # id= li['id']
                url = li['Url']
                city=li['city']
                date_Today = li['createTime']
                if 'http' not in url:
                    url = 'https:' + url
                # time.sleep(666)
                endtime=re.findall(r'\d{4}-\d{2}-\d{2}', li['endTime'])[0]
                date_Today = re.findall(r'\d{4}-\d{2}-\d{2}', date_Today)[0]
                print(title, url, date_Today)
                if tool.Transformation(date) <= tool.Transformation(date_Today):
                    if tool.removal(title, date):
                        self.parse_detile(title, url, date_Today,endtime,city)
                    else:
                        print('【existence】', url)
                        continue
                else:
                    print('日期不符, 正在切换类型', date_Today, self.url)
                    self.url = self.url_list.pop(0)
                    page = 0
                    break
            if page == 20:
                self.url = self.url_list.pop(0)
                page = 0

    def parse_detile(self, title, url, date,endtime,city):
        print(url)
        url_text = tool.requests_get(url, self.headers)
        print(url_text)
        time.sleep(666)
        url_html = etree.HTML(url_text)
        detail = url_html.xpath("//div[@class='tabBox']/div[@class='tabContent']")
        # print(url_text)
        detail_html = etree.tostring(detail, method='HTML')
        detail_html = html.unescape(detail_html.decode())
        detail_text = detail_html
        # .replace('\xa0', '').replace('\n','').replace('\r', '').replace('\t','').replace(' ', '').replace('\xa5', '')
        item = {}
        item['title'] = title.replace('\u2022', '')
        item['url'] = url
        item['date'] = date
        item['typeid'] = tool.get_typeid(item['title'])
        item['senddate'] = int(time.time())
        item['mid'] = 867
        item['address'] = tool.get_address(detail_text)
        item['nativeplace'] = float(tool.get_title_city(city))
        item['infotype'] = tool.get_infotype(item['title'])
        item['body'] = tool.qudiao_width(detail_html)
        item['endtime'] = tool.get_endtime(detail_text)
        if item['endtime'] == '':
            item['endtime'] = int(time.mktime(time.strptime(endtime, "%Y-%m-%d")))
        else:
            try:
                item['endtime'] = int(time.mktime(time.strptime(item['endtime'], "%Y-%m-%d")))
            except:
                item['endtime'] = int(time.mktime(time.strptime(endtime, "%Y-%m-%d")))
        item['tel'] = tool.get_tel(detail_text)
        item['email'] = ''
        item['linkman'] = tool.get_linkman(detail_text)
        item['function'] = tool.get_function(detail_text)
        item['resource'] = '中国盐业'
        item["shi"] = int(item["nativeplace"])
        if len(str(item["nativeplace"])) == 4:
            item['sheng'] = int(str(item["nativeplace"])[:2] + '00')
        elif len(str(item["nativeplace"])) == 5:
            item['sheng'] = int(str(item["nativeplace"])[:3] + '00')
        else:
            item['sheng'] = 0
        item['removal'] = title
        # process_item(item)
        # print(item["nativeplace"],item['address'],item['sheng'],item["shi"])
        # print(item)
        # process_item(item)
        print(item)


if __name__ == '__main__':
    import traceback,os
    try:
        jl = wenshan_ggzy()
        jl.parse()
    except Exception as e:
        traceback.print_exc()
        tool.send_error('报错文件：'+str(os.path.basename(__file__))+'报错信息：'+str(e))


