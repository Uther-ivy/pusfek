# -*- coding: utf-8 -*-
import json
import re
import time, html
import requests
from lxml import etree
from lxml.etree import HTML
import tool
from save_database import process_item

# a = 'https://book.qidian.com/info/1028874269'
#
# r = HTML(tool.requests_get(a, {})).xpath('//*[@id="j-catalogWrap"]/div[2]/div/ul/li')
#
# for i in r[54:]:
#     title = i.xpath('./a/text()')[0]
#     url = 'https:' + i.xpath('./a/@href')[0]
#     print(title, url)
#     con = HTML(tool.requests_get(url, '')).xpath('//*[@class="read-content j_readContent"]//text()')
#     [print(j) for j in con]
#     break



a = 'https://b.faloo.com/986354.html'

r = HTML(tool.requests_get(a, {})).xpath('//*[@class="DivTable"]/div')

for i in r[4:]:
    for j in i.xpath('./div')[1:]:
        title = j.xpath('./a/text()')[0]
        url = 'https:' + j.xpath('./a/@href')[0]
        print(title, url)
        con = HTML(tool.requests_get(url, '')).xpath('//*[@id="center"]/div/div[5]//text()')
        [print(j) for j in con]
        break
    break




