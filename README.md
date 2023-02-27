This is a desktop ready application for parsing log files in the Duo Authentication Proxy.

Using this tool will allow users to search their authproxy log files with an in-house Duo application that helps streamline troubleshooting and data gathering.

The GUI will match the layout of the current Authentication Proxy Manager tool and will allow administrators to use a highly customizable search function that parses out the relevant lines and surrounding logging resulting from their search query (ie: specific usernames)

Specifications

Tool will search automatically for authproxy.log file in auth proxy folder.  Custom files can also be selected manually.
If multiple files are selected, they will all be concatenated and displayed in a signle text field.

Users can type in any strings to search for in the file. 

Users can specify dates to scope the visible logs to.

If any commonly documented errors are detected, the tool will automatically note these under the "Compile Errors" tab and allow filtering to the detected errors as well as offer links to related KB articles for additional details.

To use the tool, you can initiate the gui.exe file located within the 'dist' folder from this repo:
1. Select a valid authproxy.log file (or series of log files.)
2. Type a term you wish to filter to.
3. Select a date range if desired.
4. Any items found within the selected range will be highlighted and include the context of their relevant line along with a line number for easy reference back to the original proxy files if needed.
5. If a common error was detected, it will be shown under the "Compile Error" dropdown button.
6. Clicking on any of the left-hand column of buttons displayed will filter to the errors detected in the logs.
6. Any buttons in the right hand column next to the listed errors are a summation of the cause of those errors.  If those buttons are clicked, it will lead to a related KB article detailing the issue.
7.  Hitting Reset to Default at any time will clear any set filters and restore the logs to their original state.
8.  You can hit the 'Quit' button at any time to close the application.

STRETCH Goals: 
Provide relevant help articles or recommendations for any error messages that appear.
Integrating tool directly into the Authproxy Manager Tool.

Dependencies:
Codebase - Python, Github
GUI framework - Tkinter

Relevant Resources:
Github: https://github.com/kevdtian/AuthProxyParser
Tkinter Documentation: https://docs.python.org/3/library/tk.html
https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/index.html (alt)
Regex Editor/cheat sheet: https://pythex.org
Tkcalendar: https://tkcalendar.readthedocs.io/en/stable/index.html
