# TO BE USED WITH PYTHON V2.7
# -*- coding: iso-8859-1 -*-
# -*- encoding: iso8859-1 -*-
# Author: theo43@github

import pickle, re, sys, os, glob, shutil, time
import matplotlib.pyplot as plt
import pandas as pd
from functions import *
import Tkinter as tk

if __name__ == '__main__':
    
    # Check if 'Input' folder exists
    if os.path.isdir("Input"):
        list_input_files = [n for n in glob.glob("Input/*.out")]
        if list_input_files == []:
            msg = os.getcwd()+"/Input does not contain any \".out\" file."
            print(msg)
            sys.exit(0)
    if not os.path.exists("Input"):
        msg = "The output files you want to post-treat need to be placed in "
        msg += "the folder at the following location: "+os.getcwd()+"/Input."
        os.mkdir("Input")
        msg += "\nThe \"Input\" folder is now created. Please fill it in with "
        msg += "your files and re-run the tool."
        print(msg)
        sys.exit(0)
    
    # Also check if 'Output' folder exists. If not, creat it
    if not os.path.exists("Output"):
        os.mkdir("Output")
        msg = os.getcwd()+"/Output folder does not exist.\nCreation of "
        msg += "this folder, where your resulting files will be located."
        print(msg)
    
    ##########################################################################

    root = tk.Tk()
    root.title('MAIN')
    
    # Create vertical and horizontal Scrollbars
    SbV = tk.Scrollbar(root, orient='vertical')
    SbV.grid(row=0, column=1, sticky='n'+'s')
    SbH = tk.Scrollbar(root, orient='horizontal')
    SbH.grid(row=1, column=0, sticky='E'+'W')
    
    # Create a canvas
    Ca = tk.Canvas(root, yscrollcommand=SbV.set, xscrollcommand=SbH.set)
    Ca.grid(row=0, column=0, sticky="news")
    
    # Configure the Scrollbars on the Canvas
    SbV.config(command=Ca.yview)
    SbH.config(command=Ca.xview)
    
    # Configure row index of a grid
    root.grid_rowconfigure(0, weight=1)
    # Configure column index of a grid
    root.grid_columnconfigure(0, weight=1)
    
    # Create a frame on the canvas
    Fr = tk.Frame(Ca)
      
    # Add widgets
    r = 0
    La = tk.Label(Fr, text="Welcome!")
    La.grid(row=r, columnspan=4)
    
    r += 1
    La = tk.Label(Fr, text=190*"-")
    La.grid(row=r, column=0, columnspan=4, sticky='w')
    
    r += 1
    La = tk.Label(Fr, text="What do you want to generate?")
    La.grid(row=r, columnspan=4, sticky='w')
    
    r += 1
    choice1 = tk.IntVar()
    Ch = tk.Checkbutton(Fr, text="Decay power curve",
                        variable=choice1)
    Ch.grid(row=r, column=0, sticky='w')
    
    r += 1
    choice2 = tk.IntVar()
    Ch = tk.Checkbutton(Fr, text="Source terms inventories",
                     variable=choice2)
    Ch.grid(row=r, column=0, sticky='w')
    
    r += 1
    La = tk.Label(Fr, text=190*"-")
    La.grid(row=r, column=0, columnspan=4, sticky='w')
    
    r += 1
    t = "Select the output files to post-treat "
    t += "and fill-in the required data"
    La = tk.Label(Fr, text=t)
    La.grid(row=r, columnspan=4, sticky='w')
    
    r += 1
    loc_input = os.path.dirname(os.getcwd())+'/Input'
    t = "Available \".out\" files in {}:".format(loc_input)
    La = tk.Label(Fr, text=t)
    La.grid(row=r, columnspan=4, sticky='w')
    
    r += 1
    La = tk.Label(Fr, text="Files names")
    La.grid(row=r, column=0)
    La = tk.Label(Fr, text="Number of FA")
    La.grid(row=r, column=1, sticky='w')
    La = tk.Label(Fr, text="FA mass (tons)")
    La.grid(row=r, column=2, sticky='w')
    
    dict_out = {}
    for f in sorted(list_input_files):
        r += 1
        dict_out[f] = {}
        dict_out[f]['IntVar'] = tk.IntVar()
        Ch = tk.Checkbutton(Fr,
                    text=os.path.basename(f),
                    variable=dict_out[f]['IntVar'])
        Ch.grid(row=r, column=0, sticky='w')
        dict_out[f]['nbFA'] = tk.StringVar()
        En = tk.Entry(Fr, textvariable=dict_out[f]['nbFA'])
        En.grid(row=r, column=1, sticky='w')
        dict_out[f]['FAmass'] = tk.StringVar()
        En = tk.Entry(Fr, textvariable=dict_out[f]['FAmass'])
        En.grid(row=r, column=2, sticky='w')
    
    r += 1
    La = tk.Label(Fr, text=190*"-")
    La.grid(row=r, column=0, columnspan=4, sticky='w')
    
    r += 1
    La = tk.Label(Fr, text="Information for power curve generation:")
    La.grid(row=r, columnspan=3, column=0, sticky='w')
    
    r += 1
    La = tk.Label(Fr, text="Total thermal power (MW)")
    La.grid(row=r, column=0, sticky='w')
    core_power = tk.StringVar()
    En = tk.Entry(Fr, textvariable=core_power)
    En.grid(row=r, column=1, sticky='w')
    
    r += 1
    mox = tk.IntVar()
    Ch = tk.Checkbutton(Fr, text="The fuel contains MOX", variable=mox)
    Ch.grid(row=r, columnspan=3, sticky='w')
    
    r += 1
    La = tk.Label(Fr, text="Suffix for the decay power results file name:")
    La.grid(row=r, column=0, sticky='w')
    dec_suffix = tk.StringVar()
    En = tk.Entry(Fr, textvariable=dec_suffix)
    En.grid(row=r, column=1, sticky='w')
    
    r += 1
    La = tk.Label(Fr, text=190*"-")
    La.grid(row=r, column=0, columnspan=4, sticky='w')
    
    r += 1
    La = tk.Label(Fr, text="Information for source terms generation:")
    La.grid(row=r, columnspan=3, column=0, sticky='w')
    
    r += 1
    La = tk.Label(Fr, text="Source terms are needed in:")
    La.grid(row=r, columnspan=2, column=0)
    
    r += 1
    elements_needed = tk.IntVar() 
    Ch = tk.Checkbutton(Fr, text='Elements', variable=elements_needed)
    Ch.grid(row=r, column=0, sticky='w')
    
    isotopes_needed = tk.IntVar()
    Ch = tk.Checkbutton(Fr, text='Isotopes', variable=isotopes_needed)
    Ch.grid(row=r, column=1, sticky='w')
    
    r += 1
    La = tk.Label(Fr, text="For the following units:")
    La.grid(row=r, columnspan=2, column=0)
    
    r += 1
    u_tW = tk.IntVar()
    u_gW = tk.IntVar()
    u_g = tk.IntVar()
    u_bq = tk.IntVar()
    Ch = tk.Checkbutton(Fr, text='Grams', variable=u_g)
    Ch.grid(row=r, column=0, sticky='w')
    Ch = tk.Checkbutton(Fr, text='Becquerel', variable=u_bq)
    Ch.grid(row=r, column=1, sticky='w')
    Ch = tk.Checkbutton(Fr, text='Watts (total)', variable=u_tW)
    Ch.grid(row=r, column=2, sticky='w')
    Ch = tk.Checkbutton(Fr,  text='Watts (gamma)', variable=u_gW)
    Ch.grid(row=r, column=3, sticky='w')
    
    r += 1
    La = tk.Label(Fr, text="Suffix for the source terms results file name:")
    La.grid(row=r, column=0, sticky='w')
    inv_suffix = tk.StringVar()
    En = tk.Entry(Fr, textvariable=inv_suffix)
    En.grid(row=r, column=1, sticky='w')
    
    r += 1
    La = tk.Label(Fr, text=190*"-")
    La.grid(row=r, column=0, columnspan=4, sticky='w')
    
    r += 1
    Bu = tk.Button(Fr, text='Next', command=root.destroy)
    Bu.grid(row=r, column=3, columnspan=2, sticky='w')
    
    Ca.create_window(0, 0,  window=Fr)
    Fr.update_idletasks()
    Ca.config(scrollregion=Ca.bbox("all"))
    
    root.mainloop()
    
    # End of the first interface.
    ##########################################################################
    # General data gathering.
    
    if choice1.get() == 0 and choice2.get() == 0:
        msg = "Unable to continue, you need to select at least one task"
        msg += " to perform."
        print(msg)
        sys.exit(0)
        
    list_files_post = []
    n_FA_batch = []
    FA_mass = []
    
    nb_files_selected = 0
    for f in list_input_files:
        try:
            if dict_out[f]['IntVar'].get() == 1:
                nb_files_selected += 1
                list_files_post.append(os.path.basename(f))
                n_FA_batch.append(float(dict_out[f]['nbFA'].get()))
                FA_mass.append(float(dict_out[f]['FAmass'].get()))
        except ValueError:
            print("Unable to continue: you need to fill in the blanks!")
            sys.exit(0)
    
    info = []
    info.append(list_files_post)
    info.append(FA_mass)
    info.append(n_FA_batch)
    list_loc = []
    
    for f in list_files_post:
        list_loc.append(loc_input+'/'+f)
    info.append(list_loc)
    
    df_info = pd.DataFrame(info,
                          index=['File name', 'FA mass (tons)',
                                 'Number of FA', 'File location'])
    df_info = df_info.T.groupby(['File name']).sum()
    
    if nb_files_selected == 0:
        print("Unable to continue: you need to select at least one file.")
        sys.exit(0)
    
    # End of general data gathering.
    ##########################################################################
    # Choice 1: Decay power generation chosen by the user.
 
    if choice1.get() == 1:
        list_batch_df = []
        try:
            core_power = float(core_power.get())
        except ValueError:
            print("Unable to continue: the thermal power is not a number.")
            sys.exit(0)
        mox = mox.get()
        
        for file_name in list_files_post:
            list_batch_df.append(create_df_decay_power('Input/'+file_name, 
                                                       factors_time,
                                                       regex_time,
                                                       regex_category,
                                                       reg_categ_unit))
        
        df_total = gather_df(list_batch_df,            FA_mass,
                             n_FA_batch,               list_files_post,
                             core_power,               mox,
                             act_u9_np9_uncertainty,   u9_np9_uncertainty,
                             fp_uncertainty,           fuel_uncertainty,
                             factors_time)
        
        # Check if the source terms folder exists in Output/
        # If not, it is created.    
        fdec = "Output/Decay_power_curve"
        if (os.path.exists(fdec) == 0) or \
           (os.path.exists(fdec) == 1 and os.path.isdir(fdec) == 0):
            print("Creation of {}".format(fdec))
            os.mkdir(fdec)
            
        file_name = "Output/Decay_power_curve/Decay_power_curve_"
        file_name += dec_suffix.get() + ".xlsx"
        writer = pd.ExcelWriter(file_name)
        df_info.to_excel(writer, "Data")
        df_total.to_excel(writer, "Results")
        writer.save()
        
        # Plotting of the decay power curves
        df_total = df_total.reset_index()
        df_total = df_total.set_index(['Time steps [s]'])
        df_total = df_total.drop(['Time steps', 'Sigma value [%]'], axis=1)
        ax = df_total.plot(logx=1, logy=0, title='Decay power curves', grid=1)
        ax.set_xlabel('Decay time [s]')
        ax.set_ylabel('Decay power [% FP]')
        plt.show()
    
    # Other choice.
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
        for file_name in list_files_post:
            list_batch_df.append(create_df_inventories('Input/'+file_name,
                                                       list_units,
                                                       list_categories,
                                                       factors_time,
                                                       regex_time,
                                                       regex_category,
                                                       reg_categ_unit,
                                                       reg_after_Decay))
        t1 = time.time()
        print("Time for create_df_inventories: {} sec.".format(round(t1-t0,1)))
        
        dinv = {}
        for c in list_categories:
            dinv[c] = {}
            for u in list_units:
                dinv[c][u] = list_batch_df[0][c][u]
                dinv[c][u] = dinv[c][u]*FA_mass[0]*n_FA_batch[0]
                for i, d in enumerate(list_batch_df[1:]):
                    dinv[c][u] = dinv[c][u].add(d[c][u]*FA_mass[i+1]*\
                                                n_FA_batch[i+1], fill_value=0)
         
        t2 = time.time()
        print("Time for assembling dataframes: {} sec.".format(round(t2-t1,1)))
        
         # Second interface for the user choice of time steps.
        l = dinv[list_categories[0]][list_units[0]].columns
        time_steps = sorted(l, key=lambda x: convert_str_sec(x, factors_time))
        
        root = tk.Tk()
        root.title('Available time steps')
        
        # Create vertical and horizontal Scrollbars
        SbV = tk.Scrollbar(root, orient='vertical')
        SbV.grid(row=0, column=1, sticky='N'+'S')
        SbH = tk.Scrollbar(root, orient='horizontal')
        SbH.grid(row=1, column=0, sticky='E'+'W')

        # Create a canvas
        Ca = tk.Canvas(root, yscrollcommand=SbV.set, xscrollcommand=SbH.set)
        Ca.grid(row=0, column=0, sticky="news")

        # Configure the Scrollbars on the Canvas
        SbV.config(command=Ca.yview)
        SbH.config(command=Ca.xview)

        # Configure row index of a grid
        root.grid_rowconfigure(0, weight=1)
        # Configure column index of a grid
        root.grid_columnconfigure(0, weight=1)

        # Create a frame on the canvas
        Fr = tk.Frame(Ca)
        
        La = tk.Label(Fr, text="Choose your time steps:")
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
            dict_IntVar[ts] = tk.IntVar()
            Ch = tk.Checkbutton(Fr, text=ts, variable=dict_IntVar[ts])
            Ch.grid(row=r, column=c, sticky='w')
        
        def select_all():
            for k in dict_IntVar.keys():
                dict_IntVar[k].set(1)
        def unselect_all():
            for k in dict_IntVar.keys():
                dict_IntVar[k].set(0)
        
        Bu = tk.Button(Fr, text='Next', command=root.destroy)
        Bu.grid(row=24, column=5, sticky='w')
        
        Bu = tk.Button(Fr, text='Select all', command=select_all)
        Bu.grid(row=24, column=1, sticky='w')
        
        Bu = tk.Button(Fr, text='Unselect all', command=unselect_all)
        Bu.grid(row=24, column=3, sticky='w')
        
        Ca.create_window(0, 0,  window=Fr)
        Fr.update_idletasks()
        Ca.config(scrollregion=Ca.bbox("all"))                                                          
        
        root.mainloop()
        
        # End of the second interface.
        ######################################################################
        # Chosen time steps for inventories gathering.
        
        time_steps = get_state_IntVar(dict_IntVar, factors_time)                                                          
        
        for c in list_categories:
            u_tmp = dinv[c].keys()[0]
            dict_grp_noe = get_dict_group_noe(dinv[c][u_tmp])
            dict_IntVar = {}
            
            root = tk.Tk()
            t = "Source terms generation: available " + c.lower()
            root.title(t)
            
            # Create vertical and horizontal Scrollbars
            SbV = tk.Scrollbar(root, orient='vertical')
            SbV.grid(row=0, column=1, sticky='N'+'S')
            SbH = tk.Scrollbar(root, orient='horizontal')
            SbH.grid(row=1, column=0, sticky='E'+'W')
    
            # Create a canvas
            Ca = tk.Canvas(root, yscrollcommand=SbV.set,xscrollcommand=SbH.set)
            Ca.grid(row=0, column=0, sticky="news")
    
            # Configure the Scrollbars on the Canvas
            SbV.config(command=Ca.yview)
            SbH.config(command=Ca.xview)
    
            # Configure row index of a grid
            root.grid_rowconfigure(0, weight=1)
            # Configure column index of a grid
            root.grid_columnconfigure(0, weight=1)
    
            # Create a frame on the canvas
            Fr = tk.Frame(Ca)
    
            La = tk.Label(Fr, text="Choose your {}:".format(c.lower()))
            La.grid(row=0, columnspan=15)
            
            i = 0
            for g in sorted(dict_grp_noe.keys()):
                if g not in dict_IntVar.keys():
                    dict_IntVar[g] = {}
                    
                La = tk.Label(Fr, text=g)
                La.grid(row=1,column=5*i,columnspan=3,sticky='w')
                
                (ro, co) = (1, 0)
                
                for noe in sorted(dict_grp_noe[g]):
                    if ro <= 40:
                        ro += 1
                    else:
                        ro = 2
                        co += 1
                
                    dict_IntVar[g][noe] = tk.IntVar()
                    Ch = tk.Checkbutton(Fr, text=noe.title(),
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
            Bu = tk.Button(Fr, text=t, command=select_all)
            Bu.grid(row=42, column=0, sticky='w')
            t = "Unselect all "+c.lower()
            Bu = tk.Button(Fr, text=t, command=unselect_all)
            Bu.grid(row=43, column=0, sticky='w')
            
            if 'Actinides' in dict_IntVar.keys():
                t = "Select all actinides"
                Bu = tk.Button(Fr, text=t, command=select_all_act)
                Bu.grid(row=42, column=1, sticky='w')
                t = "Unselect all actinides"
                Bu = tk.Button(Fr, text=t, command=unselect_all_act)
                Bu.grid(row=43, column=1, sticky='w')
                
            if 'Fission products' in dict_IntVar.keys():
                t = "Select all fission products"
                Bu = tk.Button(Fr, text=t, command=select_all_fp)
                Bu.grid(row=42, column=2, sticky='w')
                t = "Unselect all fission products"
                Bu = tk.Button(Fr, text=t, command=unselect_all_fp)
                Bu.grid(row=43, column=2, sticky='w')
            
            if 'Light elements' in dict_IntVar.keys():
                t = "Select all light elements"
                Bu = tk.Button(Fr, text=t, command=select_all_le)
                Bu.grid(row=42, column=3, sticky='w')
                t = "Unselect all light elements"
                Bu = tk.Button(Fr, text=t, command=unselect_all_le)
                Bu.grid(row=43, column=3, sticky='w')

            Bu = tk.Button(Fr, text='Next', command=root.destroy)
            Bu.grid(row=45, column=5, sticky='w')
            
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
            
            # Check if the source terms folder exists in Output/
            # If not, it is created.    
            finv = "Output/Source_terms"
            if (os.path.exists(finv) == 0) or (os.path.exists(finv) == 1 and
                                               os.path.isdir(finv) == 0):
                print("Creation of {}".format(finv))
                os.mkdir(finv)
                        
            inv_loc = "Output/Source_terms/Inventories_"+c.lower()
            inv_loc += "_"+inv_suffix.get()+".xlsx"
            writer = pd.ExcelWriter(inv_loc)
            
            for u in dinv[c].keys():
                dinv[c][u] = dinv[c][u].reindex(index=list_index,
                                                columns=time_steps)
                name = dict_unit[u].title()
                dinv[c][u].to_excel(writer, name)
            df_info.to_excel(writer, "Data")
        
        writer.save()  
