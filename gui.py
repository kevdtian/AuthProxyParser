import tkinter as tk
from tkcalendar import Calendar
import os
from datetime import datetime, timedelta


class MyGUI:
    def __init__(self):
        """Initializes the main frame of the GUI and populates it with the appropriate objects
        args: None
        return:none
        """
        self.date = "Any", "to", "Any"

        self.show_Date = None
        self.to_date = None
        self.to_label = None
        self.to_frame = None
        self.submit_button = None
        self.from_date = None
        self.from_label = None
        self.from_frame = None

        # Create the main frame and assign it the root variable
        self.root = tk.Tk()

        # Set the resolution and center root
        w = 1280
        h = 720
        ws = self.root.winfo_screenwidth()
        hs = self.root.winfo_screenheight()
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)

        self.root.geometry('%dx%d+%d+%d' % (w, h, x, y))

        # Set the background of root to gray
        self.root.configure(bg="#212124")

        # Set the title of root
        self.root.title("Auth Proxy Log Parser")

        # Create the first frame inside of root and assign it the topFrame variable
        self.topFrame = tk.Frame(self.root, width=50, height=40, bg="#45ba6e")
        self.topFrame.pack(fill="x", pady=5)

        # Create the second frame inside of root and assign it the leftFrame variable
        self.leftFrame = tk.Frame(self.root, width=500, height=500, bg="#212124")
        self.leftFrame.pack(
            pady=5, padx=5, ipady=5, ipadx=5, side="left", expand=True, fill="both"
        )

        # Create the third frame inside of root and assign it the rightFrame variable

        self.rightFrame = tk.Frame(self.root, width=500, height=500, bg="#212124")
        self.rightFrame.pack(ipady=5, ipadx=5, side="left", expand=True, fill="both")

        # Create the text above output field (Label Object) and adding it the label variable
        self.clear_button = tk.Button(
            self.rightFrame, text="Clear", command=self.clear, width=4, bg="#212124", fg="#FAF9F6"
        )
        self.clear_button.pack(side="top", anchor="w", padx=5, pady=5)

        # Create the text inside the topFrame  (Label Object) and adding it the label variable
        self.label = tk.Label(
            self.topFrame,
            text="Duo Security Authentication Proxy Log Parser",
            bg="#45ba6e",
            font=("ariel", 25),
        )
        self.label.grid(row=30, column=2)

        # Create the text above the search box (Label Object) and adding it the textboxLabel variable
        self.textboxLabel = tk.Label(
            self.leftFrame,
            text="Search string:",
            font=("Arial", 17),
            bg="#212124",
            fg="#FAF9F6",
        )
        self.textboxLabel.pack(anchor="nw", padx=5)

        # Create the search box (Entry object) and adding it the textbox variable
        self.textbox = tk.Entry(
            self.leftFrame, width=20, font=("Arial", 20), bg="#212124"
        )
        self.textbox.pack(anchor="n", expand=False, fill="x", padx=5)

        # Create a text object box with the appropriate sizing. Set the status to disabled (non-editable)
        self.outputBox = tk.Text(
            self.rightFrame,
            width=50,
            font=("Arial", 12),
            wrap="word",
            state=tk.DISABLED,
            bg="#212124",
            fg="#FAF9F6",
        )

        # Pack the Text object
        self.outputBox.pack(expand=True, fill="both", padx=5)

        # Create quitButton (Button Object) for the quit button. Assign frame,text, command, and pack it. Best practice is to separate the packing from the variable (to do)
        self.quitButton = tk.Button(
            self.leftFrame, text="Quit", command=self.root.destroy, bg="#212124", fg="#FAF9F6"
        )
        self.quitButton.pack(side="bottom", anchor="sw")

        # Create the search button (Button object) and adding it the searchButton variable
        self.searchButton = tk.Button(
            self.leftFrame, text="Search", command=None, width=7, bg="#212124", fg="#FAF9F6"
        )
        self.searchButton.pack(anchor="nw", padx=5, pady=10, after=self.textbox)

        # Create the date button (Button Object) and assign it the dateButton variable
        self.dateButton = tk.Button(
            self.leftFrame, text="Date", command=self.show_date, width=7, bg="#212124", fg="#FAF9F6"
        )
        self.dateButton.pack(side="top", anchor="w", padx=5)
        self.current_date_label = tk.Label(self.leftFrame, text=self.date, bg="#212124", fg="#FAF9F6")
        self.current_date_label.pack()
        self.display_output_box(conc_file, None, None)

    def start(self):
        self.root.mainloop()

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

        if words:
            # insert the input from the input textbox (Entry object) at line 1, character 0
            for line in range(len(words)):
                self.outputBox.insert(1.0, words[line])
            # self.outputBox.insert(1.0, words)
            # Change the status of the text object to DISABLED (non editable)
            self.outputBox.configure(state=tk.DISABLED)
        else:
            self.outputBox.insert(
                1.0,
                "No files found in default directories, please import Proxy log files.",
            )
            # self.outputBox.insert(1.0, words)
            # Change the status of the text object to DISABLED (non editable)
            self.outputBox.configure(state=tk.DISABLED)

    def clear(self):
        self.outputBox.configure(state=tk.NORMAL)
        self.outputBox.delete(1.0, "end")
        self.outputBox.configure(state=tk.DISABLED)

    def grab_search_box(self):
        """returns the string inputted in the search box of the gui.
        input:none
        return: str. String in the search box of the gui"""
        return self.textbox.get()

    def show_date(self):
        """Initializes a new frame for the date and time entry.
        args: None
        return: None"""
        self.dateButton.configure(state=tk.DISABLED)
        self.from_frame = tk.Frame(self.leftFrame, width=50, height=80)
        self.from_label = tk.Label(self.from_frame, text="From")
        self.from_date = Calendar(
            self.from_frame,
            showweeknumbers=False,
            showothermonthdays=False,
            date_pattern="yyyy-mm-dd",
        )
        self.submit_button = tk.Button(
            self.from_frame, text="Submit", command=self.get_date_range
        )
        self.to_frame = tk.Frame(self.leftFrame, width=50, height=80)
        self.to_label = tk.Label(self.to_frame, text="To")
        self.to_date = Calendar(
            self.to_frame,
            showweeknumbers=False,
            showothermonthdays=False,
            date_pattern="yyyy-mm-dd",
        )
        self.from_frame.pack(anchor="nw", padx=5, side="left")
        self.from_label.pack(anchor="w", padx=2)
        self.from_date.pack(anchor="w", padx=2)
        self.submit_button.pack(anchor="w")
        self.to_frame.pack(anchor="ne", padx=5, side="left")
        self.to_label.pack(anchor="w")
        self.to_date.pack(anchor="w")

    def get_date_range(self):
        self.dateButton.configure(state=tk.NORMAL)
        self.date = self.from_date.get_date(), "to", self.to_date.get_date()
        self.from_frame.destroy()
        self.to_frame.destroy()
        self.update_shown_date()
        self.display_output_box(import_default_dir()[1], self.date[0], self.date[2])
        return self.date[0], self.date[2]

    def update_shown_date(self):
        self.current_date_label.destroy()
        self.current_date_label = tk.Label(self.leftFrame, text=self.date)
        self.current_date_label.pack()


def import_default_dir():
    """Search through program files and program files x86. If the auth proxy directory is found in either, filter the log folder (to only include
    files that start with authproxy), open the files and concatenate them, then return the directory and file object. If nothing is found, return
    a string and None for the file object
    args: None
    return: str, directory that has the proxy logs. File Object, the concatenated files from the log directory
    """
    program_files = "C:\Program Files\Duo Security Authentication proxy\Log"
    program_files_x86 = r"C:\Program Files x86\Duo Security Authentication proxy\Log\'"
    if os.path.exists(program_files):
        conc_file = merge_files(
            program_files, filter_log_directory(os.listdir(program_files), "authproxy")
        )
        return program_files, conc_file
    elif os.path.exists(program_files_x86):
        conc_file = merge_files(
            program_files, filter_log_directory(os.listdir(program_files), "authproxy")
        )
        return program_files, conc_file
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


def merge_files(path, files):
    """Merge the provided proxy log files into one file object. Files are sorted in order from newest to oldest
    args: str, path of the files, list, list of the file names
    return: list. lines of concatenated files"""
    return_list = []
    files.sort()
    for file in files:
        with open(path + file, "r", encoding="latin-1") as handler:
            for line in handler.readlines():
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
    date_time_object = None
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
    from_date, to_date = convert_from_str_to_datetime(
        from_date
    ), convert_from_str_to_datetime(to_date)
    list_of_dates.append(from_date)
    if from_date or to_date != None:
        delta = (to_date - from_date).days
        for days in range(delta):
            list_of_dates.append(from_date + timedelta(days=days + 1))
    return list_of_dates


"""Add logic to detect 'Choose File' button value. If none is chosen, run the below function call"""
# Call on the import_default_dir function. Assign the two return values to directory and conc file. Note that at the moment, the value for directory
# is not used, but may become useful in the future.
directory, conc_file = import_default_dir()

s = MyGUI()
s.start()
