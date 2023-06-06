import requests
import threading
import time
# 设置最大线程池数量
MAX_REQUESTS = 5
# 设置请求时间间隔，单位为秒
REQUEST_INTERVAL = 5
# 请求处理函数
def handle_request(url):
    # 处理请求逻辑
    response = requests.get(url)
    # 输出请求结果
    print(response.text)
# 线程池类
class ThreadPool:
    def __init__(self, max_threads):
        # 最大线程池数量
        self.max_threads = max_threads
        # 空闲线程池队列
        self.idle_threads = []
        # 初始化空闲线程池
        for i in range(max_threads):
            self.idle_threads.append(i)
    # 获取一个空闲线程
    def get_thread(self):
        if len(self.idle_threads) > 0:
            return self.idle_threads.pop()
        else:
            return None
    # 释放一个线程
    def release_thread(self, thread_id):
        self.idle_threads.append(thread_id)
# 请求控制器类
class RequestController:
    def __init__(self, thread_pool):
        # 线程池
        self.thread_pool = thread_pool
        # 请求队列
        self.request_queue = []
        # 计数器，记录已处理的请求数量
        self.counter = 0
    # 添加请求
    def add_request(self, request):
        self.request_queue.append(request)
    # 执行请求任务
    def run(self):
        while True:
            # 检查是否还有未处理的请求
            if len(self.request_queue) == 0:
                return
            # 检查空闲线程数量
            thread_id = self.thread_pool.get_thread()
            if thread_id is None:
                time.sleep(1)
                continue
            # 取出一个请求
            url = self.request_queue.pop(0)
            # 创建并启动一个新线程
            threading.Thread(target=self.execute_request,
                             args=(url, thread_id)).start()
            # 计数器加一
            self.counter += 1
    # 执行单个请求
    def execute_request(self, url, thread_id):
        # 处理请求逻辑
        handle_request(url)
        # 释放线程
        self.thread_pool.release_thread(thread_id)
        # 防止过度访问，暂停 REQUEST_INTERVAL 秒
        time.sleep(REQUEST_INTERVAL)

from concurrent.futures import ThreadPoolExecutor
import time
def task(n):
    print("Start task:", n)
    time.sleep(2)
    print("End task:", n)
    return n * n
if __name__ == "__main__":
    executor = ThreadPoolExecutor(max_workers=5)
    results = []
    for i in range(10):
        future = executor.submit(task, i)
        results.append(future)

    for future in results:
        result = future.result()
        print("Result:", result)


# 示例使用：
if __name__ == '__main__':
    # 创建线程池
    thread_pool = ThreadPool(MAX_REQUESTS)
    # 创建请求控制器
    request_controller = RequestController(thread_pool)
    # 添加请求
    request_controller.add_request('https://www.baidu.com')
    request_controller.add_request('https://www.taobao.com')
    request_controller.add_request('https://www.jd.com')
    request_controller.add_request('https://www.qq.com')
    # 开始执行请求任务
    request_controller.run()