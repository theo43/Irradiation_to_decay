# -*- coding: utf-8 -*-
"""
@author: theo43@github
date: Sept. 2017
POS: page for chosen files display and corresponding data
"""

from tkinter import (Frame, Label, StringVar, Entry, messagebox,
                     Checkbutton, ttk)
from os.path import join
from page_choose_files import ChooseFilesPage
LARGE_FONT= ("Verdana", 12)


class DisplayFilesPage(Frame):
    """Display the files chosen in ChooseFilesPage, and ask the user the data
       to be used with each file

       Arguments:
           - parent (Frame): container Frame on the main Tk
           - controller (MainWindow): main page
           - data (Data)

    """

    def __init__(self, parent, controller, file_names):
        super().__init__(parent)
        self.controller = controller
        self.file_names = file_names[0]

        if self.file_names:
            self.controller.frames[ChooseFilesPage].destroy()
            self.init_UI()
        else:  # If file_names is empty: no chosen files
            title = "Error: files selection"
            txt = "No selected files!\nExiting..."
            messagebox.showerror(title, txt)
            self.controller.destroy()

    def init_UI(self):
        """Create GUI for the chosen files and its corresponding data to be
           provided

        """

        row = 0
        txt = "Fill in the data corresponding to the selected files"
        la = Label(self, text=txt, font=LARGE_FONT)
        la.grid(row=row, columnspan=3, sticky='w')

        row += 1
        la = Label(self, text="-"*150)
        la.grid(row=row, columnspan=4, sticky='w')
        
        row += 1
        la = Label(self, text="Selected files names")
        la.grid(row=row, columnspan=2, sticky='w')
        la = Label(self, text="Number of FA")
        la.grid(row=row, column=2, sticky='w')
        la = Label(self, text="FA mass (tons of U)")
        la.grid(row=row, column=3, sticky='w')
        
        working_dir = self.controller.data.working_dir
        for file in self.file_names:
            self.controller.data.file_data[file] = {
                'loc': join(working_dir, file),
                'nbFA': StringVar(),
                'FAmass': StringVar()
            }
            # Display the file name
            row += 1
            la = Label(self, text=file)
            la.grid(row=row, columnspan=2, sticky='w')
            # Field to provide corresponding number of FA
            #self.controller.data.file_data[file]['nbFA']
            var = self.controller.data.file_data[file]['nbFA']
            en = Entry(self, textvariable=var)
            en.grid(row=row, column=2, sticky='w')
            # Field to provide corresponding number of FA
            var = self.controller.data.file_data[file]['FAmass']
            en = Entry(self, textvariable=var)
            en.grid(row=row, column=3, sticky='w')

        row += 1
        la = Label(self, text="-"*150)
        la.grid(row=row, columnspan=4, sticky='w')

        row += 1
        var = self.controller.data.choice['decay']['bool']
        txt = "You want to generate decay power curves"
        ch = Checkbutton(self, text=txt, variable=var)
        ch.grid(row=row, column=0, sticky='w')

        row += 1
        txt = "Total thermal power (MW): "
        la = Label(self, text=txt)
        la.grid(row=row, column=0, sticky='w')
        var = self.controller.data.choice['decay']['power']
        en = Entry(self, textvariable=var)
        en.grid(row=row, column=1, sticky='w')

        row += 1
        txt = "Fuel contains MOX"
        var = self.controller.data.choice['decay']['mox']
        ch = Checkbutton(self, text=txt, variable=var)
        ch.grid(row=row, column=0, sticky='w')

        row += 1
        txt = ("Suffix for results file: \n(Letters, numbers or\n"
               "underscores only)")
        la = Label(self, text=txt)
        la.grid(row=row, column=0, sticky='w')
        var = self.controller.data.choice['decay']['suffix']
        en = Entry(self, textvariable=var)
        en.grid(row=row, column=1, sticky='w')

        row += 1
        la = Label(self, text="-"*150)
        la.grid(row=row, columnspan=4, sticky='w')

        row += 1
        var = self.controller.data.choice['source']['bool']
        txt = "You want to generate source terms inventories"
        ch = Checkbutton(self, text=txt, variable=var)
        ch.grid(row=row, column=0, sticky='w')

        row += 1
        la = Label(self, text="You want inventories for:")
        la.grid(row=row, column=0, sticky='w')

        row += 1
        var = self.controller.data.choice['source']['chosen_categ']['Elements']
        ch = Checkbutton(self, text="Elements", variable=var)
        ch.grid(row=row, column=0, sticky='w')
        var = self.controller.data.choice['source']['chosen_categ']['Isotopes']
        ch = Checkbutton(self, text="Isotopes", variable=var)
        ch.grid(row=row, column=1, sticky='w')

        row += 1
        la = Label(self, text="For what unit(s):")
        la.grid(row=row, column=0, sticky='w')

        row += 1
        var = self.controller.data.choice['source']['chosen_units']['g']
        ch = Checkbutton(self, text="Gram", variable=var)
        ch.grid(row=row, column=0, sticky='w')
        var = self.controller.data.choice['source']['chosen_units']['bq']
        ch = Checkbutton(self, text="Becquerel", variable=var)
        ch.grid(row=row, column=1, sticky='w')
        var = self.controller.data.choice['source']['chosen_units']['wt']
        ch = Checkbutton(self, text="Watt (total)", variable=var)
        ch.grid(row=row, column=2, sticky='w')
        var = self.controller.data.choice['source']['chosen_units']['wg']
        ch = Checkbutton(self, text="Watt (gamma)", variable=var)
        ch.grid(row=row, column=3, sticky='w')

        row += 1
        txt = ("Suffix for results file: \n(Letters, numbers or\n"
               "underscores only)")
        la = Label(self, text=txt)
        la.grid(row=row, column=0, sticky='w')
        var = self.controller.data.choice['source']['suffix']
        en = Entry(self, textvariable=var)
        en.grid(row=row, column=1, sticky='w')

        row += 1
        la = Label(self, text="-"*150)
        la.grid(row=row, columnspan=4, sticky='w')

        row += 1
        txt = "Next"
        cmd = self.controller.check_user_data
        bu = ttk.Button(self, text=txt, command=cmd)
        bu.grid(row=row, column=2, sticky='w')
