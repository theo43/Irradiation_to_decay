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

LARGE_FONT = ("Verdana", 12)


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
        label = Label(self, text=txt, font=LARGE_FONT)
        label.grid(row=row, columnspan=3, sticky='w')

        row += 1
        label = Label(self, text="-"*150)
        label.grid(row=row, columnspan=4, sticky='w')

        row += 1
        label = Label(self, text="Selected files names")
        label.grid(row=row, columnspan=2, sticky='w')
        label = Label(self, text="Number of FA")
        label.grid(row=row, column=2, sticky='w')
        label = Label(self, text="FA mass (tons of U)")
        label.grid(row=row, column=3, sticky='w')

        working_dir = self.controller.data.working_dir
        for file in self.file_names:
            self.controller.data.file_data[file] = {
                'loc': join(working_dir, file),
                'nbFA': StringVar(),
                'FAmass': StringVar()
            }
            # Display the file name
            row += 1
            label = Label(self, text=file)
            label.grid(row=row, columnspan=2, sticky='w')
            # Field to provide corresponding number of FA
            #self.controller.data.file_data[file]['nbFA']
            var = self.controller.data.file_data[file]['nbFA']
            entry = Entry(self, textvariable=var)
            entry.grid(row=row, column=2, sticky='w')
            # Field to provide corresponding number of FA
            var = self.controller.data.file_data[file]['FAmass']
            entry = Entry(self, textvariable=var)
            entry.grid(row=row, column=3, sticky='w')

        row += 1
        label = Label(self, text="-"*150)
        label.grid(row=row, columnspan=4, sticky='w')

        row += 1
        var = self.controller.data.choice['decay']['bool']
        txt = "You want to generate decay power curves"
        checkbu = Checkbutton(self, text=txt, variable=var)
        checkbu.grid(row=row, column=0, sticky='w')

        row += 1
        txt = "Total thermal power (MW): "
        label = Label(self, text=txt)
        label.grid(row=row, column=0, sticky='w')
        var = self.controller.data.choice['decay']['power']
        entry = Entry(self, textvariable=var)
        entry.grid(row=row, column=1, sticky='w')

        row += 1
        txt = "Fuel contains MOX"
        var = self.controller.data.choice['decay']['mox']
        checkbu = Checkbutton(self, text=txt, variable=var)
        checkbu.grid(row=row, column=0, sticky='w')

        row += 1
        txt = ("Suffix for results file: \n(Letters, numbers or\n"
               "underscores only)")
        label = Label(self, text=txt)
        label.grid(row=row, column=0, sticky='w')
        var = self.controller.data.choice['decay']['suffix']
        entry = Entry(self, textvariable=var)
        entry.grid(row=row, column=1, sticky='w')

        row += 1
        label = Label(self, text="-"*150)
        label.grid(row=row, columnspan=4, sticky='w')

        row += 1
        var = self.controller.data.choice['source']['bool']
        txt = "You want to generate source terms inventories"
        checkbu = Checkbutton(self, text=txt, variable=var)
        checkbu.grid(row=row, column=0, sticky='w')

        row += 1
        label = Label(self, text="You want inventories for:")
        label.grid(row=row, column=0, sticky='w')

        row += 1
        var = self.controller.data.choice['source']['chosen_categ']['Elements']
        checkbu = Checkbutton(self, text="Elements", variable=var)
        checkbu.grid(row=row, column=0, sticky='w')
        var = self.controller.data.choice['source']['chosen_categ']['Isotopes']
        checkbu = Checkbutton(self, text="Isotopes", variable=var)
        checkbu.grid(row=row, column=1, sticky='w')

        row += 1
        label = Label(self, text="For what unit(s):")
        label.grid(row=row, column=0, sticky='w')

        row += 1
        var = self.controller.data.choice['source']['chosen_units']['g']
        checkbu = Checkbutton(self, text="Gram", variable=var)
        checkbu.grid(row=row, column=0, sticky='w')
        var = self.controller.data.choice['source']['chosen_units']['bq']
        checkbu = Checkbutton(self, text="Becquerel", variable=var)
        checkbu.grid(row=row, column=1, sticky='w')
        var = self.controller.data.choice['source']['chosen_units']['wt']
        checkbu = Checkbutton(self, text="Watt (total)", variable=var)
        checkbu.grid(row=row, column=2, sticky='w')
        var = self.controller.data.choice['source']['chosen_units']['wg']
        checkbu = Checkbutton(self, text="Watt (gamma)", variable=var)
        checkbu.grid(row=row, column=3, sticky='w')

        row += 1
        txt = ("Suffix for results file: \n(Letters, numbers or\n"
               "underscores only)")
        label = Label(self, text=txt)
        label.grid(row=row, column=0, sticky='w')
        var = self.controller.data.choice['source']['suffix']
        entry = Entry(self, textvariable=var)
        entry.grid(row=row, column=1, sticky='w')

        row += 1
        label = Label(self, text="-"*150)
        label.grid(row=row, columnspan=4, sticky='w')

        row += 1
        txt = "Next"
        cmd = self.controller.check_user_data
        button = ttk.Button(self, text=txt, command=cmd)
        button.grid(row=row, column=2, sticky='w')
