import os

NLP_Suite_website_name = 'NLP Suite GitHub'

# HELP messages
introduction_main = "Welcome to this Python 3 script.\nFor brief general information about this script, click on the \"Read Me\" button.\nFor brief information on specific lines click on any of the \"?HELP\" buttons.\nFor longer information on various aspects of the script, click on the \"Open TIPS files\" button and select the pdf help file to view.\nAfter selecting an option, click on \"RUN\" (the RUN button is disabled until all I/O information has been entered).   Click on \"CLOSE\" to exit."
msg_openExplorer="\n\nA small button appears next to the select directory button. Click on the button to open Windows Explorer on the directory displayed, if one is displayed, or on the directory where the NLP script is saved."
msg_openFile="\n\nA small button appears next to the select file button. Click on the button to open the file, if one has been selected, as a check that you selected the correct file." # + msg_fileButtonDisabled
msg_Esc="\n\nPress the ESCape button to clear any previously selected options and start fresh."

msg_IO_config="The default or GUI-specific config files are 2-columns csv files with the 4 I/O labels - Input filename with path, Input files directory, Input files secondary directory, Output files directory - in the first column and the file or directory path in the second column.\n\nThe fields Input filename with path and Input files directory are MUTUALLY EXCLUSIVE. YOU CAN ONLY HAVE ONE OR THE OTHER BUT NOT BOTH.\n\nA couple of scripts in the NLP Suite require two input directories (e.g., for source and target files, as in social_science_researh_main and file_classifier_main)\n\nCONFIG FILES ARE STORED IN THE SUBDIRECTORY config OF THE MAIN NLP SUITE DIRECTORY."

msg_IO_setup="Please, using the dropdown menu, select the type of INPUT/OUTPUT configuration you wish to use in this GUI: Default I/O configuration or GUI-specific I/O configuration.\n\nEach option will allow you to select and INPUT file or directory where the files(s) to be used in input are stored and an OUTPUT directory where files produced by the NLP tools will be saved (csv, txt, html, kml, jpg).\n\n   The default configuration is the I/O option used for all GUIs as default;\n   the GUI-specific I/O configuration is an alternative I/O option only used in a specific GUI.\n\nYou can click on the display area and scroll to visualize the current configuration. You can also click on the 'Setup INPUT/OUTPUT configuration' button to get a better view of the available options.\n\nClick on the small buttons to the right of the I/O display area to open the input file, the input directory, the output directory displayed, and the config file where these options are saved. "+msg_IO_config
msg_save_uponClose="\n\nWHEN CLICKING ON CLOSE, YOU WILL BE ASKED IF YOU WANT TO SAVE YOUR SELECTED OPTIONS, IF DIFFERENT FROM CURRENT SELECTION."
msg_CoreNLP="Please, select the directory where you downloaded the Stanford CoreNLP software.\n\nYou can download Stanford CoreNLP from https://stanfordnlp.github.io/CoreNLP/download.html\n\nYou can place the Stanford CoreNLP folder anywhere on your machine. But... on some machines CoreNLP will not run unless the folder is inside the NLP folder.\n\nIf you suspect that CoreNLP may have given faulty results for some sentences, you can test those sentences directly on the Stanford CoreNLP website at https://corenlp.run\n\nYOU MUST BE CONNECTED TO THE INTERNET TO RUN CoreNLP."
msg_WordNet="Please, select the directory where you downloaded the WordNet lexicon database.\n\nYou can download WordNet from https://wordnet.princeton.edu/download/current-version."
msg_Mallet="Please, select the directory where you downloaded the MALLET topic modeling software."
msg_CoNLL="Please, select a csv CoNLL table that you would like to analyze.\n\nA CoNLL table is a file generated by the Python script StanfordCoreNLP.py. The CoreNLP script parses a set of text documents using the Stanford CoreNLP parser, providing a dependency tree for each sentence of the documents. In a CoNLL table, each token is labeled with a part-of-speech tag (POSTAG), a Dependency Relation tag (DEPREL), its dependency relation within the corresponding dependency tree, and other useful information." + msg_openFile
msg_corpusData="Please, select the directory where you store your TXT corpus to be analyzed. ALL TXT FILES PRESENT IN THE DIRECTORY WILL BE PARSED. NON TXT FILES WILL BE IGNORED. MOVE ANY TXT FILES YOU DO NOT WISH TO PROCESS TO A DIFFERENT DIRECTORY."  + msg_openExplorer # + msg_dirButtonDisabled
msg_anyData="Please, select the directory where you store the files to be analyzed. ALL FILES OF A SELECTED EXTENSION TYPE (pdf, docx, txt, csv, conll), PRESENT IN THE DIRECTORY WILL BE PROCESSED. ALL OTHER FILE TYPES WILL BE IGNORED."  + msg_openExplorer # + msg_dirButtonDisabled
msg_anyFile="Please, select the file to be analyzed (of any type: pdf, docx, txt, csv, conll)."  + msg_openFile
msg_txtFile="Please, select the TXT file to be analyzed." + msg_openFile # + msg_fileButtonDisabled
msg_csvFile="Please, select the csv file to be analyzed." + msg_openFile # + msg_fileButtonDisabled
msg_csv_txtFile="Please, select either a CSV file or a TXT file to be analyzed." + msg_openFile # + msg_fileButtonDisabled
msg_txt_htmlFile="Please, select either a TXT file or an html file to be analyzed." + msg_openFile # + msg_fileButtonDisabled
msg_outputDirectory="Please, select the directory where the script will save all OUTPUT files of any type (txt, csv, png, html).\n\nMOST GUI SCRIPTS WILL ORGANIZE OUTPUT FILES IN SPECIFIC SUBDIRECTORIES INSIDE THE MAIN OUTPUT DIRECTORY SELECTED HERE (e.g., the SVO GUI will create several subdirectories: GIS, SVO, SVO-filtered, SVO-unfiltered, SVO-lemma, WordNet)."  + msg_openExplorer
msg_outputFilename="Please, enter the OUTPUT file name. THE SELECT OUTPUT BUTTON IS DISABLED UNTIL A SEARCHED TOKEN HAS BEEN ENTERED.\n\nThe search result will be saved as a separated csv file with the file path and name entered. \n\nThe same information will be displayed in the command line."
msg_openOutputFiles="Please, tick the checkbox to open automatically (or not open) output csv file(s), including any charts." \
    "\n\nUse the dropdown menu to select the chart package you wish to use for chart visualization (e.g., Excel, plotly). If you do not wish to create and visualize charts, select the 'No charts' option." \
    "\n\nIf you select to create and visualize charts, use the next dropdown menu widget to select the chart type you wish to use (e.g., bar chart, pie chart)." \
    "\n\nIf you select to create and visualize charts, use the next dropdown menu widget to select the type of data transformation to be used for plotting ('No transformation' is the default option'). All charts involving multiple documents are automatically normalized by document size." \
    "\n\nIn the NLP Suite, all CSV FILES that contain information on web links or files with their path will encode this information as hyperlinks. If you click on the hyperlink, it will automatically open the file or take you to a website. IF YOU ARE A MAC USER, YOU MUST OPEN ALL CSV FILES WITH EXCEL, RATHER THAN NUMBERS, OR THE HYPERLINK WILL BE BARRED AND DISPLAYED AS A RED TRIANGLE."
msg_multipleDocsCoNLL="\n\nFOR CONLL FILES THAT INCLUDE MULTIPLE DOCUMENTS, THE EXCEL CHARTS PROVIDE OVERALL FREQUENCIES ACROSS ALL DOCUMENTS. FOR SPECIFIC DOCUMENT ANALYSES, PLEASE USE THE GENERAL EXCEL OUTPUT FILE."
scriptPath = os.path.dirname(os.path.abspath(__file__))
NLPPath=os.path.normpath(os.path.dirname(os.path.abspath(__file__)) + os.sep + os.pardir)
configPath = os.path.join(NLPPath,'config')
libPath = os.path.join(NLPPath,'lib')
image_libPath = os.path.join(NLPPath,'lib'+os.sep+'images')
Google_heatmaps_libPath = os.path.join(NLPPath,'lib'+os.sep+'sampleHeatmap')
Excel_charts_libPath = os.path.join(NLPPath,'lib'+os.sep+'sampleCharts')
sampleData_libPath = os.path.join(NLPPath,'lib'+os.sep+'sampleData')
sentiment_libPath = os.path.join(NLPPath,'lib'+os.sep+'sentimentLib')
concreteness_libPath = os.path.join(NLPPath,'lib'+os.sep+'concretenessLib')
CoreNLP_enhanced_dependencies_libPath = os.path.join(NLPPath,'lib'+os.sep+'CoreNLP_enhanced_dependencies')
wordLists_libPath = os.path.join(NLPPath,'lib'+os.sep+'wordLists')
namesGender_libPath = os.path.join(NLPPath, 'lib'+os.sep+'namesGender')
GISLocations_libPath = os.path.join(NLPPath,'lib'+os.sep+'GIS')
TIPSPath = os.path.join(NLPPath,'TIPS')
videosPath = os.path.join(NLPPath,'videos')
remindersPath = os.path.join(NLPPath, 'reminders')
iconicity_libPath = os.path.join(NLPPath, 'lib'+os.sep+'iconicityLib')
config_filename = 'NLP_default_IO_config.csv'
input_folder = os.path.join(os.path.expanduser("~"), "nlp-suite", "input")
output_folder = os.path.join(os.path.expanduser("~"), "nlp-suite", "output")
external_software = os.path.join(os.path.expanduser("~"), "nlp-suite", "external_software")