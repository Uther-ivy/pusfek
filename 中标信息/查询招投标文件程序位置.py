# -*- coding: utf-8 -*-
import os,time

ls = os.listdir('市级2')
ls = [i for i in ls if '.py' in i and '打不开' not in i and '验证码' not in i and '加密' not in i
      and '502' not in i and '登录' not in i and '不对' not in i and 'proxies' not in i and '中国政府采购网' not in i
      and '中国海洋石油集团有限公司' not in i and '中国石化物资招标投标网' not in i and '中国电建设备物资集中采购平台' not in i
      and '中招联合招标采购网' not in i and '全国公共资源交易平台' not in i and '内蒙古公共资源网' not in i and
      '黑龙江政府采购网' not in i and '山西公共资源' not in i and '中国交建物资采购管理信息系统' not in i
      and '国家电网新一代电子商务平台' not in i and '江苏交通控股有限公司招标与采购网' not in i
      and '全军武器装备采购信息网' not in i and '中国铁建物资采购网' not in i
      and '河南省政府采购网' not in i and '辽宁省招标投标监管网' not in i
      and '中央政府采购网电子卖场' not in i and '宁夏政府采购网' not in i]
num = 1
print(len(ls))
for i in ls:
    if '河北省公共资源' in i:
        n = int(num / 20)
        print('程序名:', n, num, i)
        break
    num +=1
