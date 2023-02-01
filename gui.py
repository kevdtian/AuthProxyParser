# -*- coding: utf-8 -*-
"""
Created on Sun Jan 22 15:27:56 2023
"""

import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry


class MyGUI:
    date = 'Any', 'to', 'Any'

    def __init__(self, root):
        '''Initializes the main frame of the GUI and populates it with the appropriate objects
        args: None
        return:none
        '''
        self.show_Date = None
        self.to_date = None
        self.to_label = None
        self.to_frame = None
        self.submit_button = None
        self.from_date = None
        self.from_label = None
        self.from_frame = None
        self.root = root

        # Create the main frame and assign it the root variable
        self.root = tk.Tk()

        # Set the resolution of root
        self.root.geometry('1288x760')

        # Set the title of root
        self.root.title('Auth Proxy Log Parser')

        # Create the first frame inside of root and assign it the topFrame variable
        self.topFrame = tk.Frame(self.root, width=50, height=40, bg='#45ba6e')
        self.topFrame.pack(fill='x', pady=5)

        # Create the second frame inside of root and assign it the leftFrame variable
        self.leftFrame = tk.Frame(self.root, width=500, height=500)
        self.leftFrame.pack(pady=5, padx=5, ipady=5, ipadx=5, side='left', expand=True, fill='both')

        # Create the third frame inside of root and assign it the rightFrame variable
        self.rightFrame = tk.Frame(self.root, width=500, height=500)
        self.rightFrame.pack(ipady=5, ipadx=5, side='left', expand=True, fill='both')

        # Create the text above output field (Label Object) and assign it the label variable
        tk.Label(self.rightFrame, text="Output:", font=('Times New Roman', 20)).pack(anchor='nw')

        # Create the text inside the topFrame  (Label Object) and assign it the label variable
        self.label = tk.Label(self.topFrame, text="Duo Security Authentication Proxy Log Parser", bg='#45ba6e',
                              font=('ariel', 25))
        self.label.grid(row=30, column=2)

        # Create the text above the search box (Label Object) and assign it the textBoxLabel variable
        tk.Label(self.leftFrame, text="Search string", font=('Times New Roman', 20)).pack(
            anchor='nw', padx=5)

        # Create the search box (Entry object) and assing it the textbox variable
        self.textbox = tk.Entry(self.leftFrame, width=40, font=('Times New Roman', 20))
        self.textbox.pack(anchor='n', expand=False, fill='x', padx=5)

        # Create a text object box with the appropriate sizing. Set the status to disabled (non-editable)
        self.outputBox = tk.Text(self.rightFrame, width=50, font=('Times New Roman', 20), state=tk.DISABLED)
        self.outputBox.insert(1.0, self.textbox.get())

        # Pack the Text object
        self.outputBox.pack(expand=True, fill='both', padx=5)

        # Create quitButton (Button Object) for the quit button. Assign frame,text, command, and pack it. Best 
        # practice is to separate the packing from the variable (to do)
        tk.Button(self.leftFrame, text='Quit', command=self.root.destroy).pack(side='bottom',
                                                                               anchor='sw')

        # Create the show button (Button object) and assign it the show variable
        tk.Button(self.leftFrame, text='Show', command=self.print_textbox, width=4).pack(anchor='nw',
                                                                                         after=self.textbox)

        # Create the date button (Button Object) and assign it the dateButton variable
        self.dateButton = tk.Button(self.leftFrame, text='Date', command=str(self.show_Date), width=4)
        self.dateButton.pack(side='top', anchor='w')

        self.current_date_label = tk.Label(self.leftFrame, text=str(self.date))
        self.current_date_label.pack()
        self.root.mainloop()

    def print_textbox(self):
        '''Inserts/prints the values entered into textbox into the output box. Changes the status of the outputBox to normal, enters the value, then changes the
        status to disabled.
        args: None
        return: None
        '''
        self.outputBox.configure(state=tk.NORMAL)
        # insert the input from the input textbox (Entry object) at line 1, character 0
        self.outputBox.insert(1.0, self.textbox.get())

        # Change the status of the text object to DISABLED (non editable)
        self.outputBox.configure(state=tk.DISABLED)

    def show_date(self):
        '''Initializes a new frame for the date and time entry.
        args: None
        return: None'''
        self.dateButton.configure(state=tk.DISABLED)
        self.from_frame = tk.Frame(self.leftFrame, width=50, height=80)
        self.from_label = tk.Label(self.from_frame, text='From')
        self.from_date = DateEntry(self.from_frame)
        self.submit_button = tk.Button(self.from_frame, text='Submit', command=self.submit_cal)
        self.to_frame = tk.Frame(self.leftFrame, width=50, height=80)
        self.to_label = tk.Label(self.to_frame, text='To')
        self.to_date = DateEntry(self.to_frame)
        self.from_frame.pack(anchor='nw', padx=5, side='left')
        self.from_label.pack(anchor='w', padx=2)
        self.from_date.pack(anchor='w', padx=2)
        self.submit_button.pack(anchor='w')
        self.to_frame.pack(anchor='ne', padx=5, side='left')
        self.to_label.pack(anchor='w')
        self.to_date.pack(anchor='w')

    def submit_cal(self):
        self.dateButton.configure(state=tk.NORMAL)
        self.date = self.from_date.get_date(), 'to', self.to_date.get_date()
        self.from_frame.destroy()
        self.to_frame.destroy()
        self.update_shown_date()

    def update_shown_date(self):
        self.current_date_label.destroy()
        self.current_date_label = tk.Label(self.leftFrame, text=str(self.date))
        self.current_date_label.pack()


MyGUI('root')
