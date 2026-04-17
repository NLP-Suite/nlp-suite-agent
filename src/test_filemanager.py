import os
from file_manager_main import run_file_manager


inputDir = r'C:\Users\chang\nlp-suite\input'
outputDir = r'C:\Users\chang\nlp-suite\output'

# Ensure the directories exist
os.makedirs(inputDir, exist_ok=True)
os.makedirs(outputDir, exist_ok=True)

run_file_manager(
    inputDir=inputDir,
    outputDir=outputDir,

    chartPackage='Excel',
    dataTransformation='No transformation',

    selectedCsvFile_var='',
    selectedCsvFile_colName='',
    utf8_var=False,
    ASCII_var=False,

    list_var=True,
    rename_var=False,
    copy_var=False,
    move_var=False,
    delete_var=False,
    count_file_manager_var=False,
    split_var=False,

    rename_new_entry='',
    by_file_type_var=True,
    file_type_menu_var='txt',

    by_creation_date_var=False,
    by_author_var=False,
    before_date_var='',
    after_date_var='',

    by_prefix_var=False,
    by_substring_var=False,
    string_entry_var='',

    by_foldername_var=False,
    folder_character_separator_var='',

    by_embedded_items_var=False,
    comparison_var='=',
    number_of_items_var=0,
    embedded_item_character_value_var='',
    include_exclude_var='',

    character_count_file_manager_var=False,
    character_entry_var='',

    include_subdir_var=False,

    fileName_embeds_date=False,
    date_format='mm-dd-yyyy',
    date_separator='-',
    date_position=0
)