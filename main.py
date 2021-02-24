from utils import lazy_iterator, iterator 
import sys

if("-s" in sys.argv):
    lazy_iterator()
else:
    iterator()