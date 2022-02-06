import os

from os import path
from subprocess import run as _run
from subprocess import STDOUT, PIPE

from typing import Union, List, Dict


commands = {}


def run_command(argv: list) -> bool:
    command = argv[0]

    if command in commands:
        commands[command][0](argv[1:])
        return True

    return False


def command(name: str, desciption: str = "No description"):
    def dec(fn):
        commands[name] = fn, desciption
        return fn
    return dec


def name_from_argv(argv: List[str]) -> Union[str, List[str]]:
    if "-n" in argv:
        return argv.pop(argv.index("-n")+1), argv
    if "--name" in argv:
        return argv.pop(argv.index("--name")+1), argv

    return None, argv


def print_unknown_values(argv: List[str]):
    for i in argv:
        if i.startswith("-"):
            print(f"Unknown flag: {i}")
        else:
            print(f"Unknown param: {i}")


def parse_flags(argv: List[str]) -> Union[Dict[str, str], List[str]]:
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

    return flags, args


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


@command("help", "Seen this message")
def help(argv):
    print("Avaiabled commands: ")
    for name, com in commands.items():
        print(f"{name}: {com[1]}")


@command("installr", "Install requirements from file")
def install_r(argv: List[str]):
    flags, args = parse_flags(argv)

    dir = args[0] if len(args) else ""
    name = flags["-n"] if "-n" in flags else "requirements.txt"

    if len(dir) and dir != "." and not os.path.isdir(dir):
        print(f"Directory {dir} not found!")
        return

    cur_dir = cd(dir)

    if not os.path.isfile(name):
        print(f"File {name} not found")
        cd(cur_dir)
        return

    out = run(f"pip install -r {name}")
    print(out.stdout)

    print("Success installing requirements!")

    cd(cur_dir)


@command("clone", "Clone Python repo")
def clone(argv: List[str]):
    flags, args = parse_flags(argv)
    
    if "-h" in flags or "--help" in flags or not len(flags) and not len(args):
        print("""   Help:
It clone Python repo and install requirements
Flags: No
""")
        return

    req_file = flags["-r"] if "-r" in flags else "requirements.txt"

    if len(args) < 0:
        print("Please, enter url")
        return

    out = run(f"git clone {args[0]}")
    std = out.stdout

    print(std)

    if out.returncode != 0:
        return
    
    dir_name = std[std.index("'")+1:]
    dir_name = dir_name[:dir_name.index("'")]

    print(f"Try install requirements from {req_file}")
    install_r(["-n", f"{dir_name}/{req_file}"])


@command("new", "Create new empty project")
def new(argv: List[str]):
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
    os.chdir(f"{name}")
    
    if "--no-git" not in flags:   # Initialize GIT repo
        run("git init")

    if "--no-readme" not in flags:
        make_file("README.md")
    else:
        print("No README.md")

    if not "--no-req":
        make_file("requirements.txt")

    if "--no-hw" not in flags:   # Create main.py file
        make_file("main.py", 'print("Hello world!")')
    else:
        make_file("main.py")

    print(f"Succesfully created project: {name}")

    os.chdir(work_dir)
