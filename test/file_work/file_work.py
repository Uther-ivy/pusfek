


def read_file(files):
    with open(file=files, mode="r", encoding="utf-8") as r:
        datas = r.readlines()
    r.close()
    return datas


def wirte_file(files,data=None):
    with open(file=files, mode="a", encoding="utf-8") as w:
        if data == 1:
            w.close()
        else:
            w.write(str(data)+'\n')



if __name__ == '__main__':
    fil1='new_yunqi_addon17.csv'
    fil2='new_siku_id.csv'
    sss=read_file(fil1)
    # print(sss,type(sss))

    cnames=list(set(sss)-set(read_file(fil2)))
    print(cnames,len(cnames))
    # for cname
    #     cname=sss.pop(0)
    #     for name in read_file(fil2):
    #         if cname in name:
    #             print(cname,len(sss))
    #         else:
            #     print(cname,name)
    # print(sss)

