from eval_first import eval_text, eval_cmd
import errors

STDLIB_PATH = "stdlib/liscript.clj"
eval_cmd(f"l {STDLIB_PATH}")


def REPL():
    while True:
        cmd = input(">> ")
        try:
            if cmd and cmd[0] == ":":
                eval_cmd(cmd[1:])
            else:
                eval_text(cmd)
        except Exception as e:
            errors.print_error_log(e)


REPL()
