# -*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup


class Bkjw:

    """
        这个是Bkjw的类负责底层操作
    """

    def __init__(self):
        self.session = requests.session()
        self.std_info: Dict[str, str] = dict()
        self.islogedin = False
        try:
            requests.get(self.root_url, timeout=1)
        except requests.exceptions.ConnectTimeout:
            print("[-] Network Unreachable")

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
        try:
            res = self.session.post(url + self.sub_url_tab["url_login"], data=keywords, json=None, timeout = 0.5)
        #  这里对超时进行异常处理
        except requests.exceptions.ConnectTimeout:
            self.islogedin = False
            print('[-] Connect Timeout!')
            return

        res = self.session.get(url + self.sub_url_tab["url_info"])
        # 验证是否成功登陆
        if res.text.find(keywords["username"]) > 0:
            print('[+] Logged in')
            self.islogedin = True
            return True
        else:
            print("Session Create Error!")
            return False

    def logout(self):
        if not self.islogedin:
            return

        self.session.get(self.sub_url_tab["url_logout"])
        self.session.close()

    def getinfo(self):
        #如果没有登陆就返回
        if not self.islogedin:
            return

        res = self.session.get(self.root_url + self.sub_url_tab["url_info"])
        # print(res.text)

        info_list = BeautifulSoup(res.content, 'html.parser').find_all('p')

        # 这里使用迭代器
        # for d in info_list:
        #     print(d)

        #从冒号开始分隔数据
        self.std_info['name'] = info_list[1].string.split(':')[1]
        self.std_info['class'] = info_list[2].string.split(':')[1]
        self.std_info['grade'] = info_list[3].string.split(':')[1]
        self.std_info['term'] = info_list[4].string.split(':')[1]

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

        res = self.session.get(self.root_url + self.sub_url_tab["url_courses"])
        print(res.text)

    def listout(self, info_set):
        """
            这里用于列出爬到的set
        """
        
        if info_set is not None:
            for d in info_set:
                print(d)
        else:
            print('[-] None Type !')


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
    bkjw.getinfo()
    print(bkjw.std_info["name"])
    bkjw.getcourses(bkjw.std_info["term"])


if __name__ == '__main__':
    main()



