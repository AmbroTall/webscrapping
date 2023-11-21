import glob
import os

import pandas as pd
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows  # Import dataframe_to_rows from openpyxl.utils

# List of CSV files
file_paths = glob.glob('/home/ambrose/PycharmProjects/WebScraping/webscrapping/SoccerArb/TeamNames/*.csv')

# Create a new Excel workbook
excel_file = Workbook()

# Iterate through CSV files and create worksheets
for csv_file in file_paths:
    df = pd.read_csv(csv_file)

    # Extract the base filename (without the path) and remove the ".csv" extension
    base_filename = os.path.basename(csv_file)
    worksheet_name = os.path.splitext(base_filename)[0]

    # Create a sanitized worksheet name (replace invalid characters with underscores)
    worksheet_name = worksheet_name.replace('/', '_')
    sheet = excel_file.create_sheet(title=worksheet_name)  # Create a new worksheet

    # Write the DataFrame to the worksheet
    for row in dataframe_to_rows(df, index=False, header=True):
        sheet.append(row)

    # Adjust column width to fit the content
    for column in sheet.columns:
        max_length = 0
        column = [cell for cell in column]
        for cell in column:
            try:
                if len(str(cell.value)) > max_length:
                    max_length = len(cell.value)
            except:
                pass
        adjusted_width = (max_length + 2)
        sheet.column_dimensions[column[0].column_letter].width = adjusted_width

# Save the Excel file
excel_file.save('combined_data.xlsx')
