# -*- coding:utf-8 -*-
import requests


class Bkjw:
    """
        这个是Bkjw的类负责底层操作
    """

    def __init__(self):
        self.session = requests.session()

    # 要提交的键值对的一个结构
    # 表单要提交到的目的地址
    keywords = {"username": "1500220519", "passwd": "709196484", 'login': '%B5%C7%A1%A1%C2%BC'}
    url = "http://172.16.64.236/student/public/login.asp"

    def login(self, url, keywords):

        # 以post的方式提交表单并保存结果在变量res中
        res = self.session.post(url, data=keywords)

        print(res.reason)
        # print(res.headers)

        res = self.session.get('http://172.16.64.236/student/Info.asp')
        # print(res.headers)

        if res.text.find('1500220519') > 0:
            print('OK')
        else:
            print("Session Create Error!")

    def logout(self):
        self.session.get('http://bkjw.guet.edu.cn/student/public/logout.asp')
        self.session.close()


def connect_test():
    request_header = {}

    res = requests.get("http://www.baidu.com")
    print(res.reason)
    print(res.headers)


def main():
    print("hello world\n")
    # connect_test()

    bkjw = Bkjw()
    bkjw.login(bkjw.url, bkjw.keywords)


if __name__ == '__main__':
    main()

