# -*- coding: utf-8 -*-
import os,time

ls = os.listdir('../市级2')
ls = [i for i in ls if '.py' in i and '打不开' not in i and '验证码' not in i and '加密' not in i
      and '502' not in i and '登录' not in i and '不对' not in i and 'proxies' not in i and '中国政府采购网' not in i
      and '全国公共资源交易平台' not in i]
while True:
    num = 1
    print(len(ls))
    for i in ls[50:60]:
        print(num, i)
        os.system('python ../市级2/'+i)
        num +=1
    date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    print('等待下一次运行...', date)
    time.sleep(1800)





