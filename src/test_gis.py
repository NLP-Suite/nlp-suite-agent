# test_topic_modeling.py
import os
from GIS_main import run_GIS

# Replace with your input and output directories
inputDir = '/Users/aidenamaya/nlp-suite/input'
outputDir = '/Users/aidenamaya/nlp-suite/output'

# Ensure the directories exist
os.makedirs(inputDir, exist_ok=True)
os.makedirs(outputDir, exist_ok=True)

# Set parameters
inputFilename  = ''
openOutputFiles = False
chartPackage = 'Excel'
dataTransformation = 'No transformation'
csv_file = ""
NER_extractor = True
location_menu = False
geocoder = "Nominatim"
country_bias_var = ""
area_var = "e.g.,"
restrict_var = False
GIS_package_var = "Google Earth Pro"



# Run the topic modeling function
run_GIS(inputFilename = inputFilename, inputDir = inputDir, outputDir = outputDir, openOutputFiles = openOutputFiles, chartPackage = chartPackage, 
        dataTransformation = dataTransformation,
        csv_file = csv_file,
        NER_extractor = NER_extractor,
        location_menu = location_menu, 
        geocoder = geocoder,
        geocode_locations="", 
        country_bias_var = country_bias_var,
        area_var = area_var, 
        restrict_var = restrict_var,
        map_locations = "", 
        GIS_package_var = GIS_package_var,
        GIS_package2_var = False
)
