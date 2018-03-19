#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Main module starting the program.
"""

from  sys import exit
from page_main import MainPage, Data


def main():
    app = MainPage(Data)
    app.mainloop()
    return 0

if __name__ == '__main__':
    exit(main())
