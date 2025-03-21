import os
import config_util
import IO_files_util
import GUI_IO_util
import IO_libraries_util
import lib_util

def run_sentiment_analysis(inputDir,outputDir, openOutputFiles, chartPackage, dataTransformation, mean_var, median_var, SA_algorithm_var):
    print(inputDir,outputDir, openOutputFiles, chartPackage, dataTransformation, mean_var, median_var, SA_algorithm_var)
    # get the NLP package and language options
    _, _, _, _, language, package_display_area_value, _, export_json_var, memory_var, document_length_var, limit_sentence_length_var = config_util.read_NLP_package_language_config()
    language_var = language
    if package_display_area_value == '':
        print('No setup for NLP package and language', "The default NLP package and language has not been setup.\n\nPlease, click on the Setup NLP button and try again.")
        return

    if SA_algorithm_var=='':
        print('Warning',"No option has been selected.\n\nPlease, select a Sentiment analysis option and try again.")
        return

    mode = "both"
    if mean_var==False and median_var==False:
        mode = "mean"
    elif mean_var==True and median_var==False:
        mode = "mean"
    elif mean_var==False and median_var==True:
        mode = "median"
    elif mean_var==True and median_var==True:
        mode = "both"

    BERT_var = 0
    SentiWordNet_var=0
    CoreNLP_var=0
    Stanza_var=0
    spaCy_var=0
    hedonometer_var=0
    vader_var=0
    anew_var=0

    if SA_algorithm_var=='*':
        if "" != '':
            inputBaseName = os.path.basename("")[0:-4]  # without .txt
        else:
            inputBaseName = os.path.basename(inputDir)
        # create a sentiment subdirectory of the output directory
        outputSentDir = os.path.join(outputDir, 'Sentiment_ALL_' + inputBaseName)
        outputSentDir = IO_files_util.make_output_subdirectory('', '', outputSentDir, label='',
                                                              silent=True)
        if outputSentDir == '':
            return
        outputDir=outputSentDir

        BERT_var=1
        CoreNLP_var=1
        spaCy_var=1
        Stanza_var=1
        anew_var=1
        hedonometer_var=1
        SentiWordNet_var=1
        vader_var=1
    elif 'BERT' in SA_algorithm_var:
        BERT_var = 1
    elif 'spaCy' in SA_algorithm_var:
        spaCy_var = 1
    elif 'Stanford CoreNLP' in SA_algorithm_var:
        CoreNLP_var = 1
    elif 'Stanza' in SA_algorithm_var:
        Stanza_var=1
    elif 'SentiWordNet' in SA_algorithm_var:
        SentiWordNet_var=1
    elif 'ANEW' in SA_algorithm_var:
        anew_var=1
    elif 'hedonometer' in SA_algorithm_var:
        hedonometer_var=1
    elif 'VADER' in SA_algorithm_var:
        vader_var=1
    else:
        print('Warning', SA_algorithm_var.lstrip() + " is not available yet. Sorry!\n\nPlease, select another option and try again.")
        return

    # NEURAL NETWORK APPROACHES -------------------------------------------------------------------

    # BERT ---------------------------------------------------------

    if BERT_var==1:
        import BERT_util
        if 'Multilingual' in SA_algorithm_var:
            model_path = "cardiffnlp/twitter-xlm-roberta-base-sentiment" # multilingual model
        else:
            model_path = "cardiffnlp/twitter-roberta-base-sentiment-latest" # English language model
        BERT_util.sentiment_main("", inputDir, outputDir, GUI_IO_util.config_filename, mode, chartPackage, dataTransformation, model_path)

    # spaCy  _______________________________________________________

    if SA_algorithm_var == '*' or spaCy_var == 1 and (mean_var or median_var):
        # check internet connection
        import IO_internet_util
        if not IO_internet_util.check_internet_availability_warning('spaCy Sentiment Analysis'):
            return
        #     flag="true" do NOT produce individual output files when processing a directory; only merged file produced
        #     flag="false" or flag="" ONLY produce individual output files when processing a directory; NO  merged file produced

        annotator = ['sentiment']
        document_length_var = 1
        limit_sentence_length_var = 1000
        import spaCy_util
        spaCy_util.spaCy_annotate(GUI_IO_util.config_filename, "", inputDir,
                                                    outputDir,
                                                    openOutputFiles,
                                                    chartPackage, dataTransformation,
                                                    annotator, False,
                                                    language_var,
                                                    memory_var, document_length_var, limit_sentence_length_var,
                                                    filename_embeds_date_var=0,
                                                    date_format='',
                                                    items_separator_var='',
                                                    date_position_var=0)

# Stanford CORENLP  _______________________________________________________

    if SA_algorithm_var=='*' or CoreNLP_var==1 and (mean_var or median_var):
        #check internet connection
        import IO_internet_util
        import Stanford_CoreNLP_util
        if not IO_internet_util.check_internet_availability_warning('Stanford CoreNLP Sentiment Analysis'):
            return
        Stanford_CoreNLP_util.CoreNLP_annotate(GUI_IO_util.config_filename, "", inputDir,
                                                                          outputDir, openOutputFiles, chartPackage,dataTransformation, 'sentiment', False,
                                                                          language_var, export_json_var,
                                                                          memory_var)

# Stanza  _______________________________________________________

    if SA_algorithm_var == '*' or Stanza_var == 1 and (mean_var or median_var):
        # check internet connection
        import IO_internet_util
        if not IO_internet_util.check_internet_availability_warning('Stanza Sentiment Analysis'):
            return

        annotator = 'sentiment'
        document_length_var = 1
        limit_sentence_length_var = 1000
        import Stanza_util
        Stanza_util.Stanza_annotate(GUI_IO_util.config_filename, "", inputDir,
                                                      outputDir,
                                                      openOutputFiles,
                                                      chartPackage, dataTransformation,
                                                      annotator, False,
                                                      [language_var], # Stanza_util takes language_var as a list
                                                      memory_var, document_length_var, limit_sentence_length_var,
                                                      filename_embeds_date_var=0,
                                                      date_format='',
                                                      items_separator_var='',
                                                      date_position_var=0)

# DICTIONARY APPROACHES -------------------------------------------------------------------

# ANEW _______________________________________________________
    import sentiment_analysis_ANEW_util
    if anew_var == 1 and (mean_var or median_var):
        if language == 'English':
            if lib_util.checklibFile(GUI_IO_util.sentiment_libPath + os.sep + 'EnglishShortenedANEW.csv',
                                     'sentiment_analysis_ANEW') == False:
                return
            if IO_libraries_util.check_inputPythonJavaProgramFile('sentiment_analysis_ANEW_util.py') == False:
                return

            sentiment_analysis_ANEW_util.main("", inputDir, outputDir, mode, 
                                                            chartPackage, dataTransformation)
            print('Analysis end', 'Finished running ANEW Sentiment Analysis at')
        else:
            print('Warning', 'The ANEW algorithm is available only for the English language.\n\nYour currently selected language is ' + language + '.\n\nYou can change the language using the Setup dropdownmenu at the bottom of this GUI and selecting "Setup NLP package and corpus language."')

# HEDONOMETER _______________________________________________________
    import sentiment_analysis_hedonometer_util
    if SA_algorithm_var=='*' or hedonometer_var==1 and (mean_var or median_var):
        if lib_util.checklibFile(GUI_IO_util.sentiment_libPath + os.sep + 'hedonometer.json', 'sentiment_analysis_hedonometer_util.py')==False:
            return
        if IO_libraries_util.check_inputPythonJavaProgramFile('sentiment_analysis_hedonometer_util.py')==False:
            return
        if language=='English':

            print('Analysis start', 'Started running HEDONOMETER Sentiment Analysis at')
            sentiment_analysis_hedonometer_util.main("", inputDir, outputDir, mode, chartPackage, dataTransformation)
            print('Analysis end', 'Finished running HEDONOMETER Sentiment Analysis at')
        else:
            print('Warning','The HEDONOMETER algorithm is available only for the English language.\n\nYour currently selected language is '+language+'.\n\nYou can change the language using the Setup dropdownmenu at the bottom of this GUI and selecting "Setup NLP package and corpus language."')

#SentiWordNet _______________________________________________________
    import sentiment_analysis_SentiWordNet_util
    if SA_algorithm_var=='*' or SentiWordNet_var==1 and (mean_var or median_var):
        if language=='English':
            if IO_libraries_util.check_inputPythonJavaProgramFile('sentiment_analysis_SentiWordNet_util.py')==False:
                return
            print('Analysis start', 'Started running SentiWordNet Sentiment Analysis at')
            sentiment_analysis_SentiWordNet_util.main("", inputDir, outputDir, GUI_IO_util.config_filename, mode, chartPackage, dataTransformation)
            print('Analysis end', 'Finished running SentiWordNet Sentiment Analysis at')
        else:
            print('Warning','The SentiWordNet algorithm is available only for the English language.\n\nYour currently selected language is '+language+'.\n\nYou can change the language using the Setup dropdownmenu at the bottom of this GUI and selecting "Setup NLP package and corpus language."')

# VADER _______________________________________________________
    import sentiment_analysis_VADER_util
    if SA_algorithm_var=='*' or vader_var==1 and (mean_var or median_var):
        if language=='English':
            if lib_util.checklibFile(GUI_IO_util.sentiment_libPath + os.sep + 'vader_lexicon.txt', 'sentiment_analysis_VADER_util.py')==False:
                return
            if IO_libraries_util.check_inputPythonJavaProgramFile('sentiment_analysis_VADER_util.py')==False:
                return
            print('Analysis start', 'Started running VADER Sentiment Analysis at')
            sentiment_analysis_VADER_util.main("", inputDir, outputDir, mode, chartPackage, dataTransformation)
            print('Analysis end', 'Finished running VADER Sentiment Analysis at')
        else:
            print('Warning','The VADER algorithm is available only for the English language.\n\nYour currently selected language is '+language+'.\n\nYou can change the language using the Setup dropdownmenu at the bottom of this GUI and selecting "Setup NLP package and corpus language."')