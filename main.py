#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: theo43@github
date: Sept. 2017
POS: main program
"""

import sys, os, time

import matplotlib.pyplot as plt

import pandas as pd

from tkinter import (Tk, Scrollbar, Label, Frame, Canvas, Checkbutton, Button,
                     IntVar)

from functions import (create_df_decay_power, gather_df_decay_power,
                       create_df_inventories, convert_str_sec,
                       get_dict_group_noe, get_state_IntVar,
                       gather_df_inventories, check_input_output)

from regular_expressions import (regex_time, regex_category, regex_categ_unit,
                                 regex_after_Decay)

from dictionaries import (act_u9_np9_uncertainty, u9_np9_uncertainty,
                          fp_uncertainty, fuel_uncertainty, factors_time,
                          dict_unit)

from classes import Multipage, UserData

LARGE_FONT = ("Verdana", 12)

if __name__ == '__main__':

    print("POS.py begins")

    # Define "Input" and "Output" folders location
    in_loc = os.path.join(os.path.dirname(os.getcwd()), 'Input')
    out_loc = os.path.join(os.path.dirname(os.getcwd()), 'Output')

    # Check Input and Output folders, return available .out files
    list_in_files = check_input_output(in_loc, out_loc)


    ##########################################################################
    
    app = Multipage(UserData,
                    location=in_loc,
                    list_in_files=list_in_files,
                    font=LARGE_FONT)
    app.mainloop()
    
    dict_out = app.frames[UserData].return_info()
    choice1, choice2 = app.frames[UserData].return_choice()
    mox = app.frames[UserData].return_mox()
    dec_suffix = app.frames[UserData].return_decaypower_suffix()
    inv_suffix = app.frames[UserData].return_inventories_suffix()
    core_power = app.frames[UserData].return_core_power()
    list_units = app.frames[UserData].return_units()
    list_categories = app.frames[UserData].return_categories()
    
    print("POST APP:", mox, dec_suffix, inv_suffix, core_power, choice1)
    print('U: ', list_units)
    print('C: ', list_categories)
    
    # End of the first interface.
    ##########################################################################
    # General data gathering.

    if choice1 == 0 and choice2 == 0:
        msg = ("\nUnable to continue, you need to select at least one task"
               " to perform.")
        print(msg)
        sys.exit(0)

    chosen_files = []      # Locations of the file names chosen by the user
    nFA_per_file = []      # Number of FA per file given by the user
    FAmass_per_file = []   # FA mass per file given by the user
    n_selected_files = 0   # Number of selected files by the user

    # Create dictionary that will contain the chosen file names and the
    # corresponding FA number per batch and FA mass
    #selected_files = {}

    for f in list_in_files:
        try:
            if dict_out[f]['IntVar'].get() == 1:
                chosen_files.append(f)
                nFA_per_file.append(float(dict_out[f]['nbFA'].get()))
                FAmass_per_file.append(float(dict_out[f]['FAmass'].get()))
                n_selected_files += 1

        except ValueError:
            print("Unable to continue: you need to fill in the blanks!")
            sys.exit(0)
    
    if n_selected_files == 0:
        print("\nUnable to continue: you need to select at least one file.")
        sys.exit(0)
    else:
        print("You selected {} files.".format(n_selected_files))
        
    # Build a list containing the information chosen by the user to be
    # inserted in a Dataframe
    info = []
    info.append([os.path.basename(f) for f in chosen_files])
    info.append(FAmass_per_file)
    info.append(nFA_per_file)
    info.append(chosen_files)

    df_info = pd.DataFrame(info,
                           index=['File name',
                                  'FA mass (tons)',
                                  'Number of FA',
                                  'File location'])
    df_info = df_info.T.groupby(['File name']).sum()

    # End of general data gathering.
    ##########################################################################
    # Choice 1: Decay power generation chosen by the user.

    if choice1 == 1:
        list_batch_df = []
        try:
            core_power = float(core_power)
        except ValueError:
            print("\nUnable to continue: the thermal power is not a number.")
            sys.exit(0)

        # Create a DataFrame for each chosen file and append it to a list
        for file_loc in chosen_files:
            list_batch_df.append(create_df_decay_power(file_loc,
                                                       factors_time,
                                                       regex_time,
                                                       regex_category,
                                                       regex_categ_unit,
                                                       regex_after_Decay))

        # Gather the DataFrames of list_batch_df in df_total
        df_total = gather_df_decay_power(list_batch_df,
                                         FAmass_per_file,
                                         nFA_per_file,
                                         core_power,
                                         mox,
                                         act_u9_np9_uncertainty,
                                         u9_np9_uncertainty,
                                         fp_uncertainty,
                                         fuel_uncertainty,
                                         factors_time)

        # Check if the decay power curve folder exists in "Output" folder
        # If not, it is created
        fold = os.path.join(out_loc, "Decay_power_curve")
        if (os.path.exists(fold) == 0) or \
           (os.path.exists(fold) == 1 and os.path.isdir(fold) == 0):
            print("Creation of:\n{}".format(fold))
            os.mkdir(fold)

        # Write the output file in Excel format
        file_name = "Decay_power_curve_" + dec_suffix + ".xlsx"
        file_name = os.path.join(fold, file_name)
        writer = pd.ExcelWriter(file_name)
        df_info.to_excel(writer, "Data")
        df_total.to_excel(writer, "Decay power results")
        writer.save()
        print("\nCreation of:\n{}".format(file_name))

        # Plotting of the decay power curves
        df_total = df_total.reset_index()
        df_total = df_total.set_index(['Time steps [s]'])
        df_total = df_total.drop(['Time steps', 'Sigma value [%]'], axis=1)
        ax = df_total.plot(logx=1, logy=0, title='Decay power curves', grid=1)
        ax.set_xlabel('Decay time [s]')
        ax.set_ylabel('Decay power [% FP]')
        #plt.show()
        file_name = "Plot_decay_power_curve_" + dec_suffix + ".eps"
        file_name = os.path.join(fold, file_name)
        plt.savefig(file_name)
        print("\nCreation of:\n{}".format(file_name))

    ##########################################################################
    # Choice 2: Source terms generation chosen by the user.

    if choice2 == 1:

        list_batch_df = []
        t0 = time.time()

        # Create a DataFrame for each chosen file and append it to a list
        for file_loc in chosen_files:
            list_batch_df.append(create_df_inventories(file_loc,
                                                       list_units,
                                                       list_categories,
                                                       factors_time,
                                                       regex_time,
                                                       regex_category,
                                                       regex_categ_unit,
                                                       regex_after_Decay))
        t1 = time.time()
        t_df = round(t1-t0, 1)

        # Gather the dictionaries (one per chosen file) into a single one
        dinv = gather_df_inventories(list_categories, list_units,
                                     list_batch_df, FAmass_per_file,
                                     nFA_per_file)

        t2 = time.time()
        t_ga = round(t2-t1, 1)
        msg = ("\nTime spent to:\n\tCreate the dataframe inventories: {} sec\n"
               "\tGather the dataframes: {} sec".format(t_df, t_ga))
        print(msg)

         # Second interface for the user choice of time steps.
        l = dinv[list_categories[0]][list_units[0]].columns
        time_steps = sorted(l, key=lambda x: convert_str_sec(x, factors_time))

        root = Tk()
        root.title('Available time steps')

        # Create vertical and horizontal Scrollbars
        SbV = Scrollbar(root, orient='vertical')
        SbV.grid(row=0, column=1, sticky='N'+'S')
        SbH = Scrollbar(root, orient='horizontal')
        SbH.grid(row=1, column=0, sticky='E'+'W')

        # Create a canvas
        Ca = Canvas(root, yscrollcommand=SbV.set, xscrollcommand=SbH.set)
        Ca.grid(row=0, column=0, sticky="news")

        # Configure the Scrollbars on the Canvas
        SbV.config(command=Ca.yview)
        SbH.config(command=Ca.xview)

        # Configure row index of a grid
        root.grid_rowconfigure(0, weight=1)
        # Configure column index of a grid
        root.grid_columnconfigure(0, weight=1)

        # Create a frame on the canvas
        Fr = Frame(Ca)

        La = Label(Fr, text="Choose your time steps:")
        La.grid(row=0, columnspan=6)

        dict_IntVar = {}
        (r, c) = (0, 0)

        for ts in time_steps:
            #print ts
            if r <= 20:
                r += 1
            else:
                r = 1
                c += 1
            dict_IntVar[ts] = IntVar()
            Ch = Checkbutton(Fr, text=ts, variable=dict_IntVar[ts])
            Ch.grid(row=r, column=c, sticky='w')

        def select_all():
            for k in dict_IntVar.keys():
                dict_IntVar[k].set(1)
        def unselect_all():
            for k in dict_IntVar.keys():
                dict_IntVar[k].set(0)

        Bu = Button(Fr, text='Next', command=root.destroy)
        Bu.grid(row=24, column=5, sticky='w')

        Bu = Button(Fr, text='Select all', command=select_all)
        Bu.grid(row=24, column=1, sticky='w')

        Bu = Button(Fr, text='Unselect all', command=unselect_all)
        Bu.grid(row=24, column=3, sticky='w')

        Ca.create_window(0, 0, window=Fr)
        Fr.update_idletasks()
        Ca.config(scrollregion=Ca.bbox("all"))

        root.mainloop()

        # End of the second interface.
        ######################################################################
        # Chosen time steps for inventories gathering.

        # Get the time steps chosen by the user
        time_steps = get_state_IntVar(dict_IntVar, factors_time)

        # Check if the source terms folder exists in "Output" folder
        # If not, it is created.
        fold = os.path.join(out_loc, "Source_terms")
        if (os.path.exists(fold) == 0) or\
           (os.path.exists(fold) == 1 and os.path.isdir(fold) == 0):
            print("Creation of:\n{}".format(fold))
            os.mkdir(fold)

        for c in list_categories:
            u_tmp = list(dinv[c].keys())[0]
            dict_grp_noe = get_dict_group_noe(dinv[c][u_tmp])
            dict_IntVar = {}

            root = Tk()
            t = "Source terms generation: available " + c.lower()
            root.title(t)

            # Create vertical and horizontal Scrollbars
            SbV = Scrollbar(root, orient='vertical')
            SbV.grid(row=0, column=1, sticky='N'+'S')
            SbH = Scrollbar(root, orient='horizontal')
            SbH.grid(row=1, column=0, sticky='E'+'W')

            # Create a canvas
            Ca = Canvas(root, yscrollcommand=SbV.set, xscrollcommand=SbH.set)
            Ca.grid(row=0, column=0, sticky="news")

            # Configure the Scrollbars on the Canvas
            SbV.config(command=Ca.yview)
            SbH.config(command=Ca.xview)

            # Configure row index of a grid
            root.grid_rowconfigure(0, weight=1)
            # Configure column index of a grid
            root.grid_columnconfigure(0, weight=1)

            # Create a frame on the canvas
            Fr = Frame(Ca)

            La = Label(Fr, text="Choose your {}:".format(c.lower()))
            La.grid(row=0, columnspan=15)

            # dict_grp_noe keys are the available group(s) of isotopes or
            # elements from the chosen files
            i = 0
            for g in sorted(dict_grp_noe.keys()):
                if g not in dict_IntVar.keys():
                    dict_IntVar[g] = {}

                La = Label(Fr, text=g)
                La.grid(row=1, column=5*i, columnspan=3, sticky='w')

                (ro, co) = (1, 0)

                # dict_grp_noe values are sorted lists of isotopes or elements
                # corresponding to the group g
                for noe in sorted(dict_grp_noe[g]):
                    if ro <= 40:
                        ro += 1
                    else:
                        ro = 2
                        co += 1

                    dict_IntVar[g][noe] = IntVar()
                    Ch = Checkbutton(Fr, text=noe.title(),
                                     variable=dict_IntVar[g][noe])
                    Ch.grid(row=ro, column=co+5*i, sticky='w')

                i += 1

            def select_all():
                for g in dict_IntVar.keys():
                    for noe in dict_IntVar[g].keys():
                        dict_IntVar[g][noe].set(1)
            def unselect_all():
                for g in dict_IntVar.keys():
                    for noe in dict_IntVar[g].keys():
                        dict_IntVar[g][noe].set(0)

            def select_all_act():
                for noe in dict_IntVar['Actinides'].keys():
                    dict_IntVar['Actinides'][noe].set(1)
            def unselect_all_act():
                for noe in dict_IntVar['Actinides'].keys():
                    dict_IntVar['Actinides'][noe].set(0)

            def select_all_fp():
                for noe in dict_IntVar['Fission products'].keys():
                    dict_IntVar['Fission products'][noe].set(1)
            def unselect_all_fp():
                for noe in dict_IntVar['Fission products'].keys():
                    dict_IntVar['Fission products'][noe].set(0)

            def select_all_le():
                for noe in dict_IntVar['Light elements'].keys():
                    dict_IntVar['Light elements'][noe].set(1)
            def unselect_all_le():
                for noe in dict_IntVar['Light elements'].keys():
                    dict_IntVar['Light elements'][noe].set(0)

            t = "Select all " + c.lower()
            Bu = Button(Fr, text=t, command=select_all)
            Bu.grid(row=42, column=0, sticky='w')
            t = "Unselect all "+c.lower()
            Bu = Button(Fr, text=t, command=unselect_all)
            Bu.grid(row=43, column=0, sticky='w')

            if 'Actinides' in dict_IntVar.keys():
                t = "Select all actinides"
                Bu = Button(Fr, text=t, command=select_all_act)
                Bu.grid(row=42, column=1, sticky='w')
                t = "Unselect all actinides"
                Bu = Button(Fr, text=t, command=unselect_all_act)
                Bu.grid(row=43, column=1, sticky='w')

            if 'Fission products' in dict_IntVar.keys():
                t = "Select all fission products"
                Bu = Button(Fr, text=t, command=select_all_fp)
                Bu.grid(row=42, column=2, sticky='w')
                t = "Unselect all fission products"
                Bu = Button(Fr, text=t, command=unselect_all_fp)
                Bu.grid(row=43, column=2, sticky='w')

            if 'Light elements' in dict_IntVar.keys():
                t = "Select all light elements"
                Bu = Button(Fr, text=t, command=select_all_le)
                Bu.grid(row=42, column=3, sticky='w')
                t = "Unselect all light elements"
                Bu = Button(Fr, text=t, command=unselect_all_le)
                Bu.grid(row=43, column=3, sticky='w')

            Bu = Button(Fr, text='Next', command=root.destroy)
            Bu.grid(row=45, column=5, sticky='w')

            Ca.create_window(0, 0, window=Fr)
            Fr.update_idletasks()
            Ca.config(scrollregion=Ca.bbox("all"))

            root.mainloop()

            list_index = []

            for g in sorted(dict_IntVar.keys()):
                for noe in sorted(dict_IntVar[g].keys()):
                    if dict_IntVar[g][noe].get() == 1 and noe != 'Total':
                        tup = (g, noe)
                        list_index.append(tup)
                if c == 'Elements':
                    tup = (g, 'Total')
                    list_index.append(tup)

            # Write the output file in Excel format
            file_name = "Source_terms_" + c.lower() + "_"
            file_name += inv_suffix + ".xlsx"
            file_name = os.path.join(fold, file_name)
            writer = pd.ExcelWriter(file_name)

            # Create the dataframe to be provided to Excel file
            # Each sheet is a chosen unit
            for u in dinv[c].keys():
                dinv[c][u] = dinv[c][u].reindex(index=list_index,
                                                columns=time_steps)
                name = dict_unit[u].title()
                dinv[c][u].to_excel(writer, name)
            df_info.to_excel(writer, "Data")

            # Save the file, the chosen sheets (one sheet/unit) being created
            writer.save()
            print("\nCreation of:\n{}".format(file_name))

    print("\nEnd of POS.py")
