# TO BE USED WITH PYTHON V2.7
# -*- coding: iso-8859-1 -*-
# -*- encoding: iso8859-1 -*-
# Author: theo43@github

import pickle, re, sys, os, glob, shutil, time
import matplotlib.pyplot as plt
#import numpy as np
import pandas as pd
from functions_dict import *
from Tkinter import *
#from tkFont import Font

### Dictionnary containing the conversion factor between different time units and seconds.
factors_time = {
                'sec': 1.,
                'min': 60., # WARNING: minutes not yet considered in find_times function
                'hr': 3600.,
                'd': 24. * 3600.,
                'yr': 365 * 24. * 3600.
               }

### ****************************** Beginnning of main ******************************

if __name__ == '__main__':
    
    list_input_files = [n for n in glob.glob("../Input/*.out")]
    
    ##########################################################################################

    root = Tk()
    root.title('Post_ORIGEN-S')
    
    # Create vertical and horizontal Scrollbars
    SbV = Scrollbar(root, orient=VERTICAL)
    SbV.grid(row=0, column=1, sticky=N+S)
    SbH = Scrollbar(root, orient=HORIZONTAL)
    SbH.grid(row=1, column=0, sticky=E+W)
    
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
    La = Label(Fr, text="Welcome in Post_ORIGEN-S!")
    La.grid(row=r, columnspan=4)
    
    r += 1
    La = Label(Fr, text=120*"-")
    La.grid(row=r, column=0, columnspan=4, sticky=W)
    
    r += 1
    La = Label(Fr, text="What do you want to generate?")
    La.grid(row=r, columnspan=4, sticky=W)
    
    r += 1
    choice1 = IntVar()
    Ch = Checkbutton(Fr, text="Decay power curve",
                     variable=choice1)
    Ch.grid(row=r, column=0, sticky=W)
    
    r += 1
    choice2 = IntVar()
    Ch = Checkbutton(Fr, text="Source terms inventories",
                     variable=choice2)
    Ch.grid(row=r, column=0, sticky=W)
    
    r += 1
    La = Label(Fr, text=120*"-")
    La.grid(row=r, column=0, columnspan=4, sticky=W)
    
    r += 1
    t = "Select the ORIGEN-S output files to post-treat "
    t += "and fill-in the required data"
    La = Label(Fr, text=t)
    La.grid(row=r, columnspan=4, sticky=W)
    
    r += 1
    loc_input = os.path.dirname(os.getcwd())+'/Input'
    t = "Available \".out\" files in {}:".format(loc_input)
    La = Label(Fr, text=t)
    La.grid(row=r, columnspan=4, sticky=W)
    
    r += 1
    La = Label(Fr, text="Files names")
    La.grid(row=r, column=0)
    La = Label(Fr, text="Number of fuel assemblies")
    La.grid(row=r, column=1, sticky=W)
    La = Label(Fr, text="Fuel assembly mass (tons)")
    La.grid(row=r, column=2, sticky=W)
    
    dict_out = {}
    for f in list_input_files:
        r += 1
        dict_out[f] = {}
        dict_out[f]['IntVar'] = IntVar()
        Ch = Checkbutton(Fr,
                    text=os.path.basename(f),
                    variable=dict_out[f]['IntVar'])
        Ch.grid(row=r, column=0, sticky=W)
        dict_out[f]['nbFA'] = StringVar()
        En = Entry(Fr, textvariable=dict_out[f]['nbFA'])
        En.grid(row=r, column=1, sticky=W)
        dict_out[f]['FAmass'] = StringVar()
        En = Entry(Fr, textvariable=dict_out[f]['FAmass'])
        En.grid(row=r, column=2, sticky=W)
    
    r += 1
    La = Label(Fr, text=120*"-")
    La.grid(row=r, column=0, columnspan=4, sticky=W)
    
    r += 1
    La = Label(Fr, text="Information for decay power generation:")
    La.grid(row=r, columnspan=3, column=0, sticky=W)
    
    r += 1
    La = Label(Fr, text="Core total thermal power (MW)")
    La.grid(row=r, column=0, sticky=W)
    core_power = StringVar()
    En = Entry(Fr, textvariable=core_power)
    En.grid(row=r, column=1, sticky=W)
    
    r += 1
    mox = IntVar()
    Ch = Checkbutton(Fr, text="The fuel contains MOX", variable=mox)
    Ch.grid(row=r, columnspan=3, sticky=W)
    
    r += 1
    La = Label(Fr, text="Suffix for the decay power results file name:")
    La.grid(row=r, column=0, sticky=W)
    dec_suffix = StringVar()
    En = Entry(Fr, textvariable=dec_suffix)
    En.grid(row=r, column=1, sticky=W)
    
    r += 1
    La = Label(Fr, text=120*"-")
    La.grid(row=r, column=0, columnspan=4, sticky=W)
    
    r += 1
    La = Label(Fr, text="Information for source terms generation:")
    La.grid(row=r, columnspan=3, column=0, sticky=W)
    
    r += 1
    La = Label(Fr, text="Source terms are needed in:")
    La.grid(row=r, columnspan=2, column=0)
    
    r += 1
    elements_needed = IntVar() 
    Ch = Checkbutton(Fr, text='Elements', variable=elements_needed)
    Ch.grid(row=r, column=0, sticky=W)
    
    isotopes_needed = IntVar()
    Ch = Checkbutton(Fr, text='Isotopes', variable=isotopes_needed)
    Ch.grid(row=r, column=1, sticky=W)
    
    r += 1
    La = Label(Fr, text="For the following units:")
    La.grid(row=r, columnspan=2, column=0)
    
    r += 1
    u_tW = IntVar()
    u_gW = IntVar()
    u_g = IntVar()
    u_bq = IntVar()
    Ch = Checkbutton(Fr, text='Grams', variable=u_g)
    Ch.grid(row=r, column=0, sticky=W)
    Ch = Checkbutton(Fr, text='Becquerel', variable=u_bq)
    Ch.grid(row=r, column=1, sticky=W)
    Ch = Checkbutton(Fr, text='Watts (total)', variable=u_tW)
    Ch.grid(row=r, column=2, sticky=W)
    Ch = Checkbutton(Fr,  text='Watts (gamma)', variable=u_gW)
    Ch.grid(row=r, column=3, sticky=W)
    
    r += 1
    La = Label(Fr, text="Suffix for the source terms results file name:")
    La.grid(row=r, column=0, sticky=W)
    inv_suffix = StringVar()
    En = Entry(Fr, textvariable=inv_suffix)
    En.grid(row=r, column=1, sticky=W)
    
    r += 1
    La = Label(Fr, text=120*"-")
    La.grid(row=r, column=0, columnspan=4, sticky=W)
    
    r += 1
    Bu = Button(Fr, text='Next', command=root.destroy)
    Bu.grid(row=r, column=3, columnspan=2, sticky=W)
    
    Ca.create_window(0, 0,  window=Fr)
    Fr.update_idletasks()
    Ca.config(scrollregion=Ca.bbox("all"))
    
    root.mainloop()
    
    # End of the first interface.
    ##########################################################################################
    # General data gathering.
    
    if choice1.get() == 0 and choice2.get() == 0:
        print "Unable to continue, you need to select at least one task to perform."
        sys.exit(0)
        
    list_OrigensOut_names = []
    n_FA_batch = []
    FA_mass = []
    
    nb_files_selected = 0
    for f in list_input_files:
        try:
            if dict_out[f]['IntVar'].get() == 1:
                nb_files_selected += 1
                list_OrigensOut_names.append(os.path.basename(f))
                n_FA_batch.append(float(dict_out[f]['nbFA'].get()))
                FA_mass.append(float(dict_out[f]['FAmass'].get()))
        except ValueError:
            print "Unable to continue: you need to fill in the blanks!"
            sys.exit(0)
    
    info = []
    info.append(list_OrigensOut_names)
    info.append(FA_mass)
    info.append(n_FA_batch)
    list_loc = []
    
    for f in list_OrigensOut_names:
        list_loc.append(loc_input+'/'+f)
    info.append(list_loc)
    
    df_info = pd.DataFrame(info,
                          index=['File name', 'FA mass (tons)',
                                 'Number of FA', 'File location'])
    df_info = df_info.T.groupby(['File name']).sum()
    
    if nb_files_selected == 0:
        print "Unable to continue: you need to select at least one file."
        sys.exit(0)
    
    # End of general data gathering.
    ##########################################################################################
    # Choice 1: Decay power generation chosen by the user.
 
    if choice1.get() == 1:
        list_batch_df = []
        try:
            core_power = float(core_power.get())
        except ValueError:
            print "Unable to continue: the core thermal power is not a number."
            sys.exit(0)
        mox = mox.get()
        
        for file_name in list_OrigensOut_names:
            list_batch_df.append(create_df_decay_power('../Input/'+file_name, factors_time))
        
        df_total = gather_df(list_batch_df,            FA_mass,
                             n_FA_batch,               list_OrigensOut_names,
                             core_power,               mox,
                             act_u9_np9_uncertainty,   u9_np9_uncertainty,
                             fp_uncertainty,           fuel_uncertainty,
                             factors_time)
        
        # Check if the source terms folder exists in ../Output. If not, it is created.    
        fdec = "../Output/Decay_power_curve"
        if (os.path.exists(fdec) == 0) or (os.path.exists(fdec) == 1 and os.path.isdir(fdec) == 0):
            print "Creation of {}".format(fdec)
            os.mkdir(fdec)
            
        file_name = "../Output/Decay_power_curve/Decay_power_curve_"
        file_name += dec_suffix.get() + ".xlsx"
        writer = pd.ExcelWriter(file_name)
        df_info.to_excel(writer, "Data")
        df_total.to_excel(writer, "Results")
        writer.save()
    
    # Other choice.
    ##########################################################################################
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
        for file_name in list_OrigensOut_names:
            list_batch_df.append(create_df_inventories('../Input/'+file_name,
                                                       list_units,
                                                       list_categories,
                                                       factors_time))
        t1 = time.time()
        print "Time for create_df_inventories: {} sec.".format(round(t1-t0, 1))
        
        dinv = {}
        for c in list_categories:
            dinv[c] = {}
            for u in list_units:
                dinv[c][u] = list_batch_df[0][c][u]
                dinv[c][u] = dinv[c][u]*FA_mass[0]*n_FA_batch[0]
                for i, d in enumerate(list_batch_df[1:]):
                    dinv[c][u] = dinv[c][u].add(d[c][u]*FA_mass[i+1]*n_FA_batch[i+1],
                                             fill_value=0)
         
        t2 = time.time()
        print "Time for assembling dataframes: {} sec.".format(round(t2-t1, 1))
        # Second interface for the user choice of time steps.
        l = dinv[list_categories[0]][list_units[0]].columns
        time_steps = sorted(l, key=lambda x: convert_str_sec(x, factors_time))
        
        root = Tk()
        root.title('Post_ORIGEN-S: available time steps')
        
        # Create vertical and horizontal Scrollbars
        SbV = Scrollbar(root, orient=VERTICAL)
        SbV.grid(row=0, column=1, sticky=N+S)
        SbH = Scrollbar(root, orient=HORIZONTAL)
        SbH.grid(row=1, column=0, sticky=E+W)

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
            Ch.grid(row=r, column=c, sticky=W)
        
        def select_all():
            for k in dict_IntVar.keys():
                dict_IntVar[k].set(1)
        def unselect_all():
            for k in dict_IntVar.keys():
                dict_IntVar[k].set(0)
        
        Bu = Button(Fr, text='Next', command=root.destroy)
        Bu.grid(row=24, column=5, sticky=W)
        
        Bu = Button(Fr, text='Select all', command=select_all)
        Bu.grid(row=24, column=1, sticky=W)
        
        Bu = Button(Fr, text='Unselect all', command=unselect_all)
        Bu.grid(row=24, column=3, sticky=W)
        
        Ca.create_window(0, 0,  window=Fr)
        Fr.update_idletasks()
        Ca.config(scrollregion=Ca.bbox("all"))                                                          
        
        root.mainloop()
        
        # End of the second interface.
        ##########################################################################################
        # Chosen time steps for inventories gathering.
        
        time_steps = get_state_IntVar(dict_IntVar, factors_time)                                                          
        
        for c in list_categories:
            u_tmp = dinv[c].keys()[0]
            dict_grp_noe = get_dict_group_noe(dinv[c][u_tmp])
            dict_IntVar = {}
            
            root = Tk()
            t = "Source terms generation: available " + c.lower()
            root.title(t)
            
            # Create vertical and horizontal Scrollbars
            SbV = Scrollbar(root, orient=VERTICAL)
            SbV.grid(row=0, column=1, sticky=N+S)
            SbH = Scrollbar(root, orient=HORIZONTAL)
            SbH.grid(row=1, column=0, sticky=E+W)
    
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
                La.grid(row=1,column=5*i,columnspan=3,sticky=W)
                
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
                    Ch.grid(row=ro, column=co+5*i, sticky=W)
                
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
            Bu.grid(row=42, column=0, sticky=W)
            t = "Unselect all "+c.lower()
            Bu = Button(Fr, text=t, command=unselect_all)
            Bu.grid(row=43, column=0, sticky=W)
            
            if 'Actinides' in dict_IntVar.keys():
                t = "Select all actinides"
                Bu = Button(Fr, text=t, command=select_all_act)
                Bu.grid(row=42, column=1, sticky=W)
                t = "Unselect all actinides"
                Bu = Button(Fr, text=t, command=unselect_all_act)
                Bu.grid(row=43, column=1, sticky=W)
                
            if 'Fission products' in dict_IntVar.keys():
                t = "Select all fission products"
                Bu = Button(Fr, text=t, command=select_all_fp)
                Bu.grid(row=42, column=2, sticky=W)
                t = "Unselect all fission products"
                Bu = Button(Fr, text=t, command=unselect_all_fp)
                Bu.grid(row=43, column=2, sticky=W)
            
            if 'Light elements' in dict_IntVar.keys():
                t = "Select all light elements"
                Bu = Button(Fr, text=t, command=select_all_le)
                Bu.grid(row=42, column=3, sticky=W)
                t = "Unselect all light elements"
                Bu = Button(Fr, text=t, command=unselect_all_le)
                Bu.grid(row=43, column=3, sticky=W)

            Bu = Button(Fr, text='Next', command=root.destroy)
            Bu.grid(row=45, column=5, sticky=W)
            
            Ca.create_window(0, 0,  window=Fr)
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
            
            # Check if the source terms folder exists in ../Output. If not, it is created.    
            finv = "../Output/Source_terms"
            if (os.path.exists(finv) == 0) or (os.path.exists(finv) == 1 and os.path.isdir(finv) == 0):
                print "Creation of {}".format(finv)
                os.mkdir(finv)
                        
            inv_loc = "../Output/Source_terms/Inventories_"+c.lower()
            inv_loc += "_"+inv_suffix.get()+".xlsx"
            writer = pd.ExcelWriter(inv_loc)
            
            for u in dinv[c].keys():
                dinv[c][u] = dinv[c][u].reindex(index=list_index, columns=time_steps)
                name = dict_unit[u].title()
                dinv[c][u].to_excel(writer, name)
            df_info.to_excel(writer, "Data")
        
        writer.save()  
