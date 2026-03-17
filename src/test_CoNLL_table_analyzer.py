# test_topic_modeling.py
import os
from CoNLL_table_analyzer_main import run_CoNLL_table_analyzer

# Replace with your input and output directories
inputDir = "/Users/aidenamaya/nlp-suite/csvInput"
outputDir = '/Users/aidenamaya/nlp-suite/output'
inputFilename = inputDir 
# Ensure the directories exist
os.makedirs(inputDir, exist_ok=True)
os.makedirs(outputDir, exist_ok=True)

# Set parameters
openOutputFiles = 1
chartPackage='Excel'
dataTransformation=''
searchedCoNLLField='FORM' #LEMMA
searchField_kw='e.g.: father'
postag=''
deprel=''
co_postag=''
co_deprel=''
Begin_K_sent_var=0
End_K_sent_var=0

postag_var = False
all_analyses_var = True
all_analyses = '*'
search_token_var = False
WordNet_var = False
compute_sentence_var = False
k_sentences_var = False

# Run the topic modeling function
# def run(inputFilename, inputDir, outputDir, openOutputFiles, chartPackage, dataTransformation,
#         searchedCoNLLField, searchField_kw, postag, deprel, co_postag, co_deprel, Begin_K_sent_var, End_K_sent_var):
run_CoNLL_table_analyzer(inputFilename, 
                         inputDir, 
                         outputDir, 
                         openOutputFiles, 
                         chartPackage, 
                         dataTransformation,
        searchedCoNLLField, 
        searchField_kw, 
        postag_var, 
        deprel,
        co_postag, 
        co_deprel, 
        Begin_K_sent_var,
        End_K_sent_var,
        all_analyses_var,
        all_analyses, 
        search_token_var,
        WordNet_var,
        compute_sentence_var,
        k_sentences_var)