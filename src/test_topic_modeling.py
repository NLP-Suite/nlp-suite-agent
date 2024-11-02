# test_topic_modeling.py
import os
from topic_modeling import run_topic_modeling

# Replace with your input and output directories
inputDir = '/Users/is2ac/nlp-suite/input'
outputDir = '/Users/is2ac/nlp-suite/output'

# Ensure the directories exist
os.makedirs(inputDir, exist_ok=True)
os.makedirs(outputDir, exist_ok=True)

# Set parameters
chartPackage='Excel',
dataTransformation='',
num_topics = 10
#BERT_var = True
BERT_var = False
split_docs_var = True
MALLET_var = True
#MALLET_var = False
optimize_intervals_var = 0
Gensim_var = True
remove_stopwords_var = False
lemmatize_var = True
nounsOnly_var = True
Gensim_MALLET_var = False



# Run the topic modeling function
run_topic_modeling(
    inputDir=inputDir,
    outputDir=outputDir,
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
