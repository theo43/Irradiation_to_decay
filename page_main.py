# -*- coding: utf-8 -*-
"""
Page definition for the main `controller` page (`Tk` instance) controlling all
the other Frames. Also defines the `Data` class which contains all the data
provided by the user, and the program results.
"""

from tkinter import (messagebox, Tk, filedialog, Scrollbar, Canvas,
                     IntVar, StringVar)
import os
from re import match, split
from time import time
from sys import exit
from page_choose_files import ChooseFilesPage
from page_display_files import DisplayFilesPage
from page_decay_power_curve import DecayPowerCurvePage
from page_choose_time_steps import ChooseTimeStepsPage
from pages_elements_isotopes_choice import ElementsPage, IsotopesPage
from functions import (create_df_decay_power, gather_df_decay_power,
                       create_df_inventories,
                       gather_df_inventories,
                       get_dict_group_ioe,
                       write_results,
                       create_df_info)
from regular_expressions import (regex_time, regex_category, regex_categ_unit,
                                 regex_after_Decay)
from dictionaries import (act_u9_np9_uncertainty, u9_np9_uncertainty,
                          fp_uncertainty, fuel_uncertainty, factors_time)

LARGE_FONT = ("Verdana", 12)


class Data():
    """
    Object containing all the gathered user data and the results

    Attributes:
        `working_dir` (str):
            Location of the folder of the files
        
        `file_data` (dict):
            Keys are chosen file names, whose values are dictionaries whose
            keys once provided in DisplayFilesPage are
                - loc (str): absolute path of the file
                - nbFA (StringVar): number of FA for this file
                - FAmass (StringVar): FA mass for this file
                
        `choice` (dict):
            Contains information regarding user choices

    """

    def __init__(self, working_dir):
        self.working_dir = working_dir
        self.file_data = {}
        self.choice = {
            'decay': {
                # Switches to a DataFrame when decay power curve is generated
                'result': False,
                'path_res': "",  # Path to 'result'
                'bool': IntVar(),  # For decay power curve generation
                'mox': IntVar(),  # If fuel contains MOX
                'suffix': StringVar(),  # Suffix name for result file
                # Total thermal power in MW for normalization
                'power': StringVar(),

            },
            'source': {
                'bool': IntVar(),  # For source terms generation
                'suffix': StringVar(),  # Suffix name for result file
                'chosen_categ': {
                    'Isotopes': IntVar(),  # For isotopes source terms
                    'Elements': IntVar(),  # For elements source terms
                },
                'chosen_units': {
                    'g': IntVar(),  # For source terms in grams
                    'bq': IntVar(),  # For source terms in Becquerels
                    'wt': IntVar(),  # For source terms in Watts (total)
                    'wg': IntVar(),  # For source terms in Watts (gamma)
                },
                # Switches to a dict when inventories are generated
                'result': False,  # Available groups, elements/isotopes, units
                'di_elem': False,  # Available groups and elements in 'result'
                'di_isot': False,  # Available groups and isotopes in 'result'
            }
        }

    def error_input(self, user_choice):
        """
        Check if input data errors were made in DisplayFilesPage

        Arguments:
            `user_choice` (str):
                'decay' for decay power curve generation, or 'source' for
                source terms inventories generation

        Returns:
            `(error, msg)` (tuple):
                - error (bool): True if an error is detected
                - msg (str): error message to be printed in the message box

        """

        error = False  # Bool switching to True if an input error is detected

        if user_choice == 'files':  # Check if data attached to files are ok
            title = "Error: files data"
            msg = ""
            FAmass_per_file = []
            nFA_per_file = []
            chosen_files = []
            for file in sorted(self.file_data):
                # Are 'nbFA' and 'FAmass' numbers
                try:
                    FAmass = float(self.file_data[file]['FAmass'].get())
                    FAmass_per_file.append(FAmass)
                    nFA = float(self.file_data[file]['nbFA'].get())
                    nFA_per_file.append(nFA)
                    location = os.path.join(self.working_dir, file)
                    chosen_files.append(location)

                except ValueError:
                    error = True
                    msg = ("Number of FA and/or FA mass provided for file {} "
                           "not a number!\nExiting...".format(file))
                    return (error, (title, msg))
                # Are they > 0
                if (float(self.file_data[file]['nbFA'].get()) <= 0) or\
                (float(self.file_data[file]['FAmass'].get()) <= 0):
                    error = True
                    msg = ("Number of FA and/or FA mass provided for file {} "
                           "must be strictly positive!"
                           "\nExiting...".format(file))
                    return (error, (title, msg))

            self.df_info = create_df_info(chosen_files=chosen_files,
                                          nFA_per_file=nFA_per_file,
                                          FAmass_per_file=FAmass_per_file)

            return (error, (title, msg))  # No error detected

        if user_choice == 'decay':  # Decay power curve generation asked
            di = self.choice[user_choice]
            title = "Error: decay power curve data"
            msg = ""
            # Check if the provided total thermal power is a number
            try:
                float(di['power'].get())
            except ValueError:
                error = True
                msg = ("Total thermal power must be a number!\n"
                       "Exiting...")
                return (error, (title, msg))

            if float(di['power'].get()) <= 0.:  # Check if power is > 0
                error = True
                msg = ("Total thermal power must be strictly positive!\n"
                        "Exiting...")
                return (error, (title, msg))

            suffix = self.choice['decay']['suffix'].get()
            for char in suffix:
                if not match(r"\w", char):  # \w represents [a-zA-Z0-9_]
                    error = True
                    msg = ("The provided suffix contains a forbidden "
                           "character!\nOnly letters, numbers and underscores"
                           " are accepted\nExiting...")
                    return (error, (title, msg))

            return (error, (title, msg))  # No error detected

        if user_choice == 'source':  # Source terms generation asked
            di = self.choice[user_choice]
            title = "Error: source terms inventories data"
            msg = ""
            # Check if a category has been selected
            error = True
            for c in di['chosen_categ'].keys():
                if di['chosen_categ'][c].get():
                    error = False
                    break
            if error:
                msg = ("No selected category of source terms!\n"
                       "(Elements or isotopes)\nExiting...")
                return (error, (title, msg))
            # Check if a unit has been selected
            error = True
            for u in di['chosen_units'].keys():
                if di['chosen_units'][u].get():
                    error = False
                    break
            if error:
                msg = ("No selected unit!\nExiting...")
                return (error, (title, msg))

            return (error, (title, msg))  # No error detected

        if (user_choice == 'Elements') or (user_choice == 'Isotopes'):
            if (user_choice == 'Elements'):
                category = 'Elements'
                di = self.choice['source']['elements']
            else:
                category = 'Isotopes'
                di = self.choice['source']['isotopes']

            title = "Error: {} selection".format(category.lower())
            msg = ""
            di['group_ioe'] = [] # List of (group, ioe) to be printed

            for group in di:
                if group != 'group_ioe':  # ioe: isotope or element
                    # Creation of a sorted list of ioe for source terms
                    list_ioe = [ioe for ioe in di[group] if ioe != "Total"]
                    list_ioe = sorted(list_ioe)
                    if category == 'Elements':
                        # "Total" only available for elements
                        list_ioe.append("Total")
                    else:
                        pass

                    for ioe in list_ioe:
                        if di[group][ioe].get():
                            di['group_ioe'].append((group, ioe))
                else:
                    pass

            if di['group_ioe'] == []:
                msg = ("No selected {}!\nExiting...".format(category.lower()))
                return (True, (title, msg))
            else:
                return (False, (title, msg))

            suffix = self.choice['source']['suffix'].get()
            for char in suffix:
                if not match(r"\w", char):  # \w represents [a-zA-Z0-9_]
                    error = True
                    msg = ("The provided suffix contains a forbidden "
                           "character!\nOnly letters, numbers and underscores"
                           " are accepted\nExiting...")
                    return (error, (title, msg))

            return (error, (title, msg))  # No error detected


    def generate_power(self):
        """
        Generate decay power curve

        Returns:
            `df` (pandas.DataFrame):
                Contains the resulting decay power values for all the available
                time steps and the following sigma values: [0, 1.645, 2, 3]

        """

        list_df = []
        FAmass_per_file = []
        nFA_per_file = []
        core_power = float(self.choice['decay']['power'].get())
        mox = float(self.choice['decay']['mox'].get())

        t0 = time()
        for file in self.file_data.keys():
            df = create_df_decay_power(self.file_data[file]['loc'],
                                       factors_time,
                                       regex_time,
                                       regex_category,
                                       regex_categ_unit,
                                       regex_after_Decay)
            list_df.append(df)
            FAmass_per_file.append(float(self.file_data[file]['FAmass'].get()))
            nFA_per_file.append(float(self.file_data[file]['nbFA'].get()))

        t1 = time()
        msg = ("Decay power curve times:\n\t- DataFrame(s) list creation: {}"
               " sec".format(round(t1-t0, 1)))
        print(msg)

        df = gather_df_decay_power(list_df,            FAmass_per_file,
                                   nFA_per_file,       core_power,
                                   mox,                act_u9_np9_uncertainty,
                                   u9_np9_uncertainty, fp_uncertainty,
                                   fuel_uncertainty,   factors_time)
        t2 = time()
        msg = ("Decay power curve times:\n\t- DataFrame(s) gathering: {}"
               " sec".format(round(t2-t1, 1)))
        print(msg)

        self.choice['decay']['bool'].set(0)

        return df

    def generate_source(self):
        """
        Generate source terms inventories

        Returns:
            `dict_df` (dict):
                - 1st key (str): categories ('Elements' or 'Isotopes')
                - 2nd key (str): units ('g', 'bq', 'wt', 'wg')
                - 2nd key values (pandas.DataFrame): source terms inventories
                  for the corresponding category, unit. All the available time
                  steps and elements/isotopes are considered. The user will
                  later choose what time steps and elements/isotopes to
                  consider in the final inventories

        """

        list_df = []
        FAmass_per_file = []
        nFA_per_file = []
        list_categories = []
        list_units = []
        di = self.choice['source']
        for categ in sorted(di['chosen_categ'].keys()):
            if di['chosen_categ'][categ].get() == 1:
                list_categories.append(categ)
        for unit in sorted(di['chosen_units'].keys()):
            if di['chosen_units'][unit].get() == 1:
                list_units.append(unit)

        t0 = time()
        for file in self.file_data.keys():
            df = create_df_inventories(self.file_data[file]['loc'],
                                       list_units,
                                       list_categories,
                                       factors_time,
                                       regex_time,
                                       regex_category,
                                       regex_categ_unit,
                                       regex_after_Decay)
            list_df.append(df)
            FAmass_per_file.append(float(self.file_data[file]['FAmass'].get()))
            nFA_per_file.append(float(self.file_data[file]['nbFA'].get()))

        t1 = time()
        msg = ("Source terms times:\n\t- DataFrame(s) list creation: {}"
               " sec".format(round(t1-t0, 1)))
        print(msg)

        # Gather the dictionaries (one per chosen file) into a single one
        dict_df = gather_df_inventories(list_categories,
                                        list_units,
                                        list_df,
                                        FAmass_per_file,
                                        nFA_per_file)
        t2 = time()
        msg = ("Source terms times:\n\t- DataFrame(s) gathering: {}"
               " sec".format(round(t2-t1, 1)))
        print(msg)
        #self.choice['source']['time']['gather_df'] = round(t2-t1, 1)

        self.choice['source']['bool'].set(0)

        return dict_df

    def get_grp_ioe(self, category):
        """
        Get the available groups and elements/isotopes in the source terms
        inventories dictionary for the corresponding `category`
        
        Arguments:
            `category` (str):
                "Elements" or "Isotopes"
        
        Returns:
            `get_dict_group_ioe` (dict):
                Dictionary whose keys are the contained group, and values are
                the sorted list of isotopes or elements contained in this group

        """

        dict_resu = self.choice['source']['result']
        u0 = list(dict_resu[category].keys())[0]

        return get_dict_group_ioe(dict_resu[category][u0])


class MainPage(Tk):
    """Main application, refered to as `controller` in the different frames"""

    def __init__(self, data):
        """
        Arguments:
            `data` (Data):
                Object containing all the data provided by the user and the
                results

        """
        super().__init__()
        Tk.wm_title(self, "Irradec")

        # Initialize parameters (could be separated in a dedicated function)
        title = ("Location of the folder containing your files")
        ini_dir = os.environ['HOME']
        working_dir = filedialog.askdirectory(title=title,
                                              initialdir=ini_dir)

        # Initialize Data object controlled by the MainWindow
        self.data = Data(working_dir)
        self.out_files = []
        self.frames = {}

        # We generate only if the path is correct
        if os.path.exists(self.data.working_dir):
            for file_name in os.listdir(self.data.working_dir):
                if file_name.endswith('.out'):
                    self.out_files.append(file_name)

            # Initializing the UI in a dedicated function
            self.init_UI()
            self.geometry('{}x{}'.format(900, 850))

    def init_UI(self):

        # Create vertical and horizontal Scrollbars
        self.SbV = Scrollbar(self, orient='vertical')
        self.SbV.grid(row=0, column=1, sticky='N'+'S')
        self.SbH = Scrollbar(self, orient='horizontal')
        self.SbH.grid(row=1, column=0, sticky='E'+'W')

        # Create a canvas
        self.ca = Canvas(self,
                         yscrollcommand=self.SbV.set,
                         xscrollcommand=self.SbH.set)
        self.ca.grid(row=0, column=0, sticky="news")

        # Configure the Scrollbars on the Canvas
        self.SbV.config(command=self.ca.yview)
        self.SbH.config(command=self.ca.xview)

        # Configure row index of a grid
        self.grid_rowconfigure(0, weight=1)
        # Configure column index of a grid
        self.grid_columnconfigure(0, weight=1)

        self.show_frame(ChooseFilesPage, self.out_files)

    def show_frame(self, container, *args):
        """Show next frame to be displayed"""

        frame = container(self.ca, self, args)
        self.frames[container] = frame
        self.ca.create_window(0, 0, window=frame)
        frame.tkraise()
        self.ca.update_idletasks()
        self.ca.config(scrollregion=self.ca.bbox("all"))

    def raise_displayer_files(self):
        """
        Display the data (file names) chosen in the ChooseFilesPage. Raise
        DisplayFilesPage

        """

        li = self.frames[ChooseFilesPage].lbox.curselection()
        chosen_files = [self.frames[ChooseFilesPage].lbox.get(i) for i in li]

        self.show_frame(DisplayFilesPage, chosen_files)

    def check_user_data(self):
        """
        Check the data and choices provided by the user. If:
            - `choice['decay']['bool'] == 1` then decay power curve is
              generated first
            - `choice['source']['bool'] == 1` then source terms inventories
              are generated for the corresponding categories and units

        """

        if (not self.data.choice['decay']['bool'].get())\
        and (not self.data.choice['source']['bool'].get()):

            if type(self.data.choice['decay']['result']) == bool:
                # If decay power curve was not generated
                title = "Error: task selection"
                msg = "No requested task!\nExiting..."
                messagebox.showerror(title, msg)
                self.destroy()
            else:
                # If only decay power curve generation was asked: normal end
                title = "End of the program"
                msg = "Normal end of the program"
                messagebox.showinfo(title, msg)
                self.destroy()
        else:
            test_error = self.data.error_input('files')
            if test_error[0]:
                messagebox.showerror(test_error[1][0], test_error[1][1])
                self.destroy()
                exit(0)

        if self.data.choice['decay']['bool'].get():
            test_error = self.data.error_input('decay')
            if test_error[0]:
                messagebox.showerror(test_error[1][0], test_error[1][1])
                self.destroy()
                exit(0)
            self.data.choice['decay']['result'] = self.data.generate_power()

            # Write the results in an Excel file
            suffix = self.data.choice['decay']['suffix'].get()
            result = self.data.choice['decay']['result']
            df_info = self.data.df_info
            list_title_msg = write_results(self.data.working_dir,
                                           "Decay_power_curve",
                                           suffix,
                                           result,
                                           df_info)
            for tup in list_title_msg:
                messagebox.showinfo(tup[0], tup[1])

            path_res = split("\n", list_title_msg[-1][1])[-1]
            self.data.choice['decay']['path_res'] = path_res

            self.show_frame(DecayPowerCurvePage)
            return  # Just leave the function

        if self.data.choice['source']['bool'].get():
            test_error = self.data.error_input('source')
            if test_error[0]:
                messagebox.showerror(test_error[1][0], test_error[1][1])
                self.destroy()
                exit(0)
            self.data.choice['source']['result'] = self.data.generate_source()
            if type(self.data.choice['decay']['result']) == bool:
                # Decay power curve was not asked. The previous page is
                # ChooseFilesPage
                self.frames[ChooseFilesPage].destroy()
            else:  # Here the previous page is DecayPowerCurvePage
                self.frames[DecayPowerCurvePage].destroy()
            self.show_frame(ChooseTimeStepsPage)
            return  # Just leave the function

    def raise_elements_isotopes(self):
        """Raise the elements or isotopes choice page"""

        di = self.data.choice['source']

        if di['chosen_categ']['Elements'].get():
            di['di_elem'] = self.data.get_grp_ioe('Elements')
            self.frames[ChooseTimeStepsPage].destroy()
            self.show_frame(ElementsPage)
            return  # Just leave the function

        if di['chosen_categ']['Isotopes'].get():
            di['di_isot'] = self.data.get_grp_ioe('Isotopes')
            if type(di['di_elem']) == bool:
                # Elements inventories was not asked
                self.frames[ChooseTimeStepsPage].destroy()
            else:
                self.frames[ElementsPage].destroy()
            self.show_frame(IsotopesPage)
            return  # Just leave the function

        if (not di['chosen_categ']['Isotopes'].get())\
        and (not di['chosen_categ']['Elements'].get()):
            title = "End of the program"
            msg = "Normal end of the program"
            messagebox.showinfo(title, msg)
            self.destroy()
            exit(0)
