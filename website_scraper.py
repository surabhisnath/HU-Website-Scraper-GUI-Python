"""
@Author: Surabhi S Nath
@Matrikelnummer: 618777
"""

# Imports
import requests
import sys
import os
from bs4 import BeautifulSoup
from tkinter import *
from helpers import *


sys.tracebacklimit = 0


def produceexcelgui(varlist, vartocol, master):
    """
    Gets user column preferences from GUI checkboxes and calls produceexcel()
    
    Parameters:
        varlist (list): list of checkbutton variables to get checked/unchecked
        vartocol (dict): maps between checkbutton variables and columns
        master (tkinter.Tk): object of class Tk. Toplevel GUI widget.

    """

    columns = []
    for v, var in enumerate(varlist):
        if var.get():
            columns.append(vartocol[v + 1])
    produceexcel(columns)
    master.destroy()


def produceexcel(columns=None):
    """
    Produces dataframe and saves it to savepath
    
    Parameters:
        columns (list): Names of columns to include in the spreadsheet

    """

    if columns is None:
        columns = defaultcolumns

    print("Scraping website...")

    # Parse student data from website
    website = requests.get(url)
    bs = BeautifulSoup(website.content, 'html.parser')
    student_data = bs.find_all('div', class_='students-list-item-full clearfix')
    num_students = len(student_data)

    # Make dataframe
    dataframe = makedataframe(student_data, columns)

    # Save dataframe
    saveexcel(dataframe, savepath, columns)

    print("DONE!")
    print("Data of {} students written to spreadsheet.".format(num_students))
    print("Spreadsheet saved to: {}".format(savepath))


def initgui():
    """
    Initialises and display GUI window. Button to generate spreadsheet calls produceexcelgui()

    """

    # Initialize GUI
    print("Displaying GUI...")
    master = Tk()
    master.title("Web Scraper for M&B")
    Label(master,
          text="This application allows you to customise your spreadsheet. Select the information to include from the "
               "list below:").grid(
        row=0)

    # Possible columns
    vartocol = {1: "Name", 2: "E-mail", 3: "Doctoral Project Title", 4: "Project Description", 5: "Supervisors",
                6: "Cohort", 7: "Funding", 8: "M&B topics", 9: "Institute", 10: "Status", 11: "Degrees obtained",
                12: "Title", 13: "URLs"}

    # Checkboxes for each column    
    num_possible_cols = len(vartocol)
    varlist = []
    for i in range(num_possible_cols):
        varlist.append(IntVar(value=(vartocol[i + 1] in defaultcolumns)))
        Checkbutton(master, text=vartocol[i + 1], variable=varlist[i]).grid(row=i + 1, sticky=W)

    # Button to create spreadsheet
    Button(master, text='Generate spreadsheet', width=25,
           command=lambda: produceexcelgui(varlist, vartocol, master)).grid(row=14)
    master.mainloop()


def test(g, sp, dg, dsp, trues, falses):
    """ 
    Tests for type and value of input arguments and raises exceptions.
    Tests are carried out only if non-default GUI/savepath options are used.
    
    Parameters:
        g (str): Indicates GUI true or false
        sp (str): Location for saving file
        dg (bool): Indicates if default GUI option was used
        dsp (bool): Indicates if default savepath option was used
        trues (list): list of strings considered as GUI true
        falses (list): list of strings considered as GUI false
    
    Raises:
        ValueError: if `gui` is not in trues or falses
        ValueError: if `savepath` does not exist
        ValueError: if no filename was specified
        ValueError: if wrong file extension was given
        
    """

    # Test for valid GUI arguement
    if dg == False:
        print("Checking if valid gui argument...")
        options = ""
        for op in trues + falses:
            options += "--gui=" + op + "\n"

        if g not in trues and g not in falses:
            raise ValueError(
                'gui argument must be either true or false.\nPlease specify using one of the following options:\n{}'.format(
                    options[:-1]))
        print("Check passed.")

    # Test for valid savepath
    if dsp == False:
        print("Checking if valid savepath...")
        head, tail = os.path.split(sp)
        if not os.path.exists(head):
            raise ValueError('Savepath {} does not exist. Please specify a valid path.'.format(head))
        print("Check passed.")

        # Test for valid filename

        print("Checking if valid filename...")
        try:
            extension = tail.split('.')[1]
        except IndexError:
            raise ValueError("No filename was specified. Please specify a .xlsx filename with savepath.") from None

        if extension != "xlsx":
            raise ValueError('Save file extension must be xlsx. {} was given.'.format(extension))
        print("Check passed.")


def argparse():
    """ 
    Parses arguments entered in command line
    
    Returns:
        str: GUI indicator
        str: Location to save spreadsheet
        bool: Indicates if default GUI was used
        bool: Indicates if default savepath was used
    """

    useddefaultgui = False
    useddefaultsavepath = False

    try:
        gui = sys.argv[1].split('=')[1]  # GUI argument
    except:
        if len(sys.argv) == 1:
            print("No GUI argument given. Using default GUI = true.")
        else:
            print("GUI argument incorrectly formatted. Using default GUI = True.")
        
        gui = defaultgui  # Default GUI
        useddefaultgui = True

    try:
        savepath = sys.argv[2].split('=')[1]  # savepath argument
    except:
        if len(sys.argv) <= 2:
            print("No savepath argument given. Using default savepath & filename.")
        else:
            print("Savepath argument incorrectly formatted. Using default savepath & filename.")
        
        savepath = defaultsavepath + "/" + defaultfilename  # Default savepath
        useddefaultsavepath = True

    return gui, savepath, useddefaultgui, useddefaultsavepath


if __name__ == "__main__":

    # Initialization --------------------------------------------------

    url = "http://www.mind-and-brain.de/people/doctoral-alumni/"
    defaultcolumns = ['Name', 'E-mail', 'Doctoral Project Title', 'Project Description', 'Supervisors', 'Cohort',
                      'URLs']  # Can be changed here or by using GUI
    defaultgui = "true" # Can be changed
    defaultsavepath = os.getcwd()   # Can be changed
    defaultfilename = "MB_DoctoralStudents.xlsx"    # Can be changed

    # Arg Parse -------------------------------------------------------
    
    gui, savepath, dg, dsp = argparse()

    # Testing and Raising Exceptions ----------------------------------
    trues = ["True", "true", "T", "t"]  # Can be changed 
    falses = ["False", "false", "F", "f"]   # Can be changed
    test(gui, savepath, dg, dsp, trues, falses)

    # Main call -------------------------------------------------------

    # Produce spreadsheet with or without GUI input
    if gui in trues:
        initgui()  # With GUI
    else:
        produceexcel()  # Without GUI
