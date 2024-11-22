# written by Roberto April 2023

from subprocess import call

import IO_csv_util
import IO_files_util
import charts_util

def run(inputFilename, outputDir,
        csv_field_visualization_var,
        points_var,
        split_data_byCategory_var,
        csv_field_boxplot_var,
        csv_field_boxplot_color_var,
        # TODO:
        inputFileData
        ):

    filesToOpen = []


    # if extra_GUIs_var.get()==False and csv_field_visualization_var == '':
    #     print("Warning, No csv file field to be used for visualization (Y-axis) has been selected.\n\nPlease, use the dropdown menu of the 'csv file field for visualization (Y-axis)' widget to select the desired field and try again.")
    #     return

    # if extra_GUIs_var.get()==False and visualizations_menu_var=='':
    #     print("Warning, No visualization option has been selected.\n\nPlease, use the dropdown menu of the 'Visualization options' widget to select the desired visualization option and try again.")
    #     return

    # if csv_field_visualization_var=='':
    #     print("Warning, No Y-axis variable has been selected.\n\nPlease, use the dropdown menu to select the csv file column to be used as Y-axis and try again.")
    #     return
    
    # boxplots --------------------------------------------------------------------------------

    if points_var == '':
        #mb.showwarning(title='Warning', message='The "Boxplots" option requires a "Data points" variable.\n\nPlease, use the dropdown menu to select a "Data points" option and try again.')
        return

    if split_data_byCategory_var and csv_field_boxplot_var=='':
        #mb.showwarning(title='Warning',
                        #message='The "Split data by category" Boxplots option requires a second CATEGORICAL csv file field for processing.\n\nPlease, use the dropdown menu to select the csv file field and try again.')
        return

    outputFilename = IO_files_util.generate_output_file_name(inputFilename, '', outputDir,
                                                                '.html', 'boxplot')
    # You cannot keep it as float inside the csv. The csv will treat everything as strings.
    # https://stackoverflow.com/questions/65393774/writing-floats-into-a-csv-file-but-floats-become-a-string
    outputfilename = charts_util.boxplot(inputFileData, outputFilename, csv_field_visualization_var,
                                points_var, split_data_byCategory_var, csv_field_boxplot_var, csv_field_boxplot_color_var) #, points_var, color=None)
    if outputfilename!='':
        filesToOpen.append(outputfilename)