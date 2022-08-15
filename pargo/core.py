import sys

try:
    import _scripts as scripts
except ModuleNotFoundError:
    from . import _scripts as scripts


def main():
    """
    Main function
    """

    argv = sys.argv[1:]
    print("Python's project manager\n")

    if not argv:
        scripts.run_command(["help"])
        return
    if not scripts.run_command(argv):
        print("Command not found!")
        return
