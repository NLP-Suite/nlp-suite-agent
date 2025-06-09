# written by Roberto Franzosi October 2019, edited Spring 2020

import sys
import IO_libraries_util

import os
from subprocess import call

import GUI_IO_util
import IO_files_util
import file_search_byWord_util
import IO_user_interface_util
import reminders_util
import constants_util
import config_util

# RUN section ______________________________________________________________________________________________________________________________________________________

def run(inputFilename,inputDir, outputDir,
    openOutputFiles,
    chartPackage,
    dataTransformation,
    search_options,
    search_by_dictionary,
    selectedCsvFile,
    search_by_keyword,
    search_keyword_values,
    minus_K_words_sentences_var,
    plus_K_words_sentences_var,
    extract_sentences_var,
    coOccurring_keywords_var,
    create_subcorpus_var,
    search_options_menu_var,
    search_options_list,
    language_list,
    language): #,
    # extract_sentences_search_words_var_str):

    config_filename = 'NLP_default_IO_config.csv'

    filesToOpen = []
    extra_GUIs_var = False 
    
    if extra_GUIs_var==False and search_by_dictionary==False and search_by_keyword==False:
            print("Input error, No search options have been selected.\n\nPlease, select a search option and try again.")
            return

    if search_options_menu_var !='' and not search_options_menu_var in str(search_options_list) :
        
        print("Warning, There is a search value '" + str(search_options_menu_var.get()) + "' that has not been added (using the + button) to the csv file fields to be processed.\n\nAre you sure you want to continue?")
        return

    # if extra_GUIs_var.get():
    #     if 'CoNLL' in extra_GUIs_menu_var.get():
    #         call("python CoNLL_table_analyzer_main.py", shell=True)
    #     if 'Style' in extra_GUIs_menu_var.get():
    #         call("python style_analysis_main.py", shell=True)
    #     if 'Ngrams searches' in extra_GUIs_menu_var.get():
    #         call("python NGrams_CoOccurrences_main.py", shell=True)
    #     if 'Wordnet' in extra_GUIs_menu_var.get():
    #         call("python knowledge_graphs_WordNet_main.py", shell=True)

    # # create a subdirectory of the output directory
    # outputDir = IO_files_util.make_output_subdirectory(inputFilename, inputDir, outputDir, label='search',
    #                                                    silent=False)
    # if outputDir == '':
    #     return

    if not 'Search within document' in search_options_list:
        if not 'Search within sentence (default)' in search_options_list:
            search_options_list.append('Search within sentence (default)')

    if 'Lemmatize' in str(search_options_list):
        useLemma = True
    else:
        useLemma = False

    if search_by_dictionary:
        label = 'SEARCH word(s) by values in dictionary file: ' + selectedCsvFile
    else:
        label = 'SEARCH word(s): ' + search_keyword_values
    #@@
    # IO_user_interface_util.timed_alert(GUI_util.window, 2000, 'Word/collocation search start',
    #                     'Started running Word/collocation search at', True,
    #                     'SEARCH options: ' + str(search_options_list)+'\n'+label,
    #                                    True, '', True)

    if search_by_dictionary or search_by_keyword:
        # print('Search options:', search_options_list)
        # print('-K +K ',minus_K_words_sentences_var, plus_K_words_sentences_var)
        if coOccurring_keywords_var:
            import NGrams_CoOccurrences_util
            outputFiles = NGrams_CoOccurrences_util.NGrams_coOccurrences_VIEWER(
                inputDir,
                outputDir,
                config_filename,
                chartPackage, dataTransformation,
                0, # n-grams VIEWER
                1, # coOccurring_keywords_var
                search_keyword_values,
                minus_K_words_sentences_var,
                plus_K_words_sentences_var,
                language_list,
                useLemma,
                0,
                '',
                0,
                '',
                '',
                0,
                search_options_list,
                0, '', '')

            if outputFiles != None:
                if isinstance(outputFiles, str):
                    filesToOpen.append(outputFiles)
                else:
                    filesToOpen.extend(outputFiles)
        else:
            filesToOpen = file_search_byWord_util.search_sentences_documents(inputFilename, inputDir, outputDir,
                                                                             config_filename,
                                                                             search_by_dictionary, selectedCsvFile,
                                                                             search_by_keyword, search_keyword_values,
                                                                             minus_K_words_sentences_var, plus_K_words_sentences_var,
                                                                             extract_sentences_var,
                                                                             create_subcorpus_var,
                                                                             search_options_list, language,
                                                                             chartPackage, dataTransformation)

    # if extract_sentences_var:
    #     if coOccurring_keywords_var:
    #         import NGrams_CoOccurrences_util
    #         outputFiles = NGrams_CoOccurrences_util.NGrams_coOccurrences_VIEWER(
    #             inputDir,
    #             outputDir,
    #             config_filename,
    #             chartPackage, dataTransformation,
    #             0, # n-grams VIEWER
    #             1, # coOccurring_keywords_var
    #             extract_sentences_search_words_var_str,
    #             minus_K_words_sentences_var,
    #             plus_K_words_sentences_var,
    #             language_list,
    #             useLemma,
    #             0,
    #             '',
    #             0,
    #             '',
    #             '',
    #             0,
    #             search_options_list,
    #             0, '', '')
    #
    #         if outputFiles != None:
    #             if isinstance(outputFiles, str):
    #                 filesToOpen.append(outputFiles)
    #             else:
    #                 filesToOpen.extend(outputFiles)