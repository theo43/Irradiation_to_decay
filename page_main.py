#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: theo43@github
date: Sept. 2017
POS: page for main window
"""

from tkinter import (Frame, messagebox, Tk, filedialog, Scrollbar, Canvas,
                     IntVar, StringVar)
import os
from re import match
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


class Data():
    """Object containing all the gathered user data

       Attributes:
           - working_dir (str): location of the folder of the files
           - file_data (dict): keys are chosen file names, whose values are
             dictionaries whose keys are
               - loc (str) --> absolute path of the file
               - nbFA (StringVar) --> number of FA for this file
               - FAmass (StringVar) --> FA mass for this file
           - choice (dict): {
                 'decay': {
                     'bool' (IntVar): if decay power curve generation is asked
                     'power' (StringVar): total thermal power (MW)
                     'suffix' (StringVar): suffix name for results file
                     'mox' (IntVar): if fuel contains MOX
                     'result' (DataFrame): decay power curve over time
                 }
                 'source': {
                     'bool' (IntVar): if source terms inventories are asked
                     'suffix' (StringVar): suffix name for results file
                     'chosen_categ': {
                         'Isotopes' (IntVar): for isotopes inventories
                         'Elements' (IntVar): for elements inventories
                     },
                     'chosen_units': {
                         'g' (IntVar): for source terms in grams
                         'bq' (IntVar): for source terms in becquerels
                         'wt' (IntVar): for source terms in watts (total)
                         'wg' (IntVar): for source terms in watts (gamma)
                     }
                     'result': (dict) 'category'--> 'unit' --> DataFrame
                }
           }
    """

    def __init__(self, working_dir):
        self.working_dir = working_dir
        self.file_data = {}
        self.choice = {
            'decay': {
                # Switches to a DataFrame when decay power curve is generated
                'result': False,
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
                'result': False
            }
        }

    def error_input(self, user_choice):
        """Check if input data errors were made in DisplayFilesPage

           Arguments:
               user_choice (str): 'decay' for decay power curve generation, or
               'source' for source terms inventories generation

           Returns:
               (error, msg) (tuple):
                   error (bool): True if an error is detected
                   msg: error message to be printed in the message box

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
                if di['chosen_categ'][c].get() == 1:
                    error = False
                    break
            if error:
                msg = ("No selected category of source terms!\n"
                       "(Elements or isotopes)\nExiting...")
                return (error, (title, msg))
            # Check if a unit has been selected
            error = True
            for u in di['chosen_units'].keys():
                if di['chosen_units'][u].get() == 1:
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
                        if di[group][ioe].get() == 1:
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
        """Generate decay power curve

           Returns:
               df (pandas.DataFrame): contains the resulting decay power values
               for all the available time steps and the following sigma values:
               [0, 1.645, 2, 3]

        """
        print("Enter Data.generate_power")
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

        # Generic function allowing saving the result file for decay power
        # curve or source terms inventories generation
        # TO BE ADDED
        self.choice['decay']['bool'].set(0)

        return df
