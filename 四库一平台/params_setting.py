
def get_params():
    params = [0, 225000 ]
    for param in params:
        # print([param, 10, 2500])
        yield [param, 5, 2] #params[0]开始数  params[1] 迭代次数 params[2]增加个数
