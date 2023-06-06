import queue
import threading
import time

que = queue.Queue()
# que.maxsize = 100
def add_test():
    num=0
    while True:
        num += 1
        if que.qsize()<10:
            a= f'我是add{num}'
            time.sleep(0.1)
            que.put(a)
            print('size',que.qsize(),'name',num)
        else:
            time.sleep(2)




def get_test():
    while True:
        time.sleep(1)
        print(que.get())
        print(que.qsize())

if __name__ == '__main__':


    thr1=threading.Thread(target=add_test)
    thr2 = threading.Thread(target=get_test)
    thr1.start()
    thr2.start()
    thr1.join()
    thr2.join()
# if que.qsize()<10:
        #     break