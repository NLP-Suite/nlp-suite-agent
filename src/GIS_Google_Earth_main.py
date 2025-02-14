# Roberto Franzosi, Jack Hester
# Edited by Roberto Franzosi and Yuhang Feng Fall 2019-Spring 2020
# Rewritten by Roberto Franzosi May, September 2020

import sys
import IO_libraries_util


import os

import io
from PIL import Image, ImageTk
# tkcolorpicker requires tkinter and pillow to be installed (https://libraries.io/pypi/tkcolorpicker)
# tkcolorpicker is both the package and module name
# pillow is the Python 3 version of PIL which was an older Python 2 version
# PIL being the commmon module for both packages, you need to check for PIL and trap PIL to tell the user to install pillow
import CoNLL_util

from urllib.request import urlopen # used to call Google website to display a selected pin

import GUI_IO_util
import GIS_Google_pin_util
import IO_files_util
import GIS_file_check_util
import GIS_pipeline_util
import IO_csv_util
import reminders_util

# RUN section ______________________________________________________________________________________________________________________________________________________

# ISO 3166-1 defines two-letter, three-letter, and three-digit country codes.
# python-iso3166 is a self-contained module that converts between these codes
#   and the corresponding country name.
# import iso3166 #pip install
# from iso3166 import countries


def run(inputFilename, inputDir, outputDir, openOutputFiles, chartPackage, dataTransformation,
            encoding_var,
            locationColumnName,
            date_var, date_format_var,
            group_var, group_number_var, group_values_entry_var_list, group_label_entry_var_list,
            icon_var_list, specific_icon_var_list,
            name_var_list, scale_var_list, color_var_list, color_style_var_list,
            description_csv_field_var, bold_var_list, italic_var_list,
            description_var_list, description_csv_field_var_list, heat_map_var):

    config_filename = "NLP_default_IO_config.csv"

    filesToOpen = []
    inputIsCoNLL = False

    if locationColumnName=='':
        print("No location column selected, No csv column containing location names has been selected.\n\nPlease, select a column and try again.")
        return

    inputIsCoNLL, inputIsGeocoded, withHeader, headers, datePresent, filenamePositionInCoNLLTable=GIS_file_check_util.CoNLL_checker(inputFilename)

    if withHeader==True:
        locationColumnNumber=IO_csv_util.get_columnNumber_from_headerValue(headers,locationColumnName, inputFilename)

    # Word is the header from Stanford CoreNLP NER annotator
    if not 'Location' in headers and not 'Word' in headers and not 'NER' in headers:
        print("Warning, The selected input csv file does not contain the word 'Location' or 'NER' in its headers.\n\nThe GIS algorithms expect in input either\n   1. a csv file\n      a. with a column of locations (with header 'Location') to be geocoded and mapped;\n      b. a csv file with a column of locations (with header 'Location') already geocoded and to be mapped (this file will also contain latitudes and longitudes, with headers 'Latitude' and 'Longitude').\n\nThe RUN button is disabled until the expected csv file is seleted in input.\n\nPlease, select the appropriate input csv file and try again.")
        return

    # if restrictions_checker(inputFilename,inputIsCoNLL,numColumns,withHeader,headers,locationColumnName)==False:
    # 	return

    if group_var == 1 and group_number_var == 1:
        print("Only One Group Chose for Multiple Group Mapping The group box is ticked for multiple groups mapping but only one group is chose.\n\nPlease, check your input and try again.")
        return

    icon_csv_field_var_name = True

    if group_var == 1 and len(icon_csv_field_var_name) < 1:
        print("No CSV field for Group Split Criterion Found The group box is ticked for multiple groups mapping but no csv field is specified for group splitting criterion.\n\nPlease, check your input and try again. ")
        return

    datePresent=False
    geocoder='Nominatim'
    encodingValue='utf-8'

    # reminders_util.checkReminder(scriptName, reminders_util.title_options_geocoder,
    #                              reminders_util.message_geocoder, True)

    country_bias = ''
    area_var = ''
    restrict = False

    # create a subdirectory of the output directory
    outputDir = IO_files_util.make_output_subdirectory(inputFilename, inputDir, outputDir, label='GIS-GEP',
                                                            silent=True)
    if outputDir == '':
        return
    if heat_map_var:
        mapping_package = 'Google Earth & Google Maps'
    else:
        mapping_package = 'Google Earth'
    filesToOpen = GIS_pipeline_util.GIS_pipeline(config_filename,
                                       inputFilename, inputDir, outputDir,
                                       geocoder, mapping_package, chartPackage, dataTransformation,
                                       datePresent,
                                       country_bias,
                                       area_var,
                                       restrict,
                                       locationColumnName,
                                       encodingValue,
                                       group_var, group_number_var, group_values_entry_var_list, group_label_entry_var_list,
                                       icon_var_list, specific_icon_var_list,
                                       name_var_list, scale_var_list, color_var_list, color_style_var_list,
                                       bold_var_list, italic_var_list,
                                       description_var_list, description_csv_field_var_list)

    return filesToOpen

