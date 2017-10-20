#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: theo43@github
date: Sept. 2017
POS: classes
"""
import tkinter as tk
from tkinter import ttk
import os.path


class Multipage(tk.Tk):
    """
    """

    def __init__(self, *args, **kwargs):
        print("args: ",args)
        tk.Tk.__init__(self)
        tk.Tk.wm_title(self, "POS")
        
        # Create vertical and horizontal Scrollbars
        SbV = tk.Scrollbar(self, orient='vertical')
        SbV.grid(row=0, column=1, sticky='n'+'s')
        SbH = tk.Scrollbar(self, orient='horizontal')
        SbH.grid(row=1, column=0, sticky='e'+'w')
        
        # Create a canvas (in order to make scrollbars work)
        Ca = tk.Canvas(self, yscrollcommand=SbV.set, xscrollcommand=SbH.set)
        Ca.grid(row=0, column=0, sticky="news")
        
        # Configure the Scrollbars on the Canvas
        SbV.config(command=Ca.yview)
        SbH.config(command=Ca.xview)
        
        # Configure row index of a grid
        self.grid_rowconfigure(0, weight=1)
        # Configure column index of a grid
        self.grid_columnconfigure(0, weight=1)
        
        # Create a frame on the canvas (himself on the Tk == self) 
        container = tk.Frame(Ca)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        self.frames = {}
        
        for F in args:
            frame = F(container, self, **kwargs)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        
        self.show_frame(args[0])
        
    def show_frame(self, container):
        """
        """
        frame = self.frames[container]
        frame.tkraise()


class UserData(tk.Frame):
    """
    """
    
    def __init__(self, parent, controller, **kwargs):
        tk.Frame.__init__(self, parent)
        self.dict_out = {}
        
        r = 0
        txt = ("Files to select and corresponding data "
               "gathering")
        label = tk.Label(self, text=txt, font=kwargs['font'])
        label.grid(row=r, columnspan=4, sticky='w')
        
        r += 1
        La = tk.Label(self, text=190*"-")
        La.grid(row=r, column=0, columnspan=4, sticky='w')

        r += 1
        La = tk.Label(self, text="What do you want to generate?")
        La.grid(row=r, columnspan=4, sticky='w')

        r += 1
        self.choice1 = tk.IntVar()
        Ch = tk.Checkbutton(self, text="Decay power curve",
                            variable=self.choice1)
        Ch.grid(row=r, column=0, sticky='w')

        r += 1
        self.choice2 = tk.IntVar()
        Ch = tk.Checkbutton(self, text="Source terms inventories",
                            variable=self.choice2)
        Ch.grid(row=r, column=0, sticky='w')

        r += 1
        La = tk.Label(self, text=190*"-")
        La.grid(row=r, column=0, columnspan=4, sticky='w')

        r += 1
        txt = ""
        label = tk.Label(self, text=txt)
        label.grid(row=r)
        
        r += 1
        txt = ("Select the output files to post-treat and fill-in the "
               "corresponding required data")
        La = tk.Label(self, text=txt)
        La.grid(row=r, columnspan=4, sticky='w')
        #La.pack()

        r += 1
        txt = "Available \".out\" files in {}:".format(kwargs['location'])
        La = tk.Label(self, text=txt)
        La.grid(row=r, columnspan=4, sticky='w')
        #La.pack()
                
        r += 1
        La = tk.Label(self, text="Files names")
        La.grid(row=r, column=0, sticky='w')
        La = tk.Label(self, text="Number of FA")
        La.grid(row=r, column=1, sticky='w')
        La = tk.Label(self, text="FA mass (tons)")
        La.grid(row=r, column=2, sticky='w')
        
        
        for f in sorted(kwargs['list_in_files']):
            r += 1
            self.dict_out[f] = {}
            self.dict_out[f]['IntVar'] = tk.IntVar()
            Ch = tk.Checkbutton(self,
                                text=os.path.basename(f),
                                variable=self.dict_out[f]['IntVar'])
            Ch.grid(row=r, column=0, sticky='w')
            self.dict_out[f]['nbFA'] = tk.StringVar()
            En = tk.Entry(self, textvariable=self.dict_out[f]['nbFA'])
            En.grid(row=r, column=1, sticky='w')
            self.dict_out[f]['FAmass'] = tk.StringVar()
            En = tk.Entry(self, textvariable=self.dict_out[f]['FAmass'])
            En.grid(row=r, column=2, sticky='w')
  
        r += 1
        La = tk.Label(self, text=190*"-")
        La.grid(row=r, column=0, columnspan=4, sticky='w')

        r += 1
        La = tk.Label(self, text="Information for power curve generation:")
        La.grid(row=r, columnspan=3, column=0, sticky='w')

        r += 1
        La = tk.Label(self, text="Total thermal power (MW)")
        La.grid(row=r, column=0, sticky='w')
        self.core_power = tk.StringVar()
        En = tk.Entry(self, textvariable=self.core_power)
        En.grid(row=r, column=1, sticky='w')
    
        r += 1
        self.mox = tk.IntVar()
        Ch = tk.Checkbutton(self, text="The fuel contains MOX",
                            variable=self.mox)
        Ch.grid(row=r, columnspan=3, sticky='w')
    
        r += 1
        t = ("Suffix for the result file:\n"
             "(\"Decay_power_curve_<suffix>.xlsx\")")
        La = tk.Label(self, text=t)
        La.grid(row=r, column=0, sticky='w')
        self.dec_suffix = tk.StringVar()
        En = tk.Entry(self, textvariable=self.dec_suffix)
        En.grid(row=r, column=1, sticky='w')
    
        r += 1
        La = tk.Label(self, text=190*"-")
        La.grid(row=r, column=0, columnspan=4, sticky='w')
    
        r += 1
        La = tk.Label(self, text="Information for source terms generation:")
        La.grid(row=r, columnspan=3, column=0, sticky='w')
    
        r += 1
        La = tk.Label(self, text="Source terms are needed in:")
        La.grid(row=r, columnspan=2, column=0)
    
        r += 1
        self.elements_needed = tk.IntVar()
        Ch = tk.Checkbutton(self, text='Elements',
                            variable=self.elements_needed)
        Ch.grid(row=r, column=0, sticky='w')
    
        self.isotopes_needed = tk.IntVar()
        Ch = tk.Checkbutton(self, text='Isotopes',
                            variable=self.isotopes_needed)
        Ch.grid(row=r, column=1, sticky='w')

        r += 1
        La = tk.Label(self, text="For the following units:")
        La.grid(row=r, columnspan=2, column=0)
    
        r += 1
        self.u_tW = tk.IntVar()
        self.u_gW = tk.IntVar()
        self.u_g = tk.IntVar()
        self.u_bq = tk.IntVar()
        Ch = tk.Checkbutton(self, text='Grams', variable=self.u_g)
        Ch.grid(row=r, column=0, sticky='w')
        Ch = tk.Checkbutton(self, text='Becquerel', variable=self.u_bq)
        Ch.grid(row=r, column=1, sticky='w')
        Ch = tk.Checkbutton(self, text='Watts (total)', variable=self.u_tW)
        Ch.grid(row=r, column=2, sticky='w')
        Ch = tk.Checkbutton(self, text='Watts (gamma)', variable=self.u_gW)
        Ch.grid(row=r, column=3, sticky='w')
    
        r += 1
        t = ("Suffix for the result file:\n"
             "(\"Source_terms_<category>_<suffix>.xlsx\")")
        La = tk.Label(self, text=t)
        La.grid(row=r, column=0, sticky='w')
        self.inv_suffix = tk.StringVar()
        En = tk.Entry(self, textvariable=self.inv_suffix)
        En.grid(row=r, column=1, sticky='w')
    
        r += 1
        La = tk.Label(self, text=190*"-")
        La.grid(row=r, column=0, columnspan=4, sticky='w')
    
        r += 1
        Bu = tk.Button(self, text='Next', command=controller.destroy)
        Bu.grid(row=r, column=3, columnspan=2, sticky='w')
        
    def return_info(self):
        return self.dict_out
    
    def return_choice(self):
        return self.choice1.get(), self.choice2.get()
    
    def return_mox(self):
        return self.mox.get()
    
    def return_core_power(self):
        return self.core_power.get()
    
    def return_decaypower_suffix(self):
        return self.dec_suffix.get()
    
    def return_inventories_suffix(self):
        return self.inv_suffix.get()
    
    def return_categories(self):
        categ_names = ['Elements', 'Isotopes']
        list_categories = []
        for i, c in enumerate([self.elements_needed, self.isotopes_needed]):
            if c.get() == 1:
                list_categories.append(categ_names[i])
        return list_categories
    
    def return_units(self):
        unit_names = ['g', 'Bq', 'W', 'W_gamma']
        list_units = []
        for i, u in enumerate([self.u_g, self.u_bq, self.u_tW, self.u_gW]):
            if u.get() == 1:
                list_units.append(unit_names[i])
        return list_units
        
