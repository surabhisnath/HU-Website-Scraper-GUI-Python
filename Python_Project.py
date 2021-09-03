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

def getrow(d):
    return {i:d.get(i, "") for i in columns}

def saveexcel(df, excelfile):
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

def makedataframe(student_data):
    dataframe = pd.DataFrame(columns = columns)
    
    for sid, student in enumerate(student_data):
        datadict = getdetails(student)
        row = getrow(datadict)
        assert(len(row) == len(columns))
        dataframe.loc[sid,:] = row;
    
    return dataframe

def produceexcel(columns, excelfile):
    website = "http://www.mind-and-brain.de/people/doctoral-alumni/"
    website = requests.get(website)
    
    bs = BeautifulSoup(website.content, 'html.parser')
    student_data = bs.find_all('div', class_ = 'students-list-item-full clearfix')
    num_students = len(student_data)

    dataframe = makedataframe(student_data)  
    print(dataframe.columns.values)
    saveexcel(dataframe, excelfile)

def initgui():
    master = Tk()
    var1 = IntVar()
    Checkbutton(master, text='male', variable=var1).grid(row=0, sticky=W)
    var2 = IntVar()
    Checkbutton(master, text='female', variable=var2).grid(row=1, sticky=W)
    mainloop()

if __name__ == "__main__":
    columns = ['Name', 'E-mail', 'Doctoral Project Title', 'Project Description', 'Supervisors', 'Cohort', 'URLs']
    excelfile = "/Users/mac/Desktop/excel.xlsx"
    initgui()
    #produceexcel(columns, excelfile)
    