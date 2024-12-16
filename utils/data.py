import os
import sys

def get_data_file(name):
    m = sys.modules[__name__]
    dir1 = os.path.dirname(m.__file__)
    dir2 = os.path.dirname(dir1)
    path = os.path.join(dir2, "data", name)
    return path
