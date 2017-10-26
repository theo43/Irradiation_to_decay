#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: theo43@github
date: Sept. 2017
POS: page for choice of files to be post-treated
"""

from tkinter import Frame, Label, StringVar, END, Listbox, ttk, Entry
from functools import partial


class ChooseFilesPage(Frame):
    """Page for output files choice"""

    def __init__(self, parent, controller, *files):
        """Arguments:
               - parent (Frame)
               - controller (Tk)
               - files (list)
        """
        super().__init__(parent)
        self.controller = controller
        self.files = sorted(files[0][0])
        self.init_UI()

    # Create main GUI window
    def init_UI(self):
        #yDefilB = Scrollbar(self, orient='vertical')

        txt = "Select the file you want to display in the next page"
        label = Label(self, text=txt)
        label.pack()

        label_entry = Label(self, text='Filter : ')
        label_entry.pack()

        self.search_var = StringVar()
        self.search_var.trace("w",
                              lambda name, index, mode: self.update_list())
        self.entry = Entry(self, textvariable=self.search_var, width=13)
        self.entry.pack()


        self.lbox = Listbox(self, width=45, height=15,
                            selectmode='multiple')
        self.lbox.pack()

        btn_select_all = ttk.Button(self, text='Select all',
                                    command=self.select_all)
        btn_select_all.pack()

        btn_unselect_all = ttk.Button(self, text='Unselect all',
                                      command=self.unselect_all)
        btn_unselect_all.pack()

        txt = "Display selected items"
        # Command allowing comunication to controller (Tk), calling
        # raise_displayer_files method with selected files in self.data
        cmd = partial(self.controller.raise_displayer_files)
        self.btn_next = ttk.Button(self, text=txt, command=cmd)
        self.btn_next.pack()

        # update_list needs to be called here to populate the listbox
        self.update_list()


    def update_list(self):
        """Update the list while doing the search with the filter
           Warning: the selection is reset when the listbox is updated!
        """
        search_term = self.search_var.get()

        # Generic list to populate the listbox
        lbox_list = self.files

        self.lbox.delete(0, END)

        for item in lbox_list:
            if search_term.lower() in item.lower():
                self.lbox.insert(END, item)

    def select_all(self):
        self.lbox.select_set(0, END)

    def unselect_all(self):
        self.lbox.select_clear(0, END)
