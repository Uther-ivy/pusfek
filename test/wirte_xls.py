import xlwt


def wirte_xls():

    with open('../四库一平台/test_siku/companyname/河北二级.txt', 'r', encoding='utf-8') as r:
        datalist=r.readlines()

    print(datalist)
    # time.sleep(2222)
    book = xlwt.Workbook(encoding="utf-8", style_compression=0)
    sheet = book.add_sheet('河北二级数据', cell_overwrite_ok=True)
    caption = ['company', 'phone', 'email', 'address']
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


    book.save('./河北二级数据.xls')  # 保存
