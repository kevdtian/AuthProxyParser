<Still In Development>
This is a desktop ready application for parsing log files in the Duo Authentication Proxy.

Using this tool will allow users to search their authproxy log files with an in-house Duo application that helps streamline troubleshooting and data gathering.

The GUI will match the layout of the current Authentication Proxy Manager tool and will allow Kit's to use a highly customizable search function that parses out the relevant lines and surrounding logging resulting from their search query (ie: specific usernames)

Specifications

Tool will search automatically for authproxy.log file in auth proxy folder.  Custom files can also be selected manually.

Users can type in any strings to search for in the file. 

Users can specify search by dates. 

Automatically merge multiple log files to search. (authproxy, authproxy1, authproxy2, etc).

STRETCH Goals: 
Compiles the most common errors and provide checkbox/dropdown selections to parse for these directly. 
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

Exepected Completion February 22nd.
This documentation will be revised as more technical and functional details are made known through development.
