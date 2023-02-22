import tkinter as tk
import webbrowser
from functools import partial
from tkinter import filedialog
from tkinter import Scrollbar
from tkinter import Toplevel
from tkinter import Label
from tkinter import Button
from tkcalendar import DateEntry
import os
from datetime import datetime, timedelta

class CustomText(tk.Text):
    '''A scrolledtext widget with a new method, highlight_pattern()
    example:
    text = CustomText()
    text.tag_configure("red", foreground="#ff0000")
    text.highlight_pattern("this should be red", "red")
    '''
    def __init__(self, *args, **kwarg,):
        tk.Text.__init__(self, *args, **kwarg)

    def highlight_pattern(self, pattern, tag, start="1.0", end="end",
                          regexp=True):
        '''Apply the given tag to all text that matches the given pattern
        If 'regexp' is set to True, pattern will be treated as a regular
        expression according to Tcl's regular expression syntax.
        '''
        start = self.index(start)
        end = self.index(end)
        self.mark_set("matchStart", start)
        self.mark_set("matchEnd", start)
        self.mark_set("searchLimit", end)

        count = tk.IntVar()
        while True:
            index = self.search(pattern, "matchEnd","searchLimit", nocase=True,
                                count=count, regexp=regexp)
            if index == "": break
            if count.get() == 0: break # degenerate pattern which matches zero-length strings
            self.mark_set("matchStart", index)
            self.mark_set("matchEnd", "%s+%sc" % (index, count.get()))
            self.tag_add(tag, "matchStart", "matchEnd")

class MyGUI(tk.Frame):
    def __init__(self):
        """Initializes the main frame of the GUI and populates it with the appropriate objects
        args: None
        return:none
        """
        self.createWidgets()

    def createWidgets(self):
        self.date = "Any", "to", "Any"
        self.concatenated_file = None
        self.default_file = None
        self.show_Date = None
        self.to_date = None
        self.to_label = None
        self.to_frame = None
        self.submit_button = None
        self.from_date = None
        self.from_label = None
        self.from_frame = None
        self.submit_frame = None
        self.name = None
        # Create the main frame and assign it the root variable

        self.root = tk.Tk()
        # Set the resolution and center root
        w = 1280
        h = 720
        ws = self.root.winfo_screenwidth()
        hs = self.root.winfo_screenheight()
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)
        self.root.geometry('%dx%d+%d+%d' % (w, h, x, y))
        # Set the background of root to gray
        self.root.configure(bg="#212124")
        # Set the title of root
        self.root.title("Auth Proxy Log Parser")

        # Create the first frame inside of root and assign it the topFrame variable
        self.topFrame = tk.Frame(self.root, width=50, height=40, bg='#45ba6e')

        # Create the second frame inside of root and assign it the leftFrame variable
        self.leftFrame = tk.Frame(self.root, width=500, height=500, bg="#212124")

        # Create the third frame inside of root and assign it the rightFrame variable
        self.rightFrame = tk.Frame(self.root, width=500, height=500, bg="#212124")

        # Create the bottom right frame inside of the right frame and assign it the rightFrame variable
        self.bottomRightFrame = tk.Frame(self.rightFrame, width=50, height=20, bg="#212124")

        # Create the bottom left frame inside of the left frame and assign it the rightFrame variable
        self.bottomLeftFrame = tk.Frame(self.leftFrame, width=50, height=275, bg="#212124")

        self.compileFrameLeft = tk.Frame(self.bottomLeftFrame, height=275, width=250, bg="red")

        self.compileFrameRight = tk.Frame(self.bottomLeftFrame, height=275,width=250, bg="blue")

        # Create the reset button
        self.reset_button = tk.Button(self.rightFrame, text="Reset to Default", command=self.reset,
                                      highlightcolor="#212124", highlightbackground="#212124", bg="white")

        # Create the choose file button
        self.choose_file = tk.Button(self.rightFrame, text="Choose File", command=self.open_file,
                                     highlightcolor="#212124", highlightbackground="#212124", bg="white")

        # Create the text inside the topFrame  (Label Object) and add it the label variable
        self.label = tk.Label(
            self.topFrame,
            text="Duo Security Authentication Proxy Log Parser",
            bg="#45ba6e",
            font=("ariel", 25),
        )

        # Create the text above the search box (Label Object) and adding it the textboxLabel variable
        self.textboxLabel = tk.Label(
            self.leftFrame,
            text="Search string:",
            font=("Arial", 17),
            bg="#212124",
            fg="#FAF9F6",
        )

        # Create the search box (Entry object) and adding it the textbox variable
        self.textbox = tk.Entry(
            self.leftFrame, width=47, font=("Arial", 16), insertbackground="#FAF9F6", bg="#212124", fg="#FAF9F6",
            justify='left'
        )
        self.textbox.bind("<Return>", self.search_input)

        # Create a text object box with the appropriate sizing. Set the status to disabled (non-editable)
        self.scrollBar = Scrollbar(self.bottomRightFrame, orient='vertical', bg="#212124", troughcolor="#212124",
                                   highlightbackground="#212124", jump=0,)

        self.outputBox = CustomText(
            self.bottomRightFrame,
            width=50,
            font=("Arial", 12),
            wrap="word",
            state=tk.DISABLED,
            bg="#212124",
            fg="#FAF9F6",
            yscrollcommand=self.scrollBar.set
        )
        self.scrollBar.config(command=self.outputBox.yview)

        # Create quitButton (Button Object) for the quit button. Assign frame,text, command, and pack it.
        self.quitButton = tk.Button(
            self.leftFrame, text="Quit", command=self.root.destroy, highlightcolor="#212124",
            highlightbackground="#212124", bg="white"
        )

        # Create the search button (Button object) and adding it the searchButton variable
        self.searchButton = tk.Button(
            self.leftFrame, text="Search", command=self.search_input, width=7, highlightcolor="#212124",
            highlightbackground="#212124", bg="white"
        )

        # Create the date button (Button Object) and assign it the dateButton variable
        self.dateButton = tk.Button(
            self.leftFrame, text="Date", command=self.show_date, width=7, highlightcolor="#212124",
            highlightbackground="#212124", bg="white"
        )

        self.current_date_label = tk.Label(self.leftFrame, text=None, highlightcolor="#212124",
                                           highlightbackground="#212124", bg="#212124", fg="#FAF9F6")

        self.errorsButton = tk.Button(
            self.bottomLeftFrame, text="Compile Errors", command=self.init_compiler, width=12, highlightcolor="#2c6fbb",
            highlightbackground="#2c6fbb", bg='#2c6fbb'
        )

        self.topFrame.pack(fill='x', pady=5)
        self.leftFrame.pack(pady=5, padx=5, ipady=5, ipadx=5, side='left', fill='both')
        self.rightFrame.pack(ipady=5, ipadx=5, side="left", expand=True, fill="both")
        self.bottomRightFrame.pack(ipady=5, ipadx=5, side="bottom", expand=True, fill="both")
        self.bottomLeftFrame.pack(ipady=5, ipadx=5, side="bottom", fill='both', expand=True)
        self.reset_button.pack(side="left", anchor="w")
        self.choose_file.pack(side="left", anchor="w", padx=5)
        self.label.grid(row=30, column=2)
        self.textboxLabel.pack(anchor="nw", padx=5)
        self.textbox.pack(anchor="n", expand=False, fill="x", padx=5)
        self.scrollBar.pack(side='right', fill='y')
        self.outputBox.pack(expand=True, fill="both", side="left", anchor="w", padx=1, pady=1)
        self.quitButton.pack(side="bottom", anchor="sw", before=self.bottomLeftFrame)
        self.searchButton.pack(anchor="nw", padx=5, pady=10)
        self.dateButton.pack(anchor="nw", padx=5)
        self.current_date_label.pack(anchor='w', padx=50)
        self.errorsButton.pack(anchor='e')

    def start(self):
        self.root.mainloop()

    def popup(self):
        top = Toplevel(self.root, bg="#212124")
        w=320
        h=100
        ws = self.root.winfo_screenwidth()
        hs = self.root.winfo_screenheight()
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)
        top.geometry('%dx%d+%d+%d' % (w, h, x, y))
        top.grab_set()
        Label(top, wraplength=300, bg="#212124", fg="#FAF9F6", text="Too many results found. Displaying first 100 events. Please refine your search.", font=("Arial")).place(x=20,y=10)
        Button(top, text="Close", command=top.destroy, width=6, font=("Arial")).place(x=126,y=55)

    def display_output_box(self, words, from_date, to_date):
        """Inserts/prints the values entered into textbox into the output box. Changes the status of the outputBox to normal, enters the value, then changes the
        status to disabled.
        input: str. What to be displayed in the output box.
        return: None
        """
        self.outputBox.configure(state=tk.NORMAL)
        self.outputBox.delete(1.0, "end")

        if from_date and to_date:
            words = filter_by_date(words, from_date, to_date)
            # self.concatenated_file = words

        search = self.get_search_box().casefold()
        count = 0
        if type(words) is list:

            # insert the input from the input textbox (Entry object) at line 1, character 0
            for line in range(len(words)):

                # Define threshold for number of search returns as 100
                if count >= 100:
                    self.popup()
                    break

                elif search.casefold() in str(words[line]).casefold() and search.casefold() != '':

                    self.outputBox.insert(1.0, words[line])
                    self.outputBox.tag_configure("text", foreground="#f1e740")
                    self.outputBox.highlight_pattern(search, "text")
                    count += 1

                else:

                    self.outputBox.insert(1.0, words[line])

            # Change the status of the text object to DISABLED (non editable)
            self.outputBox.configure(state=tk.DISABLED)

        elif type(words) is str:
            self.outputBox.insert(1.0, words)

        else:
            self.outputBox.insert(
                1.0,
                "No files found in default directories, please import Proxy log files.",
            )
            # Change the status of the text object to DISABLED (non editable)
            self.outputBox.configure(state=tk.DISABLED)

    def reset(self):
        self.outputBox.configure(state=tk.NORMAL)
        self.textbox.delete(0, 'end')
        print(self.textbox.get())
        self.concatenated_file = self.default_file
        self.current_date_label.destroy()
        self.date = "Any", "to", "Any"
        self.display_output_box(self.concatenated_file, None, None)
        self.outputBox.configure(state=tk.DISABLED)

    def get_search_box(self):
        """returns the string inputted in the search box of the gui.
        input:none
        return: str. String in the search box of the gui"""
        return str(self.textbox.get())

    def show_date(self):
        """Initializes a new frame for the date and time entry.
        args: None
        return: None"""
        self.dateButton.configure(state=tk.DISABLED)
        self.from_frame = tk.Frame(self.leftFrame, bg="#212124", width=10)
        self.from_label = tk.Label(self.from_frame, text="From")
        self.from_date = DateEntry(
            self.from_frame,
            showweeknumbers=False,
            showothermonthdays=False,
            date_pattern="yyyy-mm-dd",
        )

        self.to_frame = tk.Frame(self.leftFrame, bg="#212124", width=10)
        self.to_label = tk.Label(self.from_frame, text="To")
        self.to_date = DateEntry(
            self.from_frame,
            showweeknumbers=False,
            showothermonthdays=False,
            date_pattern="yyyy-mm-dd",
        )


        self.submit_frame = tk.Frame(self.from_frame, bg="#212124", width=10)
        self.submit_button = tk.Button(
            self.from_frame, text="Submit", command=self.get_date_range, height=1, bg="white"
        )

        self.from_frame.pack(anchor="nw", padx=2, side="left")
        self.from_label.pack(anchor="w", padx=1, side='left')
        self.from_date.pack(anchor='w', padx=1, side='left')

        #self.to_frame.pack(anchor="ne", padx=2, side="left")
        self.to_label.pack(anchor="w", padx=1, side='left')
        self.to_date.pack(anchor="w", padx=1, side='left')

        #self.submit_frame.pack(anchor="nw", padx=5)
        self.submit_button.pack(anchor="w", padx=2, side='left')

    def get_date_range(self):
        self.dateButton.configure(state=tk.NORMAL)
        self.date = self.from_date.get_date(), "to", self.to_date.get_date()
        self.from_frame.destroy()
        self.to_frame.destroy()
        self.submit_frame.destroy()
        self.update_shown_date()
        self.display_output_box(self.concatenated_file, self.date[0], self.date[2])

    def update_shown_date(self):
        self.current_date_label.destroy()
        self.current_date_label = tk.Label(self.leftFrame, text=self.date, highlightcolor="#212124",  highlightbackground="#212124", bg="#212124", fg="#FAF9F6")
        self.current_date_label.pack(anchor='w', padx=1)

    def open_file(self):
        file_object = tk.filedialog.askopenfilenames()
        encoded = list()
        for file in file_object:
            handler = open(file, mode="r", encoding="latin-1")
            encoded.append(handler)
        if len(encoded) > 0:
            concatenated_file = merge_files(encoded)
        else:
            return None
        for file in encoded:
            file.close()
        try:
            datetime.strptime(concatenated_file[0][0:10], "%Y-%m-%d")
        except ValueError:
            self.display_output_box("Incorrect proxy log file", None, None)
        except IndexError:
            self.display_output_box("Incorrect proxy log file", None, None)
        else:
            concatenated_file.reverse()
            self.concatenated_file = concatenated_file
            self.default_file = concatenated_file
            self.display_output_box(self.concatenated_file, None, None)


    def search_input(self, event=None):
        search = self.get_search_box()
        file = self.concatenated_file

        searched_file = search_file(search, file)

        if self.date[0] == "Any" and self.date[2] == "Any":
            self.display_output_box(searched_file, None, None)
        else:
            self.display_output_box(searched_file, self.date[0], self.date[2])

    def init_compiler(self):
        self.errorsButton.configure(command=self.destroy_event_compiler)
        self.compileFrameLeft.pack(side='left', fill='x', anchor='e', pady=10)
        self.compileFrameRight.pack(side='right', fill='x', anchor='w')
        button_names, lines, kbs = compile_events(self.concatenated_file)

        for index in range(len(button_names)):
            if len(lines[index]) > 0:
                self.name = tk.Button(self.compileFrameLeft,
                                      command=partial(self.display_output_box, lines[index], None, None),
                                      text=button_names[index], width=21)
                self.name.pack()
                if len(kbs[index]) > 0:
                    self.kb = tk.Button(self.compileFrameRight,
                                          command=partial(open_page, kbs[index][1]),
                                          text=kbs[index][0], width=30)
                    self.kb.pack()

    def destroy_event_compiler(self):
        self.errorsButton.configure(command=self.init_compiler)
        self.compileFrameRight.destroy()
        self.compileFrameLeft.destroy()
        self.compileFrameLeft = tk.Frame(self.bottomLeftFrame, height=275, bg="red")
        self.compileFrameRight = tk.Frame(self.bottomLeftFrame, height=275, bg="blue")
        '''objects_in_frame = self.compileFrameLeftLeftFrame.winfo_children()
        kbs_in_frame = self.compileFrameLeftLeftFrame.winfo_children()
        for obj in objects_in_frame:
            if obj.cget('text') != "Compile Errors":
                obj.destroy()
            elif obj.cget('text') == 'Compile Errors':
                obj.configure(command=self.init_compiler)
'''
def compile_events(conc_file):
    # The dictionary format is: {KEY(str)    name of button:
    #                           VALUE(list)      [(error strs),[line log file]]}
    events_dic = {'Successful Authentication': (('Success, Logging you in',), [], ('Authentication successful, no action needed','')),
                  'Incorrect Password': (('invalidCredentials', 'data 52e',), [], ('Please check users password','https://help.duo.com/s/article/2953?language=en_US#incorrectpw')),
                  'Invalid SKEY': (('Invalid SKEY',), [], ('Check the Skey','https://help.duo.com/s/article/2953?language=en_US#invalidskey')),
                  'No User LDAP permission': (('data 531',), [], ('Ensure user has permission to login to machine','https://help.duo.com/s/article/2953?language=en_US#usernologin')),
                  'Auth Proxy Start': (('Duo Security Authentication Proxy', 'Init Complete',), [], ('Auth Proxy successfully started','')),
                  'Disabled AD User': (('data 533', 'data534'), [], ('Account disabled in AD','https://help.duo.com/s/article/2953?language=en_US#disabledadacct')),
                  'Locked AD Account': (('data 775',), [], ('Please unlock user in AD','https://help.duo.com/s/article/2953?language=en_US#lockedadacct')),
                  'Service Account no bind': (('Error sending AD auth request', 'invalid Credentials,',),
                                                           [], ('Please check service account creds','https://help.duo.com/s/article/2953?language=en_US#bindissue')),
                  'Bind after disconnect': (
                      ('Attempt to bindRequest multiple times in the same LDAP connection',), [], ('Appliance is binding after 2FA','https://help.duo.com/s/article/2953?language=en_US#multiplebinds')),
                  'Invalid RADIUS IP': (('dropping packet', 'Unknown Client',), [], ('Check the appliance IP is listed correctly in config','https://help.duo.com/s/article/2953?language=en_US#noradiusclientip')),
                  'Shared secret mismatch': (('Cannot decode password',), [], ('Verify the RADIUS Secret ','https://help.duo.com/s/article/1168')),
                  'Invalid encrypted secret': (('Invalid secret',), [], ('Please try an unencrypted secret','https://help.duo.com/s/article/1168')),
                  'Primary auth disconnect': (('User timeout caused connection failure',),
                                                                         [], ('Proxy cannot reach AD','https://help.duo.com/s/article/2953?language=en_US#dnsresolutionnotworking')),
                  'DNS failing': (('DNS lookup failed',), [], ('DNS failing resolution','https://help.duo.com/s/article/2953?language=en_US#nodnsresolution')),
                  'DNS failing secure': (
                      ('DNSLookupError', 'Denied Duo login on preauth failure'), [], ('DNS failing, FailClosed','https://help.duo.com/s/article/2953?language=en_US#nodnsresolutionfailclosed')),
                  'Cloud unreachable TCP': (
                      ('TCPTimedOutError', 'allowed Duo login on preauth failure'), [], ('Check outbound access on 443','https://help.duo.com/s/article/1337')),
                  'Invalid protected SKEY': (('CryptUnprotectData', 'The data is invalid',), [], ('Check for correct SKEY','https://help.duo.com/s/article/2953?language=en_US#invalidprotectedskey')),
                  'Invalid IKEY': (('Invalid integration key in request credentials', '40102'), [], ('Please grab IKEY from app in Admin Panel','https://help.duo.com/s/article/2953?language=en_US#invalidikey')),
                  'Invalid private key file': (('Could not open private key file',), [], ('Please verify the location of private key file','https://help.duo.com/s/article/2953?language=en_US#invalidprivatekeyfile')),
                  'User not in sec group': (
                      ('Tried to search security group DN for object sid but it could not be found',), [], ('Verify user security group membership','https://help.duo.com/s/article/2953?language=en_US#invalidusererror')),
                  'User not enrolled block': (('enroll', 'enrolled'), [], ('Please verify username exists in Admin Panel','https://help.duo.com/s/article/2953?language=en_US#preauthmessages')),
                  'No reply from user': (('Login timed out',), [], ('User not accepting 2FA','https://help.duo.com/s/article/2953?language=en_US#preauthmessages')),
                  'User not enrolled pass': (('Allowing unknown user',), [], ('Username does not exist in Admin Panel. Allowed via policy','https://help.duo.com/s/article/2953?language=en_US#preauthmessages')),
                  'Plain auth required': (('0xA3',), [], ('AD auth protocol error','https://help.duo.com/s/article/2953?language=en_US#protocolerrors')),
                  'Bad RADIUS protocol': (
                      ('Missing or improperly formatted password',), [], ('RADIUS protocol unsupported','https://help.duo.com/s/article/2953?language=en_US#protocolerrors')),
                  'User not found': (('data 525',), [], ('Cannot find user in AD','https://help.duo.com/s/article/2953?language=en_US#aderrorcodeguide')),
                  'User PW Expired': (('data 532',), [], ('User Password expired, please reset','https://help.duo.com/s/article/2953?language=en_US#aderrorcodeguide')),
                  'User PW Reset': (('data 773',), [], ('Please reset user password','https://help.duo.com/s/article/2953?language=en_US#aderrorcodeguide')),
                  'unlike hosts AD sync': (('sections must have the exact same',), [], ('Multiple ADSyncs in single Proxy','https://help.duo.com/s/article/3671')),
                  'NTLMv2 disabled on DC': (('data 1',), [], ('Please enable NTLM','https://help.duo.com/s/article/2953?language=en_US#ntlmdisabled')),
                  'Invalid mail attribute': (('Invalid LDAP filter',), [], ('Please verify user mail attribute','https://help.duo.com/s/article/6413'))
                  }

    if conc_file:
        for line in conc_file:
            for values in events_dic.values():
                for search_str in values[0]:
                    if search_str.lower() in line.lower():
                        values[1].append(line)

    error_lines = [error[1] for error in events_dic.values()]
    kb_lines = [kb[2] for kb in events_dic.values()]

    return list(events_dic.keys()), error_lines, kb_lines

def import_default_dir():
    """Search through program files and program files x86. If the auth proxy directory is found in either, filter the log folder (to only include
    files that start with authproxy), open the files and concatenate them, then return the directory and file object. If nothing is found, return
    a string and None for the file object
    args: None
    return: str, directory that has the proxy logs. File Object, the concatenated files from the log directory
    """
    #program_files = "C:\Program Files\Duo Security Authentication proxy\Log\""
    #program_files = '/Users/bsaleem/Desktop/git_stuff/authproxylog/'
    program_files = "D:/Work/Coding/AuthProxyLogParser/authproxytest/"
    program_files_x86 = r"C:\Program Files x86\Duo Security Authentication proxy\Log\'"

    if os.path.exists(program_files):
        # list for io wrappers
        io_wrappers = list()
        # init filtered list and call on filter function
        authproxy_logs = filter_log_directory(os.listdir(program_files), "authproxy")
        authproxy_logs.sort()
        # for file in filtered list
        for file in authproxy_logs:
            # open it and append handler to io wrappers list
            handler = open(program_files + file, "r", encoding="latin-1")
            io_wrappers.append(handler)
        # Call on merge_files to return a readlines list of all the io wrappers provided
        concatenated_file = merge_files(io_wrappers)
        for wrapper in io_wrappers:
            wrapper.close()
        concatenated_file.reverse()
        return program_files, concatenated_file
    elif os.path.exists(program_files_x86):
        # list for io wrappers
        io_wrappers = list()
        # init filtered list and call on filter function
        authproxy_logs = filter_log_directory(os.listdir(program_files), "authproxy")
        authproxy_logs.sort()
        # for file in filtered list
        for file in authproxy_logs:
            # open it and append handler to io wrappers list
            handler = open(program_files + file, "r", encoding="latin-1")
            io_wrappers.append(handler)
        # Call on merge_files to return a readlines list of all the io wrappers provided
        concatenated_file = merge_files(io_wrappers)
        for wrapper in io_wrappers:
            wrapper.close()
        concatenated_file.reverse()
        return program_files, concatenated_file

    else:
        return (
            "No files found in default directories, please import Proxy log files",
            None,
        )


def filter_log_directory(path, start_with):
    """Filter the items in the provided list to ensure that they start with the appropriate string.
    args: list, path of the log folder. str, the string to filter by (what the files begin with). (case sensitive).
    return: list, list of files that start with the given argument"""
    return [file for file in path if file.startswith(start_with)]


def merge_files(files):
    """Merge the provided proxy log files into one list of every line in the file objects provided. Files are sorted in order from newest to oldest
    args: list, list of io_wrappers/file objects for the log files
    return: list. lines of concatenated files"""
    return_list = []
    files.reverse()
    for file in files:
        for line in file.readlines():
            return_list.append(line)

    return return_list


def filter_by_date(lines, from_date, to_date):
    dates = calculate_date_difference(from_date, to_date)
    dates_list = convert_from_datetime_to_str(dates)
    filtered_list = list()
    if lines:
        for line in lines:
            if line[0:10] in dates_list or line[0:5] == " ":
                filtered_list.append(line)
    return filtered_list


def convert_from_str_to_datetime(date_string):
    """convert authproxy date time value to a date time object
    args: str, date time in the format of the auth proxy log
    return: date time object, a dtm object of the string argument if the formatting is correct.
            None, if the formatting is not correct"""
    date_string = str(date_string)
    try:
        date_time_object = datetime.strptime(date_string, "%Y-%m-%d").date()
    except ValueError:
        date_time_object = None
    return date_time_object


def convert_from_datetime_to_str(dates):
    for i in range(len(dates)):
        dates[i] = str(dates[i])
    return dates


def calculate_date_difference(from_date, to_date):
    list_of_dates = list()
    from_date = convert_from_str_to_datetime(from_date)
    to_date = convert_from_str_to_datetime(to_date)

    list_of_dates.append(from_date)
    if from_date or to_date is not None:
        delta = (to_date - from_date).days
        for days in range(delta):
            list_of_dates.append(from_date + timedelta(days=days + 1))
    return list_of_dates


def search_file(search_param, lines):
    # Store search input.
    new_list = list()
    search_param = search_param
    lines = lines

    # Loop through each line in the list.
    for line in lines:
        if search_param.casefold() in line.casefold():
            new_list.append(line)

    return new_list

def open_page(page):
    webbrowser.open(page)

# Call on the import_default_dir function. Assign the two return values to directory and conc file. Note that at the moment, the value for directory
# is not used, but may become useful in the future.

s = MyGUI()
s.concatenated_file = import_default_dir()[1]
s.default_file = s.concatenated_file
s.display_output_box(s.concatenated_file, None, None)
s.start()