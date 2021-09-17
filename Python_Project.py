#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 14 13:52:31 2021
Author: Surabhi S Nath
Matrikelnummer: 618777
"""
import requests
from bs4 import BeautifulSoup
import pandas as pd
import validators
from tkinter import *
from PyQt5.QtWidgets import QApplication, QLabel

def getrow(d, columns):
    return {i:d.get(i, "") for i in columns}

def saveexcel(df, excelfile, columns):
    writer = pd.ExcelWriter(excelfile, engine='xlsxwriter', options = {'strings_to_numbers': True})
    df.to_excel(writer, encoding='utf-8', index=False, sheet_name='HU Doctoral Project Details')
    workbook = writer.book
    worksheet = writer.sheets['HU Doctoral Project Details']
    header_format = workbook.add_format({'bold': True, 'align': 'center', 'valign': 'vcenter', 'border': 1})
    for col, value in enumerate(df.columns.values):
        worksheet.write(0, col, value, header_format)
    data_format = workbook.add_format({'text_wrap': True, 'align': 'justify', 'valign': 'top', 'border': 1})
    worksheet.set_column(0, len(columns) - 1, 60, data_format)
    writer.save()

def getdetails(student):
    datadict = {}
    datadict["Name"] = student.find('div', class_ = 'students-list-item-full-name').find('a').text 
    datadict["URLs"] = ""
    project_details = student.find('table')
    webnamestocolnames = {'Doctoral project': 'Doctoral Project Title', 'Description': 'Project Description'}
    
    for tr in project_details.findAll('tr'):
        td = tr.find('td')
        datadict[webnamestocolnames.get(tr.find('th').text, tr.find('th').text)] = td.text
        if tr.find('th').text == "E-mail" and td.text.find('@') >= 0 and td.text[td.text.find('@') + 1:].find('.') >= 0:
            email = td.text.replace("-please remove this text-", "")
            datadict["E-mail"] = tr.find('th').text + ": " + email + "\n"
        if td.find('a') and validators.url(td.find('a').get('href')):
            datadict["URLs"] += tr.find('th').text + ": " + td.find('a').get('href') + "\n"
    return datadict

def makedataframe(student_data, columns):
    dataframe = pd.DataFrame(columns = columns)
    
    for sid, student in enumerate(student_data):
        datadict = getdetails(student)
        row = getrow(datadict, columns)
        assert(len(row) == len(columns))
        dataframe.loc[sid,:] = row;
    
    return dataframe

def produceexcelgui(varlist, vartocol, master):
    columns = []
    for v, var in enumerate(varlist):
        if var.get():
            columns.append(vartocol[v+1])
    produceexcel(columns, excelfile)
    master.destroy()
    
def produceexcel(columns, excelfile):
    website = "http://www.mind-and-brain.de/people/doctoral-alumni/"
    website = requests.get(website)
    
    bs = BeautifulSoup(website.content, 'html.parser')
    student_data = bs.find_all('div', class_ = 'students-list-item-full clearfix')
    num_students = len(student_data)

    dataframe = makedataframe(student_data, columns)  
    print(dataframe.columns.values)
    saveexcel(dataframe, excelfile, columns)
    print("DONE")
    
     
def initgui():
    master = Tk()
    master.title("Web Scraper for M&B")
    Label(master, text="This application allows you to customise your spreadsheet. Select the information to include from the list below:").grid(row=0)
    vartocol = {1: "Name", 2: "E-mail", 3: "Doctoral Project Title", 4: "Project Description", 5: "Supervisors", 6: "Cohort", 7: "Funding", 8: "M&B topics", 9: "Institute", 10: "Status", 11: "Degrees obtained", 12: "Title", 13: "URLs"}
    num_possible_cols = 13
    varlist = []
    for i in range(num_possible_cols):
        varlist.append(IntVar(value=(vartocol[i+1] in defaultcolumns)))
        Checkbutton(master, text=vartocol[i + 1], variable=varlist[i]).grid(row=i + 1, sticky=W)
    
    button = Button(master, text='Generate spreadsheet', width=25, command = lambda : produceexcelgui(varlist, vartocol, master)).grid(row=14)
    master.mainloop()

if __name__ == "__main__":
    gui = True
    defaultcolumns = ['Name', 'E-mail', 'Doctoral Project Title', 'Project Description', 'Supervisors', 'Cohort', 'URLs']
    excelfile = "/Users/surabhisnath/Desktop/Python/excel.xlsx"
    if gui == True:
        initgui()
    else:
        produceexcel(defaultcolumns, excelfile)
    