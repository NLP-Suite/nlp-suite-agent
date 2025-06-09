import sys
import IO_libraries_util

import os
import tkinter as tk
from tkinter import ttk
from subprocess import call

import GUI_IO_util
import CoNLL_util
import CoNLL_table_search_util
import statistics_csv_util
import charts_util
import IO_files_util
import IO_csv_util
import IO_user_interface_util
import Stanford_CoreNLP_tags_util
import CoNLL_k_sentences_util
import reminders_util

import logging
import CoNLL_clause_analysis_util

import CoNLL_noun_analysis_util
import CoNLL_verb_analysis_util
import CoNLL_function_words_analysis_util
import CoNLL_table_search_util
import IO_csv_util
import CoNLL_util

# from data_manager_main import extract_from_csv

# more imports (e.g., import CoNLL_clause_analysis_util) are called below under separate if statements

# RUN section ______________________________________________________________________________________________________________________________________________________

# the values of the GUI widgets MUST be entered in the command otherwise they will not be updated
def run_conll(inputFilename, inputDir, outputDir, openOutputFiles, chartPackage, dataTransformation,
        searchedCoNLLField, searchField_kw, postag, deprel, co_postag, co_deprel, Begin_K_sent_var, End_K_sent_var, compute_sentence_var,
        search_token_var, k_sentences_var, all_analyses_var, all_analyses
        ):

    #INPUTE FILENAME WILLBE INPUT DIR, CoNLL Table to be parsed as one in directory 
    inputFilename = inputDir
    
    
    global recordID_position, documentId_position, data, all_CoNLL_records
    recordID_position = 9 # NEW CoNLL_U
    documentId_position = 11 # NEW CoNLL_U

    noResults = "No results found matching your search criteria for your input CoNLL file. Please, try different search criteria.\n\nTypical reasons for this warning are:\n   1.  You are searching for a token/word not found in the FORM or LEMMA fields (e.g., 'child' in FORM when in fact FORM contains 'children', or 'children' in LEMMA when in fact LEMMA contains 'child'; the same would be true for the verbs 'running' in LEMMA instead of 'run');\n   2. you are searching for a token that is a noun (e.g., 'children'), but you select the POS value 'VB', i.e., verb, for the POSTAG of searched token."
    config_filename = "NLP_default_IO_config.csv"
    filesToOpen = []  # Store all files that are to be opened once finished
    outputFiles = []
    WordNet_var = False
    
    if  all_analyses_var == False and\
        search_token_var == False and \
        WordNet_var == False and \
        compute_sentence_var == False and \
        k_sentences_var == False:
            print("No option selected, No option has been selected.\n\nPlease, select an option by ticking a checkbox and try again.")
            return

    # if extra_GUIs_var:
    #     if 'Data manipulation' in extra_GUIs_menu_var:
    #         call("python data_manipulation_main.py", shell=True)
    #     elif 'Style' in extra_GUIs_menu_var:
    #         call("python style_analysis_main.py", shell=True)
    #     if 'Ngrams searches' in extra_GUIs_menu_var:
    #         call("python NGrams_CoOccurrences_main.py", shell=True)
    #     if 'Word searches' in extra_GUIs_menu_var:
    #         call("python file_search_byWord_main.py", shell=True)
    #     if 'Wordnet' in extra_GUIs_menu_var:
    #         call("python knowledge_graphs_WordNet_main.py", shell=True)

#CONLL_TABLE_ANALYZER_MAIN


    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    # Reading CoNLL file data
    data, header = IO_csv_util.get_csv_data(inputFilename, True)
    if len(data) == 0:
        return
    all_CoNLL_records = CoNLL_util.CoNLL_record_division(data)
    if all_CoNLL_records is None or len(all_CoNLL_records) == 0:
        return

    if searchedCoNLLField == 'FORM':
        logger.info("Running FORM-based search")
    else:
        logger.info("Running LEMMA-based search")

    # Clause Analysis
    if 'CoNLL' in inputFilename and not '_nn_' in inputFilename:
        outputFiles = CoNLL_clause_analysis_util.clause_stats(inputFilename, '', outputDir, data, all_CoNLL_records, openOutputFiles, chartPackage, dataTransformation)
        if outputFiles:
            filesToOpen.extend(outputFiles)
    
    # Noun Analysis
    outputFiles = CoNLL_noun_analysis_util.noun_stats(inputFilename, outputDir, data, all_CoNLL_records, openOutputFiles, chartPackage, dataTransformation)
    if outputFiles:
        filesToOpen.extend(outputFiles)

    # Verb Analysis
    outputFiles = CoNLL_verb_analysis_util.verb_stats(config_filename, inputFilename, outputDir, data, all_CoNLL_records, openOutputFiles, chartPackage, dataTransformation)
    if outputFiles:
        filesToOpen.extend(outputFiles)

    # Function Words (Stop words) Analysis
    outputFiles = CoNLL_function_words_analysis_util.function_words_stats(inputFilename, outputDir, data, all_CoNLL_records, openOutputFiles, chartPackage, dataTransformation)
    if outputFiles:
        filesToOpen.extend(outputFiles)

    if searchField_kw and searchField_kw != 'e.g.: father':
        logger.info("Running token search on: %s", searchField_kw)
        temp_outputDir, outputFiles = CoNLL_table_search_util.search_CoNLL_table(inputFilename, outputDir, config_filename, chartPackage, dataTransformation, all_CoNLL_records, searchField_kw, searchedCoNLLField, postag, deprel, co_postag, co_deprel)
        if outputFiles:
            filesToOpen.extend(outputFiles)

# Ngrams searches & VIEWER','Word searches


    if search_token_var and searchField_kw=='e.g.: father':
        print("Search error, The 'Searched token' field must be different from 'e.g.: father'. Please, enter a CoNLL table token/word and try again.")

        return

    withHeader = True
    # TODO Chen we are reading inputFilename twice, once here then again as a dataframe
    data, header = IO_csv_util.get_csv_data(inputFilename, withHeader)
    if len(data) == 0:
        return
    all_CoNLL_records = CoNLL_util.CoNLL_record_division(data)
    if all_CoNLL_records == None:
        return
    if len(all_CoNLL_records) == 0:
        return

# ANALYSES -----------------------------------------------------------------------------------

    if all_analyses_var:
        # # create a subdirectory of the output directory; should create a subdir with increasing number to avoid writing ver
        # outputDir_temp = IO_files_util.make_output_subdirectory(inputFilename, '', outputDir, label='CoNLL_analyses',
        #                                                    silent=True)
        # if outputDir_temp == '':
        #     return
        #
        # outputDir=outputDir_temp
        #
        if all_analyses == '*':
            label = "Clause, noun, verb, function words"
        else:
            label = all_analyses
        # startTime=IO_user_interface_util.timed_alert('Analysis start', 'Started running CoNLL table ' + label + ' analyses at',
        #                                              True, '', True, '', False)

        outputDirSV = outputDir

        if all_analyses == '*' or all_analyses == 'Clause analysis':
            # create a subdirectory of the output directory; should create a subdir with increasing number to avoid writing ver
            outputDir_temp = IO_files_util.make_output_subdirectory(inputFilename, '', outputDir,
                                                                    label='CoNLL_clause',
                                                                    silent=True)
            if outputDir_temp == '':
                return
            outputDir = outputDir_temp

            if 'CoNLL' in inputFilename and '_nn_' in inputFilename:
                if all_analyses == 'Clause analysis':
                    print("Input file error, The CLAUSE analysis algorithm expects in input a CoNLL table generated by the Stanford CoreNLP PCFG parser, rather than the nn, neural network parser.\n\nOnly the PCFG parser exports clause tags.\n\nPlease check your input file and try again.")

            if 'CoNLL' in inputFilename and not '_nn_' in inputFilename:
                outputFiles = CoNLL_clause_analysis_util.clause_stats(inputFilename, '', outputDir,
                                                                      data,
                                                                      all_CoNLL_records,
                                                                      openOutputFiles, chartPackage, dataTransformation)
                if outputFiles!=None:
                    filesToOpen.extend(outputFiles)

        if all_analyses =='*' or all_analyses =='Noun analysis':
            # create a subdirectory of the output directory; should create a subdir with increasing number to avoid writing ver
            outputDir_temp = IO_files_util.make_output_subdirectory(inputFilename, '', outputDirSV,
                                                                    label='CoNLL_noun',
                                                                    silent=True)
            if outputDir_temp == '':
                return
            outputDir = outputDir_temp
            outputFiles = CoNLL_noun_analysis_util.noun_stats(inputFilename, outputDir, data, all_CoNLL_records,
                                                              openOutputFiles,
                                                              chartPackage,
                                                              dataTransformation)
            if outputFiles!=None:
                filesToOpen.extend(outputFiles)
        if all_analyses =='*' or all_analyses =='Verb analysis':
            # create a subdirectory of the output directory; should create a subdir with increasing number to avoid writing ver
            outputDir_temp = IO_files_util.make_output_subdirectory(inputFilename, '', outputDirSV,
                                                                    label='CoNLL_verb',
                                                                    silent=True)
            if outputDir_temp == '':
                return
            outputDir = outputDir_temp
            outputFiles = CoNLL_verb_analysis_util.verb_stats(config_filename, inputFilename, outputDir, data, all_CoNLL_records,
                                                              openOutputFiles, chartPackage, dataTransformation)

            if outputFiles!=None:
                filesToOpen.extend(outputFiles)

        if all_analyses =='*' or all_analyses =='Function (junk/stop) words analysis':
            # create a subdirectory of the output directory; should create a subdir with increasing number to avoid writing ver
            outputDir_temp = IO_files_util.make_output_subdirectory(inputFilename, '', outputDirSV,
                                                                    label='CoNLL_stop',
                                                                    silent=True)
            if outputDir_temp == '':
                return
            outputDir = outputDir_temp
            outputFiles = CoNLL_function_words_analysis_util.function_words_stats(inputFilename, outputDir, data,
                                                                                  all_CoNLL_records, openOutputFiles,
                                                                                  chartPackage, dataTransformation)
            if outputFiles!=None:
                filesToOpen.extend(outputFiles)

        # IO_user_interface_util.timed_alert(2000,'Analysis end',
        #                                    'Finished running CoNLL table ' + label + ' analyses at',
        #                                    True, '', True, startTime, False)

# SEARCH -----------------------------------------------------------------------------------

    if search_token_var and searchField_kw != 'e.g.: father':
        # # create a subdirectory of the output directory
        # outputDir = IO_files_util.make_output_subdirectory(inputFilename, '', outputDir, label='CoNLL_search',
        #                                                    silent=True)

        if ' ' in searchField_kw:
            print("Search error, The CoNLL table search can only contain one token/word since the table has one record for each token/word.\n\nPlease, enter a different word and try again.\n\nIf you need to search your corpus for collocations, i.e., multi-word expressions, you need to use the 'N-grams/Co-occurrence searches' or the 'Words/collocations searches' in the ALL searches GUI.")
            return
        
        if searchedCoNLLField.lower() not in ['lemma', 'form']:
            searchedCoNLLField = ('FORM')
        if postag!= '*':
            postag = postag.split(' - ')[0]
            postag = postag.strip()
        else:
            postag = '*'
        if deprel != '*':
            deprel = str(deprel).split(' - ')[0]
            deprel = deprel.strip()
        else:
            deprel = '*'
        if co_postag != '*':
            co_postag = str(co_postag).split(' - ')[0]
            co_postag = co_postag.strip()
        else:
            co_postag = '*'
        if co_deprel != '*':
            co_deprel = str(co_deprel).split(' - ')[0]
            co_deprel = co_deprel.strip()
        else:
            co_deprel = '*'

        if 'e.g.: father' in searchField_kw:
            if (not os.path.isfile(inputFilename.strip())) and \
                    ('CoNLL' not in inputFilename) and \
                    (not inputFilename.strip()[-4:] == '.csv'):
                
                print("INPUT File Path Error, Please, check INPUT FILE PATH and try again. The file must be a CoNLL table (extension .conll with Stanford CoreNLP no clausal tags, extension .csv with Stanford CoreNLP with clausal tags)")

                return
            msg = "Please, check the \'Searched token\' field and try again.\n\nThe value entered must be different from the default value (e.g.: father)."
            print("Searched Token Input Error" + msg)
            return  # breaks loop
        if len(searchField_kw) == 0:
            msg = "Please, check the \'Searched token\' field and try again.\n\nThe value entered must be different from blank."
            print("Searched Token Input Error " + msg)

            return  # breaks loop

        # startTime=IO_user_interface_util.timed_alert(2000,'Analysis start', 'Started running CoNLL search at',
        #                                              True, '', True, '', True)

        withHeader = True
        data, header = IO_csv_util.get_csv_data(inputFilename, withHeader)

        if len(data) <= 1000000:
            try:
                data = sorted(data, key=lambda x: int(x[recordID_position]))
            except:
                print("CoNLLL table ill formed The CoNLL table is ill formed. You may have tinkered with it. Please, rerun the Stanford CoreNLP parser since many scripts rely on the CoNLL table.")
                return

        temp_outputDir, filesToOpen = CoNLL_table_search_util.search_CoNLL_table(inputFilename, outputDir, config_filename,
                                          chartPackage, dataTransformation,
                                          all_CoNLL_records, searchField_kw, searchedCoNLLField,
                                          related_token_POSTAG=co_postag,
                                          related_token_DEPREL=co_deprel, _tok_postag_=postag,
                                          _tok_deprel_=deprel)

        if len(filesToOpen)>0:
            outputDir = temp_outputDir

# WordNet ------------------------------------------------------------------------------

    if WordNet_var:
        # create a subdirectory of the output directory; should create a subdir with increasing number to avoid writing ver
        outputDir_SV = outputDir
        outputDir = IO_files_util.make_output_subdirectory(inputFilename, '', outputDir, label='CoNLL_WordNet',
                                                           silent=False)
        if outputDir == '':
            return

        import pandas as pd
        df = pd.read_csv(inputFilename)
        df_nouns = df[df['POS'].isin(['NN', 'NNPS', 'NNP', 'NNS'])][['Lemma', 'POS']]
        inputFilename_nouns = outputDir + os.sep + "CoNLL_nouns_forWordNet.csv"
        df_nouns.to_csv(inputFilename_nouns, index=False) # , header=None
        df_verbs = df[df['POS'].isin(['VB', 'VBN', 'VBD', 'VBG', 'VBP', 'VBZ'])][['Lemma', 'POS']]
        inputFilename_verbs = outputDir + os.sep + "CoNLL_verbs_forWordNet.csv"
        df_verbs.to_csv(inputFilename_verbs, index=False) # , header=None

        filesToOpen.append(inputFilename_nouns)
        filesToOpen.append(inputFilename_verbs)

        # the WordNet installation directory is now checked in aggregate_GoingUP
        WordNetDir = ''
        import knowledge_graphs_WordNet_util
        output = knowledge_graphs_WordNet_util.aggregate_GoingUP(WordNetDir, inputFilename_nouns, outputDir,
                                                                 config_filename, 'NOUN',
                                                                 openOutputFiles, chartPackage, dataTransformation,
                                                                 language_var='English')
        if output != None:
            if isinstance(output, str):
                filesToOpen.append(output)
            else:
                filesToOpen.extend(output)

        output = knowledge_graphs_WordNet_util.aggregate_GoingUP(WordNetDir, inputFilename_verbs, outputDir,
                                                                 config_filename, 'VERB',
                                                                 openOutputFiles, chartPackage,dataTransformation,
                                                                 language_var='English')
        if output != None:
            if isinstance(output, str):
                filesToOpen.append(output)
            else:
                filesToOpen.extend(output)

        outputDir=outputDir_SV

# -----------------------------------------------------------------------------------------------------------------------------
    if compute_sentence_var:
        tempOutputFile = CoNLL_util.compute_sentence_table(inputFilename, outputDir)
        filesToOpen.append(tempOutputFile)

# -----------------------------------------------------------------------------------------------------------------------------
    if k_sentences_var:
        if Begin_K_sent_var==0 or End_K_sent_var==0:
            print("Warning, The Repetion finder algorithm needs beginning and end K sentences.\n\nPlease, enter valid K number(s) of sentences and try again.")
            return
        # startTime = IO_user_interface_util.timed_alert(2000, 'Analysis start',
        #                                                'Started running the CoNLL table K-sentences analyzer at',
        #                                                True, '', True, '', False)
        temp_outputDir, outputFiles = CoNLL_k_sentences_util.k_sent(inputFilename, outputDir, chartPackage, dataTransformation, Begin_K_sent_var, End_K_sent_var)
        if outputFiles!=None:
            outputDir = temp_outputDir
            filesToOpen.extend(outputFiles)
        # IO_user_interface_util.timed_alert(2000,'Analysis end',
        #                                    'Finished running the CoNLL table K-sentences analyzer at',
        #                                    True, '', True, startTime, False)
        
        
    return filesToOpen

