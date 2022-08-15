import os

from typing import Union, List, Dict


def name_from_argv(argv: List[str]) -> Union[str, List[str]]:
    """
    Search args with -n or --name prefix
    :param argv: List of args from terminal
    :return: Finded name or None and changed list without this argument
    """

    if "-n" in argv:
        return argv.pop(argv.index("-n")+1), argv
    if "--name" in argv:
        return argv.pop(argv.index("--name")+1), argv

    return None, argv


def print_unknown_values(argv: List[str]):
    """
    Print unparsed values from terminal args
    :param argv: Terminal arguments
    """
    for i in argv:
        if i.startswith("-"):
            print(f"Unknown flag: {i}")
        else:
            print(f"Unknown param: {i}")


def parse_flags(argv: List[str]) -> Union[Dict[str, str], List[str]]:
    """
    Parse terminal args to dictionary
    :param argv: List of teminal arguments
    :return: Dict with parsed data and list with unparsed data
    """
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


def is_help(flags: dict) -> bool:
    if "-h" in flags or "--help" in flags:
        return True
    return False


def make_file(_dir, data: str = ""):
    """
    Crate new file 'dir' with 'data' data
    :param dir: Destination of file
    :param data: Data, what will be written in file
    """
    with open(_dir, "w") as file:
        file.write(data)


def cd(dir: str) -> str:
    """
    Cd another directory
    :param dir: Cd - destination
    :return: Previous directory
    """

    last_dir = os.getcwd()

    if len(dir) and dir != ".":
        os.chdir(dir)

    return last_dir

