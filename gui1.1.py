#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 22 15:27:56 2023
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

        self.leftframe = tk.Frame(self.root, width=500,height= 500)
        self.leftframe.pack(ipady=5,ipadx=5,side='left', expand=True, fill='both')

        self.rightframe = tk.Frame(self.root, width=500,height= 500)
        self.rightframe.pack(ipady=5,ipadx=5,side='left', expand=True, fill='both')


        self.textboxlabel = tk.Label(self.rightframe,text="Output:", font=('Times New Roman', 20)).pack(anchor='nw')

        self.label = tk.Label(self.topframe, text="Duo Security Authentication Proxy Log Parser",bg='#45ba6e', font=('ariel',25))
        self.label.grid(row=30, column=2)

        self.textboxlabel = tk.Label(self.leftframe,text="Search string", font=('Times New Roman', 20)).pack(anchor='nw',padx=5)

        self.textbox = tk.Entry(self.leftframe, width=40, font=('Times New Roman', 20))
        self.textbox.pack(anchor='n',expand=False,fill='x',padx=5)

        #Create a text object box with the appropriate sizing. Set the status to disabled (non-editable)
        self.outputbox = tk.Text(self.rightframe, width=50, font=('Times New Roman', 20), state=tk.DISABLED)

        self.outputbox.insert(1.0,self.textbox.get())
        #Pack the Text object
        self.outputbox.pack(expand=True,fill='both',padx=5)

        #Create quitbutton (Button Object) for the quit button. Assign frame,text, command, and pack it. Best practice is to seperate the packing from the variable (to do)
        self.quitbutton = tk.Button(self.leftframe, text = 'Quit', command = self.root.destroy).pack(side='bottom',anchor='sw',pady=5,padx=5)

        self.show = tk.Button(self.leftframe, text = 'show', command = self.printtextbox).pack(anchor='nw',after=self.textbox,padx=5)
    def printtextbox(self):
        '''Inserts/prints the values entered into textbox into the output box. Changes the status of the outputbox to normal, enters the value, then changes the
        status to disabled.

        args: None
        return:: None
        '''
        self.outputbox.configure(state=tk.NORMAL)
        #insert the input from the input textbox (Entry object) at line 1, character 0
        self.outputbox.insert(1.0,self.textbox.get())
        #Change the status of the text object to DISABLED (non editable)
        self.outputbox.configure(state=tk.DISABLED)

MyGUI()
