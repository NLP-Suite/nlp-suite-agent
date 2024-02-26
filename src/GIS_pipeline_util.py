# Cynthia Dong May 2020
# Cynthia Dong May 2020
# Roberto Franzosi September 2020
# Mino Cha September 2022

import os
import pandas as pd
import tkinter.messagebox as mb
import tkinter as tk
import csv

import IO_files_util
import IO_csv_util
import GUI_IO_util
import reminders_util
import GIS_file_check_util
import GIS_location_util
import GIS_geocode_util
import GIS_KML_util
import GIS_Google_Maps_util
import IO_libraries_util
import config_util
import TIPS_util
import constants_util
import charts_util

# The script is used by SVO_main and by Google_Earth_main to run a csv file that 1. needs geocoding; 2. mapping geocoded location onto Google Earth Pro.
import IO_user_interface_util

# Google_config: 'Google-geocode-API_config.csv' or 'Google-Maps-API_config.csv'
def getGoogleAPIkey(window,Google_config, display_key=False):
    configFilePath = os.path.join(GUI_IO_util.configPath, Google_config)
    configAPIKey = []
    if os.path.isfile(configFilePath):
        f_config = open(configFilePath, 'r', encoding='utf-8', errors='ignore')
        configAPIKey = f_config.readlines()
    if len(configAPIKey) == 0 or display_key:
        if 'Maps' in Google_config:
            msg='Maps'
            config_file = 'Google-Maps-API_config.csv'
        else:
            msg='geocoder'
            config_file = 'Google-geocode-API_config.csv'
        if len(configAPIKey) == 0:
            message = 'No config file ' + config_file + ' was found in the config subfolder of the NLP-SUIte.\n\nGoogle ' + msg + ' requires an API key (in fact, Google requires two separate free API keys, one for Google geocoder, the other for Google Maps).'
            if 'geocode' in Google_config:
                message = message + '\n\nWithout a Google geocoder API key you can only geocode locations with Nominatim.'
            if 'Maps' in Google_config:
                message = message + '\n\nWithout a Google Maps API key you can only map locations in Google Earth Pro.'
            message = message + '\n\nPlease, read the TIPS file TIPS_NLP_GIS_Google API Key.pdf on how to obtain free Google API keys.\n\nWould you like to open the TIPS file now?'
            answer = tk.messagebox.askyesno("Warning",message)
            if answer:
                TIPS_util.open_TIPS('TIPS_NLP_GIS_Google API Key.pdf')
        if 'Maps' in Google_config:
            config_type='Maps'
        else:
            config_type = 'geocoder'
        if display_key and len(configAPIKey) > 0:
            key=configAPIKey[0]
        else:
            key=''
        if key=='':
            message = "Enter the Google " + config_type + " API key"
        else:
            message = "Enter a new Google " + config_type + " API key if you want to change the key"
        key, string_out = GUI_IO_util.enter_value_widget(message, 'Enter', 1, key, 'API key', key)
        # save the API key
        if key!='':
            config_util.Google_API_Config_Save(window,Google_config, key)
    else:
        key = configAPIKey[0]
    return key


# the list of arguments reflect the order of widgets in the Google_Earth_main GUI
# processes one file at a time
def GIS_pipeline(window, config_filename, inputFilename, inputDir, outputDir,
                        geocoder, mapping_package, chartPackage, dataTransformation,
                        datePresent,
                        country_bias,
                        area_var,
                        restrict,
                        locationColumnName,
                        encodingValue,
                        group_var, group_number_var, group_values_entry_var_list, group_label_entry_var_list,
                        icon_var_list, specific_icon_var_list, # pushpin, red
                        name_var_list, scale_var_list, color_var_list, color_style_var_list,
                        bold_var_list, italic_var_list,
                        description_var_list=[], description_csv_field_var_list=[]):

    filesToOpen=[]

    # if datePresent:
    #     date, dateStr = IO_files_util.getDateFromFileName(inputFilename, dateFormat, dateDelimiter, int(datePosition))
        # if date == '':
        #     continue  # TODO: Warn user this file has a bad date; done in getDate
        # else:

    inputIsCoNLL, inputIsGeocoded, withHeader, headers, datePresent, filenamePositionInCoNLLTable = GIS_file_check_util.CoNLL_checker(inputFilename)

    locationColumnNumber=IO_csv_util.get_columnNumber_from_headerValue(headers,locationColumnName, inputFilename)

    if locationColumnNumber == None:
        return

    dateColumnNumber = -1
    if datePresent == True:
        dateColumnNumber=IO_csv_util.get_columnNumber_from_headerValue(headers,"Date", inputFilename)

    outputCsvLocationsOnly = ''

    software=config_filename.replace('_config.csv','')
    # check that the GEP has been setup
    GoogleEarthProDir, existing_software_config, errorFound = IO_libraries_util.external_software_install('GIS_pipeline_util',
                                                                                         'Google Earth Pro',
                                                                                         '',
                                                                                         silent=False, errorFound=False)

    if GoogleEarthProDir == None or GoogleEarthProDir == '':
        return

    startTime = IO_user_interface_util.timed_alert(window, 2000, 'Analysis start', 'Started running GIS pipeline at',
                                                   True, '', True, '', False)

    head, scriptName = os.path.split(os.path.basename(__file__))
    reminders_util.checkReminder(scriptName,
                                 reminders_util.title_options_GIS_timing,
                                 reminders_util.message_GIS_timing,
                                 True)

    #
    # ------------------------------------------------------------------------------------
    # get locations
    # ------------------------------------------------------------------------------------

    reminders_util.checkReminder(scriptName,
                                 reminders_util.title_options_GIS_MWL,
                                 reminders_util.message_GIS_MWL,
                                 True)

    if inputIsCoNLL == True:
        outputCsvLocationsOnly = IO_files_util.generate_output_file_name(inputFilename, '', outputDir, '.csv', 'GIS',
                                                                   'NER_locations', '', '', '', False, True)
        locations = GIS_location_util.extract_NER_locations(window, inputFilename, encodingValue,
                                                            datePresent)
    else:
        # locations is a double list of names of locations in the form [['United States','COUNTRY']]
        locations = GIS_location_util.extract_csvFile_locations(window, inputFilename, withHeader, locationColumnNumber, encodingValue, datePresent, dateColumnNumber)
        if locations == None or len(locations) == 0:
            return
        if not inputIsGeocoded and geocoder == 'Nominatim':
            changed = False
            if datePresent:
                nom_df = pd.DataFrame(locations, columns=['Location', 'Date', 'NER']) if len(locations[0])==3 else pd.DataFrame(locations, columns=['Location', 'Index', '0', 'NER'])
            else:
                nom_df = pd.DataFrame(locations, columns=['Location', 'NER']) if len(locations[0])==2 else pd.DataFrame(locations, columns=['Location', 'Index', '0', 'NER'])
            if nom_df is None:
                return
            drop_idx = []
            changed_idx = {}
            for i,row in nom_df.iterrows():
                # if i!=0 and row[0] in constants_util.continents and nom_df.at[i-1, 'Location'] in constants_util.directions:
                if i!=0 and \
                    (row[0] == 'Africa' or \
                    row[0] == 'Antarctica' or \
                    row[0] == 'Asia' or \
                    row[0] == 'Australia' or \
                    row[0] == 'Europe' or \
                    row[0] == 'Oceania' or \
                    row[0] == 'America'):
                    nom_df.at[i, 'Location'] = nom_df.at[i-1, 'Location'] + ' ' + row[0]
                    drop_idx.append(i-1)
                    changed_idx[i] = nom_df.at[i, 'Location']
                    changed = True
            if changed:
                tmp_df = pd.read_csv(inputFilename,encoding='utf-8',on_bad_lines='skip')
                for k,v in changed_idx.items():
                    tmp_df.at[k, 'Location'] = v
                tmp_df = tmp_df.drop(drop_idx)
                tmp_df.to_csv(inputFilename, index=False) # TODO: drop a index column, which will produce error with producing KML (if selected).
            nom_df = nom_df.drop(drop_idx)
            locations = [row.values.tolist() for _,row in nom_df.iterrows()]

    if locations == None or len(locations) == 0:
        return

    # ------------------------------------------------------------------------------------
    # geocode (the new geocoding function also creates the kml Google Earth Pro map file)
    # ------------------------------------------------------------------------------------

    if geocoder!='':
        geoName = 'geo-' + str(geocoder[:3])
    else:
        geoName = 'geo-'
    geocodedLocationsOutputFilename = IO_files_util.generate_output_file_name(inputFilename, '', outputDir, '.csv',
                                                                              'GIS',
                                                                              geoName, locationColumnName, '', '',
                                                                              False,
                                                                              True)
    #@@@
    # must be the same name as set in GIS_geocode_util
    # locationsNotFoundoutputFilename = IO_files_util.generate_output_file_name(inputFilename, '', outputDir, '.csv',
    #                                                                           'GIS',
    #                                                                           geoName, 'not_found',
    #                                                                           locationColumnName, '',
    #                                                                           False, True)
    locationsNotFoundoutputFilename = IO_files_util.generate_output_file_name(inputFilename, '', outputDir, '.csv',
                                                                              'GIS',
                                                                              geoName, '',
                                                                              locationColumnName, '',
                                                                              False, True)
    locationsNotFoundoutputFilename=locationsNotFoundoutputFilename.replace('LOCATIONS','LOCATIONS_not-found')

    geocodedLocationsOutputFilename=inputFilename

    kmloutputFilename = geocodedLocationsOutputFilename.replace('.csv', '.kml')

    if not inputIsGeocoded:
        geocodedLocationsOutputFilename, \
        locationsNotFoundoutputFilename, \
        locationsNotFoundNonDistinctoutputFilename, \
        kmloutputFilename = \
            GIS_geocode_util.geocode(window, locations, inputFilename, outputDir,
                locationColumnName,geocoder,country_bias, area_var,restrict,
                encodingValue)

        if kmloutputFilename!='':
            filesToOpen.append(kmloutputFilename)
        if geocodedLocationsOutputFilename=='' and locationsNotFoundoutputFilename=='': #when geocoding cannot run because of internet connection
            return
    else:
        kmloutputFilename = GIS_geocode_util.process_geocoded_data_for_kml(window, locations, inputFilename, outputDir,
                                      locationColumnName, encodingValue, geocoder)
        if kmloutputFilename!='':
            filesToOpen.append(kmloutputFilename)

    if len(locations) > 0 and inputIsCoNLL == True:
        # locations contains the following values:
        #	location, sentence, filename, date (if present)
        filesToOpen.append(outputCsvLocationsOnly)
        if datePresent == True:
            # always use the location_var variable passed by algorithms to make sure locations are then matched
            locations.insert(0, ['Location', 'NER', 'Sentence ID', 'Sentence', 'Document ID', 'Document',  'Date'])
        else:
            # always use the location_var variable passed by algorithms to make sure locations are then matched
            locations.insert(0, ['Location', 'NER', 'Sentence ID', 'Sentence', 'Document ID', 'Document'])
        IO_csv_util.list_to_csv(window, locations, outputCsvLocationsOnly)

    # the plot of locations frequencies is done in the CoreNLP_annotator_util
    # the plot of location NERs frequencies is done in the function CoreNLP_annotator_util
    # need to plot locations geocoded and not geocoded

    nRecordsFound, nColumns  = IO_csv_util.GetNumberOf_Records_Columns_inCSVFile(geocodedLocationsOutputFilename)
    if geocodedLocationsOutputFilename != '' and nRecordsFound >0:
        # set inputIsGeocoded
        inputIsGeocoded=True
        filesToOpen.append(geocodedLocationsOutputFilename)
        if chartPackage!='No charts':
            if geocoder=='':
                chart_title = 'Frequency of Locations'
            else:
                chart_title = 'Frequency of Locations Found by ' + geocoder

            outputFiles = charts_util.visualize_chart(chartPackage, dataTransformation,
                                                               geocodedLocationsOutputFilename,
                                                               outputDir,
                                                               columns_to_be_plotted_xAxis=[], columns_to_be_plotted_yAxis=['Location'],
                                                               chart_title=chart_title,
                                                               # count_var = 1 for columns of alphabetic values
                                                               count_var=1, hover_label=[],
                                                               outputFileNameType='', #'found',  # 'NER_tag_bar',
                                                               column_xAxis_label='Locations',
                                                               groupByList=[],
                                                               plotList=[],
                                                               chart_title_label='')

            if outputFiles!=None:
                if len(outputFiles) > 0:
                    # must split the file in case both path and filename contain the word LOCATION
                    head, tail = os.path.split(outputFiles[0])
                    tail = tail.replace('LOCATIONS', 'LOCATIONS_found')

                    # change the filename on the computer drive
                    os.rename(outputFiles[0], head+os.sep+tail)
                    outputFiles[0] = head+os.sep+tail
                    filesToOpen.extend(outputFiles)

            outputFiles = charts_util.visualize_chart(chartPackage, dataTransformation,
                                                               geocodedLocationsOutputFilename,
                                                               outputDir,
                                                               columns_to_be_plotted_xAxis=[], columns_to_be_plotted_yAxis=['Country from Geocoder'],
                                                               chart_title='Frequency of Countries Found by ' + geocoder,
                                                               # count_var = 1 for columns of alphabetic values
                                                               count_var=1, hover_label=[],
                                                               outputFileNameType='', #'found',  # 'NER_tag_bar',
                                                               column_xAxis_label='Country found by ' + geocoder,
                                                               groupByList=[],
                                                               plotList=[],
                                                               chart_title_label='')

            if outputFiles!=None:
                if isinstance(outputFiles, str):
                    filesToOpen.append(outputFiles)
                else:
                    filesToOpen.extend(outputFiles)

    if not inputIsGeocoded:
        if locationsNotFoundNonDistinctoutputFilename!='':
            nRecordsNotFound, nColumns  = IO_csv_util.GetNumberOf_Records_Columns_inCSVFile(locationsNotFoundNonDistinctoutputFilename)
            if nRecordsNotFound>0:
                filesToOpen.append(locationsNotFoundNonDistinctoutputFilename)
                if chartPackage!='No charts':

                    outputFiles = charts_util.visualize_chart(chartPackage, locationsNotFoundNonDistinctoutputFilename,
                                                                           outputDir,
                                                                           columns_to_be_plotted_xAxis=[], columns_to_be_plotted_yAxis=['Location'],
                                                                           chart_title='Frequency of Locations not Found by ' + geocoder,
                                                                           # count_var = 1 for columns of alphabetic values
                                                                           count_var=1, hover_label=[],
                                                                           outputFileNameType='', #'not-found',  # 'NER_tag_bar',
                                                                           column_xAxis_label='Locations',
                                                                           groupByList=[],
                                                                           plotList=[],
                                                                           chart_title_label='')
                    if outputFiles!=None:
                        if len(outputFiles) > 0:
                            # must split the file in case both path and filename contain the word LOCATION
                            head, tail = os.path.split(outputFiles[0])
                            tail = tail.replace('LOCATIONS', 'LOCATIONS_not_found')
                            # change the filename on the computer drive
                            outputFiles[0] = os.rename(outputFiles[0], head + os.sep + tail)
                            filesToOpen.extend(outputFiles)

                # save to csv file and run visualization
                # outputFilename= IO_files_util.generate_output_file_name(inputFilename, '', outputDir, '.csv','found-notFound')
                outputFilename= IO_files_util.generate_output_file_name(inputFilename, '', outputDir, '.csv')
                outputFilename = outputFilename.replace('LOCATIONS','LOCATIONS_found-notFound')
                with open(outputFilename, "w", newline="", encoding='utf-8', errors='ignore') as csvFile:
                    writer = csv.writer(csvFile)
                    writer.writerow(
                        ["Number of Distinct Locations Found by Geocoder ", "Number of Distinct Locations NOT Found by Geocoder"])
                    writer.writerow([nRecordsFound, nRecordsNotFound])
                    csvFile.close()
                # no need to display since the chart will contain the values
                # return_files.append(outputFilename)
                columns_to_be_plotted_yAxis=["Number of Distinct Locations Found by Geocoder ", "Number of Distinct Locations NOT Found by Geocoder"]
                outputFiles = charts_util.visualize_chart(chartPackage, dataTransformation,
                                                                   outputFilename,
                                                                   outputDir,
                                                                   columns_to_be_plotted_xAxis=[], columns_to_be_plotted_yAxis=columns_to_be_plotted_yAxis,
                                                                   chart_title='Number of DISTINCT Locations Found and not Found by Geocoder',
                                                                   # count_var = 1 for columns of alphabetic values
                                                                   count_var=0, hover_label=[],
                                                                   outputFileNameType='',
                                                                   column_xAxis_label='Geocoder results',
                                                                   groupByList=[],
                                                                   plotList=[],
                                                                   chart_title_label='')
                if outputFiles!=None:
                    if isinstance(outputFiles, str):
                        filesToOpen.append(outputFiles)
                    else:
                        filesToOpen.extend(outputFiles)

    nRecordsFound, nColumns = IO_csv_util.GetNumberOf_Records_Columns_inCSVFile(geocodedLocationsOutputFilename)

    # ------------------------------------------------------------------------------------
    # map
    # ------------------------------------------------------------------------------------

    if nRecordsFound > 0 and 'folium' in mapping_package:
        import GIS_folium_map_util
        folium_pinmap_outputFilename = IO_files_util.generate_output_file_name(inputFilename, inputDir,
                                                                                  outputDir, '.html', 'GIS_pin',
                                                                                  geoName, locationColumnName, '',
                                                                                  '',
                                                                                  False, True)
        folium_heatmap_outputFilename=folium_pinmap_outputFilename.replace('pin','heat')
        outputFiles = GIS_folium_map_util.run(geocodedLocationsOutputFilename, folium_pinmap_outputFilename, folium_heatmap_outputFilename)
        filesToOpen.extend(outputFiles)


    # ------------------------------------------------------------------------------------
    # Google Earth Pro (geocoding above produces the GEP map)
    # ------------------------------------------------------------------------------------

    # ------------------------------------------------------------------------------------
    # Google Maps heat map
    # ------------------------------------------------------------------------------------

    if nRecordsFound > 0 and 'Google Maps' in mapping_package:

        heatMapoutputFilename = IO_files_util.generate_output_file_name(inputFilename, '', outputDir,
                                                                        '.html', 'GIS',
                                                                        geocoder, locationColumnName, '', '',
                                                                        False, True)
        coordList = []

        df = pd.read_csv(geocodedLocationsOutputFilename, encoding='utf-8', on_bad_lines='skip')
        if 'Latitude' in df and 'Longitude' in df:
            lat = df.Latitude
            lon = df.Longitude

            for i in range(len(lat)):
                coordList.append([lat[i], lon[i]])
        else:
            mb.showwarning('Warning',
                           'The input csv file\n\n' + geocodedLocationsOutputFilename + '\n\ndoes not contain geocoded data with Latitude or Longitude columns required for Google Maps to produce heat maps.\n\nPlease, select a geocoded csv file in input and try again.')
            return

        Google_Maps_API = getGoogleAPIkey(window,'Google-Maps-API_config.csv')
        if Google_Maps_API == '':
            return

        GIS_Google_Maps_util.create_js(window, heatMapoutputFilename, coordList, geocoder, True)
        filesToOpen.append(heatMapoutputFilename)

    IO_user_interface_util.timed_alert(window, 2000, 'Analysis end', 'Finished running GIS pipeline at', True, '', True, startTime)
    return filesToOpen
