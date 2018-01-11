# -*- coding:utf-8 -*-
from time import sleep
import sys
import traceback

sys.path.append('./modules')
from bkjwer import Bkjw
from usrshl import Cmd0


def main():
    print("hello world")
    # connect_test()
    cmd = Cmd0()
    try:
        while True:
            cmd.cmd_line()

    except KeyboardInterrupt:
        print("\n" + exit_msg)
        sleep(1)

    except Exception:
        traceback.print_exc(file=sys.stdout)
        sys.exit(0)


if __name__ == '__main__':
    main()



