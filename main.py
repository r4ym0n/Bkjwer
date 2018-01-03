# -*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup


class Bkjw:

    """
        这个是Bkjw的类负责底层操作
    """

    def __init__(self):
        self.session = requests.session()
        self.islogedin = False

    # 要提交的键值对的一个结构
    keywords = {"username": "1500110428", "passwd": "529160", 'login': '%B5%C7%A1%A1%C2%BC'}
    term = {"term": "2017-2018_1"}

    root_url = "http://172.16.64.236/"

    # 表单要提交到的子地址
    sub_url_tab = {
        "url": "http://172.16.64.236/",
        "url_login": "student/public/login.asp",
        "url_info": "student/Info.asp",
        "url_logout": "student/public/logout.asp",
        "url_courses": "student/Selected.asp",
    }

    def login(self, url, keywords):

        # 以post的方式提交表单并保存结果在变量res中
        res = self.session.post(url + self.sub_url_tab["url_login"], data=keywords)
        print(res.reason)

        res = self.session.get(url + self.sub_url_tab["url_info"])
        # 验证是否成功登陆
        if res.text.find(keywords["username"]) > 0:
            print('OK')
            self.islogedin = True
        else:
            print("Session Create Error!")

    def logout(self):
        self.session.get(self.sub_url_tab["url_logout"])
        self.session.close()

    def getinfo(self):
        #如果没有登陆就返回
        if not self.islogedin:
            return

        res = self.session.get(self.root_url + self.sub_url_tab["url_info"])
        # print(res.text)

        info_list = BeautifulSoup(res.content, 'html.parser').find_all('p')
        # print(info_list[0])
        # print(info_list[1])
        # 这里使用迭代器
        # for d in info_list:
        #     print(d)

        return info_list

    def getcourses(self, payload):
        if not self.islogedin:
            return

        res = self.session.post(self.root_url + self.sub_url_tab["url_courses"], data=payload)
        # print(res.text)
        # raw_tab = BeautifulSoup(res.content, 'html.parser').find_all('tr')
        # courses_list = BeautifulSoup(raw_tab.source, 'html.parser').find_all('td')
        # for d in courses_list:
        #     print(d)

        # res = self.session.get("http://172.16.64.236/student/Selected.asp")
        # print(res.text)

    def listout(self, infoset):
        for d in infoset:
            print(d)


def connect_test():
    request_header = {}

    res = requests.get("http://www.baidu.com")
    print(res.reason)
    print(res.headers)


def main():
    print("hello world\n")
    # connect_test()

    bkjw = Bkjw()
    bkjw.login(bkjw.root_url, bkjw.keywords)
    bkjw.listout(bkjw.getinfo())
    bkjw.getcourses(bkjw.term)


if __name__ == '__main__':
    main()

