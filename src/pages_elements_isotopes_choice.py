# -*- coding: utf-8 -*-
"""
Pages for choice of elements and isotopes for source terms inventories.
"""

import tkinter
from functools import partial
from sys import exit
from .functions import write_results
from .dictionaries import factors_time


LARGE_FONT = ("Verdana", 12)


class ElementsPage(tkinter.Frame):
    """Choice of the elements for source terms inventories generation"""

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

    # Create main GUI window
    def init_UI(self):

        row = 0
        txt = "Choose the required elements for source terms inventories"
        label = tkinter.Label(self, text=txt, font=LARGE_FONT)
        label.grid(row=row, columnspan=6, sticky='w')

        dict_grp_ioe = self.controller.data.choice['source']['di_elem']

        self.controller.data.choice['source']['elements'] = {}
        di = self.controller.data.choice['source']['elements']

        i = 0
        list_ch_grp = []
        for grp in sorted(dict_grp_ioe):
            cmd = partial(self.select_all, grp)
            ch_sel = tkinter.ttk.Button(self,
                                        text="Select all {}".format(grp.lower()),
                                        command=cmd)
            cmd = partial(self.unselect_all, grp)
            ch_unsel = tkinter.ttk.Button(self,
                                          text="Unselect all {}".format(grp.lower()),
                                          command=cmd)
            list_ch_grp.append((ch_sel, ch_unsel))

            di[grp] = {}

            # Display the group name ("Actinides", "Fission products", ..)
            label = tkinter.Label(self, text=grp.title(), font=LARGE_FONT)
            label.grid(row=1, column=3*i, sticky='w')

            (row, col) = (1, 0)

            for ioe in sorted(dict_grp_ioe[grp]):
                if row <= 16:
                    row += 1
                else:
                    row= 2
                    col += 1
                di[grp][ioe] = tkinter.IntVar()
                ch = tkinter.Checkbutton(self,
                                         text=ioe.title(),
                                         variable=di[grp][ioe])
                ch.grid(row=row, column=col+3*i, sticky='w')
            i += 1

        row = 45

        txt = "Select all elements"
        cmd = partial(self.select_all,
                      'Actinides',
                      'Fission products',
                      'Light elements')
        bu = tkinter.ttk.Button(self, text=txt, command=cmd)
        bu.grid(row=row, column=0, sticky='w')

        txt = "Unselect all elements"
        cmd = partial(self.unselect_all,
                      'Actinides',
                      'Fission products',
                      'Light elements')
        bu = tkinter.ttk.Button(self, text=txt, command=cmd)
        bu.grid(row=row+1, column=0, sticky='w')

        co = 1
        for tup in list_ch_grp:  # List containing tuples of Buttons
            tup[0].grid(row=row, column=co, sticky='w')
            tup[1].grid(row=row+1, column=co, sticky='w')
            co += 1

        txt = "Next"
        cmd = partial(self.after_elements)
        bu = tkinter.ttk.Button(self, text=txt, command=cmd)
        bu.grid(row=row+1, column=4, sticky='w')

    def after_elements(self):
        """
        Process tests, write elements inventory results and display next Frame
        depending on user choices

        """

        di_chosen_categ = self.controller.data.choice['source']['chosen_categ']
        di_chosen_categ['Elements'].set(0)
        test_error = self.controller.data.error_input('Elements')
        if test_error[0]:
            tkinter.messagebox.showerror(test_error[1][0], test_error[1][1])
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
                                       category="Elements",
                                       factors_time=factors_time)

        for tup in list_title_msg:
            tkinter.messagebox.showinfo(tup[0], tup[1])

        self.controller.raise_elements_isotopes()

    def select_all(self, *args):
        """Select all elements from all groups"""

        dictio = self.controller.data.choice['source']['elements']
        for group in dictio:
            if group in args:
                for ioe in dictio[group]:
                    dictio[group][ioe].set(1)

    def unselect_all(self, *args):
        """Unselect all elements from all groups"""

        dictio = self.controller.data.choice['source']['elements']
        for group in dictio:
            if group in args:
                for ioe in dictio[group]:
                    dictio[group][ioe].set(0)


class IsotopesPage(tkinter.Frame):
    """Choice of the isotopes for source terms inventories generation"""

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

    # Create main GUI window
    def init_UI(self):

        row = 0
        txt = "Choose the required isotopes for source terms inventories"
        label = tkinter.Label(self, text=txt, font=LARGE_FONT)
        label.grid(row=row, columnspan=6, sticky='w')

        dict_grp_ioe = self.controller.data.choice['source']['di_isot']

        self.controller.data.choice['source']['isotopes'] = {}
        di = self.controller.data.choice['source']['isotopes']

        i = 0
        list_ch_grp = []
        for grp in sorted(dict_grp_ioe):
            cmd = partial(self.select_all, grp)
            ch_sel = tkinter.ttk.Button(self,
                                        text="Select all {}".format(grp.lower()),
                                        command=cmd)
            cmd = partial(self.unselect_all, grp)
            ch_unsel = tkinter.ttk.Button(self,
                                          text="Unselect all {}".format(grp.lower()),
                                          command=cmd)
            list_ch_grp.append((ch_sel, ch_unsel))

            di[grp] = {}

            # Display the group name ("Actinides", "Fission products", ..)
            label = tkinter.Label(self, text=grp.title(), font=LARGE_FONT)
            label.grid(row=1, column=5*i, sticky='w')

            (row, col) = (1, 0)

            for noe in sorted(dict_grp_ioe[grp]):
                if row <= 43:
                    row += 1
                else:
                    row= 2
                    col += 1
                di[grp][noe] = tkinter.IntVar()
                ch = tkinter.Checkbutton(self, text=noe.title(),
                                         variable=di[grp][noe])
                ch.grid(row=row, column=col+5*i, sticky='w')
            i += 1

        row = 45

        txt = "Select all isotopes"
        cmd = partial(self.select_all, 'Actinides', 'Fission products',
                      'Light elements')
        bu = tkinter.ttk.Button(self, text=txt, command=cmd)
        bu.grid(row=row, column=0, sticky='w')

        txt = "Unselect all isotopes"
        cmd = partial(self.unselect_all, 'Actinides', 'Fission products',
                      'Light elements')
        bu = tkinter.ttk.Button(self, text=txt, command=cmd)
        bu.grid(row=row+1, column=0, sticky='w')

        co = 1
        for tup in list_ch_grp:  # List containing tuples of Buttons
            tup[0].grid(row=row, column=co, sticky='w')
            tup[1].grid(row=row+1, column=co, sticky='w')
            co += 1

        txt = "Next"
        cmd = partial(self.after_isotopes)
        bu = tkinter.ttk.Button(self, text=txt, command=cmd)
        bu.grid(row=row+1, column=4, sticky='w')


    def after_isotopes(self):
        """
        Process tests, write isotopes inventory results and display next Frame
        depending on user choices

        """

        di_chosen_categ = self.controller.data.choice['source']['chosen_categ']
        di_chosen_categ['Isotopes'].set(0)
        test_error = self.controller.data.error_input('Isotopes')
        if test_error[0]:
            tkinter.messagebox.showerror(test_error[1][0], test_error[1][1])
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
                                       category="Isotopes",
                                       factors_time=factors_time)

        for tup in list_title_msg:
                tkinter.messagebox.showinfo(tup[0], tup[1])

        self.controller.raise_elements_isotopes()

    def select_all(self, *args):
        """Select all isotopes from all groups"""

        dictio = self.controller.data.choice['source']['isotopes']
        for group in dictio:
            if group in args:
                for ioe in dictio[group]:
                    dictio[group][ioe].set(1)

    def unselect_all(self, *args):
        """Unselect all isotopes from all groups"""

        dictio = self.controller.data.choice['source']['isotopes']
        for group in dictio:
            if group in args:
                for ioe in dictio[group]:
                    dictio[group][ioe].set(0)
