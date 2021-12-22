import os

from os import path


commands = {}


def run_command(argv: list) -> bool:
    command = argv[0]

    if command in commands:
        commands[command](argv[1:])
        return True

    return False


def command(name: str):
    def dec(fn):
        commands[name] = fn
        return fn  
    return dec


def name_from_argv(argv: list[str]) -> (str, list[str]):
    if "-n" in argv:
        return argv.pop(argv.index("-n")+1), argv
    if "--name" in argv:
        return argv.pop(argv.index("--name")+1), argv

    return None, argv


def print_unknown_values(argv: list[str]):
    for i in argv:
        if i.startswith("-"):
            print(f"Unknown flag: {i}")
        else:
            print(f"Unknown param: {i}")


def parse_flags(argv: list[str]) -> (dict[str, str], list[str]):
    args = []
    flags = {}

    for ind, el in enumerate(argv):
        if ind > 0:
            if argv[ind-1].startswith("-"):
                flags[argv[ind-1]] = el
            else:
                args.append(el)

        elif not el.startswith("-"):
            args.append(el)

    return flags, argv


def make_file(_dir):
    open(_dir, "w").close()


@command("help")
def help(argv):
    print("This is a help!")


@command("new")
def new(argv: list[str]):
    flags, args = parse_flags(argv)

    name = args.pop(0) if len(args) else None

    for fl in flags:
        if fl == "-n" or fl == "--name":
            name = flags[fl]

    if not name:
        print("Please, enter name!")
        return

    if len(argv):
        print_unknown_values(argv)
        return

    os.mkdir(name) if not path.isdir(name) else None
    make_file(f"{name}/main.py")
    print("Name:", name)
