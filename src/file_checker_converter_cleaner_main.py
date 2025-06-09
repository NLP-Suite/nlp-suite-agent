# written by Roberto Franzosi October 2019, edited Spring 2020
# the script checks the CONTENT of txt files with various options:
#   utf-compliance
#   spelling
# the script also converts files types (pdf-->txt; docx-->txt)

import sys
import IO_libraries_util


import os
import importlib
from subprocess import call

import GUI_IO_util
import IO_files_util
import reminders_util
import config_util

# RUN section ______________________________________________________________________________________________________________________________________________________


def run(inputFilename,inputDir, outputDir,
    openOutputFiles,
    chartPackage,
    dataTransformation,
    check_tools,
    convert_tools,
    clean_tools,
    menu_option,
    script_to_run,
    function_to_run):

    config_filename = 'NLP_default_IO_config.csv'
    filesToOpen=[]

    if (check_tools=='') and (convert_tools=='') and (clean_tools==""):
        mb.showwarning(title='No options selected', message='No options have been selected.\n\nPlease, select one of the available options and try again.')
        return

    if menu_option=='Document converter (rtf --> txt)':
        mb.showwarning(title='rtf --> txt converter (Mac OS)', message='In a Mac OS, there is a simple way to batch convert a set of rtf files to txt. THIS ONLY APPLIES TO MAC OS!\n\nOpen the command prompt and change directory to where the rtf files are stored, then type:\n\nfind . -name \*.rtf -print0 | xargs -0 textutil -convert txt\n\nHit return. All txt converted files will be found in the same input directory as the original rtf files.\n\nFor more information, see the post by Alexander Refsum Jensenius at:\nhttps://www.arj.no/2013/01/08/batch-convert-rtf-files-to-txt/.')
        # return

    if ((check_tools!='') and (clean_tools!='')) and ((inputDir=="") and (inputFilename=="")):
        mb.showwarning(title='Input error', message='The selected option - ' + menu_option + ' - requires either a txt file or a directory in input.\n\nPlease, select a txt file or directory and try again.')
        return

    if check_tools!='' or convert_tools!='' or clean_tools!='':
        if 'check_for_typo' in function_to_run:
            mb.showwarning(title='Option not available', message='The Levenshtein\'s distance option is not available from this GUI.\n\nPlease, run the script from the spell_checker_main.')
            return

        pythonFile = importlib.import_module(script_to_run)
        func = getattr(pythonFile, function_to_run)
        # the func function will be executed (e.g., newspaper_titles in file_cleaner_util,
        #   if function_to_run contains "newspaper title"
        # correct values are checked in NLP_GUI
        if IO_libraries_util.check_inputPythonJavaProgramFile(script_to_run + ".py") == False:
            return
        outputFile=[]

        # different functions take a different number of arguments; check above in pydict and
        #   go to the function to see which arguments it takes or...
        #   standardize the number of arguments in all functions even if not used

        # predict_encoding uses default first 20 lines
        if 'predict_encoding' in function_to_run or \
                'check_utf8' in function_to_run or \
                'convert_2_ASCII' in function_to_run or \
                'empty_file' in function_to_run or \
                'find_replace' in function_to_run:
            func(GUI_util.window,inputFilename,inputDir,outputDir, config_filename)
        elif 'sentence_length' in function_to_run:
            outputFile=func(inputFilename,inputDir,outputDir,config_filename, chartPackage, dataTransformation)
        else:
            func(GUI_util.window,inputFilename,inputDir, outputDir,config_filename, openOutputFiles, chartPackage, dataTransformation)

        if len(outputFile)>0:
            filesToOpen.append(outputFile)

    if openOutputFiles:
        IO_files_util.OpenOutputFiles(GUI_util.window, openOutputFiles, filesToOpen, outputDir, scriptName)
