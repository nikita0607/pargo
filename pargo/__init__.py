"""
This module add new python package manager in your system
"""


try:
    import core
except ModuleNotFoundError:
    from . import core


__all__ = ['core', '_utils', '_scripts']
