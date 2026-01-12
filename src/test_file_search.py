

import os
from file_search_byWord_main import run_search_byWord
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

search_options = "Case sensitive (default)"
search_by_dictionary= False 
selectedCsvFile = "" 
search_by_keyword = True 
search_keyword_values = ""
minus_K_words_sentences_var = 0
plus_K_words_sentences_var = 0
extract_sentences_var = 1
coOccurring_keywords_var = 1
create_subcorpus_var = 0
search_options_menu_var = ""
search_options_list = []
language_list = ["English"]
language = "English"

run_search_byWord(inputFilename = inputFilename,
                  inputDir = inputDir, 
                  outputDir = outputDir,
    openOutputFiles = openOutputFiles,
    chartPackage = chartPackage,
    dataTransformation = dataTransformation,
    search_options = search_options,
    search_by_dictionary = search_by_dictionary,
    selectedCsvFile = selectedCsvFile,
    search_by_keyword = search_by_keyword,
    search_keyword_values = search_keyword_values,
    minus_K_words_sentences_var = minus_K_words_sentences_var,
    plus_K_words_sentences_var = plus_K_words_sentences_var,
    extract_sentences_var = extract_sentences_var,
    coOccurring_keywords_var = coOccurring_keywords_var,
    create_subcorpus_var = create_subcorpus_var,
    search_options_menu_var = search_options_menu_var,
    search_options_list = search_options_list,
    language_list = language_list,
    language = language)
