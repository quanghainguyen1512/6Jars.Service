# import os
# import glob

# print(os.path.dirname(__file__))
# __all__ = [os.path.basename(f)[:-3] for f in glob.glob(os.path.dirname(__file__) + '/*.py')]
# __all__ = ['categories', 'users']
from .categories import Categories
from .users import *