# -*- coding: utf-8 -*-
"""
Created on Fri Oct 20 10:42:01 2017
@author: theo43@github
"""

from  sys import exit
from page_main import MainPage, Data


def main():
    app = MainPage(Data)
    app.mainloop()
    return 0
    
if __name__ == '__main__':
    exit(main())
