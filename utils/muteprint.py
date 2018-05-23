"""
Usage: importer dans la classe dont les prints doivent etre redefinis
ajouter les instructions:
from utils.muteprint import mute_print
print = mute_print(print)
"""

import config.config as conf

def mute_print(func):
    def wrapped_func(*args,**kwargs):
        if conf.USE_STORM is False:
            return func(*args, **kwargs)
    return wrapped_func


