import xlwt


def wirte_xls():

    with open('companyname/企知道国企.txt', 'r', encoding='utf-8') as r:
        datalist=r.readlines()

    print(datalist)
    # time.sleep(2222)
    book = xlwt.Workbook(encoding="utf-8", style_compression=0)
    sheet = book.add_sheet('河北国企', cell_overwrite_ok=True)
    caption = ['企业名称', '组织机构代码', '有效期','企业法人','电话','地址','业务范围']
    print()
    for i in range(0, len(caption)):
        sheet.write(0, i, caption[i])
    print(len(datalist))
    for i in range(len(datalist)):
        print(type(datalist[i]),datalist[i])
        # time.sleep(2222)
        if '[' in datalist[i]:
            for j in range(len(caption)):
                print(i+1,j,eval(datalist[i])[j])
                sheet.write(i+1,j,eval(datalist[i])[j])  # 写入一行数据
        else:
            style = xlwt.easyxf('font: bold on')
            sheet.write(i + 1, 0, datalist[i], style)


    book.save('./企知道河北国企.xls')  # 保存
wirte_xls()
