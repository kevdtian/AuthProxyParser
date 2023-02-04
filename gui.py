import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry, Calendar


class MyGUI:
    def __init__(self):
        '''Initializes the main frame of the GUI and populates it with the appropriate objects
        args: None
        return:none
        '''
        
        self.date = 'Any','to','Any'
        
        self.show_Date = None
        self.to_date = None
        self.to_label = None
        self.to_frame = None
        self.submit_button = None
        self.from_date = None
        self.from_label = None
        self.from_frame = None
        
        #Create the main frame and assign it the root variable
        self.root = tk.Tk()
        
        #Set the resolution of root
        self.root.geometry('1920x1080')
        
        #Set the title of root
        self.root.title('Auth Proxy Log Parser')
        
        #Create the first frame inside of root and assign it the topframe variable
        self.topframe = tk.Frame(self.root, width=50,height= 40, bg='#45ba6e')
        self.topframe.pack(fill='x', pady=5)
        
        #Create the second frame inside of root and assign it the leftframe variable
        self.leftframe = tk.Frame(self.root, width=500,height= 500)
        self.leftframe.pack(pady=5,padx=5,ipady=5,ipadx=5,side='left', expand=True, fill='both')
        
        #Create the third frame inside of root and assign it the rightframe variable
        self.rightframe = tk.Frame(self.root, width=500,height= 500)
        self.rightframe.pack(ipady=5,ipadx=5,side='left', expand=True, fill='both')
        
        #Create the text above output field (Label Object) and assing it the label variable
        self.textboxlabel = tk.Label(self.rightframe,text="Output:", font=('Times New Roman', 20)).pack(anchor='nw')
        
        #Create the text inside the topframe  (Label Object) and assing it the label variable
        self.label = tk.Label(self.topframe, text="Duo Security Authentication Proxy Log Parser",bg='#45ba6e', font=('ariel',25))
        self.label.grid(row=30, column=2)
        
        #Create the text above the serach box (Label Object) and assing it the textboxlabel variable
        self.textboxlabel = tk.Label(self.leftframe,text="Search string", font=('Times New Roman', 20)).pack(anchor='nw',padx=5)
        
        #Create the search box (Entry object) and assing it the textbox variable
        self.textbox = tk.Entry(self.leftframe, width=40, font=('Times New Roman', 20))
        self.textbox.pack(anchor='n',expand=False,fill='x',padx=5)
        
        #Create a text object box with the appropriate sizing. Set the status to disabled (non-editable)
        self.outputbox = tk.Text(self.rightframe, width=50, font=('Times New Roman', 20), wrap='word', state=tk.DISABLED)
        
        #Pack the Text object
        self.outputbox.pack(expand=True,fill='both',padx=5)
        
        #Create quitbutton (Button Object) for the quit button. Assign frame,text, command, and pack it. Best practice is to seperate the packing from the variable (to do)
        self.quitbutton = tk.Button(self.leftframe, text = 'Quit', command = self.root.destroy).pack(side='bottom',anchor='sw')
        
        #Create the show button (Button object) and assing it the show variable
        self.show= tk.Button(self.leftframe, text = 'Search', command = None,width=4)
        self.show.pack(anchor='nw',after=self.textbox)
        
        #Create the date button (Button Object) and assign it the datebutton variable
        self.datebutton = tk.Button(self.leftframe, text='Date', command = self.showdate, width=4)
        self.datebutton.pack(side='top',anchor='w')
        self.current_date_label = tk.Label(self.leftframe, text=self.date)
        
        self.current_date_label.pack()

    def start(self):
        self.root.mainloop()



    def display_output_box(self, *words):
        '''Inserts/prints the values entered into textbox into the output box. Changes the status of the outputbox to normal, enters the value, then changes the

        status to disabled.
        input: str. What to be displayed in the output box.
        return: None
        '''

        if words:
            word = words[0]
            self.outputbox.configure(state=tk.NORMAL)
            #insert the input from the input textbox (Entry object) at line 1, character 0
            self.outputbox.insert(1.0,words[0])
            #Change the status of the text object to DISABLED (non editable)
            self.outputbox.configure(state=tk.DISABLED)
    def grab_search_box(self):
        '''returns the string inputted in the search box of the gui.
        input:none
        return: str. String in the search box of the gui'''
        print(self.textbox.get())
        return self.textbox.get()

    def show_date(self):
        '''Initializes a new frame for the date and time entry.
        args: None
        return: None'''
        self.datebutton.configure(state=tk.DISABLED)
        self.from_frame = tk.Frame(self.leftframe, width=50,height= 80)
        self.from_label= tk.Label(self.from_frame, text='From')
        self.from_date= Calendar(self.from_frame, showweeknumbers=False,showothermonthdays=False)
        self.submit_button = tk.Button(self.from_frame, text='Submit', command=self.get_date_range)
        self.to_frame = tk.Frame(self.leftframe, width=50,height= 80)
        self.to_label= tk.Label(self.to_frame, text='To')
        self.to_date= Calendar(self.to_frame, showweeknumbers=False,showothermonthdays=False)
        self.from_frame.pack(anchor='nw',padx=5,side='left')
        self.from_label.pack(anchor='w',padx=2)
        self.from_date.pack(anchor='w',padx=2)
        self.submit_button.pack(anchor='w')
        self.to_frame.pack(anchor='ne', padx=5, side='left')
        self.to_label.pack(anchor='w')
        self.to_date.pack(anchor='w')


    def get_date_range(self):
        self.datebutton.configure(state=tk.NORMAL)
        self.date = self.from_date.get_date(),'to', self.to_date.get_date()
        self.from_frame.destroy()
        self.to_frame.destroy()
        self.update_shown_date()
        return self.date[0],self.date[2]

    def update_shown_date(self):
        self.current_date_label.destroy()
        self.current_date_label = tk.Label(self.leftframe, text=self.date)
        self.current_date_label.pack()

if __name__ == '__main__':
    s = MyGUI()
    s.start()
