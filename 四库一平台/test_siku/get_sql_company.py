import time

import pymysql
import xlwt

db = pymysql.connect(
        # host='localhost',
        # port=3306,
        # user='root',
        # password='root',
        # database='uther_test',
        # charset='utf8',
    host='47.92.73.25',
    user='python',
    passwd='Kp123...',
    db='yqc',
    port=3306,
    charset="utf8"
    )



def get_sql_company(data):
    cur = db.cursor()
    sql = "select qymc,addtime,phone,xxdz,nativeplace from yunqi_addon17 where (nativeplace='{}')".format(data)
    cur.execute(sql)
    data = cur.fetchall()
    cur.close()
    db.close()
    return data

def save_xls(datalist):
    book = xlwt.Workbook(encoding="utf-8", style_compression=0)
    sheet = book.add_sheet('河北库里数据', cell_overwrite_ok=True)
    caption = ['公司名称', '电话', '地址', '省市代码']

    for i in range(0, len(caption)):
        sheet.write(0, i, caption[i])
    for i in range(len(datalist)):
        data = datalist[i]
        print(data)
        for j in range(0, len(caption)):
            sheet.write(i + 1, j, data[j])  # 写入一行数据
        book.save('./河北库里数据.xls')  # 保存

if __name__ == '__main__':
    datalist = get_sql_company('0')
    # save_xls(datalist)
    for data in datalist:
        # if '浙江'  not in data[3]:
        # with open('./companyname/errorname2.txt','w',encoding='utf-8'):


        print(data)