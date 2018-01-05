# -*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup
import re

TIMEOUT = 5

class Bkjw:
    """
    这个是Bkjw的类负责底层操作
    """
    def __init__(self):
        self.root_url = "http://172.16.64.236/"
        self.session = requests.session()
        self.std_info: Dict[str, str] = dict()
        self.islogedin = False
        self.NET_STATUES = False
        # 检测是否网络可达
        try:
            requests.get(self.root_url, timeout=TIMEOUT)
        except requests.exceptions.ConnectTimeout:
            print("[-] Network Unreachable")
            self.NET_STATUES = False
            return
        self.NET_STATUES = True

    # 要提交的键值对的一个结构
    # keywords = {"username": "1500110428", "passwd": "529160", 'login': '%B5%C7%A1%A1%C2%BC'}
    keywords = {"username": "1500220519", "passwd": "709196484", 'login': '%B5%C7%A1%A1%C2%BC'}
    # term = {"term": "2017-2018_1"}

    # 表单要提交到的子地址
    sub_url_tab = {
        "url_login": "student/public/login.asp",
        "url_info": "student/Info.asp",
        "url_logout": "student/public/logout.asp",
        "url_courses": "student/Selected.asp",
        "url_elva": "student/teachinpj.asp",
    }

    def login(self, keywords):
        """
        登陆方法
        :param url: bkjw的根路径
        :param keywords: 账号密码键值
        :return: BOOL 是否成功
        """
        if self.NET_STATUES is False:
            return

        # 以post的方式提交表单并保存结果在变量res中
        # print(self.root_url + self.sub_url_tab["url_login"])
        try:
            res = self.session.post(self.root_url + self.sub_url_tab["url_login"],
                                    data=keywords, json=None, timeout=TIMEOUT)
        # 这里对超时进行异常处理
        except requests.exceptions.ConnectTimeout:
            self.islogedin = False
            print('[-] Connect Timeout!')
            return False

        res = self.session.get(self.root_url + self.sub_url_tab["url_info"])
        # 验证是否成功登陆
        if res.text.find(keywords["username"]) > 0:
            print('[+] Logged in')
            print(self.session.cookies)
            self.islogedin = True
            return True
        else:
            print("[-] Login Error!")
            return False

    def logout(self):
        """
        登出方法
        :return: None
        """
        if not self.islogedin:
            return

        self.session.get(self.sub_url_tab["url_logout"])
        self.session.close()

    def get_info(self):
        """
        获取信息列表
        :return: set
        """
        # 如果没有登陆就返回
        if not self.islogedin:
            return

        res = self.session.get(self.root_url + self.sub_url_tab["url_info"])
        info_list = BeautifulSoup(res.content, 'html.parser').find_all('p')

        #从冒号开始分隔数据
        self.std_info['name'] = info_list[1].string.split(':')[1]
        self.std_info['class'] = info_list[2].string.split(':')[1]
        self.std_info['grade'] = info_list[3].string.split(':')[1]
        self.std_info['term'] = info_list[4].string.split(':')[1]

        return info_list

    def get_courses(self, term):
        """
        :param term:当前学期
        :return:已选课程SET
        """
        if not self.islogedin:
            return

        # 建立正则表达式
        check_regex = re.compile("\d+-\d+_[12]")
        if check_regex.match(term) is None:
            # raise 如 throw 抛个异常， 类型自己指定 如 ValueError
            raise ValueError('[-] 学期格式不正确，正确的示例：2017-2018_1，意为2017年到2018年上学期')

        # payload: Dict[str, str] = dict()
        # payload["term"] = term

        payload = {'term': term}

        res = self.session.post(self.root_url + self.sub_url_tab["url_courses"], data=payload)
        # print(res.text)
        # 这里是findall 之前写了find 只找了一个
        raw_tab = BeautifulSoup(res.content, 'html.parser').find_all('tr')

        th = raw_tab[0]         # 第一个就是表头
        data = raw_tab[1:-1]    # 后面的就是数据了 -1 是索引的最后一个

        selected_lesson_headers = list()
        selected_lesson_data = list()

        # get headers, and delete redundant characters from them.
        # 再次把标签分离并且替换\xa0 和 \u3000 两种空格符
        for h in th.find_all('th'):
            selected_lesson_headers.append(h.string.replace('\u3000', '').replace('\xa0', ''))

        tmp_data = list()
        for d in data:
            tmp_data.clear()
            for col in d.find_all("td"):
                tmp_data.append(col.string.encode().decode())
            selected_lesson_data.append(tmp_data.copy())

        return selected_lesson_headers, selected_lesson_data

    @staticmethod
    def list_out(info_set):
        """
        这里用于列出爬到的set
        """

        if info_set is not None:
            for d in info_set:
                print(d)
        else:
            print('[-] None Type !')
        
    def elva_teaching(self):
        """
            一键强制评教的实现
        """
        header, data = self.get_courses(self.std_info["term"])
        cno = list()
        cid = list()
        for d in data:
            cno.append(d[0])       # cno 课程序号
            cid.append(d[1])       # cid 课程代码

        # for course in course_list:
        #     payload[] = course.cid
        #     payload[] = course.cno
        # 默认全部好评的表单数据
        payload = "score1027=100&id=1027&qz=.02&score1028=100&id=1028&qz=.03&score1029=100&id=1029&" \
                  "qz=.12&score1030=100&id=1030&qz=.15&score1031=100&id=1031&qz=.15&score1032=100&id=1032" \
                  "&qz=.15&score1033=100&id=1033&qz=.05&score1034=100&id=1034&qz=.1&score1035=100&id=1035" \
                  "&qz=.05&score1036=100&id=1036&qz=.15&score1037=100&id=1037&qz=.02&score1038=100&id=1038" \
                  "&qz=.01&py=&pjlb=2&gx=i&tno=6357++++++++&lwBtntijiao=%CC%E1%BD%BB&"

        # 设置内容类型 重要
        self.session.headers["Content-Type"] = "application/x-www-form-urlencoded"
        for 
            res = self.session.post(self.root_url + self.sub_url_tab["url_elva"],
                                    data=(payload + "cno=%s&term=%s&cid=%s" % ("1711451", "2017-2018_1", "BT020006111")))
            page = BeautifulSoup(res.content, 'html.parser')
            if page.text.find("已提交") > 0:
                print("[*] OK")


def connect_test():
    request_header = {}

    res = requests.get("http://www.baidu.com")
    print(res.reason)
    print(res.headers)


def main():
    print("hello world")
    # connect_test()

    bkjw = Bkjw()
    if bkjw.login(bkjw.keywords):
        bkjw.get_info()
        print(bkjw.std_info["term"])
        # header, data = bkjw.get_courses(bkjw.std_info["term"])
        # bkjw.list_out(header)
        # bkjw.list_out(data)
        bkjw.elva_teaching()


if __name__ == '__main__':
    main()



