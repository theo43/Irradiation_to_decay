#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: theo43@github
date: Sept. 2017
POS: pages for choice of elements or isotopes (source terms inventories)
"""

from tkinter import Frame, Label, IntVar, Checkbutton, ttk, messagebox
from functools import partial
from sys import exit
from functions import write_results
LARGE_FONT= ("Verdana", 12)

class ElementsPage(Frame):
    """Choice of the elements for source terms inventories generation"""

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
        txt = "Choose the required elements for source terms inventories"
        label = Label(self, text=txt, font=LARGE_FONT)
        label.grid(row=row, columnspan=6, sticky='w')

        dict_grp_ioe = self.controller.data.choice['source']['di_elem']

        self.controller.data.choice['source']['elements'] = {}
        di = self.controller.data.choice['source']['elements']

        i = 0
        list_ch_grp = []
        for grp in sorted(dict_grp_ioe):
            cmd = partial(self.select_all, grp)
            ch_sel = ttk.Button(self,
                                text="Select all {}".format(grp.lower()),
                                command=cmd)
            cmd = partial(self.unselect_all, grp)
            ch_unsel = ttk.Button(self,
                                  text="Unselect all {}".format(grp.lower()),
                                  command=cmd)
            list_ch_grp.append((ch_sel, ch_unsel))
            
            di[grp] = {}
            
            # Display the group name ("Actinides", "Fission products", ..)
            label = Label(self, text=grp.title(), font=LARGE_FONT)
            label.grid(row=1, column=3*i, sticky='w')

            (row, col) = (1, 0)

            for ioe in sorted(dict_grp_ioe[grp]):
                if row <= 16:
                    row += 1
                else:
                    row= 2
                    col += 1
                di[grp][ioe] = IntVar()
                ch = Checkbutton(self,
                                 text=ioe.title(),
                                 variable=di[grp][ioe])
                ch.grid(row=row, column=col+3*i, sticky='w')
            i += 1

        row = 45

        txt = "Select all elements"
        cmd = partial(self.select_all, 'Actinides', 'Fission products',
                      'Light elements')
        bu = ttk.Button(self, text=txt, command=cmd)
        bu.grid(row=row, column=0, sticky='w')

        txt = "Unselect all elements"
        cmd = partial(self.unselect_all, 'Actinides', 'Fission products',
                      'Light elements')
        bu = ttk.Button(self, text=txt, command=cmd)
        bu.grid(row=row+1, column=0, sticky='w')

        co = 1
        for tup in list_ch_grp:  # List containing tuples of Buttons
            tup[0].grid(row=row, column=co, sticky='w')
            tup[1].grid(row=row+1, column=co, sticky='w')
            co += 1

        txt = "Next"
        cmd = partial(self.after_elements)
        bu = ttk.Button(self, text=txt, command=cmd)
        bu.grid(row=row+1, column=4, sticky='w')

    def after_elements(self):
        """Process tests, write elements inventory results and display next
           Frame depending on user choices
        
        """
        di_chosen_categ = self.controller.data.choice['source']['chosen_categ']
        di_chosen_categ['Elements'].set(0)
        test_error = self.controller.data.error_input('Elements')
        if test_error[0]:
            messagebox.showerror(test_error[1][0], test_error[1][1])
            self.destroy()
            exit(0)

        # Write the results in an Excel file
        suffix = self.controller.data.choice['source']['suffix'].get()
        result = self.controller.data.choice['source']['result']
        df_info = self.controller.data.df_info
        time_steps = self.controller.data.choice['source']['time_steps']
        index_group_ioe = self.controller.data.choice['source']['elements']
        index_group_ioe = index_group_ioe['group_ioe']
        list_title_msg = write_results(self.controller.data.working_dir,
                                       "Source_terms",
                                       suffix,
                                       result,
                                       df_info,
                                       index_group_ioe=index_group_ioe,
                                       time_steps=time_steps,
                                       category="Elements")

        for tup in list_title_msg:
                messagebox.showinfo(tup[0], tup[1])

        self.controller.raise_elements_isotopes()

    def select_all(self, *args):
        """Select all elements from all groups"""
        
        di = self.controller.data.choice['source']['elements']
        for grp in di:
            if grp in args:
                for ioe in di[grp]:
                    di[grp][ioe].set(1)

    def unselect_all(self, *args):
        """Unselect all elements from all groups"""
        
        di = self.controller.data.choice['source']['elements']
        for grp in di:
            if grp in args:
                for ioe in di[grp]:
                    di[grp][ioe].set(0)


class IsotopesPage(Frame):
    """Choice of the isotopes for source terms inventories generation"""

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
        txt = "Choose the required isotopes for source terms inventories"
        label = Label(self, text=txt, font=LARGE_FONT)
        label.grid(row=row, columnspan=6, sticky='w')

        dict_grp_ioe = self.controller.data.choice['source']['di_isot']

        self.controller.data.choice['source']['isotopes'] = {}
        di = self.controller.data.choice['source']['isotopes']

        i = 0
        list_ch_grp = []
        for grp in sorted(dict_grp_ioe):
            cmd = partial(self.select_all, grp)
            ch_sel = ttk.Button(self,
                                text="Select all {}".format(grp.lower()),
                                command=cmd)
            cmd = partial(self.unselect_all, grp)
            ch_unsel = ttk.Button(self,
                                  text="Unselect all {}".format(grp.lower()),
                                  command=cmd)
            list_ch_grp.append((ch_sel, ch_unsel))

            di[grp] = {}
            
            # Display the group name ("Actinides", "Fission products", ..)
            label = Label(self, text=grp.title(), font=LARGE_FONT)
            label.grid(row=1, column=5*i, sticky='w')

            (row, col) = (1, 0)

            for noe in sorted(dict_grp_ioe[grp]):
                if row <= 43:
                    row += 1
                else:
                    row= 2
                    col += 1
                di[grp][noe] = IntVar()
                ch = Checkbutton(self, text=noe.title(),
                                 variable=di[grp][noe])
                ch.grid(row=row, column=col+5*i, sticky='w')
            i += 1

        row = 45

        txt = "Select all isotopes"
        cmd = partial(self.select_all, 'Actinides', 'Fission products',
                      'Light elements')
        bu = ttk.Button(self, text=txt, command=cmd)
        bu.grid(row=row, column=0, sticky='w')

        txt = "Unselect all isotopes"
        cmd = partial(self.unselect_all, 'Actinides', 'Fission products',
                      'Light elements')
        bu = ttk.Button(self, text=txt, command=cmd)
        bu.grid(row=row+1, column=0, sticky='w')

        co = 1
        for tup in list_ch_grp:  # List containing tuples of Buttons
            tup[0].grid(row=row, column=co, sticky='w')
            tup[1].grid(row=row+1, column=co, sticky='w')
            co += 1

        txt = "Next"
        cmd = partial(self.after_isotopes)
        bu = ttk.Button(self, text=txt, command=cmd)
        bu.grid(row=row+1, column=4, sticky='w')


    def after_isotopes(self):
        """Process tests, write isotopes inventory results and display next
           Frame depending on user choices
        
        """
        di_chosen_categ = self.controller.data.choice['source']['chosen_categ']
        di_chosen_categ['Isotopes'].set(0)
        test_error = self.controller.data.error_input('Isotopes')
        if test_error[0]:
                messagebox.showerror(test_error[1][0], test_error[1][1])
                self.destroy()
                exit(0)

        # Write the results in an Excel file
        suffix = self.controller.data.choice['source']['suffix'].get()
        result = self.controller.data.choice['source']['result']
        df_info = self.controller.data.df_info
        time_steps = self.controller.data.choice['source']['time_steps']
        index_group_ioe = self.controller.data.choice['source']['isotopes']
        index_group_ioe = index_group_ioe['group_ioe']
        list_title_msg = write_results(self.controller.data.working_dir,
                                       "Source_terms",
                                       suffix,
                                       result,
                                       df_info,
                                       index_group_ioe=index_group_ioe,
                                       time_steps=time_steps,
                                       category="Isotopes")

        for tup in list_title_msg:
                messagebox.showinfo(tup[0], tup[1])

        self.controller.raise_elements_isotopes()

    def select_all(self, *args):
        """Select all isotopes from all groups"""
        
        di = self.controller.data.choice['source']['isotopes']
        for grp in di:
            if grp in args:
                for ioe in di[grp]:
                    di[grp][ioe].set(1)

    def unselect_all(self, *args):
        """Unselect all isotopes from all groups"""
        
        di = self.controller.data.choice['source']['isotopes']
        for grp in di:
            if grp in args:
                for ioe in di[grp]:
                    di[grp][ioe].set(0)
