"""
@Author: Surabhi S Nath
@Matrikelnummer: 618777
"""

# Imports
import pandas as pd
import validators


def getrow(d, columns):
    """
    Gets relevant information from student dictionary based on columns to include in spreadsheet

    Parameters:
        d (dict): contains one student's information as dictionary
        columns (list): list of columns to write on spreadsheet

    Returns:
        dict: relevant subset of dictionary based on columns to write on spreadsheet

    """

    return {i: d.get(i, "") for i in columns}


def saveexcel(df, savepath, columns):
    """
    Saves excel spreadsheet to specified location

    Parameters:
        df (pd.Dataframe): Number of dice to roll
        savepath (str): Location to save spreadsheet
        columns (list): list of columns to write on spreadsheet

    """

    print("Saving spreadsheet...")

    # Initialize writer
    writer = pd.ExcelWriter(savepath, engine='xlsxwriter', options={'strings_to_numbers': True})
    df.to_excel(writer, encoding='utf-8', index=False, sheet_name='HU Doctoral Student Details')
    workbook = writer.book
    worksheet = writer.sheets['HU Doctoral Student Details']

    # Format spreadsheet design
    header_format = workbook.add_format({'bold': True, 'align': 'center', 'valign': 'vcenter'})
    for col, value in enumerate(df.columns.values):
        worksheet.write(0, col, value, header_format)
    data_format = workbook.add_format({'text_wrap': True, 'align': 'justify', 'valign': 'top'})
    worksheet.set_column(0, len(columns) - 1, 60, data_format)

    writer.save()


def getdetails(student):
    """
    Parses all information for one student

    Parameters:
        student (bs4.element.Tag): student bs4 object

    Returns:
        dict: contains student information as dictionary

    Examples: getdetails(bs4.element.Tag) {'Name': 'Sanders, Lia', 'URLs': 'Researchgate:
    https://www.researchgate.net/profile/Lia_Sanders\n', 'Doctoral Project Title': 'Visual spatio-temporal
    integration in patients with Schizophrenia', 'Project Description': 'General theories of brain function assert
    that the brain works like an inference machine, whereby prior expectations are used to derive perceptual
    experiences from the sensory inputs. Impaired perceptual inference has been suggested as one possible causal
    factor underlying positive symptoms, and in particular delusions, in schizophrenia. According to this framework,
    delusional explanations are thought to reflect the attempt to cope with unusual percepts resulting from such
    impaired perceptual inference. During my PhD, we conducted a series of clinical studies testing this theoretical
    model. Methods: psychophysics, EEG, fMRI. \r\n', 'Funding': 'Mind and Brain scholarship\nMind and Brain
    postdoctoral scholarship', 'Supervisors': 'Prof. Dr. Philipp Sterzer\r\nProf. Dr. Andreas Heinz\r\nProf. Dr.
    Norbert Kathmann', 'M&B topics': 'Topic 1: Perception, attention, consciousness\nTopic 5: Brain disorders and
    mental dysfunction', 'Degrees obtained': 'MD, Federal University of Ceará – Fortaleza, Brazil', 'Institute':
    'Klinik für Psychiatrie, CCM, Charité – Universitätsmedizin Berlin', 'Title': 'Dr.', 'Cohort': '2009',
    'Status': 'Alumna', 'Researchgate': 'https://www.researchgate.net/profile/Lia_Sanders'}

    """

    # Initialize dict
    datadict = {"Name": student.find('div', class_='students-list-item-full-name').find('a').text, "URLs": ""}

    project_details = student.find('table')
    webnamestocolnames = {'Doctoral project': 'Doctoral Project Title',
                          'Description': 'Project Description'}  # Maps html tag name to column names

    # Populates dictionary
    for tr in project_details.findAll('tr'):
        td = tr.find('td')
        if tr.find('th').text == "E-mail" and td.text.find('@') >= 0 and td.text[td.text.find('@') + 1:].find('.') >= 0:
            towrite = td.text.replace("-please remove this text-", "")
        elif tr.find('th').text == "M&B topics":
            towrite = td.text[0] + td.text[1:].replace('Topic', '\nTopic')
        else:
            towrite = td.text

        datadict[webnamestocolnames.get(tr.find('th').text, tr.find('th').text)] = towrite

        # Writes url only if valid
        if td.find('a') and validators.url(td.find('a').get('href')):
            datadict["URLs"] += tr.find('th').text + ": " + td.find('a').get('href') + "\n"

    return datadict


def makedataframe(student_data, columns):
    """
    Creates and populates dataframe with scraped data

    Parameters:
        student_data (list): student information extracted from website
        columns (list): List of columns to write on spreadsheet

    Returns:
        pd.Dataframe: populated dataframe

    """

    print("Making dataframe...")
    dataframe = pd.DataFrame(columns=columns)

    # Writes one row for each student
    for sid, student in enumerate(student_data):
        datadict = getdetails(student)
        row = getrow(datadict, columns)
        assert (len(row) == len(columns))
        dataframe.loc[sid, :] = row

    return dataframe
