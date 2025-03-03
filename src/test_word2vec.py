# test_topic_modeling.py
import os
from word2vec import run_word2vec

# Replace with your input and output directories
inputDir = '/Users/aidenamaya/nlp-suite/input'
outputDir = '/Users/aidenamaya/nlp-suite/output'

# Ensure the directories exist
os.makedirs(inputDir, exist_ok=True)
os.makedirs(outputDir, exist_ok=True)

# Set parameters
inputFilename = ""
chartPackage='Excel'
dataTransformation=''
remove_stopwords_var = True
lemmatize_var = True
WSI_var = True
BERT_var = False
Gensim_var = False
sg_menu_var = False
vector_size_var = 100
window_var = 5
min_count_var = 5
vis_menu_var = "Plot word vectors"
dim_menu_var = "2D"
compute_distances_var = True
top_words_var = 200
keywords_var = False
keywordInput = "harry, magic"
range4 = 4
range6 = 6
range20 = 10 
ngramsDropDown = "3-grams (trigrams)"
#Vairbalke names for training architecute for gensim: Skip-Gram , CBOW
# Run the topic modeling function
run_word2vec(inputFilename, inputDir, outputDir, chartPackage, dataTransformation,
                 remove_stopwords_var, lemmatize_var, WSI_var,
                 BERT_var, Gensim_var,
                 sg_menu_var, vector_size_var, window_var, min_count_var,
                 vis_menu_var, dim_menu_var, compute_distances_var, top_words_var, keywords_var,
                 keywordInput, range4, range6, range20, ngramsDropDown)
