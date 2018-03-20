# -*- coding: utf-8 -*-
"""
Page displaying the files chosen by the user, and enables giving the data
needed for each file post-processing.

"""

import tkinter
import os.path
from .page_choose_files import ChooseFilesPage

LARGE_FONT = ("Verdana", 12)


class DisplayFilesPage(tkinter.Frame):
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
            tkinter.messagebox.showerror(title, txt)
            self.controller.destroy()

    def init_UI(self):
        """
        Create GUI for the chosen files and its corresponding data to be
        provided

        """

        row = 0
        txt = "Fill in the data corresponding to the selected files"
        label = tkinter.Label(self, text=txt, font=LARGE_FONT)
        label.grid(row=row, columnspan=3, sticky='w')

        row += 1
        label = tkinter.Label(self, text="-" * 170)
        label.grid(row=row, columnspan=4, sticky='w')

        row += 1
        label = tkinter.Label(self, text="Selected files names")
        label.grid(row=row, columnspan=2, sticky='w')
        label = tkinter.Label(self, text="Number of fuel assemblies")
        label.grid(row=row, column=2, sticky='w')
        label = tkinter.Label(self, text="Assemblies mass (tons of U/Pu)")
        label.grid(row=row, column=3, sticky='w')

        working_dir = self.controller.data.working_dir
        for file in self.file_names:
            self.controller.data.file_data[file] = {
                'loc': os.path.join(working_dir, file),
                'nbFA': tkinter.StringVar(),
                'FAmass': tkinter.StringVar()
            }
            # Display the file name
            row += 1
            label = tkinter.Label(self, text=file)
            label.grid(row=row, columnspan=2, sticky='w')
            # Field to provide corresponding number of FA
            var = self.controller.data.file_data[file]['nbFA']
            entry = tkinter.Entry(self, textvariable=var)
            entry.grid(row=row, column=2, sticky='w')
            # Field to provide corresponding number of FA
            var = self.controller.data.file_data[file]['FAmass']
            entry = tkinter.Entry(self, textvariable=var)
            entry.grid(row=row, column=3, sticky='w')

        row += 1
        label = tkinter.Label(self, text="-" * 170)
        label.grid(row=row, columnspan=4, sticky='w')

        row += 1
        var = self.controller.data.choice['decay']['bool']
        txt = "Generate decay power curves"
        checkbu = tkinter.Checkbutton(self, text=txt, variable=var)
        checkbu.grid(row=row, column=0, sticky='w')

        row += 1
        txt = "Total thermal power (MWth): "
        label = tkinter.Label(self, text=txt)
        label.grid(row=row, column=0, sticky='w')
        var = self.controller.data.choice['decay']['power']
        entry = tkinter.Entry(self, textvariable=var)
        entry.grid(row=row, column=1, sticky='w')

        row += 1
        txt = "Fuel contains MOX"
        var = self.controller.data.choice['decay']['mox']
        checkbu = tkinter.Checkbutton(self, text=txt, variable=var)
        checkbu.grid(row=row, column=0, sticky='w')

        row += 1
        txt = ("Suffix for results file: (Letters, numbers or "
               "underscores only)")
        label = tkinter.Label(self, text=txt)
        label.grid(row=row, column=0, sticky='w')
        var = self.controller.data.choice['decay']['suffix']
        entry = tkinter.Entry(self, textvariable=var)
        entry.grid(row=row, column=1, sticky='w')

        row += 1
        label = tkinter.Label(self, text="-" * 170)
        label.grid(row=row, columnspan=4, sticky='w')

        row += 1
        var = self.controller.data.choice['source']['bool']
        txt = "Generate source terms inventories"
        checkbu = tkinter.Checkbutton(self, text=txt, variable=var)
        checkbu.grid(row=row, column=0, sticky='w')

        row += 1
        label = tkinter.Label(self, text="Make inventories of:")
        label.grid(row=row, column=0, sticky='w')

        row += 1
        var = self.controller.data.choice['source']['chosen_categ']['Elements']
        checkbu = tkinter.Checkbutton(self, text="Elements", variable=var)
        checkbu.grid(row=row, column=0, sticky='w')
        var = self.controller.data.choice['source']['chosen_categ']['Isotopes']
        checkbu = tkinter.Checkbutton(self, text="Isotopes", variable=var)
        checkbu.grid(row=row, column=1, sticky='w')

        row += 1
        label = tkinter.Label(self, text="Output unit(s) (many options are possible):")
        label.grid(row=row, column=0, sticky='w')

        row += 1
        var = self.controller.data.choice['source']['chosen_units']['g']
        checkbu = tkinter.Checkbutton(self, text="Gram", variable=var)
        checkbu.grid(row=row, column=0, sticky='w')
        var = self.controller.data.choice['source']['chosen_units']['bq']
        checkbu = tkinter.Checkbutton(self, text="Becquerel", variable=var)
        checkbu.grid(row=row, column=1, sticky='w')
        var = self.controller.data.choice['source']['chosen_units']['wt']
        checkbu = tkinter.Checkbutton(self, text="Watt (total)", variable=var)
        checkbu.grid(row=row, column=2, sticky='w')
        var = self.controller.data.choice['source']['chosen_units']['wg']
        checkbu = tkinter.Checkbutton(self, text="Watt (gamma)", variable=var)
        checkbu.grid(row=row, column=3, sticky='w')

        row += 1
        txt = ("Suffix for results file: (Letters, numbers or "
               "underscores only)")
        label = tkinter.Label(self, text=txt)
        label.grid(row=row, column=0, sticky='w')
        var = self.controller.data.choice['source']['suffix']
        entry = tkinter.Entry(self, textvariable=var)
        entry.grid(row=row, column=1, sticky='w')

        row += 1
        label = tkinter.Label(self, text="-" * 170)
        label.grid(row=row, columnspan=4, sticky='w')

        row += 1
        txt = "Next"
        cmd = self.controller.check_user_data
        button = tkinter.ttk.Button(self, text=txt, command=cmd)
        button.grid(row=row, column=3, sticky='w')
