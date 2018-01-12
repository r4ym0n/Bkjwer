import sys
import getpass
import time
from terminaltables import DoubleTable

from bkjwer import Bkjw

exit_msg = "\n[++] Shutting down ... Goodbye. ( ^_^)／\n"


class Cmd0:

    def __init__(self):
        self.bkjw = Bkjw()
        self.user_name = getpass.getuser()

        self.log_statue = False     # 登陆状态
        curr_time = time.strftime('%H:%M:%S', time.localtime(time.time()))

        print('\033[1;32m')
        print('*' * 50)
        print('*USR:\t', self.user_name)
        # print('*URI:\t', 'http://127.0.0.1')
        print('*TIME:\t', curr_time)
        print('*' * 50)
        print('\033[1;m')
        print(self.dbg_info["dbg"] % "Please type 'help' to view commands.")

        return

    dbg_info = {"err": "\033[1;91m\n[!] %s \033[1;m",
                "info": "\033[1;32m\n[+] %s \n\033[1;m",
                "dbg":"\033[1;32m\n[*] %s \n\033[1;m"
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

        else:
            print("\033[1;91m\n[!] Error : Command not found.\033[1;m")

    def __listC__(self):
        if self.log_statue is False:
            print(self.dbg_info["err"] % "login First!")
        header, data, tab = self.bkjw.get_courses(self.bkjw.std_info["term"])

        # table = DoubleTable("[" + tmp) 这里也想打印表，可是实在搞不来 求PR
        # print(table.table)
        # 投机取巧，以这种既不美好的方式结束战斗。。。
        print(str(tab).replace("], [", "\n").strip("[").strip("]"))

    def __elva_teaching__(self):
        self.bkjw.elva_teaching()       # 这里一键评教

    @staticmethod
    def __help__():
        print("")
        table_datas = [
            ["\033[1;36m\nMODULES\n", """
        login       :  user login
        help        :  show this list
        listC       :  List selected courses
        exit        :  Exit Current Program
         
        \033[1;m"""]
        ]
        table = DoubleTable(table_datas)
        print(table.table)

    def __login__(self):
        # 输密码
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
