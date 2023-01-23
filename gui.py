#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 22 15:27:56 2023

@author: bsaleem
"""
import tkinter as tk
from tkinter import ttk

class MyGUI:

    def __init__(self):

        self.root = tk.Tk()
        self.root.geometry('1288x760')
        self.root.title('Auth Proxy Log Parser')

        self.topframe = tk.Frame(self.root, width=50,height= 40, bg='#45ba6e')
        self.topframe.pack(fill='x', pady=5)
        self.topframe.grid_propagate(0)

        self.leftframe = tk.Frame(self.root, width=500,height= 500)
        self.leftframe.pack(padx=5,side='left', expand=True, fill='both')

        self.rightframe = tk.Frame(self.root, width=500,height= 500)
        self.rightframe.pack(padx=5,side='left', expand=True, fill='both')


        self.textboxlabel = tk.Label(self.rightframe,text="Output:", font=('Times New Roman', 20)).pack(anchor='nw')


        self.label = tk.Label(self.topframe, text="Duo Security Authentication Proxy Log Parser",bg='#45ba6e', font=('ariel',25))
        self.label.grid(row=30, column=2)

        self.textboxlabel = tk.Label(self.leftframe,text="Search string", font=('Times New Roman', 20)).pack(anchor='nw')

        self.textbox = tk.Entry(self.leftframe, width=50, font=('Times New Roman', 20)).pack(anchor='n',expand=True,fill='x')


        self.outputbox = tk.Text(self.rightframe, width=50, font=('Times New Roman', 20)).pack(expand=True,fill='both')

        self.root.mainloop()


MyGUI()
