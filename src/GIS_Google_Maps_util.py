# util to create google maps from table data
# jack hester September 2020

"""
Use the Google Maps API to create a heatmap of locations
Gathers the points of the location in lat, long format then puts them into the template file
Saves that template file with the addition to user-specified file name/location\
Template file should be located in the lib folder
"""
import GUI_IO_util
import GIS_geocode_util
import os
import reminders_util
import GIS_pipeline_util


# gathers the template html/js file to build a heat map,
# inserts correct javascript containing all of the points to plot on heatmap_template
# gmaps_list is a list of lat/long values to be written in the java script html output file
# then saves a new file that contains the html/js to display the heatmap
def create_google_heatmap(outputFilename, gmaps_list):
    api_key = GIS_pipeline_util.getGoogleAPIkey('Google-Maps-API_config.csv')
    # 10 is a random number because the APY key is a long set of characters
    if len(api_key)< 5 or api_key == None :
        import tkinter.messagebox as mb
        mb.showwarning(title='Google Maps API key error',
                       message="The expected API key required by Google Maps is missing in the config file Google-Maps-API_config.csv.\n\nPlease, make sure to obtain the key, enter it, and save it correctly in the Google-Maps-API_config.csv file and try again.\n\nNo Google Maps heatmap can be produced.")
        # import IO_user_interface_util
        # IO_user_interface_util.timed_alert('', 2000, 'Google Maps API key error',
        #                                    'The expected API key required by Google Maps is missing. Please, make sure to obtain the key, enter it, and save it correctly in the Google-Maps-API_config.csv file.')
        return

    js_template_loc = GUI_IO_util.Google_heatmaps_libPath + os.sep + "heatmap_template.html"
    open_js = open(js_template_loc, 'r')
    js_contents = open_js.readlines()
    js_template = "".join(js_contents)
    open_js.close()

    js_to_write = js_template.split("//DO NOT REMOVE! PROGRAM INSERTS THE CORRECT JS HERE!")
    #js_to_write.insert(1,js_to_insert)
    s = ""
    for item in gmaps_list:
        s += str(item+"\n")
    js_output_file = open(outputFilename, 'w+')
    js_output_file.write(js_to_write[0].replace("<YOUR API KEY HERE>",api_key))
    js_output_file.write(s)
    js_output_file.write(js_to_write[1])
    js_output_file.close()
    return

# generate the javascript to be inserted into the template file to create the map
# returns lines with lat long pairs in google maps api syntax
# outputFilename where to save heatmap html file
# locations is either a list of locations or a list of lat long lists
# api_key is your google api key
# if latLongList is true, then the locations do not need to be generated,
# must provide geocoder if points are locations rather than lat longs
# if lat longs are provided, it should be via a nested list, i.e. [[lat1, long1], [lat2, long2], ...]
# otherwise it assumes the item provided is a list of locations (as strings)
def create_js(outputFilename, locations, geocoder, latLongList):
    gmaps_list = []
    if not latLongList:
        latLongList = []
        for l in locations:
            returned_loc = GIS_geocode_util.nominatim_geocode(geocoder, l)
            latLongList.append([returned_loc.latitude, returned_loc.longitude])
    else:
        latLongList = locations
    for item in latLongList:
        gmaps_str = ''.join(["new google.maps.LatLng(",str(item[0]),", ",str(item[1]),"),"])
        gmaps_list.append(gmaps_str)
        # gmaps_list geocoded values`
    create_google_heatmap(outputFilename, gmaps_list)
    head, scriptName = os.path.split(os.path.basename(__file__))
    reminders_util.checkReminder(scriptName,
                            reminders_util.title_options_Google_API,
                            reminders_util.message_Google_API,
                            True)

