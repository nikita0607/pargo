"""
This module contains all console commands
"""


import os

from os import path
from subprocess import run as _run
from subprocess import STDOUT, PIPE

from typing import List

try:
    import _utils
except ModuleNotFoundError:
    from . import _utils


commands = {}


def run_command(argv: list) -> bool:
    """
    Run entered command
    """

    command = argv[0]

    if command in commands:
        commands[command][0](argv[1:])
        return True

    return False


def command(name: str, desciption: str = "No description"):
    """
    Decorator for new command's function
    """

    def dec(fn):
        commands[name] = fn, desciption
        return fn

    return dec


def run(comm: str):
    """
    Run command in console
    """

    out = _run(comm.split(), stdout=PIPE, stderr=STDOUT, text=True, check=False)

    return out


@command("help", "Seen this message")
def _help(_):
    """
    Print help message in console
    """

    print("Avaiabled commands: \n")
    for name, com in commands.items():
        print(f"{name}: {com[1]}")


@command("installr", "Install requirements from file")
def install_r(argv: List[str]):
    """
    This command install requirements
    """

    flags, args = _utils.parse_flags(argv)

    _dir = args[0] if len(args) else ""
    name = flags["-n"] if "-n" in flags else "requirements.txt"

    if _dir and _dir != "." and not os.path.isdir(_dir):
        print(f"Directory {dir} not found!")
        return

    cur_dir = _utils.cd(_dir)

    if not os.path.isfile(name):
        print(f"File {name} not found")
        _utils.cd(cur_dir)
        return

    out = run(f"pip install -r {name}")
    print(out.stdout)

    print("Success installing requirements!")

    _utils.cd(cur_dir)


@command("clone", "Clone Python repo")
def clone(argv: List[str]):
    """
    This command clone git repository
    """

    flags, args = _utils.parse_flags(argv)

    if "-h" in flags or "--help" in flags or not flags and not args:
        print(
            """   Help:
It clone Python repo and install requirements
Flags: No
"""
        )
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

    dir_name = std[std.index("'") + 1 :]
    dir_name = dir_name[: dir_name.index("'")]

    print(f"Try install requirements from {req_file}")
    install_r(["-n", f"{dir_name}/{req_file}"])


@command("new", "Create new empty project")
def new(argv: List[str]):
    """
    This command create new empty project
    """

    work_dir = os.getcwd()

    flags, args = _utils.parse_flags(argv)

    # print(flags)

    if _utils.is_help(flags) or not flags and not args:
        print(
            """   Help:
Flags:
 --no-git: Don't initialize git repo.
 --no-readme: Don't create README.md file.
 --no-req: Don't create requirements.txt.
 --no-hw:  Don't create hello world code.
"""
        )
        return

    name = args.pop(0) if len(args) else None

    if name is None:
        if "-n" in flags:
            name = flags["-n"]
        if "--name" in flags:
            name = flags["--name"]

    if not name:
        print("Please, enter name!")
        return

    if not path.isdir(name):
        os.mkdir(name)

    os.chdir(f"{name}")

    if "--no-readme" not in flags:
        _utils.make_file("README.md")
    else:
        print("No README.md")

    if "--no-req" not in flags:
        _utils.make_file("requirements.txt")
    
    if "--no-gignore" not in flags:
        ignore = "\n".join(("__pycache__", "env", "*.swp"))
        _utils.make_file(".gitignore", ignore)

    if "--lib" in flags:
        _lib_create(name, flags)
    else:
        _st_create(flags)

    if "--no-git" not in flags:  # Initialize GIT repo
        print("GIT init status: ", run("git init").stdout)
        run("git commit -m Init commit")

    print(f"Succesfully created project: {name}")

    os.chdir(work_dir)

def _lib_create(name, flags):
    os.mkdir(name)
    
    _setup = """from setuptools import setup, find_packages
from os.path import join, dirname


setup(
    name='{}',
    version='',
    url='',
    license='',

    author="",
    author_email="",

    packages=find_packages(),
    long_description=open(join(dirname(__file__), 'README.md')).read(),

    install_requires=[]
)""".format(name)

    _utils.make_file("setup.py", _setup)

    _utils.cd(name)
    if "--no-hw" not in flags:  # Create main.py file
        _utils.make_file("__init__.py", 'if __name__ == "__main__":\n'\
                                    '  print("Hello world!")')
    else:
        _utils.make_file("__init__.py", 'if __name__ == "__main__":\n'\
                                    '  pass')

def _st_create(flags):
    if "--no-hw" not in flags:  # Create main.py file
        _utils.make_file("main.py", 'print("Hello world!")')
    else:
        _utils.make_file("main.py")

