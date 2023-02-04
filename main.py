import os
from gui import MyGUI as g


def import_default_dir():
    #program_files = 'C:\Program Files\Duo Security Authentication proxy\Log'
    program_files = '/tmp/authproxy/log/'
    program_files_x86=r'C:\Program Files x86\Duo Security Authentication proxy\Log'
    if os.path.exists(program_files):
        conc_files = merge_files(program_files,filter_log_file(os.listdir(program_files)))
        return program_files, conc_files
    elif os.path.exists(program_files_x86):
        conc_files = merge_files(program_files,filter_log_file(os.listdir(program_files)))
        return program_files, conc_files
    else:
        return 'No files found in default directories, please import Proxy log files', None

def filter_log_file(path):
    return [file for file in path if file.startswith('auth')]

def merge_files(path, files):
    return_str = ''
    for file in files:
        with open(path+file, 'r', encoding='latin-1') as handler:
            return_str +=  handler.read() +'\n'
    return return_str

directory, conc_file = import_default_dir()

gui = g()
gui.display_output_box(conc_file)
gui.start()
#while gui.grab_search_box() == '':

#gui.display_output_box(gui.grab_search_box())
