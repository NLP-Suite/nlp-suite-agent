# Roberto Franzosi Fall 2019-Spring 2020

# INPUT The function computeDistance assumes that:
#   the location name is always the column of the FIRST location name followed by its latitude and longitude
#       followed by the SECOND location name followed by its latitude and longitude
#   longitude is always in the next column of latitude 1 and 2

# geodesic distance
# Geopy can calculate geodesic distance between two points using
#   the geodesic distance
#   the great-circle distance

# The geodesic distance (also called great circle distance) is the shortest distance on the surface of an ellipsoidal model of the earth.
# There are multiple popular ellipsoidal models.
#   Which one will be the most accurate depends on where your points are located on the earth.
#   The default is the WGS-84 ellipsoid, which is the most globally accurate.
#   geopy includes a few other models in the distance.ELLIPSOIDS dictionary.

import sys
import IO_libraries_util

import os


import IO_files_util
import GUI_IO_util
import GIS_file_check_util
import GIS_distance_util
import IO_csv_util
import GIS_geocode_util
import GIS_pipeline_util

# RUN section ______________________________________________________________________________________________________________________________________________________

def run(inputFilename,outputDir, openOutputFiles, chartPackage, dataTransformation,
        encoding, geocoder,
        # geocode,
        compute_pairwise_distances, compute_baseline_distances, baselineLocation,locationColumn,locationColumn2):
    config_filename = "NLP_default_IO_config.csv"

    filesToOpen = []

    # step 1 - geocoder_Google_Earth
    # step 2 - extract_NER_locations
    # step 3 - geocode
    # step 4 - generate_kml
    # compute geodesic distances
    # compute geodesic distances from specific location

    # this will check the appended country names and short name
    # from iso3166 import countries
    # for c in countries:
    #     print(c)

    inputIsCoNLL, inputIsGeocoded, withHeader, headers, datePresent, filenamePositionInCoNLLTable=GIS_file_check_util.CoNLL_checker(inputFilename)

    # if input_main_dir_path.get()!='':
    #     mb.showwarning(title='File type error',
    #                    message='The GIS distance scripts expects in input a csv file. Please, select a csv file and try again.')
    #     return
    # if inputFilename.endswith('.csv') == False:
    #     mb.showwarning(title='File type error',
    #                    message='The input file\n\n' + inputFilename + '\n\nis not an expected csv file. Please, check the file and try again.')
    #     return

    if compute_pairwise_distances== False and compute_baseline_distances==False:
        print("Warning, No options have been selected.\n\nPlease, select an option and try again.")
        return

    if compute_pairwise_distances== True and inputIsGeocoded==False:
        print("Warning, You are running the GIS algorithm for pairwise distances with an input file that seems to be non-geocoded. You cannot run this option with non-geocoded data. You can only run the option 'Compute distances from baseline location.'\n\nPlease, select a different option or a geocoded file with six columns and try again.")
        return

    if compute_pairwise_distances and (locationColumn==""):
        print("Warning, You are running the GIS algorithm for pairwise distances. You must select the column containing the First location names.\n\nPlease, using the dropdown menu, select the column of the FIRST location names and try again. ")
        return

    if compute_pairwise_distances== True and inputIsGeocoded and len(headers)<6:
        print("Warning, You are running the GIS algorithm for pairwise distances. But your input file has fewer than the expected 6 headers (Location1, Latitude1, Longitude1, Location2, Latitude2, Longitude2):\n\n' "+ str(headers) + "\n\nPlease, select a different file and try again.")
        return

    if compute_pairwise_distances== False and inputIsGeocoded and (locationColumn=="" or locationColumn2==""):
        print("Warning, You are running the GIS distance algorithm using two sets of locations. You must select the columns containing the First and Second location names.\n\nPlease, using the dropdown menu, select the column of the FIRST and SECOND location names and try again. ")
        return

    if compute_baseline_distances and baselineLocation != '' and locationColumn=="":
        print("Warning, You are running the GIS distance algorithm from the baseline location '" + baselineLocation + "'. You must select the column containing the First location name.\n\nPlease, using the dropdown menu, select the column of the FIRST location names and try again.")
        return


    locationColumnNumber = 0
    locationColumnNumber2 = 0

    if withHeader==True:
        locationColumnNumber=IO_csv_util.get_columnNumber_from_headerValue(headers,locationColumn, inputFilename)
        if len(locationColumn2)>0:
            locationColumnNumber2=IO_csv_util.get_columnNumber_from_headerValue(headers,locationColumn2, inputFilename)

    encodingValue='utf-8'

    geocoder = 'Nominatim'

    if "Google" in geocoder:
        Google_API = GIS_pipeline_util.getGoogleAPIkey('Google-geocode-API_config.csv')
    else:
        Google_API=''

    geolocator = GIS_geocode_util.get_geolocator(geocoder,Google_API)

    distinctValues=True

    numColumns=len(headers)
    split_locations=''

    if compute_baseline_distances and baselineLocation!='':
        filesToOpen=GIS_distance_util.computeDistancesFromSpecificLocation(inputFilename, outputDir, geolocator,geocoder,inputIsGeocoded,baselineLocation, headers,locationColumnNumber,locationColumn, distinctValues,withHeader,inputIsCoNLL,split_locations,datePresent,filenamePositionInCoNLLTable,encodingValue)
        if len(filesToOpen)==0:
            return
    if compute_pairwise_distances:
        filesToOpen=GIS_distance_util.computePairwiseDistances(inputFilename,outputDir,headers,locationColumnNumber,locationColumnNumber2,locationColumn,locationColumn2, distinctValues,geolocator,geocoder,inputIsCoNLL,datePresent,encodingValue)
        if len(filesToOpen)==0:
            return
        if len(filesToOpen) == 0:
            return

    return filesToOpen