#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: theo43@github
date: Sept. 2017
POS: main program
"""

import sys, os, glob, time
import matplotlib.pyplot as plt
import pandas as pd
from tkinter import (Tk, Scrollbar, Label, Frame, Canvas, Checkbutton, Button,
                     IntVar, StringVar, Entry)
from functions import (create_df_decay_power, gather_df, create_df_inventories,
                       convert_str_sec, get_dict_group_noe, get_state_IntVar)
from regular_expressions import (regex_time, regex_category, regex_categ_unit,
                                 regex_after_Decay)
from dictionaries import (act_u9_np9_uncertainty, u9_np9_uncertainty,
                          fp_uncertainty, fuel_uncertainty, factors_time,
                          dict_unit)

if __name__ == '__main__':

    print("POS.py begins")

    # Define "Input" and "Output" folders location
    in_loc = os.path.join(os.path.dirname(os.getcwd()), 'Input')
    out_loc = os.path.join(os.path.dirname(os.getcwd()), 'Output')

    # Check if 'Input' folder exists
    if os.path.isdir(in_loc):
        list_in_files = [f for f in glob.glob(os.path.join(in_loc, '*.out'))]

        # If empty, restart needed
        if list_in_files == []:
            msg = ("\nWarning, the following folder:\n{}\ndoes not contain any"
                   " \".out\" file. The files you want to post-treat need to "
                   "be placed in it. Please restart.".format(in_loc))
            print(msg)
            sys.exit(0)

    if not os.path.exists(in_loc):
        msg = ("\nWarning, the following folder doesn't exist:\n{}\nIt is now "
               "created and empty. The files you want to post-treat need to "
               "be placed in it. Please restart.".format(in_loc))
        os.mkdir(in_loc)
        print(msg)
        sys.exit(0)

    # Also check if 'Output' folder exists. If not, create it
    if not os.path.exists(out_loc):
        os.mkdir(out_loc)
        msg = ("\nThe following folder doesn't exist:\n{}\nCreation of this "
               "folder, where your resulting files will be located."\
               .format(out_loc))
        print(msg)

    ##########################################################################

    root = Tk()
    root.title('POS - main page')

    # Create vertical and horizontal Scrollbars
    SbV = Scrollbar(root, orient='vertical')
    SbV.grid(row=0, column=1, sticky='n'+'s')
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

    # Add widgets
    r = 0
    La = Label(Fr, text="Welcome to POS.py!")
    La.grid(row=r, columnspan=4)

    r += 1
    La = Label(Fr, text=190*"-")
    La.grid(row=r, column=0, columnspan=4, sticky='w')

    r += 1
    La = Label(Fr, text="What do you want to generate?")
    La.grid(row=r, columnspan=4, sticky='w')

    r += 1
    choice1 = IntVar()
    Ch = Checkbutton(Fr, text="Decay power curve",
                     variable=choice1)
    Ch.grid(row=r, column=0, sticky='w')

    r += 1
    choice2 = IntVar()
    Ch = Checkbutton(Fr, text="Source terms inventories",
                     variable=choice2)
    Ch.grid(row=r, column=0, sticky='w')

    r += 1
    La = Label(Fr, text=190*"-")
    La.grid(row=r, column=0, columnspan=4, sticky='w')

    r += 1
    t = "Select the output files to post-treat and fill-in the required data"
    La = Label(Fr, text=t)
    La.grid(row=r, columnspan=4, sticky='w')

    r += 1
    t = "Available \".out\" files in {}:".format(in_loc)
    La = Label(Fr, text=t)
    La.grid(row=r, columnspan=4, sticky='w')

    r += 1
    La = Label(Fr, text="Files names")
    La.grid(row=r, column=0)
    La = Label(Fr, text="Number of FA")
    La.grid(row=r, column=1, sticky='w')
    La = Label(Fr, text="FA mass (tons)")
    La.grid(row=r, column=2, sticky='w')

    dict_out = {}
    for f in sorted(list_in_files):
        r += 1
        dict_out[f] = {}
        dict_out[f]['IntVar'] = IntVar()
        Ch = Checkbutton(Fr,
                         text=os.path.basename(f),
                         variable=dict_out[f]['IntVar'])
        Ch.grid(row=r, column=0, sticky='w')
        dict_out[f]['nbFA'] = StringVar()
        En = Entry(Fr, textvariable=dict_out[f]['nbFA'])
        En.grid(row=r, column=1, sticky='w')
        dict_out[f]['FAmass'] = StringVar()
        En = Entry(Fr, textvariable=dict_out[f]['FAmass'])
        En.grid(row=r, column=2, sticky='w')

    r += 1
    La = Label(Fr, text=190*"-")
    La.grid(row=r, column=0, columnspan=4, sticky='w')

    r += 1
    La = Label(Fr, text="Information for power curve generation:")
    La.grid(row=r, columnspan=3, column=0, sticky='w')

    r += 1
    La = Label(Fr, text="Total thermal power (MW)")
    La.grid(row=r, column=0, sticky='w')
    core_power = StringVar()
    En = Entry(Fr, textvariable=core_power)
    En.grid(row=r, column=1, sticky='w')

    r += 1
    mox = IntVar()
    Ch = Checkbutton(Fr, text="The fuel contains MOX", variable=mox)
    Ch.grid(row=r, columnspan=3, sticky='w')

    r += 1
    La = Label(Fr, text="Suffix for the decay power results file name:")
    La.grid(row=r, column=0, sticky='w')
    dec_suffix = StringVar()
    En = Entry(Fr, textvariable=dec_suffix)
    En.grid(row=r, column=1, sticky='w')

    r += 1
    La = Label(Fr, text=190*"-")
    La.grid(row=r, column=0, columnspan=4, sticky='w')

    r += 1
    La = Label(Fr, text="Information for source terms generation:")
    La.grid(row=r, columnspan=3, column=0, sticky='w')

    r += 1
    La = Label(Fr, text="Source terms are needed in:")
    La.grid(row=r, columnspan=2, column=0)

    r += 1
    elements_needed = IntVar()
    Ch = Checkbutton(Fr, text='Elements', variable=elements_needed)
    Ch.grid(row=r, column=0, sticky='w')

    isotopes_needed = IntVar()
    Ch = Checkbutton(Fr, text='Isotopes', variable=isotopes_needed)
    Ch.grid(row=r, column=1, sticky='w')

    r += 1
    La = Label(Fr, text="For the following units:")
    La.grid(row=r, columnspan=2, column=0)

    r += 1
    u_tW = IntVar()
    u_gW = IntVar()
    u_g = IntVar()
    u_bq = IntVar()
    Ch = Checkbutton(Fr, text='Grams', variable=u_g)
    Ch.grid(row=r, column=0, sticky='w')
    Ch = Checkbutton(Fr, text='Becquerel', variable=u_bq)
    Ch.grid(row=r, column=1, sticky='w')
    Ch = Checkbutton(Fr, text='Watts (total)', variable=u_tW)
    Ch.grid(row=r, column=2, sticky='w')
    Ch = Checkbutton(Fr, text='Watts (gamma)', variable=u_gW)
    Ch.grid(row=r, column=3, sticky='w')

    r += 1
    La = Label(Fr, text="Suffix for the source terms results file name:")
    La.grid(row=r, column=0, sticky='w')
    inv_suffix = StringVar()
    En = Entry(Fr, textvariable=inv_suffix)
    En.grid(row=r, column=1, sticky='w')

    r += 1
    La = Label(Fr, text=190*"-")
    La.grid(row=r, column=0, columnspan=4, sticky='w')

    r += 1
    Bu = Button(Fr, text='Next', command=root.destroy)
    Bu.grid(row=r, column=3, columnspan=2, sticky='w')

    Ca.create_window(0, 0, window=Fr)
    Fr.update_idletasks()
    Ca.config(scrollregion=Ca.bbox("all"))

    root.mainloop()

    # End of the first interface.
    ##########################################################################
    # General data gathering.

    if choice1.get() == 0 and choice2.get() == 0:
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

    # Build a list containing the information chosen by the user to be
    # inserted in a Dataframe
    info = []
    info.append(os.path.basename(f))
    info.append(FAmass_per_file)
    info.append(nFA_per_file)
    info.append(chosen_files)

    df_info = pd.DataFrame(info,
                           index=['File name',
                                  'FA mass (tons)',
                                  'Number of FA',
                                  'File location'])
    df_info = df_info.T.groupby(['File name']).sum()

    if n_selected_files == 0:
        print("\nUnable to continue: you need to select at least one file.")
        sys.exit(0)
    else:
        print("You selected {} files.".format(n_selected_files))

    # End of general data gathering.
    ##########################################################################
    # Choice 1: Decay power generation chosen by the user.

    if choice1.get() == 1:
        list_batch_df = []
        try:
            core_power = float(core_power.get())
        except ValueError:
            print("\nUnable to continue: the thermal power is not a number.")
            sys.exit(0)
        mox = mox.get()

        # Create a DataFrame for each chosen file and add it to list_batch_df
        for file_loc in chosen_files:
            list_batch_df.append(create_df_decay_power(file_loc,
                                                       factors_time,
                                                       regex_time,
                                                       regex_category,
                                                       regex_categ_unit,
                                                       regex_after_Decay))

        # Gather the DataFrames of list_batch_df in df_total
        df_total = gather_df(list_batch_df,
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
        file_name = "Decay_power_curve_" + dec_suffix.get() + ".xlsx"
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
        file_name = "Plot_decay_power_curve_" + dec_suffix.get() + ".eps"
        file_name = os.path.join(fold, file_name)
        plt.savefig(file_name)
        print("\nCreation of:\n{}".format(file_name))

    ##########################################################################
    # Choice 2: Source terms generation chosen by the user.

    if choice2.get() == 1:
        list_units = []
        if u_tW.get() == 1:
            list_units.append('W')
        if u_gW.get() == 1:
            list_units.append('W_gamma')
        if u_g.get() == 1:
            list_units.append('g')
        if u_bq.get() == 1:
            list_units.append('Bq')

        list_categories = []
        if elements_needed.get() == 1:
            list_categories.append('Elements')
        if isotopes_needed.get() == 1:
            list_categories.append('Isotopes')

        list_batch_df = []
        t0 = time.time()
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

        dinv = {}
        for c in list_categories:
            dinv[c] = {}
            for u in list_units:
                dinv[c][u] = list_batch_df[0][c][u]
                dinv[c][u] = dinv[c][u] * FAmass_per_file[0]*\
                             nFA_per_file[0]
                for i, d in enumerate(list_batch_df[1:]):
                    df_to_add = d[c][u] * FAmass_per_file[i+1] *\
                                nFA_per_file[i+1]
                    dinv[c][u] = dinv[c][u].add(df_to_add, fill_value=0)

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

            i = 0
            for g in sorted(dict_grp_noe.keys()):
                if g not in dict_IntVar.keys():
                    dict_IntVar[g] = {}

                La = Label(Fr, text=g)
                La.grid(row=1, column=5*i, columnspan=3, sticky='w')

                (ro, co) = (1, 0)

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
            file_name += inv_suffix.get() + ".xlsx"
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
