"""
Python 3 script
author: Roberto Franzosi, May 2019
"""

import GUI_IO_util
import os
import subprocess

def check_lib_stopwords():
    lib_filename="stopwords.txt"
    stopwords_libPath = GUI_IO_util.libPath + os.sep + "wordLists"
    stopwords_file_withPath=stopwords_libPath+os.sep+lib_filename
    if os.path.isfile(stopwords_file_withPath)!=True:
        print("lib warning", "The lib file "+stopwords_file_withPath+" could not be found in your expected lib subdirectory " + str(stopwords_libPath))
        check_lib_stopwords=""
    else:
        check_lib_stopwords=stopwords_file_withPath
    return check_lib_stopwords

# libfile MUST have a path, since lib files are now stored in subdirs of lib 
# it appears that it is never called
def get_lib(libfile):
    if os.path.isfile(libfile)==False:
        libFile_Exists=False
    else:
        libFile_Exists=True
        subprocess.Popen([libfile],shell=True)
    return libFile_Exists

# libfile MUST have a path, since lib files are now stored in subdirs of lib 
# called by sentiment/concreteness scripts
def checklibFile(libfile,script):
    if os.path.isfile(libfile)==False:
        print('File not found', 'The script ' + script + ' expects the file\n\n' + libfile + '\n\nin the directory\n\n' + GUI_IO_util.sentiment_libPath + '\n\na subdirectory of the directory where the NLP script is stored.\n\nPlease, check your lib directory and try again.')
        return False
    return True

def checkLibLicense(libfile):
    if os.path.isfile(GUI_IO_util.libPath + os.sep + libfile)==False:
        print('License agreement file not found', 'The NLP Suite expects a license agreement file ' + libfile + ' in a directory "lib" expected to be a subdirectory of the directory where the NLP Suite is stored.\n\nPlease, check your lib subdirectory and license agreement file and try again.')
        return False
    return True

def checklibDir():
    lib_dir_exists = True
    if not os.path.isdir('lib'+os.sep):
        print("lib Warning", "The lib directory " + GUI_IO_util.libPath + " could not be found in your expected lib subdirectory of " + str(
            GUI_IO_util.NLPPath) + "\n\nRoutine will exit.")
        lib_dir_exists = False
    return lib_dir_exists