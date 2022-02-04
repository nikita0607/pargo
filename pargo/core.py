import sys

try:
    import scripts
except:
    from . import scripts

def main(*args, **kwargs):
    argv = sys.argv[1:]

    print("Python's project manager\n")

    if not len(argv):
        scripts.help([])
        return

    if not scripts.run_command(argv):
        print("Command not found!")
        return
