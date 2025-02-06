# test_topic_modeling.py
import os
from SVO import run_svo

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
coref_var = False 
manual_coref_var = False 
normalized_NER_date_extractor_var = False
package_var = 'Stanford CoreNLP'
gender_var = False
quote_var = False
subjects_dict_path_var = False 
verbs_dict_path_var = False
objects_dict_path_var = False 
filter_subjects = False
filter_verbs = False
filter_objects = False
lemmatize_subjects = False
lemmatize_verbs = False
lemmatize_objects = False 
gephi_var = False 
wordcloud_var = False 
google_earth_var = False



# Run the topic modeling function
run_svo(inputFilename = inputFilename, inputDir = inputDir, outputDir = outputDir, openOutputFiles = openOutputFiles, chartPackage = chartPackage, dataTransformation = dataTransformation,
        coref_var = coref_var,
        manual_coref_var = manual_coref_var,
        normalized_NER_date_extractor_var = normalized_NER_date_extractor_var,
        package_var = package_var,
        gender_var = gender_var,
        quote_var = quote_var,
        subjects_dict_path_var = subjects_dict_path_var,
        verbs_dict_path_var = verbs_dict_path_var,
        objects_dict_path_var = objects_dict_path_var,
        filter_subjects = filter_subjects,
        filter_verbs = filter_verbs,
        filter_objects = filter_objects,
        lemmatize_subjects = lemmatize_subjects,
        lemmatize_verbs = lemmatize_verbs,
        lemmatize_objects = lemmatize_objects,
        gephi_var = gephi_var,
        wordcloud_var = wordcloud_var,
        google_earth_var = google_earth_var
)
