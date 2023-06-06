# coding=utf-8
import random

import threading
from dbutils.pooled_db import PooledDB
from dbutils.persistent_db import PersistentDB

import time
import pymysql

from configuration.config import system_logger, db_config


class MysqlHelper(object):
    def __init__(self, db_config):
        self.__pool = PooledDB(creator=pymysql,
                               mincached=1,
                               maxcached=5,
                               maxshared=5,
                               maxconnections=5,
                               maxusage=5,
                               blocking=True,
                               user=db_config.get('user'),
                               passwd=db_config.get('password'),
                               db=db_config.get('database'),
                               host=db_config.get('host'),
                               port=db_config.get('port'),
                               charset=db_config.get('charset'),
                               )

    def getConn(self):
        conn = self.__pool.connection()  # 从连接池获取一个链接
        cursor = conn.cursor()
        return conn, cursor


    @staticmethod
    def dispose(cursor, conn):
        cursor.close()
        conn.close()

    def getOne(self, sql):

        conn, cursor = self.getConn()

        th_name = threading.currentThread().getName()
        # print(f'{th_name} {self.conn} {self.cursor} {time.time():.4f} start {sql}')
        cursor.execute(sql)
        rows = cursor.fetchall()
        print(f"{th_name} {conn} {cursor} {time.time():.4f} {rows}")
        # self.dispose()
        self.dispose(cursor, conn)
        return rows

    def queryOne(self, sql):
        system_logger.info("----------------------sql start ----------------------")
        system_logger.info(sql)
        try:
            conn, cursor = self.getConn()
            result = cursor.execute(sql)
            # rows = cursor.fetchall()
            json_data = self.sql_fetch_json(cursor)
            # 将连接返回
            self.dispose(cursor, conn)
            system_logger.info(f"-----------------------queryByKey result:{result} " + str(json_data))
            if len(json_data) == 1:
                return json_data[0]
            return None

        except Exception as e:
            system_logger.info("-----------predict exception line: " + str(e.__traceback__.tb_lineno) + " of " +
                               e.__traceback__.tb_frame.f_globals["__file__"])
            system_logger.info(e)
            return None

    @staticmethod
    def sql_fetch_json(cursor: pymysql.cursors.Cursor):
        """ Convert the pymysql SELECT result to json format """
        keys = []
        for column in cursor.description:
            keys.append(column[0])
        key_number = len(keys)

        json_data = []
        for row in cursor.fetchall():
            item = dict()
            for q in range(key_number):
                item[keys[q]] = row[q]
            json_data.append(item)
        return json_data


def test1(pool):
    phone_no = f"1390709000{random.randint(6,7)}"
    strsql = f"select * from zy_phone where policy_holder_phone_no={phone_no} order by insure_date " \
             + "desc, kafka_etl_time asc limit 1 "

    while True:
        time.sleep(1)
        pool.getOne(strsql)
        # time.sleep(0.001)
        j = 0
        th_name = threading.currentThread().getName()
        # if th_name in ['Thread-2','Thread-5']:
        #     # print(f"task {th_name}")
        #     time.sleep(0.003)


def main(pool):
    # pool.getConn()
    ths = []
    for i in range(5):
        th = threading.Thread(target=test1, args=(pool,))
        ths.append(th)
    for th in ths:
        th.start()

    for th in ths:
        th.join()


if __name__ == "__main__":
    mysqlhelper = MysqlHelper(db_config)
    main(mysqlhelper)
    time.sleep(3)
    while True:
        time.sleep(1)
