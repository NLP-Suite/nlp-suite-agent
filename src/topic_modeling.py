import topic_modeling_bert_util
import topic_modeling_mallet_util
#import topic_modeling_gensim_util
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

def run_topic_modeling(inputDir, outputDir, openOutputFiles, chartPackage, dataTransformation, num_topics,
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

    # Initialize filesToOpen list
    filesToOpen = []

    
    labels = []
    if BERT_var:
        labels.append('BERTopic')
    if MALLET_var:
        labels.append('MALLET')
    if Gensim_var:
        labels.append('Gensim')

    if not labels:
        print('Warning: No options selected. Please select at least one of the available options (BERTopic, MALLET, or Gensim) and try again.')
        return

    label = '-'.join(labels)

    # Check internet availability
    if not IO_internet_util.check_internet_availability_warning(label + ' Topic Modeling'):
        return

    if num_topics == 20:
        reminders_util.checkReminder(scriptName, reminders_util.title_options_topic_modelling_number_of_topics,
                                     reminders_util.message_topic_modelling_number_of_topics, True)

    # Create a subdirectory of the output directory
    outputDir = IO_files_util.make_output_subdirectory('', inputDir, outputDir, label='TM-' + label, silent=True)
    if outputDir == '':
        return

    # Run BERTopic
    if BERT_var:
        
        bert_files = topic_modeling_bert_util.run_BERTopic(inputDir, outputDir, split_docs_var)
        # if bert_files:
        #     filesToOpen.extend(bert_files)
    
    # Run MALLET
    if MALLET_var:

        mallet_files = topic_modeling_mallet_util.run_MALLET(inputDir, outputDir, chartPackage, dataTransformation,
                                                             optimize_intervals_var, num_topics)
        # if mallet_files:
        #     filesToOpen.extend(mallet_files)
    
    # Run Gensim
    #if Gensim_var:
        # gensim_files = topic_modeling_gensim_util.run_Gensim(inputDir, outputDir, num_topics,
        #                                                      remove_stopwords_var, lemmatize_var, nounsOnly_var,
        #                                                      Gensim_MALLET_var, chartPackage, dataTransformation)
        # if gensim_files:
        #     filesToOpen.extend(gensim_files)
    

    return #filesToOpen
