"""
author: Grey
selenium 获取长截图 转换二进制
"""
import re
import time
from selenium import webdriver


def selemium_screenshot(url):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--dns-prefetch-disable')
    options.add_argument('--no-referrers')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-audio')
    options.add_argument('--no-sandbox')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--allow-insecure-localhost')
    options.add_argument("--window-size=1440,1024")
    options.add_argument("--hide-scrollbars")
    # driver = webdriver.Chrome(options=options)
    driver =webdriver.Chrome('chromedriver')
    driver.get(url)
    # width = driver.execute_script(  # screen wight
    #     "return Math.max(document.body.scrollWidth, document.body.offsetWidth, document.documentElement.clientWidth, "
    #     "document.documentElement.scrollWidth, document.documentElement.offsetWidth)")
    # height = driver.execute_script(  # screen height
    #     "return Math.max(document.body.scrollHeight, document.body.offsetHeight, "
    #     "document.documentElement.clientHeight, document.documentElement.scrollHeight, "
    #     "document.documentElement.offsetHeight)")
    # if width > height:
    #     width = height
    driver.maximize_window()
    # driver.set_window_size() #set_size
    pathname = re.findall(r"https?://.*\.(\w+)\..*/", url)#sitename use pic_name
    picpath=f'{pathname}.png'
    driver.find_element('xpath',"//input[@class='c-input op_trust_pername']").send_keys("武文刚")
    time.sleep(5)
    driver.find_element('xpath',"//button[@class='c-btn c-btn-primary op_trust_btnSearch']").click()

    time.sleep(3)
    ss=driver.find_elements('xpath',"//div[@class='op_trust_reperson']//li")
    for s in ss:
        print(s.text)
        # print(s.find_elements('xpath',"//div[@class='op_trust_info']"))
    # driver.save_screenshot(picpath)#screenshot and savepath
    # driver.get_screenshot_as_file(picpath)
    # print(driver.get_screenshot_as_png())#binary
    print(picpath,"all ready")
    # driver.quit()


if __name__ == '__main__':
    url = 'https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=1&tn=baidu&wd=%E5%A4%B1%E4%BF%A1%E4%BA%BA%E5%90%8D%E5%8D%95&oq=%25E5%25A4%25B1%25E4%25BF%25A1%25E4%25BA%25BA%25E5%2590%258D%25E5%258D%2595&rsv_pq=bdbbfeda0004e482&rsv_t=3e62Dentwa4s65LjguEHSRWvu2VCC1%2FwtnQDM4ISgEWl%2BTp%2F2dSkL8SKzN8&rqlang=cn&rsv_enter=0&rsv_dl=tb&rsv_btype=t&rsv_sug3=15&rsv_sug1=14&rsv_sug7=100&rsv_sug4=574'


    selemium_screenshot(url)