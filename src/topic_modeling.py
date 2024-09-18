import GUI_IO_util
import topic_modeling_bert_util
import topic_modeling_mallet_util
import topic_modeling_gensim_util
import IO_internet_util
import reminders_util
import IO_files_util

# RUN section ______________________________________________________________________________________________________________________________________________________

"""
# get CLAs of input dir and output file name
parser = argparse.ArgumentParser()
parser.add_argument("-i", "--inputDir", help="Directs the input to your text directory")
parser.add_argument("-o", "--outputFilename", help="Directs the output to a file name and path of your choice, MUST end in .html")
args = parser.parse_args()
"""


def run_topic_modelling(inputDir, outputDir, openOutputFiles, chartPackage, dataTransformation, num_topics,
        BERT_var,
        split_docs_var,
        MALLET_var,
        optimize_intervals_var,
        Gensim_var,
        remove_stopwords_var, lemmatize_var, nounsOnly_var, Gensim_MALLET_var):

    print(inputDir, outputDir, openOutputFiles, chartPackage, dataTransformation, num_topics,
        BERT_var,
        split_docs_var,
        MALLET_var,
        optimize_intervals_var,
        Gensim_var,
        remove_stopwords_var, lemmatize_var, nounsOnly_var, Gensim_MALLET_var)
    
    scriptName = "topic_modeling.py"
    
    if not BERT_var and not MALLET_var and not Gensim_var:
        print(title='Warning', message='There are no options selected.\n\nPlease, select one of the available options (MALLET or Gensim) and try again.')
        return

    
    if BERT_var:
        label = 'BERTopic'
    if MALLET_var:
        label = 'MALLET'
    if Gensim_var:
        label = 'Gensim'

    if not IO_internet_util.check_internet_availability_warning(label + ' Topic Modeling'):
        return

    if num_topics==20:
        reminders_util.checkReminder(scriptName, reminders_util.title_options_topic_modelling_number_of_topics,
                                     reminders_util.message_topic_modelling_number_of_topics, True)

    # create a subdirectory of the output directory
    outputDir = IO_files_util.make_output_subdirectory('', inputDir, outputDir, label='TM-'+label,
                                                       silent=True)
    if outputDir == '':
        return
    if BERT_var:
        topic_modeling_bert_util.run_BERTopic(inputDir, outputDir, openOutputFiles, split_docs_var)
    if MALLET_var:
        topic_modeling_mallet_util.run_MALLET(inputDir, outputDir, openOutputFiles, chartPackage, dataTransformation,
                                                     optimize_intervals_var, num_topics)
    if Gensim_var:
        topic_modeling_gensim_util.run_Gensim(None, inputDir, outputDir, GUI_IO_util.config_filename, num_topics, #GUI_UTIL.window <- None
                                          remove_stopwords_var, lemmatize_var, nounsOnly_var, Gensim_MALLET_var, openOutputFiles, chartPackage, dataTransformation)
