

import os
from NGrams_CoOccurrences import run_ngrams
import GUI_IO_util

inputDir = '/Users/aidenamaya/nlp-suite/input'
outputDir = '/Users/aidenamaya/nlp-suite/output'

# Ensure the directories exist
os.makedirs(inputDir, exist_ok=True)
os.makedirs(outputDir, exist_ok=True)

inputFilename = '' 
openOutputFiles = False
chartPackage = 'Excel'
dataTransformation = 'No transformation'

ngrams_options_list = ['Case sensitive (default)']
Ngrams_compute_var = True
ngrams_menu_var = 'Character'
ngrams_options_menu_var = ""
ngrams_size = 2


search_words = ''
minus_K_words_var = 0
plus_K_words_var = 0
Ngrams_search_var = False
csv_file_var = ''
ngrams_viewer_var = False
CoOcc_Viewer_var = ''
# within_sentence_co_occurrence_search_var = False  # commented in run()
date_options = False
temporal_aggregation_var = False
viewer_options_list = []
language_list = ["English"]
config_input_output_numeric_options = [0,1,0,1]
number_of_years = 0

run_ngrams(
    inputFilename=inputFilename,
    inputDir=inputDir,
    outputDir=outputDir,
    openOutputFiles=openOutputFiles,
    chartPackage=chartPackage,
    dataTransformation=dataTransformation,

    ngrams_options_list=ngrams_options_list,
    Ngrams_compute_var=Ngrams_compute_var,
    ngrams_menu_var=ngrams_menu_var,
    ngrams_options_menu_var=ngrams_options_menu_var,
    ngrams_size=ngrams_size,
    search_words=search_words,
    minus_K_words_var=minus_K_words_var,
    plus_K_words_var=plus_K_words_var,
    Ngrams_search_var=Ngrams_search_var,
    csv_file_var=csv_file_var,
    ngrams_viewer_var=ngrams_viewer_var,
    CoOcc_Viewer_var=CoOcc_Viewer_var,
    # within_sentence_co_occurrence_search_var=within_sentence_co_occurrence_search_var,
    date_options=date_options,
    temporal_aggregation_var=temporal_aggregation_var,
    viewer_options_list=viewer_options_list,
    language_list=language_list,
    config_input_output_numeric_options=config_input_output_numeric_options,
    number_of_years=number_of_years
)
