# written by Roberto Franzosi (Spring/summer 2020)
import sys
import IO_libraries_util

import os
from subprocess import call

import GUI_IO_util
import IO_files_util
import statistics_txt_util

# RUN section ______________________________________________________________________________________________________________________________________________________

def run_sentence_analysis(inputFilename, inputDir, outputDir,openOutputFiles,chartPackage,dataTransformation,
    compute_sentence_length_var,
    visualize_bySentenceIndex_var,
    visualize_bySentenceIndex_options_var,
    script_to_run,
    IO_values,
    sentence_complexity_var,
    text_readability_var,
    visualize_sentence_structure_var, num_sentences):

    config_filename = 'NLP_default_IO_config.csv'

    filesToOpen = []  # Store all files that are to be opened once finished

    if (compute_sentence_length_var==False and
        visualize_bySentenceIndex_var==False and
        sentence_complexity_var==False and
        text_readability_var==False and
        visualize_sentence_structure_var==False):
            print("No options have been selected.\n\nPlease, select an option and try again")
            return

    if compute_sentence_length_var:
        filesToOpen = statistics_txt_util.compute_sentence_length(inputFilename,inputDir, outputDir, config_filename, chartPackage,dataTransformation )

    if visualize_bySentenceIndex_var:
        filesToOpen = IO_files_util.runScript_fromMenu_option(script_to_run, IO_values,
                                                inputFilename, inputDir, outputDir,
                                                openOutputFiles, chartPackage,dataTransformation,
                                                visualize_bySentenceIndex_options_var)

    if sentence_complexity_var==True:
        if IO_libraries_util.check_inputPythonJavaProgramFile('statistics_txt_util.py')==False:
            return
        filesToOpen=statistics_txt_util.compute_sentence_complexity(inputFilename, inputDir, outputDir, config_filename, openOutputFiles,chartPackage, dataTransformation)
        if filesToOpen==None:
            return

    if text_readability_var==True:
        if IO_libraries_util.check_inputPythonJavaProgramFile('statistics_txt_util.py')==False:
            return
        statistics_txt_util.compute_sentence_text_readability(inputFilename, inputDir, outputDir,
                                                              config_filename, openOutputFiles, chartPackage, dataTransformation)

    if visualize_sentence_structure_var==True:
        # if IO_libraries_util.check_inputPythonJavaProgramFile('DependenSee.Jar')==False:
        #     return
        # errorFound, error_code, system_output = IO_libraries_util.check_java_installation('Sentence structure visualization')
        # if errorFound:
        #     return
        # if inputFilename=='' and inputFilename.strip()[-4:]!='.txt':
        #     mb.showwarning(title='Input file error', message='The Sentence tree viewer script requires a single txt file in input.\n\nPlease, select a txt file and try again.')
        #     return
        # IO_user_interface_util.timed_alert(GUI_util.window,2000,'Analysis start', 'Started running Sentence visualization: Dependency tree viewer (png graphs) at', True, '\n\nYou can follow Sentence Complexity in command line.')
        # subprocess.call(['java', '-jar', 'DependenSee.Jar', inputFilename, outputDir])
        # mb.showwarning(title='Analysis end',message='Finished running the Dependency tree viewer (png graphs).\n\nMake sure to open the png files in output, one graph for each sentence.')

        
        def first_file(path):
            try:
                entries = os.listdir(path)

                first =  None
                for entry in entries:
                    if entry.endswith(".txt"):
                        first = os.path.join(path, entry)
                        return first
            
                return None
            
            except Exception as e:
                print("Error ", e , " has occurred.")
                return None 

        inputFilename = first_file(inputDir)
        statistics_txt_util.sentence_structure_tree(inputFilename, outputDir, num_sentences)

