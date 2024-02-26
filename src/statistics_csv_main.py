import sys
import GUI_util
import IO_libraries_util

if IO_libraries_util.install_all_Python_packages(GUI_util.window,"Statistics_csv",['tkinter'])==False:
    sys.exit(0)

import os
import tkinter as tk
import tkinter.messagebox as mb

import GUI_IO_util
import IO_csv_util
import IO_user_interface_util
import IO_files_util
import statistics_csv_util

# RUN section ______________________________________________________________________________________________________________________________________________________

def run(inputFilename,inputDir,outputDir,openOutputFiles,chartPackage,dataTransformation,
        all_csv_stats,csv_field_freq,
        csv_list,hover_over_list, groupBy_list, script_to_run):

    if GUI_util.setup_IO_menu_var.get() == 'Default I/O configuration':
        config_filename = 'NLP_default_IO_config.csv'
    else:
        config_filename = scriptName.replace('main.py', 'config.csv')

    filesToOpen=[]

    window=GUI_util.window

    # if inputDir=='' and corpus_stats:
    #     mb.showwarning(title='Input error', message='The selected option - ' + script_to_run + ' - requires a directory in input.\n\nPlease, select a directory and try again.')
    #     return

    if inputFilename!='' and (all_csv_stats or csv_field_freq):
        if inputFilename[-4:]!='.csv':
            mb.showwarning(title='Input error', message='The selected option - ' + script_to_run + ' - requires an input file of type csv.\n\nPlease, select a csv input file and try again.')
            return

    if all_csv_stats or csv_field_freq:
        if IO_libraries_util.check_inputPythonJavaProgramFile('statistics_csv_util.py')==False:
            return
        if csv_field_freq and len(csv_list) == 0:
            mb.showwarning(title='Warning', message='You have selected to compute the frequency of a csv file field but no field has been selected.\n\nPlease, select a csv file field and try again.')
            return

    if all_csv_stats:
        # tempOutputFiles=statistics_csv_util.compute_csv_column_statistics(window,inputFilename,outputDir,
        #                         groupBy_list, [], '', chartPackage, dataTransformation)

        outputFiles=statistics_csv_util.compute_csv_column_statistics_NoGroupBy(window,inputFilename,outputDir,openOutputFiles,chartPackage, dataTransformation)
        if outputFiles:
            if isinstance(outputFiles, str):
                filesToOpen.append(outputFiles)
            else:
                filesToOpen.extend(outputFiles)

    if csv_field_freq:
        if len(csv_list) == 0:
            mb.showwarning(title='Warning', message='You have selected to compute the frequency of a csv file field but no field has been selected.\n\nPlease, select a csv file field and try again.')
            return
        chart_title=''
        # csv_list=['Document','Date']
        outputFiles=statistics_csv_util.compute_csv_column_frequencies(window,
                                                           inputFilename,
                                                           None,
                                                           outputDir,
                                                           openOutputFiles, chartPackage,dataTransformation,
                                                           csv_list,hover_over_list,groupBy_list,
                                                           False,
                                                           chart_title=chart_title,
                                                           fileNameType='CSV',chartType='line',pivot=False)

        if outputFiles!=None:
            if isinstance(outputFiles, str):
                filesToOpen.append(outputFiles)
            else:
                filesToOpen.extend(outputFiles)

    if openOutputFiles:
        IO_files_util.OpenOutputFiles(GUI_util.window, openOutputFiles, filesToOpen, outputDir, scriptName)

#the values of the GUI widgets MUST be entered in the command otherwise they will not be updated
#def run(inputFilename,inputDir,outputDir, dictionary_var, annotator_dictionary, DBpedia_var, annotator_extractor, openOutputFiles):
run_script_command=lambda: run(
                GUI_util.inputFilename.get(),
                GUI_util.input_main_dir_path.get(),
                GUI_util.output_dir_path.get(),
                GUI_util.open_csv_output_checkbox.get(),
                GUI_util.charts_package_options_widget.get(),
                GUI_util.data_transformation_options_widget.get(),
                all_csv_stats_var.get(),
                csv_field_freq_var.get(),
                csv_list,
                hover_over_list,
                groupBy_list,
                script_to_run)

GUI_util.run_button.configure(command=run_script_command)

# GUI section ______________________________________________________________________________________________________________________________________________________

# the GUIs are all setup to run with a brief I/O display or full display (with filename, inputDir, outputDir)
#   just change the next statement to True or False IO_setup_display_brief=True
IO_setup_display_brief=True
GUI_size, y_multiplier_integer, increment = GUI_IO_util.GUI_settings(IO_setup_display_brief,
                             GUI_width=GUI_IO_util.get_GUI_width(3),
                             GUI_height_brief=360, # height at brief display
                             GUI_height_full=440, # height at full display
                             y_multiplier_integer=GUI_util.y_multiplier_integer,
                             y_multiplier_integer_add=2, # to be added for full display
                             increment=2)  # to be added for full display

GUI_label='Graphical User Interface (GUI) for Statistical Analyses of csv Files'
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
config_input_output_numeric_options=[3,0,0,1]

GUI_util.set_window(GUI_size, GUI_label, config_filename, config_input_output_numeric_options)

window = GUI_util.window
# config_input_output_numeric_options = GUI_util.config_input_output_numeric_options
# config_filename = GUI_util.config_filename
inputFilename = GUI_util.inputFilename
inputDir = GUI_util.input_main_dir_path

GUI_util.GUI_top(config_input_output_numeric_options, config_filename, IO_setup_display_brief, scriptName)

n_grams_list=[]
csv_list = []
hover_over_list = []
groupBy_list = []

all_csv_stats_var = tk.IntVar()
csv_field_freq_var = tk.IntVar()
csv_field_var = tk.StringVar()
csv_hover_over_field_var = tk.StringVar()
csv_groupBy_field_var = tk.StringVar()

# corpus_statistics_var = tk.IntVar()
# corpus_statistics_options_menu_var = tk.StringVar()
# corpus_text_options_menu_var = tk.StringVar()
#
# n_grams_var = tk.IntVar()
# n_grams_menu_var = tk.StringVar()
# csv_options_menu_var = tk.StringVar()
# n_grams_options_menu_var = tk.StringVar()

script_to_run = ''


def get_script_to_run(text):
    global script_to_run
    script_to_run = text


def clear(e):
    # corpus_statistics_var.set(0)
    # corpus_statistics_options_menu_var.set('*')
    # corpus_text_options_menu_var.set('')
    all_csv_stats_var.set(0)
    csv_field_freq_var.set(0)
    # n_grams_menu_var.set('Word')
    # reset_n_grams_list()
    reset_csv_list()
    GUI_util.clear("Escape")
window.bind("<Escape>", clear)


all_csv_stats_var.set(0)
all_csv_field_checkbox = tk.Checkbutton(window, text='Compute statistics on all csv-file fields (numeric fields only)',
                                        variable=all_csv_stats_var, onvalue=1, offvalue=0,
                                        command=lambda: get_script_to_run(
                                            'Compute statistics on all csv-file fields (numeric fields only)'))
# place widget with hover-over info
y_multiplier_integer = GUI_IO_util.placeWidget(window,GUI_IO_util.labels_x_coordinate, y_multiplier_integer,
                                   all_csv_field_checkbox,
                                   False, False, True, False, 90, GUI_IO_util.labels_x_coordinate,
                                   "Tick the checkbox then the RUN button to compute basic statistics for all the NUMERIC fields in the input csv file"
                                   "\nCount, Mean, Mode, Median, Standard deviation, Minimum, Maximum, Skewness, Kurtosis, 25% quantile, 50% quantile; 75% quantile")

csv_field_freq_var.set(0)
csv_field_checkbox = tk.Checkbutton(window, text='Compute frequencies of csv-file field(s)',
                                    variable=csv_field_freq_var, onvalue=1, offvalue=0,
                                    command=lambda: get_script_to_run('Compute frequencies of selected csv-file field'))
# place widget with hover-over info
y_multiplier_integer = GUI_IO_util.placeWidget(window,GUI_IO_util.labels_x_coordinate, y_multiplier_integer,
                                   csv_field_checkbox,
                                   True, False, True, False, 90, GUI_IO_util.labels_x_coordinate,
                                   "Tick the checkbox to compute the frequency of a selected csv field"
                                   "\nONLY ONE FIELD CAN BE SELECTED (although multiple group-by and hover-over fields can be selected)")


def activate_viewer_options(*args):
    print()
    # if csv_field_var.get()!='':
    #     if csv_field_var.get() in csv_field_list:
    #         mb.showwarning(title='Warning', message='The option has already been selected. Selection ignored.\n\nYou can see your current selections by clicking the Show button.')
    #         return
    #     if 'Partial match' in viewer_options_menu_var.get() or \
    #             'Normalize' in viewer_options_menu_var.get() or \
    #             'Scale' in viewer_options_menu_var.get():
    #             mb.showwarning(title='Warning', message='The option is not available yet.\n\nSorry!')
    #             return
    #     # remove the case option, when a different one is selected
    #     if 'insensitive' in viewer_options_menu_var.get() and 'sensitive' in str(viewer_options_list):
    #         viewer_options_list.remove('Case sensitive (default)')
    #     if 'sensitive' in viewer_options_menu_var.get() and 'insensitive' in str(viewer_options_list):
    #         viewer_options_list.remove('Case insensitive')
    #     viewer_options_list.append(viewer_options_menu_var.get())
    #     viewer_options_menu.configure(state="disabled")
    #     add_viewer_button.configure(state='normal')
    #     reset_viewer_button.configure(state='normal')
    #     show_viewer_button.configure(state='normal')
    # else:
    #     add_viewer_button.configure(state='disabled')
    #     reset_viewer_button.configure(state='disabled')
    #     show_viewer_button.configure(state='disabled')
    #     viewer_options_menu.configure(state="normal")

activate_viewer_options()

add_csv_field_button = tk.Button(window, text='+', width=GUI_IO_util.add_button_width,height=1,state='normal',command=lambda: activate_viewer_options())
# place widget with hover-over info
y_multiplier_integer = GUI_IO_util.placeWidget(window, GUI_IO_util.open_TIPS_x_coordinate+20, y_multiplier_integer,
                                               add_csv_field_button, True, False, False, False, 90,
                                               GUI_IO_util.open_reminders_x_coordinate,
                                               "Click on the + button to add another csv file field")

menu_values = ['']
reset_csv_button = tk.Button(window, text='Reset ', width=GUI_IO_util.reset_button_width,height=1,state='disabled',command=lambda: reset_csv_list())
# place widget with hover-over info
y_multiplier_integer = GUI_IO_util.placeWidget(window,GUI_IO_util.statistics_csv_reset_csv_button_pos, y_multiplier_integer,
                                   reset_csv_button,
                                   True, False, True, False, 90, GUI_IO_util.statistics_csv_reset_csv_button_pos,
                                   "Click the 'Reset ' button to clear all selected csv field, group-by field and hover-over field, and start fresh")

show_csv_button = tk.Button(window, text='Show', width=GUI_IO_util.show_button_width,height=1,state='disabled',command=lambda: show_csv_list())
# place widget with hover-over info
y_multiplier_integer = GUI_IO_util.placeWidget(window,GUI_IO_util.statistics_csv_show_csv_button_pos, y_multiplier_integer,
                                   show_csv_button,
                                   True, False, True, False, 90, GUI_IO_util.statistics_csv_show_csv_button_pos,
                                   "Click the 'Show' button to display the currrently selected csv field, group-by field and hover-over field")

csv_field_lb = tk.Label(window, text='csv field')
y_multiplier_integer = GUI_IO_util.placeWidget(window,GUI_IO_util.statistics_csv_csv_field_lb_pos, y_multiplier_integer,
                                               csv_field_lb, True)

csv_field_menu = tk.OptionMenu(window, csv_field_var, *menu_values)
# place widget with hover-over info
y_multiplier_integer = GUI_IO_util.placeWidget(window,GUI_IO_util.statistics_csv_csv_field_menu_pos, y_multiplier_integer,
                                   csv_field_menu,
                                   False, False, True, False, 90, GUI_IO_util.open_TIPS_x_coordinate,
                                   "Use the dropdown menu to select the csv file field to be used to compute frequencies"
                                   "\nONLY ONE FIELD CAN BE SELECTED (although multiple group-by and hover-over fields can be selected)")

def reset_csv_list():
    csv_list.clear()
    hover_over_list.clear()
    groupBy_list.clear()
    csv_field_var.set('')
    csv_groupBy_field_var.set('')
    csv_hover_over_field_var.set('')
    csv_field_menu.configure(state='normal')

def show_csv_list():
    if len(csv_list)==0:
        mb.showwarning(title='Warning', message='There are no currently selected csv field options.')
    else:
        mb.showwarning(title='Warning', message='The currently selected csv field options are:\n'
        '\n   CSV FIELD: ' + ', '.join(csv_list) +
        '\n   GROUP-BY FIELD(S): ' + ', ' .join(groupBy_list) +
        '\n   HOVER-OVER FIELD(S): ' + ', ' .join(hover_over_list) +
        '\n\nPlease, press the RESET button (or ESCape) to start fresh.')

def activate_plus1(*args):
    # if csv_field_var.get() in csv_list:
    # 	mb.showwarning(title='Warning', message='The csv field "'+ csv_field_var.get() + '" is already in your selection list: '+ str(csv_list) + '.\n\nPlease, select another field.')
    # 	window.focus_force()
    # 	return
    if csv_field_var.get() != '':
        csv_list.clear()  # only 1 value is now allowed
        csv_list.append(csv_field_var.get())
        csv_hover_over_field_menu.configure(state='normal')
        csv_groupBy_field_menu.configure(state='normal')


# csv_field_menu.configure(state="disabled")
# add_field1_button.configure(state='normal')
csv_field_var.trace('w', activate_plus1)


def activate_hover_over_field_menu():
    if csv_hover_over_field_var.get() != '':
        csv_hover_over_field_menu.configure(state="normal")

# add extra group_by field
add_field3_button = tk.Button(window, text='+', width=GUI_IO_util.add_button_width, height=1, state='disabled',
                              command=lambda: activate_groupBy_field_menu())
# place widget with hover-over info
y_multiplier_integer = GUI_IO_util.placeWidget(window,GUI_IO_util.labels_x_indented_coordinate, y_multiplier_integer,
                                   add_field3_button,
                                   True, False, True, False, 90, GUI_IO_util.labels_x_indented_coordinate,
                                   "Click the + button, when available, to add another group-by field to aggregate the data")

csv_groupBy_field_lb = tk.Label(window, text='Group-by field')
y_multiplier_integer = GUI_IO_util.placeWidget(window,GUI_IO_util.statistics_csv_csv_groupBy_field_lb_pos, y_multiplier_integer,
                                               csv_groupBy_field_lb, True)

csv_groupBy_field_menu = tk.OptionMenu(window, csv_groupBy_field_var, *menu_values)
# place widget with hover-over info
y_multiplier_integer = GUI_IO_util.placeWidget(window,GUI_IO_util.statistics_csv_csv_groupBy_field_menu_pos, y_multiplier_integer,
                                   csv_groupBy_field_menu,
                                   True, False, True, False, 90, GUI_IO_util.labels_x_coordinate,
                                   "Use the dropdown menu to select the csv file field to be used to group the selected csv file field"
                                   "\nMULTIPLE GROUP-BY FIELDS CAN BE SELECTED")

# add extra hover_over field
add_field2_button = tk.Button(window, text='+', width=GUI_IO_util.add_button_width, height=1, state='disabled',
                              command=lambda: activate_hover_over_field_menu())
# place widget with hover-over info
y_multiplier_integer = GUI_IO_util.placeWidget(window,GUI_IO_util.statistics_csv_add_field2_button_pos, y_multiplier_integer,
                                   add_field2_button,
                                   True, False, True, False, 90, GUI_IO_util.open_reminders_x_coordinate,
                                   "Click the + button, when available, to add another hover-over field")

csv_hover_over_field_lb = tk.Label(window, text='Hover-over field')
y_multiplier_integer = GUI_IO_util.placeWidget(window,GUI_IO_util.statistics_csv_csv_hover_over_field_lb_pos, y_multiplier_integer,
                                               csv_hover_over_field_lb, True)

csv_hover_over_field_menu = tk.OptionMenu(window, csv_hover_over_field_var, *menu_values)
# place widget with hover-over info
y_multiplier_integer = GUI_IO_util.placeWidget(window,GUI_IO_util.statistics_csv_csv_hover_over_field_menu_pos, y_multiplier_integer,
                                   csv_hover_over_field_menu,
                                   False, False, True, False, 90, GUI_IO_util.open_reminders_x_coordinate,
                                   "Use the dropdown menu to select the csv file field to be used to display hover-over information"
                                   "\nMULTIPLE HOVER-OVER FIELDS CAN BE SELECTED"
                                   "\nTHE OPTION IS AVAILABLE FOR EXCEL CHARTS ONLY" )

# groupBy_list=[]
def activate_plus2(*args):
    if csv_hover_over_field_var.get() in hover_over_list:
        mb.showwarning(title='Warning',
                       message='The csv field "' + csv_hover_over_field_var.get() + '" is already in your selection list: ' + str(
                           hover_over_list) + '.\n\nPlease, select another field.')
        window.focus_force()
        return
    if csv_hover_over_field_var.get() != '':
        hover_over_list.append(csv_hover_over_field_var.get())
        csv_hover_over_field_menu.configure(state="disabled")
        add_field2_button.configure(state='normal')

csv_hover_over_field_var.trace('w', activate_plus2)


def activate_groupBy_field_menu():
    if csv_groupBy_field_var.get() != '':
        csv_groupBy_field_menu.configure(state="normal")


def activate_plus3(*args):
    if csv_groupBy_field_var.get() in groupBy_list:
        mb.showwarning(title='Warning',
                       message='The csv field "' + csv_groupBy_field_var.get() + '" is already in your selection list: ' + str(
                           groupBy_list) + '.\n\nPlease, select another field.')
        window.focus_force()
        return
    if csv_groupBy_field_var.get() != '':
        groupBy_list.append(csv_groupBy_field_var.get())
        csv_groupBy_field_menu.configure(state="disabled")
        add_field3_button.configure(state='normal')


csv_groupBy_field_var.trace('w', activate_plus3)


def activate_all_options(menu_values, from_csv_field_freq_var=False):
    if inputFilename.get()[-4:] == '.txt':
        # corpus_statistics_checkbox.configure(state='normal')
        all_csv_field_checkbox.configure(state='disabled')
        csv_field_checkbox.configure(state='disabled')
        # n_grams_checkbox.configure(state='normal')
        # n_grams_menu.configure(state='normal')
        # n_grams_options_menu.configure(state='normal')
    elif inputFilename.get()[-4:] == '.csv':
        all_csv_field_checkbox.configure(state='normal')
        csv_field_checkbox.configure(state='normal')
        # corpus_statistics_checkbox.configure(state='disabled')
        # n_grams_checkbox.configure(state='disabled')
        # n_grams_menu.configure(state='disabled')
        # n_grams_options_menu .configure(state='disabled')
    else:
        # corpus_statistics_checkbox.configure(state='normal')
        all_csv_field_checkbox.configure(state='normal')
        csv_field_checkbox.configure(state='normal')
        # n_grams_checkbox.configure(state='normal')
        # n_grams_menu.configure(state='disabled')
        # n_grams_options_menu.configure(state='disabled')

    # if corpus_statistics_var.get() == 1:
    #     all_csv_field_checkbox.configure(state='disabled')
    #     csv_field_checkbox.configure(state='disabled')
    #     # n_grams_checkbox.configure(state='disabled')
    #     # n_grams_menu.configure(state='disabled')
    #     # n_grams_options_menu .configure(state='disabled')

    if all_csv_stats_var.get() == 1:
        # corpus_statistics_checkbox.configure(state='disabled')
        csv_field_checkbox.configure(state='disabled')
        # n_grams_checkbox.configure(state='disabled')
        # n_grams_menu.configure(state='disabled')
        # n_grams_options_menu.configure(state='disabled')

    if csv_field_freq_var.get() == 1:
        if from_csv_field_freq_var == True:
            if menu_values == ['']:  # first time through
                changed_filename()
        # corpus_statistics_checkbox.configure(state='disabled')
        all_csv_field_checkbox.configure(state='disabled')
        # n_grams_checkbox.configure(state='disabled')
        # n_grams_menu.configure(state='disabled')
        # n_grams_options_menu .configure(state='disabled')
        reset_csv_button.configure(state='normal')
        show_csv_button.configure(state='normal')
        csv_field_menu.configure(state='normal')
        csv_hover_over_field_menu.configure(state='disabled')
        csv_groupBy_field_menu.configure(state='disabled')
    else:
        csv_field_var.set('')
        reset_csv_button.configure(state='normal')
        show_csv_button.configure(state='normal')
        csv_hover_over_field_var.set('')
        csv_field_menu.configure(state='disabled')
        csv_hover_over_field_menu.configure(state='disabled')
        csv_groupBy_field_menu.configure(state='disabled')

    # if n_grams_var.get() == 1:
    #     # corpus_statistics_checkbox.configure(state='disabled')
    #     all_csv_field_checkbox.configure(state='disabled')
    #     csv_field_checkbox.configure(state='disabled')
    #     # n_grams_menu.configure(state='normal')
        # n_grams_options_menu.configure(state='normal')
    # else:
    #     n_grams_menu.configure(state='disabled')
    #     n_grams_options_menu.configure(state='disabled')

# corpus_statistics_var.trace('w', lambda x, y, z: activate_all_options(menu_values))
all_csv_stats_var.trace('w', lambda x, y, z: activate_all_options(menu_values))
csv_field_freq_var.trace('w', lambda x, y, z: activate_all_options(menu_values, True))
# n_grams_var.trace('w', lambda x, y, z: activate_all_options(menu_values))

activate_all_options(menu_values)


# the first call is placed at the buttom of this script so that all widgets would have been dispayed
def changed_filename(*args):
    clear('Escape')
    global menu_values
    if inputFilename.get()[-4:] == '.csv':
        # continue only if the input file is csv
        menu_values = IO_csv_util.get_csvfile_headers(inputFilename.get())
        m = csv_field_menu["menu"]
        m1 = csv_hover_over_field_menu["menu"]
        m2 = csv_groupBy_field_menu["menu"]
        m.delete(0, "end")
        m1.delete(0, "end")
        m2.delete(0, "end")
        for s in menu_values:
            m.add_command(label=s, command=lambda value=s: csv_field_var.set(value))
            m1.add_command(label=s, command=lambda value=s: csv_hover_over_field_var.set(value))
            m2.add_command(label=s, command=lambda value=s: csv_groupBy_field_var.set(value))
    activate_all_options(menu_values)

# at the bottom of the script after laying out the GUI
# inputFilename.trace('w',changed_filename)
# changed_filename()

videos_lookup = {'No videos available':''}
videos_options='No videos available'

TIPS_lookup = {'csv files - Problems & solutions':'TIPS_NLP_csv files - Problems & solutions.pdf',
               'Statistical tools in the NLP Suite': 'TIPS_NLP_Statistical tools.pdf',
               'Statistical descriptive measures': "TIPS_NLP_Statistical measures.pdf",
               'Lemmas & stopwords':'TIPS_NLP_NLP Basic Language.pdf',
               'Style measures': 'TIPS_NLP_Style measures.pdf',
               # 'N-Grams (word & character)': "TIPS_NLP_Ngrams (word & character).pdf",
               # 'NLP Ngram and Word Co-Occurrence Viewer': "TIPS_NLP_NLP Ngram and Co-Occurrence Viewer.pdf",
               # 'Google Ngram Viewer': 'TIPS_NLP_Ngram Google Ngram Viewer.pdf',
               'Excel smoothing data series': 'TIPS_NLP_Excel smoothing data series.pdf'}
TIPS_options = 'Statistical tools in the NLP Suite', 'Statistical descriptive measures', 'csv files - Problems & solutions', 'Lemmas & stopwords', 'Excel smoothing data series'


# add all the lines to the end to every special GUI
# change the last item (message displayed) of each line of the function y_multiplier_integer = help_buttons
# any special message (e.g., msg_anyFile stored in GUI_IO_util) will have to be prefixed by GUI_IO_util.
def help_buttons(window, help_button_x_coordinate, y_multiplier_integer):
    if not IO_setup_display_brief:
        y_multiplier_integer = GUI_IO_util.place_help_button(window, help_button_x_coordinate,y_multiplier_integer,"NLP Suite Help", GUI_IO_util.msg_txtFile)
        y_multiplier_integer = GUI_IO_util.place_help_button(window, help_button_x_coordinate,y_multiplier_integer,"NLP Suite Help",
                                      GUI_IO_util.msg_corpusData)
        y_multiplier_integer = GUI_IO_util.place_help_button(window, help_button_x_coordinate,y_multiplier_integer,"NLP Suite Help",
                                      GUI_IO_util.msg_outputDirectory)
    else:
        y_multiplier_integer = GUI_IO_util.place_help_button(window, help_button_x_coordinate,y_multiplier_integer,"NLP Suite Help",
                                      GUI_IO_util.msg_IO_setup)

    y_multiplier_integer = GUI_IO_util.place_help_button(window, help_button_x_coordinate, y_multiplier_integer, "NLP Suite Help",
                                  'Please, tick the checkbox if you wish to compute basic statistics on all the numeric fields of a csv file.\n\nIn INPUT the script expects a csv file.\n\nIn OUTPUT, the script generates a csv file of statistics for each numeric field in the input csv file: Count, Mean, Mode, Median, Standard deviation, Minimum, Maximum, Skewness, Kurtosis, 25% quantile, 50% quantile; 75% quantile.')
    y_multiplier_integer = GUI_IO_util.place_help_button(window, help_button_x_coordinate, y_multiplier_integer, "NLP Suite Help",
                                  'Please, tick the checkbox if you wish to compute the frequency of a specific field of a csv file. ONLY ONE FIELD CAN BE CURRENTLY SELECTED. But multiple group-by fields and hover-over fields can be selected.\n\nYou can select to group the frequencies by specific field(s) and/or have hover-over field(s) if you wish to display information in an Excel chart.\n\nIn INPUT the script expects a csv file.\n\nIn OUTPUT, the script generates a csv file of frequencies for the selected field.')
    y_multiplier_integer = GUI_IO_util.place_help_button(window, help_button_x_coordinate, y_multiplier_integer, "NLP Suite Help",
                                  'Please, using the dropdown menu, for the selected csv field, selected  one or more group-by fields (e.g., compute the frequencies of POSTAG values by DocumentID in a CoNLL table displaying both words and lemmas in hover over.) \n\nMultiple fields can be selected by pressing the + button.')
    y_multiplier_integer = GUI_IO_util.place_help_button(window, help_button_x_coordinate, y_multiplier_integer, "NLP Suite Help",
                                  GUI_IO_util.msg_openOutputFiles)
    return y_multiplier_integer -1
y_multiplier_integer = help_buttons(window, GUI_IO_util.help_button_x_coordinate, 0)

# change the value of the readMe_message
readMe_message = "The Python 3 scripts provide ways of analyzing csv files and obtain basic descriptive statistics."
readMe_command = lambda: GUI_IO_util.display_help_button_info("NLP Suite Help", readMe_message)
GUI_util.GUI_bottom(config_filename, config_input_output_numeric_options, y_multiplier_integer, readMe_command, videos_lookup, videos_options, TIPS_lookup, TIPS_options, IO_setup_display_brief, scriptName)

changed_filename()
inputFilename.trace('w', changed_filename)

GUI_util.window.mainloop()

