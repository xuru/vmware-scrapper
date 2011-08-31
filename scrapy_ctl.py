#!/usr/bin/python
import sys, os.path
from scrapy.cmdline import execute
sys.path.insert(0, os.path.dirname(__file__))

os.environ.setdefault('SCRAPY_SETTINGS_MODULE', 'visdk41')
print sys.argv
execute(sys.argv)