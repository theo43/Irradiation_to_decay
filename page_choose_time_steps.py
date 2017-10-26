#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: theo43@github
date: Sept. 2017
POS: page for choice time steps (source terms inventories)
"""

from tkinter import Frame, Label, IntVar, Checkbutton, ttk, messagebox
from functools import partial
from functions import convert_str_sec
from dictionaries import factors_time


class ChooseTimeStepsPage(Frame):
    """Choice of the time steps for source terms inventories generation"""

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

        row = 0
        txt = "Choose the required time steps for source terms inventories"
        label = Label(self, text=txt)
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
            ch = Checkbutton(self, text=step, variable=var)
            ch.grid(row=row, column=col, sticky='w')


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
        """

        chosen_steps = []
        dict_steps = self.controller.data.choice['source']['times']
        for step in dict_steps.keys():
            if dict_steps[step].get() == 1:
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
