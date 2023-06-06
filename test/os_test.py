import sys
import time


def tesss():
    dad =int(time.time())
    while True:
        print('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
        print(dad)
        if int(time.time()) >= dad+5:
            print('sdasdadadas')
            sys.exit()



if __name__ == '__main__':
    tesss()

