# test_topic_modeling.py
import os
from topic_modeling import run_topic_modeling

# Replace with your input and output directories
inputDir = 'C:/Users/sherry/OneDrive/Desktop/QTM446W/Input'
outputDir = 'C:/Users/sherry/OneDrive/Desktop/QTM446W/Ouput'

# Ensure the directories exist
os.makedirs(inputDir, exist_ok=True)
os.makedirs(outputDir, exist_ok=True)

# Set parameters
openOutputFiles = 1
chartPackage='Excel',
dataTransformation='',
num_topics = 10
BERT_var = True
split_docs_var = True
#MALLET_var = True
MALLET_var = False
optimize_intervals_var = 0
Gensim_var = False
remove_stopwords_var = False
lemmatize_var = False
nounsOnly_var = False
Gensim_MALLET_var = False



# Run the topic modeling function
run_topic_modeling(
    inputDir=inputDir,
    outputDir=outputDir,
    openOutputFiles=openOutputFiles,
    chartPackage=chartPackage,
    dataTransformation=dataTransformation,
    num_topics=num_topics,
    BERT_var=BERT_var,
    split_docs_var=split_docs_var,
    MALLET_var=MALLET_var,
    optimize_intervals_var=optimize_intervals_var,
    Gensim_var=Gensim_var,
    remove_stopwords_var=remove_stopwords_var,
    lemmatize_var=lemmatize_var,
    nounsOnly_var=nounsOnly_var,
    Gensim_MALLET_var=Gensim_MALLET_var
)
