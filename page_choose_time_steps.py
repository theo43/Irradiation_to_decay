# -*- coding: utf-8 -*-
"""
Page displaying all the available time steps for source terms inventories.
"""

from tkinter import Frame, Label, IntVar, Checkbutton, ttk, messagebox
from functools import partial
from functions import convert_str_sec
from dictionaries import factors_time
from page_decay_power_curve import DecayPowerCurvePage
from page_display_files import DisplayFilesPage

LARGE_FONT = ("Verdana", 12)


class ChooseTimeStepsPage(Frame):
    """Choice of the time steps for source terms inventories generation"""

    def __init__(self, parent, controller, *args):
        """
        Arguments:
            `parent` (Frame):
                Parent page

            `controller` (Tk):
                Main controller page

        """
        super().__init__(parent)
        self.controller = controller
        self.init_UI()
        # Destroy the previous frame
        if type(self.controller.data.choice['decay']['result']) == bool:
            # If decay power source was generated, previous page was
            # DisplayFilesCurvePage
            self.controller.frames[DisplayFilesPage].destroy()
        else:  # Else, previous page was DecayPowerCurvePage
            self.controller.frames[DecayPowerCurvePage].destroy()

    def init_UI(self):
        """Create main GUI window"""

        row = 0
        txt = "Choose the required time steps for source terms inventories"
        label = Label(self, text=txt, font=LARGE_FONT)
        label.grid(row=row, columnspan=6, sticky='w')

        dict_df = self.controller.data.choice['source']['result']
        k1 = list(dict_df.keys())[0]
        k2 = list(dict_df[k1].keys())[0]
        l = dict_df[k1][k2].columns
        time_steps = sorted(l, key=lambda x: convert_str_sec(x, factors_time))
        self.controller.data.choice['source']['times'] = {}

        (row, col) = (0, 0)
        for step in time_steps:
            if row <= 20:
                row += 1
            else:
                row = 1
                col += 1
            self.controller.data.choice['source']['times'][step] = IntVar()
            var = self.controller.data.choice['source']['times'][step]
            checkbu = Checkbutton(self, text=step, variable=var)
            checkbu.grid(row=row, column=col, sticky='w')

        row += 22
        bu = ttk.Button(self, text="Select all", command=self.select_all)
        bu.grid(row=row, column=0, sticky='w')
        bu = ttk.Button(self, text="Unselect all", command=self.unselect_all)
        bu.grid(row=row, column=1, sticky='w')
        txt = "Next"
        cmd = partial(self.after_time_steps)
        bu = ttk.Button(self, text=txt, command=cmd)
        bu.grid(row=row, column=2, sticky='w')

    def after_time_steps(self):
        """
        After time steps choice for source terms inventories, raise the
        page corresponding to the user choice: elements choice page then/or
        isotopes choice page

        """

        chosen_steps = []
        dict_steps = self.controller.data.choice['source']['times']
        for step in dict_steps.keys():
            if dict_steps[step].get():
                chosen_steps.append(step)
        if chosen_steps == []:
            title = "Error: source terms inventories time steps"
            txt = ("No selected time steps!\nExiting...")
            messagebox.showerror(title, txt)
            self.controller.destroy()
        else:
            self.controller.data.choice['source']['time_steps'] = chosen_steps

        self.controller.raise_elements_isotopes()

    def select_all(self):
        dict_steps = self.controller.data.choice['source']['times']
        for step in dict_steps.keys():
            dict_steps[step].set(1)

    def unselect_all(self):
        dict_steps = self.controller.data.choice['source']['times']
        for step in dict_steps.keys():
            dict_steps[step].set(0)
