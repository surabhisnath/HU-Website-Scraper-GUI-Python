# Enclosed in the folder are the following files:
	
1. webscraper.py - main code to be executed
2. helpers.py - file containing helper functions
3. requirements.txt - specifies the external packages required to run the code
4. README.md - this file

# Description:

The code is an implementation of Project 3: The Internet - Web Scraping on the Mind and Brain Doctoral Alumni webpage hosted at http://www.mind-and-brain.de/people/doctoral-alumni/. The student information acquired from the webpage is saved to an EXCEL spreadsheet. A Python GUI is also implemented to give the user more control on the information to be saved onto the spreadsheet.
The code was implemented and tested on MAC OS 2021 Big Sur operating system with M1 architecture, Python version 3.8.8, Anaconda.

# Executing the code:

The code MUST be executed from the command line. This is a necessary for 2 reasons. One, the GUI package "Tkinter" does not interact well with IDEs such as Spyder or PyCharm. And two, the user can pass command line arguments when the code is executed from command line. 

The command can be executed as follows:

```
python webscraper.py --gui=[true or false] --savepath=[desired path to save the excel spreadsheet]
```

The `--gui` and `--savepath` flags are optional.	
[Note: there should be no spaces before or after the = sign as the command line interpreters splits arguments by spaces]

### GUI Argument

The `--gui` flag determines whether or not to display the GUI. Without the GUI, the default columns mentioned in the project instructions (namely, 1 - student name, 2 - title of their doctoral project, 3 - description of their doctoral project, 4 - list of supervisors, 5 - cohort year, 6 - URLs of any websites they have listed) are written onto the spreadsheet. With the GUI however, the user can customise the spreadsheet by choosing the columns to include or exclude.

The GUI argument can be specified in one of the following ways: 
1. `--gui=True`
2. `--gui=true`
3. `--gui=T`
4. `--gui=t`
5. `--gui=False`
6. `--gui=false`
7. `--gui=F`
8. `--gui=f`

where 1., 2., 3., 4. result in the GUI being displayed whereas 5, 6., 7., 8. do not display the GUI.
If no `--gui` flag is specified, the default is considered to the true and the GUI is displayed.

### Savepath Argument

The `--savepath` flag can be used to specify the location of where the spreadsheet should be saved.
The path must include the path to the directory along with the filename. The paths can be absolute or relative.
Examples of valid usage:
1. `--savepath=/Users/surabhisnath/Desktop/excel.xlsx`
2. `--savepath=./excel.xlsx`
3. `--savepath="../alumnidetails.xlsx"`

If no `--savepath` flag is specified, the default savepath is set to current directory and the default filename "MB_DoctoralAlumni.xlsx" is used.

# Notes:

* The code has been formatted as per the PEP8 guidelines.
* Different steps are handled by different functions with helper functions defined in helpers.py (in order to not clutter the main file).
* Testing and error handling is implemented using asserts, exceptions, try/catch blocks. Exceptions are raised in the following conditions:
	- Incorrect GUI argument specified
	- Invalid savepath specified
	- No filename specified along with path
	- Invalid filename extension specified
* Default values are all initialised in the main and can be changed easily. These include:
	- Default spreadsheet columns - Name, Doctoral Project Title, Project Description, Supervisors, Cohort, URLs
	- Default GUI argument - set to true
	- Default savepath - set to current directory from where the code is executed
	- Default filename - MB_DoctoralAlumni.xlsx
	- List of strings for which GUI parameter is considered true - set to ["True", "true", "T", "t"] 
	- List of strings for which GUI parameter is considered false - set to ["False", "false", "F", "f"] 
* Spreadsheet formatting
	- Why Excel (as opposed to csv or other formats)? The excel file i.e., .xlsx was found to be optimal to write multi-line data with possible non-ascii German/French alphabets.
	- Spreadsheet was formatted so that the information can be displayed neatly. The formatting options can be modified by changing the variable values in the saveexcel() function. 
* Print statements are used at each step (eg.: Displaying GUI..., Saving spreadsheet... etc.) for user understanding and code transparency.
* Comments are used to explain all parts of the code and each function includes a docstring.
* Since there were no strict rules on how the spreadsheet should be formatter, I have used my freedom in the following ways:
	- All URLs such as Researchgate, Academia.edu etc combined onto one column "URLs" where only valid URLs were written
	- A separate email column was created where only valid E-mail IDs were written
* All code is original and No code snippets were borrowed from anywhere.

# Author details
Name: Surabhi S Nath

Matrikelnummer: 618777

Program: M&B MSc., Track Brain
