from parse import eval_text, eval_cmd

eval_cmd("l stdlib/liscript.clj")


def REPL():
    while True:
        cmd = input(">> ")
        try:
            if cmd and cmd[0] == ":":
                eval_cmd(cmd[1:])
            else:
                eval_text(cmd)
        except Exception as e:
            # raise e
            print(e)


REPL()
