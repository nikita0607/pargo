import os

from os import path
from subprocess import run as _run
from subprocess import STDOUT, PIPE


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
            if el.startswith("-"):
                flags[el] = ""
            elif argv[ind-1].startswith("-"):
                flags[argv[ind-1]] = el
            else:
                args.append(el)

        elif not el.startswith("-"):
            args.append(el)

        else:
            flags[el] = ""

    return flags, argv


def make_file(_dir, data: str = ""):
    with open(_dir, "w") as file:
        file.write(data)


def cd(dir: str) -> str:
    last_dir = os.getcwd()

    if len(dir) and dir != ".":
        os.chdir(dir)

    return last_dir


def run(command: str):
    out = _run(command.split(), stdout=PIPE, stderr=STDOUT, text=True)
    return out


@command("help")
def help(argv):
    print("This is a help!")


@command("installr")
def install_r(argv: list[str]):
    flags, args = parse_flags(argv)

    dir = args[0] if len(args) else ""
    name = flags["-n"] if "-n" in flags else "requirements.txt"

    if len(dir) and dir != "." and not os.path.isdir(dir):
        print("Directory {dir} not found!")
        return

    cur_dir = cd(dir)

    if not os.path.isfile(name):
        print(f"File {name} not found")
        cd(cur_dir)
        return

    out = run(f"pip install -r {name}")
    print(out.stdout)

    print("Success!")

    cd(cur_dir)



@command("new")
def new(argv: list[str]):
    work_dir = os.getcwd()

    flags, args = parse_flags(argv)

    print(flags)

    if "-h" in flags or "--help" in flags or not len(flags) and not len(args):
        print("""   Help:
Flags:
 --no-git: Don't initialize git repo.
 --no-readme: Don't create README.md file.
 --no-req: Don't create requirements.txt.
 --no-hw:  Don't create hello world code.
""")
        return

    name = args.pop(0) if len(args) else None

    if name is None:
        if "-n" in flags:
            name = flags["-n"]
        if "--name" in flags:
            name = flags["--name"]

    if not name or not len(name):
        print("Please, enter name!")
        return

    os.mkdir(name) if not path.isdir(name) else None

    if not "--no-git" in flags:   # Initialize GIT repo
        os.chdir(f"{name}")
        code = os.system("git init")
        print(code)

    if not "--no-readme" in flags:
        make_file("README.md")
    else:
        print("No README.md")

    if not "--no-req":
        make_file("requirements.txt")

    if not "--no-hw" in flags:   # Create main.py file
        make_file(f"main.py", 'print("Hello world!")')
    else:
        make_file("main.py")
        print("No Hello world")

    print(f"Succesfully created project: {name}")

    os.chdir(work_dir)
