# -*- coding: utf-8 -*-
"""
Page displaying the files chosen by the user, and enables giving the data
needed for each file post-processing.

"""

from tkinter import (Frame, Label, StringVar, Entry, messagebox,
                     Checkbutton, ttk)
from os.path import join
from .page_choose_files import ChooseFilesPage

LARGE_FONT = ("Verdana", 12)


class DisplayFilesPage(Frame):
    """
    Display the files chosen in ChooseFilesPage, and ask the user the data to
    be used with each file

    """

    def __init__(self, parent, controller, file_names):
        """
        Arguments:
            `parent` (Frame):
                Parent page

            `controller` (Tk):
                Main controller page

            `file_names` (list):
                Chosen file names

        """
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
        """
        Create GUI for the chosen files and its corresponding data to be
        provided

        """

        row = 0
        txt = "Fill in the data corresponding to the selected files"
        label = Label(self, text=txt, font=LARGE_FONT)
        label.grid(row=row, columnspan=3, sticky='w')

        row += 1
        label = Label(self, text="-"*170)
        label.grid(row=row, columnspan=4, sticky='w')

        row += 1
        label = Label(self, text="Selected files names")
        label.grid(row=row, columnspan=2, sticky='w')
        label = Label(self, text="Number of fuel assemblies")
        label.grid(row=row, column=2, sticky='w')
        label = Label(self, text="Assemblies mass (tons of U/Pu)")
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
        label = Label(self, text="-"*170)
        label.grid(row=row, columnspan=4, sticky='w')

        row += 1
        var = self.controller.data.choice['decay']['bool']
        txt = "Generate decay power curves"
        checkbu = Checkbutton(self, text=txt, variable=var)
        checkbu.grid(row=row, column=0, sticky='w')

        row += 1
        txt = "Total thermal power (MWth): "
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
        txt = ("Suffix for results file: (Letters, numbers or "
               "underscores only)")
        label = Label(self, text=txt)
        label.grid(row=row, column=0, sticky='w')
        var = self.controller.data.choice['decay']['suffix']
        entry = Entry(self, textvariable=var)
        entry.grid(row=row, column=1, sticky='w')

        row += 1
        label = Label(self, text="-"*170)
        label.grid(row=row, columnspan=4, sticky='w')

        row += 1
        var = self.controller.data.choice['source']['bool']
        txt = "Generate source terms inventories"
        checkbu = Checkbutton(self, text=txt, variable=var)
        checkbu.grid(row=row, column=0, sticky='w')

        row += 1
        label = Label(self, text="Make inventories of:")
        label.grid(row=row, column=0, sticky='w')

        row += 1
        var = self.controller.data.choice['source']['chosen_categ']['Elements']
        checkbu = Checkbutton(self, text="Elements", variable=var)
        checkbu.grid(row=row, column=0, sticky='w')
        var = self.controller.data.choice['source']['chosen_categ']['Isotopes']
        checkbu = Checkbutton(self, text="Isotopes", variable=var)
        checkbu.grid(row=row, column=1, sticky='w')

        row += 1
        label = Label(self, text="Output unit(s) (many options are possible):")
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
        txt = ("Suffix for results file: (Letters, numbers or "
               "underscores only)")
        label = Label(self, text=txt)
        label.grid(row=row, column=0, sticky='w')
        var = self.controller.data.choice['source']['suffix']
        entry = Entry(self, textvariable=var)
        entry.grid(row=row, column=1, sticky='w')

        row += 1
        label = Label(self, text="-"*170)
        label.grid(row=row, columnspan=4, sticky='w')

        row += 1
        txt = "Next"
        cmd = self.controller.check_user_data
        button = ttk.Button(self, text=txt, command=cmd)
        button.grid(row=row, column=3, sticky='w')