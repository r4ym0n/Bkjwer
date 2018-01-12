import sys
import getpass
import time
import re
from terminaltables import DoubleTable

from bkjwer import Bkjw

exit_msg = "\n[++] Shutting down ... Goodbye. ( ^_^)／\n"


class Cmd0:

    def __init__(self):
        self.bkjw = Bkjw()
        self.user_name = getpass.getuser()

        self.log_statue = False     # 登陆状态
        curr_time = time.strftime('%H:%M:%S', time.localtime(time.time()))

        # print('\f')     # 翻新的一页

        print('\033[1;32m')
        print('*' * 50)
        print('*USR:\t', self.user_name)

        net_q = self.bkjw.net_quality
        if net_q > 0:
            if net_q == self.bkjw.attempt:
                net_rank = "Good"
            else:
                net_rank = "OK"
        else:
            net_rank = "Bad"

        print('*NET:\t', self.bkjw.net_quality, "\t", net_rank)
        print('*TIME:\t', curr_time)
        print('*' * 50)
        print('\033[1;m')
        print(self.dbg_info["dbg"] % "Please type 'help' to view commands.")

        return

    dbg_info = {"err": "\033[1;91m\n[!] %s \033[1;m",
                "info": "\033[1;32m\n[+] %s \n\033[1;m",
                "dbg": "\033[1;32m\n[*] %s \n\033[1;m"
    }

    def cmd_line(self):
        """
        交互命令
        :return:
        """
        cmd_0 = input("\033[1;36m\033[4m" + self.user_name + "\033[0m\033[1;36m ➮ \033[1;m").strip()
        if cmd_0 == "help":  # Map the network
            self.__help__()

        elif cmd_0 == "login":  # Login.
            self.__login__()

        elif cmd_0 == "exit":
            sys.exit(exit_msg)

        elif cmd_0 == "listC":  # list out selected.
            self.__listC__()

        elif cmd_0 == "elva":  # elva_teaching
            self.__elva_teaching__()

        elif cmd_0 == "logout":
            self.__logout__()

        elif cmd_0 == "who":
            self.__who__()

        elif cmd_0 == "term":
            self.__set_term__()

        else:
            print("\033[1;91m\n[!] Error : Command not found.\033[1;m")

    @staticmethod
    def __help__():
        print("")
        table_datas = [
            ["\033[1;36m\nMODULES\n", """
          login       :  user login
          logout      :  user logout
          who         :  show Current user
          tern        :  show and set Current term
          help        :  show this list
          listC       :  List selected courses
          exit        :  Exit Current Program
          \033[1;m"""]
        ]
        table = DoubleTable(table_datas)
        print(table.table)

    def __who__(self):
        if not self.__check_log_statue__():
            return
        print(self.bkjw.std_info["name"])
        print(self.bkjw.std_info["class"])
        print(self.bkjw.std_info["grade"])

    def __listC__(self):
        """
        列出当前所选所有课程
        :return:
        """
        if not self.__check_log_statue__():
            return

        header, data, tab = self.bkjw.get_courses(self.bkjw.std_info["term"])

        # table = DoubleTable("[" + tmp) 这里也想打印表，可是实在搞不来 求PR
        # print(table.table)
        # 投机取巧，以这种既不美好的方式结束战斗。。。
        print(str(tab).replace("], [", "\n").strip("[").strip("]"))

    def __elva_teaching__(self):
        if not self.__check_log_statue__():
            return
        self.bkjw.elva_teaching()       # 这里一键评教

    def __set_term__(self):
        if not self.__check_log_statue__():
            return
        print(self.dbg_info["dbg"] % "Current term:" + self.bkjw.std_info["term"])
        qus = input("\033[1;32m\n[*] %s\t\033[1;m" % "New Term? [y/n]:")

        if 'y' in qus or 'Y' in qus:
            n_term = input(self.dbg_info["dbg"] % "Set Term:\t")

            check_regex = re.compile("\d+-\d+_[12]")
            if check_regex.match(n_term) is None:
                print(self.dbg_info["err"] % '学期格式不正确，正确的示例：2017-2018_1，意为2017年到2018年上学期')
            else:
                self.bkjw.std_info["term"] = n_term
        else:
            pass

    def __login__(self):
        # 输密码
        if self.log_statue is True:
            print(self.dbg_info["err"] % "Already Logged in!")

        uname = input("\033[1;32m\n[*] Username:\t\033[1;m")
        passwd = input("\033[1;32m\n[*] Password:\t\033[1;m")

        if (len(uname) and len(passwd)) == 0:
            print(self.dbg_info["err"] % "Username or Password cannot be empty!")
            return
        self.bkjw.keywords["username"] = uname
        self.bkjw.keywords["passwd"] = passwd
        # print(self.bkjw.keywords)
        # bkjw 登陆，保存状态
        self.log_statue = self.bkjw.login(self.bkjw.keywords)
        if self.log_statue is True:
            self.bkjw.get_info()
            print(self.dbg_info["info"] % "Hello" + self.bkjw.std_info["name"])

    def __logout__(self):
        """
        登出
        :return:None
        """
        if not self.__check_log_statue__():
            return
        print(self.dbg_info["info"] % "bye~bye")
        self.bkjw.logout()
        self.log_statue = False

    def __check_log_statue__(self):
        """
        登陆状态检测
        :return: 返回 BOOL
        """
        if self.log_statue is False:
            print(self.dbg_info["err"] % "login First!")
            return False
        return True