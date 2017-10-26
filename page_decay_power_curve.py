#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: theo43@github
date: Sept. 2017
POS: page for decay power curve plotting
"""

from tkinter import Frame, Label, StringVar, END, Listbox, ttk, Entry
from functools import partial


class DecayPowerCurvePage(Frame):
    """
    """

    def __init__(self, parent, controller, *args):
        """Arguments:
               - parent (Frame)
               - controller (Tk)
        """
        super().__init__(parent)
        self.controller = controller
        self.init_UI()

    # Create main GUI window
    def init_UI(self):

        #row = 0
        txt = "Plotting time!!!"
        label = Label(self, text=txt)
        label.pack()




        txt = "Next"
        cmd = partial(self.controller.check_user_data)
        bu = ttk.Button(self, text=txt, command=cmd)
        bu.pack()

        # update_list needs to be called here to populate the listbox
        #self.update_list()


    def after_decay(self):
        """
        """
        #self.controller.data.choice['decay']['bool'].set(0)
        self.controller.check_user_data()

    def update_list(self):
        """Update the list while doing the search with the filter
           Warning: the selection is reset when the listbox is updated!
        """
        search_term = self.search_var.get()

        # Generic list to populate the listbox
        lbox_list = self.files

        self.lbox.delete(0, END)

        for item in lbox_list:
            print(item)
            if search_term.lower() in item.lower():
                self.lbox.insert(END, item)

    def select_all(self):
        self.lbox.select_set(0, END)

    def unselect_all(self):
        self.lbox.select_clear(0, END)
