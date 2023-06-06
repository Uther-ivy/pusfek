import redis
import pymysql
# 连接redis
r = redis.Redis(host='47.92.73.25', port=6379, db=11,password='jtkp0987654321')
conn = pymysql.connect(host='47.92.73.25', user='duxie', password='jtkpwangluo.com', db='yqc')
def creat():
    mycursor = conn.cursor()
    query="SELECT qymc FROM yunqi_addon17;"
    mycursor.execute(query)
    results = mycursor.fetchall()

    # 企业名、type类型、id列表
    company_list = results
    mycursor.close()
    conn.close()
    # 将企业名、type类型、id存入redis
    print(company_list)
    for company in company_list:
        r.rpush('company_list', f"{company[0]}_type0_skidf_")
def select():
    # 获取存储的企业名、type类型、id列表
    stored_company_list = r.lrange('company_list', 0, -1)

    # 打印存储的企业名、type类型、id列表
    for stored_company in stored_company_list:
        print(stored_company.decode())
def find():#刘超采集四库企业名称
    stored_company_list = r.lrange('company_list', 0, -1)
    for stored_company in stored_company_list:
        stored_company_str = stored_company.decode()
        if 'type0' in stored_company_str:
            print(stored_company_str)
            break
def find1():#少鹏查询企业名称
    stored_company_list = r.lrange('company_list', 0, -1)
    for stored_company in stored_company_list:
        stored_company_str = stored_company.decode()
        if 'type1' in stored_company_str:
            print(stored_company_str)
            break
def update1(qymc):#少鹏采集完变更状态
    stored_company_list = r.lrange('company_list', 0, -1)
    for i, stored_company in enumerate(stored_company_list):
        stored_company_str = stored_company.decode()
        if f"{qymc}" in stored_company_str:
            new_stored_company_str = stored_company_str.replace(f'type1', f'type2')
            r.lset('company_list', i, new_stored_company_str)
    # 打印修改后的企业名、type类型、id列表
    print("完成")
def update(qymc):#刘超采集完变更状态
    stored_company_list = r.lrange('company_list', 0, -1)
    for i, stored_company in enumerate(stored_company_list):
        stored_company_str = stored_company.decode()
        if f"{qymc}" in stored_company_str:
            new_stored_company_str = stored_company_str.replace(f'type0', f'type1')
            r.lset('company_list', i, new_stored_company_str)

    # 打印修改后的企业名、type类型、id列表
    print("完成")
if __name__ == '__main__':
    creat()
    # find()
    # update('陕西路远建设工程有限公司')

