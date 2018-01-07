# -*- coding: utf-8 -*-
"""
Page for files to post-process choice.
"""

from tkinter import Frame, Label, StringVar, END, Listbox, ttk, Entry
from functools import partial

LARGE_FONT = ("Verdana", 12)


class ChooseFilesPage(Frame):
    """Page for output files choice"""

    def __init__(self, parent, controller, *files):
        """
        Arguments:
            `parent` (Frame):
                Parent page

            `controller` (Tk):
                Main controller page

            `files` (list):
                Available .out files

        """

        super().__init__(parent)
        self.controller = controller
        self.files = sorted(files[0][0])
        self.init_UI()

    # Create main GUI window
    def init_UI(self):

        txt = "Select the file(s) you want to post-process"
        label = Label(self, text=txt, font=LARGE_FONT)
        label.grid(row=0, columnspan=2, sticky='w')

        label_entry = Label(self, text='Filter:')
        label_entry.grid(row=1, column=0, sticky='w')

        self.search_var = StringVar()
        self.search_var.trace("w",
                              lambda name, index, mode: self.update_list())
        self.entry = Entry(self, textvariable=self.search_var, width=13)
        self.entry.grid(row=1, column=1, sticky='w')

        self.lbox = Listbox(self, width=45, height=15,
                            selectmode='multiple')
        self.lbox.grid(row=2, columnspan=2)

        bu = ttk.Button(self, text='Select all', command=self.select_all)
        bu.grid(row=3, columnspan=2, sticky='w')

        bu = ttk.Button(self, text='Unselect all', command=self.unselect_all)
        bu.grid(row=4, columnspan=2, sticky='w')

        txt = "Display selected files"
        # Command allowing comunication to controller (Tk), calling
        # raise_displayer_files method with selected files in self.data
        cmd = partial(self.controller.raise_displayer_files)
        bu = ttk.Button(self, text=txt, command=cmd)
        bu.grid(row=5, columnspan=2, sticky='w')

        # update_list needs to be called here to populate the listbox
        self.update_list()


    def update_list(self):
        """
        Update the list while doing the search with the filter Warning: the
        selection is reset when the listbox is updated!

        """

        search_term = self.search_var.get()

        # Generic list to populate the listbox
        lbox_list = self.files

        self.lbox.delete(0, END)

        for item in lbox_list:
            if search_term.lower() in item.lower():
                self.lbox.insert(END, item)

    def select_all(self):
        """Select all the file names"""

        self.lbox.select_set(0, END)

    def unselect_all(self):
        """Unselect all the file names"""

        self.lbox.select_clear(0, END)
