import random
import threading
import time
from multiprocessing import Process


def worker(a):
    print(threading.current_thread().name, 'Starting')

    while True:
        print('*'*20,f'process-{a}','*'*20)
        print(threading.current_thread().name, 'Exiting')

def work_process(a):
    threads = []
    print('threads','**'*30)
    for i in range(10000):
        t = threading.Thread(target=worker,args=(a,))
        threads.append(t)
        t.start()


if __name__ == '__main__':

    process=[]
    for a in range(10):
        p = Process(target=work_process,args=(a,))
        print(p.name)
        p.start()
        process.append(p)
    for pro in process:
        time.sleep(3 + random.random() * 5)
        pro.join()
        print('采集完成')

