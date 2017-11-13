# -*- coding: utf-8 -*-
"""
@author: theo43@github
date: Sept. 2017
POS: page for decay power curve plotting
"""

from page_display_files import DisplayFilesPage
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
                                               NavigationToolbar2TkAgg)
from matplotlib.figure import Figure
from tkinter import Frame, Label, BOTTOM, BOTH, TOP, ttk
from functools import partial

LARGE_FONT = ("Verdana", 12)


class DecayPowerCurvePage(Frame):
    """Plotting of the decay power curves"""

    def __init__(self, parent, controller, *args):
        """Arguments:
               - parent (Frame)
               - controller (Tk)
        """
        super().__init__(parent)
        self.controller = controller
        self.controller.frames[DisplayFilesPage].destroy()
        self.init_UI()

    # Create main GUI window
    def init_UI(self):

        txt = "Decay power curves"
        label = Label(self, text=txt, font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        path_res = self.controller.data.choice['decay']['path_res']
        txt = ("You can save the figure by selecting the saving button at the "
               "bottom of the page.\nDetailed values are provided in the "
               "newly created following file:\n{}".format(path_res))
        label = Label(self, text=txt)
        label.pack()

        # Instanciate the Figure and
        fig = Figure(figsize=(6, 6), dpi=100)
        axe = fig.add_subplot(111)

        # Plot of the decay power curves
        df_total = self.controller.data.choice['decay']['result']
        df_total = df_total.reset_index()
        df_total = df_total.set_index(['Time steps [s]'])
        df_total = df_total.drop(['Time steps', 'Sigma value [%]'], axis=1)
        df_total.plot(logx=1, logy=0, grid=1, ax=axe)
        axe.set_xlabel('Decay time [s]')
        axe.set_ylabel('Decay power [% FP]')

        canvas = FigureCanvasTkAgg(fig, self)
        canvas.show()
        canvas.get_tk_widget().pack(side=BOTTOM, fill=BOTH, expand=True)

        toolbar = NavigationToolbar2TkAgg(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=TOP, fill=BOTH, expand=True)

        txt = "Next"
        cmd = partial(self.controller.check_user_data)
        button = ttk.Button(self, text=txt, command=cmd)
        button.pack()
