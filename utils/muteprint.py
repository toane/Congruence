"""
Usage: importer dans la classe dont les prints doivent etre redefinis
ajouter les instructions:
from utils.muteprint import mute_print
print = mute_print(print)
"""

DEBUG = True

def mute_print(func):
    def wrapped_func(*args,**kwargs):
        if DEBUG is True:
            return func(*args, **kwargs)
    return wrapped_func


