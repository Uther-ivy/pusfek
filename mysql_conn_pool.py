import mysql.connector
import pymysql
from dbutils.pooled_db import PooledDB
from mysql.connector import pooling


class MySQLPool:
    __pool = None


    @staticmethod
    def get_pool():
        if MySQLPool.__pool is None:
            MySQLPool.create_pool()
        return MySQLPool.__pool

    @staticmethod
    def create_pool():
        try:
            print(1111111)
            MySQLPool.__pool = pooling.MySQLConnectionPool(pool_name="mypool",
                                                       pool_size=32,
                                                       pool_reset_session=True,
                                                       port=3306,
                                                       charset="utf8",
                                                       host='120.211.70.99',
                                                       database='new',
                                                       user='root',
                                                       password='zx1234')
        except:
            print("Error: {}")
            MySQLPool.create_pool()
    @staticmethod
    def close_connection(connection, cursor):
        cursor.close()
        connection.close()

    @staticmethod
    def execute_query(query, params=None, commit=False):
            try:
                connection = MySQLPool.get_pool().get_connection()
                print(1111111)
                if connection:
                    cursor = connection.cursor()
                    cursor.execute(query, params)
                    if commit:
                        connection.commit()
                    result = cursor.fetchall()
                    return result
            except:
                print("Error: {}")
            finally:
                MySQLPool.close_connection(connection, cursor)


if __name__ == '__main__':
    # 创建连接池
    # MySQLPool.create_pool()

    # 执行查询
    # result = MySQLPool.execute_query("SELECT * FROM siku_id")
    # print(result)
    # 执行带参数查询
    # result = MySQLPool.execute_query("SELECT * FROM siku_id WHERE skid=%s", ('002105291258793726',))
    # print(result)
    # 执行更新操作
    # MySQLPool.execute_query("INSERT INTO users (username, password) VALUES (%s, %s)", ("john", "password"), True)
    # 关闭连接池
    # MySQLPool.get_pool().close()
    # '这个连接池包含了创建连接池、获取连接、执行查询和更新操作、关闭连接的功能。它使用了mysql-connector的连接池模块，可以在多个线程中共享连接池中的连接。'



    def conn():
        db = PooledDB(
            creator=pymysql,
            blocking=True,
            maxconnections=50,
            maxshared=50,
            host='120.211.70.99',
            user='root',
            passwd='zx1234',
            db='new',
            port=3306,
            charset="utf8"
        )

        try:
            pooldb = db.connection()
            print('dasdasd')
            return pooldb
        except Exception as e:
            print(e)
            conn()





    conn()