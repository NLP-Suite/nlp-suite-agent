import sys
import GUI_util
import IO_libraries_util

if not IO_libraries_util.install_all_Python_packages(GUI_util.window, "spell-checker_main.py",
                                              ['os', 're', 'nltk', 'pandas',
                                               'collections','subprocess', 'time', 'tkinter']):
    sys.exit(0)

import os
import tkinter as tk
import tkinter.messagebox as mb

import GUI_util
import GUI_IO_util
import IO_files_util
import file_spell_checker_util

# RUN section ______________________________________________________________________________________________________________________________________________________

def run(inputFilename, inputDir, outputDir,
        openOutputFiles,
        chartPackage,
        dataTransformation,
        by_all_words_var,
        bydictionary_value_var,
        selectedCsvFile_var,
        byNER_value_var,
        NER_list,
        similarity_value,
        check_withinSubDir,
        spelling_checker_var,
        checker_value_var,
        check_withinSubDir_spell_checker_var):

    config_filename = GUI_util.config_filename_selected_config.get()

    filesToOpen = []
    df_list = []
    df = []

# spell checking by Python NLTK unusual words algorithms -------------------------------------------------------------------------------------------------

    if spelling_checker_var:
        if checker_value_var == '*' or checker_value_var == "Spell checker (via NLTK unusual words)":
            print("checker_value_var", checker_value_var)
            if checker_value_var == '*':
                silent=True
            else:
                silent=False
            # openOutputFiles=False
            filesToOpen=file_spell_checker_util.nltk_unusual_words(GUI_util.window, inputFilename, inputDir, outputDir, config_filename, False,
													   chartPackage, dataTransformation, silent, config_filename)

        if checker_value_var == '*' or "detector" in checker_value_var:
            file_spell_checker_util.language_detection(window, inputFilename, inputDir, outputDir, config_filename, openOutputFiles, chartPackage, dataTransformation)

        if checker_value_var == '*' or 'autocorrect' in checker_value_var or 'pyspellchecker' in checker_value_var or 'textblob' in checker_value_var:
            autocorrect_df, pyspellchecker_df,textblob_df = file_spell_checker_util.spellcheck(inputFilename, inputDir, checker_value_var, check_withinSubDir_spell_checker_var)
        if checker_value_var == '*' or 'autocorrect' in checker_value_var:
            autocorrect_file_name = IO_files_util.generate_output_file_name(inputFilename, inputDir, outputDir, '.csv', 'spell_autocorrect')
            autocorrect_df.to_csv(autocorrect_file_name,encoding='utf-8', index=False)
            filesToOpen.append(autocorrect_file_name)
        if checker_value_var == '*' or 'BERT' in checker_value_var:
            pyspellchecker_file_name = IO_files_util.generate_output_file_name(inputFilename, inputDir, outputDir, '.csv', 'spell_pyspellchecker')
            import BERT_util
            BERT_output = BERT_util.spell_checker_bert(window, inputFilename, inputDir, outputDir, '', chartPackage, dataTransformation)
            filesToOpen.append(BERT_output)
        if checker_value_var == '*' or 'pyspellchecker' in checker_value_var:
            pyspellchecker_file_name = IO_files_util.generate_output_file_name(inputFilename, inputDir, outputDir, '.csv', 'spell_pyspellchecker')
            pyspellchecker_df.to_csv(pyspellchecker_file_name,encoding='utf-8', index=False)
            filesToOpen.append(pyspellchecker_file_name)
        if checker_value_var == '*' or 'textblob' in checker_value_var:
            textblob_file_name = IO_files_util.generate_output_file_name(inputFilename, inputDir, outputDir, '.csv', 'spell_textblob')
            textblob_df.to_csv(textblob_file_name,encoding='utf-8', index=False)
            filesToOpen.append(textblob_file_name)
        if 'Replace' in checker_value_var:
            file_spell_checker_util.spelling_checker_cleaner(window,inputFilename, inputDir, outputDir, openOutputFiles,config_filename)

        if checker_value_var == "Spell checker (via Java tool)":
            mb.showwarning(title='Option not available',
                           message="The 'Spell checker(via Java tool)' is not available.\n\nPlease, select one of the other available options and try again.\n\nSorry!")
            return

# spell checking by CoreNLP algorithms -------------------------------------------------------------------------------------------------

    else:
        if bydictionary_value_var:
            mb.showwarning(title='Option under testing',
                           message='The dictionary option is not completed yet.\n\nPlease, use with caution.')
            # return
        if by_all_words_var == False and byNER_value_var == False and spelling_checker_var == False and bydictionary_value_var == False:
            mb.showwarning(title='No selected options',
                           message='No options have been seleced.\n\nPlease, select one of the available options and try again.')
            return

        if byNER_value_var and len(NER_list) == 0:
            mb.showwarning(title='Missing NER tag',
                           message='The word similarity script requires a valid NER entry.\n\nPlease, select an NER tag and try again.')
            return

        if inputFilename!='':
            mb.showwarning(title='Input warning',
                           message='The Levenshtein\'s distance can only be computed for documents in a directory and/or sub-directories.\n\nPlease, select a directory in input and try again.')
            return

        if check_withinSubDir and (not spelling_checker_var) and (not bydictionary_value_var):
            # def check_for_typo_sub_dir(inputDir, outputDir, inputCsvDictionaryFile, openOutputFiles, chartPackage,
            #                            dataTransformation, NERs, similarity_value, by_all_tokens_var,
            #                            spelling_checker_var=False):
            #
                outputFiles = file_spell_checker_util.check_for_typo_sub_dir(inputDir, outputDir, selectedCsvFile_var,
                                                                         openOutputFiles,
                                                                         chartPackage,
                                                                         dataTransformation,
																		 NER_list, similarity_value,
																		 by_all_words_var,
                                                                         spelling_checker_var)
        else:
            outputFiles = file_spell_checker_util.check_for_typo(inputDir, outputDir, selectedCsvFile_var,
                                                                 openOutputFiles, chartPackage,
                                                                 dataTransformation,
                                                                 NER_list, similarity_value,
																 by_all_words_var)

        if outputFiles!=None:
            filesToOpen.append(outputFiles)

    if openOutputFiles:
        IO_files_util.OpenOutputFiles(GUI_util.window, openOutputFiles, filesToOpen, outputDir, scriptName)

# the values of the GUI widgets MUST be entered in the command otherwise they will not be updated
run_similarity_command = lambda: run(
                                     GUI_util.inputFilename.get(),
                                     GUI_util.input_main_dir_path.get(),
                                     GUI_util.output_dir_path.get(),
                                     GUI_util.open_csv_output_checkbox.get(),
                                     GUI_util.charts_package_options_widget.get(),
                                     GUI_util.data_transformation_options_widget.get(),
                                     by_all_words_var.get(),
                                     bydictionary_value_var.get(),
                                     selectedCsvFile_var.get(),
                                     byNER_value_var.get(),
                                     NER_list,
                                     similarity_value_var.get(),
                                     check_withinSubDir_var.get(),
                                     spelling_checker_var.get(),
                                     checker_value_var.get(),
                                     check_withinDir_spell_checker_var.get())

GUI_util.run_button.configure(command=run_similarity_command)

# GUI section ______________________________________________________________________________________________________________________________________________________
# the GUIs are all setup to run with a brief I/O display or full display (with filename, inputDir, outputDir)
#   just change the next statement to True or False IO_setup_display_brief=True
IO_setup_display_brief=True
GUI_width=GUI_IO_util.get_GUI_width(3)
GUI_height=640 # height of GUI with full I/O display

if IO_setup_display_brief:
    GUI_height = GUI_height - 80
    y_multiplier_integer = GUI_util.y_multiplier_integer  # IO BRIEF display
    increment=0 # used in the display of HELP messages
else: # full display
    # GUI CHANGES add following lines to every special GUI
    # +3 is the number of lines starting at 1 of IO widgets
    # y_multiplier_integer=GUI_util.y_multiplier_integer+2
    y_multiplier_integer = GUI_util.y_multiplier_integer + 2  # IO FULL display
    increment=2

GUI_size = str(GUI_width) + 'x' + str(GUI_height)

GUI_label = 'Graphical User Interface (GUI) for Spelling Checker and Word Similarity (Levenshtein\'s Word/Edit Distance)'
config_filename = 'NLP_default_IO_config.csv'

head, scriptName = os.path.split(os.path.basename(__file__))

# The 4 values of config_option refer to:
#   input file
        # 1 for CoNLL file
        # 2 for TXT file
        # 3 for csv file
        # 4 for any type of file
        # 5 for txt or html
        # 6 for txt or csv
#   input dir
#   input secondary dir
#   output dir
config_input_output_numeric_options=[2,1,0,1]

GUI_util.set_window(GUI_size, GUI_label, config_filename, config_input_output_numeric_options)

window = GUI_util.window
# config_input_output_numeric_options = GUI_util.config_input_output_numeric_options
# config_filename = GUI_util.config_filename
inputFilename = GUI_util.inputFilename
input_main_dir_path = GUI_util.input_main_dir_path

GUI_util.GUI_top(config_input_output_numeric_options, config_filename, IO_setup_display_brief, scriptName)

NER_list = []

Levenshtein_distance_var = tk.IntVar()
by_all_words_var = tk.IntVar()
bydictionary_value_var = tk.IntVar()
selectedCsvFile_var=tk.StringVar()
byNER_value_var = tk.IntVar()
NER_value_var = tk.StringVar()
selected_NER_list_var = tk.StringVar()
similarity_value_var = tk.IntVar()
check_withinSubDir_var = tk.IntVar()
spelling_checker_var = tk.IntVar()
checker_value_var = tk.StringVar()
check_withinDir_spell_checker_var = tk.IntVar()

def clear(e):
    by_all_words_var.set(0)
    bydictionary_value_var.set(0)
    selectedCsvFile_var.set('')
    byNER_value_var.set(0)
    NER_value_var.set('')
    selected_NER_list_var.set('')
    NER_list = []
    similarity_value_var.set(80)
    checker_value_var.set('')
    GUI_util.tips_dropdown_field.set('Open TIPS files')


window.bind("<Escape>", clear)


def build_NER_list():
    if NER_value_var.get() in selected_NER_list_var.get():
        return
    if NER_value_var.get() == '*' or selected_NER_list_var.get() == '*':
        selected_NER_list_var.set('')
    if NER_value_var.get() != '*' and NER_value_var.get() != '' and selected_NER_list_var.get() != '' and NER_value_var.get() not in selected_NER_list_var.get():
        selected_NER_list_var.set(selected_NER_list_var.get() + "," + str(NER_value_var.get()))
    else:
        selected_NER_list_var.set(NER_value_var.get())
    return


Levenshtein_distance_checkbox = tk.Checkbutton(window, text='Run Levensthein\' distance algorithm', state='normal',
                                               variable=Levenshtein_distance_var, onvalue=1, offvalue=0, command=lambda: activate_all_options())
# the button widget has hover-over effects (no_hover_over_widget=False) and the info displayed is in text_info
# the two x-coordinate and x-coordinate_hover_over must have the same values
y_multiplier_integer = GUI_IO_util.placeWidget(window,
    GUI_IO_util.labels_x_coordinate, y_multiplier_integer,
    Levenshtein_distance_checkbox, False, False, True, False, 90, GUI_IO_util.labels_x_coordinate, 'Check the spelling of words in your corpus using the Levenshtein edit distance.\nSelect any of the options listed below.')

by_all_words_var.set(0)
by_all_words_checkbox = tk.Checkbutton(window, text='Check all words against one another', state='normal',
                                        variable=by_all_words_var, onvalue=1, offvalue=0, command=lambda: activate_all_options())
# the button widget has hover-over effects (no_hover_over_widget=False) and the info displayed is in text_info
# the two x-coordinate and x-coordinate_hover_over must have the same values
y_multiplier_integer = GUI_IO_util.placeWidget(window,
    GUI_IO_util.labels_x_indented_coordinate, y_multiplier_integer,
    by_all_words_checkbox, False, False, True, False, 90, GUI_IO_util.labels_x_indented_coordinate, 'Check each word in your corpus against each and every other word in the corpus.')

bydictionary_value_var.set(0)
bydictionary_value_checkbox = tk.Checkbutton(window, state='disabled', text='Check all words against dictionary "true" values', variable=bydictionary_value_var,
                                      onvalue=1, offvalue=0, command=lambda: activate_all_options())
# the button widget has hover-over effects (no_hover_over_widget=False) and the info displayed is in text_info
# the two x-coordinate and x-coordinate_hover_over must have the same values
y_multiplier_integer = GUI_IO_util.placeWidget(window,
    GUI_IO_util.labels_x_indented_coordinate, y_multiplier_integer,
    bydictionary_value_checkbox, False, False, True, False, 90, GUI_IO_util.labels_x_indented_coordinate, 'Check all words against a set of "true" spelling values in a csv file.\nOnly the first column will be considered; any other colum will be ignored.')

dictionary_button=tk.Button(window, width=20, text='Select dictionary file',command=lambda: get_dictionary_file(window,'Select INPUT dictionary file', [("dictionary files", "*.csv")]))
y_multiplier_integer=GUI_IO_util.placeWidget(window,GUI_IO_util.labels_x_indented_coordinate, y_multiplier_integer,dictionary_button,True)

def get_dictionary_file(window,title,fileType):
    initialFolder = os.path.dirname(os.path.abspath(__file__))
    filePath = tk.filedialog.askopenfilename(title = title, initialdir = initialFolder, filetypes = fileType)
    if len(filePath)>0:
        #always disabled; user cannot tinker with the selection
        #selectedCsvFile.config(state='disabled')
        selectedCsvFile_var.set(filePath)

#setup a button to open Windows Explorer on the selected input directory
# current_y_multiplier_integer=y_multiplier_integer-1
openInputFile_button = tk.Button(window, width=GUI_IO_util.open_file_directory_button_width, text='', command=lambda: IO_files_util.openFile(window, selectedCsvFile_var.get()))
# the button widget has hover-over effects (no_hover_over_widget=False) and the info displayed is in text_info
# the two x-coordinate and x-coordinate_hover_over must have the same values
y_multiplier_integer = GUI_IO_util.placeWidget(window,
    GUI_IO_util.file_search_byWord_openInputFile_button_pos, y_multiplier_integer,
    openInputFile_button, True, False, True, False, 90, GUI_IO_util.file_search_byWord_openInputFile_button_pos, "Open selected csv dictionary file")

selectedCsvFile = tk.Entry(window,width=GUI_IO_util.file_search_byWord_widget_width,state='disabled',textvariable=selectedCsvFile_var)
y_multiplier_integer=GUI_IO_util.placeWidget(window,GUI_IO_util.file_search_byWord_selectedCsvFile_pos,y_multiplier_integer,selectedCsvFile)

byNER_value_var.set(0)

byNER_value_checkbox = tk.Checkbutton(window, state='normal', text='Check words by their NER tag', variable=byNER_value_var,
                                      onvalue=1, offvalue=0, command=lambda: activate_all_options())
y_multiplier_integer = GUI_IO_util.placeWidget(window,GUI_IO_util.labels_x_indented_coordinate, y_multiplier_integer,
                                               byNER_value_checkbox)

NER_value_lb = tk.Label(window, text='Select NER tag for computing word similarity')
y_multiplier_integer = GUI_IO_util.placeWidget(window,GUI_IO_util.labels_x_indented_coordinate + 20,
                                               y_multiplier_integer, NER_value_lb, True)
NER_value = tk.OptionMenu(window, NER_value_var, '*', 'CITY', 'COUNTRY', 'STATE_OR_PROVINCE', 'LOCATION',
                          'ORGANIZATION', 'PERSON')
y_multiplier_integer = GUI_IO_util.placeWidget(window,GUI_IO_util.entry_box_x_coordinate + 50, y_multiplier_integer,
                                               NER_value, True)

selected_NER_list_var.set('')
selected_NER_list = tk.Entry(window, width=40, textvariable=selected_NER_list_var)
selected_NER_list.config(state='disabled')
y_multiplier_integer = GUI_IO_util.placeWidget(window,GUI_IO_util.labels_x_coordinate + 600, y_multiplier_integer,
                                               selected_NER_list)


def activate_NER_list_entry(*args):
    global NER_list
    if NER_value_var.get() != '':
        if '*' in selected_NER_list_var.get():
            mb.showwarning(title='Selection error',
                           message="You have already selected to process all NER values via *. You cannot select any other NER tag.\n\nPress ESCape to clear the current selection.")
            return
        build_NER_list()
        NER_list = [selected_NER_list_var.get()]


NER_value_var.trace('w', activate_NER_list_entry)
activate_NER_list_entry()

similarity_value_var.set(80)
similarity_value_lb = tk.Label(window, text='Enter word length for computing similarity')
y_multiplier_integer = GUI_IO_util.placeWidget(window,GUI_IO_util.labels_x_indented_coordinate, y_multiplier_integer,
                                               similarity_value_lb, True)
similarity_value = tk.Entry(window, width=5, textvariable=similarity_value_var)
y_multiplier_integer = GUI_IO_util.placeWidget(window,GUI_IO_util.entry_box_x_coordinate, y_multiplier_integer,
                                               similarity_value, True)

check_withinSubDir_var.set(0)
check_withinSubDir_checkbox = tk.Checkbutton(window, text='Check WITHIN each subdirectory only',
                                             variable=check_withinSubDir_var, onvalue=1, offvalue=0)
y_multiplier_integer = GUI_IO_util.placeWidget(window,GUI_IO_util.labels_x_coordinate + 600, y_multiplier_integer,
                                               check_withinSubDir_checkbox)

spelling_checker_checkbox = tk.Checkbutton(window, text='Run spelling checker',state='normal',variable=spelling_checker_var, onvalue=1, offvalue=0, command=lambda: activate_all_options())
# the button widget has hover-over effects (no_hover_over_widget=False) and the info displayed is in text_info
# the two x-coordinate and x-coordinate_hover_over must have the same values
y_multiplier_integer = GUI_IO_util.placeWidget(window,
    GUI_IO_util.labels_x_coordinate, y_multiplier_integer,
    spelling_checker_checkbox, True, False, True, False, 90, GUI_IO_util.labels_x_coordinate, 'Check the spelling of words in your corpus using various spelling algorithms edit distance.')

checker_value_var.set('*')
spelling_checker_value_lb = tk.Label(window, text='Select script')
y_multiplier_integer=GUI_IO_util.placeWidget(window,GUI_IO_util.labels_x_indented_coordinate+150,y_multiplier_integer,spelling_checker_value_lb,True)
spelling_checker_value = tk.OptionMenu(window, checker_value_var, '*',
                                       'Language detector',
                                       'Spell checker (via autocorrect)',
                                       'Spell checker (via BERT)',
                                       'Spell checker (via NLTK unusual words)',
                                       'Spell checker (via pyspellchecker)',
                                       'Spell checker (via textblob)',
                                       'Find & Replace string (via csv file)')

# the button widget has hover-over effects (no_hover_over_widget=False) and the info displayed is in text_info
# the two x-coordinate and x-coordinate_hover_over must have the same values
y_multiplier_integer = GUI_IO_util.placeWidget(window,
    GUI_IO_util.entry_box_x_coordinate, y_multiplier_integer,
    spelling_checker_value, True, False, True, False, 90, GUI_IO_util.entry_box_x_coordinate, 'Check the spelling of words in your corpus using various spelling algorithms.\nSelect * to run all algorithms.')
# y_multiplier_integer=GUI_IO_util.placeWidget(window,GUI_IO_util.entry_box_x_coordinate, y_multiplier_integer,spelling_checker_value,True)

check_withinDir_spell_checker_var.set(1)
check_withinDir_spell_checker_checkbox = tk.Checkbutton(window, text='Check WITHIN main directory only',
                                             variable=check_withinDir_spell_checker_var, onvalue=1, offvalue=0)
y_multiplier_integer = GUI_IO_util.placeWidget(window,GUI_IO_util.labels_x_coordinate + 600, y_multiplier_integer,
                                               check_withinDir_spell_checker_checkbox)

def activate_all_options(*args):
    Levenshtein_distance_checkbox.configure(state='normal')
    spelling_checker_checkbox.configure(state='normal')
    by_all_words_checkbox.configure(state='disabled')
    bydictionary_value_checkbox.configure(state='disabled')
    byNER_value_checkbox.configure(state='disabled')
    NER_value.config(state='disabled')
    NER_value_var.set('')
    selected_NER_list_var.set('')
    NER_value.config(state='disabled')
    similarity_value.config(state='disabled')
    check_withinSubDir_checkbox.config(state='disabled')
    selected_NER_list.config(state='disabled')
    spelling_checker_value.config(state='disabled')
    if Levenshtein_distance_var.get() == True:
        spelling_checker_checkbox.configure(state='disabled')
        by_all_words_checkbox.configure(state='normal')
        bydictionary_value_checkbox.configure(state='normal')
        byNER_value_checkbox.configure(state='normal')
        similarity_value.config(state='normal')
        check_withinSubDir_checkbox.config(state='normal')
        if by_all_words_var.get() == True:
            bydictionary_value_checkbox.configure(state='disabled')
            byNER_value_checkbox.configure(state='disabled')
        if bydictionary_value_var.get() == True:
            by_all_words_checkbox.configure(state='disabled')
            byNER_value_checkbox.configure(state='disabled')
        if byNER_value_var.get() == True:
            by_all_words_checkbox.configure(state='disabled')
            NER_value.config(state='normal')
            selected_NER_list.config(state='normal')
    else:
        spelling_checker_checkbox.configure(state='normal')
    if spelling_checker_var.get() == True:
        Levenshtein_distance_checkbox.configure(state='disabled')
        spelling_checker_value.config(state='normal')
    else:
        Levenshtein_distance_checkbox.configure(state='normal')


# Levenshtein_distance_var.trace('w', activate_all_options)
# by_all_words_var.trace('w', activate_all_options)
# bydictionary_value_var.trace('w', activate_all_options)
# byNER_value_var.trace('w', activate_all_options)
# spelling_checker_var.trace('w', activate_all_options)

activate_all_options()

videos_lookup = {'No videos available':''}
videos_options='No videos available'

TIPS_lookup = {'Word similarity (Levenshtein edit distance)': 'TIPS_NLP_Word similarity (Levenshtein edit distance).pdf',
               'File checker, converter, cleaner':'TIPS_NLP_File checker & converter & cleaner.pdf',
               'Filename checker':'TIPS_NLP_Filename checker.pdf',
               'Text encoding':'TIPS_NLP_Text encoding.pdf',
               'utf-8 text encoding':'TIPS_NLP_Text encoding (utf-8).pdf',
               'Spelling checker': 'TIPS_NLP_Spelling checker.pdf'}
TIPS_options = 'Text encoding', 'utf-8 text encoding', 'Spelling checker', 'Word similarity (Levenshtein edit distance)', 'File checker, converter, cleaner', 'Filename checker'


# add all the lines to the end to every special GUI
# change the last item (message displayed) of each line of the function y_multiplier_integer = help_buttons
# any special message (e.g., msg_anyFile stored in GUI_IO_util) will have to be prefixed by GUI_IO_util.
def help_buttons(window, help_button_x_coordinate, y_multiplier_integer):
    if not IO_setup_display_brief:
        y_multiplier_integer = GUI_IO_util.place_help_button(window, help_button_x_coordinate, y_multiplier_integer, "NLP Suite Help",
                                      GUI_IO_util.msg_txtFile)
        y_multiplier_integer = GUI_IO_util.place_help_button(window, help_button_x_coordinate, y_multiplier_integer, "NLP Suite Help",
                                      GUI_IO_util.msg_corpusData)
        y_multiplier_integer = GUI_IO_util.place_help_button(window, help_button_x_coordinate, y_multiplier_integer, "NLP Suite Help",
                                      GUI_IO_util.msg_outputDirectory)
    else:
        y_multiplier_integer = GUI_IO_util.place_help_button(window, help_button_x_coordinate, y_multiplier_integer, "NLP Suite Help",
                                      GUI_IO_util.msg_IO_setup)

    y_multiplier_integer = GUI_IO_util.place_help_button(window, help_button_x_coordinate, y_multiplier_integer, "NLP Suite Help",
                                  'Please, tick the checkbox if you wish to use Levenshtein\' edit distance algorithm.' + GUI_IO_util.msg_Esc)
    y_multiplier_integer = GUI_IO_util.place_help_button(window, help_button_x_coordinate, y_multiplier_integer, "NLP Suite Help",
                                  'Please, tick the checkbox if you wish to find the edit distance of any word in your input document(s), regardless of their NER tag.' + GUI_IO_util.msg_Esc)
    y_multiplier_integer = GUI_IO_util.place_help_button(window,help_button_x_coordinate,y_multiplier_integer,"NLP Suite Help", "Please, tick the checkbox to search input txt file(s) using the values contained in a csv dictionary file.")
    y_multiplier_integer = GUI_IO_util.place_help_button(window,help_button_x_coordinate,y_multiplier_integer,"NLP Suite Help", "Please, click to select a csv file containing a list of values to be used as a dictionary for searching the input file(s).\n\nEntries in the file, one per line, can be single words or collocations, i.e., combinations of words such as 'coming out,' 'standing in line'.\n\nThe little square button to the right will allow you to open the selected csv file.\n\nThe csv filename will be displayed in the entry widget to the right.")
    y_multiplier_integer = GUI_IO_util.place_help_button(window, help_button_x_coordinate, y_multiplier_integer, "NLP Suite Help",
                                  'Please, tick the checkbox if you wish to find the edit distance of words in your input document(s) by their selected NER values.' + GUI_IO_util.msg_Esc)
    y_multiplier_integer = GUI_IO_util.place_help_button(window, help_button_x_coordinate, y_multiplier_integer, "NLP Suite Help",
                                  'Please, using the dropdown menu, select the NER (Named Entity Recognition) type you wish to use for computing spelling differences (Levenshtein\'s edit distance).\n\nFor all NER values, select *; for multiple values, but not *, enter the NER values, comma separated, in the next widget.' + GUI_IO_util.msg_Esc)
    y_multiplier_integer = GUI_IO_util.place_help_button(window, help_button_x_coordinate, y_multiplier_integer, "NLP Suite Help",
                                  'Please, enter the value of word length (in number of characters) to be used to gage Levenshtein\'s edit distance or word similarity (default value 80). You can enter a number on a scale from 0 to 100, with 100 being completely the same.\n\nIf a word is shorter than the selected word lenght (in number of characters):\n   1 or more character difference will be considered as a possible typo;\n\nIf a word is equal or longer than the selected word lenght (in number of characters):\n   2 or more characters difference will be considered as a possible typo.\n\nYou have the option of checking for selected NER values WITHIN each subdirectory only or ACROSS all subdirectories (or an entire directory, for that matter); in this second option, the algorithm will take much longer to process.\n\nThe output list fully processes words with a frequency greater than 1.' + GUI_IO_util.msg_Esc)
    y_multiplier_integer = GUI_IO_util.place_help_button(window, help_button_x_coordinate, y_multiplier_integer, "NLP Suite Help",
                                  'Please, tick the checkbox if you wish to run a spelling checker.\n\nLanguage detection is carried out via LANGDETECT, LANGID, SPACY, STANZA. Languages are exported via the ISO 639 two-letter code. ISO 639 is a standardized nomenclature used to classify languages (check here for the list https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes).\nAll language detection algorithms, except for Stanza, export the probability of detection of a specific detected language.' + GUI_IO_util.msg_Esc)
    y_multiplier_integer = GUI_IO_util.place_help_button(window, help_button_x_coordinate, y_multiplier_integer, "NLP Suite Help",
                                  GUI_IO_util.msg_openOutputFiles)
    return y_multiplier_integer -1

y_multiplier_integer = help_buttons(window, GUI_IO_util.help_button_x_coordinate, 0)

# change the value of the readMe_message
readMe_message = "This Python 3 script provides a way of checking for word similarieties (or dissimilarities) using the Levenshtein's distance (also popularly called the edit distance). The algorithm can also be used to check word spelling.\n\nIn INPUT the scripts expect a directory where the software Stanford CoreNLP has been downloaded and a main drectory where txt files to be analyzed are stored.\n\nIn OUTPUT, the scripts will save the csv files and Excel charts written by the various scripts. The csv output list contains words with a frequency greater than 1."
readMe_command = lambda: GUI_IO_util.display_help_button_info("NLP Suite Help", readMe_message)
GUI_util.GUI_bottom(config_filename, config_input_output_numeric_options, y_multiplier_integer, readMe_command, videos_lookup, videos_options, TIPS_lookup, TIPS_options, IO_setup_display_brief, scriptName)

GUI_util.window.mainloop()
