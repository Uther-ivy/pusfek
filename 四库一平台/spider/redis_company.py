import redis
import pymysql
# conn = pymysql.connect(host='47.92.73.25', user='duxie', password='jtkpwangluo.com', db='yqc')
class RedisDeduplication:
    def __init__(self, host='47.92.73.25', port=6379, db=11,password='jtkp0987654321'):
        self.redis = redis.Redis(host=host, port=port, db=db,password=password)

    def add(self, key, value):
        """
        添加一条记录
        :param key: 企业类型
        :param value: 企业名称
        :return: True表示添加成功，False表示已存在
        """
        return self.redis.sadd(key, value)

    def remove(self, key, *values):
        """
        从set中删除元素
        :param key: set的名称
        :param values: 要删除的元素
        :return: 删除成功的元素数量
        """
        return self.redis.srem(key, *values)
    def exists(self, key, value):
        """
        判断一条记录是否存在
        :param key: 企业类型
        :param value: 企业名称
        :return: True表示已存在，False表示不存在
        """
        return self.redis.sismember(key, value)

    def get_one(self, key):
        """
        获取一条记录
        :param key: 企业类型
        :return: 企业名称
        """
        return self.redis.srandmember(key)
def xingyong():#获取一个待采集企业
    dedup = RedisDeduplication()
    return dedup.get_one('type2').decode('utf-8')
def xingyong_over(qymc):#采集企业结束
    dedup = RedisDeduplication()
    dedup.add('type3', qymc)
    return dedup.remove('type2', qymc)
def company_four():#获取一个未采集的四库名称
    dedup = RedisDeduplication()
    return dedup.get_one('new_company_name').decode('utf-8')

def company_four_over(qymc):#采集四库信息结束
    dedup = RedisDeduplication()
    dedup.add('type2',qymc)
    return dedup.remove('new_company_name',qymc)

if __name__ == '__main__':
    dedup = RedisDeduplication()
    print(dedup.__sizeof__())
    # mycursor = conn.cursor()
    # query = "SELECT qymc FROM yunqi_addon17 order by aid limit 10"
    # mycursor.execute(query)
    # results = mycursor.fetchall()
    # company_list = results
    # mycursor.close()
    # conn.close()
    # for company in company_list:
    #     dedup.add('type1',company[0])

    # 获取一条记录

