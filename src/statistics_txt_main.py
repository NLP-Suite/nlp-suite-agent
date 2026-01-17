# written by Roberto Franzosi (Spring/summer 2020)

import sys
import IO_libraries_util


import os
from subprocess import call

import GUI_IO_util



# RUN section ______________________________________________________________________________________________________________________________________________________

def run_statistics(inputFilename, inputDir, outputDir,
        corpus_statistics_options_menu_var,
        corpus_text_options_menu_var,
        openOutputFiles,chartPackage,dataTransformation,
        corpus_statistics_var,
        corpus_statistics_byPOS_var):

    config_filename = 'NLP_default_IO_config.csv'
    filesToOpen = []  # Store all files that are to be opened once finished
    config_input_output_numeric_options = [1,0,0,1]
    if not corpus_statistics_var and not corpus_statistics_byPOS_var:
        print("Warning, No option has been selected.\n\nPlease, select an option and try again.")
        return

    # corpus statistics --------------------------------------------------------------------

    if corpus_statistics_var:
        stopwords_var = False
        lemmatize_var = False
        if corpus_text_options_menu_var == '*':
            stopwords_var = True
            lemmatize_var = True
        if 'Lemmatize' in corpus_text_options_menu_var:
            lemmatize_var = True
        if 'stopwords' in corpus_text_options_menu_var:
            stopwords_var = True
        if "*" in corpus_statistics_options_menu_var or \
                'frequencies' in corpus_statistics_options_menu_var:

            import statistics_txt_util
            outputFiles, outputDir = statistics_txt_util.compute_corpus_statistics(inputFilename, inputDir, outputDir,
                                                                        config_filename, False, 
                                                                        chartPackage, dataTransformation,stopwords_var, lemmatize_var)
            if outputFiles != None:
                if isinstance(outputFiles, str):
                    filesToOpen.append(outputFiles)
                else:
                    filesToOpen.extend(outputFiles)
        if "Compute sentence length" in corpus_statistics_options_menu_var or "*" in corpus_statistics_options_menu_var:
            import statistics_txt_util
            outputFiles = statistics_txt_util.compute_sentence_length(inputFilename, inputDir, outputDir,
                                                                      config_filename, chartPackage, dataTransformation)
            if outputFiles != None:
                if isinstance(outputFiles, str):
                    filesToOpen.append(outputFiles)
                else:
                    filesToOpen.extend(outputFiles)

        if "Compute line length" in corpus_statistics_options_menu_var or "*" in corpus_statistics_options_menu_var:
            import statistics_txt_util
            outputFiles = statistics_txt_util.compute_line_length(config_filename, inputFilename, inputDir,
                                                                  outputDir,
                                                                  False, chartPackage, dataTransformation)
            if outputFiles != None:
                if isinstance(outputFiles, str):
                    filesToOpen.append(outputFiles)
                else:
                    filesToOpen.extend(outputFiles)

    if corpus_statistics_byPOS_var:
        import Stanza_util
        import config_util
        # get the NLP package and language options
        error, package, parsers, package_basics, language, package_display_area_value, encoding_var, export_json_var, memory_var, document_length_var, limit_sentence_length_var = \
            config_util.read_NLP_package_language_config()
        # get the date options from filename
        filename_embeds_date_var, date_format_var, items_separator_var, date_position_var, config_file_exists = \
            config_util.get_date_options(config_filename, config_input_output_numeric_options)
        language_var = language
        language_list = [language]

        document_length_var = 1
        limit_sentence_length_var = 1000
        memory_var = 6
        annotator='POS'
        outputFiles = Stanza_util.Stanza_annotate(config_filename, inputFilename, inputDir,
                                                      outputDir,
                                                      openOutputFiles,
                                                      chartPackage, dataTransformation,
                                                      annotator, False,
                                                      language_list,
                                                      memory_var, document_length_var, limit_sentence_length_var,
                                                      filename_embeds_date_var=filename_embeds_date_var,
                                                      date_format=date_format_var,
                                                      items_separator_var=items_separator_var,
                                                      date_position_var=date_position_var)

        if outputFiles == None:
            return
        if isinstance(outputFiles, str):
            filesToOpen.append(outputFiles)
        else:
            filesToOpen.extend(outputFiles)
        
    return filesToOpen
