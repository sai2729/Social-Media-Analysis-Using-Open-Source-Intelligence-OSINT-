from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
import pandas as pd
import os

# Create your views here.
excel_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'Reddit.xlsx')

def reddit(request):
    # Load the Excel file
    excel_file = pd.ExcelFile(excel_file_path)

    # Get the sheet names
    sheet_names = excel_file.sheet_names

    # Create an empty dictionary to store the submission counts for each sheet
    submission_counts = {}
    indAttacksPieChartDataList = dict()
    indAttackBarChartData = dict()

    # Loop through each sheet
    for sheet_name in sheet_names:
        # Load the sheet into a DataFrame
        df = pd.read_excel(excel_file_path, sheet_name=sheet_name)

        # Count the number of submissions in the sheet
        num_submissions = df[df['type'] == 'submission'].shape[0]

        indAttackPieChartData = df.groupby('type').size()
        indAttacksPieChartDataList[sheet_name]=indAttackPieChartData.to_list()

        # Add the submission count to the dictionary
        submission_counts[sheet_name] = num_submissions

    # Sort the submission counts in descending order
    submission_counts = dict(sorted(submission_counts.items(), key=lambda item: item[1], reverse=True))

    
    df = pd.read_excel(excel_file_path, sheet_name=None)

    for sheet_name in df:
        # Create a new column 'day_of_week'
        df[sheet_name]['day_of_week'] = pd.to_datetime(df[sheet_name]['date']).dt.day_name()

        # Count the number of posts on each day of the week
        counts = df[sheet_name]['day_of_week'].value_counts()

        indAttackBarChartData[sheet_name]=counts


    # Create a dictionary of context data to pass to the template
    context = {
        'attacks':submission_counts,
        'indAttacksPieChartData':indAttacksPieChartDataList,
        'indAttacksBarChartData':indAttackBarChartData
    }
    print(context)
    # Render the template with the context data
    return render(request, 'reddit.html', context)
