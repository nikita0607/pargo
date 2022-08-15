try:
    import core
except ModuleNotFoundError:
    from . import core

core.main()
